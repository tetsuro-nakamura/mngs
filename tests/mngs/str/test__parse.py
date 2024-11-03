# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-10-25 12:09:29 (ywatanabe)"
# # File: _parse.py
# 
# import re
# from typing import Dict, Union
# import logging
# 
# def parse(string: str, expression: str) -> Dict[str, Union[str, int]]:
#     """
#     Parse a string based on a given expression pattern.
# 
#     Parameters
#     ----------
#     string : str
#         The string to parse
#     expression : str
#         The expression pattern to match against the string
# 
#     Returns
#     -------
#     Dict[str, Union[str, int]]
#         A dictionary containing parsed information
# 
#     Raises
#     ------
#     ValueError
#         If the string format does not match the given expression
#         If duplicate placeholders have inconsistent values
# 
#     Example
#     -------
#     >>> string = "./data/mat_tmp/Patient_23_002/Data_2010_07_31/Hour_12/UTC_12_02_00.mat"
#     >>> expression = "./data/mat_tmp/Patient_{patient_id}/Data_{YYYY}_{MM}_{DD}/Hour_{HH}/UTC_{HH}_{mm}_00.mat"
#     >>> parse_str(string, expression)
#     # {'patient_id': '23_002', 'YYYY': 2010, 'MM': 7, 'DD': 31, 'HH': 12, 'mm': 2}
# 
#     # Inconsistent version
#     >>> string = "./data/mat_tmp/Patient_23_002/Data_2010_07_31/Hour_12/UTC_99_02_00.mat"
#     >>> expression = "./data/mat_tmp/Patient_{patient_id}/Data_{YYYY}_{MM}_{DD}/Hour_{HH}/UTC_{HH}_{mm}_00.mat"
#     >>> parse_str(string, expression)
#     # ValueError: Inconsistent values for placeholder 'HH'
#     """
# 
#     # Formatting
#     string = string.replace("/./", "/")
#     expression = expression.replace("f\"", "").replace("\"", "")
# 
#     placeholders = re.findall(r'{(\w+)}', expression)
#     pattern = re.sub(r'{(\w+)}', '([^/]+)', expression)
#     match = re.match(pattern, string)
# 
#     if not match:
#         logging.warning(f"String format does not match the given expression. \nString input: {string}\nExpression: {expression}")
#         return {}
#         # raise ValueError(f"String format does not match the given expression. \nString input: {string}\nExpression: {expression}")
# 
# 
#     groups = match.groups()
#     result = {}
# 
#     for placeholder, value in zip(placeholders, groups):
#         if placeholder in result and result[placeholder] != value:
#             raise ValueError(f"Inconsistent values for placeholder '{placeholder}'")
#         result[placeholder] = value
# 
#     return result
# 
# if __name__ == '__main__':
#     string = "./data/mat_tmp/Patient_23_002/Data_2010_07_31/Hour_12/UTC_12_02_00.mat"
#     expression = "./data/mat_tmp/Patient_{patient_id}/Data_{YYYY}_{MM}_{DD}/Hour_{HH}/UTC_{HH}_{mm}_00.mat"
#     results = parse_str(string, expression)
#     print(results)
# 
#     # Inconsistent version
#     string = "./data/mat_tmp/Patient_23_002/Data_2010_07_31/Hour_12/UTC_99_99_00.mat"
#     expression = "./data/mat_tmp/Patient_{patient_id}/Data_{YYYY}_{MM}_{DD}/Hour_{HH}/UTC_{HH}_{mm}_00.mat"
#     results = parse_str(string, expression) # this should raise error
#     print(results)

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
    sys.path.insert(0, project_root)

from src.mngs.str._parse import *

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
