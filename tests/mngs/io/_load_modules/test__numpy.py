# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-14 07:55:44 (ywatanabe)"
# # File: ./mngs_repo/src/mngs/io/_load_modules/_numpy.py
# 
# from typing import Any
# 
# import numpy as np
# 
# 
# def _load_npy(lpath: str, **kwargs) -> Any:
#     """Load NPY or NPZ file."""
#     if lpath.endswith(".npy"):
#         return __load_npy(lpath, **kwargs)
#     elif lpath.endswith(".npz"):
#         return __load_npz(lpath, **kwargs)
#     raise ValueError("File must have .npy or .npz extension")
# 
# 
# def __load_npy(lpath: str, **kwargs) -> Any:
#     """Load NPY file."""
#     return np.load(lpath, allow_pickle=True, **kwargs)
# 
# 
# def __load_npz(lpath: str, **kwargs) -> Any:
#     """Load NPZ file."""
#     obj = np.load(lpath)
#     return [v for v in dict(obj).values()]
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

from mngs..io._load_modules._numpy import *

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
