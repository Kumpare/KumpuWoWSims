from General.Ability import Buff, TickingBuff
from General.Spec import Specialization
import pandas as pd
from typing import Union
import numpy as np


class BuffManager():

    def __init__(self, time: float=0):

        self._buff_name_to_id = dict[str, int]()
        self._buffs = dict[int, Buff]()
        self._buff_df = pd.DataFrame(index=['Next tick', 'Expiration time', 'Active'], dtype='float32')
        self._next_buff_id = 0
        self._time = time

    @property
    def buffs(self):
        return self._buffs

    def get_buff(self, buff_id: Union[int, str]):
        if isinstance(buff_id, int):
            return self._buffs[buff_id]
        return self._buffs[self._buff_name_to_id[buff_id]]

    def apply_buff(self, buff: Buff, time_of_application: float):
        if buff.name in self._buff_name_to_id:
            buff_id = self._buff_name_to_id[buff.name]
            buff.apply(time_of_application)
            self._buff_df.at[buff_id, 'Expiration time'] = time_of_application + buff.remaining_duration

        self._buff_name_to_id[buff.name] = self._next_buff_id
        self._buffs[self._next_buff_id] = buff
        next_tick = buff._tick_rate if isinstance(buff, TickingBuff) else np.nan
        self._buff_df[self._next_buff_id] = (next_tick, time_of_application + buff.duration, 1)
        buff.apply(time_of_application)
        self._next_buff_id += 1

    def extend_buff(self, buff: Union[int, str, Buff], t_amount: float):

        buff_id = self._get_id(buff)

        buff = self._buffs[buff_id]

        buff.extend_duration(t_amount)
        self._buff_df.at[buff_id, 'Expiration time'] += t_amount

        return

    def _get_id(self, buff: Union[str, Buff]):

        if isinstance(buff, int):
            return buff

        buff_id = None

        if isinstance(buff, Buff):
            buff_id = self._buff_name_to_id[buff.name]

        if isinstance(buff, str):
            buff_id = self._buff_name_to_id[buff]

        return buff_id

    def refresh_buff(self, buff: Union[int, str, Buff], time_of_application: float):

        buff_id = self._get_id(buff)
        buff = self._buffs[buff_id]

        buff.refresh_duration()
        self._buff_df.at[buff_id, 'Expiration time'] = time_of_application + buff.remaining_duration

    def consume_buff(self, buff: Union[int, str, Buff]):

        buff_id = self._get_id(buff)
        buff = self._buffs[buff_id]

        buff.expire()
        self._buff_df.at[buff_id, 'Active'] = -1
        return

    def progress_time(self, t_delta: float):

        for buff_id, buff in self._buffs.items():
            buff.progress_time(t_delta)
            self._buff_df.at[buff_id, 'Active'] = 2*int(buff.buff_active) - 1
            if isinstance(buff, TickingBuff):
                self._buff_df.at[buff_id, 'Next tick'] = buff.time_until_next_tick
        pass

    def get_time_until_next_event(self):

        active_mask = self._buff_df['Active'] > 0
        ticks = self._buff_df.loc['Next tick'].loc[self._buff_df['Next tick'].notna].loc[active_mask]
        expirations = self._buff_df['Expiration time'].loc[active_mask]

        min_tick = self._time + ticks.min() if ticks.size > 0 else np.inf
        min_expiration = expirations.min() if expirations.size > 0 else np.inf

        return np.minimum(min_tick, min_expiration)




