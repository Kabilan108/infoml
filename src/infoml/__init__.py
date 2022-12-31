"""
infoml
======

infoml is a Python package for perfoming bioinformatics analysis and machine learning
tasks on genomic and bioimaging data.
"""

# TODO: Create CONFIG class
#   Create a dataclass that will store configuration information for the package

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
