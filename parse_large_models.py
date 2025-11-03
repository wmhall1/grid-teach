import re
import argparse
import numpy as np
from math import sqrt

PARAM_NAMES = [
    "temp", "mass", "menv", "mhe", "mh", "Xhebar",
    "alph1", "alph2", "alpha", "h1", "h2", "h3",
    "w1", "w2", "w3"
]

def stream_models(filename):
    num = len(PARAM_NAMES)
    pattern = rf"^(\s*-?\d+(\.\d+)?\s+){{{num-1}}}-?\d+(\.\d+)?$"
    """Generator that yields one model at a time from the file."""
    with open(filename, "r") as f:
        params = None
        modes_by_l = {}
        for line in f:
            line = line.strip()
            # Detect header (16 floats)
            if re.match(pattern, line):
                # yield the previous model if one exists
                if params is not None:
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


def summarize_models_stream(filename):
    """Compute parameter min/max/spacing while streaming through models."""
    param_values = {p: [] for p in PARAM_NAMES}
    n_models = 0

    for model in stream_models(filename):
        for p, v in model["params"].items():
            param_values[p].append(v)
        n_models += 1
        if n_models % 10000 == 0:
            print(f"Processed {n_models} models...")

    print(f"\nTotal models: {n_models}\n{'='*60}")
    for p, vals in param_values.items():
        if not vals:
            continue
        vals = sorted(vals)
        diffs = [vals[i+1] - vals[i] for i in range(len(vals)-1) if vals[i+1] - vals[i] > 1e-6]
        spacing = np.unique(np.round(diffs, 8))
        print(f"Parameter: {p}")
        print(f"  Min: {vals[0]}")
        print(f"  Max: {vals[-1]}")
        print(f"  Unique steps: {spacing}")
        print("-" * 40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stream and summarize massive model files.")
    parser.add_argument("--models", required=True, help="Path to the model file")
    args = parser.parse_args()

    summarize_models_stream(args.models)

