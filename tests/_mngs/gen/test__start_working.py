# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-05 00:21:46 (ywatanabe)"
# # File: ./mngs_repo/src/mngs/gen/_start.py
# 
# import inspect
# import os as _os
# import re
# from datetime import datetime
# from pprint import pprint
# from time import sleep
# 
# import matplotlib
# import mngs
# 
# from ..dict import DotDict
# from ..io._load import load
# from ..path import split
# from ..reproduce._fix_seeds import fix_seeds
# from ..reproduce._gen_ID import gen_ID
# 
# 
# def start(
#     sys=None,
#     plt=None,
#     sdir=None,
#     sdir_suffix=None,
#     verbose=True,
#     # Random seeds
#     os=None,
#     random=None,
#     np=None,
#     torch=None,
#     tf=None,
#     seed=42,
#     # matplotlib
#     agg=False,
#     fig_size_mm=(160, 100),
#     fig_scale=1.0,
#     dpi_display=100,
#     dpi_save=300,
#     font_size_base=10,
#     font_size_title=10,
#     font_size_axis_label=8,
#     font_size_tick_label=7,
#     font_size_legend=6,
#     hide_top_right_spines=True,
#     alpha=0.9,
#     line_width=0.5,
#     clear: bool = False,
# ):
#     """
#     Example:
# 
#     \"""
#     This script does XYZ.
#     \"""
# 
#     # Imports
# 
#     import matplotlib.pyplot as plt
#     import numpy as np
#     import pandas as pd
#     import torch
#     import torch.nn as nn
#     import torch.nn.functional as F
# 
#     # Config
#     CONFIG = mngs.gen.load_configs()
# 
#     # Functions
#     # (Your awesome code here)
# 
#     if __name__ == '__main__':
#         # Start
#         CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(sys, plt)
# 
#         # (Your awesome code here)
# 
#         # Close
#         mngs.gen.close(CONFIG)
# 
#     # EOF
# 
#     \"""
#     /home/ywatanabe/template.py
#     \"""
#     """
# 
#     # Initialize plt
#     plt.close("all")
# 
#     # Timer
#     start_time = datetime.now()
# 
#     IS_DEBUG = _get_debug_mode()
# 
#     # ID
#     ID = gen_ID(N=4)
#     ID = ID if not IS_DEBUG else "DEBUG_" + ID
#     PID = _os.getpid()
#     print(
#         f"\n{'#'*40}\n## mngs v{mngs.__version__}\n## {ID} (PID: {PID})\n{'#'*40}\n"
#     )
#     sleep(1)
# 
#     ########################################
#     # Defines SDIR
#     ########################################
#     if sdir is None:
#         __file__ = inspect.stack()[1].filename
#         if "ipython" in __file__:
#             __file__ = f"/tmp/fake_{_os.getenv('USER')}.py"
#         spath = __file__
#         # spath = mngs.path.get_spath()
#         _sdir, sfname, _ = split(spath)
#         sdir = _sdir + sfname + "/" + "RUNNING" + "/" + ID + "/"
#         sdir = sdir.replace("/./", "/")
#         if sdir_suffix:
#             sdir = sdir[:-1] + f"-{sdir_suffix}/"
# 
#     if clear:
#         _clear_python_log_dir(_sdir + sfname + "/")
# 
#     _os.makedirs(sdir, exist_ok=True)
# 
#     relative_sdir = _simplify_relative_path(sdir)
# 
#     # # Relative SDIR
#     # base_path = _os.getcwd()
#     # relative_sdir = _os.path.relpath(sdir, base_path) if base_path else sdir
#     # # relative_srid = "scripts/memory-load/distance_between_gs_stats/RUNNING/2024Y-09M-12D-02h44m40s_GlBZ"
#     # relative_sdir.replace("scripts/", "./").replace("RUNNING/", "").replace(2024Y-09M-12D-02h44m40s_GlBZ, "")
# 
#     ########################################
#     # CONFIGs
#     ########################################
#     CONFIGS = mngs.io.load_configs(IS_DEBUG).to_dict()
#     CONFIGS["ID"] = ID
#     CONFIGS["START_TIME"] = start_time
#     CONFIGS["SDIR"] = sdir
#     CONFIGS["REL_SDIR"] = relative_sdir
#     if verbose:
#         print(f"\n{'-'*40}\n")
#         print(f"CONFIG:")
#         for k, v in CONFIGS.items():
#             print(f"\n{k}:\n{v}\n")
#         print(f"\n{'-'*40}\n")
# 
#     # Logging (tee)
#     if sys is not None:
#         sys.stdout, sys.stderr = mngs.gen.tee(
#             sys, sdir=sdir, verbose=verbose
#         )
#         CONFIGS["sys"] = sys
# 
#     # Random seeds
#     if (
#         (os is not None)
#         or (random is not None)
#         or (np is not None)
#         or (torch is not None)
#         or (tf is not None)
#     ):
#         fix_seeds(
#             os=os,
#             random=random,
#             np=np,
#             torch=torch,
#             seed=seed,
#             verbose=verbose,
#         )
# 
#     # Matplotlib configuration
#     if plt is not None:
#         plt, CC = mngs.plt.configure_mpl(
#             plt,
#             fig_size_mm=(160, 100),
#             fig_scale=fig_scale,
#             dpi_display=dpi_display,
#             dpi_save=dpi_save,
#             # font_size_base=font_size_base,
#             # font_size_title=font_size_title,
#             # font_size_axis_label=font_size_axis_label,
#             # font_size_tick_label=font_size_tick_label,
#             # font_size_legend=font_size_legend,
#             hide_top_right_spines=hide_top_right_spines,
#             alpha=alpha,
#             line_width=line_width,
#             verbose=verbose,
#         )
#         CC["gray"] = CC["grey"]
# 
#     if agg:
#         matplotlib.use("Agg")
# 
#     CONFIGS = DotDict(CONFIGS)
# 
#     if verbose:
#         print(f"\n{'-'*40}\n")
#         pprint(CONFIGS)
#         print(f"\n{'-'*40}\n")
# 
#     return CONFIGS, sys.stdout, sys.stderr, plt, CC
# 
# def _simplify_relative_path(sdir):
#     """
#     Simplify the relative path by removing specific patterns.
# 
#     Example
#     -------
#     sdir = '/home/user/scripts/memory-load/distance_between_gs_stats/RUNNING/2024Y-09M-12D-02h44m40s_GlBZ'
#     simplified_path = simplify_relative_path(sdir)
#     print(simplified_path)
#     # Output: './memory-load/distance_between_gs_stats/'
# 
#     Parameters
#     ----------
#     sdir : str
#         The directory path to simplify
# 
#     Returns
#     -------
#     str
#         Simplified relative path
#     """
#     base_path = _os.getcwd()
#     relative_sdir = _os.path.relpath(sdir, base_path) if base_path else sdir
#     simplified_path = relative_sdir.replace("scripts/", "./").replace(
#         "RUNNING/", ""
#     )
#     # Remove date-time pattern and random string
#     simplified_path = re.sub(
#         r"\d{4}Y-\d{2}M-\d{2}D-\d{2}h\d{2}m\d{2}s_\w+/?$", "", simplified_path
#     )
#     return simplified_path
# 
# 
# def _get_debug_mode():
#     # Debug mode check
#     try:
#         IS_DEBUG_PATH = "./config/IS_DEBUG.yaml"
#         if _os.path.exists(IS_DEBUG_PATH):
#             IS_DEBUG = load(IS_DEBUG_PATH).get("IS_DEBUG", False)
#             if IS_DEBUG == "true":
#                 IS_DEBUG = True
#         else:
#             IS_DEBUG = False
# 
#     except Exception as e:
#         print(e)
#         IS_DEBUG = False
#     return IS_DEBUG
# 
# 
# def _clear_python_log_dir(log_dir):
#     try:
#         if _os.path.exists(log_dir):
#             _os.system(f"rm -rf {log_dir}")
#     except Exception as e:
#         print(f"Failed to clear directory {log_dir}: {e}")
# 
# if __name__ == "__main__":
#     """
#     This script does XYZ.
#     """
# 
#     # Imports
#     import os
#     import sys
# 
#     import matplotlib.pyplot as plt
# 
#     # Config
#     CONFIG = mngs.io.load_configs()
# 
#     # Functions
#     # Your awesome code here :)
# 
#     if __name__ == "__main__":
#         # Start
#         CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(sys, plt)
# 
#         # Your awesome code here :)
# 
#         # Close
#         mngs.gen.close(CONFIG)
# 
# # EOF
# 
# """
# /home/ywatanabe/proj/entrance/mngs/gen/_start.py
# """
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

from mngs.gen._start_working import *

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
