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

def summarize_models(models):
    if not models:
        print("No models provided.")
        return

    # Get all param names from the first model
    param_names = models[0]["params"].keys()

    for param in param_names:
        values = sorted([model["params"][param] for model in models])
        # Check spacing
        diffs = [values[i+1] - values[i] for i in range(len(values)-1) if values[i+1] - values[i] > 1e-6]
        spacing = np.unique(diffs)
        min_val = values[0]
        max_val = values[-1]
        print(f"Parameter: {param}")
        print(f"  Min: {min_val}")
        print(f"  Max: {max_val}")
        print(f"Spaced: {spacing}")
        print("-" * 40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fit observed oscillation periods to stellar models."
    )
    parser.add_argument("--models", required=True, help="Path to the model file")
    parser.add_argument(
        "--out",
        default="fits_output.csv",
        help="Output CSV file name (default: fits_output.csv)"
    )
    args = parser.parse_args()

    if not SCIPY_AVAILABLE:
        print("⚠️  SciPy not found — using simple matching. "
              "Install SciPy for faster fitting with many modes.")

    models = parse_model_file(args.models)
    summarize_models(models)
    
