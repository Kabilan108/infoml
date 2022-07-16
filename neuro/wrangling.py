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
__all__ = ['_load_connectome', 'load_connectomes', 'savetxt_compact']


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
    get_id = lambda x: re.search(id_pattern, x)[0]
    files = [x for x in glob.glob(f"{dir}/{ext}") if get_id(x) in ids]

    # Load connectomes
    cntms = np.array([ _load_connectome(f, zero_diag) for f in files ])

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

