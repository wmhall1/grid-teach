#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import matplotlib.colors as mcolors

def corner_plot_2dhist(csv_file, params, color_param="S", output_file=None,
                       cmap="viridis", bins=50, log_scale=False):
    """
    Corner plot with 2D histograms for off-diagonal plots, showing minimum S per bin.
    
    Parameters:
        csv_file (str): CSV file with fit results
        params (list of str): parameters to plot
        color_param (str): column to color by (S value)
        output_file (str): filename to save figure
        cmap (str): colormap
        bins (int): number of bins for 2D histograms
        log_scale (bool): use log scale for color intensity
    """
    df = pd.read_csv(csv_file)

    # Check that all requested columns exist
    for p in params + [color_param]:
        if p not in df.columns:
            raise ValueError(f"Column '{p}' not found in CSV")

    n = len(params)
    fig, axes = plt.subplots(n, n, figsize=(3*n, 3*n), constrained_layout=True)

    # Loop over all subplot axes
    for i, x_param in enumerate(params):
        for j, y_param in enumerate(params):
            ax = axes[i, j]

            if i == j:
                # Diagonal: 1D histogram
                ax.hist(df[x_param].values, bins=bins, color='skyblue', edgecolor='k')
            else:
                # Off-diagonal: 2D histogram colored by min S per bin
                x = df[y_param].values
                y = df[x_param].values
                C = df[color_param].values

                # Bin edges
                x_edges = np.linspace(np.min(x), np.max(x), bins+1)
                y_edges = np.linspace(np.min(y), np.max(y), bins+1)

                # Create empty 2D array for min S
                H = np.full((bins, bins), np.nan)

                # Digitize data into bins
                x_idx = np.digitize(x, x_edges) - 1
                y_idx = np.digitize(y, y_edges) - 1
                x_idx = np.clip(x_idx, 0, bins-1)
                y_idx = np.clip(y_idx, 0, bins-1)

                # Aggregate min S per bin
                for xi, yi, ci in zip(x_idx, y_idx, C):
                    if np.isnan(H[yi, xi]):
                        H[yi, xi] = ci
                    else:
                        H[yi, xi] = min(H[yi, xi], ci)

                # Plot using pcolormesh to match bin edges
                X, Y = np.meshgrid(x_edges, y_edges)
                if log_scale:
                    norm = mcolors.LogNorm(vmin=np.nanmin(H[~np.isnan(H)]),
                                           vmax=np.nanmax(H[~np.isnan(H)]))
                else:
                    norm = None

                im = ax.pcolormesh(X, Y, H.T, cmap=cmap, shading='auto', norm=norm)

            # Axis labels only on outer edges
            if j == 0:
                ax.set_ylabel(x_param, fontsize=10)
            else:
                ax.set_yticks([])
            if i == n-1:
                ax.set_xlabel(y_param, fontsize=10)
            else:
                ax.set_xticks([])

    # Add colorbar for off-diagonal heatmaps
    cbar = fig.colorbar(im, ax=axes, fraction=0.02, pad=0.02)
    cbar.set_label(color_param, fontsize=12)

    if output_file:
        plt.savefig(output_file, dpi=300)
        print(f"✅ Saved corner plot with 2D histograms to {output_file}")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Corner plot with 2D histograms for large datasets")
    parser.add_argument("--csv", required=True, help="CSV file with fit results")
    parser.add_argument("--params", required=True, nargs="+", help="Parameters to plot")
    parser.add_argument("--color", default="S", help="Column to color by (min S per bin)")
    parser.add_argument("--out", help="Output image file")
    parser.add_argument("--cmap", default="viridis", help="Colormap")
    parser.add_argument("--bins", type=int, default=50, help="Number of bins for 2D histograms")
    parser.add_argument("--log", action="store_true", help="Use log scale for color intensity")
    args = parser.parse_args()

    corner_plot_2dhist(args.csv, args.params, args.color, args.out, args.cmap, args.bins, args.log)

