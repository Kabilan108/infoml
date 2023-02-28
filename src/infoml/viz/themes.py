"""
infoml.themes
-----------

This module contains themes for plotly and matplotlib (seaborn included).
"""

from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class FigureTheme(ABC):
    """
    Abstract base clas for figure themes.
    """

    @abstractmethod
    def apply(self, fig):
        """
        Apply the theme to a figure.

        Parameters
        ----------
        fig : object
            A figure object for the corresponding plotting library.

        This method should be implemented by concrete theme classes to apply
        the specific aesthetic defined by the theme to a figure.
        """
        pass


# class MatplotlibTheme(FigureTheme):
#     """
#     A theme for matplotlib figures.
#     """

#     def __init__(self, style="graphpaper"):
#         """
#         Initialize a matplotlib theme.

#         Parameters
#         ----------
#         style : str, optional
#             The style to use for the theme. The default is "graphpaper".
#         """
#         self._style = style

#     def apply(self, fig):
#         """
#         Apply the theme to a figure.

#         Parameters
#         ----------
#         fig : object
#             A figure object for the corresponding plotting library.

#         Returns
#         -------
#         None.

#         """
#         # Check if style is built-in
#         if self._style in plt.style.available:
#             plt.style.use(self._style)
#         else:
#             raise ValueError(f"Style {self._style} is not available.")


class MplTheme(FigureTheme):
    """
    A theme for matplotlib figures.
    """

    def __init__(self, style="graphpaper"):
        self._style = style

    def apply(self, fig, axis, **kwargs):
        # Check if style is built-in
        if self._style in plt.style.available:
            plt.style.use(self._style)

        elif self._style == "graphpaper":
            # Read arguments
            gridcolor = kwargs.get("gridcolor", "black")
            majorgridwidth = kwargs.get("majorgridwidth", 0.5)
            minorgridwidth = kwargs.get("minorgridwidth", 0.5)
            majorgridalpha = kwargs.get("majorgridalpha", 0.5)
            minorgridalpha = kwargs.get("minorgridalpha", 0.2)

            # Set style
            axis.spines[["top", "right"]].set_visible(False)
            axis.spines[["left", "bottom"]].set_linewidth(1.2)
            axis.xaxis.set_ticks_position("bottom")
            axis.yaxis.set_ticks_position("left")
            axis.set_xlabel("Time (s)")
            axis.minorticks_on()
            axis.grid(
                which="major",
                linestyle="-",
                linewidth=majorgridwidth,
                color=gridcolor,
                alpha=majorgridalpha,
            )
            axis.grid(
                which="minor",
                linestyle=":",
                linewidth=minorgridwidth,
                color=gridcolor,
                alpha=minorgridalpha,
            )

    def __enter__(self, *args, **kwargs):
        self._fig, self._axis = plt.subplots(*args, **kwargs)
        self.apply(self._fig, self._axis)
        return self._axis

    def __exit__(self, *args, **kwargs):
        plt.show()


class PlotlyTheme(FigureTheme):
    """
    A theme for plotly figures.
    """

    def __init__(self, style="plotly"):
        """
        Initialize a plotly theme.

        Parameters
        ----------
        style : str, optional
            The style to use for the theme. The default is "plotly".
        """
        self._style = style

    def apply(self, fig):
        """
        Apply the theme to a figure.

        Parameters
        ----------
        fig : object
            A figure object for the corresponding plotting library.

        Returns
        -------
        None.

        """
        fig.update_layout(template=self._style)


if __name__ == "__main__":
    print("This module is not intended to be run directly.")
else:
    # Define module I/O
    __all__ = []
    __all__ += [m for m in dir() if m.startswith("__")]

    def __dir__():
        """Override dir() to only show public attributes."""
        return __all__

    def __getattr__(name):
        """Override getattr() to only show public attributes."""
        if name in __all__:
            return globals()[name]
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
