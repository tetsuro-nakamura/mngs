# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-04 02:11:25 (ywatanabe)"
# # File: ./mngs_repo/src/mngs/dsp/_psd.py
# 
# """This script does XYZ."""
# 
# import torch
# 
# from ..decorators import torch_fn
# from ..nn._PSD import PSD
# 
# 
# @torch_fn
# def psd(
#     x,
#     fs,
#     prob=False,
#     dim=-1,
# ):
#     """
#     import matplotlib.pyplot as plt
# 
#     x, t, fs = mngs.dsp.demo_sig()  # (batch_size, n_chs, seq_len)
#     pp, ff = psd(x, fs)
# 
#     # Plots
#     plt, CC = mngs.plt.configure_mpl(plt)
#     fig, ax = mngs.plt.subplots()
#     ax.plot(fs, pp[0, 0])
#     ax.xlabel("Frequency [Hz]")
#     ax.ylabel("log(Power [uV^2 / Hz]) [a.u.]")
#     plt.show()
#     """
#     psd, freqs = PSD(fs, prob=prob, dim=dim)(x)
#     return psd, freqs
# 
# def band_powers(self, psd):
#     """
#     Calculate the average power for specified frequency bands.
#     """
#     assert len(self.low_freqs) == len(self.high_freqs)
# 
#     out = []
#     for ll, hh in zip(self.low_freqs, self.high_freqs):
#         band_indices = torch.where((freqs >= ll) & (freqs <= hh))[0].to(
#             psd.device
#         )
#         band_power = psd[..., band_indices].sum(dim=self.dim)
#         bandwidth = hh - ll
#         avg_band_power = band_power / bandwidth
#         out.append(avg_band_power)
#     out = torch.stack(out, dim=-1)
#     return out
# 
#     # Average Power in Each Frequency Band
#     avg_band_powers = self.calc_band_avg_power(psd, freqs)
#     return (avg_band_powers,)
# 
# if __name__ == "__main__":
#     import sys
#     import mngs
# 
#     import matplotlib.pyplot as plt
# 
#     # Start
#     CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(sys, plt)
# 
#     # Parameters
#     SIG_TYPE = "chirp"
# 
#     # Demo signal
#     xx, tt, fs = mngs.dsp.demo_sig(SIG_TYPE)  # (8, 19, 384)
# 
#     # PSD calculation
#     pp, ff = psd(xx, fs, prob=True)
# 
#     # Plots
#     fig, axes = mngs.plt.subplots(nrows=2)
# 
#     axes[0].plot(tt, xx[0, 0], label=SIG_TYPE)
#     axes[1].set_title("Signal")
#     axes[0].set_xlabel("Time [s]")
#     axes[0].set_ylabel("Amplitude [?V]")
# 
#     axes[1].plot(ff, pp[0, 0])
#     axes[1].set_title("PSD (power spectrum density)")
#     axes[1].set_xlabel("Frequency [Hz]")
#     axes[1].set_ylabel("Log(Power [?V^2 / Hz]) [a.u.]")
# 
#     mngs.io.save(fig, "psd.png")
# 
#     # Close
#     mngs.gen.close(CONFIG)
# 
# # EOF
# 
# """
# /home/ywatanabe/proj/entrance/mngs/dsp/_psd.py
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

from mngs..dsp._psd import *

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
