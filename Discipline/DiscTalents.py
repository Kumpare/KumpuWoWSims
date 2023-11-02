from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Discipline.Disc import Discipline
from Discipline.DiscAbilities import DiscBuff, DiscAbility, DiscTickingBuff
from General.Constants import *
from typing import Union
from General.ThroughputTypes import ThroughputType


class DiscTalentWrapper(DiscBuff):

    def __init__(self, name:str, disc: Discipline, n_points: int, ability: Union[DiscAbility, DiscBuff, DiscTickingBuff] = None,
                 cast_time: float = 0., gcd: float = 0,
                 cooldown: float = 0., cooldown_haste_scale: bool = False,
                 haste_effect: float = 1., charges: int = 1, buff_duration: float = None,
                 max_stacks: int=1):
        super().__init__(name=name, disc=disc, cast_time=cast_time, gcd=gcd, cooldown=cooldown,
                         cooldown_haste_scale=cooldown_haste_scale, haste_effect=haste_effect,
                         charges=charges, buff_duration=buff_duration, max_stacks=max_stacks)
        self.ability = ability
        self.n_points = n_points
        if ability is not None:
            self.ability.cast = self._decorator(self.ability.cast)

    def _decorator(self, ability_cast):

        def wrapper(*args, **kwargs):
            self.before_cast()
            ability_event = ability_cast(*args, **kwargs)
            self.after_cast()
            return ability_event

        return wrapper

    def _decorator_after(self, ability_cast):

        def wrapper(*args, **kwargs):
            ability_events = ability_cast(*args, **kwargs)
            self.after_cast()
            return ability_events

        return wrapper

    def _decorator_before(self, ability_cast):

        def wrapper(*args, **kwargs):
            self.before_cast()
            ability_events = ability_cast(*args, **kwargs)
            return ability_events

        return wrapper

    def before_cast(self):
        NotImplementedError()

    def after_cast(self):
        NotImplementedError()

    def _consume_self(self, ability_cast):

        def wrapper(*args, **kwargs):
            ability_event = ability_cast(*args, **kwargs)
            if self.buff_active:
                self.disc.consume_buff(buff_id=self.id, buff=self)
            return ability_event

        return wrapper

class BorrowedTime(DiscTalentWrapper):

    def __init__(self, disc: Discipline, ability: DiscAbility, n_points: int):
        super().__init__(name="BT", disc=disc, ability=ability, n_points=n_points,
                         cast_time=0, gcd=0, max_stacks=1, buff_duration=4)
        self.haste_effect = 1 + self.n_points*0.04

    def before_cast(self):
        self.disc.apply_buff(self)

    def after_cast(self):
        pass

    def _on_apply(self):
        self.disc.increase_haste(self.haste_effect)

    def _on_expire(self):
        self.disc.increase_haste(1./self.haste_effect)

class TrainOfThought(DiscTalentWrapper):

    def __init__(self, disc: Discipline, ability: DiscAbility, n_points: int=1):
        super().__init__(name="ToT", disc=disc, ability=ability, n_points=n_points,
                         cast_time=0, gcd=0)
        self._cdr_reduction = 0.5
        self._penance = disc.abilities["penance"]

    def before_cast(self):
        pass

    def after_cast(self):
        self._penance.progress_time(self._cdr_reduction)

class TrainOfThought_PWS(DiscTalentWrapper):

    def __init__(self, disc: Discipline, n_points: int=1):
        super().__init__(name="ToT_pws", disc=disc, n_points=n_points,
                         cast_time=0, gcd=0)

        self._cdr_reduction = 1
        self._pws = disc.abilities["pws"]

        self._renew = disc.abilities["renew"]
        self._flash_heal = disc.abilities["flash_heal"]

        self._renew.cast = self._decorator(self._renew.cast)
        self._flash_heal.cast = self._decorator(self._flash_heal.cast)


    def before_cast(self):
        pass

    def after_cast(self):
        self._pws.progress_time(self._cdr_reduction)

class Schism(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__(name="Schism", disc=disc, ability=disc.abilities["mind_blast"], n_points=1, gcd=0, buff_duration=9)

        self._buff_effect = 1.1
        self._reverse_buff_effect = 1/self._buff_effect

    def before_cast(self):
        pass

    def after_cast(self):
        self.disc.apply_buff(self)
        pass

    def _on_apply(self):
        self.disc.throughput_type_dmg_effects[ThroughputType.NONE_TYPE] *= self._buff_effect

    def _on_expire(self):
        self.disc.throughput_type_effects[ThroughputType.NONE_TYPE] *= self._reverse_buff_effect

class DarkIndulgence(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__(name="DI", disc=disc, n_points=1, ability=disc.abilities["mind_blast"], gcd=0,
                         buff_duration=30)

        self._penance = self.disc.abilities["penance"]
        self._penance_heal = self.disc.abilities['penance_heal']
        self._penance.cast = self._consume_self(self._penance.cast)
        self._penance_heal.cast = self._consume_self(self._penance_heal.cast)
        self._buff_effect = 1.5
        self._reverse_buff_effect = 1/1.5

    def before_cast(self):
        pass

    def after_cast(self):
        self.id = self.disc.apply_buff(self)
        pass

    def _on_apply(self):
        self._penance.dmg_sp_coef *= self._buff_effect
        self._penance.heal_sp_coef *= self._buff_effect

    def _on_expire(self):
        self._penance.dmg_sp_coef *= self._reverse_buff_effect
        self._penance.heal_sp_coef *= self._reverse_buff_effect

class PainfulPunishment(DiscTalentWrapper):

    def __init__(self, disc:Discipline):
        super().__init__(name='PP', disc=disc, n_points=1, ability=disc.abilities['penance'], gcd=0)

        self._dot_extension_per_bolt = 1.5
        self._ptw = self.disc.abilities['ptw']

    def before_cast(self):
        if self._ptw.buff_active:
            self.disc.extend_buff(self._ptw, self.ability.n_bolts*self._dot_extension_per_bolt)
        pass

    def after_cast(self):
        pass

class ShadowCovenant(DiscTalentWrapper):

    def __init__(self, disc:Discipline):
        bender_chosen = disc.talents['Bender'] > 0
        ability = disc.abilities['bender'] if bender_chosen else disc.abilities['sfiend']
        super().__init__(name='SC', disc=disc, n_points=1, ability=ability, gcd=0, buff_duration= 12 + 3*int(not bender_chosen))

        self.throughput_type = ThroughputType.SHADOW
        self._buff_effect = 1.20 + 0.15*int(not bender_chosen)
        self._reverse_buff_effect = 1./self._buff_effect
        self._penance = self.disc.abilities['penance']
        self._mind_blast = self.disc.abilities['mind_blast']
        self._swd = self.disc.abilities['swd']
        self._swd_execute = self.disc.abilities['swd_execute']
        self._halo = self.disc.abilities['halo']


        #todo: ds

    def before_cast(self):
        self.id = self.disc.apply_buff(self)

    def after_cast(self):
        pass

    def _on_apply(self):
        self.disc.throughput_type_heal_effects[self.throughput_type] *= self._buff_effect
        self.disc.throughput_type_dmg_effects[self.throughput_type] *= self._buff_effect
        self._penance.throughput_type = self.throughput_type
        self._halo.throughput_type = self.throughput_type
        #todo ds

    def _on_expire(self):
        self.disc.throughput_type_heal_effects[self.throughput_type] *= self._reverse_buff_effect
        self.disc.throughput_type_dmg_effects[self.throughput_type] *= self._reverse_buff_effect
        self._penance.throughput_type = ThroughputType.LIGHT
        self._halo.throughput_type = ThroughputType.LIGHT

class VoidSummoner(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__("VS", disc=disc, n_points=1)

        self._cdr_amount = 2 + 2*int(self.disc.talents["Bender"] == 0)

        self._pet = disc.abilities['bender'] if self._cdr_amount == 2 else disc.abilities['sfiend']

        self._smite = disc.abilities["smite"]
        self._smite_4p = disc.abilities["smite_4p"]
        self._penance = disc.abilities["penance"]
        self._mind_blast = disc.abilities["mind_blast"]

        for ability in [self._smite, self._smite_4p, self._penance, self._mind_blast]:
            ability.cast = self._decorator(ability_cast=ability.cast)

    def before_cast(self):
        self._pet.reduce_remaining_cd(self._cdr_amount)
        pass

    def after_cast(self):
        pass

class Amirdrassil_2p(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__(name='Amirdrassil_2p', disc=disc, n_points=1)
        self._extend_amount = 2
        self._smite = disc.abilities['smite']
        self._smite_4p = disc.abilities['smite_4p']

        self._smite.cast = self._decorator_after(self._smite.cast)
        self._smite_4p.cast = self._decorator_after(self._smite_4p.cast)

    def before_cast(self):
        pass

    def after_cast(self):
        self.disc.active_atonements.extend_random(self._extend_amount)

class Amirdrassil_4p(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__(name='Amirdrassil_4p', disc=disc, n_points=1)
        self._scov = disc._buffs["SC"]
        self._smite_4p = disc.abilities['smite_4p']
        self.disc.cast = self._after_disc_cast(self.disc.cast)

    def _after_disc_cast(self, disc_cast):

        def wrapper_4p(*args, **kwargs):
            cast_results, timestamp = disc_cast(*args, **kwargs)
            ability_name = kwargs['ability_name'] if 'ability_name' in kwargs else args[0]
            if self._scov.buff_active and ability_name == 'smite':
                cast_results2, _ = disc_cast(self._smite_4p.name)
                cast_results.extend(cast_results2)
            return cast_results, timestamp

        return wrapper_4p

    def before_cast(self):
        pass

    def after_cast(self):
        if self._scov.buff_active:
            self.disc.cast("smite_4p")

class InescapableTorment(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__("IT", disc=disc, n_points=1)

        self._bender_talented = disc.talents['Bender'] > 0
        self._pet = disc.abilities['bender'] if self._bender_talented else disc.abilities['sfiend']
        self._pet_name = "bender" if self._bender_talented else "sfiend"
        self._scov = self.disc._buffs["SC"]
        self._scov_extension_amount = 1. - 0.3*int(self._bender_talented)
        self._pet_extension_amount = self._scov_extension_amount
        self._it = disc.abilities['IT']

        self._penance = disc.abilities['penance']
        self._mind_blast = disc.abilities['mind_blast']
        self._swd = disc.abilities['swd']
        self._swd_execute = disc.abilities['swd_execute']

        for ability in [self._penance, self._swd, self._swd_execute]:
            ability.cast = self._decorator_before(ability.cast)

        for ability in [self._mind_blast]:
            ability.cast = self._decorator_after(ability.cast)

    def before_cast(self):
        if self._pet.buff_active:
            self.disc.cast('IT')
            self.disc.extend_buff(self._scov, self._scov_extension_amount)
            self.disc.extend_buff(self._pet, self._pet_extension_amount)

    def after_cast(self):
        if self._pet.buff_active:
            self.disc.cast('IT')
            self.disc.extend_buff(self._scov, self._scov_extension_amount)
            self.disc.extend_buff(self._pet, self._pet_extension_amount)

class HarshDiscipline(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__("HD", disc=disc, n_points=disc.talents["HD"], ability=disc.abilities["pwr"], max_stacks=2, buff_duration=30)

        self._penance = disc.abilities['penance']
        self._penance_heal = disc.abilities['penance_heal']
        self._penance.cast = self._consume_self(self._penance.cast)
        self._penance_heal.cast = self._consume_self(self._penance_heal.cast)


    def before_cast(self):
        pass

    def after_cast(self):
        self.disc.apply_buff(self)

    def _on_apply(self):
        self._penance.n_bolts += self.n_points
        self._penance_heal.n_bolts += self.n_points

    def _on_expire(self):
        self._penance.n_bolts -= self._stacks*self.n_points
        self._penance_heal.n_bolts -= self._stacks*self.n_points

class WordsOfThePious(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__(name="WordsOfThePious", disc=disc, n_points=1, buff_duration=10)

        self._buff_effect = 1.1
        self._reverse_buff_effect = 1/1.1
        self._pws = disc.abilities["pws"]
        self._pws_rapture = disc.abilities["pws_rapture"]
        self._smite = disc.abilities["smite"]
        self._smite_4p = disc.abilities["smite_4p"]

        self._pws.cast = self._decorator_after(self._pws.cast)
        self._pws_rapture.cast = self._decorator_after(self._pws_rapture.cast)

    def before_cast(self):
        pass

    def after_cast(self):
        self.disc.apply_buff(self)

    def _on_apply(self):
        self._smite.dmg_sp_coef *= self._buff_effect
        self._smite_4p.dmg_sp_coef *= self._buff_effect

    def _on_expire(self):
        self._smite.dmg_sp_coef *= self._reverse_buff_effect
        self._smite_4p.dmg_sp_coef *= self._reverse_buff_effect

class TwilightEquilibrium(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__(name="TwilightEquilibrium", disc=disc, n_points=1, buff_duration=6)
        self._buff_effect = 1.15
        self._reverse_buff_effect = 1/1.15
        self._last_cast_type = None
        self._curr_applied_type = None

        self.disc.cast = self._disc_cast_after(self.disc.cast)

    def _disc_cast_after(self, disc_cast):

        def te_wrapper(*args, **kwargs):
            ability_to_cast = kwargs["ability_name"] if "ability_name" in kwargs else args[0]
            ability_to_cast = self.disc.abilities[ability_to_cast]
            if ability_to_cast.dmg_sp_coef > 0:
                self._last_cast_type = ability_to_cast.throughput_type
            ability_events, timestamp = disc_cast(*args, **kwargs)
            if self._last_cast_type in (ThroughputType.LIGHT, ThroughputType.SHADOW):
                if self.buff_active and self._curr_applied_type == self._last_cast_type:
                    self.disc.consume_buff(buff=self)
                self.disc.apply_buff(self)
            return ability_events, timestamp

        return te_wrapper

    def before_cast(self):
        pass

    def after_cast(self):
        pass

    def _on_apply(self):
        applied_type = ThroughputType.LIGHT if self._last_cast_type == ThroughputType.SHADOW else ThroughputType.SHADOW
        if applied_type == self._curr_applied_type:
            return
        self.disc.throughput_type_dmg_effects[applied_type] *= self._buff_effect
        self._curr_applied_type = applied_type

    def _on_expire(self):
        self.disc.throughput_type_dmg_effects[self._curr_applied_type] *= self._reverse_buff_effect
        self._curr_applied_type = None

class Evangelism(DiscTalentWrapper):

    def __init__(self, disc: Discipline):
        super().__init__("Evangelism", disc=disc, n_points=1, buff_duration=0)
        self._extend_duration = 6
        self._evangelism = disc.abilities["evangelism"]
        self._evangelism.cast = self._decorator(self._evangelism.cast)

    def before_cast(self):
        atonement_handler = self.disc.active_atonements
        atonement_handler.active_atonements[atonement_handler.target_has_atonement] += self._extend_duration

    def after_cast(self):
        pass

class HeavensWrath(DiscTalentWrapper):

    def __init__(self, disc: Discipline, n_points: int):
        super().__init__("HW", disc=disc, n_points=n_points)

        self._penance = disc.abilities['penance']
        self._up = disc.abilities['up']
        self._cdr_reduction_per_bolt = self.n_points

        self._penance.cast = self._decorator(self._penance.cast)
        self._bolts_fired = 0

    def after_cast(self):
        self._up.progress_time(self._bolts_fired*self._cdr_reduction_per_bolt)
        pass


    def before_cast(self):
        self._bolts_fired = self._penance.n_bolts
        pass