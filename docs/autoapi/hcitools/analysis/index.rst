:py:mod:`hcitools.analysis`
===========================

.. py:module:: hcitools.analysis

.. autoapi-nested-parse::

   This module contains functions and classes for performing statistical analysis
   and machine learning



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   hcitools.analysis.dim_reduction



Attributes
~~~~~~~~~~

.. autoapisummary::

   hcitools.analysis.RANDOMSTATE


.. py:data:: RANDOMSTATE
   :annotation: = 69

   

.. py:function:: dim_reduction(data, method=['pca', 'tsne', 'umap'], pca_kws=None, tsne_kws=None, umap_kws=None)

   Perform dimensionality reduction on data

   :param `data`: Data frame of features. Should only contain numeric columns.
                  Metadata can be stored in the index
   :type `data`: pd.DataFrame
   :param `method`: Method(s) to use for dimensionality reduction,
                    by default ['pca', 'tsne', 'umap']
   :type `method`: str or list, optional
   :param `{pca: Arguments for the estimators, by default None
   :type `{pca: dict, optional
   :param tsne: Arguments for the estimators, by default None
   :type tsne: dict, optional
   :param umap}_kws`: Arguments for the estimators, by default None
   :type umap}_kws`: dict, optional

   :returns: * *pd.DataFrame* -- Data frame of low-dimensional projections
             * *np.array* -- Only if 'pca' in method, list of explained variances


