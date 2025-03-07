# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-02 04:06:54 (ywatanabe)"
# # File: ./mngs_repo/src/mngs/str/_readable_bytes.py
# 
# def readable_bytes(num, suffix="B"):
#     """Convert a number of bytes to a human-readable format.
# 
#     Parameters
#     ----------
#     num : int
#         The number of bytes to convert.
#     suffix : str, optional
#         The suffix to append to the unit (default is "B" for bytes).
# 
#     Returns
#     -------
#     str
#         A human-readable string representation of the byte size.
# 
#     Example
#     -------
#     >>> readable_bytes(1024)
#     '1.0 KiB'
#     >>> readable_bytes(1048576)
#     '1.0 MiB'
#     >>> readable_bytes(1073741824)
#     '1.0 GiB'
#     """
#     for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
#         if abs(num) < 1024.0:
#             return "%3.1f %s%s" % (num, unit, suffix)
#         num /= 1024.0
#     return "%.1f %s%s" % (num, "Yi", suffix)
# 
# 
# # EOF

# test from here --------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
import pytest
import numpy as np

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, os.path.join(project_root, "src"))

from mngs..str._readable_bytes import *

class Test_MainFunctionality:
    def setup_method(self):
        # Setup test fixtures
        pass

    def teardown_method(self):
        # Clean up after tests
        pass

    def test_basic_functionality(self):
        # Basic test case
        pass

    def test_edge_cases(self):
        # Edge case testing
        pass

    def test_error_handling(self):
        # Error handling testing
        pass
