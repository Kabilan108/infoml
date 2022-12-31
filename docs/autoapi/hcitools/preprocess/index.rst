:py:mod:`hcitools.preprocess`
=============================

.. py:module:: hcitools.preprocess

.. autoapi-nested-parse::

   This module contains functions for data preprocessing



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   hcitools.preprocess.drop_high_corr
   hcitools.preprocess.drop_low_variance
   hcitools.preprocess._printif
   hcitools.preprocess._intersperse
   hcitools.preprocess.clean_data
   hcitools.preprocess.normalize



.. py:function:: drop_high_corr(data, thresh=0.95, method='pearson')

   Remove features with correaltions above a threshold from a data frame.

   :param `data`: Original data frame
   :type `data`: pd.DataFrame
   :param `thresh`: Correlation threshold, by default 0.95
   :type `thresh`: float, optional
   :param `method`: Either 'pearson' or 'spearman', by default 'pearson'
   :type `method`: str, optional

   :returns: * *pd.DataFrame* -- Data frame without highly correlated features
             * *dict* -- Keys = features still in data frame
               Values = list of highly correlated features


.. py:function:: drop_low_variance(data, thresh=0.0, na_replacement=-999)

   Remove low-variance features from a data frame

   :param `data`: Original data frame
   :type `data`: pd.DataFrame
   :param `thresh`: Variance threshold, by default 0.0
   :type `thresh`: float, optional
   :param `na_replacement`: Replacement value for NAs, by default -999
   :type `na_replacement`: int, optional

   :returns: Data frame without low-variance features
   :rtype: pd.DataFrame


.. py:function:: _printif(cond, *args, **kwargs)

   Print if cond is true


.. py:function:: _intersperse(array, item)

   Insert item between each item in an array


.. py:function:: clean_data(data, metacols, dropna=False, drop_low_var=None, corr_thresh=None, corr_method='pearson', intens_norm=False, intens_rgx='Intensity', num_objs='number of objects', verbose=False)

   Perform preprocessing steps on a high-content imaging data

   :param `data`: Original data frame
   :type `data`: pd.DataFrame
   :param `metacols`: List of non-numeric columns in data frame
   :type `metacols`: list
   :param `dropna`: Drop NA-only columns and any rows with NAs, by default False
   :type `dropna`: bool, optional
   :param `drop_low_var`: Threshold for dropping low variance features, by default None
   :type `drop_low_var`: float, optional
   :param `corr_thresh`: Threshold for dropping highly correlated features, by default None
   :type `corr_thresh`: float, optional
   :param `corr_method`: Correlation method, by default 'spearman'
   :type `corr_method`: str, optional
   :param `intens_norm`: Should intensity-based features be normalized, by default False
   :type `intens_norm`: bool, optional
   :param `intens_rgx`: Regular expression for identifying intensity based features,
                        by default `r'Intensity'`
   :type `intens_rgx`: str, optional
   :param `num_objs`: Feature definining object counts, by default 'number of objects'
   :type `num_objs`: str, optional
   :param `verbose`: Should a log of processing steps be returned, by default False
   :type `verbose`: bool, optional

   :returns: * *pd.DataFrame* -- Preprocessed data
             * *list* -- Only if `verbose == True`, preprocessing log


.. py:function:: normalize(df, method='minmax')

   Normalize a data frame

   :param df: Original data frame
   :type df: pd.DataFrame
   :param method: Either 'minmax' or 'z', by default 'minmax'
   :type method: str, optional

   :returns: Normalized data frame
   :rtype: pd.DataFrame

   :raises NotImplementedError: If method isn't 'minmax' or 'z'


