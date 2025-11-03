#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def corner_plot_grid(csv_file, params, color_param="S", output_file=None,
                     cmap="viridis", log_scale=False):
    """
    Corner plot using 2D heatmaps for off-diagonal plots (regular grids).

    Diagonal plots are 1D histograms. Off-diagonal plots are 2D heatmaps
    of the specified color_param (e.g., S) computed on the regular parameter grid.

    Parameters:
        csv_file (str): CSV file with model fit results
        params (list of str): parameters to plot
        color_param (str): column to color by (S)
        output_file (str): filename to save figure
        cmap (str): colormap
        log_scale (bool): use log scale for color intensity
    """
    df = pd.read_csv(csv_file)

    # Check that all columns exist
    for p in params + [color_param]:
        if p not in df.columns:
            raise ValueError(f"Column '{p}' not found in CSV")

    n = len(params)
    fig, axes = plt.subplots(n, n, figsize=(3*n, 3*n), constrained_layout=True)

    for i, x_param in enumerate(params):
        for j, y_param in enumerate(params):
            ax = axes[i, j]

            if i == j:
                # Diagonal: 1D histogram
                ax.hist(df[x_param].values, bins=50, color='skyblue', edgecolor='k')
            else:
                # Off-diagonal: 2D heatmap on regular grid
                x_vals = np.sort(df[y_param].unique())
                y_vals = np.sort(df[x_param].unique())

                # Create 2D array of min S in each (x, y) grid cell
                Z = np.full((len(y_vals), len(x_vals)), np.nan)
                for xi, xv in enumerate(x_vals):
                    for yi, yv in enumerate(y_vals):
                        mask = (df[y_param] == xv) & (df[x_param] == yv)
                        if np.any(mask):
                            Z[yi, xi] = df.loc[mask, color_param].min()

                # Plot with pcolormesh
                im = ax.pcolormesh(x_vals, y_vals, Z, cmap=cmap, shading='auto')
                if log_scale:
                    im.set_norm(plt.matplotlib.colors.LogNorm())

            # Axis labels only on outer edges
            if j == 0:
                ax.set_ylabel(x_param, fontsize=10)
            else:
                ax.set_yticks([])

            if i == n-1:
                ax.set_xlabel(y_param, fontsize=10)
            else:
                ax.set_xticks([])

    # Add colorbar for heatmaps
    if n > 1:
        cbar = fig.colorbar(im, ax=axes, fraction=0.02, pad=0.02)
        cbar.set_label(color_param, fontsize=12)

    if output_file:
        plt.savefig(output_file, dpi=300)
        print(f"✅ Saved corner plot with 2D heatmaps to {output_file}")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Corner plot with 2D heatmaps")
    parser.add_argument("--csv", required=True, help="CSV file with fit results")
    parser.add_argument("--params", required=True, nargs="+", help="Parameters to plot")
    parser.add_argument("--color", default="S", help="Column to color by")
    parser.add_argument("--out", help="Output image file")
    parser.add_argument("--cmap", default="viridis", help="Colormap")
    parser.add_argument("--log", action="store_true", help="Use log scale for color")
    args = parser.parse_args()

    corner_plot_grid(args.csv, args.params, args.color, args.out, args.cmap, args.log)

