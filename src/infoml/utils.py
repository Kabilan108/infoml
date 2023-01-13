"""
infoml.utils
------------

This module contains utility functions for the infoml package.
Some of these functions are modified from the bmes package by Dr. Ahmet Sacan.
"""

# Imports from standard library
from tempfile import NamedTemporaryFile
from zipfile import ZipFile as zopen
from unicodedata import normalize
from itertools import islice
from shutil import copyfile
from pathlib import Path
import os, platform, re, sqlite3, subprocess

# Imports from third party packages
from pandas import DataFrame
from tqdm.auto import tqdm
from rich import print
import requests

# Imports from local source
from . import CONFIG


def ispc() -> bool:
    """Check if the current platform is Windows"""
    system = platform.system()
    return system == "Windows" or system.startswith("CYGWIN")


def isnonemptydir(path: Path | str) -> bool:
    """Check if a directory is non-empty"""
    path = Path(path)
    return path.is_dir() and len(os.listdir(path)) > 0


def isnonemptyfile(path: Path | str) -> bool:
    """Check if a file is non-empty"""
    path = Path(path)
    return path.is_file() and path.stat().st_size > 0


def tempfile(filename: str = "") -> Path:
    """Get a temporary file path"""
    if not filename:
        with NamedTemporaryFile() as f:
            filename = f.name
    return CONFIG.tempdir() / filename


def unzip(file: str | Path, dest: str | Path = ""):
    """
    Unzip a file

    Parameters
    ----------
    file : str | Path
        Path to the file to be unzipped
    dest : str | Path, optional
        Path to the destination directory, by default ''
    """

    # Convert file to Path
    file = Path(file)

    # Define destination directory
    if not dest:
        dest = CONFIG.tempdir() / Path(file).stem
        if not dest.exists():
            dest.mkdir(parents=True)
    else:
        dest = Path(dest)

    with zopen(file, "r") as zip:
        zip.extractall(dest)


def slugify(text: str, allow_unicode: bool = False) -> str:
    """
    Convert a string to a slug

    Based on Django's slugify function [1]_. This function converts a string to
    a slug. A slug is a string that contains only letters, numbers, underscores
    or hyphens. It is typically used to generate URL-friendly strings.

    Parameters
    ----------
    text : str
        The string to be sluggified
    allow_unicode : bool, optional
        Should unicode characters be permitted, by default False

    Returns
    -------
    str
        The sluggified string

    Raises
    ------
    AttributeError
        The input must be a string

    Examples
    --------
    >>> slugify("Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/")
    'jack-jill-like-numbers-123-and-4-and-silly-characters'

    References
    ----------
    .. [1] Django. (n.d.). Django/text.py at main · Django/Django. GitHub.
           Retrieved January 2, 2023, from
           https://github.com/django/django/blob/main/django/utils/text.py
    """

    if not isinstance(text, str):
        raise AttributeError("The input must be a string")

    if allow_unicode:
        text = normalize("NFKC", text)
    else:
        text = normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    text = re.sub(r"[^\w.\s-]", "", text).strip().lower()

    return re.sub(r"[-\s]+", "-", text)


def downloadurl(
    url: str,
    file: str | Path = CONFIG.tempdir(),
    overwrite: bool = False,
    progress: bool = True,
) -> Path:
    """
    Download and save file from a given URL

    Parameters
    ----------
    url : str
        The URL to download the file from
    file : str, optional
        Path to file (or directory) where downloaded file will be stored, by
        default the file will be saved to a temporary directory
    overwrite : bool, optional
        Should existing files be overwritten, by default False
    progress : bool, optional
        Should a progress bar be displayed, by default True

    Returns
    -------
    Path
        Path to downloaded file

    Raises
    ------
    FileNotFoundError
        If the file does not exist
    FileExistsError
        If the file already exists and overwrite is False
    ConnectionError
        If the URL is not valid

    Examples
    --------
    >>> downloadurl("https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png")
    PosixPath('/tmp/googlelogo_color_272x92dp.png')
    """

    # Convert file to Path object
    file = Path(file)

    # If URL is not a remote address, assume it is a local file
    if not re.search(r"(http[s]?|ftp):\/\/", url):
        if not Path(url).exists():
            raise FileNotFoundError(f"File {url} does not exist")
        if not overwrite:
            if Path(file).exists():
                raise FileExistsError(f"File {file} already exists")
            copyfile(url, file)
            return Path(file)

    # Get file name from URL
    if file.is_dir():
        fname = slugify(url.split("?")[0].split("/")[-1])
        file = (file / fname).resolve()
    else:
        file = file.resolve()

    # Return file if it exists and overwrite is False
    if isnonemptyfile(file) and not overwrite:
        return file

    # Download the file
    # TODO: See if urllib.request.urlretrieve can be used instead
    r = requests.get(url, stream=True, allow_redirects=True, timeout=(3, 30))
    if r.status_code == 200:
        size = int(r.headers.get("content-length", 0))

        if progress:
            with open(file, "wb") as stream:
                with tqdm(
                    total=size,
                    unit="B",
                    unit_scale=True,
                    desc=file.name,
                    leave=False,
                    dynamic_ncols=True,
                    initial=0,
                ) as pbar:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            stream.write(chunk)
                            pbar.update(len(chunk))

        else:
            with open(file, "wb") as stream:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        stream.write(chunk)

    elif r.status_code == 404:
        raise FileNotFoundError(f"File {url} does not exist")
    else:
        raise ConnectionError(f"{r.status_code}: Could not download file {url}")

    return file


class SQLite:
    """
    Wrapper for connecting to and querying SQLite databases

    Attributes
    ----------
    file : Path
        Path to SQLite database file
    conn : sqlite3.Connection
        Connection to SQLite database

    Methods
    -------
    execute(query: str, *args, **kwargs) -> sqlite3.Cursor
        Execute a query on the database
    select(query: str, *args, **kwargs) -> list[sqlite3.Row]
        Execute a query on the database and return the results as a DataFrame
    insert(table: str, data: dict, **kwargs) -> None
        Insert data into a table
    is_table(table: str) -> bool
        Check if a table exists in the database
    drop(table: str) -> None
        Drop a table from the database
    tables() -> dict
        Return a list of tables in the database and their schema
    close() -> None
        Close the connection to the database
    """

    def __init__(self, file: str | Path, quiet: bool = False, **kwargs) -> None:
        """Initialize SQLite class"""

        self.file = Path(file).resolve()
        if not self.file.suffix and not self.file.is_dir():
            self.file = self.file.with_suffix(".db")
        self.conn = sqlite3.connect(self.file, **kwargs)
        self.conn.row_factory = sqlite3.Row
        self.quiet = quiet
        if self.quiet:
            print(f"Connected to {self.file.name}")

    def __enter__(self):
        """Enter context manager"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context manager"""
        self.conn.commit()
        self.conn.close()

    def __repr__(self) -> str:
        """Return string representation of SQLite class"""
        return f"{self.__class__.__name__}({self.file})"

    def __str__(self) -> str:
        """Return string representation of SQLite class"""
        return f"{self.__class__.__name__}({self.file})"

    def execute(self, query: str, *args, **kwargs) -> sqlite3.Cursor | DataFrame | None:
        """
        Execute a query

        Parameters
        ----------
        query : str
            Query to execute

        Returns
        -------
        sqlite3.Cursor
            Cursor object

        Raises
        ------
        AttributeError
            If the input is not a string

        Examples
        --------
        >>> db = SQLite("test.db")
        >>> db.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
        <sqlite3.Cursor object at 0x7f8b8c0b0e00>
        >>> db.execute("INSERT INTO test (name) VALUES ('John')")
        <sqlite3.Cursor object at 0x7f8b8c0b0e00>
        >>> db.execute("INSERT INTO test (name) VALUES ('Jane')")
        <sqlite3.Cursor object at 0x7f8b8c0b0e00>
        >>> db.close()
        """

        if not isinstance(query, str):
            raise AttributeError("The input must be a string")

        if query.upper().strip().startswith("SELECT"):
            return self.select(query, *args, **kwargs)

        try:
            cursor = self.conn.execute(query, *args, **kwargs)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

    def select(self, query: str, *args, **kwargs) -> DataFrame:
        """
        Execute a SELECT query and return the results as a DataFrame

        Parameters
        ----------
        query : str
            Query to execute

        Returns
        -------
        DataFrame
            Results of query

        Raises
        ------
        AttributeError
            If the input is not a string

        Examples
        --------
        >>> db = SQLite("test.db")
        >>> db.select("SELECT * FROM test")
            id  name  age
            0  1  John   30
            1  2  Jane   25
        """

        if not isinstance(query, str):
            raise AttributeError("The input must be a string")

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, *args, **kwargs)
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return DataFrame()

        if len(rows) == 0:
            print("No results found")
            return DataFrame()
        else:
            df = DataFrame(rows)
            df.columns = [col[0] for col in cursor.description]  # type: ignore
            return df

    def insert(self, table: str, data: dict, **kwargs) -> None:
        """
        Insert data into a table

        Parameters
        ----------
        table : str
            Name of table
        data : dict
            Data to insert

        Raises
        ------
        AttributeError
            If the table does not exist
            If the dictionary values are not lists of the same length
            If a database column is missing from the dictionary

        Examples
        --------
        >>> db = SQLite("test.db")
        >>> data = {'name': ['John', 'James', 'Rose', 'Jane'],
                    'age':  [30, 25, 60, 45]}
        >>> db.insert("test", data)
        >>> db.close()
        """

        # Check if table exists
        if not self.is_table(table):
            raise AttributeError(f"Table '{table}' does not exist")

        # Dictionary values must be lists of the same length
        if not all(len(v) == len(data[list(data.keys())[0]]) for v in data.values()):
            raise AttributeError("Dictionary values must be lists of the same length")
        nrows = len(data[list(data.keys())[0]])

        # Get column information
        info = self.select(f"PRAGMA table_info({table})")
        columns = info["name"].tolist()
        types = info["pk"].tolist()

        # Check if all columns are present (except for autoincrementing columns)
        for col, type in zip(columns, types):
            if col not in data and type == 0:
                raise AttributeError(f"Column '{col}' is missing")

        # Execute queries
        for _, vals in zip(range(nrows), zip(*list(data.values()))):
            cols = ", ".join(data.keys())
            subs = ", ".join("?" * len(data))
            query = f"INSERT INTO {table} ({cols}) VALUES ({subs})"
            self.execute(query, vals, **kwargs)

    def is_table(self, table: str) -> bool:
        """
        Check if a table exists in the database

        Parameters
        ----------
        table : str
            Name of table

        Returns
        -------
        bool
            True if table exists, False otherwise

        Examples
        --------
        >>> db = SQLite("test.db")
        >>> db.is_table("test")
        True
        >>> db.is_table("foo")
        False
        """

        try:
            self.select(
                ("SELECT name FROM sqlite_master " "WHERE type='table' AND name=?"),
                (table,),
            )
        except sqlite3.OperationalError:
            return False

        return True

    def drop(self, table: str) -> None:
        """
        Drop a table from the database

        Parameters
        ----------
        table : str
            Name of table

        Examples
        --------
        >>> db = SQLite("test.db")
        >>> db.drop("test")
        """

        self.execute(f"DROP TABLE {table}")

    def tables(self) -> dict:
        """
        List all tables in the database and their schema

        Returns
        -------
        dict
            Dictionary of table names and their schema

        Examples
        --------
        >>> db = SQLite("test.db")
        >>> db.tables()
        {'test': 'CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)'}
        """

        tables = {}
        for row in self.select(
            ("SELECT name, sql FROM sqlite_master " "WHERE type='table'")
        ):
            tables[row["name"]] = row["sql"]  # type: ignore
        return tables

    def close(self) -> None:
        """Close the database connection"""

        self.conn.commit()
        self.conn.close()
        if self.quiet:
            print(f"Closed connection to {self.file.name}")


def iohead(file: str, n: int = 5) -> None:
    """
    Print the first n rows of a text file

    Parameters
    ----------
    file : str
        Name of file
    n : int, optional
        Number of rows to print
    """

    # Check if file exists
    if not isnonemptyfile(file):
        print("[red bold]ERROR:[/red bold] File not found.")
        return

    # Read and print file
    with open(file, "r") as f:
        for line in islice(f, n):
            if len(line) > 80:
                print(line[:80] + "...")
            else:
                print(line.rstrip())

    return


def system(
    command: str,
    stdout: str | None = None,
    stderr: str | None = None,
    quiet: bool = False,
    *args,
    **kwargs,
) -> str:
    """
    Run a system command; allows you to redirect stdout and stderr.

    Parameters
    ----------
    command : str
        Command to run
    stdout : str, optional
        File to redirect stdout to, by default ''
    stderr : str, optional
        File to redirect stderr to, by default ''
    quiet : bool, optional
        Suppress output, by default False

    Returns
    -------
    str
        Output from the command
    """

    if not quiet:
        print("[green bold]RUNNING:[/green bold] " + command)

    try:
        if stdout:
            command += f" > {stdout}"

        if stderr:
            command += f" 2> {stderr}"
        else:
            stderr = subprocess.STDOUT  # type: ignore

        out = subprocess.check_output(
            command,
            stderr=stderr,  # type: ignore
            shell=True,
            *args,
            **kwargs,  # type: ignore
        )
    except subprocess.CalledProcessError as E:
        out = E.output.decode()

    if not quiet:
        print(out.decode())

    return out.decode()


if __name__ == "__main__":
    print("This module is not intended to be run directly.")
else:
    # Define module I/O
    __all__ = [
        "ispc",
        "isnonemptydir",
        "isnonemptyfile",
        "tempfile",
        "unzip",
        "slugify",
        "downloadurl",
        "SQLite",
        "iohead",
        "system",
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
