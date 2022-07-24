"""metrics.py
This module contains functions for computing graph theory metrics.
"""

# Imports
import numpy.linalg as LA
import numpy as np


# Export functions
__all__ = ['compute_global_metric', 'intrahemispheric_stength', 
           'interhemispheric_stength', 'connectivity_strength', 'density']


def compute_global_metric(cntms, func, *args, **kwargs):
            """
            Compute global metrics for a list of connectomes

            @param: cntms -> (k x m x n); k = subjects
            @param: function that returns a 1D array of length k
            """

            values = []
            for cntm in cntms:
                values.append( func(cntm, *args, **kwargs) )
            return np.array(values)


def intrahemispheric_strength(cntm, hemispheremap):
    """
    Compute the intra-hemispheric connectivity of a connectome.

    Parameters
    ----------
    cntm : np.ndarray
        Connectome.
    hemispheremap : np.ndarray
        Hemispheric mapping.
        0 = left hemisphere;  1 = right hemisphere.
    """

    # Check inputs
    assert isinstance(cntm, np.ndarray), "cntm must be a numpy array"
    assert cntm.ndim == 2, "cntm must be a 2D array"
    assert cntm.shape[0] == cntm.shape[1], "cntm must be a square matrix"
    assert cntm.shape[0] == len(hemispheremap), \
        "cntm must have the same number of rows as hemishperemap"
    assert hemispheremap.ndim == 1, "hemishperemap must be a 1D array"
    hemispheremap = hemispheremap.astype(bool)
    inv_hemispheremap = np.invert(hemispheremap)


    # Number of nodes
    num_nodes = len(cntm)

    # Compute intrahemispheric strength
    val = (np.sum(cntm * (cntm > 0) * np.outer(hemispheremap, hemispheremap)) + np.sum(cntm * (cntm > 0) * np.outer(inv_hemispheremap, inv_hemispheremap))) / 2.0

    return np.array(val)


def interhemispheric_strength(cntm, hemispheremap):
    """
    Compute the inter-hemispheric connectivity of a connectome.

    Parameters
    ----------
    cntm : np.ndarray
        Connectome.
    hemispheremap : np.ndarray
        Hemispheric mapping.
        0 = left hemisphere;  1 = right hemisphere.
    """

    # Check inputs
    assert isinstance(cntm, np.ndarray), "cntm must be a numpy array"
    assert cntm.ndim == 2, "cntm must be a 2D array"
    assert cntm.shape[0] == cntm.shape[1], "cntm must be a square matrix"
    assert cntm.shape[0] == len(hemispheremap), \
        "cntm must have the same number of rows as hemishperemap"
    assert hemispheremap.ndim == 1, "hemishperemap must be a 1D array"
    hemispheremap = hemispheremap.astype(bool)
    inv_hemispheremap = np.invert(hemispheremap)

    # Number of nodes
    num_nodes = len(cntm)

    # Compute intrahemispheric strength
    val = (np.sum(cntm * (cntm > 0) * np.outer(hemispheremap, hemispheremap)) + np.sum(cntm * (cntm > 0) * np.outer(inv_hemispheremap, hemispheremap))) / 2.0

    return np.array(val)


def connectivity_strength(cntm):
    """
    Compute Connectivity Strength
    """

    return np.sum(cntm * (cntm > 0)) / 2.0 + np.trace(cntm * (cntm > 0)) / 2.0


def density(cntm):
    """
    Compute Connection Density
    """
    return np.sum(cntm > 0) * 100.0 / float(cntm.shape[0] * (cntm.shape[0]-1))


