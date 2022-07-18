"""cli.py
Command line interface for neuro sub-package.
This progam allows for the generation of figures, running of quality control
scripts, and computation of graph theory metrics.
"""

# Imports
from typer import Typer, Argument, Option
from neuro import wrangling, plot
from enum import Enum
import numpy.linalg as LA
import nibabel as nib
import numpy as np
import os

from neuro import wrangling, stats, plot, metrics


class cli:
    # Initialize typer
    app = Typer()

    # Define options for CLI commands
    class arg_sign(str, Enum):
        full, positive, negative = 'full', 'positive', 'negative'
    class arg_ext(str, Enum):
        png, svg, jpg, pdf = '.png', '.svg', '.jpg', '.pdf'

    # plot_connectome command
    @app.command()
    def plot_connectome(
        path: str = Argument(..., help='Path to connectome matrix'),
        outpath: str = Argument('none', help='Path to save figure to'),
        threshold: float = Option(0.0, help='Threshold for the magnitude of the cell values'),
        bgcolor: str = Option('black', help='Color for cells below the threshold'),
        cmap: str = Option('jet', help='Matplotlib colormap to use'),
        ext: arg_ext = Option(arg_ext.png, case_sensitive=False, help='File extension for figure'),
        show: bool = Option(False),
        sign: arg_sign = Option(arg_sign.full, case_sensitive=False, help="Plot the 'full' matrix or just the 'positive' or 'negative' side"),
        logscale: bool = Option(False, help='log-scale connectivity'),
        zero_diag: bool = Option(True, help='Set the diagonal to zero'), 
        symmetric: bool = Option(False, help='If the data contains values above and below zero, set the middle point of the range to zero while displaying'),
        min: float = Option(None, help='min range of the plot'), 
        max: float = Option(None, help='max range of the plot')
    ):
    
        """
        Generate visualizations for a connectome.
        """

        # Load connectome
        cntm = wrangling._load_connectome(path, zero_diag=zero_diag)

        # Check inputs
        outpath = os.path.expanduser(outpath)
        if outpath == 'none':
            outpath = None
        elif outpath == '.':
            outpath = os.path.basename(path.rsplit('.', 1)[0]) + ext
        
        # Plot connectome
        plot.connectome(cntm, sign=sign, threshold=threshold, bgcolor=bgcolor, 
                        cmap=cmap, show=show, save=outpath, logscale=logscale, 
                        symmetric=symmetric, min=min, max=max);

        
    # QC command
    @app.command()
    def qc(

    ):
        """
        Quality control for connectomes.
        """
        pass


if __name__ == '__main__':
    neuro = cli()
    neuro.app()