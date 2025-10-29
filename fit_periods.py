#!/usr/bin/env python3
import re
import argparse
import numpy as np
import pandas as pd
from math import sqrt
try:
    from scipy.optimize import linear_sum_assignment
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


# ---- Parameter names ----
PARAM_NAMES = [
    "temp", "mass", "menv", "mhe", "mh", "Xhebar",
    "alph1", "alph2", "alpha", "h1", "h2", "h3",
    "w1", "w2", "w3", "w4"
]


# ---- File parsers ----
def parse_model_file(filename):
    """Parse a model file into a list of dicts with parameters and mode data."""
    models = []
    with open(filename, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Detect 16-parameter header line
        if re.match(r"^(\s*-?\d+(\.\d+)?\s+){15}-?\d+(\.\d+)?", line):
            params = list(map(float, line.split()))
            l_modes = []
            i += 1
            # Read subsequent lines of modes until blank or separator
            while i < len(lines):
                lline = lines[i].strip()
                if not lline or lline.startswith("0.0") or lline.startswith("100000"):
                    break
                parts = lline.split()
                if len(parts) == 2:
                    l_val = int(parts[0])
                    period = float(parts[1])
                    l_modes.append((l_val, period))
                i += 1
            # Store model
            modes_by_l = {}
            for l_val, p in l_modes:
                modes_by_l.setdefault(l_val, []).append(p)
            models.append({
                "params": dict(zip(PARAM_NAMES, params)),
                "modes": modes_by_l
            })
        i += 1
        if i % 1000 == 0:
            print(i)
    return models


def parse_observed_file(filename):
    """Parse observed periods and uncertainties."""
    periods, uncertainties = [], []
    with open(filename, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.split()
            periods.append(float(parts[0]))
            uncertainties.append(float(parts[1]) if len(parts) > 1 else 1.0)
    return np.array(periods), np.array(uncertainties)


# ---- Core fitting function ----
def compute_best_fit(model, p_obs, sigma_obs, l_vals):
    """Compute best-fit S for a single model."""
    w = 1 / np.where(sigma_obs == 0, 1, sigma_obs)
    Nm = sum(len(v) for v in model["modes"].values())

    matched_p_model = []
    matched_indices = []

    total_weighted_sq = 0.0
    total_weights = 0.0

    for i, (p, lw) in enumerate(zip(p_obs, l_vals)):
        if lw not in model["modes"]:
            return None  # cannot match this model to this obs
        model_modes = np.array(model["modes"][lw])

        # Cost array (difference squared × weight)
        cost = (p - model_modes) ** 2 * w[i]
        idx = np.argmin(cost)  # simplest one-to-one since ℓ handled separately
        matched_p_model.append(model_modes[idx])
        matched_indices.append(idx)
        total_weighted_sq += cost[idx]
        total_weights += w[i]

    S = sqrt(total_weighted_sq / total_weights) * Nm / 100.0
    return {
        "S": S,
        "Nm": Nm,
        "matched_p_model": matched_p_model,
        "matched_model_mode_index": matched_indices
    }


# ---- Runner ----
def run_fitting(model_file, observed_file, l_values, output_csv="fits_output.csv"):
    models = parse_model_file(model_file)
    p_obs, sigma_obs = parse_observed_file(observed_file)
    l_values = np.array(l_values, dtype=int)

    results = []
    for model_index, model in enumerate(models):
        if model_index % 1000 == 0:
            print(f"Model number {model_index}")
        fit = compute_best_fit(model, p_obs, sigma_obs, l_values)
        if fit is None:
            continue
        row = {**model["params"]}
        row.update({
            "model_index": model_index,
            "S": fit["S"],
            "Nm": fit["Nm"]
        })
        for j, (po, pm, li, idx) in enumerate(
            zip(p_obs, fit["matched_p_model"], l_values, fit["matched_model_mode_index"])
        ):
            row[f"matched_p_obs{j}"] = po
            row[f"matched_p_model{j}"] = pm
            row[f"matched_l{j}"] = li
            row[f"matched_model_mode_index{j}"] = idx
        results.append(row)

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved {len(df)} fits to {output_csv}")
    return df


# ---- CLI interface ----
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fit observed oscillation periods to stellar models."
    )
    parser.add_argument("--models", required=True, help="Path to the model file")
    parser.add_argument("--obs", required=True, help="Path to the observed periods file")
    parser.add_argument(
        "--lvals",
        required=True,
        nargs="+",
        type=int,
        help="List of ℓ values (same length/order as observed periods)"
    )
    parser.add_argument(
        "--out",
        default="fits_output.csv",
        help="Output CSV file name (default: fits_output.csv)"
    )
    args = parser.parse_args()

    if not SCIPY_AVAILABLE:
        print("⚠️  SciPy not found — using simple matching. "
              "Install SciPy for faster fitting with many modes.")

    run_fitting(args.models, args.obs, args.lvals, args.out)

