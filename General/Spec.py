from General.Stats import Stats, stat_to_percent
from typing import Union
from General.Constants import *

class Specialization:

    def __init__(self, stats: Stats = Stats()):
        self.stats = stats
        self.stat_increases = {
            'main': 1.05,
            'haste': 1.01,
            'crit': 1,
            'vers': 1.03,
            'mast': 1,
        }

    @staticmethod
    def globals_in_time_window(t_window: float, haste: Union[int, float],
                               from_start: bool = True) -> int:
        """
        Returns the amount of globals that can be fit into time frame t_window.
        :param t_window:    The time frame.
        :param haste:       Amount of haste. If int, will be treated as a raw stat.
                            If float, will be treated as the effective haste.
        :param from_start:  If True, the returned value will be the amount of globals
                            that can be started within that time frame. If False, the
                            amount of globals that can be finished within the time frame.
        :return: The amount of globals within the time frame.
        """
        assert t_window >= 0, f'Argument {t_window}, must be geq 0.'
        haste_effect = haste if isinstance(haste, float) else stat_to_percent(haste, "haste")
        return int(t_window*(1 +haste_effect)/GCD + int(from_start))

    def stat_to_percent(self, stat: str):
        return self.stats.stat_to_percent(stat)


