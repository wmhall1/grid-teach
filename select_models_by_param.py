#!/usr/bin/env python3
import pandas as pd
import argparse
import sys

def parse_param_filters(param_list):
    """
    Parse a list of key=value pairs into a dictionary.
    Example: ["temp=11000", "mass=800.0"]
    → {"temp": 11000.0, "mass": 8.0}
    """
    filters = {}
    for item in param_list:
        if "=" not in item:
            print(f"❌ Invalid parameter format: '{item}' (use name=value)")
            sys.exit(1)
        key, value = item.split("=", 1)
        try:
            value = float(value)
        except ValueError:
            pass  # keep as string if not numeric
        filters[key] = value
    return filters


def select_models(csv_file, output_file, param_filters):
    df = pd.read_csv(csv_file)
    print(f"📄 Loaded {len(df)} models from {csv_file}")

    # Apply filters
    for param, value in param_filters.items():
        if param not in df.columns:
            print(f"⚠️  Column '{param}' not found in CSV — skipping filter.")
            continue
        before = len(df)
        df = df[df[param] == value]
        print(f"🔹 Filtered {param} = {value} → {len(df)} models (from {before})")

    # Save output
    df.to_csv(output_file, index=False)
    print(f"\n✅ Saved {len(df)} matching models to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Select all models from a grid CSV with given parameter values."
    )
    parser.add_argument("--csv", required=True, help="Input model CSV file")
    parser.add_argument("--out", required=True, help="Output CSV file")
    parser.add_argument(
        "--param",
        nargs="+",
        required=True,
        help="Parameter filters as key=value pairs (e.g. temp=11000 mass=800)"
    )
    args = parser.parse_args()

    filters = parse_param_filters(args.param)
    select_models(args.csv, args.out, filters)

