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
from . import CONFIG


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


def slugify(text: str, allow_unicode: bool=False) -> str:
    """
    Convert a string to a slug

    Based on Django's slugify function [1]_. This function converts a string to
    a slug. A slug is a string that contains only letters, numbers, underscores
    or hyphens. It is typically used to generate URL-friendly strings.

    Parameters
    ----------
    text : str
        The string to be sluggified
    allow_unicode : bool, optional
        Should unicode characters be permitted, by default False

    Returns
    -------
    str
        The sluggified string

    Raises
    ------
    AttributeError
        The input must be a string

    Examples
    --------
    >>> slugify("Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/")
    'jack-jill-like-numbers-123-and-4-and-silly-characters'

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


def downloadurl(url: str, file: str | Path=CONFIG.tempdir(), 
                overwrite: bool=False, progress: bool=True) -> Path:
    """
    Download and save file from a given URL

    Modified from `bmes.downloadurl` by Ahmet Sacan.

    Parameters
    ----------
    url : str
        The URL to download the file from
    file : str, optional
        Path to file (or directory) where downloaded file will be stored, by 
        default the file will be saved to a temporary directory
    overwrite : bool, optional
        Should existing files be overwritten, by default False
    progress : bool, optional
        Should a progress bar be displayed, by default True

    Returns
    -------
    Path
        Path to downloaded file

    Raises
    ------

    Examples
    --------

    """

    # Convert file to Path object
    file = Path(file)

    # If URL is not a remote address, assume it is a local file
    if not re.search(r'(http[s]?|ftp):\/\/', url):
        if not Path(url).exists():
            raise FileNotFoundError(f"File {url} does not exist")
        if not overwrite:
            if Path(file).exists():
                raise FileExistsError(f"File {file} already exists")
            shutil.copyfile(url, file)
            return Path(file)

    # Get file name from URL
    if file.is_dir():
        fname = slugify(url.split('?')[0].split('/')[-1])
        file = (file / fname).resolve()
    else:
        file = file.resolve()

    # Return file if it exists and overwrite is False
    if isnonemptyfile(file) and not overwrite:
        return file

    # Download the file
    r = requests.get(url, stream=True, allow_redirects=True, timeout=(3, 30))
    if r.status_code == 200:
        size = int(r.headers.get("content-length", 0))

        if progress:
            with open(file, "wb") as stream:
                with tqdm(
                    total=size, unit="B", unit_scale=True, desc=file.name,
                    leave=False, dynamic_ncols=True, initial=0
                ) as pbar:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            stream.write(chunk)
                            pbar.update(len(chunk))

        else:
            with open(file, "wb") as stream:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        stream.write(chunk)

    elif r.status_code == 404:
        raise FileNotFoundError(f"File {url} does not exist")
    else:
        raise ConnectionError(f"{r.status_code}: Could not download file {url}")

    return file


# Define module I/O
__all__ = [
    "ispc",
    "isnonemptydir",
    "isnonemptyfile",
    "slugify",
    "downloadurl",
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