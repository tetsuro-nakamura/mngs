#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-04-12 23:51:57 (ywatanabe)"

"""
This script does XYZ.
"""

# Imports
import math
import sys
import time

import mngs
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from mngs.general import torch_fn

# Config
CONFIG = mngs.gen.load_configs()

# Functions
class ModulationIndex(nn.Module):
    def __init__(self, n_bins=18, fp16=False):
        super(ModulationIndex, self).__init__()
        self.n_bins = n_bins
        self.fp16 = fp16
        self.register_buffer(
            "pha_bin_cutoffs", torch.linspace(-np.pi, np.pi, n_bins + 1)
        )

    def forward(self, pha, amp, epsilon=1e-9):
        """
        Compute the Modulation Index based on phase (pha) and amplitude (amp) tensors.

        Parameters:
        - pha (torch.Tensor): Tensor of phase values with shape
                              (batch_size, n_channels, n_freqs_pha, n_segments, sequence_length).
        - amp (torch.Tensor): Tensor of amplitude values with a similar shape as pha.
                              (batch_size, n_channels, n_freqs_amp, n_segments, sequence_length).

        Returns:
        - MI (torch.Tensor): The Modulation Index for each batch and channel.
        """
        assert pha.ndim == amp.ndim == 5

        if self.fp16:
            pha, amp = pha.half().contiguous(), amp.half().contiguous()
        else:
            pha, amp = pha.float().contiguous(), amp.float().contiguous()

        device = pha.device

        pha_masks = self._phase_to_masks(pha, self.pha_bin_cutoffs.to(device))
        # (batch_size, n_channels, n_freqs_pha, n_segments, sequence_length, n_bins)

        # Expands amp and masks to utilize broadcasting
        i_batch = 0
        i_chs = 1
        i_freqs_pha = 2
        i_freqs_amp = 3
        i_segments = 4
        i_time = 5
        i_bins = 6

        # Coupling
        pha_masks = pha_masks.unsqueeze(i_freqs_amp)
        amp = amp.unsqueeze(i_freqs_pha).unsqueeze(i_bins)
        amp_bins = pha_masks * amp

        # Takes mean amplitude in each bin
        amp_sums = amp_bins.sum(dim=i_time, keepdims=True)
        counts = pha_masks.sum(dim=i_time, keepdims=True)
        amp_means = amp_sums / (counts + epsilon)

        amp_probs = amp_means / (
            amp_means.sum(dim=-1, keepdims=True) + epsilon
        )

        MI = (
            torch.log(torch.tensor(self.n_bins, device=device) + epsilon)
            + (amp_probs * (amp_probs + epsilon).log()).sum(dim=-1)
        ) / torch.log(torch.tensor(self.n_bins, device=device))

        # Squeeze the n_bin dimension
        MI = MI.squeeze(-1)

        # Takes mean along the n_segments dimension
        MI = MI.mean(axis=-1)

        if MI.isnan().any():
            raise ValueError(
                "NaN values detected in Modulation Index calculation."
            )

        return MI

    @staticmethod
    def _phase_to_masks(pha, phase_bin_cutoffs):
        n_bins = int(len(phase_bin_cutoffs) - 1)
        bin_indices = (
            (
                (
                    torch.bucketize(pha, phase_bin_cutoffs, right=False) - 1
                ).clamp(0, n_bins - 1)
            )
            .long()
            .to(pha.device)
        )
        one_hot_masks = F.one_hot(
            bin_indices,
            num_classes=n_bins,
        )
        return one_hot_masks


def _reshape(x, batch_size=2, n_chs=4):
    return (
        torch.tensor(x)
        .float()
        .unsqueeze(0)
        .unsqueeze(0)
        .repeat(batch_size, n_chs, 1, 1, 1)
    )


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import mngs
    import seaborn as sns
    import tensorpac
    from tensorpac import Pac
    from tqdm import tqdm

    # Start
    CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(
        sys, plt, fig_scale=3
    )

    # Parameters
    FS = 512
    T_SEC = 5

    # Demo signal
    xx, tt, fs = mngs.dsp.demo_sig(fs=FS, t_sec=T_SEC, sig_type="tensorpac")
    # xx.shape: (8, 19, 20, 512)

    # Tensorpac
    (
        pha,
        amp,
        freqs_pha,
        freqs_amp,
        pac_tp,
    ) = mngs.dsp.utils.pac.calc_pac_with_tensorpac(xx, fs, t_sec=T_SEC)

    # GPU calculation with mngs.dsp.nn.ModulationIndex
    pha, amp = _reshape(pha), _reshape(amp)
    pac_mngs = mngs.dsp.modulation_index(pha, amp).cpu().numpy()
    i_batch, i_ch = 0, 0
    pac_mngs = pac_mngs[i_batch, i_ch]

    # Plots
    fig = mngs.dsp.utils.pac.plot_PAC_mngs_vs_tensorpac(
        pac_mngs, pac_tp, freqs_pha, freqs_amp
    )
    # fig = plot_PAC_mngs_vs_tensorpac(pac_mngs, pac_tp, freqs_pha, freqs_amp)
    mngs.io.save(fig, CONFIG["SDIR"] + "modulation_index.png")  # plt.show()

    # Close
    mngs.gen.close(CONFIG)

# EOF

"""
/home/ywatanabe/proj/entrance/mngs/nn/_ModulationIndex.py
"""
