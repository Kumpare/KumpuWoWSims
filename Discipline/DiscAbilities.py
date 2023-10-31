from __future__ import annotations
from General.Ability import Ability, AbilityEvent, Buff, TickingBuff
from General.Constants import *
from General.ThroughputTypes import ThroughputType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Discipline.Disc import Discipline


class DiscAbility(Ability):

    def __init__(self, name: str, cast_time: float = 0, gcd: float = GCD, cooldown: float = 0,
                 cooldown_haste_scale: bool = False, haste_effect: float = 1., charges: int = 1,
                 heal_sp_coef: float = 0., dmg_sp_coef: float = 0., procs_atonement: bool = False,
                 n_atonements_applied: int = 0, atonement_duration: float = 15., throughput_type: ThroughputType = ThroughputType.NONE_TYPE):
        super().__init__(name=name, cast_time=cast_time, gcd=gcd, cooldown=cooldown,
                         cooldown_haste_scale=cooldown_haste_scale, haste_effect=haste_effect, charges=charges, throughput_type=throughput_type
                         )
        self.heal_sp_coef = heal_sp_coef
        self.dmg_sp_coef = dmg_sp_coef
        self.procs_atonement = procs_atonement
        self.n_atonements_applied = n_atonements_applied
        self.atonement_duration = atonement_duration
        assert procs_atonement == (dmg_sp_coef > 0)

    def ability_event(self, cast_start_time: float):
        to_return = DiscAbilityEvent(dmg=self.dmg_sp_coef, heal=self.heal_sp_coef, timestamp=cast_start_time + self.cast_time,
                                     ability_name=self.name,
                                     procs_atonement=self.procs_atonement, throughput_type=self.throughput_type)
        return to_return


class DiscBuff(Buff):

    def __init__(self, name: str, disc: Discipline, cast_time: float = 0., gcd: float = GCD,
                 cooldown: float = 0., cooldown_haste_scale: bool = False,
                 haste_effect: float = 1., charges: int = 1, buff_duration: float = None,
                 max_stacks: int = 1):
        super().__init__(name=name, cast_time=cast_time, gcd=gcd, cooldown=cooldown,
                         cooldown_haste_scale=cooldown_haste_scale, haste_effect=haste_effect,
                         charges=charges, buff_duration=buff_duration, max_stacks=max_stacks)
        self.disc = disc


class DiscTickingBuff(TickingBuff):

    def __init__(self, name: str, cast_time: float = 0., gcd: float = GCD,
                 cooldown: float = 0., cooldown_haste_scale: bool = False,
                 haste_effect: float = 1., charges: int = 1, buff_duration: float = None,
                 max_stacks: int = 1, tick_rate: float = 1, scales_from_haste: bool = True, sp_coef: float = 0,
                 heal_sp_coef: float = None, dmg_sp_coef: float = None, procs_atonement: bool = False):
        TickingBuff.__init__(self, name=name, cast_time=cast_time, gcd=gcd, cooldown=cooldown,
                             cooldown_haste_scale=cooldown_haste_scale, haste_effect=haste_effect,
                             charges=charges, buff_duration=buff_duration, max_stacks=max_stacks,
                             tick_rate=tick_rate, scales_from_haste=scales_from_haste,
                             sp_coef=sp_coef)

        self.heal_sp_coef = heal_sp_coef if heal_sp_coef is not None else sp_coef
        self.dmg_sp_coef = dmg_sp_coef if dmg_sp_coef is not None else sp_coef
        self.procs_atonement = procs_atonement
        assert procs_atonement == (self.dmg_sp_coef > 0)

    def ability_event(self, cast_start_time: float):
        to_return = DiscAbilityEvent(dmg=self._tick_sp_coef, heal=0, timestamp=cast_start_time,
                                     ability_name=self.name, procs_atonement=self.procs_atonement,
                                     throughput_type=self.throughput_type)
        return to_return


class DiscAbilityEvent(AbilityEvent):

    def __init__(self, dmg: float, heal: float, timestamp: float, ability_name:str, throughput_type: ThroughputType, procs_atonement: bool = True):
        super().__init__(dmg=dmg, heal=heal, timestamp=timestamp, ability_name=ability_name, throughput_type=throughput_type)
        self.procs_atonement = procs_atonement


class SWD_Execute(DiscAbility):

    def __init__(self):
        super().__init__('swd_execute', dmg_sp_coef=1, cooldown=12, charges=2, procs_atonement=True)

    def base_cast(self, cast_start_time: float):
        if self.remaining_cooldown > 0 and self._charges == 0:
            raise ValueError(f'Ability {self.name} is still on cooldown')

        self._charges -= 1
        self._remaining_cooldown = self.cooldown if self._charges == 0 else self._remaining_cooldown
        to_return = self.ability_event(cast_start_time)
        return to_return

    def progress_time(self, t: float):
        if self.remaining_cooldown <= 0:
            return

        self._remaining_cooldown -= t
        if self._remaining_cooldown < 0:
            self._charges = self._max_charges
            self._remaining_cooldown = 0

class Penance(DiscAbility):

    def __init__(self, haste_effect: float=1., dmg_sp_coef: float = 0, heal_sp_coef: float = 0, procs_atonement: bool=False):
        super().__init__(name=f"penance{'_heal' if heal_sp_coef > 0 else ''}", cast_time=0, gcd=2, cooldown=9, cooldown_haste_scale=False,
                         haste_effect=haste_effect, dmg_sp_coef=dmg_sp_coef, heal_sp_coef=heal_sp_coef, procs_atonement=procs_atonement,
                         throughput_type=ThroughputType.LIGHT)
        self.n_bolts = 3

    def ability_event(self, cast_start_time: float):
        to_return = DiscAbilityEvent(dmg=self.dmg_sp_coef*self.n_bolts, heal=self.heal_sp_coef*self.n_bolts, timestamp=cast_start_time + self.cast_time,
                                     ability_name=self.name, procs_atonement=self.procs_atonement, throughput_type=self.throughput_type)
        return to_return
