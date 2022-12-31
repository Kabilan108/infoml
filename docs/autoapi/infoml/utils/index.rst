:py:mod:`infoml.utils`
======================

.. py:module:: infoml.utils

.. autoapi-nested-parse::

   utils.py
   General Utility Functions



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   infoml.utils.isnonemptyfile
   infoml.utils.sanitizefilename
   infoml.utils.tempdir
   infoml.utils.download
   infoml.utils.io_head
   infoml.utils.color_bool



.. py:function:: isnonemptyfile(file: str)

   Does a file exist and is it empty


.. py:function:: sanitizefilename(file)

   Clean up a file name
   https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename


.. py:function:: tempdir(dirname: str = 'ToolBox')

   Create path to a temporary directory


.. py:function:: download(url: str, file: str = '', overwrite: bool = False)

   Download files from a URL
   @param url
       URL of file to download
   @param file
       Name of file to write URL to
   @param overwrite
       Should existing files be overwritten
   @return
       path to downloaded file


.. py:function:: io_head(file: str, n: int = 5)

   Print the first n rows in a text file.
   @param file
       Name (and path) of file to read
   @param n
       Number of lines to print


.. py:function:: color_bool(val: int) -> str

   Mapping for styling pandas DataFrames


