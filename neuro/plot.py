"""plot.py
This module contains functions for plotting.
"""

# Imports
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import numpy as np

from neuro import stats


# Export functions
__all__ = ['heatmap', 'corrplot']


def heatmap(matrix, show=False, save=None, cmap='jet', bgcolor='white', 
            threshold=None, figsize=(6, 6), **hmap_kwargs):
    """
    Generate heatmap for a given matrix

    Parameters
    ----------
    matrix : np.ndarray
        Matrix to plot
    show : bool
        If True, plot is shown. If False, figure handle is returned only
    cmap : str
        Seaborn color palette 
    bgcolor : 
        heatmap background color (values < threshold)
    threshold : float
        Threshold for the heatmap. If None, no threshold is applied
    figsize : tuple
        Figure size [ for plt.subplots() ]
    hmap_kwargs : dict
        Keyword arguments for seaborn.heatmap()

    Returns
    -------
    fig, ax : matplotlib.figure.Figure, matplotlib.axes.Axes
    """

    # Check inputs
    assert isinstance(matrix, np.ndarray), "matrix must be a numpy array"
    assert isinstance(show, bool), "show must be a boolean"
    assert isinstance(save, str) or save is None, "save must be a string"
    assert isinstance(cmap, str), "cmap must be a string"
    assert isinstance(bgcolor, str), "bgcolor must be a string"
    assert isinstance(threshold, float) or threshold is None, \
        "threshold must be a float"
    assert isinstance(figsize, tuple), "figsize must be a tuple"

    # Create colormap
    cmap = mpl.cm.get_cmap(cmap).copy()
    cmap.set_under(bgcolor)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot heatmap
    sns.heatmap(matrix, cmap=cmap, vmin=threshold, ax=ax,
                square=True, annot=False, **hmap_kwargs)

    # Show and/or save figure
    if show:
        plt.show()
    if save is not None:
        plt.savefig(save, dpi=300, transparent=True, bbox_inches='tight')

    return fig, ax


def corrplot(X, Y, parametric=True, xlab='X', ylab='Y', title='', 
             save=None, pt_annot=None, text=None, figsize=(6,4), 
             regplot_kws=None):
    """
    Generate regression plot for X and Y, annotated with 
    correlation coefficient and p-value.

    Parameters
    ----------
    X, Y : np.ndarray
        Data sets to correlate
    parametric : bool
        If True, perform parametric analysis. If False, perform non-parametric
    xlab : str
        X-axis label
    ylab : str
        Y-axis label
    title : str
        Figure title
    save : str
        Path to save figure to
    pt_annot : list
        Point annotations. If None, no annotations are added.
    text : str
        Text to display
    figsize : tuple
        Figure size [ for plt.subplots() ]
    regplot_kws : dict
        Keyword arguments for seaborn.regplot()

    Returns
    -------
    fig, ax : matplotlib.figure.Figure, matplotlib.axes.Axes
    """

    # Check inputs
    X = np.asarray(X)
    Y = np.asarray(Y)
    assert isinstance(X, np.ndarray), "X must be a numpy array"
    assert isinstance(Y, np.ndarray), "Y must be a numpy array"
    assert isinstance(xlab, str), "xlab must be a string"
    assert isinstance(ylab, str), "ylab must be a string"
    assert isinstance(title, str), "title must be a string"
    assert isinstance(save, str) or save is None, "save must be a string"
    assert isinstance(pt_annot, str) or save is None, "pt_annot must be a list"
    assert isinstance(text, str) or text is None, "text must be a string"
    assert isinstance(figsize, tuple), "figsize must be a tuple"
    assert isinstance(regplot_kws, dict) or regplot_kws is None, \
        "regplot_kws must be a dictionary"

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot regression
    sns.regplot(x=X, y=Y, ax=ax, 
                scatter_kws={'s': 60, 'edgecolor': 'none', 'alpha': 0.6, 
                             'color': '#0000CC'}, 
                line_kws={'color': 'red'})
    sns.despine()

    # Plot labels
    ax.set_xlabel(xlab, fontsize=13)
    ax.set_ylabel(ylab, fontsize=13)
    ax.set_title(title, fontsize=15)
    ax.tick_params(axis='both', labelsize=11)

    # Set font
    mpl.rcParams['font.sans-serif'] = 'Times New Roman'
    mpl.rcParams['font.family'] = 'serif'

    # Compute correlation coefficient and p-value
    r, p = stats.corrtest(X, Y, parametric=parametric)

    # Add correlation coefficient and p-value annotations
    if text is None:
        text = f"r = {r:.3f}\np = {p:.3f}"
    ax.text(0.78, 0.88, text, transform=ax.transAxes,
            color='black', fontsize=12,
            horizontalalignment='left', verticalalignment='center',
            bbox={'facecolor': 'white', 'alpha': 0.6, 
                  'pad': 10, 'linewidth': 0})

    # Show and/or save figure
    if save is not None:
        plt.savefig(save, dpi=300, transparent=True, bbox_inches='tight')

    return fig, ax


