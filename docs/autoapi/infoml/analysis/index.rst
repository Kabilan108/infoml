:py:mod:`infoml.analysis`
=========================

.. py:module:: infoml.analysis

.. autoapi-nested-parse::

   analysis.py
   These functions come in handy when working on data analysis projects.
   I've mainly used them so far in my work for Dr. Laudanski



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   infoml.analysis.show_dfs
   infoml.analysis.see_distn
   infoml.analysis.rmoutliers
   infoml.analysis.elbow_plot
   infoml.analysis.calculate_pvalues
   infoml.analysis.kmeans
   infoml.analysis.write_dfs
   infoml.analysis.clusterplot



.. py:function:: show_dfs(*args: pandas.DataFrame, titles: itertools.cycle = Iter.cycle([''])) -> None

   Display dataframes next to each other in a jupyter notebook.
   @param *args
       Multiple pandas dataframes
   @param title
       Title(s) for dataframes


.. py:function:: see_distn(data: pandas.DataFrame, title: str = '') -> None

   Create boxplots that show the distribution of numeric variables in a dataframe.
   @param data
       Pandas dataframe with specific column names (ideally, the result of pd.DataFrame.melt())
   @param title
       Title for distribution figure


.. py:function:: rmoutliers(x: pandas.Series, method: str = 'remove') -> pandas.Series

   Remove statistical outliers from pandas series
   @param x
       Pandas series


.. py:function:: elbow_plot(data: pandas.DataFrame, max_k: int = 10, title: str = '') -> None

   Generate an elbow plot to determine optimal K for K-means clusters.
   @param data
       Pandas DataFrame
   @param max_k
       Maximum number of clusters to test
   @param title
       Title of Elbow plot


.. py:function:: calculate_pvalues(df: pandas.DataFrame) -> pandas.DataFrame

   Generate p-values matrix from data frame
   @param df
       Pandas Data Frame


.. py:function:: kmeans(data: pandas.DataFrame, k: int = 2, facet_by: str = None) -> tuple

   Wrapper for sklearn.cluster.KMeans()
   @param data
       Pandas dataframe (Result of pd.DataFrame.melt())
   @param k
       Number of clusters
   @param facet
       Column to split data on when clustering. Must be within Data Frame Index
   @return
       Tuple containing cluster info and labelled data


.. py:function:: write_dfs(writer: pandas.ExcelWriter, sheet_name: str, **dfs) -> None

   Write multiple data frames to an excel file.
   @param writer
       An pd.ExcelWriter object
   @param sheet_name
       Name of sheet to write data to
   @param **dfs
       Names and pandas dataframes


.. py:function:: clusterplot(data: pandas.DataFrame, id_vars: list = ['Cluster'], hue: str = None, hue_order: list = None, kind: str = 'bar', title: str = '', xlabs: list = None, filename: str = None, scale='log', col_title='Cluster ', **plt_kwargs) -> None

   Generate Visualizations for KMeans Clustering Results
   @param data
       Pandas Data Frame
   @param id_vars
       List of id_vars for the pd.DataFrame.melt() method
   @param hue
       data column to use for figure colors
   @param hue_order
       List defining color order
   @param kind
       Type of plot to generate (either 'bar' or 'box')
   @param title
       Figure title
   @param xlabs
       List of labels for the horizontal axis


