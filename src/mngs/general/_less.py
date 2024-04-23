#!./env/bin/python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-04-21 12:05:35"
# Author: Yusuke Watanabe (ywata1989@gmail.com)

"""
This script does XYZ.
"""

import os
import sys

import matplotlib.pyplot as plt

# Imports
import mngs
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

# # Config
# CONFIG = mngs.gen.load_configs()

# Functions
def less(output):
    """
    Print the given output using `less` in an IPython or IPdb session.
    """
    import os
    import tempfile

    from IPython import get_ipython

    # Create a temporary file to hold the output
    with tempfile.NamedTemporaryFile(delete=False, mode="w+t") as tmpfile:
        # Write the output to the temporary file
        tmpfile.write(output)
        tmpfile_name = tmpfile.name

    # Use IPython's system command access to pipe the content of the temporary file to `less`
    get_ipython().system(f"less {tmpfile_name}")

    # Clean up the temporary file
    os.remove(tmpfile_name)


# (YOUR AWESOME CODE)

if __name__ == "__main__":
    # Start
    CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(
        sys, plt, verbose=False
    )

    # (YOUR AWESOME CODE)

    # Close
    mngs.gen.close(CONFIG, verbose=False, notify=False)

# EOF

"""
/ssh:ywatanabe@444:/home/ywatanabe/proj/entrance/mngs/gen/_less.py
"""
