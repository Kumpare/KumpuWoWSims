import numpy as np
import pandas as pd
from typing import Collection
from General.Ability import AbilityEvent
from Discipline.Disc import Discipline

class ThroughputTracker:

    def __init__(self, disc:Discipline):

        self.disc = disc
        self.disc.cast = self.track_cast_results(self.disc.cast)
        self.data = pd.DataFrame(index=['Damage', 'Healing'])


    def handle_ability_event(self, events: Collection[AbilityEvent]):

        for event in events:
            try:
                self.data[event.timestamp] += (event.dmg, event.heal)
            except KeyError:
                self.data[event.timestamp] = (event.dmg, event.heal)

        pass

    def cast(self, ability_name: str):
        cast_results, timestamp = self.disc.cast(ability_name=ability_name)
        # self.handle_ability_event(cast_results)
        return cast_results, timestamp

    def track_cast_results(self, cast_func):

        def wrapper(*args, **kwargs):

            cast_results, timestamp = cast_func(*args, **kwargs)
            self.handle_ability_event(cast_results)
            return cast_results, timestamp

        return wrapper