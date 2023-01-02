"""
Tests for the `infoml.utils` module.
"""

import pytest


def test_ispc():
    """Test the function `ispc`."""
    from infoml.utils import ispc

    assert isinstance(ispc(), bool)


def test_isnonemptydir():
    """Test the function `isnonemptydir`."""
    from infoml.utils import isnonemptydir
    from pathlib import Path

    assert isinstance(isnonemptydir(Path()), bool)


def test_isnonemptyfile():
    """Test the function `isnonemptyfile`."""
    from infoml.utils import isnonemptyfile
    from pathlib import Path

    assert isinstance(isnonemptyfile(Path()), bool)


def test_slugify():
    """Test the function `sluggify`."""
    from infoml.utils import slugify

    text = " Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/"
    assert isinstance(slugify(text), str)
    assert (
        slugify(text) == "jack-jill-like-numbers-123-and-4-and-silly-characters",
        "The sluggified text is not correct",
    )  # type: ignore

    text = "S'mores are delicious"
    assert isinstance(slugify(text), str)
    assert (
        slugify(text) == "smores-are-delicious",
        "The sluggified text is not correct",
    )  # type: ignore


# TODO: Write tests for the `infoml.utils.SQLite` class
