"""plot.py
This module contains functions for plotting.
"""

# Imports
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import numpy as np
import itertools

from neuro import stats

# Global Plot options
sns.set(font='Times New Roman')


# Export functions
__all__ = ['heatmap', 'corrplot', 'boxplot']


def heatmap(matrix, save=None, cmap='jet', bgcolor='black', threshold=None, 
            figsize=(6, 6), **hmap_kwargs):
    """
    Generate heatmap for a given matrix

    Parameters
    ----------
    matrix : np.ndarray
        Matrix to plot
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
    assert isinstance(save, str) or save is None, "save must be a string"
    assert isinstance(cmap, str), "cmap must be a string"
    assert isinstance(bgcolor, str), "bgcolor must be a string"
    assert type(threshold) in [int, float] or threshold is None, \
        "threshold must be numeric"
    assert isinstance(figsize, tuple), "figsize must be a tuple"

    # Create colormap
    cmap = mpl.cm.get_cmap(cmap).copy()
    cmap.set_under(bgcolor)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot heatmap
    sns.heatmap(matrix, cmap=cmap, vmin=threshold, ax=ax,
                square=True, annot=False, **hmap_kwargs)

    # save figure
    if save is not None:
        plt.savefig(save, dpi=300, transparent=True, bbox_inches='tight')

    return fig, ax


def corrplot(X, Y, parametric=True, xlab='X', ylab='Y', title='', 
             save=None, pt_annot=None, text=None, figsize=(6,4), 
             **regplot_kws):
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

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot regression
    sns.regplot(x=X, y=Y, ax=ax, 
                scatter_kws={'s': 60, 'edgecolor': 'none', 'alpha': 0.5, 
                            'color': '#0000CC'}, 
                line_kws={'color': 'red'},
                **regplot_kws)

    # Plot labels
    ax.set_xlabel(xlab, fontsize=13)
    ax.set_ylabel(ylab, fontsize=13)
    ax.set_title(title, fontsize=15)
    ax.tick_params(axis='both', labelsize=11)

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

    # Figure styling
    ax.set_facecolor('white')
    ax.grid(True, which='both', color='lightgrey', linestyle='--')
    sns.despine()
    ax.spines['left'].set(color='black', linewidth=1)
    ax.spines['bottom'].set(color='black', linewidth=1)

    # save figure
    if save is not None:
        plt.savefig(save, dpi=300, transparent=True, bbox_inches='tight')

    return fig, ax


def boxplot(data, labels, jitter=False, title='', xlab='', ylab='', 
            middleline=['median'], figsize=(6,4), save=None,
            boxplot_kws={}, swarmplot_kws={}):
    """
    Create boxplot for data with labels

    Parameters
    ----------
    data : np.ndarray
        Data to plot
    labels : list
        Labels for data
    jitter : bool
        If True, add jitter to data
    title : str
        Figure title
    xlab : str
        X-axis label
    ylab : str  
        Y-axis label
    middleline : list
        Type of middle line to plot. Can show 'median' and 'mean'
    figsize : tuple
        Figure size [ for plt.subplots() ]
    save : str
        Path to save figure to
    boxplot_kws : dict
        Keyword arguments for seaborn.boxplot()
    swarmplot_kws : dict
        Keyword arguments for seaborn.swarmplot()

    Returns
    -------
    fig, ax : matplotlib.figure.Figure, matplotlib.axes.Axes
    """

    # Check inputs
    data = np.asarray(data)
    assert isinstance(data, np.ndarray), "data must be a numpy array"
    assert data.ndim <= 2, "data must be 1 or 2 dimensional"
    assert isinstance(labels, list), "labels must be an list"
    assert isinstance(jitter, bool), "jitter must be a boolean"
    assert isinstance(title, str), "title must be a string"
    assert isinstance(xlab, str), "xlab must be a string"
    assert isinstance(ylab, str), "ylab must be a string"
    assert isinstance(middleline, list), "middleline must be a list"
    assert isinstance(figsize, tuple), "figsize must be a tuple"
    assert isinstance(save, str) or save is None, "save must be a string"


    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Boxplot options
    markersize = 0 if jitter else 6
    boxprops = dict(linestyle='-', linewidth=1.5)
    flierprops = dict(marker='o', markerfacecolor='grey', markersize=markersize, 
                      markeredgecolor='none', linestyle='none')
    capprops = dict(linestyle='-', linewidth=2, color='grey')
    whiskerprops = dict(linestyle='--', linewidth=2, color='grey')
    medianprops = dict(linewidth=0)
    meanprops = dict(linewidth=0)
    meanline = 'mean' in middleline
    showmeans = 'mean' in middleline
    if 'median' in middleline:
        medianprops = dict(linestyle='-', linewidth=1, color='firebrick')
    if 'mean' in middleline:
        meanprops = dict(linestyle='-', linewidth=1, color='firebrick', 
                         marker='D', markersize=4, markerfacecolor='black')

    # Create boxplot
    sns.boxplot(data=data, ax=ax,
                boxprops=boxprops, flierprops=flierprops,
                capprops=capprops, whiskerprops=whiskerprops,
                medianprops=medianprops, meanprops=meanprops, 
                meanline=meanline, showmeans=showmeans,
                **boxplot_kws)

    # Boxplot styling
    colors = itertools.cycle(['#2096BA', '#AB3E16', '#351C4D', '#849974', 
                              '#F7DFD4', '#F5AB99'])
    for patch, color in zip(ax.patches, colors):
        patch.set_facecolor(color)
        patch.set_edgecolor(color)
        patch.set_alpha(.6)

    # Add points to boxplot
    if jitter:
        sns.swarmplot(data=data, ax=ax, color='black', alpha=.3, s=4,
                      **swarmplot_kws)

    # Plot labels and axis styling
    ax.set_xlabel(xlab, fontsize=13)
    ax.set_ylabel(ylab, fontsize=13)
    ax.set_title(title, fontsize=15)
    ax.set_xticklabels(labels, fontsize=12)
    ax.tick_params(axis='both', labelsize=11)

    # Figure styling
    ax.set_facecolor('white')
    ax.grid(True, which='both', axis='y', color='lightgrey', linestyle='--')
    sns.despine(offset=10, trim=True, bottom=True)
    ax.spines['left'].set(color='black', linewidth=1)
    ax.spines['bottom'].set(color='black', linewidth=1)

    # save figure
    if save is not None:
        plt.savefig(save, dpi=300, transparent=True, bbox_inches='tight')

    return fig, ax

