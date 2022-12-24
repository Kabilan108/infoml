"""wrangling.py
This module contains functions for data wrangling, preprocessing
and quality control.
"""

# Imports
import pandas as pd
import numpy as np
import glob
import os
import re


# Export functions
__all__ = ['_load_connectome', 'load_connectomes', 'savetxt_compact'
           'load_computed_measures']

# TODO: Move these to separate text files
# Define feature sets
# Nodal measures
NODAL = ['degree', 'degree_interHemisphere', 'degree_intraHemisphere', 'degree_withinModule', 'degree_betweenModule', 'strength_noSelf',
         'strength_interHemisphere', 'strength_intraHemisphere', 'strength_withinModule', 'strength_betweenModule',
         'strength_selfConnections_nodal', 'node_betweenness_centrality', 'eigenvector_centrality', 'modularity_nodal',
         'participation_coefficient', 'clustering_coefficient', 'eccentricity', 'rich_club_coefficient', 'degree_neg', 'degree_interHemisphere_neg',
         'degree_intraHemisphere_neg', 'degree_withinModule_neg', 'degree_betweenModule_neg', 'strength_noSelf_neg',
         'strength_interHemisphere_neg', 'strength_intraHemisphere_neg', 'strength_withinModule_neg', 'strength_betweenModule_neg',
         'participation_coefficient_pos', 'participation_coefficient_neg', 'modularity_nodal_neg', 'clustering_coefficient_neg',
         'clustering_coefficient_zhang', 'clustering_coefficient_zhang_neg']

# Global measures
GLOBAL = ['degree_avg', 'degree_interHemisphere_avg', 'degree_intraHemisphere_avg', 'degree_withinModule_avg',
          'degree_betweenModule_avg', 'strength_global', 'strength_global_offDiagonal', 'strength_interHemisphere_global',
          'strength_intraHemisphere_global', 'strength_selfConnections_global', 'node_betweenness_centrality_avg', 'eigenvector_centrality_avg',
          'participation_coefficient_avg', 'clustering_coefficient_avg', 'eccentricity_avg', 'characteristic_path_length', 'global_efficiency',
          'radius', 'diameter', 'modularity_global', 'assortativity', 'density', 'degree_neg_avg', 'degree_interHemisphere_neg_avg',
          'degree_intraHemisphere_neg_avg', 'degree_withinModule_neg_avg', 'degree_betweenModule_neg_avg', 'strength_global_neg',
          'strength_global_offDiagonal_neg', 'strength_interHemisphere_global_neg', 'strength_intraHemisphere_global_neg', 'participation_coefficient_pos_avg',
          'participation_coefficient_neg_avg', 'clustering_coefficient_neg_avg', 'modularity_global_neg', 'clustering_coefficient_zhang_avg',
          'clustering_coefficient_zhang_neg_avg',]


def _load_connectome(fname, zero_diag=True):
    """
    Load a connectome from a text file.

    Parameters
    ----------
    fname : str
        Path to file.
    zero_diag : bool
        Whether to zero the diagonal of the connectome.

    Returns
    -------
    cntm : np.ndarray
        Connectome.
    """

    # Check inputs
    fname = os.path.expanduser(fname)
    assert os.path.exists(fname), "fname must be a valid file"
    assert isinstance(zero_diag, bool), "zero_diag must be a boolean"

    # Load connectome
    cntm = np.loadtxt(fname)
    if zero_diag:
        np.fill_diagonal(cntm, 0)

    return cntm


def load_connectomes(dir, ids, id_pattern, ext='*.txt', zero_diag=True):
    """
    Load connectomes from a directory

    Parameters
    ----------
    dir : str
        Path to directory containing connectome files.
    ids : array_like
        List of IDs to load.
    id_pattern : str
        Regular expression pattern to match IDs.
    ext : str
        Pattern for file extensions.
    zero_diag : bool
        Whether to zero the diagonal of the connectome.

    Returns
    -------
    cntms : np.ndarray
        3D array of connectomes (subjects x rows x columns) (k x i x j)
    """

    # Check inputs
    ids = list(ids)
    assert os.path.isdir(dir), "dir must be a valid directory"
    assert isinstance(zero_diag, bool), "zero_diag must be a boolean"

    # Get list of files corresponding to the subjects
    def get_id(x): return re.search(id_pattern, x)[0]
    files = [x for x in glob.glob(f"{dir}/{ext}") if get_id(x) in ids]

    # Load connectomes
    cntms = np.array([_load_connectome(f, zero_diag) for f in files])

    return cntms


def savetxt_compact(fname, mat, fmt='%.6f', delim='\t', fileaccess='a'):
    """
    Save a matrix to a text file in a compact format.

    Parameters
    ----------
    fname : str
        Path to file.
    mat : np.ndarray
        Matrix to save.
    fmt : str
        Format of the numbers.
    delim : str
        Delimiter to use.
    fileaccess : str
        File access mode.
    """

    # Check inputs
    assert isinstance(fname, str), "fname must be a string"
    assert isinstance(mat, np.ndarray), "mat must be a numpy array"
    assert isinstance(fmt, str), "fmt must be a string"
    assert isinstance(delim, str), "delim must be a string"
    assert isinstance(fileaccess, str), "fileaccess must be a string"

    # Save matrix
    with open(fname, fileaccess) as f:
        for row in mat:
            line = delim.join('0' if val == 0 else fmt % val for val in row)
            f.write(line + '\n')


def load_computed_measures(path, scale):
    """
    Load Graph-Theory Measures Computed Using the `bctpy` Wrapper.

    Parameters
    ----------
    path : str
        Path to directory where computed features are stored
    scale : str
        Either 'global' or 'nodal'

    Returns
    -------
    features : pd.DataFrame or dict
        scale = global: dataframe with measures as columns; subjects as rows
        scale = nodal:  dictionary with measures as keys, and matrices with 
                        subjects as rows and nodes as columns as values
    """

    # Check inputs
    assert os.path.isdir(path), "Path does not exist"
    assert scale in ['global', 'nodal'], "Scale must be 'global' or 'nodal'"

    # Select feature list to use
    if scale == 'nodal':
        FSET = NODAL
    elif scale == 'global':
        FSET = GLOBAL
    else:
        raise ValueError("scale must be nodal or global")

    # Retreive paths to desired features
    feature_paths = [x for x in glob.glob(path + '/*.txt') if
                     os.path.basename(x)[:-4] in FSET]

    # Load features
    features = dict()
    for fpath in feature_paths:
        features[os.path.basename(fpath)[:-4]] = np.loadtxt(fpath)

    # Convert to dataframe if needed
    if scale == 'global':
        features = pd.DataFrame(features)

    return features
