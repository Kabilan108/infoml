# Useful python functions, classes etc.

# Imports
import matplotlib.pyplot as plt
import scipy.stats as stats
import itertools as Iter
import sklearn as sk
import seaborn as sb
import pandas as pd
import numpy as np

from IPython.display import display_html


# Definitions
def show_dfs(*args, titles=Iter.cycle([''])):
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

    
    