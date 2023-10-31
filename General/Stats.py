from dataclasses import dataclass
from typing import Union, Type
from General.Constants import *
from General.util import *
import General.math as wowmath


class Stats:

    def __init__(self, main: int = 1, crit: int = 0, haste: int = 0,
                 mast: int = 0, vers: int = 0):
        self.main = main
        self.crit = crit
        self.haste = haste
        self.mast = mast
        self.vers = vers

        self._initialize_conversion_functions()

    @assert_not_None(['stat'])
    @assert_in_collection([SECONDARY_STATS], ['stat'])
    def stat_to_percent(self, stat: str) -> Union[float, NotImplementedError]:
        stat_amount = getattr(self, stat.lower())
        return self._stat_to_percent[stat](stat_amount)

    @assert_in_collection([SECONDARY_STATS], ['stat'])
    def __getitem__(self, stat: str):
        return getattr(self, stat)

    def _initialize_conversion_functions(self):
        to_return = {}
        for stat_name, initial_inc in STAT_CONVERSIONS.items():
            if initial_inc:
                increments = [initial_inc * i for i in STAT_DR_PENALTIES]
                to_return[stat_name] = wowmath.partially_linear_function(increments=increments, thresholds=STAT_DR_BREAKPOINTS)
            else:
                to_return[stat_name] = NotImplementedError
        self._stat_to_percent = to_return
        pass

def stat_to_percent(amount: Union[Stats, int], stat: str) -> float:
    if not isinstance(amount, Stats):
        val = amount
        amount = Stats()
        amount.__setattr__(stat.lower(), val)

    return amount.stat_to_percent(stat)


if __name__ == "__main__":
    print(stat_to_percent(180, 'crit'))
    stats1 = Stats(haste=30)
    print(stats1.stat_to_percent('haste'))
