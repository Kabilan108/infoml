# Useful python functions, classes etc.

# Imports
import sklearn.preprocessing as preprocess
import sklearn.cluster as cluster
import matplotlib.pyplot as plt
import scipy.stats as stats
import itertools as Iter
import seaborn as sns
import pandas as pd
import numpy as np
import rich

from IPython.display import display_html


# Definitions
def show_dfs(*args: pd.DataFrame, titles: Iter.cycle=Iter.cycle([''])) -> None:
    """
    Display dataframes next to each other in a jupyter notebook.
    @param *args
        Multiple pandas dataframes
    @param title
        Title(s) for dataframes
    """

    html_str = ''
    for (df, title) in zip(args, Iter.chain(titles, Iter.cycle(['</br>']))):
        html_str += "<th style='text-align: center'><td style='vertical-align: top'>"
        html_str += f"<h2>{title}</h2>"
        html_str += df.to_html().replace("table", "table style='display: inline'")
        html_str += "</td></th>"
    display_html(html_str, raw=True)

    return

def see_distn(data: pd.DataFrame, title: str='') -> None:
    """
    Create boxplots that show the distribution of numeric variables in a dataframe.
    @param data
        Pandas dataframe with specific column names (ideally, the result of pd.DataFrame.melt())
    @param title
        Title for distribution figure
    """
    try:
        g = sns.catplot(y='value', kind='box', col='variable', col_wrap=4,
                        sharey=False, height=2, data=data)
        g.set_titles('{col_name}', size=12, pad=13)\
         .set_ylabels('')\
         .despine(bottom=True)
        g.fig.suptitle(title, size=20)
        g.fig.subplots_adjust(hspace=.3, top=.9)
        plt.show()
    except:
        rich.print("[red]ERROR:[/red] Please provide a valid DataFrame (Ideally, the result of pd.DataFrame.melt()).")

def rmoutliers(x: pd.Series) -> pd.Series:
    """
    Remove statistical outliers from pandas series
    @param x
        Pandas series
    """
    # Compute quartiles
    Q1, Q3 = x.quantile((.25, .75))
    # Fix outliers
    x[x > Q3 + 1.5*(Q3-Q1)] = np.NaN

    return x

def elbow_plot(data: pd.DataFrame, max_k: int=10, title: str='') -> None:
    """
    Generate an elbow plot to determine optimal K for K-means clusters.
    @param data
        Pandas DataFrame
    @param max_k
        Maximum number of clusters to test
    @param title
        Title of Elbow plot
    """

    # Scale data before use
    scaler = preprocess.StandardScaler()
    normal_data = scaler.fit_transform(data.dropna().values)

    # Create elbow plot
    inertia = []
    for k in range(1, max_k+1):
        fit = cluster.KMeans(n_clusters=k).fit(normal_data)
        fit.fit(normal_data)
        inertia.append(fit.inertia_)

    # Create figure
    plt.figure(figsize=(5,3))
    plt.plot(range(1, max_k+1), inertia, 'go-')
    plt.xlabel("k")
    plt.ylabel("Inertia")
    plt.title(title)
    plt.show()

def calculate_pvalues(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate p-values matrix from data frame
    @param df
        Pandas Data Frame
    """

    # Extract numeric data from df
    df = df.dropna()._get_numeric_data()
    # Create empty p-values matrix (same rows & columns)
    cols = pd.DataFrame(columns=df.columns)
    pvalues = cols.transpose().join(cols, how='outer')
    # Populate matrix
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(stats.pearsonr(df[r], df[c])[1], 10)

    return pvalues

def kmeans(data: pd.DataFrame, k: int=2, facet_by: str=None) -> tuple:
    """
    Wrapper for sklearn.cluster.KMeans()
    @param data
        Pandas dataframe (Result of pd.DataFrame.melt())
    @param k
        Number of clusters
    @param facet
        Column to split data on when clustering. Must be within Data Frame Index
    """

    # Remove missing data and select only numeric columns from data
    data = data._get_numeric_data().dropna()
    
    if facet_by is not None:
        # Verify that facet is valid
        if facet_by in data.index.names:
            # Loop through facets
            info = []
            sset = []
            for facet in data.index.to_frame(index=False)[facet_by].unique():
                # Compute clusters on subset of data (recursive)
                (i,d) = kmeans(data[data.index.get_level_values(facet_by).isin([facet])], k)
                # Add facet to cluster information
                i[facet_by] = facet
                # Append new data
                info.append(i)
                sset.append(d)

            # Concatenate data
            info = pd.concat(info)
            data = pd.concat(sset)
                        
            return (info, data)
        else:
            rich.print("[red]ERROR:[/red] Facet not in Data Frame Index.")
    else:
        # Fit data to kmeans cluster model
        fit = cluster.KMeans(n_clusters=k, random_state=69).fit(data.values)
        
        # Add cluster labels to data
        data = pd.concat([data.reset_index(), pd.DataFrame(fit.labels_)], axis=1)\
                .rename({0: 'Cluster'}, axis=1)\
                .set_index(data.index.names)
        data.name = "Cluster Data"
        
        # Store cluster information
        info = pd.concat([
            pd.DataFrame(fit.cluster_centers_, columns=data.columns[:-1]).round(2),
            pd.DataFrame(data.groupby('Cluster').count().mean(axis=1).apply(round), columns=['Size'])
        ], axis=1).rename_axis('Cluster')
        info.name = "Cluster Information"

        return (info.reset_index(), data.reset_index())

def write_dfs(writer: pd.ExcelWriter, sheet_name: str, **dfs) -> None:
    """
    Wrire multiple data frames to an excel file.
    @param writer
        An pd.ExcelWriter object
    @param sheet_name
        Name of sheet to write data to
    @param **dfs
        Names and pandas dataframes
    """
    # Initialize worksheet
    worksheet = writer.book.create_sheet(sheet_name)
    writer.sheets[sheet_name] = worksheet

    # Write Data Frames to sheet
    i = 1
    for (name, df) in dfs.items():
        # Write data frame to sheet
        worksheet.cell(row=i, column=1, value=name.replace("_", " "))
        df.to_excel(writer, sheet_name=sheet_name, startrow=i, startcol=0)
        # Next data frame starts at
        i += df.shape[0] + 4