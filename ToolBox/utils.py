""" utils.py
General Utility Functions
"""

# Imports
import rich
import os


# Definitions
def io_head(file: str, n: int=5):
    """
    Print the first n rows in a text file.
    @param file
        Name (and path) of file to read
    @param n
        Number of lines to print
    """
    # Verify that file exists
    if not os.path.exists(file):
        rich.print("[red bold]ERROR:[/red bold] File Not Found.")
        return

    # Read and print file
    with open(file, 'r') as f:
        for _ in range(n):
            print(f.readline().strip())

    return