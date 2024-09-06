#!./env/bin/python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-09-03 06:04:45 (ywatanabe)"
# /home/ywatanabe/proj/mngs_repo/src/mngs/pd/_mv.py


def mv(df, key, position, axis=1):
    """
    Move a row or column to a specified position in a DataFrame.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    key (str): The label of the row or column to move.
    position (int): The position to move the row or column to.
    axis (int, optional): 0 for rows, 1 for columns. Defaults to 1.

    Returns:
    pandas.DataFrame: A new DataFrame with the row or column moved.
    """
    if axis == 0:
        items = df.index.tolist()
    else:
        items = df.columns.tolist()
    items.remove(key)

    if position < 0:
        position += len(items) + 1

    items.insert(position, key)
    return df.reindex(items, axis=axis)


def mv_to_first(df, key, axis=0):
    """
    Move a row or column to the first position in a DataFrame.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    key (str): The label of the row or column to move.
    axis (int, optional): 0 for rows, 1 for columns. Defaults to 0.

    Returns:
    pandas.DataFrame: A new DataFrame with the row or column moved to the first position.
    """
    return mv(df, key, 0, axis)


def mv_to_last(df, key, axis=0):
    """
    Move a row or column to the last position in a DataFrame.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    key (str): The label of the row or column to move.
    axis (int, optional): 0 for rows, 1 for columns. Defaults to 0.

    Returns:
    pandas.DataFrame: A new DataFrame with the row or column moved to the last position.
    """
    return mv(df, key, -1, axis)
