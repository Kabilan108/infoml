"""
datasets
--------

This module contains functions to get the paths to the datasets used in the
"""

# Imports
from numpy import ndarray, loadtxt
from importlib import resources
from typing import Tuple
import gzip


def get_ceman_counts():
    """
    Get path the GSE50499 [1]_ gene counts matrix.

    Returns
    -------
    pathlib.PosixPath
        Path to file

    References
    ----------
    .. [1] Kenny PJ, Zhou H, Kim M, Skariah G et al. MOV10 and FMRP regulate
           AGO2 association with microRNA recognition elements. Cell Rep 2014
           Dec 11;9(5):1729-1741. PMID: 25464849
    """

    with resources.path("infoml.data", "GSE50499_GEO_Ceman_counts.txt.gz") as f:
        datapath = f
    return datapath


def load_boston() -> Tuple[ndarray, ndarray, list]:
    """
    Load the Boston Housing dataset [1]_ for house porice prediction.

    Columns
    -------
    `CRIM`: per capita crime rate by town
    `ZN`: proportion of residential land zoned for lots over 25,000 sq.ft.
    `INDUS`: proportion of non-retail business acres per town
    `CHAS`: Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
    `NOX`: nitric oxides concentration (parts per 10 million)
    `RM`: average number of rooms per dwelling
    `AGE`: proportion of owner-occupied units built prior to 1940
    `DIS`: weighted distances to five Boston employment centres
    `RAD`: index of accessibility to radial highways
    `TAX`: full-value property-tax rate per $10,000
    `PTRATIO`: pupil-teacher ratio by town
    `B`: 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
    `LSTAT`: % lower status of the population
    `MEDV`: Median value of owner-occupied homes in $1000's

    Returns
    -------
    Tuple[ndarray, ndarray, list]
        Tuple of (X, y, feature_names) where X is the input data, y is the
        target variable, and feature_names is the list of feature names.

    References
    ----------
    .. [1] Harrison, Jr., David, Rubinfeld, Daniel L. (1978/03)."Hedonic housing
           prices and the demand for clean air." Journal of Environmental
           Economics and Management 5(1): 81-102.
    """

    with resources.path("infoml.data", "boston-housing.txt.gz") as f:
        datapath = f
        with gzip.open(datapath, "rt") as f:
            rows = f.readlines()
            feature_names = rows[23].strip().split("\t")
            data = loadtxt(datapath, skiprows=24)

    X = data[:, :-1]
    y = data[:, -1]
    return X, y, feature_names
