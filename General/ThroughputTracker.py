import numpy as np
import pandas as pd
from typing import Collection
from General.Ability import AbilityEvent
from Discipline.Disc import Discipline

class ThroughputTracker:

    def __init__(self, disc:Discipline):

        self.disc = disc
        #self.disc.cast = self.track_cast_results(self.disc.cast)
        self.data = pd.DataFrame(index=['Damage', 'Healing'], dtype=float)
        self.cast_abilities = pd.Series(dtype=str)


    def handle_ability_event(self, events: Collection[AbilityEvent], timestamp: float, ability_name: str):

        if not timestamp in self.data.columns:
            self.data.loc[:, timestamp] = (0, 0)
            self.cast_abilities[timestamp] = ability_name
        for event in events:
            self.data.loc[['Damage', 'Healing'], timestamp] += (event.dmg, event.heal)

        pass

    def cast(self, ability_name: str):
        cast_results, timestamp = self.disc.cast(ability_name=ability_name)
        self.handle_ability_event(cast_results, timestamp, ability_name)
        return cast_results, timestamp

    def track_cast_results(self, cast_func):

        def wrapper(*args, **kwargs):

            cast_results, timestamp = cast_func(*args, **kwargs)
            self.handle_ability_event(cast_results, timestamp, args[0])
            return cast_results, timestamp

        return wrapper