:py:mod:`hcitools`
==================

.. py:module:: hcitools

.. autoapi-nested-parse::

   .. include:: ../README.md

   # Examples
   .. include:: ../docs/heatmaps.md
   .. include:: ../docs/clustering.md



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   analysis/index.rst
   plot/index.rst
   preprocess/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   hcitools.datasets




.. py:class:: datasets

   Class for loading built-in datasets

   .. py:attribute:: _avail
      

      

   .. py:method:: list_datasets()

      List available built-in datasets


   .. py:method:: load_dataset()

      Load a built-in dataset

      :param `dataset`: One of 'covid', 'caer' or 'ros-mito'
      :type `dataset`: str

      :returns: Desired dataset
      :rtype: pd.DataFrame



