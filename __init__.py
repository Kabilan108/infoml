"""
Collection of useful python functions, classes etc.
"""

# Defince computer-specific folders
class dirs:
    DATADIR = "/home/kabil/.data"
    TEMPDIR = "/tmp/data/"

# Define visible modules
__all__ = ['analysis', 'binf', 'utils', 'neuro']

# TODO:  Set up cache and data directories for storing data in the long and short term
# TODO: Write clean up scripts for getting rid of cached data (pickles)