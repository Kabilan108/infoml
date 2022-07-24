"""cli.py
Command line interface for neuro sub-package.
This progam allows for the generation of figures, running of quality control
scripts, and computation of graph theory metrics.
"""

# Imports
from typer import Typer, Argument, Option
from rich import print
from enum import Enum
import pandas as pd
import numpy as np
import os
import re

import wrangling, stats, plot, metrics


class cli:
    # Initialize typer
    app = Typer()

    # Define options for CLI commands
    class arg_sign(str, Enum):
        full, positive, negative = 'full', 'positive', 'negative'
    class arg_ext(str, Enum):
        png, svg, jpg, pdf = '.png', '.svg', '.jpg', '.pdf'
    class arg_modality(str, Enum):
        structural, functional = 'structural', 'functional'

    # plot-connectome command
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
        indir: str = Option(..., help='Path to the folder containing the connectomes'),
        outdir: str = Option(..., help="File to write the statistics to"),
        subjects: str = Option("", help='File with subject IDs'),
        file_stub: str = Option(".txt", help='trailing text that follows subject IDs in the file name.'),
        name_pattern: str = Option("R\d*_V\d*", help="Regular expression for extracting subject names from file names."),
        nodes: int = Option(..., help="Number of ROIs in the atlas. Use this flag only if the region IDs are sequential."),
        hemisphere_map: str = Option("", help="File that contains the hemisphere information for the nodes"),        
        std: int = Option(2.33, help='Label subjects as problematic for being this many standard deviations away from the mean of healthy controls'),
        droplastnode: bool = Option(False, help='drop last node of the connectome (brain stem) from strength calculations across hemispheres'),
        modality: arg_modality = Option(arg_modality.structural, help="Structural or functional connectome?"),
        zero_diag: bool = Option(False, help='Set the diagonal to zero'),
        title: str = Option("Distribution of Metrics", help="Title for the figure")
    ):
        """
        Quality control for connectomes.
        """

        # Get list of connectome paths
        if subjects != "":
            subjects = [x + file_stub for x in open(subjects, 'r').read().splitlines()]
        else:
            subjects = sorted(os.listdir(indir))

        # Create output directory
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        # Obtain subject names from the file names
        subject_names = [re.search(name_pattern, x)[0] for x in subjects]
        
        # Load connectomes
        connectomes = wrangling.load_connectomes(
            indir, subject_names, id_pattern=name_pattern, zero_diag=zero_diag
        )

        # Exclude connectomes if they have a different number of nodes
        discard_idx = []
        discard_subjects = []
        discard_subject_node_count = []
        for i, cntm in enumerate(connectomes):
            if len(cntm) != nodes:
                discard_idx.append(i)
                discard_subjects.append(subject_names[i])
                discard_subject_node_count.append(len(cntm))
        connectomes = np.delete(connectomes, discard_idx, axis=0)

        # Subject numbers and orders
        num_subjects = len(connectomes)
        subject_order = np.arange(num_subjects)

        # Load hemisphere map
        if hemisphere_map != "":
            hemisphere_map = np.array(np.loadtxt(hemisphere_map), dtype=bool)
        else:
            hemisphere_map = np.ones(nodes, dtype=bool)
            hemisphere_map[0:int(nodes/2)] = False

        # Drop last node of the connectome
        if droplastnode:
            hemisphere_map[-1] = 0
            inverted_hemisphere_map = np.invert(hemisphere_map)
            inverted_hemisphere_map[-1] = 0
        else:
            inverted_hemisphere_map = np.invert(hemisphere_map)

        # Keep track of statistics in a dictionary
        statistics = dict()

        # Calculate statistics
        statistics['Total Connectivity'] = \
            metrics.compute_global_metric(connectomes, metrics.connectivity_strength)
        statistics['Intrahemispheric Connectivity'] = \
            metrics.compute_global_metric(connectomes, metrics.intrahemispheric_strength, hemisphere_map)
        statistics['Interhemispheric Connectivity'] = \
            metrics.compute_global_metric(connectomes, metrics.interhemispheric_strength, hemisphere_map)
        statistics['Density'] = \
            metrics.compute_global_metric(connectomes, metrics.density)

        ##* Stat:  Off-diagonal Connectivity & Self Edges (Diagonal Strength)
        if zero_diag == False:
            diag, off_diag = [], []
            for cntm in connectomes:
                diag.append( np.trace(cntm))
                conn = cntm.copy()
                np.fill_diagonal(conn, 0)
                off_diag.append( np.sum(conn * (conn > 0) / 2.0) )
            statistics['Total Off-Diagonal Connectivity'] = np.array(off_diag)
            statistics['Self Edges'] = np.array(diag)

        if modality == 'functional':
            neg_connectomes = -connectomes

            statistics['Total Connectivity'] = \
                metrics.compute_global_metric(neg_connectomes, metrics.connectivity_strength)
            statistics['Intrahemispheric Connectivity'] = \
                metrics.compute_global_metric(neg_connectomes, metrics.intrahemispheric_strength, hemisphere_map)
            statistics['Interhemispheric Connectivity'] = \
                metrics.compute_global_metric(neg_connectomes, metrics.interhemispheric_strength, hemisphere_map)
            statistics['Density'] = \
                metrics.compute_global_metric(neg_connectomes, metrics.density)

        # Calculate z-scores, if indicated by the user
        zscores = {k: stats.zscore(v, subject_order) for k,v in statistics.items()}

        ##* Fig: Boxplots with threshold for std above and below zero, and
        ##*      outlier names will be shown.
        # This line will plot the z-scores for each statistic
        # plot.boxplots(pd.DataFrame(zscores), name_outliers=True, subject_ids=subject_names)
        fig, ax = plot.boxplots(pd.DataFrame(statistics), 
                                figsize=(10,6), title=title,
                                jitter=True, name_outliers=True, 
                                subject_ids=subject_names)
        fig.savefig(outdir + '/metric_distributions.pdf', dpi=300)
        
        # Get a list of subjects with very large/small ROIs relative to
        # healthy control population
        outliers_small_name = []
        outliers_small_std = []
        outliers_small_score = []
        for stat in statistics:
            outliers_small_name.append([name for name, truth in zip(subject_names, zscores[stat] <= -std) if truth])
            outliers_small_score.append([score for score, truth in zip(statistics[stat], zscores[stat] <= -std) if truth])
            outliers_small_std.append([score for score in zscores[stat] if score <= -std])

        outliers_large_name = []
        outliers_large_std = []
        outliers_large_score = []
        for stat in statistics:
            outliers_large_name.append([name for name, truth in zip(subject_names, zscores[stat] >= std) if truth])
            outliers_large_score.append([score for score, truth in zip(statistics[stat], zscores[stat] >= std) if truth])
            outliers_large_std.append([score for score in zscores[stat] if score >= std])
        
        # Save list of subjects with outlier ROIs
        with open(outdir + 'Outlier-Report.txt', 'w') as f:

            # Report on outliers
            f.write('============= Discarded Subjects Due to Missing Node =============\n')
            for subject, node_ct in zip(discard_subjects, discard_subject_node_count):
                f.write('%s: %d nodes\n' % (subject, node_ct))
            f.write('\n')

            f.write('========== Outlier Statistics > %.1f Standard Deviations ==========\n' % std)
            for i, stat in enumerate(statistics):
                f.write('%s ==> ' % stat)
                for j, outlier in enumerate(outliers_large_name[i]):
                    f.write('(%s: %.2f +/- %.2f)\t' % (outlier, outliers_large_score[i][j], outliers_large_std[i][j]))
                f.write('\n\n')

            f.write('========== Outlier Statistics < %.1f Standard Deviations ==========\n' % std)
            for i, stat in enumerate(statistics):
                f.write('%s ==> ' % stat)
                for j, outlier in enumerate(outliers_small_name[i]):
                    print(outlier)
                    f.write('(%s: %.2f +/- %.2f)\t' % (outlier, outliers_small_score[i][j], outliers_small_std[i][j]))
                f.write('\n\n')

            # Create table with subjects indicating whether they are outliers
            outlier = ['' for _ in subjects]
            large_flat = [x for sub in outliers_large_name for x in sub]
            small_flat = [x for sub in outliers_small_name for x in sub]
            for i, subject in enumerate(subject_names):
                if subject in discard_subjects:
                    outlier[i] += 'Missing Node'
                if subject in large_flat:
                    outlier[i] = f'> {std} STD'
                elif subject in small_flat:
                    outlier[i] = f'< {std} STD'
            outlier_table = pd.DataFrame({'Subject': subject_names, 
                                          'Outlier': outlier})

            # Write table to file
            f.write('=========== Table with Outlier Status for each Subject ===========\n')
            f.write(outlier_table.to_string())

        print("[red bold]QC Complete![/red bold]")


if __name__ == '__main__':
    print('Running QC...')
    neuro = cli()
    neuro.app()