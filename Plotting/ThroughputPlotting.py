import matplotlib.pyplot as plt
from General.ThroughputTracker import ThroughputTracker
from typing import Union, Collection
import pandas as pd
import numpy as np


def plot_throughputs(throughputs: Collection[ThroughputTracker], metric_to_track: str = "Healing", labels: list = None):
    for throughput in throughputs:
        assert metric_to_track in throughput.data.index

    f, (ps_axis, c_axis) = plt.subplots(nrows=2)

    ps_axis.set_ylabel(f'{metric_to_track} per second \n (in thousands)')
    c_axis.set_ylabel(f'{metric_to_track} done \n (in millions)')
    c_axis.set_xlabel(f'Time')
    ps_axis.set_facecolor('grey')
    c_axis.set_facecolor('grey')
    ps_axis.grid(True)
    c_axis.grid(True)

    for i, throughput in enumerate(throughputs):
        data = throughput.data.loc[metric_to_track, :]
        data = data.sort_values(key=lambda x: x.index)
        print(data.index)

        ps_data = smoothen_data(data) / 1e3
        c_data = data.cumsum() / 1e6

        lbl = labels[i] if labels is not None else str(i)
        p = ps_axis.plot(ps_data.index, ps_data)[0]
        p.set_label(lbl)

        c_axis.fill_between(c_data.index, c_data)

    if labels is not None:
        ps_axis.legend(loc='upper left')
    plt.show()
    plt.clf()


def smoothen_data(data: pd.Series, ticks: float = 1, radius: float = 1) -> pd.Series:
    last_idx = (int(data.index.max() / ticks) + 1) * ticks

    idxs = np.arange(0, last_idx, ticks)

    to_return = pd.Series(index=idxs)
    for idx in idxs:
        sub_data = data.loc[np.abs(data.index - idx) <= radius]
        mean = sub_data.mean()
        to_return[idx] = mean
    return to_return
