"""stats.py
Statistical Methods for Connectomics
"""

# Imports
import scipy.stats as sps
import numpy as np


# Export functions
__all__ = ['fdr', 'remove_outliers', 'get_outlier_idx', 'group_difference', 
           'compare_variances', 'corrtest',
           'edgewise_correlation']


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


def group_difference(X, Y, parametric=True, paired=False, rmoutliers=False, 
                     alternative='two-sided'):
    """
    Compute the group difference between X and Y

    Parameters
    ----------
    X, Y : np.ndarray
        Data sets to compare.
    parametric : bool
        If True, use parametric test. If False, use non-parametric test.
    paired : bool
        If True, use paired test. If False, use unpaired test.
    rmoutliers : bool
        If True, remove outliers from the data. If False, do not remove outliers.
    alternative : str
        Type of alternative hypothesis to test. Options are:
        ['two-sided', 'greater', 'less']

    Returns
    -------
    effect_size : float
        Effects size of the difference.
    pval : float
        P-values for each element of diff.
    """

    # Check inputs
    X = np.asarray(X)
    Y = np.asarray(Y)
    assert X.ndim == 1, "X must be 1-dimensional, i.e., of shape (n,)"
    assert Y.ndim == 1, "Y must be 1-dimensional, i.e., of shape (n,)"
    assert X.shape == Y.shape, "X and Y must have the same shape"
    assert alternative in ['two-sided', 'greater', 'less'], \
        "Alternative must be one of 'two-sided', 'greater', or 'less'"

    # Remove outliers if requested
    if rmoutliers:
        X = remove_outliers(X)
        Y = remove_outliers(Y)

    # Compute descriptive statistics
    mean = np.array([X.mean(), Y.mean()])
    var = np.array([X.var(), Y.var()])
    std = np.array([X.std(), Y.std()])
    size = np.array([X.size, Y.size])

    # If there is no variation, return 0
    if (var == (0,0)).all():
        return 0, 1

    if parametric:
        if paired:
            # Student's t-test for normally distributed repeateed measures
            _, pval = sps.ttest_rel(X, Y)

            # Calculate effect size (see: https://bit.ly/PairedCohensD)
            _, r = sps.pearsonr(X, Y)
            s_z = np.sqrt(var.sum() - 2*r*std.prod())
            s_rm = s_z / np.sqrt(2*(1-r))
            effect_size = (mean[0] - mean[1]) / s_rm
        elif not paired:
            # Student's t-test for normally distributed independent variables
            
            # F-tests for unequal variances: 
            #   if fpval < 0.05, distributions have unequal variances
            if var[1] != 0:
                F = var[0] / var[1]
                fpval = 1 - sps.f.cdf(F, len(X)-1, len(Y)-1)
            else:
                # If variance of one of the data is zero while the other is not 
                # then consider this as the two dataset has different variance
                fpval = 0

            # Perform ttest for independent variables
            if fpval > 0.05:
                _, pval = sps.ttest_ind(X, Y, equal_var=True)
            else:
                _, pval = sps.ttest_ind(X, Y, equal_var=False)

            # Compute effect size (see: https://bit.ly/IndependentCohensD)
            s_pooled = np.sqrt(((size -1) * var).sum() / (size.sum() - 2))
            effect_size = (mean[0] - mean[1]) / s_pooled
        else:
            raise ValueError("paired must be either True or False")
    elif not parametric:
        if paired:
            # Wilcoxon's rank-sum test for non-normally distributed repeated measures
            _, pval = sps.wilcoxon(X, Y, alternative=alternative)

            # Calculate effect size (see: https://bit.ly/WilcoxonEffectSize)
            # effect_size = z / sqrt(N)
            # z = sum of signed ranks divided by the square root of the sum
            #     of their squares: https://bit.ly/3aMaTnp
            #     w / sqrt(sum of squares of ranks)
            # abs(r) -> small=0.1   medium=0.3  large=0.5
            diff = Y - X
            abs_diff = np.abs(diff)
            ranks = sps.rankdata(abs_diff)
            signs = [1 if x > 0 else -1 for x in diff]
            signed_ranks = ranks * signs
            # the statistic is calculated as follows (gives the same result 
            # with the fisrt output of the stt.wilcoxon(X, Y) function)
            # -  positiveRanks = signed_rank[signed_rank>0]
            # -  negativeRanks = -signed_rank[signed_rank<0]
            # -  w = min(np.sum(positiveRanks), np.sum(negativeRanks))
            z = np.sum(signed_ranks) / np.sqrt(np.sum(signed_ranks**2))
            effect_size = z / np.sqrt(size.sum())

        elif not paired:
            # Mann-Whitney U test for non-normally distributed independent variables
            U, pval = sps.mannwhitneyu(X, Y, alternative=alternative)

            # Calculate effect size (see: https://bit.ly/MannWhitneyEffectSize)
            # effect_size = z / sqrt(N)
            # abs(r) -> small=0.1   medium=0.3  large=0.5
            # z = (U - m_U) / std_U  (see: https://bit.ly/3AUPBiq)
            # m_U = size_x * size_y / 2
            # std_U = sqrt(size_x * size_y * (size_x + size_y + 1) / 12)
            m_U = size.prod() / 2
            std_U = np.sqrt(size.prod() * (size.sum() +1) / 12.0)
            z = (U - m_U) / std_U
            effect_size = z / np.sqrt(size.sum())
            
        else:
            raise ValueError("paired must be either True or False")
    else:
        raise ValueError("parametric must be either True or False")

    return effect_size, pval


def compare_variances(X, Y, test='F', rmoutliers=False):
    """
    Compare the variances of two distibutions using various statistical tests

    Parameters
    ----------
    X, Y :
        Data sets to compare.
    test : str
        Type of test of variance to use. Options are:
        ['F', 'bartlett', 'levene']

    Returns
    -------
    statistic: float
        Test statistic
    pval: float
        P-value
    """

    # Check inputs
    X = np.asarray(X)
    Y = np.asarray(Y)
    assert X.ndim == 1, "X must be 1-dimensional, i.e., of shape (n,)"
    assert Y.ndim == 1, "Y must be 1-dimensional, i.e., of shape (n,)"
    assert X.shape == Y.shape, "X and Y must have the same shape"
    assert np.all([x in 'abeflnrtv' for x in test.lower()]), \
        "test must be one of 'F', 'bartlett', 'levene'"

    if rmoutliers:
        X = remove_outliers(X)
        Y = remove_outliers(Y)
    
    if test.upper() == 'F':
        pval = 1 - sps.f.cdf(X.var() / Y.var(), len(X)-1, len(Y)-1)
        statistic = -1  # not implemented
    elif test.lower() in ['b', 'bartlett']:
        statistic, pval = sps.bartlett(X, Y)
    elif test.lower() in ['l', 'levene']:
        statistic, pval = sps.levene(X, Y, center='mean')

    return statistic, pval


def corrtest(X, Y, parametric=True):
    """
    Compute correlation coefficient and p-value for two vectors

    Parameters
    ----------
    X, Y : np.ndarray
        Vectors to compare
    parametric : bool
        If True, use Pearson's correlation coefficient. If False, use Spearman's

    Returns
    -------
    r : float
        Correlation coefficient
    p : float
        p-value
    """

    # Check inputs
    assert isinstance(X, np.ndarray), "X must be a numpy array"
    assert isinstance(Y, np.ndarray), "Y must be a numpy array"
    assert X.ndim == 1, "X must be 1-dimensional, i.e., of shape (n,)"
    assert Y.ndim == 1, "Y must be 1-dimensional, i.e., of shape (n,)"
    assert X.shape == Y.shape, "X and Y must have the same shape"
    assert isinstance(parametric, bool), "parametric must be a boolean"

    # Compute correlation coefficient
    if parametric:
        # Pearson's correlation coefficient
        r, p = sps.pearsonr(X, Y)
    elif not parametric:
        # Spearman's correlation coefficient
        r, p = sps.spearmanr(X, Y)
    else:
        raise ValueError("parametric must be a boolean")

    return r, p


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
            cmat[i,j], pval[i,j] = sps.pearsonr(cntms[i,j,:], vctr)

    return cmat, pval
