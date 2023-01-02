"""
infoml.utils
-----------

This module contains utility functions for the infoml package.
"""

# Imports from standard library
from pathlib import Path
import os, pickle, platform, re, shutil, sqlite3, tempfile, unicodedata

# Imports from third party packages
from pandas import DataFrame
from tqdm.auto import tqdm
from rich import print
import requests

# Imports from local source
from .utils import CONFIG


def ispc() -> bool:
    """Check if the current platform is Windows"""
    system = platform.system()
    return system == "Windows" or system.startswith("CYGWIN")


# Define module I/O
__all__ = [
    "ispc",
]
__all__ += [m for m in dir() if m.startswith("__")]


def __dir__():
    """Override default dir() behavior"""
    return __all__


def __getattr__(name):
    """Override default getattr() behavior"""
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return globals()[name]