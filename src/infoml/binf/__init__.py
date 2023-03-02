"""
infoml.binf
-----------

This sub-package contains functions for bioinformatics.
"""

from . import data


if __name__ == "__main__":
    print("This module is not intended to be run directly.")
else:
    # Define module I/O
    __all__ = [
        "data",
    ]
    __all__ += [m for m in dir() if m.startswith("__")]

    def __dir__():
        """Override dir() to only show public attributes."""
        return __all__

    def __getattr__(name):
        """Override getattr() to only show public attributes."""
        if name in __all__:
            return globals()[name]
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
