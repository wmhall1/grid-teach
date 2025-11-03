#!/usr/bin/env python3
import re
import argparse
import numpy as np
import pandas as pd
from math import sqrt
from csv import DictWriter

try:
    from scipy.optimize import linear_sum_assignment
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


# ---- Parameter names ----
PARAM_NAMES = [
    "temp", "mass", "menv", "mhe", "mh", "Xhebar",
    "alph1", "alph2", "alpha", "h1", "h2", "h3",
    "w1", "w2", "w3", "w4"  # ← DELETE w4 if using Agnes grid
]


# ---- Streaming model parser ----
def stream_models(filename):
    """
    Generator yielding one model at a time from the file.
    Reads line-by-line to avoid loading the whole file.
    """
    num = len(PARAM_NAMES)
    pattern = rf"^(\s*-?\d+(\.\d+)?\s+){{{num-1}}}-?\d+(\.\d+)?$"

    with open(filename, "r") as f:
        params = None
        modes_by_l = {}

        for line in f:
            line = line.strip()
            # Detect header (num parameters)
            if re.match(pattern, line):
                if params is not None:
                    # yield previous model before starting new one
                    yield {"params": params, "modes": modes_by_l}
                values = list(map(float, line.split()))
                params = dict(zip(PARAM_NAMES, values))
                modes_by_l = {}
            elif line and not line.startswith(("0.0", "100000")):
                parts = line.split()
                if len(parts) == 2:
                    l_val, period = int(parts[0]), float(parts[1])
                    modes_by_l.setdefault(l_val, []).append(period)

        # yield last model
        if params is not None:
            yield {"params": params, "modes": modes_by_l}


# ---- Observed file parser ----
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


# ---- Core fitting ----
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
        cost = (p - model_modes) ** 2 * w[i]
        idx = np.argmin(cost)
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


def is_one_to_one(fit, l_vals):
    """
    Check that each observed period maps uniquely to a model mode per ℓ.
    Returns True if one-to-one, False if any duplicates exist.
    """
    l_to_indices = {}
    for l, idx in zip(l_vals, fit["matched_model_mode_index"]):
        l_to_indices.setdefault(l, []).append(idx)

    # Each l group must have unique indices
    for l, indices in l_to_indices.items():
        if len(set(indices)) != len(indices):
            return False
    return True


def run_fitting(model_file, observed_file, l_values, output_csv="fits_output.csv"):
    """Stream models, fit each, and write results incrementally to CSV."""
    p_obs, sigma_obs = parse_observed_file(observed_file)
    l_values = np.array(l_values, dtype=int)

    fieldnames = PARAM_NAMES + ["model_index", "S", "Nm"]
    for j in range(len(p_obs)):
        fieldnames += [
            f"matched_p_obs{j}",
            f"matched_p_model{j}",
            f"matched_l{j}",
            f"matched_model_mode_index{j}",
        ]

    with open(output_csv, "w", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for model_index, model in enumerate(stream_models(model_file)):
            if model_index % 1000 == 0:
                print(f"Processing model {model_index}...")

            fit = compute_best_fit(model, p_obs, sigma_obs, l_values)
            if fit is None:
                continue

            # 🔍 Require one-to-one match
            if not is_one_to_one(fit, l_values):
                continue  # skip this model entirely

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

            writer.writerow(row)

    print(f"✅ Finished streaming fit. Results written to {output_csv}")


# ---- CLI ----
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fit observed oscillation periods to stellar models (streaming version)."
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

