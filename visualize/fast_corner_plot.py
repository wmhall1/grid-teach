#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import matplotlib.colors as mcolors

def corner_plot(csv_file, params, color_param="S", output_file=None,
                cmap="viridis", max_points=5000, use_hexbin=False):
    """
    Fast corner plot with optional color coding and hexbin for large datasets.

    Parameters:
        csv_file (str): path to CSV with model fit results
        params (list of str): columns to include in the corner plot
        color_param (str): column to use for coloring scatter points
        output_file (str): optional filename to save figure
        cmap (str): matplotlib colormap for points
        max_points (int): maximum number of points to plot (downsample if necessary)
        use_hexbin (bool): use hexbin for off-diagonal plots instead of scatter
    """
    df = pd.read_csv(csv_file)

    # --- Check requested columns ---
    for p in params + [color_param]:
        if p not in df.columns:
            raise ValueError(f"Parameter '{p}' not found in {csv_file}")

    # --- Downsample for speed if dataset is huge ---
    if len(df) > max_points:
        df = df.sample(max_points, random_state=42)
        print(f"⚡ Downsampled to {max_points} points for faster plotting.")

    color_values = df[color_param].values
    norm = mcolors.Normalize(vmin=np.nanmin(color_values), vmax=np.nanmax(color_values))

    n = len(params)
    fig, axes = plt.subplots(n, n, figsize=(3*n, 3*n), constrained_layout=True)

    for i, x_param in enumerate(params):
        for j, y_param in enumerate(params):
            ax = axes[i, j]

            if i == j:
                # Diagonal: histogram
                ax.hist(df[x_param].values, bins=25, color='skyblue', edgecolor='k')
            else:
                # Off-diagonal: scatter or hexbin
                if use_hexbin:
                    hb = ax.hexbin(df[y_param].values, df[x_param].values, C=color_values,
                                   gridsize=50, cmap=cmap, reduce_C_function=np.min, mincnt=1)
                else:
                    sc = ax.scatter(df[y_param].values, df[x_param].values,
                                    c=color_values, cmap=cmap, s=10, alpha=0.7,
                                    edgecolors='none')

            # Only show outer labels
            if j > 0:
                ax.set_yticks([])
            else:
                ax.set_ylabel(x_param, fontsize=10)

            if i < n-1:
                ax.set_xticks([])
            else:
                ax.set_xlabel(y_param, fontsize=10)

    # Add colorbar
    if n > 1:
        if use_hexbin:
            cbar = fig.colorbar(hb, ax=axes, fraction=0.02, pad=0.02)
        else:
            cbar = fig.colorbar(sc, ax=axes, fraction=0.02, pad=0.02)
        cbar.set_label(color_param, fontsize=12)

    if output_file:
        plt.savefig(output_file, dpi=300)
        print(f"✅ Saved corner plot to {output_file}")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fast corner plot for model fit results.")
    parser.add_argument("--csv", required=True, help="CSV file with fit results")
    parser.add_argument("--params", required=True, nargs="+",
                        help="List of parameters/columns to plot in the corner plot")
    parser.add_argument("--color", default="S", help="Column name to color points by")
    parser.add_argument("--out", help="Optional output image filename")
    parser.add_argument("--cmap", default="viridis", help="Matplotlib colormap")
    parser.add_argument("--max_points", type=int, default=5000,
                        help="Max points to plot (downsample if larger)")
    parser.add_argument("--hexbin", action="store_true",
                        help="Use hexbin for off-diagonal plots (faster for dense datasets)")
    args = parser.parse_args()

    corner_plot(args.csv, args.params, args.color, args.out, args.cmap, args.max_points, args.hexbin)

