#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-11-08 04:35:31 (ywatanabe)"
# File: ./mngs_repo/src/mngs/pd/_to_numeric.py

import pandas as pd


def to_numeric(df):
    """Convert all possible columns in a DataFrame to numeric types.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame

    Returns
    -------
    pd.DataFrame
        DataFrame with numeric columns converted
    """
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            continue
    return df

# EOF
