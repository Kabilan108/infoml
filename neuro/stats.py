"""stats.py
Statistical Methods for Connectomics
"""

# Imports
from scipy import stats
import numpy as np

# Export functions
__all__ = ['fdr', 'edgewise_correlation']


def _ecdf(x):
    """
    Empirical cumulative distribution function.
    """
    n = len(x)
    return np.arange(1, n+1) / float(n)


def fdr(pvals, correction='bh'):
    """
    Perform FDR correction on a list of p-values.

    Parameters
    ----------
    pvals : array-like, 1d
        Set of p-values of the individual tests.
    correction : Type of correction to use. Options are:
        ['bh', 'benjamini-hochberg'] (Default); 
        ['b', 'bonf', 'bonferroni']; 
        ['h', 'holm']

    Returns
    -------
    adj_pvals : ndarray
        pvalues adjusted for multiple comparisons.
    """

    # Check inputs
    pvals = np.asarray(pvals)
    assert pvals.ndim == 1, "pvals must be 1-dimensional, i.e., of shape (n,)"
    assert correction in ['Benjamini-Hochberg', 'Bonferroni', 'Holm'], \
        "Correction must be one of 'Benjamini-Hochberg', 'Bonferroni', or 'Holm'"

    # Keep track of p-values that are not equal to 1
    # pvalues = 1 when the model was not fit and the element was skipped over
    w = np.where(pvals == 1)[0]

    if correction.lower() in ['bh', 'benjamini-hochberg']:
        # Sort pvals
        pvals_sortind = np.argsort(pvals)
        pvals_sorted = np.take(pvals, pvals_sortind)

        # Compute ecdf factor
        ecdf = _ecdf(pvals_sorted)

        # Compute corrected p-values
        adj_pvals = np.minimum.accumulate((pvals_sorted / ecdf)[::-1])[::-1]

        # Reorder pvalues to match original
        adj_pvals[pvals_sortind] = adj_pvals

    elif correction.lower() in ['b', 'bonf', 'bonferroni']:
        # Compute corrected p-values
        adj_pvals = pvals * float(len(pvals))

    elif correction.lower() in ['h', 'holm']:
        # Compute corrected p-values
        adj_pvals = np.maximum.accumulate(pvals * np.arange(len(pvals), 0, -1))

    # Replace skipped pvalues with 1s
    adj_pvals[w] = 1

    return adj_pvals


def remove_outliers(data):
    """
    Remove outliers from a data set.

    Parameters
    ----------
    data : np.ndarray
        Data set to remove outliers from.

    Returns
    -------
    data : np.ndarray
        Data set without outliers.
    """

    # Check inputs
    data = np.asarray(data)
    assert isinstance(data, np.ndarray), "data must be a numpy array or array-like"

    # Compuite the upper and lower quartiles
    lower, upper = np.percentile(data, [25, 75])
    IQD = upper - lower
    lower_bound = lower - 1.5 * IQD
    upper_bound = upper + 1.5 * IQD

    # Remove outliers
    data = data[(data <= upper_bound) & (data >= lower_bound)]

    return data


def get_outlier_idx(data):
    """
    Get indices of outliers in a data set.

    Parameters
    ----------
    data : np.ndarray
        Data set to remove outliers from.

    Returns
    -------
    idx : np.ndarray
        Indices of outliers.
    """

    # Check inputs
    data = np.asarray(data)
    assert isinstance(data, np.ndarray), "data must be a numpy array or array-like"

    # Compuite the upper and lower quartiles
    lower, upper = np.percentile(data, [25, 75])
    IQD = upper - lower
    lower_bound = lower - 1.5 * IQD
    upper_bound = upper + 1.5 * IQD

    # Get indices of outliers
    idx = np.argwhere((data <= upper_bound) & (data >= lower_bound))

    return idx


def edgewise_correlation(cntms, vctr):
    """
    Calculate the correlation between the edges of a connectivity matrix 
    and a vector.

    Parameters
    ----------
    cntms : np.ndarray
        Connectivity matrix (i x j x k;  k -> number of subjects)
    vctr : np.ndarrau
        Vector (k x 1)

    Returns
    -------
    cmat: np.ndarray
        Correlation matrix
    pval: np.ndarray
        P-values for each edge
    """

    # Get the matrix dimensions
    I, J, K = cntms.shape

    # Initialize the correlation and pvalue matrices
    cmat = pval = np.zeros(cntms.shape[:2])

    # Populate the correlation and pvalues
    for i in range(I):
        for j in range(J):
            cmat[i,j], pval[i,j] = stats.pearsonr(cntms[i,j,:], vctr)

    return cmat, pval