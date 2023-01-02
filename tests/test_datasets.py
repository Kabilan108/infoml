"""
Tests for the `infoml.datasets` module.
"""

import pytest
import gzip


def test_get_ceman_counts():
    """
    Test the function `get_ceman_counts`.
    """
    from infoml.datasets import get_ceman_counts

    assert get_ceman_counts().exists()

    with gzip.open(get_ceman_counts()) as f:
        lines = f.readlines()
    assert len(lines) == 23369
