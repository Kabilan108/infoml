:py:mod:`hcitools.plot`
=======================

.. py:module:: hcitools.plot

.. autoapi-nested-parse::

   This module contains functions for visualizing data and analysis results.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   hcitools.plot.colormap
   hcitools.plot.LabelEncoder



Functions
~~~~~~~~~

.. autoapisummary::

   hcitools.plot.set_renderer
   hcitools.plot._make_plate
   hcitools.plot.plate_heatmap
   hcitools.plot.pca_comps
   hcitools.plot.clusters
   hcitools.plot._make_grid
   hcitools.plot._v
   hcitools.plot._hls_to_rgb
   hcitools.plot._get_colors
   hcitools.plot.distplot
   hcitools.plot.textplot
   hcitools.plot.gifify
   hcitools.plot.heatmap



Attributes
~~~~~~~~~~

.. autoapisummary::

   hcitools.plot.LETTERS
   hcitools.plot.ONE_THIRD
   hcitools.plot.ONE_SIXTH
   hcitools.plot.TWO_THIRD


.. py:data:: LETTERS
   :annotation: = ABCDEFGHIJKLMNOPQRSTUVWXYZ

   

.. py:data:: ONE_THIRD
   

   

.. py:data:: ONE_SIXTH
   

   

.. py:data:: TWO_THIRD
   

   

.. py:function:: set_renderer(renderer)

   Set the plotly default renderer


.. py:class:: colormap

   Custom colormaps for plotly figures

   These colormaps assume the data has been scaled to between 0 and 1.

   .. attribute:: `OgBu`

      Seaborn diverging colorscale from blue (low) to orange (high)

      :type: list

   .. py:attribute:: OgBu
      :annotation: = [[0.0, '#3F7F93'], [0.1, '#6296A6'], [0.2, '#85ADB9'], [0.3, '#A9C4CC'], [0.4, '#CDDBE0'], [0.5,...

      


.. py:class:: LabelEncoder

   Encode target labels with values between 0 and n_classes-1

   .. attribute:: `encoder`

      dictionary mapping target labels to encodings

      :type: dict

   .. attribute:: `decoder`

      dictionary mapping encodings to target labels

      :type: dict

   .. attribute:: `dtype`

      dtype of original labels

      :type: np.dtype

   .. method:: `encode(labels)`

      Encode a list of target labels

   .. method:: `decode(enc_labels)`

      Decode a list of encoded labels


   .. py:method:: encode(labels)

      :param `labels`: list of target labels
      :type `labels`: array_like

      :returns: Encoded labels
      :rtype: np.array

      :raises AssertionError: If `enc_labels` is not 1-dimensional


   .. py:method:: decode(enc_labels)

      :param `enc_labels`: list of encoded lavels
      :type `enc_labels`: array_like

      :returns: Decoded labels
      :rtype: np.array

      :raises AssertionError: If `enc_labels` is not 1-dimensional



.. py:function:: _make_plate(data, feature, time_col='timepoint')

   Convert a feature data frame into a plate layout.

   This assumes `data` contains the following columns: `row`, `column` and
   `time_col`.

   :param `data`: a data frame of features including certain metadata columns
   :type `data`: pd.DataFrame
   :param `feature`: feature to populate plate with
   :type `feature`: str
   :param `time_col`: column that defines time points, by default 'timepoint'
   :type `time_col`: str, optional

   :returns: $(k     imes r  imes c)$ array where `k` = timepoint
   :rtype: np.array


.. py:function:: plate_heatmap(data, feature, time_col='timepoint', colorscale=colormap.OgBu)

   Create an interactive plate heatmap; Including an animation for timelapses

   This function assumes that `data` contains the following columns: `row`,
   `column`, `time_col`, `compound`, `conc`.

   :param `data`: a data frame of features including certain metadata columns
   :type `data`: pd.DataFrame
   :param `feature`: feature to populate plate with
   :type `feature`: str
   :param `time_col`: column that defines time points, by default 'timepoint'
                      This assumes the first time point is 1.
   :type `time_col`: str, optional
   :param `colorscale`: Plotly-compatible colormap, by default `colormap.OgBu`
                        See `colormap.OgBu` for examples.
   :type `colorscale`: list, optional

   :returns: Plotly figure
   :rtype: go.Figure


.. py:function:: pca_comps(proj, exp_var, time_col='timepoint', n_comps=4)

   Plot a scatter grid of PCA components

   This function is written to use the output from `process.dim_reduction`

   :param `proj`: Data frame with pca projections, from `process.dim_reduction`
   :type `proj`: _pd.DataFrame
   :param `exp_var`: List of explained variances for each PCA component
   :type `exp_var`: array_like
   :param `time_col`: Column containing time points; must be in index; by default 'timepoint'
   :type `time_col`: str, optional
   :param `n_comps`: Number of pca components to plot, by default 4
   :type `n_comps`: int, optional

   :returns: Plotly figure
   :rtype: go.Figure


.. py:function:: clusters(data, compound_a, compound_b, method, time_col='timepoint')

   Create clustering figures that compare 2 compounds.

   This function is written to use the output from `process.dim_reduction`

   :param `data`: _description_
   :type `data`: pd.DataFrame
   :param `compound_a`: Compound A (red points)
   :type `compound_a`: str
   :param `compound_b`: Compound B (green points)
   :type `compound_b`: str
   :param `method`: One of 'PCA', 'tSNE' or 'UMAP'
   :type `method`: str
   :param `time_col`: Column containing time points, by default 'timepoint'
   :type `time_col`: str, optional

   :returns: Plotly figure
   :rtype: go.Figure


.. py:function:: _make_grid(items, col_wrap=2)

   Split a list of items into a grid for subplots

   :param `items`: List of items for each subplot (e.g., tiles)
   :type `items`: list
   :param `col_wrap`: Number of columns allowed in layout, by default 2
   :type `col_wrap`: int, optional

   :returns: Plotly figure
   :rtype: go.Figure


.. py:function:: _v(m1, m2, hue)


.. py:function:: _hls_to_rgb(h, l, s)

   Convert HLS (Hue, Luminance, Saturation) to RGB


.. py:function:: _get_colors(n)

   Generate n visually distinct colors.

   This is taken from [this](https://stackoverflow.com/a/9701141) stack
   overflow post.


.. py:function:: distplot(data, features, group_col, tooltips=None, kind='box', col_wrap=2, title_len=30)

   Create boxplots showing the distibution of features for different groups.

   This generates a figure with as many subplots as there are features

   :param `data`: Data frame to plot
   :type `data`: pd.DataFrame
   :param `features`: List of features to visualize
   :type `features`: list
   :param `group_col`: `data` column that contains groups of interest
   :type `group_col`: str
   :param `tooltips`: Dictionary that defines annotation tooltips, by default None
                      Keys = Tooltip Name;
                      Values = Corresponding column in `data`
   :type `tooltips`: dict, optional
   :param `kind`: Type of plot to generate; one of 'box', 'bar', by default 'box'
   :type `kind`: str, optional
   :param `col_wrap`: Number of columns allowed in layout, by default 3
   :type `col_wrap`: int, optional
   :param `title_len`: Wrap length for subplot titles, by default 30
   :type `title_len`: int, optional

   :returns: Plotly figure
   :rtype: go.Figure

   :raises NotImplementedError: When `kind != 'box'`


.. py:function:: textplot(text)

   Create a blank figure to display some text. Serves as placeholder for
   actual figure.

   :param `text`: Message to display in figure
   :type `text`: str

   :returns: Plotly figure
   :rtype: go.Figure


.. py:function:: gifify(fig, file, frame_title='Frame', fps=30) -> None

   Export a plotly animation as a gif

   :param `fig`: Plotly figure
   :type `fig`: go.Figure
   :param `file`: Path to file where figure gif will be stored
   :type `file`: str
   :param `frame_title`: Title that describes each frame, by default 'Frame'
   :type `frame_title`: str, optional
   :param `fps`: Frame rate, by default 30
   :type `fps`: int, optional


.. py:function:: heatmap(data, col_groups=None, col_colors=None, col_group_names=None, row_groups=None, row_colors=None, row_group_names=None, clust_cols=True, clust_rows=True, cluster_kws=dict())

   Construct an interactive heatmap

   :param data: Data to plota
   :type data: pd.DataFrame
   :param {row: Dictionary assigning groups to rows or columns.
                Keys should be the index or columns of data.
                Values should be a list of groups.
   :type {row: dict
   :param col}_groups: Dictionary assigning groups to rows or columns.
                       Keys should be the index or columns of data.
                       Values should be a list of groups.
   :type col}_groups: dict
   :param {row: Names for each of the row/col groups
                Should be the same length as the lists in {row, col}_groups
   :type {row: list
   :param col}_group_names: Names for each of the row/col groups
                            Should be the same length as the lists in {row, col}_groups
   :type col}_group_names: list
   :param {row: Dictionary defining colors for each group.
                Keys = groups;  Values = colors;
   :type {row: dict
   :param col}_colors: Dictionary defining colors for each group.
                       Keys = groups;  Values = colors;
   :type col}_colors: dict
   :param clust_{rows: Should row and/or column clustering be performed
   :type clust_{rows: bool
   :param cols}: Should row and/or column clustering be performed
   :type cols}: bool
   :param cluster_kws: kwargs for sns.clustermap
   :type cluster_kws: dict


