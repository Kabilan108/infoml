#!/bin/bash
# 

heatMap_py=~/repo/code/python/heatMap.py
histogramOfEdges_py=~/repo/code/python/histogramOfEdges.py
mergeImages_py=~/repo/code/python/mergeImages.py
mergeImages_folder_py=~/repo/code/python/mergeImages_folder.py
edgeDistributionPlot_py=~/repo/code/python/edgeDistributionPlot.py
qaFunctionalTimeseries_py=~/repo/code/python/QA/qaFunctionalTimeseries.py
qaConnectivity_py=~/repo/code/python/QA/qaConnectivity.py


action=${1} #subjectwiseEdges, randomEdges, connectivity
plotExtension=png #png or svg
numROI=86
colorMap=jet #RdBu
standardDeviation=2


pipelines=(10M 500per method2 method3)
edgeWeights=(raw sift2 nodevol sift2_nodevol)
rootFolder=/home/yusuf/data/TBI/TBI_drew


hemisphereMaps=/home/yusuf/data/atlases/Desikan86/hemisphereMaps_Desikan86.txt

samples="" #"-samples src/list_strFuncIntersection_connected.txt"

#### clean up connectivity summary file, if exists
if [[ $action == "connectivity" ]];then
	for pipeline in ${pipelines[@]}; do
		rm -f $rootFolder/QA/connectivity/$pipeline/connectivitySummary.txt
	done
fi

for pipeline in ${pipelines[@]}; do
	for edgeWeight in ${edgeWeights[@]}; do
		connectomesRoot=$rootFolder/connectomes/$pipeline/$edgeWeight
		subjectwiseEdgesRoot=$rootFolder/QA/subjectwiseEdges/$pipeline"_"$edgeWeight
		randomEdgesRoot=$rootFolder/QA/randomEdges/$pipeline"_"$edgeWeight
		connectivityRoot=$rootFolder/QA/connectivity/$pipeline

		####generate heatmaps of connectomes as well as draw histograms of edge distribution per subject
		if [[ $action == "subjectwiseEdges" ]];then
			numOutputFiles="--numOutputFiles 2"

			mkdir -p $subjectwiseEdgesRoot
			for connPath in $connectomesRoot/*; do
				filename=$(basename $connPath | sed -e 's/.txt//')
				python $heatMap_py -i $connPath -o $subjectwiseEdgesRoot/$filename"_heatMap."$plotExtension --colorMap $colorMap $symmetricRangeAroundZero
				python $histogramOfEdges_py --inputPath $connPath --outputPath $subjectwiseEdgesRoot/$filename"_histogram."$plotExtension --title $filename --zeroDiagonals
				python $mergeImages_py --outputPath $subjectwiseEdgesRoot/$filename".png" --numInputs 2 --grid 1 2 --inputPaths $subjectwiseEdgesRoot/$filename"_heatMap.png" $subjectwiseEdgesRoot/$filename"_histogram.png" --noTitle
				rm $subjectwiseEdgesRoot/$filename"_heatMap.png" $subjectwiseEdgesRoot/$filename"_histogram.png"
			done

			python $mergeImages_folder_py --inputFolder $subjectwiseEdgesRoot/ --outputPath $subjectwiseEdgesRoot".jpg" --size 6000  $numOutputFiles
			rm -rf $subjectwiseEdgesRoot/
		fi


		####test connectivity of connectomes
		if [[ $action == "connectivity" ]];then
			mkdir -p $connectivityRoot

			connectivitySummaryFile_path=$connectivityRoot/connectivitySummary.txt
			echo "============"$pipeline"    "$edgeWeight"============">> $connectivitySummaryFile_path
			echo "------------Missing ROIs per subject (there should be "$numROI" nodes in each)-----------" >> $connectivitySummaryFile_path
			brainMatch -utility missingNode -connectomePath $connectomesRoot/ -type matrix -numNodes $numROI >> $connectivitySummaryFile_path
			echo -e "\n------------Connectivity of connectomes per subject -----------" >> $connectivitySummaryFile_path
			brainMatch -utility graphConnectivity -connectomePath $connectomesRoot/ -connectivity structure -type matrix -printComponents >> $connectivitySummaryFile_path
			echo -e "\n" >> $connectivitySummaryFile_path

			connectivityDetailFile_path=$connectivityRoot/$pipeline"_"$edgeWeight"_connectivityDetail.txt"
			echo -e "------------Density of connectomes per subject for ------------" > $connectivityDetailFile_path
			brainMatch -utility matrixDensity -folderPath $connectomesRoot/ >> $connectivityDetailFile_path
			echo -e "\n\n------------Strength of connectivity per subject for ------------" >> $connectivityDetailFile_path
			brainMatch -utility matrixConnectivityStrength -folderPath $connectomesRoot/ -hemispheres $hemisphereMaps >> $connectivityDetailFile_path

			python $qaConnectivity_py --inputFolder $connectomesRoot/ --numNodes $numROI --hemisphereMaps $hemisphereMaps --plotPath $connectivityRoot/$pipeline"_"$edgeWeight"_connectivityDistribution."$plotExtension --reportFile $connectivityRoot/$pipeline"_"$edgeWeight"_connectivityOutliers.txt" --standardDeviation $standardDeviation --title "$pipeline"\ "$edgeWeight"
		fi


		#### generate histogram of random edges across subjects
		if [[ "$action" == "randomEdges" ]];then
			mkdir -p $randomEdgesRoot

			for i in {1..4};do
				python $edgeDistributionPlot_py -c $connectomesRoot/ -o $randomEdgesRoot/"edges_"$i"."$plotExtension -np 4 --group all
			done
		fi
	done
done


