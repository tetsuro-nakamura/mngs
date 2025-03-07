# src from here --------------------------------------------------------------------------------
# import matplotlib.pyplot as plt
# import numpy as np
# 
# 
# def map_ticks(ax, src, tgt, axis="x"):
#     """
#     Maps source tick positions or labels to new target labels on a matplotlib Axes object.
#     Supports both numeric positions and string labels for source ticks ('src'), enabling the mapping
#     to new target labels ('tgt'). This ensures only the specified target ticks are displayed on the
#     final axis, enhancing the clarity and readability of plots.
# 
#     Parameters:
#     - ax (matplotlib.axes.Axes): The Axes object to modify.
#     - src (list of str or numeric): Source positions (if numeric) or labels (if str) to map from.
#       When using string labels, ensure they match the current tick labels on the axis.
#     - tgt (list of str): New target labels to apply to the axis. Must have the same length as 'src'.
#     - axis (str): Specifies which axis to apply the tick modifications ('x' or 'y').
# 
#     Returns:
#     - ax (matplotlib.axes.Axes): The modified Axes object with adjusted tick labels.
# 
#     Examples:
#     --------
#     Numeric Example:
#         fig, ax = plt.subplots()
#         x = np.linspace(0, 2 * np.pi, 100)
#         y = np.sin(x)
#         ax.plot(x, y)  # Plot a sine wave
#         src = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]  # Numeric src positions
#         tgt = ['0', 'π/2', 'π', '3π/2', '2π']  # Corresponding target labels
#         map_ticks(ax, src, tgt, axis="x")  # Map src to tgt on the x-axis
#         plt.show()
# 
#     String Example:
#         fig, ax = plt.subplots()
#         categories = ['A', 'B', 'C', 'D', 'E']  # Initial categories
#         values = [1, 3, 2, 5, 4]
#         ax.bar(categories, values)  # Bar plot with string labels
#         src = ['A', 'B', 'C', 'D', 'E']  # Source labels to map from
#         tgt = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']  # New target labels
#         map_ticks(ax, src, tgt, axis="x")  # Apply the mapping
#         plt.show()
#     """
#     if len(src) != len(tgt):
#         raise ValueError(
#             "Source ('src') and target ('tgt') must have the same number of elements."
#         )
# 
#     # Determine tick positions if src is string data
#     if all(isinstance(item, str) for item in src):
#         if axis == "x":
#             all_labels = [label.get_text() for label in ax.get_xticklabels()]
#         else:
#             all_labels = [label.get_text() for label in ax.get_yticklabels()]
# 
#         # Find positions of src labels
#         src_positions = [all_labels.index(s) for s in src if s in all_labels]
#     else:
#         # Use src as positions directly if numeric
#         src_positions = src
# 
#     # Set the ticks and labels based on the specified axis
#     if axis == "x":
#         ax.set_xticks(src_positions)
#         ax.set_xticklabels(tgt)
#     elif axis == "y":
#         ax.set_yticks(src_positions)
#         ax.set_yticklabels(tgt)
#     else:
#         raise ValueError("Invalid axis argument. Use 'x' or 'y'.")
# 
#     return ax
# 
# 
# def numeric_example():
#     fig, axs = plt.subplots(2, 1, figsize=(10, 6))  # Two rows, one column
# 
#     # Original plot
#     x = np.linspace(0, 2 * np.pi, 100)
#     y = np.sin(x)
#     axs[0].plot(x, y)  # Plot a sine wave on the first row
#     axs[0].set_title("Original Numeric Labels")
# 
#     # Numeric src positions for ticks (e.g., multiples of pi) and target labels
#     src = [0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]
#     tgt = ["0", "π/2", "π", "3π/2", "2π"]
# 
#     # Plot with mapped ticks
#     axs[1].plot(x, y)  # Plot again on the second row for mapped labels
#     map_ticks(axs[1], src, tgt, axis="x")
#     axs[1].set_title("Mapped Numeric Labels")
# 
#     return fig
# 
# 
# def string_example():
#     fig, axs = plt.subplots(2, 1, figsize=(10, 6))  # Two rows, one column
# 
#     # Original plot with categorical string labels
#     categories = ["A", "B", "C", "D", "E"]
#     values = [1, 3, 2, 5, 4]
#     axs[0].bar(categories, values)
#     axs[0].set_title("Original String Labels")
# 
#     # src as the existing labels to change and target labels
#     src = categories
#     tgt = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
# 
#     # Plot with mapped string labels
#     axs[1].bar(
#         categories, values
#     )  # Bar plot again on the second row for mapped labels
#     map_ticks(axs[1], src, tgt, axis="x")
#     axs[1].set_title("Mapped String Labels")
# 
#     return fig
# 
# 
# # Execute examples
# if __name__ == "__main__":
#     fig_numeric = numeric_example()
#     fig_string = string_example()
# 
#     plt.tight_layout()
#     plt.show()

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

from mngs..plt.ax._map_ticks import *

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
