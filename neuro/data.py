"""data.py
This module contains functions for loading and preprocessing data.
"""

# Imports
import pandas as pd
import numpy as np
import glob


def load_connectomes(dir: str, demo: pd.DataFrame) -> np.ndarray:
    """
    Load connectomes from a directory
    Returns a 3D array of connectomes (subjects x rows x columns)
    """

    # Get list of files corresponding to the subjects
    files = [x for x in glob.glob(f"{dir}/*.txt") 
            if x[len(dir)+1:len(dir)+12] in demo.Subject.tolist()]

    # Load connectomes
    cntms = list()
    for file in files:
        cntms.append(np.loadtxt(file))

    return np.array(cntms)