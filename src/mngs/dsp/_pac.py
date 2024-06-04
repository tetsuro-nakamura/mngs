#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-04-29 11:03:51 (ywatanabe)"

import sys

import matplotlib.pyplot as plt
import mngs
import numpy as np
from mngs.general import batch_fn, torch_fn
from mngs.nn import PAC

"""
mngs.dsp.pac function
"""


@torch_fn
@batch_fn
def pac(
    x,
    fs,
    pha_start_hz=2,
    pha_end_hz=20,
    pha_n_bands=100,
    amp_start_hz=60,
    amp_end_hz=160,
    amp_n_bands=100,
    device="cuda",
    batch_size=1,
    fp16=False,
    trainable=False,
    n_perm=None,
    amp_prob=False,
):
    """
    Compute the phase-amplitude coupling (PAC) for signals. This function automatically handles inputs as
    PyTorch tensors, NumPy arrays, or pandas DataFrames.

    Arguments:
    - x (torch.Tensor | np.ndarray | pd.DataFrame): Input signal. Shape can be either (batch_size, n_chs, seq_len) or
    - fs (float): Sampling frequency of the input signal.
    - pha_start_hz (float, optional): Start frequency for phase bands. Default is 2 Hz.
    - pha_end_hz (float, optional): End frequency for phase bands. Default is 20 Hz.
    - pha_n_bands (int, optional): Number of phase bands. Default is 100.
    - amp_start_hz (float, optional): Start frequency for amplitude bands. Default is 60 Hz.
    - amp_end_hz (float, optional): End frequency for amplitude bands. Default is 160 Hz.
    - amp_n_bands (int, optional): Number of amplitude bands. Default is 100.

    Returns:
    - torch.Tensor: PAC values. Shape: (batch_size, n_chs, pha_n_bands, amp_n_bands)
    - numpy.ndarray: Phase bands used for the computation.
    - numpy.ndarray: Amplitude bands used for the computation.

    Example:
        FS = 512
        T_SEC = 4
        xx, tt, fs = mngs.dsp.demo_sig(
            batch_size=1, n_chs=1, fs=FS, t_sec=T_SEC, sig_type="tensorpac"
        )
        pac, pha_mids_hz, amp_mids_hz = mngs.dsp.pac(xx, fs)
    """
    m = PAC(
        x.shape[-1],
        fs,
        pha_start_hz=pha_start_hz,
        pha_end_hz=pha_end_hz,
        pha_n_bands=pha_n_bands,
        amp_start_hz=amp_start_hz,
        amp_end_hz=amp_end_hz,
        amp_n_bands=amp_n_bands,
        fp16=fp16,
        trainable=trainable,
        n_perm=n_perm,
        amp_prob=amp_prob,
    ).to(device)
    return m(x.to(device)), m.PHA_MIDS_HZ, m.AMP_MIDS_HZ


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import mngs
    import numpy as np

    # Start
    CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(sys, plt)

    # Parameters
    FS = 512
    T_SEC = 4
    # IS_TRAINABLE = False
    # FP16 = True

    for IS_TRAINABLE in [True, False]:
        for FP16 in [True, False]:

            # Demo signal
            xx, tt, fs = mngs.dsp.demo_sig(
                batch_size=1, n_chs=1, fs=FS, t_sec=T_SEC, sig_type="pac"
            )

            # mngs calculation
            pac_mngs, pha_mids_mngs, amp_mids_mngs = mngs.dsp.pac(
                xx,
                fs,
                pha_n_bands=50,
                amp_n_bands=30,
                trainable=IS_TRAINABLE,
                fp16=FP16,
            )
            i_batch, i_ch = 0, 0
            pac_mngs = pac_mngs[i_batch, i_ch]

            # Tensorpac calculation
            (
                _,
                _,
                _pha_mids_tp,
                _amp_mids_tp,
                pac_tp,
            ) = mngs.dsp.utils.pac.calc_pac_with_tensorpac(xx, fs, T_SEC)

            # Validates the consitency in frequency definitions
            assert np.allclose(pha_mids_mngs, _pha_mids_tp)
            assert np.allclose(amp_mids_mngs, _amp_mids_tp)

            mngs.io.save(
                (pac_mngs, pac_tp, pha_mids_mngs, amp_mids_mngs),
                "./data/cache.npz",
            )

            # ################################################################################
            # # cache
            # pac_mngs, pac_tp, pha_mids_mngs, amp_mids_mngs = mngs.io.load(
            #     "./data/cache.npz"
            # )
            # ################################################################################

            # Plots
            fig = mngs.dsp.utils.pac.plot_PAC_mngs_vs_tensorpac(
                pac_mngs, pac_tp, pha_mids_mngs, amp_mids_mngs
            )
            fig.suptitle(
                "Phase-Amplitude Coupling calculation\n\n(Bandpass Filtering -> Hilbert Transformation-> Modulation Index)"
            )
            plt.show()

            mngs.gen.reload(mngs.dsp)

            # Saves the figure
            trainable_str = "trainable" if IS_TRAINABLE else "static"
            fp_str = "fp16" if FP16 else "fp32"
            mngs.io.save(
                fig, f"pac_with_{trainable_str}_bandpass_{fp_str}.png"
            )

# EOF

"""
/home/ywatanabe/proj/entrance/mngs/dsp/_pac.py
"""
