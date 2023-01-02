"""
datasets
--------

This module contains functions to get the paths to the datasets used in the
"""

# Imports
from importlib import resources


def get_ceman_counts():
    """
    Get path the GSE50499 [1]_ gene counts matrix.

    Returns
    -------
    pathlib.PosixPath
        Path to file

    References
    ----------
    .. [1] Kenny PJ, Zhou H, Kim M, Skariah G et al. MOV10 and FMRP regulate
           AGO2 association with microRNA recognition elements. Cell Rep 2014
           Dec 11;9(5):1729-1741. PMID: 25464849
    """

    with resources.path("infoml.data", "GSE50499_GEO_Ceman_counts.txt.gz") as f:
        datapath = f
    return datapath
