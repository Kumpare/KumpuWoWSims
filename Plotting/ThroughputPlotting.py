import matplotlib.pyplot as plt
from General.ThroughputTracker import ThroughputTracker
from typing import Union, Collection
import pandas as pd
import numpy as np


def plot_throughputs(throughputs: Collection[ThroughputTracker], metric_to_track: str = "Healing", labels: list = None):
    for throughput in throughputs:
        assert metric_to_track in throughput.data.index

    px = 1/plt.rcParams['figure.dpi']
    f, (ps_axis, c_axis) = plt.subplots(nrows=2, figsize=(1600*px, 960*px))

    ps_axis.set_ylabel(f'{metric_to_track} per second \n (in thousands)')
    c_axis.set_ylabel(f'{metric_to_track} done \n (in millions)')
    c_axis.set_xlabel(f'Time')
    #ps_axis.set_facecolor('grey')
    #c_axis.set_facecolor('grey')
    ps_axis.grid(True)
    c_axis.grid(True)
    radius = 2.5
    ps_axis.set_title(f'Hps calculated based on healing done \n over {radius*2:.1f} second period')

    for i, throughput in enumerate(throughputs):
        data = throughput.data.loc[metric_to_track, :]
        data = data.sort_values(key=lambda x: x.index)

        ps_data = smoothen_data(data, radius=radius) / 1e3
        c_data = data.cumsum() / 1e6

        lbl = labels[i] if labels is not None else str(i)
        p = ps_axis.plot(ps_data.index, ps_data)[0]
        p.set_label(lbl)

        c_axis.plot(c_data.index, c_data)
        pwr_casts = throughput.cast_abilities.loc[throughput.cast_abilities == 'pwr']
        eva_casts = throughput.cast_abilities.loc[throughput.cast_abilities == 'evangelism']

        col = p.get_color()
        c_max = c_data.max()
        ps_max = ps_data.max()
        pwr_handle = None
        eva_handle = None
        for t_stamp, _ in pwr_casts.items():
            pwr_handle = c_axis.scatter(t_stamp, c_max, c=col, marker='*', label='PW:R')
            ps_axis.scatter(t_stamp, ps_max, c=col, marker='*')
            ps_axis.plot([t_stamp, t_stamp], [0,ps_max], c=col, linestyle='--')
            c_axis.plot([t_stamp, t_stamp], [0,c_max], c=col, linestyle='--')

        for t_stamp, _ in eva_casts.items():
            eva_handle = c_axis.scatter(t_stamp, c_max, c=col, marker='v', label='Evangelism')
            ps_axis.scatter(t_stamp, ps_max, c=col, marker='v')
            ps_axis.plot([t_stamp, t_stamp], [0, ps_max], c=col, linestyle=':')
            c_axis.plot([t_stamp, t_stamp], [0, c_max], c=col, linestyle=':')

        handles = [hndl for hndl in [pwr_handle, eva_handle] if hndl is not None]
        ps_axis.legend(handles=handles, loc='upper left')

    plt.show()
    plt.clf()


def smoothen_data(data: pd.Series, ticks: float = 1, radius: float = 2.5) -> pd.Series:
    last_idx = (int(data.index.max() / ticks) + 1) * ticks

    idxs = np.arange(0, last_idx, ticks)

    to_return = pd.Series(index=idxs, dtype='float32')
    for idx in idxs:
        sub_data = data.loc[np.abs(data.index - idx) <= radius]
        mean = sub_data.sum()/(2*radius)
        to_return[idx] = mean
    return to_return
