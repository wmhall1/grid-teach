#!/usr/bin/env python3

import pandas as pd
import argparse
import sys
import re


def parse_param_filters(param_list):
    """
    Parse parameter filters.

    Examples:
        temp=11000
        mass>800
        S<=3

    Returns:
        [
            ("temp", "=", 11000.0),
            ("mass", ">", 800.0),
            ...
        ]
    """

    filters = []

    for item in param_list:

        # Match operators in order so >= and <= are caught before > and <
        match = re.match(r"^([^<>=]+)(<=|>=|=|<|>)(.+)$", item)

        if not match:
            print(
                f"❌ Invalid parameter format: '{item}' "
                "(use name=value, name<value, name>value, etc.)"
            )
            sys.exit(1)

        key, operator, value = match.groups()

        key = key.strip()
        value = value.strip()

        try:
            value = float(value)
        except ValueError:
            pass  # keep as string if not numeric

        filters.append((key, operator, value))

    return filters


def select_models(csv_file, output_file, param_filters):

    df = pd.read_csv(csv_file)

    print(f"📄 Loaded {len(df)} models from {csv_file}")

    # Apply filters
    for param, operator, value in param_filters:

        if param not in df.columns:
            print(f"⚠️ Column '{param}' not found in CSV — skipping filter.")
            continue

        before = len(df)

        if operator == "=":
            df = df[df[param] == value]

        elif operator == ">":
            df = df[df[param] > value]

        elif operator == "<":
            df = df[df[param] < value]

        elif operator == ">=":
            df = df[df[param] >= value]

        elif operator == "<=":
            df = df[df[param] <= value]

        print(
            f"🔹 Filtered {param} {operator} {value} "
            f"→ {len(df)} models (from {before})"
        )

    # Save output
    df.to_csv(output_file, index=False)

    print(f"\n✅ Saved {len(df)} matching models to {output_file}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Select models from a grid CSV using parameter filters."
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Input model CSV file"
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output CSV file"
    )

    parser.add_argument(
        "--param",
        nargs="+",
        required=True,
        help=(
            "Parameter filters, e.g. "
            "temp=11000 mass>800 S<3"
        )
    )

    args = parser.parse_args()

    filters = parse_param_filters(args.param)

    select_models(args.csv, args.out, filters)
