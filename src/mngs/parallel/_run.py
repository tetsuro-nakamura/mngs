#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-11-07 07:32:16 (ywatanabe)"
# File: ./mngs_repo/src/mngs/parallel/_run.py

"""
1. Functionality:
   - Runs functions in parallel using ProcessPoolExecutor
   - Handles both single and multiple return values
   - Supports automatic CPU core detection
2. Input:
   - Function to run
   - List of items to process
   - Optional parameters for execution control
3. Output:
   - List of results or concatenated DataFrame/tuple
4. Prerequisites:
   - concurrent.futures
   - pandas
   - tqdm
"""

import multiprocessing
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, List

from tqdm import tqdm


def run(
    func: Callable,
    items: List[Any],
    n_jobs: int = -1,
    desc: str = "Processing",
) -> List[Any]:
    """Runs function in parallel using ThreadPoolExecutor.

    Parameters
    ----------
    func : Callable
        Function to run in parallel
    items : List[Any]
        List of items to process
    n_jobs : int, optional
        Number of jobs to run in parallel. -1 means using all processors
    desc : str, optional
        Description for progress bar

    Returns
    -------
    List[Any]
        Results of parallel execution
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    if not callable(func):
        raise ValueError("Func must be callable")
    if not isinstance(items, (list, tuple)):
        raise TypeError("Items must be a list or tuple")
    if not isinstance(n_jobs, int):
        raise TypeError("n_jobs must be an integer")

    cpu_count = multiprocessing.cpu_count()
    n_jobs = cpu_count if n_jobs < 0 else n_jobs

    if n_jobs > cpu_count:
        warnings.warn(f"n_jobs ({n_jobs}) is greater than CPU count ({cpu_count})")
    if n_jobs < 1:
        raise ValueError("n_jobs must be >= 1 or -1")

    results = [None] * len(items)  # Pre-allocate list
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = {executor.submit(func, item): idx
                  for idx, item in enumerate(items)}
        for future in tqdm(as_completed(futures), total=len(items), desc=desc):
            idx = futures[future]
            results[idx] = future.result()

    # If results contain multiple values (tuples), transpose them
    if results and isinstance(results[0], tuple):
        n_vars = len(results[0])
        return tuple([result[i] for result in results] for i in range(n_vars))

    return results


# EOF
