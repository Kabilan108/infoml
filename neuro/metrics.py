"""metrics.py
This module contains functions for computing graph theory metrics.
"""

# Imports
import numpy.linalg as LA
import numpy as np


# Export functions
__all__ = ['intrahemispheric_stength', 'interhemispheric_stength']


def intrahemispheric_stength(cntm, hemispheremap):
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

    # Number of nodes
    num_nodes = len(cntm)

    # Compute intrahemispheric strength
    strength = []
    for i in range(num_nodes):
        strength.append( cntm[i][hemispheremap == hemispheremap[i]].sum() )

    return np.array(strength)


def interhemispheric_stength(cntm, hemispheremap):
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

    # Number of nodes
    num_nodes = len(cntm)

    # Compute intrahemispheric strength
    strength = []
    for i in range(num_nodes):
        strength.append( cntm[i][hemispheremap != hemispheremap[i]].sum() )

    return np.array(strength)


def strength(cntm):
    """
    Compute Strength
    """

    return np.sum(cntm * (cntm > 0)) / 2.0 + np.trace(cntm * (cntm > 0)) / 2.0