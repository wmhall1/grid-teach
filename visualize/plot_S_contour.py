#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import argparse
import matplotlib.colors as colors


def plot_S_contour(csv_file, output_file=None, levels=20, log=False):
    """Make a contour plot of S values in temperature/mass space, or a line plot if 1D."""
    df = pd.read_csv(csv_file)

    # --- Check required columns ---
    for col in ["temp", "mass", "S"]:
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}' in {csv_file}")

    temp = df["temp"].values
    mass = df["mass"].values
    S = df["S"].values

    unique_temp = np.unique(temp)
    unique_mass = np.unique(mass)

    # --- Case 1: only one-dimensional grid ---
    if len(unique_mass) < 3 or len(unique_temp) < 3:
        print("⚠️ Detected a 1D grid (mass or temperature constant). Using line plot instead.")
        plt.figure(figsize=(7, 5))
        if len(unique_mass) < len(unique_temp):
            # fixed mass, varying temperature
            plt.plot(temp, S, "o-", label="Models")
            plt.xlabel("Effective Temperature (K)")
            plt.title(f"S vs Temperature (mass ≈ {np.mean(mass):.3f})")
        else:
            # fixed temperature, varying mass
            plt.plot(mass, S, "o-", label="Models")
            plt.xlabel("Mass (M$_\\odot$)")
            plt.title(f"S vs Mass (temp ≈ {np.mean(temp):.0f} K)")

        plt.ylabel("S value")
        plt.grid(True, ls="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        if output_file:
            plt.savefig(output_file, dpi=300)
            print(f"✅ Saved 1D plot to {output_file}")
        else:
            plt.show()
        return

    # --- Case 2: 2D grid, make contour plot ---
    ti = np.linspace(temp.min(), temp.max(), 200)
    mi = np.linspace(mass.min(), mass.max(), 200)
    Ti, Mi = np.meshgrid(ti, mi)

    # Try cubic interpolation, fall back if needed
    try:
        Si = griddata((temp, mass), S, (Ti, Mi), method="cubic")
    except Exception as e:
        print("⚠️ Cubic interpolation failed, falling back to 'linear'.")
        print(f"   Reason: {e}")
        Si = griddata((temp, mass), S, (Ti, Mi), method="linear")

    if Si is None or np.all(np.isnan(Si)):
        print("⚠️ Linear interpolation failed too, using 'nearest'.")
        Si = griddata((temp, mass), S, (Ti, Mi), method="nearest")
    #Clip negatives which shouldn't exist
    Si = np.clip(Si, a_min=0, a_max=None)

    # --- Plot contour ---
    plt.figure(figsize=(8, 6))
    
# choose normalization: log scale if range is large
    if log:
        norm = colors.LogNorm(vmin=max(S.min(), 1e-6), vmax=S.max())
        contour = plt.contourf(Ti, Mi, Si, levels=levels, cmap="viridis_r", norm=norm)
        cbar_label = "log(S value)"
    else:
        contour = plt.contourf(Ti, Mi, Si, levels=levels, cmap="viridis_r")
        cbar_label = "S value"
    cbar = plt.colorbar(contour)
    cbar.set_label(cbar_label, fontsize=12)

    # overlay model points
    #plt.scatter(temp, mass, c="k", s=15, alpha=0.8, label="Models")

    # highlight best-fit model (lowest S)
    best_idx = np.nanargmin(S)
    plt.scatter(temp[best_idx], mass[best_idx], s=100, c="red", edgecolor="white",
                marker="*", label=f"Best Fit {np.min(S)}")

    plt.xlabel("Effective Temperature (K)", fontsize=12)
    plt.ylabel("Mass ($M_\\odot$)", fontsize=12)
    plt.title("Best-fit S values in Temperature–Mass Space", fontsize=14)
    plt.legend()
    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=300)
        print(f"✅ Saved contour plot to {output_file}")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot S contour from fit results.")
    parser.add_argument("--csv", required=True, help="CSV file with fit results")
    parser.add_argument("--out", help="Optional output image filename")
    parser.add_argument("--levels", type=int, default=20, help="Number of contour levels (default 20)")
    parser.add_argument("--log", action="store_true", help="Log scale S colorbar")
    args = parser.parse_args()

    plot_S_contour(args.csv, args.out, args.levels, args.log)

