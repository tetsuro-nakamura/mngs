# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-04 01:37:36 (ywatanabe)"
# # File: ./mngs_repo/src/mngs/ai/_gen_ai/_calc_cost.py
# 
# """
# Functionality:
#     - Calculates usage costs for AI model API calls
#     - Handles token-based pricing for different models
# Input:
#     - Model name
#     - Number of input and output tokens used
# Output:
#     - Total cost in USD based on token usage
# Prerequisites:
#     - MODELS parameter dictionary with pricing information
#     - pandas package
# """
# 
# from typing import Union, Any
# import pandas as pd
# 
# from .PARAMS import MODELS
# 
# 
# def calc_cost(
#     model: str,
#     input_tokens: int,
#     output_tokens: int
# ) -> float:
#     """Calculates API usage cost based on token count.
# 
#     Example
#     -------
#     >>> cost = calc_cost("gpt-4", 100, 50)
#     >>> print(f"${cost:.4f}")
#     $0.0030
# 
#     Parameters
#     ----------
#     model : str
#         Name of the AI model
#     input_tokens : int
#         Number of input tokens used
#     output_tokens : int
#         Number of output tokens used
# 
#     Returns
#     -------
#     float
#         Total cost in USD
# 
#     Raises
#     ------
#     ValueError
#         If model is not found in MODELS
#     """
#     models_df = pd.DataFrame(MODELS)
#     indi = models_df["name"] == model
# 
#     if not indi.any():
#         raise ValueError(f"Model '{model}' not found in pricing table")
# 
#     costs = models_df[["input_cost", "output_cost"]][indi]
#     cost = (
#         input_tokens * costs["input_cost"]
#         + output_tokens * costs["output_cost"]
#     ) / 1_000_000
# 
#     return cost.iloc[0]
# 
# # def calc_cost(model, input_tokens, output_tokens):
# #     indi = MODELS["name"] == model
# #     costs = MODELS[["input_cost", "output_cost"]][indi]
# #     cost = (
# #         input_tokens * costs["input_cost"]
# #         + output_tokens * costs["output_cost"]
# #     ) / 1_000_000
# #     return cost.iloc[0]
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

from mngs..ai._gen_ai._calc_cost import *

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
