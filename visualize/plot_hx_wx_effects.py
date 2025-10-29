#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse

def plot_hx_wx_effects(csv_file, output_prefix=None):
    df = pd.read_csv(csv_file)

    # Parameters of interest
    hx = ["h1","h2","h3"]
    wx = ["w1","w2","w3","w4"]
    params = hx + wx
    
    '''
    # --- 1. Scatter plots of each parameter vs S ---
    plt.figure(figsize=(16, 8))
    for i, p in enumerate(params):
        plt.subplot(2, 4, i+1)
        plt.scatter(df[p], df["S"], c=df["S"], cmap="viridis_r", s=40, alpha=0.7)
        plt.xlabel(p)
        plt.ylabel("S")
        plt.title(f"S vs {p}")
        plt.colorbar(label="S", shrink=0.7)
    plt.tight_layout()
    if output_prefix:
        plt.savefig(f"{output_prefix}_scatter.png", dpi=300)
        print(f"✅ Saved scatter plots to {output_prefix}_scatter.png")
    else:
        plt.show()
    '''
    '''
    # --- 2. Pairwise heatmaps for all parameter pairs ---
    for i, p1 in enumerate(params):
        for j, p2 in enumerate(params):
            if j <= i:
                continue
            pivot = df.pivot_table(index=p1, columns=p2, values="S", aggfunc="min")
            if pivot.empty:
                continue
            plt.figure(figsize=(6,5))
            sns.heatmap(pivot, cmap="viridis_r", annot=False)
            plt.title(f"Min S: {p1} vs {p2}")
            plt.xlabel(p2)
            plt.ylabel(p1)
            plt.tight_layout()
            if output_prefix:
                plt.savefig(f"{output_prefix}_heatmap_{p1}_{p2}.png", dpi=300)
                plt.close()
            else:
                plt.show()
    '''
    '''
    # --- 3. Correlation matrix ---
    corr = df[params + ["S"]].corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation matrix of hx/wx parameters with S")
    plt.tight_layout()
    if output_prefix:
        plt.savefig(f"{output_prefix}_corr.png", dpi=300)
        print(f"✅ Saved correlation matrix to {output_prefix}_corr.png")
    else:
        plt.show()
   '''
# --- 2. Fast binned pairwise heatmaps ---
    n_bins = 20  # Number of bins for each parameter

    for i, p1 in enumerate(params):
        for j, p2 in enumerate(params):
            if j <= i:
                continue

            # Bin the continuous parameters
            p1_bins = pd.cut(df[p1], bins=n_bins)
            p2_bins = pd.cut(df[p2], bins=n_bins)

            # Create pivot table on binned data
            pivot = df.pivot_table(index=p1_bins, columns=p2_bins, values="S", aggfunc="min")
            if pivot.empty:
                continue

            plt.figure(figsize=(6,5))
            sns.heatmap(pivot, cmap="viridis_r", annot=False)
            plt.title(f"Min S: {p1} vs {p2}")
            plt.xlabel(p2)
            plt.ylabel(p1)
            plt.tight_layout()
            if output_prefix:
                plt.savefig(f"{output_prefix}_heatmap_{p1}_{p2}.png", dpi=300)
                plt.close()
            else:
                plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize effect of h/w parameters on fit strength S")
    parser.add_argument("--csv", required=True, help="CSV file with fit results")
    parser.add_argument("--out", help="Prefix for output figures")
    args = parser.parse_args()

    plot_hx_wx_effects(args.csv, args.out)

