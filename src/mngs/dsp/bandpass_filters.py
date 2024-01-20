#!/usr/bin/env python


import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal
import torch
import torch.nn as nn
import torch.nn.functional as F
from obspy.imaging.cm import obspy_sequential
from obspy.signal.tf_misfit import cwt


class BandPassFilterTorch(nn.Module):
    """
    A PyTorch module that applies a bandpass filter to an input signal using FIR filter coefficients.

    Attributes:
        fs (int): The sampling frequency of the input signal.
        order (int): The order of the filter. Defaults to the sampling frequency if not provided.
        numtaps (int): The number of taps in the filter (order + 1).
        filters (torch.Tensor): The FIR filter coefficients, shaped as (1, 1, numtaps).

    Parameters:
        order (int, optional): The order of the filter. Defaults to the sampling frequency if not provided.
        low_hz (float): The lower cutoff frequency for the bandpass filter.
        high_hz (float): The higher cutoff frequency for the bandpass filter.
        fs (int): The sampling frequency of the input signal.
        n_chs (int): The number of channels in the input signal.

    Methods:
        forward(x): Applies the bandpass filter to the input signal `x`.

    Args:
        x (torch.Tensor): The input signal to be filtered, shaped as (batch_size, n_chs, signal_length) for 3D input
                          or (batch_size, signal_length) for 2D input.

    Returns:
        torch.Tensor: The filtered signal, with the same shape as the input signal.

    References:
        - SincNet implementation: https://raw.githubusercontent.com/mravanelli/SincNet/master/dnn_models.py
        - FIR filter design: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html
    """

    def __init__(self, order=None, low_hz=30, high_hz=60, fs=250, n_chs=19):
        super().__init__()
        self.fs = fs
        # nyq = fs / 2
        self.order = fs if order is None else order
        self.numtaps = self.order + 1
        filter_npy = scipy.signal.firwin(
            self.numtaps,
            [low_hz, high_hz],
            pass_zero="bandpass",
            fs=fs,
        )

        self.register_buffer(
            "filters", torch.tensor(filter_npy).unsqueeze(0).unsqueeze(0)
        )

    def forward(self, x):
        """
            Apply the bandpass filter to the input signal.

        The method applies a bandpass filter to the input signal using a FIR filter with the coefficients stored in the `filters` attribute. The filtering is performed in two passes to ensure zero-phase distortion: first forward and then backward.

        Arguments:
            x (torch.Tensor): The input signal tensor. If the input is 3D, it should have the shape (batch_size, n_chs, signal_length), where `n_chs` is the number of channels and `signal_length` is the length of the signal. If the input is 2D, it should have the shape (batch_size, signal_length).

        Returns:
            torch.Tensor: The filtered signal tensor. The output tensor will have the same shape as the input tensor.

        Data Types:
            Input: torch.Tensor (float32 or float64 typically, depending on the model's precision)
            Output: torch.Tensor (same type as input)

        Data Shapes:
            Input: (batch_size, n_chs, signal_length) for 3D input or (batch_size, signal_length) for 2D input
            Output: Same as input

        References:
            - Convolution operation: https://pytorch.org/docs/stable/generated/torch.nn.functional.conv1d.html
            - Zero-phase filtering technique: https://en.wikipedia.org/wiki/Zero-phase_filtering
        """

        dim = x.ndim
        # sig_len_orig = x.shape[-1]

        if dim == 3:
            bs, n_chs, sig_len = x.shape
            x = x.reshape(bs * n_chs, 1, sig_len)

        filted = F.conv1d(
            x, self.filters.type_as(x), padding=int(self.numtaps / 2)
        )
        filted = filted.flip(dims=[-1])  # to backward
        filted = F.conv1d(
            filted, self.filters.type_as(x), padding=int(self.numtaps / 2)
        )
        filted = filted.flip(dims=[-1])  # reverse to the original order

        filted = filted[..., 1:-1]
        # print(self.order, filted.shape[-1])

        if dim == 3:
            filted = filted.reshape(bs, n_chs, -1)

        return filted


class BandPasserCPUTorch:
    """
    A class that applies a bandpass filter to an input signal using a Butterworth filter on the CPU.

    Attributes:
        sos (numpy.ndarray): The second-order sections representation of the filter.

    Parameters:
        low_hz (float): The lower cutoff frequency for the bandpass filter.
        high_hz (float): The higher cutoff frequency for the bandpass filter.
        fs (int): The sampling frequency of the input signal.

    References:
        - Butterworth filter: https://en.wikipedia.org/wiki/Butterworth_filter
        - scipy.signal.butter: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
        - scipy.signal.sosfilt: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfilt.html
    """

    def __init__(self, low_hz=100, high_hz=250, fs=1000):
        from scipy.signal import butter, sosfilt

        self.butter = butter
        self.sosfilt = sosfilt

        self.sos = self.mk_sos(low_hz, high_hz, fs)

    def __call__(self, raw_sig):
        """
        Apply the bandpass filter to the input signal.

        Parameters:
            raw_sig (numpy.ndarray): The raw input signal. The shape of the array should be (n_samples,) for a 1D signal or (n_channels, n_samples) for a multi-channel signal.

        Returns:
            numpy.ndarray: The filtered signal. The shape of the array will be the same as the input signal.

        Data Types:
            Input: numpy.ndarray (typically float32 or float64)
            Output: numpy.ndarray (same type as input)

        Data Shapes:
            Input: (n_samples,) or (n_channels, n_samples)
            Output: Same as input

        References:
            - scipy.signal.sosfilt: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfilt.html
        """
        filted = self.sosfilt(self.sos, raw_sig)
        return filted

    def mk_sos(self, low_hz, high_hz, fs, order=5):
        """
        Create the second-order sections representation of the Butterworth filter.

        Parameters:
            low_hz (float): The lower cutoff frequency for the bandpass filter.
            high_hz (float): The higher cutoff frequency for the bandpass filter.
            fs (int): The sampling frequency of the input signal.
            order (int): The order of the filter.

        Returns:
            numpy.ndarray: The second-order sections representation of the filter.

        Data Types:
            Return: numpy.ndarray (typically float64)

        Data Shapes:
            Return: (n_sections, 6) where n_sections is the number of second-order filter sections.

        References:
            - scipy.signal.butter: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
        """
        nyq = fs / 2.0
        sos = self.butter(
            order,
            [low_hz / nyq, high_hz / nyq],
            analog=False,
            btype="band",
            output="sos",
        )
        return sos


def wavelet_np(wave, samp_rate, f_min=100, f_max=None, plot=False, title=None):
    """
    Perform a continuous wavelet transform on a signal and optionally plot the scalogram.

    Parameters:
        wave (numpy.ndarray): The input signal. Shape should be (n_samples,).
        samp_rate (float): The sampling rate of the signal in Hz.
        f_min (float): The minimum frequency for the wavelet transform. Defaults to 100 Hz.
        f_max (float, optional): The maximum frequency for the wavelet transform. Defaults to half the sampling rate.
        plot (bool): If True, plot the scalogram. Defaults to False.
        title (str, optional): The title for the plot if plot is True.

    Returns:
        pandas.DataFrame: A DataFrame containing the wavelet transform scalogram with frequencies as the index.

    Data Types:
        Input:
            wave: numpy.ndarray (typically float32 or float64)
            samp_rate: float
            f_min: float
            f_max: float or None
            plot: bool
            title: str or None
        Output:
            pandas.DataFrame

    Data Shapes:
        Input:
            wave: (n_samples,)
        Output:
            DataFrame: (n_frequencies, n_samples)

    References:
        - Continuous wavelet transform: https://en.wikipedia.org/wiki/Continuous_wavelet_transform
        - scipy.signal.cwt: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.cwt.html
        - obspy.imaging.cm.obspy_sequential: https://docs.obspy.org/packages/autogen/obspy.imaging.cm.obspy_sequential.html
        - pandas.DataFrame: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
        - matplotlib.pyplot: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html

    Raises:
        ValueError: If the input signal is not a 1D numpy.ndarray.
    """

    dt = 1.0 / samp_rate
    npts = len(wave)
    t = np.linspace(0, dt * npts, npts)
    if f_min is None:
        f_min = 0.1
    if f_max is None:
        f_max = int(samp_rate / 2)
        scalogram = cwt(wave, dt, 8, f_min, f_max)

    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x, y = np.meshgrid(
            t,
            np.logspace(np.log10(f_min), np.log10(f_max), scalogram.shape[0]),
        )

        ax.pcolormesh(x, y, np.abs(scalogram), cmap=obspy_sequential)
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Frequency [Hz]")
        ax.set_yscale("log")
        ax.set_title(title)
        ax.set_ylim(f_min, f_max)
        fig.show()

    Hz = pd.Series(
        np.logspace(np.log10(f_min), np.log10(f_max), scalogram.shape[0])
    )
    df = pd.DataFrame(np.abs(scalogram))
    df["Hz"] = Hz
    df.set_index("Hz", inplace=True)

    return df


# from here, not important


class TimeKeeper:
    """
    A simple class to keep track of elapsed time.

    Methods:
        __call__(message=None): Print the elapsed time with an optional message.
        start(): Reset the start time to the current time.
    """

    def __init__(
        self,
    ):
        """
        Initialize the TimeKeeper with the current time as the start time.
        """

        self.start_time = time.time()

    def __call__(self, message=None):
        """
        Print the elapsed time since the start time with an optional message.

        Parameters:
            message (str, optional): An optional message to print before the elapsed time.
        """

        self.elapsed = time.time() - self.start_time
        print(message)
        print("elapsed time: {:.5f} [sec]".format(self.elapsed))

    def start(
        self,
    ):
        """
        Reset the start time to the current time.
        """

        self.start_time = time.time()


if __name__ == "__main__":
    # Parameters
    PASS_LOW_HZ = 40
    PASS_HIGH_HZ = 80
    T_sec = 50.0
    fs = 250
    freqs_hz = [30, 60, 100, 200, 1000]
    n_chs = 19
    bs = 64
    i_batch_show = 0
    i_ch_show = 0
    sig_orig = np.array(
        [
            mngs.dsp.prepare_demo_data(
                T_sec=T_sec, fs=fs, freqs_hz=freqs_hz, n_chs=n_chs
            )
            for _ in range(bs)
        ]
    )
    print("sig_orig_shape: {}".format(sig_orig.shape))
    tk = TimeKeeper()

    # Original
    title_orig = "Original, #{}, ch{} (Demo Freqs: {} Hz)".format(
        i_batch_show, i_ch_show, freqs_hz
    )
    wv_out_orig = wavelet_np(
        sig_orig[i_batch_show, i_ch_show],
        fs,
        f_min=1,
        plot=True,
        title=title_orig,
    )

    # CPU Bandpass Filtering
    bp_cpu = BandPasserCPUTorch(
        low_hz=PASS_LOW_HZ, high_hz=PASS_HIGH_HZ, fs=fs
    )
    filted_cpu = sig_orig.copy()
    ## calculation start ###
    tk.start()
    for i_batch in range(bs):
        for i_ch in range(n_chs):
            filted_cpu[i_batch, i_ch] = bp_cpu(filted_cpu[i_batch, i_ch])
            tk(message="CPU")
            ## calculation end ###
    title_filt_cpu = "[CPU] Bandpass Filted, #{}, ch{} (Freqs: (Low_lim, High_lim) = ({}, {}) Hz) (time: {:.5f} [sec])".format(
        i_batch_show, i_ch_show, PASS_LOW_HZ, PASS_HIGH_HZ, tk.elapsed
    )
    _wv_out_filted_cpu = wavelet_np(
        filted_cpu[i_batch_show, i_ch_show],
        fs,
        f_min=1,
        plot=True,
        title=title_filt_cpu,
    )

    # GPU Bandpass Filtering
    BandPassFilterGPUTorch = BandPassFilterTorch
    bp_gpu = BandPassFilterGPUTorch(
        low_hz=PASS_LOW_HZ, high_hz=PASS_HIGH_HZ, fs=fs
    ).cuda()
    # sig_torch = torch.tensor(sig_orig).unsqueeze(0).unsqueeze(0).cuda()
    sig_torch = torch.tensor(sig_orig).cuda()
    ## calculation start ###
    tk.start()
    filted_gpu = bp_gpu(sig_torch)
    tk(message="GPU")
    ## calculation end ###
    title_filt_gpu = "[GPU] Bandpass Filted, #{}, ch{} (Freqs: (Low_lim, High_lim) = ({}, {}) Hz) (time: {:.5f} [sec])".format(
        i_batch_show, i_ch_show, PASS_LOW_HZ, PASS_HIGH_HZ, tk.elapsed
    )
    _wv_out_filted_gpu = wavelet(
        filted_gpu[i_batch_show, i_ch_show].cpu(),
        fs,
        f_min=1,
        plot=True,
        title=title_filt_gpu,
    )


from scipy.signal import butter, sosfilt, sosfreqz


def bandpassfilter_np(data, lo_hz, hi_hz, fs, order=5):
    """
    Apply a Butterworth bandpass filter to a given data array.

    Parameters:
        data (ndarray): The input signal to be filtered.
        lo_hz (float): The lower cutoff frequency of the bandpass filter in Hz.
        hi_hz (float): The upper cutoff frequency of the bandpass filter in Hz.
        fs (float): The sampling rate of the signal in Hz.
        order (int): The order of the filter. Higher order means a sharper frequency cutoff,
                     but the filter might become unstable. Defaults to 5.

    Returns:
        ndarray: The filtered signal.
    """

    def _mk_butter_bandpass(order=5):
        """
        Create a Butterworth bandpass filter using second-order sections representation.

        Parameters:
            order (int): The order of the filter.

        Returns:
            ndarray: Second-order sections representation of the Butterworth bandpass filter.
        """

        nyq = 0.5 * fs
        low, high = lo_hz / nyq, hi_hz / nyq
        sos = butter(
            order, [low, high], analog=False, btype="band", output="sos"
        )
        return sos

    def _butter_bandpass_filter(data):
        """
        Apply a Butterworth bandpass filter to a given data array.

        Parameters:
            data (ndarray): The input signal to be filtered.

        Returns:
            ndarray: The filtered signal.
        """

        sos = _mk_butter_bandpass()
        y = sosfilt(sos, data)
        return y

    sos = _mk_butter_bandpass(order=order)
    y = _butter_bandpass_filter(data)

    return y

    # EOF
