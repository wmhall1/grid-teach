#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import matplotlib.colors as mcolors

def corner_plot(csv_file, params, color_param="S", output_file=None, cmap="viridis"):
    """
    Make a corner plot (histograms on the diagonal, scatter off-diagonal) 
    for the given list of parameters from a CSV file, with points colored 
    by `color_param` (e.g., S value).

    Parameters:
        csv_file (str): path to CSV with fit results
        params (list of str): columns to include in the corner plot
        color_param (str): column to use for coloring scatter points
        output_file (str): optional filename to save the figure
        cmap (str): matplotlib colormap for coloring
    """
    df = pd.read_csv(csv_file)

    # --- Check that all requested parameters exist ---
    for p in params + [color_param]:
        if p not in df.columns:
            raise ValueError(f"Parameter '{p}' not found in {csv_file}")

    color_values = df[color_param].values
    norm = mcolors.Normalize(vmin=np.nanmin(color_values), vmax=np.nanmax(color_values))

    n = len(params)
    fig, axes = plt.subplots(n, n, figsize=(3*n, 3*n))
    plt.subplots_adjust(wspace=0.05, hspace=0.05)

    for i, x_param in enumerate(params):
        for j, y_param in enumerate(params):
            ax = axes[i, j]
            
            if i == j:
                # Diagonal: histogram
                ax.hist(df[x_param].values, bins=25, color='skyblue', edgecolor='k')
            else:
                # Off-diagonal: scatter plot with color
                sc = ax.scatter(df[y_param].values, df[x_param].values,
                                c=color_values, cmap=cmap, s=15, alpha=0.7, edgecolors='k')
            
            # Only show outer labels
            if j > 0:
                ax.set_yticks([])
            else:
                ax.set_ylabel(x_param, fontsize=10)
            
            if i < n-1:
                ax.set_xticks([])
            else:
                ax.set_xlabel(y_param, fontsize=10)

    # Add colorbar if using scatter plots
    if n > 1:
        cbar = fig.colorbar(sc, ax=axes, fraction=0.02, pad=0.02)
        cbar.set_label(color_param, fontsize=12)

    plt.tight_layout()
    if output_file:
        plt.savefig(output_file, dpi=300)
        print(f"✅ Saved corner plot to {output_file}")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create corner plots for selected parameters with color coding by S.")
    parser.add_argument("--csv", required=True, help="CSV file with model fit results")
    parser.add_argument("--params", required=True, nargs="+",
                        help="List of parameters/columns to plot in the corner plot")
    parser.add_argument("--color", default="S",
                        help="Column name to color points by (default 'S')")
    parser.add_argument("--out", help="Optional output image filename")
    parser.add_argument("--cmap", default="viridis", help="Matplotlib colormap for points (default 'viridis')")
    args = parser.parse_args()

    corner_plot(args.csv, args.params, args.color, args.out, args.cmap)

