"""wrangling.py
This module contains functions for data wrangling, preprocessing
and quality control.
"""

# Imports
import pandas as pd
import numpy as np
import glob
import os


def load_connectomes(dir, demo, zero_diag=True):
    """
    Load connectomes from a directory

    Parameters
    ----------
    dir : str
        Path to directory containing connectome files.
    demo : pd.DataFrame
        Demographic information.
    zero_diag : bool
        Whether to zero the diagonal of the connectome.

    Returns
    -------
    cntms : np.ndarray
        3D array of connectomes (subjects x rows x columns) (k x i x j)
    """

    # Check inputs
    assert os.path.isdir(dir), "dir must be a valid directory"
    assert isinstance(demo, pd.DataFrame), "demo must be a pandas DataFrame"
    assert isinstance(zero_diag, bool), "zero_diag must be a boolean"

    # Get list of files corresponding to the subjects
    files = [x for x in glob.glob(f"{dir}/*.txt") 
            if x[len(dir)+1:len(dir)+12] in demo.Subject.tolist()]

    # Load connectomes
    cntms = list()
    for file in files:
        cntm = np.loadtxt(file)
        if zero_diag:
            np.fill_diagonal(cntm, 0)
        cntms.append(cntm)

    return np.array(cntms)


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

