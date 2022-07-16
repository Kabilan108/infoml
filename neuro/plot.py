"""plot.py
This module contains functions for plotting.
"""

# Imports
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import numpy as np


# Export functions
__all__ = ['heatmap']


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
    if save is not None and isinstance(save, str):
        plt.savefig(save, dpi=300, transparent=True, dpi=300, 
                    bbox_inches='tight')
    else:
        raise ValueError("save must be a path to a file")

    return fig, ax

