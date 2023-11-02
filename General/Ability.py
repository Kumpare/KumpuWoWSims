from General.Constants import *
import numpy as np
from General.ThroughputTypes import ThroughputType

class Ability:

    def __init__(self, name:str, throughput_type: ThroughputType=ThroughputType.NONE_TYPE, cast_time: float = 0., gcd: float = GCD,
                 cooldown: float = 0., cooldown_haste_scale: bool = False,
                 haste_effect: float = 1.,
                 charges: int = 1):
        self._cast_time = cast_time
        self._base_cast_time = cast_time
        self._base_gcd = gcd
        self._gcd = gcd
        self._base_cooldown = cooldown
        self._remaining_cooldown = 0.
        self._cooldown_haste_scale = cooldown_haste_scale
        self._haste_effect = haste_effect
        self._max_charges = charges
        self._charges = charges
        self.throughput_type = throughput_type
        self.name = name
        self.cast = self.base_cast

    def base_cast(self, cast_start_time: float):
        if self.remaining_cooldown > 0 and self._charges == 0:
            raise ValueError(f'Ability {self.name} is still on cooldown')
        self._remaining_cooldown = self.cooldown if self._charges == self._max_charges else self._remaining_cooldown
        self._charges -= 1
        to_return = self.ability_event(cast_start_time)
        return to_return

    @property
    def cast_time(self):
        return self._cast_time / self._haste_effect

    @property
    def gcd(self):
        return np.maximum(self._gcd, self._base_gcd/2)

    @property
    def cast_times(self):
        return self.cast_time, self.gcd

    @property
    def time_taken(self):
        return np.maximum(self.cast_time, self.gcd)

    @property
    def remaining_cooldown(self):
        return self._remaining_cooldown

    @property
    def cooldown(self):
        return self._base_cooldown / (1 + (self._haste_effect - 1) * int(self._cooldown_haste_scale))

    def progress_time(self, t: float):
        if self.remaining_cooldown <= 0:
            return

        self._remaining_cooldown -= t
        if self._remaining_cooldown < 0:
            self._charges += 1
            self._remaining_cooldown = self.cooldown + self.remaining_cooldown if self._charges < self._max_charges else 0

    def set_haste(self, haste_effect: float):
        cd_progress = self.remaining_cooldown / self.cooldown if self.cooldown > 0 else 0
        self._haste_effect = haste_effect
        self._remaining_cooldown = cd_progress * self.cooldown
        self._gcd = self._base_gcd / self._haste_effect
        self._cast_time = self._base_cast_time / self._haste_effect

    def ability_event(self, cast_start_time: float):
        NotImplementedError()

class Buff(Ability):

    def __init__(self, name:str, cast_time: float = 0., gcd: float = 0,
                 cooldown: float = 0., cooldown_haste_scale: bool = False,
                 haste_effect: float = 1., charges: int = 1, buff_duration: float = None,
                 max_stacks: int=1):
        super().__init__(name=name, cast_time=cast_time, gcd=gcd, cooldown=cooldown,
                         cooldown_haste_scale=cooldown_haste_scale, haste_effect=haste_effect,
                         charges=charges)
        self._buff_duration = buff_duration
        self._remaining_duration = 0
        self._stacks = 0
        self._max_stacks = max_stacks
        self.time_applied = None
        self.id = None

    def progress_time(self, t: float):
        super().progress_time(t)

        if self.buff_active:
            self._remaining_duration -= t
            if self._remaining_duration < 0:
                self._remaining_duration = 0
                self.time_applied = None
                self._stacks = 0

    def apply(self, time_applied: float, n_stacks: int = 1):
        self._on_apply()
        self.time_applied = time_applied
        self._remaining_duration = np.minimum(self._buff_duration*1.3, self._buff_duration + self._remaining_duration)
        self._stacks = min(self._stacks + n_stacks, self._max_stacks)

    @property
    def buff_active(self):
        return self._stacks > 0

    @property
    def duration(self):
        return self._buff_duration
    @property
    def remaining_duration(self):
        return self._remaining_duration

    def refresh_duration(self):
        self._remaining_duration = np.minimum(self._buff_duration + self._remaining_duration, self._buff_duration*1.3)

    def _on_apply(self):
        pass

    def expire(self):
        self._on_expire()
        self._remaining_duration = 0
        self._stacks = 0

    def _on_expire(self):
        pass

    def extend_duration(self, amount: float):
        if self.buff_active:
            self._remaining_duration += amount
        pass

class TickingBuff(Buff):

    def __init__(self, name:str, cast_time: float = 0., gcd: float = GCD,
                 cooldown: float = 0., cooldown_haste_scale: bool = False,
                 haste_effect: float = 1., charges: int = 1, buff_duration: float = None,
                 max_stacks: int=1, tick_rate: float= 1,
                 scales_from_haste: bool = True, sp_coef: float=0, throughput_type=ThroughputType.NONE_TYPE):

        super().__init__(name=name, cast_time=cast_time, gcd=gcd, cooldown=cooldown,
                         cooldown_haste_scale=cooldown_haste_scale, haste_effect=haste_effect,
                         charges=charges, buff_duration=buff_duration, max_stacks=max_stacks)

        self.throughput_type = throughput_type
        self._base_tick_rate = tick_rate
        self._scales_from_haste = scales_from_haste
        self._tick_rate = self._base_tick_rate/haste_effect if scales_from_haste else self._base_tick_rate
        self._time_from_last_tick = 0

        self._sp_coef = sp_coef
        n_ticks = buff_duration/tick_rate
        self._tick_sp_coef = self._sp_coef/n_ticks

    def progress_time(self, t: float):
        super().progress_time(t)

        if self.buff_active:
            n_ticks, time_from_last_tick = np.divmod(self._time_from_last_tick + t, self._tick_rate)
            self._time_from_last_tick = time_from_last_tick
            return n_ticks
        return 0

    def reduce_remaining_cd(self, t:float):
        self._remaining_cooldown = np.maximum(0, self._remaining_cooldown - t)

    @property
    def time_until_next_tick(self):
        return self._tick_rate - self._time_from_last_tick

    def set_haste(self, haste_effect: float):
        super().set_haste(haste_effect)
        if self._scales_from_haste:
            new_tick_rate = self._base_tick_rate/haste_effect
            tick_progress = self._time_from_last_tick/self._tick_rate
            self._tick_rate = new_tick_rate
            self._time_from_last_tick = tick_progress*self._tick_rate

    def apply(self, time_applied: float, n_stacks: int=1):
        super().apply(time_applied, n_stacks)
        self._time_from_last_tick = 0

    @property
    def tick_rate(self):
        return self._tick_rate


class AbilityEvent:

    def __init__(self, dmg: float, heal: float, timestamp: float, ability_name:str, throughput_type: ThroughputType):
        self.dmg = dmg
        self.heal = heal
        self.timestamp = timestamp
        self.throughput_type = throughput_type
        self.ability_name = ability_name