#!/usr/bin/env python3
"""
Find the global minimum-S model across one or many CSV files (with variable numbers
of matched_* columns), and print a one-block summary that you can append to a file.

Internal uncertainty for selected parameters (temp, mass, menv, mhe, mh):
    sigma^2 = d^2 / (S1 - S0)
where:
  S0 = minimum S
  S1 = second-lowest S (global)
  d  = difference in that parameter between the two models
"""

from __future__ import annotations

import argparse
import glob
import math
import os
import sys
from typing import Dict, List, Optional, Sequence, Tuple

import pandas as pd


REQ_COLS = ["S", "temp", "mass", "menv", "mhe", "mh", "Xhebar", "h1", "h2", "w1"]
SIGMA_PARAMS = ["temp", "mass", "menv", "mhe", "mh"]


def read_one_csv(path: str) -> pd.DataFrame:
    # engine="python" is more tolerant if some rows have weird quoting; can be slower.
    df = pd.read_csv(path)
    df["_source_file"] = os.path.basename(path)
    return df


def gather_csvs(patterns: Sequence[str]) -> List[str]:
    paths: List[str] = []
    for p in patterns:
        hits = glob.glob(p)
        if hits:
            paths.extend(hits)
        else:
            # allow passing a literal filename that doesn't include glob meta
            if os.path.exists(p):
                paths.append(p)
    # unique + stable
    seen = set()
    uniq = []
    for x in paths:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def ensure_numeric(df: pd.DataFrame, cols: Sequence[str]) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def find_two_best(df_all: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    if "S" not in df_all.columns:
        raise ValueError("No 'S' column found after concatenation.")
    df_sorted = df_all.sort_values("S", ascending=True, kind="mergesort")
    df_sorted = df_sorted[df_sorted["S"].notna()]
    if len(df_sorted) < 2:
        raise ValueError("Need at least two models with finite S to compute sigmas.")
    best = df_sorted.iloc[0]
    second = df_sorted.iloc[1]
    return best, second


def internal_sigma(best: pd.Series, second: pd.Series, param: str) -> float:
    S0 = best["S"]
    S1 = second["S"]
    d = second[param] - best[param]
    denom = (S1 - S0)
    # Guardrails
    if pd.isna(S0) or pd.isna(S1) or pd.isna(d):
        return float("nan")
    if denom <= 0:
        # This should not happen if S1 is truly the second-lowest and not equal,
        # but keep it safe.
        return float("inf")
    sig2 = (d * d) / denom
    if sig2 < 0:
        return float("nan")
    return math.sqrt(sig2)


def fmt(x: object, ndp: int = 6) -> str:
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "nan"
    if isinstance(x, (int,)):
        return str(x)
    if isinstance(x, (float,)):
        return f"{x:.{ndp}g}"  # compact scientific if needed
    return str(x)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Report global minimum-S solution across one/many CSVs."
    )
    ap.add_argument(
        "inputs",
        nargs="+",
        help="CSV filename(s) or glob patterns (e.g. 'results/*.csv')",
    )
    ap.add_argument(
        "--ndp",
        type=int,
        default=6,
        help="Significant digits for numeric printing (default: 6)",
    )
    args = ap.parse_args(argv)

    paths = gather_csvs(args.inputs)
    if not paths:
        print("ERROR: No CSV files matched your inputs.", file=sys.stderr)
        return 2

    dfs = []
    for p in paths:
        df = read_one_csv(p)
        # only enforce required numeric columns we need; matched_* can vary freely
        df = ensure_numeric(df, ["S"] + SIGMA_PARAMS + ["Xhebar", "h1", "h2", "w1"])
        # keep only rows that have the required columns present (skip bad files cleanly)
        missing = [c for c in REQ_COLS if c not in df.columns]
        if missing:
            print(f"WARNING: skipping {p} (missing columns: {missing})", file=sys.stderr)
            continue
        dfs.append(df)

    if not dfs:
        print("ERROR: None of the CSVs contained the required columns.", file=sys.stderr)
        return 2

    df_all = pd.concat(dfs, ignore_index=True)

    best, second = find_two_best(df_all)

    S0 = best["S"]
    S1 = second["S"]

    # Compute sigmas for the requested physical parameters
    sigmas: Dict[str, float] = {}
    for p in SIGMA_PARAMS:
        sigmas[p] = internal_sigma(best, second, p)

    # Print in an append-friendly block (single model summary)
    # You can redirect/append: python report_min.py results/*.csv >> summary.txt
    print("# --- minimum-S model summary ---")
    print(f"# files_considered = {len(dfs)} (from {len(paths)} matched paths)")
#    print(f"# best_source_file = {best.get('_source_file', 'unknown')}")
    print(f"# second_source_file = {second.get('_source_file', 'unknown')}")
    print(f"# S0(best) = {fmt(S0, args.ndp)}")
    print(f"# S1(2nd)  = {fmt(S1, args.ndp)}")
    print(f"# deltaS   = {fmt(S1 - S0, args.ndp)}")
    print("#")

    # Core parameters
    print(f"temp   = {fmt(best['temp'], args.ndp)}   sigma_temp   = {fmt(sigmas['temp'], args.ndp)}")
    print(f"mass   = {fmt(best['mass'], args.ndp)}   sigma_mass   = {fmt(sigmas['mass'], args.ndp)}")
    print(f"menv   = {fmt(best['menv'], args.ndp)}   sigma_menv   = {fmt(sigmas['menv'], args.ndp)}")
    print(f"mhe    = {fmt(best['mhe'], args.ndp)}   sigma_mhe    = {fmt(sigmas['mhe'], args.ndp)}")
    print(f"mh     = {fmt(best['mh'], args.ndp)}   sigma_mh     = {fmt(sigmas['mh'], args.ndp)}")

    # Other requested outputs (no sigma)
    print(f"Xhebar = {fmt(best['Xhebar'], args.ndp)}")
    print(f"h1     = {fmt(best['h1'], args.ndp)}")
    print(f"h2     = {fmt(best['h2'], args.ndp)}")
    print(f"w1     = {fmt(best['w1'], args.ndp)}")

    # Optional: show model_index if present (often useful)
    if "model_index" in df_all.columns:
        print(f"model_index = {fmt(best.get('model_index', 'nan'), args.ndp)}")

    print("# --- end summary ---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

