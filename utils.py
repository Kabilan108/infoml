""" utils.py
General Utility Functions
"""

# Imports
import os
import re
import rich
import string
import shutil
import urllib
import tempfile as temp

# Definitions
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
    if not file: file = 'noname'

    return file


def tempdir(dirname: str):
    """
    Create path to a temporary directory
    """

    name = os.path.join(temp.gettempdir().replace("\\","/"), dirname)
    if not os.path.isdir(name): os.mkdir(name)

    return name


def download(url: str, file: str='', overwrite: bool=False):
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
        file = tempdir() + '/' + sanitizefilename(url.split('?')[0].split('/')[-1])
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