"""
infoml.binf.data
----------------

This module contains functions for downloading data from bioinformatics
repositiories like Gene Expression Omnibus and the Curated Microarray Database.
"""

# Imports from standard library
from pathlib import Path
from typing import Union
import warnings
import pickle
import json
import re
import os

# Imports from third party packages
from GEOparse.GEOTypes import GPL, GSE
from GEOparse import get_GEO
from tqdm.auto import tqdm
from rich import print
import pandas as pd
import numpy as np

# Imports from local source
from ..utils import CONFIG
