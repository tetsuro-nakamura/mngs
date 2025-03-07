#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-12-23 13:11:43 (ywatanabe)"
# File: /home/ywatanabe/proj/mngs_repo/src/mngs/io/_load_modules/_txt.py

__file__ = "/home/ywatanabe/proj/mngs_repo/src/mngs/io/_load_modules/_txt.py"

import warnings

def _load_txt(lpath, **kwargs):
    """Load text file and return non-empty lines."""
    try:
        if not lpath.endswith((".txt", ".log", ".event", ".py", ".sh", "")):
            warnings.warn("File must have .txt, .log or .event extension")

        # Try UTF-8 first (most common)
        try:
            with open(lpath, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.read().splitlines() if line.strip()]
        except UnicodeDecodeError:
            # Fallback to system default encoding
            with open(lpath, "r") as f:
                return [line.strip() for line in f.read().splitlines() if line.strip()]

    except (ValueError, FileNotFoundError) as e:
        raise ValueError(f"Error loading file {lpath}: {str(e)}")

# def _load_txt(lpath, **kwargs):
#     """Load text file and return non-empty lines."""
#     try:
#         if not lpath.endswith((".txt", ".log", ".event", ".py", ".sh", "")):
#             warnings.warn("File must have .txt, .log or .event extension")

#         # with open(lpath, 'r', encoding='utf-8') as f:
#         #     return [
#         #         line.strip() for line in f.read().splitlines() if line.strip()
#         #     ]

#         encoding = _check_encoding(lpath)
#         with open(lpath, "r", encoding="utf-8") as f:
#             return [
#                 line.strip() for line in f.read().splitlines() if line.strip()
#             ]
#     except (ValueError, FileNotFoundError) as e:
#         raise ValueError(f"Error loading file {lpath}: {str(e)}")


def _check_encoding(file_path):
    """Check file encoding by trying common encodings."""
    encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1', 'ascii']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Unable to determine encoding for {file_path}")

# def _check_encoding(file_path):
#     """
#     Check the encoding of a given file.

#     This function attempts to read the file with different encodings
#     to determine the correct one.

#     Parameters:
#     -----------
#     file_path : str
#         The path to the file to check.

#     Returns:
#     --------
#     str
#         The detected encoding of the file.

#     Raises:
#     -------
#     IOError
#         If the file cannot be read or the encoding cannot be determined.
#     """
#     import chardet

#     with open(file_path, "rb") as file:
#         raw_data = file.read()

#     result = chardet.detect(raw_data)
#     return result["encoding"]

# EOF
