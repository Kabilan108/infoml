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


def isnonemptydir(path: Path) -> bool:
    """Check if a directory is non-empty"""
    return path.is_dir() and len(os.listdir(path)) > 0


def isnonemptyfile(path: Path) -> bool:
    """Check if a file is non-empty"""
    return path.is_file() and path.stat().st_size > 0


def sluggify(text: str, allow_unicode: bool=False) -> str:
    """
    Convert a string to a slug

    Based on Django's slugify function [1]_. This function converts a string to
    a slug. A slug is a string that contains only letters, numbers, underscores
    or hyphens. It is typically used to generate URL-friendly strings.

    Parameters
    ----------
    text : str
        _description_
    allow_unicode : bool, optional
        _description_, by default False

    Returns
    -------
    str
        _description_

    Raises
    ------
    AttributeError
        _description_

    References
    ----------
    .. [1] Django. (n.d.). Django/text.py at main · Django/Django. GitHub. 
           Retrieved January 2, 2023, from 
           https://github.com/django/django/blob/main/django/utils/text.py 
    """

    if not isinstance(text, str):
        raise AttributeError("The input must be a string")

    if allow_unicode:
        text = unicodedata.normalize("NFKC", text)
    else:
        text = (unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("ascii"))

    text = re.sub(r'[^\w.\s-]', '', text).strip().lower()

    return re.sub(r'[-\s]+', '-', text)


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