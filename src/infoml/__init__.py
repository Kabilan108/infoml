"""
infoml
------

`infoml` is a Python package for perfoming bioinformatics analysis and machine 
learning tasks on genomic and bioimaging data.
"""

# Import modules
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


    def cache(self, new_path: Path | str=""):
        """Cache directory"""

        if new_path:
            self.__cache = Path(new_path)

            if not self.__cache.exists():
                self.__cache.mkdir(parents=True)

        return self.__cache


    def datadir(self, new_path: Path | str=""):
        """Data directory"""

        if new_path:
            self.__datadir = Path(new_path)

            if not self.__datadir.exists():
                self.__datadir.mkdir(parents=True)

        return self.__datadir


    def tempdir(self, new_path: Path | str=""):
        """Temporary directory"""

        if new_path:
            self.__tempdir = Path(new_path)

            if not self.__tempdir.exists():
                self.__tempdir.mkdir(parents=True)

        return self.__tempdir


class dirs:
    DATADIR = "/home/kabil/.data"
    TEMPDIR = "/tmp/data/"


# TODO: Create a function to auto clean any cache files

# FEAT: Make modules accessible from the main module

# Define package version
from importlib.metadata import version

__version__ = version("infoml")

# Define visible modules
# __all__ = ['analysis', 'binf', 'utils', 'neuro']
