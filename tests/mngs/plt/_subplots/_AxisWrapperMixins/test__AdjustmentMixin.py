# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-25 00:33:37 (ywatanabe)"
# # File: ./mngs_repo/src/mngs/plt/_subplots/_AxisWrapperMixins/_AdjustmentMixin.py
# 
# __file__ = "/home/ywatanabe/proj/mngs_repo/src/mngs/plt/_subplots/_AxisWrapperMixins/_AdjustmentMixin.py"
# 
# """
# Functionality:
#     * Provides methods for adjusting matplotlib plot aesthetics
# Input:
#     * Label rotations, axis labels, tick values, spines, and plot extent
# Output:
#     * Modified matplotlib axis object
# Prerequisites:
#     * matplotlib, mngs.plt.ax
# """
# 
# from typing import List, Optional, Union
# from ....plt import ax as ax_module
# 
# 
# class AdjustmentMixin:
#     """Mixin class for matplotlib axis adjustments."""
# 
#     def rotate_labels(
#         self,
#         x: float = 30,
#         y: float = 30,
#         x_ha: str = "right",
#         y_ha: str = "center",
#     ) -> None:
#         self.axis = ax_module.rotate_labels(
#             self.axis, x=x, y=y, x_ha=x_ha, y_ha=y_ha
#         )
# 
# 
#     def legend(self, loc: str = "upper left") -> None:
#         """Places legend at specified location, with support for outside positions.
# 
#         Parameters
#         ----------
#         loc : str
#             Legend position. Standard matplotlib positions plus:
#             - upper/lower/center variants: e.g. "upper right out", "lower left out"
#             - directional shortcuts: "right", "left", "upper", "lower"
#             - center variants: "center right out", "center left out"
#             - alternative formats: "right upper out", "left lower out" etc.
#         """
# 
#         outside_positions = {
#             # Upper right variants
#             "upper right out": ("center left", (1.15, 0.85)),
#             "right upper out": ("center left", (1.15, 0.85)),
#             # Center right variants
#             "center right out": ("center left", (1.15, 0.5)),
#             "right out": ("center left", (1.15, 0.5)),
#             "right": ("center left", (1.05, 0.5)),
#             # Lower right variants
#             "lower right out": ("center left", (1.15, 0.15)),
#             "right lower out": ("center left", (1.15, 0.15)),
#             # Upper left variants
#             "upper left out": ("center right", (-0.25, 0.85)),
#             "left upper out": ("center right", (-0.25, 0.85)),
#             # Center left variants
#             "center left out": ("center right", (-0.25, 0.5)),
#             "left out": ("center right", (-0.25, 0.5)),
#             "left": ("center right", (-0.15, 0.5)),
#             # Lower left variants
#             "lower left out": ("center right", (-0.25, 0.15)),
#             "left lower out": ("center right", (-0.25, 0.15)),
#             # Upper center variants
#             "upper center out": ("lower center", (0.5, 1.25)),
#             "upper out": ("lower center", (0.5, 1.25)),
#             # Lower center variants
#             "lower center out": ("upper center", (0.5, -0.25)),
#             "lower out": ("upper center", (0.5, -0.25)),
#         }
# 
#         if loc in outside_positions:
#             location, bbox = outside_positions[loc]
#             return self.axis.legend(loc=location, bbox_to_anchor=bbox)
#         return self.axis.legend(loc=loc)
# 
#     def set_xyt(
#         self,
#         x: Optional[str] = None,
#         y: Optional[str] = None,
#         tt: Optional[str] = None,
#         format_labels: bool = True,
#     ) -> None:
#         self.axis = ax_module.set_xyt(
#             self.axis,
#             x=x,
#             y=y,
#             t=tt,
#             format_labels=format_labels,
#         )
# 
#     def set_supxyt(
#         self,
#         xlabel: Optional[str] = None,
#         ylabel: Optional[str] = None,
#         title: Optional[str] = None,
#         format_labels: bool = True,
#     ) -> None:
#         self.axis = ax_module.set_supxyt(
#             self.axis,
#             xlabel=xlabel,
#             ylabel=ylabel,
#             title=title,
#             format_labels=format_labels,
#         )
# 
#     def set_ticks(
#         self,
#         xvals: Optional[List[Union[int, float]]] = None,
#         xticks: Optional[List[str]] = None,
#         yvals: Optional[List[Union[int, float]]] = None,
#         yticks: Optional[List[str]] = None,
#     ) -> None:
#         self.axis = ax_module.set_ticks(
#             self.axis,
#             xvals=xvals,
#             xticks=xticks,
#             yvals=yvals,
#             yticks=yticks,
#         )
# 
#     def set_n_ticks(self, n_xticks: int = 4, n_yticks: int = 4) -> None:
#         self.axis = ax_module.set_n_ticks(
#             self.axis, n_xticks=n_xticks, n_yticks=n_yticks
#         )
# 
#     def hide_spines(
#         self,
#         top: bool = True,
#         bottom: bool = True,
#         left: bool = True,
#         right: bool = True,
#         ticks: bool = True,
#         labels: bool = True,
#     ) -> None:
#         self.axis = ax_module.hide_spines(
#             self.axis,
#             top=top,
#             bottom=bottom,
#             left=left,
#             right=right,
#             ticks=ticks,
#             labels=labels,
#         )
# 
#     def extend(self, x_ratio: float = 1.0, y_ratio: float = 1.0) -> None:
#         self.axis = ax_module.extend(
#             self.axis, x_ratio=x_ratio, y_ratio=y_ratio
#         )
# 
#     def shift(self, dx: float = 0, dy: float = 0) -> None:
#         self.axis = ax_module.shift(self.axis, dx=dx, dy=dy)
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

from mngs..plt._subplots._AxisWrapperMixins._AdjustmentMixin import *

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
