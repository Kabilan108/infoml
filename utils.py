""" utils.py
General Utility Functions
"""

# Imports
import tempfile as temp
import string
import shutil
import urllib
import rich
import re
import os
from itertools import islice


def isnonemptyfile(file: str):
    """
    Does a file exist and is it empty
    """
    return os.path.isfile(file) and os.stat(file).st_size != 0


def sanitizefilename(file):
    """
    Clean up a file name
    https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    """

    valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
    file = ''.join(c for c in file if c in valid_chars)
    if not file:
        file = 'noname'

    return file


def tempdir(dirname: str = 'ToolBox'):
    """
    Create path to a temporary directory
    """

    name = os.path.join(temp.gettempdir().replace("\\", "/"), dirname)
    if not os.path.isdir(name):
        os.mkdir(name)

    return name


def download(url: str, file: str = '', overwrite: bool = False):
    """
    Download files from a URL
    @param url
        URL of file to download
    @param file
        Name of file to write URL to
    @param overwrite
        Should existing files be overwritten
    @return
        path to downloaded file
    """

    # If url is not a vaild URL
    if not re.search(r'^(http[s]?|ftp)', url):
        if not file:
            file = url
            return file
        if not overwrite:
            if isnonemptyfile(file):
                return file
            shutil.copyfile(url, file)
            return file

    if not file:
        file = tempdir() + '/' + \
            sanitizefilename(url.split('?')[0].split('/')[-1])
    elif file.endswith('/'):
        file = file + '/' + sanitizefilename(url)

    if isnonemptyfile(file):
        return file

    file = file.replace('\\', '/').replace('//', '/')

    if not ('/' in file):
        file = tempdir() + '/' + file
        if isnonemptyfile(file):
            return file
        file = file.replace('\\', '/').replace('//', '/')

    # Download file
    urllib.request.urlretrieve(url, file)

    return file


def io_head(file: str, n: int = 5):
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
        for line in islice(f, n):
            if len(line) > 80:
                print(line[:80] + '...')
            else:
                print(line.rstrip())

    return


def color_bool(val: int) -> str:
    """
    Mapping for styling pandas DataFrames
    """
    color = ''
    if val is True:
        color = '#6dcf6d'
    elif val is False:
        color = '#ff5862'

    return f'background-color: {color}'
