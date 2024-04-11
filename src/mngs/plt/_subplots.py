#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-04-10 20:30:24 (ywatanabe)"

from collections import OrderedDict

import matplotlib.pyplot as plt
import mngs
import numpy as np
import pandas as pd


class SubplotsManager:
    """
    A manager class monitors data plotted using the ax methods from matplotlib.pyplot.
    This data can be converted into a CSV file formatted for SigmaPlot compatibility.
    Additionally, refer to the SigmaPlot macros available at mngs.gists (https://github.com/ywatanabe1989/mngs/tree/main/src/mngs/gists).

    Currently, available methods are as follows:
        ax.plot, ax.scatter, ax.boxplot, and ax.bar

    Example:
        import matplotlib
        import mngs

        matplotlib.use("Agg")  # "TkAgg"

        fig, ax = subplots()
        ax.plot([1, 2, 3], [4, 5, 6], id="plot1")
        ax.plot([4, 5, 6], [1, 2, 3], id="plot2")
        mngs.io.save(fig, "/tmp/subplots_demo/plots.png")

        # Behaves like native matplotlib.pyplot.subplots without tracking
        fig, ax = subplots(track=False)
        ax.plot([1, 2, 3], [4, 5, 6], id="plot3")
        ax.plot([4, 5, 6], [1, 2, 3], id="plot4")
        mngs.io.save(fig, "/tmp/subplots_demo/plots.png")

        fig, ax = subplots()
        ax.scatter([1, 2, 3], [4, 5, 6], id="scatter1")
        ax.scatter([4, 5, 6], [1, 2, 3], id="scatter2")
        mngs.io.save(fig, "/tmp/subplots_demo/scatters.png")

        fig, ax = subplots()
        ax.boxplot([1, 2, 3], id="boxplot1")
        mngs.io.save(fig, "/tmp/subplots_demo/boxplot1.png")

        fig, ax = subplots()
        ax.bar(["A", "B", "C"], [4, 5, 6], id="bar1")
        mngs.io.save(fig, "/tmp/subplots_demo/bar1.png")

        print(ax.to_sigma())
        #    plot1_plot_x  plot1_plot_y  plot2_plot_x  ...  boxplot1_boxplot_x  bar1_bar_x  bar1_bar_y
        # 0           1.0           4.0           4.0  ...                 1.0           A         4.0
        # 1           2.0           5.0           5.0  ...                 2.0           B         5.0
        # 2           3.0           6.0           6.0  ...                 3.0           C         6.0

        print(ax.to_sigma().keys())  # plot3 and plot 4 are not tracked
        # [3 rows x 11 columns]
        # Index(['plot1_plot_x', 'plot1_plot_y', 'plot2_plot_x', 'plot2_plot_y',
        #        'scatter1_scatter_x', 'scatter1_scatter_y', 'scatter2_scatter_x',
        #        'scatter2_scatter_y', 'boxplot1_boxplot_x', 'bar1_bar_x', 'bar1_bar_y'],
        #       dtype='object')

        # If a path is passed, the SigmaPlot-friendly dataframe is saved as a csv file.
        ax.to_sigma("./tmp/subplots_demo/for_sigmaplot.csv")
        # Saved to: ./tmp/subplots_demo/for_sigmaplot.csv
    """

    def __init__(
        self,
    ):
        """Initialize the SubplotsManager with an empty plot history."""
        self._plot_history = OrderedDict()

    def __call__(self, *args, track=True, **kwargs):
        """
        Create subplots and wrap the axes with AxisDataCollector.

        Returns:
            tuple: A tuple containing the figure and wrapped axes
            in the same manner with matplotlib.pyplot.subplots.
        """
        fig, axes = plt.subplots(*args, **kwargs)
        # fig.tight_layout(rect=[0, 0.03, 1, 0.95])

        axes = np.atleast_1d(axes)
        axes_orig_shape = axes.shape

        if axes_orig_shape == (1,):
            ax_wrapped = AxisDataCollector(axes[0], self._plot_history, track)
            return fig, ax_wrapped

        else:

            axes = axes.ravel()
            axes_wrapped = [
                AxisDataCollector(ax, self._plot_history, track) for ax in axes
            ]
            axes = (
                np.array(axes_wrapped).reshape(axes_orig_shape)
                if axes_orig_shape
                else axes_wrapped[0]
            )

            return fig, axes
        # # Wraps the axes
        # for ax in axes:
        #     ax = AxisDataCollector(ax, self._plot_history, track)

        # axes = np.array(axes).reshape(axes_orig_shape)

        # return fig, axes if axes_orig_shape else axes[0]

        # ax = np.atleast_1d(ax)
        # ax_wrapped = [
        #     AxisDataCollector(a, self._plot_history, track) for a in ax
        # ]
        # return fig, ax_wrapped if len(ax_wrapped) > 1 else ax_wrapped[0]
        # return fig, axes if len(ax_wrapped) > 1 else ax_wrapped[0]

    @property
    def history(self):
        """
        Get the sorted plot history.

        Returns:
            dict: The sorted plot history.
        """
        return {k: self._plot_history[k] for k in self._plot_history}

    def reset_history(self):
        """Reset the plot history to an empty state."""
        self._plot_history = OrderedDict()

    @property
    def to_sigma(self):
        """
        Convert the plot history data to a SigmaPlot-compatible format DataFrame.

        Returns:
            DataFrame: The plot history in SigmaPlot format.
        """
        data_frames = [to_sigmaplot_format(v) for v in self.history.values()]
        combined_data = pd.concat(data_frames)
        return combined_data.apply(
            lambda col: col.dropna().reset_index(drop=True)
        )


class AxisDataCollector:
    """
    A wrapper class for a Matplotlib axis that collects plotting data.
    """

    def __init__(self, axis, history, track):
        """
        Initialize the AxisDataCollector with a given axis and history reference.
        """
        self.axis = axis
        self._history = history
        self.track = track

    def __getattr__(self, attr):
        """
        Wrap the axis attribute access to collect plot calls or return the attribute directly.
        """
        original_attr = getattr(self.axis, attr)

        if callable(original_attr):

            def wrapper(
                *args, id=None, track=True, n_xticks=4, n_yticks=4, **kwargs
            ):
                result = original_attr(*args, **kwargs)

                # Apply set_n_ticks after the plotting method is called
                if attr in ["plot", "scatter", "bar", "boxplot"]:
                    self.axis = mngs.plt.ax.set_n_ticks(
                        self.axis, n_xticks=n_xticks, n_yticks=n_yticks
                    )

                # Only store the history if tracking is enabled and an ID is provided
                if self.track and (id is not None):
                    self._history[id] = (id, attr, args, kwargs)
                return result

            return wrapper
        else:
            # Return the attribute directly if it's not callable
            return original_attr

    @property
    def history(self):
        """
        Get the sorted history for this axis.

        Returns:
            dict: The sorted history for this axis.
        """
        return {k: self._history[k] for k in self._history}

    def reset_history(self):
        """Reset the history for this axis."""
        self._history = {}

    def to_sigma(self, lpath=None):
        """
        Convert the axis history to a sigma format DataFrame.

        Returns:
            DataFrame: The axis history in sigma format.
        """
        try:
            data_frames = [
                to_sigmaplot_format(v) for v in self.history.values()
            ]
            combined_data = pd.concat(data_frames)
            combined_data = combined_data.apply(
                lambda col: col.dropna().reset_index(drop=True)
            )

        except Exception as e:
            print(e)
            combined_data = pd.DataFrame()

        if lpath is not None:
            mngs.io.save(combined_data, lpath)

        return combined_data

    def imshow2d(
        self,
        arr_2d,
        id=None,
        track=True,
        cbar=True,
        cbar_label=None,
        cbar_shrink=0.8,
        cmap="viridis",
        vmin=None,
        vmax=None,
    ):
        """
        Imshows an two-dimensional array with theese two conditions:
        1) The first dimension represents the x dim, from left to right.
        2) The second dimension represents the y dim, from bottom to top
        """

        assert arr_2d.ndim == 2

        # Cals the original ax.imshow() method on the transposed array
        im = self.axis.imshow(arr_2d.T, cmap=cmap, vmin=vmin, vmax=vmax)

        # Creates a colorbar
        fig = self.axis.get_figure()

        if cbar:
            _cbar = fig.colorbar(im, ax=self.axis, shrink=cbar_shrink)
            if cbar_label:
                _cbar.set_label(cbar_label)

        # Invert y-axis to match typical image orientation
        self.axis.invert_yaxis()

        # Store the history if tracking is enabled and an ID is provided
        if track and id is not None:
            self._history[id] = (id, "imshow2d", arr_2d, None)

        return fig  # Return the figure object


def to_sigmaplot_format(record):
    """
    Convert a single plot record to a sigma format DataFrame.

    Arguments:
        record (tuple): A tuple containing the plot id, method, arguments, and keyword arguments.

    Returns:
        DataFrame: The plot data in sigma format.
    """

    id, method, args, kwargs = record
    if method in ["plot", "scatter"]:
        x, y = args
        df = pd.DataFrame({f"{id}_{method}_x": x, f"{id}_{method}_y": y})
    elif method == "bar":
        x, y = args
        df = pd.DataFrame({f"{id}_{method}_x": x, f"{id}_{method}_y": y})
    elif method == "boxplot":
        x = args[0]
        df = pd.DataFrame({f"{id}_{method}_x": x})
    return df


subplots = SubplotsManager()


if __name__ == "__main__":
    import matplotlib
    import mngs

    matplotlib.use("TkAgg")  # "TkAgg"

    fig, ax = subplots()
    ax.plot([1, 2, 3], [4, 5, 6], id="plot1")
    ax.plot([4, 5, 6], [1, 2, 3], id="plot2")
    mngs.io.save(fig, "/tmp/subplots_demo/plots.png")

    # Behaves like native matplotlib.pyplot.subplots without tracking
    fig, ax = subplots(track=False)
    ax.plot([1, 2, 3], [4, 5, 6], id="plot3")
    ax.plot([4, 5, 6], [1, 2, 3], id="plot4")
    mngs.io.save(fig, "/tmp/subplots_demo/plots.png")

    fig, ax = subplots()
    ax.scatter([1, 2, 3], [4, 5, 6], id="scatter1")
    ax.scatter([4, 5, 6], [1, 2, 3], id="scatter2")
    mngs.io.save(fig, "/tmp/subplots_demo/scatters.png")

    fig, ax = subplots()
    ax.boxplot([1, 2, 3], id="boxplot1")
    mngs.io.save(fig, "/tmp/subplots_demo/boxplot1.png")

    fig, ax = subplots()
    ax.bar(["A", "B", "C"], [4, 5, 6], id="bar1")
    mngs.io.save(fig, "/tmp/subplots_demo/bar1.png")

    print(ax.to_sigma())
    #    plot1_plot_x  plot1_plot_y  plot2_plot_x  ...  boxplot1_boxplot_x  bar1_bar_x  bar1_bar_y
    # 0           1.0           4.0           4.0  ...                 1.0           A         4.0
    # 1           2.0           5.0           5.0  ...                 2.0           B         5.0
    # 2           3.0           6.0           6.0  ...                 3.0           C         6.0

    print(ax.to_sigma().keys())  # plot3 and plot 4 are not tracked
    # [3 rows x 11 columns]
    # Index(['plot1_plot_x', 'plot1_plot_y', 'plot2_plot_x', 'plot2_plot_y',
    #        'scatter1_scatter_x', 'scatter1_scatter_y', 'scatter2_scatter_x',
    #        'scatter2_scatter_y', 'boxplot1_boxplot_x', 'bar1_bar_x', 'bar1_bar_y'],
    #       dtype='object')

    # If a path is passed, the sigmaplot-friendly dataframe is saved as a csv file.
    ax.to_sigma("./tmp/subplots_demo/for_sigmaplot.csv")
    # Saved to: ./tmp/subplots_demo/for_sigmaplot.csv

# EOF

"""
/home/ywatanabe/proj/entrance/mngs/plt/_subplots.py
"""
