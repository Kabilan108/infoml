"""
infoml
------

`infoml` is a Python package for perfoming bioinformatics analysis and machine 
learning tasks on genomic and bioimaging data.
"""

# Imports from standard library
from importlib.metadata import version
from pathlib import Path
import tempfile


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

    def cache(self, new_path: Path | str = ""):
        """Cache directory"""

        if new_path:
            self.__cache = Path(new_path)

            if not self.__cache.exists():
                self.__cache.mkdir(parents=True)

        return self.__cache

    def datadir(self, new_path: Path | str = ""):
        """Data directory"""

        if new_path:
            self.__datadir = Path(new_path)

            if not self.__datadir.exists():
                self.__datadir.mkdir(parents=True)

        return self.__datadir

    def tempdir(self, new_path: Path | str = ""):
        """Temporary directory"""

        if new_path:
            self.__tempdir = Path(tempfile.gettempdir()) / new_path

            if not self.__tempdir.exists():
                self.__tempdir.mkdir(parents=True)

        return self.__tempdir


# Export modules
CONFIG = config()
from . import datasets
from . import utils


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
