#!/home/kabil/.anaconda3/envs/r-env/bin/Rscript

# Useful R Functions for data analysis

# Load Necessary Packages
pkgs <- c("tidyverse", "OlinkAnalyze", "lubridate", "survival", "survminer", "gridExtra", "ggpubr",
			"haven", "readxl", "parallel", "xlsx", "ggcorrplot", "ggpmisc", "ggdendro",
			"grid", "ComplexHeatmap", "RColorBrewer", "ggvenn", "gganimate", "ggVennDiagram", "readxl",
			"patchwork")
pkgs <- lapply(pkgs, require, character.only=TRUE)

# Try making environment for functions
# .env <- new.env()
# .env$s <- base::summary
# attach(.env)
# print.functions() <- function(){cat() cat() cat()}}


# Wrapper for read.csv that returns a tibble
readCSV <- function(file) {read.csv(file) %>% tibble()}

# Remove all variables
rmA <- function() rm(list=ls())

# Generate frequency distribution plots
freqPlot <- function (data, markers = NULL) {
	# Use only specified markers
	if (!is.null(markers)) {data <- data[markers]}
	# Calculate K-Means Cluster Centers
	cc <- sapply(data, function(M) sort(kmeans(M$Levels, 2)$centers[,]))
	# Create figures
	fd <- lapply(X = seq_along(data), function(i) {
		ggplot(data[[i]], aes(Levels)) + 
			geom_density(fill = "red", color = "red", alpha = 0.1) +
			stat_central_tendency(type = "mean", linetype = "dashed", color = "red") +
			ggtitle(names(data[i])) +
			geom_vline(aes(xintercept = cc[1, names(data[i])])) +
			geom_vline(aes(xintercept = cc[2, names(data[i])])) +
			theme(plot.title = element_text(hjust = 0.5, size = 10))
	})
	return(ggarrange(plotlist = fd))
}

# Kaplan Meier Survival Curve Plotting
kaplanMeier <- function (
				data, 
				time = "Hstay", 
				event,
				markers = NULL,
				titles = "",
				xlabs = "Hospital Stay (Days)",
				ylabs = "",
				fnm.str = NULL) {
	# Use only specified markers
	if (!is.null(markers)) {data <- data[markers]}
	# Fit curves
	p <- lapply(X = seq_along(data), function(i) {
		df <- data[[i]] %>% select(all_of(time), all_of(event), Level) %>% setNames(c("Time", "Event", "Level"))
		ft <- survfit(Surv(time = Time, event = Event) ~ Level, df)
		if (isTRUE(surv_pvalue(fit=ft, data=df)[["pval"]] <= 0.05)) {
			km <- ggsurvplot(
					fit = ft, 
					data = df,
					break.time.by = 2,
					xlim = c(0, 28),
					pval = TRUE,
					xlab = xlabs,
					ylab = ylabs,
					subtitle = names(data[i]) %>% gsub("\\.", "-", .),
					legend = "bottom",
					legend.labs = levels(factor((df$Level))),
					risk.table = TRUE,
					risk.table.y.text = FALSE,
					ggtheme = theme_pubr())
			km$plot <- km$plot + theme(
									plot.title = element_text(hjust = 0.5, size = 15), 
									plot.subtitle = element_text(hjust = 0.5, size = 15), 
									legend.text = element_text(size = 15), 
									legend.key.size = unit(1.2, "cm"),
									legend.title = element_blank())
			km$table <- km$table + theme(plot.title = element_text(hjust = 0.5))
			# Save figures if necessary
			if (!is.null(fnm.str)) {ggsave(str_c("fig/", fnm.str, names(data[i]), ".png"), print(km), width = 6, height = 7)}
			return(km)
		}
		#if (surv_pvalue(fit=ft, data=df)[["pval"]] <= 0.05) {return(km)}
	})
	return(p)
}


# Formatting NPX data for databanks
formatNPX <- function(npx, fnm, shtnm, mode, spss = FALSE) {
	if (mode == "pivot") {
		tbls <- lapply(X = split(npx, npx$Assay), FUN = function(Assay) {
			tbl <- lapply(X = split(Assay, Assay$Time), FUN = function(A.Time) {
					tibble(A.Time$PICOBS, A.Time$NPX - A.Time$Adj_factor) %>% 
					setNames(., c("PICOBS", str_c(unique(A.Time$Assay), unique(A.Time$Time), sep = "-"))) %>%
					full_join(data.frame(PICOBS = 1:106), ., by = "PICOBS")
				})
			# Join Tables for each Time
			tbl <- tbl %>% reduce(full_join, by = "PICOBS") %>% 
				aggregate(., list(.$PICOBS), mean) %>% arrange(PICOBS) %>% 
				group_by(PICOBS) %>% select(-Group.1)
			# Stack columns
			df <- data.frame(tbl[1], stack(tbl[-1])) %>%
					add_column(Time = str_extract(.$ind, "[tSH]\\d")) %>% 
					add_column(Assay = unique(Assay$Assay)) %>%
					select(PICOBS, Time, NPX = values)
			#setNames(c("PICOBS", str_c("Assay", unique(Assay$Assay), sep="."), str_c("Time", unique(Assay$Assay), sep="."), str_c("NPX", unique(Assay$Assay), sep=".")))
			if (isTRUE(spss)) {
				colnames(df) <- c("PICOBS", str_c("Time", unique(Assay$Assay), sep="."), str_c("NPX", unique(Assay$Assay), sep="."))
				return(df)
			} else {return(df)}
		})
		# Create and Exprot Excel Workbook
		wb <- createWorkbook("xlsx")
		style.Colnames <- CellStyle(wb) + Alignment(horizontal = "ALIGN_CENTER") + 
			Border(color = "Black", 
				position = c("TOP", "BOTTOM", "LEFT", "RIGHT"), 
				pen = rep("BORDER_THIN", 4))
		sht <- createSheet(wb, sheetName = shtnm)
		row <- createRow(sht, rowIndex = 2)
		for (i in 1:length(tbls)) {
			addMergedRegion(sheet = sht, startRow = 2, endRow = 2, startColumn = 3+4*(i-1), endColumn = 4+4*(i-1))
			cell <- createCell(row, colIndex = 3 + 4*(i-1))
			ttl <- mapply(setCellValue, cell[,1], names(tbls[i]))
			addDataFrame(x = tbls[[i]], sheet = sht,
				row.names = FALSE, colnamesStyle = style.Colnames,
				startRow = 3, startColumn = 2 + 4*(i-1))
		}
		saveWorkbook(wb, fnm)
	} else if (mode == "format") {
		tbls <- lapply(X = split(npx, npx$Assay), FUN = function(Assay) {
			tbl <- lapply(X = split(Assay, Assay$Time), FUN = function(A.Time) {
					tibble(A.Time$PICOBS, A.Time$NPX - A.Time$Adj_factor) %>% 
					setNames(., c("PICOBS", str_c(unique(A.Time$Assay), unique(A.Time$Time), sep = "-"))) %>%
					full_join(data.frame(PICOBS = 1:106), ., by = "PICOBS")
				})
			# Join Tables for each Time
			tbl <- tbl %>% reduce(full_join, by = "PICOBS") %>% 
				aggregate(., list(.$PICOBS), mean) %>% arrange(PICOBS) %>% 
				group_by(PICOBS) %>% select(-Group.1) %>% as.data.frame()
			return(tbl)
		})
		# Create and Exprot Excel Workbook
		wb <- createWorkbook("xlsx")
		style.Colnames <- CellStyle(wb) + Alignment(horizontal = "ALIGN_CENTER") + 
			Border(color = "Black", 
				position = c("TOP", "BOTTOM", "LEFT", "RIGHT"), 
				pen = rep("BORDER_THIN", 4))
		sht <- createSheet(wb, sheetName = shtnm)
		row <- createRow(sht, rowIndex = 2)
		for (i in 1:length(tbls)) {
			addMergedRegion(sheet = sht, startRow = 2, endRow = 2, startColumn = 2+6*(i-1), endColumn = 5+6*(i-1))
			cell <- createCell(row, colIndex = 3 + 6*(i-1))
			ttl <- mapply(setCellValue, cell[,1], names(tbls[i]))
			addDataFrame(x = tbls[[i]], sheet = sht,
				row.names = FALSE, colnamesStyle = style.Colnames,
				startRow = 3, startColumn = 2 + 6*(i-1))
		}
		saveWorkbook(wb, fnm)
	}
}

# Format Elisa Data for Databanks
pivotElisa <- function(df, fnm) {
	tbls <- mclapply(split(df, df$Marker), mc.cores = detectCores(), function(M) {
		tbl <- mclapply(split(M, M$Time), mc.cores = detectCores(), function(M.T) {M.T %>% select(PICOBS, Levels) %>% setNames(c("PICOBS", str_c(unique(M.T$Marker), "-", unique(M.T$Time))))})
		tbl <- tbl %>% reduce(full_join, by = "PICOBS") %>% full_join(., data.frame(PICOBS = 1:106), by="PICOBS") %>% arrange(PICOBS)
		data.frame(tbl[1], stack(tbl[-1])) %>%
			add_column(Time = str_extract(.$ind, "[TSH]\\d$")) %>%
			add_column(Assay = unique(M$Marker)) %>%
			select(PICOBS, Time, NPX = values) %>%
			setNames(c("PICOBS", str_c("Time", unique(M$Marker), sep="."), str_c("NPX", unique(M$Marker), sep=".")))
	})
	# Create & Export Excel Workbook
	wb <- createWorkbook("xlsx")
	style.Colnames <- CellStyle(wb) + Alignment(horizontal = "ALIGN_CENTER") + Border(color = "Black", position = c("TOP", "BOTTOM", "LEFT", "RIGHT"), pen = rep("BORDER_THIN", 4))
	sht <- createSheet(wb, sheetName = "Data")
	row <- createRow(sht, rowIndex = 2)
	for (i in 1:length(tbls)) {
		addMergedRegion(sheet = sht, startRow = 2, endRow = 2, startColumn = 3+3*(i-1), endColumn = 4+3*(i-1))
		cell <- createCell(row, colIndex = 3 + 3*(i-1))
		ttl <- mapply(setCellValue, cell[,1], names(tbls[i]))
		addDataFrame(x = tbls[[i]], sheet = sht, row.names = FALSE, colnamesStyle = style.Colnames, startRow = 3, startColumn = 2 + 3*(i-1))
	}
	saveWorkbook(wb, fnm)
}

# Return percentage of true values
pctTRUE <- function(bool.mask) {length(which(bool.mask)) / length(bool.mask) * 100}

# Vectorized pctTRUE
pctTRUEv <- function(bool.masks) {apply(bool.masks, 2, function(x) str_c(round(length(which(x)) / length(x) * 100, 2), "%"))}

# Create Correlation Line Graphs
ggcorrelate <- function(df, save=FALSE) {
	# Create Figure
	plt <- ggplot(data = df, aes(x = NPX.U, y = NPX.B)) + geom_point() + geom_smooth(method = "lm") +
			ggtitle(unique(df$Assay)) + ylab("Blood") + xlab("Urine") +
			stat_cor(method="pearson") +
			theme_classic() +
			theme(plot.title = element_text(hjust = 0.5, size = 20), 
				axis.title = element_text(size = 15))
	# Save File If Necessary
	if (isTRUE(save)) {ggsave(sprintf("fig/0522_BU_Corr_%s.png", unique(df$Assay) %>% gsub("/", ".", .)), plt, width=7, height=7)}
	# Return figure
	return(plt)
}

# Save figure
figSave <- function (fig, fnm, w=1080, h=720) {
	png(str_c("fig/", fnm), width = w, height = h)
	print(fig)
	dev.off()
}

# Function for Creating Heatmaps
HeatMap <- function (df, ID, title="", grp.var=NULL, annot.var=NULL, fnm=NULL, scale="none") {
	# Create Color Palette
	col <- colorRampPalette(RColorBrewer::brewer.pal(11, "RdBu")[11:1])(2560)
	
	# Create Heatmaps
	colRng <- ncol(pivot_wider(df, names_from="Assay", values_from="NPX")) - 91
	if (!is.null(grp.var)) {
		# If a grouping variable was provided, create a grouped matrix and 
		# order the groups by hierarchical clustering
		mat <- lapply(split(df, df[grp.var]), function(group) {
			m <- pivot_wider(group, names_from="Assay", values_from="NPX") %>% ungroup() %>% select(all_of(ID), all_of(colRng):ncol(.)) %>% as.data.frame() %>% column_to_rownames(., all_of(ID)) %>% as.matrix()
			m <- m[order.dendrogram(as.dendrogram(hclust(dist(m)))), ]
			return(m)
		}) %>% reduce(., rbind)
		row.clust = FALSE
		row.annotation <- as.data.frame(unique(select(df, all_of(ID), all_of(grp.var)))) %>% arrange(eval(parse(text=grp.var))) %>% column_to_rownames(all_of(ID))
		row.annotation <- row.annotation[match(rownames(mat), rownames(row.annotation)), , drop=FALSE]
		# Specify Row Annotation Colors (RColorBrewer: Set 1)
		row.colors <- list(category = brewer.pal(9, "Set1")[1:nrow(unique(df[grp.var]))]) %>% setNames(grp.var)
		names(row.colors[[1]]) <- levels(df[[grp.var]])
		# Generate Heatmap
		hm <- pheatmap(mat, main = title, annotation_row = row.annotation, show_rownames = FALSE,
				color = col, border_color = NA, scale = scale, cluster_rows = row.clust,
				annotation_colors = row.colors)
	} else if (!is.null(annot.var)) {
		mat <- pivot_wider(df, names_from = "Assay", values_from = "NPX") %>% ungroup() %>% select(all_of(ID), all_of(colRng):ncol(.)) %>% as.data.frame() %>% column_to_rownames(., all_of(ID)) %>% as.matrix()
		row.annotation <- as.data.frame(unique(select(df, all_of(ID), all_of(annot.var)))) %>% arrange(eval(parse(text=annot.var))) %>% column_to_rownames(all_of(ID))
		row.colors <- list(category = brewer.pal(9, "Set1")[1:nrow(unique(df[annot.var]))]) %>% setNames(annot.var)
		names(row.colors[[1]]) <- levels(df[[annot.var]])
		hm <- pheatmap(mat, main = title, annotation_row = row.annotation, show_rownames = FALSE,
						color = col, border_color = NA, scale = scale, cluster_rows = TRUE,
						annotation_colors = row.colors) %>% suppressWarnings()
	} else {
		mat <- pivot_wider(df, names_from = "Assay", values_from = "NPX") %>% ungroup() %>% select(all_of(ID), all_of(colRng):ncol(.)) %>% as.data.frame() %>% column_to_rownames(., all_of(ID)) %>% as.matrix()
		hm <- pheatmap(mat, main = title, show_rownames = FALSE, color = col, border_color = NA,
				scale = scale, cluster_rows=TRUE)
	}
	if (!is.null(fnm)) figSave(hm, fnm, w=1080, h=720)
	return(hm)
}

myVolcano <- function (npx, variable, title, xlab, fnm=NULL) {
	ttest_results <- olink_ttest(df = npx, variable = variable)
	ttest_sign <- ttest_results %>% head(n=10) %>% pull(OlinkID)
	vp <- olink_volcano_plot(p.val_tbl = ttest_results, olinkid_list = ttest_sign) +
		ggtitle(title) + xlab(xlab)  +
		theme(plot.title = element_text(hjust = 0.5, size = 20),
			axis.title = element_text(size = 15),
			legend.title = element_text(size = 15), 
			legend.text = element_text(size = 12))
	if (!is.null(fnm)) figSave(vp, fnm, w=540, h=720)
	return(vp)
}

BoxPlot <- function(Assay, title) {
	ggplot(Assay, aes(x=Time, NPX, color=Time, fill=Time)) + 
		scale_color_brewer(palette="Dark2") + 
		scale_fill_brewer(palette="Dark2") +
		geom_boxplot(alpha=0.7) +
		ggtitle(title) +
		theme_pubr() +
		theme(plot.title=element_text(hjust=0.5))
}

MarkerVenn <- function (x, title = "", subtitle = "", set_size = 7, label_size = 5) {
	# Create Data for Figure
	venn <- Venn(x)
	data <- process_data(venn)
	n <- nrow(data@region)

	# Create Labels
	region_label <- filter(data@region, .data$component == "region") %>%
					mutate(percent = paste(round(.data$count*100/sum(.data$count)),"%", sep=""), 
					  		both = paste(.data$count,paste0("(",.data$percent,")"),sep = "\n"))
	# Create Figure
	ggplot()+
		geom_sf(aes_string(fill="name"), data = data@region, show.legend = F) +
		geom_sf(data = data@setEdge, show.legend = F, color="black", 
			lty = "solid", size = 0.5) +
		geom_sf_text(aes_string(label = "name"), data = data@setLabel,
				size = set_size, color = "black") +
		scale_fill_manual(values = colorRampPalette(brewer.pal(8, "Pastel1"))(n)) +
		geom_sf_label(aes_string(label="both"), data = region_label,
					alpha=0, color = "black",
					size = label_size, lineheight = 0.85, label.size = NA) +
		ggtitle(title, subtitle = subtitle) +
		theme_void() +
		theme(plot.title = element_text(size=25, hjust=0.5), 
			plot.subtitle = element_text(size=20, hjust=0.5),
			text = element_text(size = 10))
}

myviolin <- function(data, variable) {
                ggplot(data, aes(x = 1, y = eval(parse(text = variable)))) +
                    geom_jitter(alpha = 0.6, size = 3) +
                    geom_violin(alpha = 0.7) +
                    xlab("") + ylab("") + ggtitle(variable) +
                    theme_pubr() +
                    theme(text = element_text(family = "Arial"),
                        plot.title = element_text(hjust = 0.5))
            }

HGroup <- function(x) {
            ifelse(x <= 2, "H1", ifelse(x <= 4, "H2",
                                    ifelse(x <= 7, "H3",
                                        ifelse(x <= 28, "H4", "H5"))))
        }
