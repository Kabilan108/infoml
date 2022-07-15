"""stats.py
Statistical Methods for Connectomics
"""

# Imports
from scipy import stats
import numpy as np


def edgewise_correlation(cntms: np.ndarray, vctr: np.ndarray) -> np.ndarray:
    """
    Calculate the correlation between the edges of a connectivity matrix 
    and a vector.

    :param cntms: Connectivity matrix (i x j x k;  k -> number of subjects)
    :param vctr: Vector (k x 1)
    :return: Correlation matrix
    """

    # Get the matrix dimensions
    I, J, K = cntms.shape

    # Initialize the correlation and pvalue matrices
    cmap = pval = np.zeros(cntms.shape[:2])

    # Populate the correlation and pvalues
    for i in range(I):
        for j in range(J):
            cmap[i,j], pval[i,j] = stats.pearsonr(cntms[i,j,:], vctr)

    return cmap, pval
