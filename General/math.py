import numpy as np
from General.Constants import *
from typing import Union, Collection
from functools import lru_cache

def gcd_from_haste(haste: float):
    return max(GCD_CAP, GCD/haste)

def half_gcd_from_haste(haste: float):
    return max(HALF_GCD_CAP, HALF_GCD/haste)

def partially_linear_function(increments: Collection[Union[int, float]],
                              thresholds: Collection[Union[int, float]]):
    assert len(increments) == len(thresholds) + 1

    threshold_amounts = []
    prev_threshold = 0
    for th, curr_inc in zip(thresholds, increments):
        req_gain = th - prev_threshold
        amount = req_gain/curr_inc
        threshold_amounts.append(int(amount))
        prev_threshold = th
    threshold_amounts = np.cumsum(threshold_amounts)

    @lru_cache(maxsize=None)
    def wrapper(x: Union[float, int]):
        for i, th in enumerate(threshold_amounts):
            if x < th:
                return thresholds[i] - increments[i]*(th - x)

        return thresholds[-1] + increments[-1]*(x - th)

    return wrapper




