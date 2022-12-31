:py:mod:`infoml.binf.binf`
==========================

.. py:module:: infoml.binf.binf

.. autoapi-nested-parse::

   alg.py
   Bioinformatics Algorithms
   These are methods, functions and classes that I've used for different
   Bioinformatics Applications including custom implementation of certain
   algorithms.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   infoml.binf.binf.BWT



Functions
~~~~~~~~~

.. autoapisummary::

   infoml.binf.binf.swalign
   infoml.binf.binf.nwalign
   infoml.binf.binf.geodlparse
   infoml.binf.binf.targetscandb



.. py:class:: BWT

   A simple implementation of the Burrows-Wheeler Transform

   .. py:method:: transform() -> str


   .. py:method:: inverse() -> str



.. py:function:: swalign(a: str, b: str, gap: int = -5, scoreonly: bool = False, submat: Bio.Align.substitution_matrices.Array = None, identonly: bool = False) -> Union[int, float, dict]

   This is a custom implementation of the Smith-Waterman Local Sequence
   Alignment Algorithm.
   Based on a code written by Dr. Ahmet Sacan <ahmetmsacan@gmail.com>
   Uses the Dynamic Programming algorithm to obtain an optimal sequence
   alignment.
   This function only supports linear gap penalties.
   @param a: str, b: str
       Sequences to align
   @param gap: int
       Gap score
   @param submat: Align.substitution_matrices.Array
       Scoring matrix (BLOSUM62 is the default)
   @param scoreonly: bool
       Return alignment score only
   @param identonly: bool
       Return percent identity only
   @return
       Alignment score, percent identiy, and or alignment


.. py:function:: nwalign(a: str, b: str, match: int = 1, mismatch: int = -1, gap: int = -2, score_only: bool = False, ident_only: bool = False, alphabet: str = 'nt', submat: Bio.Align.substitution_matrices.Array = None, penalize_end_gaps=False) -> Union[int, float, dict]

   Custom implementation of the Needleman-Wunsch algorithm


.. py:function:: geodlparse(acc: str, limit_runs: int = 1)

   Download, parse and cache data from GEO

   @param acc
       GEO accession
   @param limit_runs
       Number of runs to retrieve for each SRX
   @return
       parsed GEO data


.. py:function:: targetscandb(mirna: str, scorethr: float = 0.8, db: str = 'mir2target')

   Retreive data from a table in the TargetScan Database


