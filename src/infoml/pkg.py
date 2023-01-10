"""
infoml.pkg
----------

This module contains functions for managing - install, uninstall, check - 
python packages with both `pip` and `conda`.
"""

# Imports from standard library
import sys

# Imports from local source
from .utils import system


def check_package(importname: str) -> bool:
    """
    Check if a package is installed.

    Parameters
    ----------
    importname : str
        Name used when importing the package

    Returns
    -------
    bool
        True if package is installed, False otherwise
    """

    try:
        __import__(importname)
    except ImportError:
        return False

    return True


def pipinstall(
    packagename: str,
    importname: str = "",
    version: str = "",
    reinstall: bool = False,
) -> None:
    """
    Install a python package with `pip`.

    Modified from the `bmes` package by Ahmet Sacan.

    Parameters
    ----------
    packagename : str, optional
        Name used for installing the package
    importname : str
        Name used when importing the package, by default None
        In most cases, this is identical to `packagename` but both must be
        provided when they are different.
    version : str, optional
        Version of the package to install, by default None
    reinstall : bool, optional
        Should the package be reinstalled, by default False

    Examples
    --------
    >>> pipinstall('numpy');
    >>> pipinstall('pandas', version='1.0.0');
    >>> pipinstall('biopython', 'Bio')
    """

    # Function for construction commands
    def __construct_cmd():
        if version is None:
            cmd = f"{sys.executable} -m pip install -U {packagename}"
        else:
            cmd = f"{sys.executable} -m pip install -U {packagename}=={version}"
        return cmd

    # Set the import name
    importname = importname or packagename

    # Check if the package is already installed
    if check_package(importname):
        if reinstall:
            print(f"Reinstalling {packagename}...")
            pipuninstall(packagename, importname)
        else:
            print(f"{packagename} is already installed.")
            return

    # Install the package
    out = system(__construct_cmd())
    known_errors = [
        "ERROR: Could not install packages",
        "Consider using the `--user` option",
    ]

    # Try again with `--user` option
    if known_errors[0] in str(out) and known_errors[1] in str(out):
        out = system(__construct_cmd() + " --user")

    # Check if package was installed
    if check_package(importname):
        print(f"{packagename} is installed.")
    else:
        print(f"{packagename} could not be installed.")
        print(out)

    return


def pipuninstall(packagename: str, importname: str = "") -> None:
    """
    Uninstall a python package with `pip`.

    Parameters
    ----------
    packagename : str
        Name used for installing the package
    importname : str, optional
        Name used when importing the package, by default None
        In most cases, this is identical to `packagename` but both must be
        provided when they are different.

    Examples
    --------
    >>> pipuninstall('numpy');
    """

    # Set the import name
    importname = importname or packagename

    # Check if the package is installed
    if not check_package(importname):
        print(f"{packagename} is not installed.")
        return

    # Uninstall the package
    out = system(f"{sys.executable} -m pip uninstall -y {packagename}")

    # Check if package was uninstalled
    if not check_package(importname):
        print(f"{packagename} is uninstalled.")
    else:
        print(f"{packagename} could not be uninstalled.")
        print(out)

    return


if __name__ == "__main__":
    print("This module is not intended to be run directly.")
else:
    # Define module I/O
    __all__ = [
        "check_package",
        "pipinstall",
        "pipuninstall",
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
