"""
Collection of useful python functions, classes etc.
"""

# Defince computer-specific folders
# TODO: Define paths needed for each submodule
#   Dir for downloading data
#   Dir for temporary data
#   Dir for storing figures
class dirs:
    DATADIR = "/home/kabil/.data"
    TEMPDIR = "/tmp/data/"

# Define visible modules
__all__ = ['analysis', 'binf', 'utils', 'neuro']

# TODO:  Set up cache and data directories for storing data in the long and short term
# TODO: Write clean up scripts for getting rid of cached data (pickles)