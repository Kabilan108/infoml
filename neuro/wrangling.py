"""wrangling.py
This module contains functions for data wrangling, preprocessing
and quality control.
"""

# Imports
import pandas as pd
import numpy as np
import glob


def load_connectomes(dir: str, demo: pd.DataFrame, zero_diag: bool=True):
    """
    Load connectomes from a directory
    Returns a 3D array of connectomes (subjects x rows x columns) (k x i x j)
    """

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