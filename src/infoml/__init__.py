"""
infoml
------

`infoml` is a Python package for perfoming bioinformatics analysis and machine
learning tasks on genomic and bioimaging data.
"""

# Imports from standard library
from importlib.metadata import version
from socket import gethostname
from pathlib import Path
from rich import print
import sys, tempfile


class config:
    """
    Configuration class for infoml package

    Methods
    -------
    cache : pathlib.PosixPath
        Path to the cache directory. This will be the default location for
        storing cached data.
    datadir : pathlib.PosixPath
        Path to the data directory. This will be the default location for
        storing downloaded data.
    tempdir : pathlib.PosixPath
        Path to the temporary directory. This will be the default location for
        storing temporary files.

    Examples
    --------
    >>> from infoml import CONFIG
    >>> CONFIG.DATADIR
    PosixPath('/home/kabil/.data/infoml')
    >>> # Change the default data directory
    >>> CONFIG.DATADIR = "./data"
    """

    __cache = Path.home() / ".cache" / "infoml"
    __datadir = Path.home() / ".data" / "infoml"
    __tempdir = Path(tempfile.gettempdir()) / "infoml"

    def __init__(self):
        """Initialize the configuration class"""

        if not self.__cache.exists():
            self.__cache.mkdir(parents=True)

        if not self.__datadir.exists():
            self.__datadir.mkdir(parents=True)

        if not self.__tempdir.exists():
            self.__tempdir.mkdir(parents=True)

    def cache(self, new_path: Path | str = "") -> Path:
        """Cache directory"""

        if new_path:
            self.__cache = Path(new_path)

            if not self.__cache.exists():
                self.__cache.mkdir(parents=True)

        return self.__cache

    def datadir(self, new_path: Path | str = "") -> Path:
        """Data directory"""

        if new_path:
            self.__datadir = Path(new_path)

            if not self.__datadir.exists():
                self.__datadir.mkdir(parents=True)

        return self.__datadir

    def tempdir(self, new_path: Path | str = "") -> Path:
        """Temporary directory"""

        if new_path:
            self.__tempdir = Path(tempfile.gettempdir()) / new_path

            if not self.__tempdir.exists():
                self.__tempdir.mkdir(parents=True)

        return self.__tempdir

    def sysinfo(self) -> dict:
        """Get System Information"""
        return {
            "host_name": gethostname(),
            "operating_system": sys.platform,
            "python_version": sys.version,
            "python_executable": sys.executable,
            "infoml_version": version("infoml"),
            "infoml_path": Path(__file__).parent.absolute(),
        }

    def __str__(self):
        """String representation of the class"""
        return str(
            dict(
                cache=self.cache(),
                datadir=self.datadir(),
                tempdir=self.tempdir(),
            )
        )

    def __repr__(self):
        """Representation of the class"""
        return str(self)


# Export modules
CONFIG = config()
from . import datasets
from . import utils
from . import pkg
from . import viz
from . import binf


# Deine package version
__version__ = version(__name__)


if __name__ == "__main__":
    print("This module is not intended to be run directly.")
else:
    # Define module I/O
    __all__ = [
        "CONFIG",
        "datasets",
        "utils",
        "pkg",
        "viz",
        "binf",
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
