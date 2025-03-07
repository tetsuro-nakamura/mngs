# src from here --------------------------------------------------------------------------------
# #!/./env/bin/python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-09-28 11:17:22 (ywatanabe)"
# # /home/ywatanabe/proj/mngs_repo/src/mngs/pd/_to_xyz.py
# 
# import mngs
# import numpy as np
# import pandas as pd
# 
# def to_xyz(data_frame):
#     """
#     Convert a heatmap DataFrame into x, y, z format.
# 
#     Ensure the index and columns are the same, and if either exists, replace with that.
# 
#     Example
#     -------
#     data_frame = pd.DataFrame(...)  # Your DataFrame here
#     out = to_xyz(data_frame)
#     print(out)
# 
#     Parameters
#     ----------
#     data_frame : pandas.DataFrame
#         The input DataFrame to be converted.
# 
#     Returns
#     -------
#     pandas.DataFrame
#         A DataFrame formatted with columns ['x', 'y', 'z']
#     """
#     assert data_frame.shape[0] == data_frame.shape[1]
# 
#     if not data_frame.index.equals(data_frame.columns):
#         if np.array_equal(data_frame.index, np.arange(len(data_frame.index))):
#             data_frame.columns = data_frame.index
#         elif np.array_equal(data_frame.columns, np.arange(len(data_frame.columns))):
#             data_frame.index = data_frame.columns
#         else:
#             raise ValueError("Either index or columns must be a range of integers")
# 
#     x_name = data_frame.index.name or 'x'
#     y_name = data_frame.columns.name or 'y'
# 
#     formatted_data_frames = []
# 
#     for column in data_frame.columns:
#         column_data_frame = data_frame[column]
#         formatted_data = pd.DataFrame({
#             x_name: column_data_frame.index,
#             y_name: column,
#             'z': column_data_frame.values
#         })
#         formatted_data_frames.append(formatted_data)
# 
#     result = pd.concat(formatted_data_frames, ignore_index=True)
#     result = mngs.pd.mv(result, 'z', -1)
# 
#     return result
# 
# # def to_xyz(data_frame):
# #     """
# #     Convert a heatmap DataFrame into x, y, z format.
# 
# #     Ensure the index and columns are the same, and if either exists, replace with that.
# 
# #     Example
# #     -------
# #     data_frame = pd.DataFrame(...)  # Your DataFrame here
# #     out = to_xy(data_frame)
# #     print(out)
# 
# #     Parameters
# #     ----------
# #     data_frame : pandas.DataFrame
# #         The input DataFrame to be converted.
# 
# #     Returns
# #     -------
# #     pandas.DataFrame
# #         A DataFrame formatted with columns ['x', 'y', 'z']
# #     """
# #     assert data_frame.shape[0] == data_frame.shape[1]
# 
# #     if not data_frame.index.equals(data_frame.columns):
# 
# #         if (data_frame.index == np.array(range(len(data_frame.index)))).all():
# #             data_frame.columns = data_frame.index
# #         elif (
# #             data_frame.columns == np.array(range(len(data_frame.columns)))
# #         ).all():
# #             data_frame.index = data_frame.columns
# #         else:
# #             raise ValueError("Either index or columns must be a range of integers")
# 
# #     formatted_data_frames = []
# 
# #     for column in data_frame.columns:
# #         column_data_frame = data_frame[column]
# #         y_label = column_data_frame.name
# #         column_data_frame = pd.DataFrame(column_data_frame)
# #         column_data_frame["x"] = column_data_frame.index
# #         column_data_frame["y"] = y_label
# #         column_data_frame = column_data_frame.reset_index().drop(
# #             columns=["index"]
# #         )
# #         column_data_frame = column_data_frame.rename(columns={y_label: "z"})
# #         column_data_frame = mngs.pd.mv(column_data_frame, "z", -1)
# #         formatted_data_frames.append(column_data_frame)
# 
# #     return pd.concat(formatted_data_frames, ignore_index=True)

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

from mngs..pd._to_xyz import *

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
