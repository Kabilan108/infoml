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
    plt.plot(K, inertia, 'go-')
    plt.xlabel("k")
    plt.ylabel("Inertia")
    plt.title(title)
    plt.show()