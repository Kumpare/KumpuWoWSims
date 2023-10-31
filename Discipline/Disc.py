from General.Spec import Specialization
from typing import Union
from General.Stats import Stats
from General.math import partially_linear_function
from General.Constants import *
import numpy as np
from General.Ability import Ability, Buff, TickingBuff, AbilityEvent
import pandas as pd
pd.options.mode.chained_assignment = None
from Discipline import DiscTalents
from Discipline.DiscAbilities import DiscAbility, DiscBuff, DiscTickingBuff, DiscAbilityEvent, Penance, SWD_Execute
from General.ThroughputTypes import ThroughputType


class Discipline(Specialization):
    _MASTERY_EFFECT_FACTOR = 1.15

    _BASE_ATONEMENT_DURATION = 15.
    _BASE_ATONEMENT_TRANSFER = 0.4

    _BASE_RADIANCE_ATONEMENT_DURATION_MODIFIER = 0.6
    _BASE_RADIANCE_CAST_TIME = 2

    _PWS_COOLDOWN = 7.5

    #talent durations
    _BORROWED_TIME_DURATION = 4
    _BASE_RAPTURE_DURATION = 9

    _SINS_MULTIPLIERS = [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.1725,
                        1.15, 1.125, 1.1, 1.075, 1.055, 1.04, 1.025,
                        1.02, 1.015, 1.0125, 1.01, 1.0075, 1.00625, 1.005]
    _SINS_MULTIPLIERS = np.array(_SINS_MULTIPLIERS)

    def __init__(self, talents: dict, stats: Stats = Stats()):
        super().__init__(stats)
        self.active_atonements = AtonementHandler()
        self.time = 0
        self.talents = {
            # class tree
            'Rhapsody': 0,
            'WotP': 0,
            'ST': 0,
            'Sanlayn': 0,
            'ToP': 0,
            'UW': 0,
            'BH': 0,
            'Benevolence': 0,
            'Halo': 0,
            'DS': 0,
            'Essence Devourer': 0,

            # spec tree
            'DI': 0,
            'PP': 0,
            'SC': 0,
            'Schism': 0,
            'TC': 0,
            'Rapture': 0,
            'Indemnity': 0,
            'Exaltation': 0,
            'PaS': 0,
            'Castigation': 0,
            'BT': 0,
            'AR': 0,
            'ToT': 0,
            'DA': 0,
            'BoL': 0,
            'UP': 0,
            'UP_CDR': 0,
            'UP_A': 0,
            'Evangelism': 0,
            'Lenience': 0,
            'HD': 0,
            'TE': 0,
            'Expiation': 0,
            'VS': 0,
            'IT': 0,
            'Bender': 0
        }
        self._buffs = dict()
        for key in talents:
            assert key in self.talents, f'Key {key} not a valid talent'
            self.talents[key] = talents[key]

        self.gcd = GCD/stats.stat_to_percent('haste')
        self.half_gcd = HALF_GCD/stats.stat_to_percent('haste')
        self.radiance_cast = 2/stats.stat_to_percent('haste')

        self.pws_atonement_duration = 17 if self.talents['Indemnity'] > 0 else 15

        self._init_abilities()

        self.active_buffs = pd.DataFrame(columns=['Next tick', 'Expiration time', 'ID'])
        self._active_buffs = dict()
        self._next_buff_id = 0

        self.throughput_type_effects = {tp_type: 1 for tp_type in ThroughputType}

    def progress_time(self, amount: float):
        self.time += amount
        self.active_atonements.progress_time(amount)

        for ability in self.abilities.values():
            ability.progress_time(amount)

        #remove expiring buffs
        expiring_buff_mask = self.active_buffs['Expiration time'] <= self.time
        expiring_buffs = self.active_buffs.loc[expiring_buff_mask]
        if expiring_buffs.size > 0:
            for event_id in expiring_buffs['ID']:
                ability = self._active_buffs.pop(event_id)
                ability.expire()

        self.active_buffs = self.active_buffs.loc[~expiring_buff_mask, :]

        #update next ticks
        tick_update_mask = self.active_buffs['Next tick'] <= self.time
        tick_ids = self.active_buffs.loc[tick_update_mask, 'ID']
        for ind, tick_id in tick_ids.items():
            ability = self._active_buffs[tick_id]
            assert isinstance(ability, DiscTickingBuff)
            self.active_buffs.at[ind, 'Next tick'] = self.time + ability.time_until_next_tick +int(ability.time_until_next_tick < 1e-3)*ability._tick_rate
        pass

    def stat_to_percent(self, stat: str):
        to_return = super().stat_to_percent(stat)
        m = 1. if stat.lower() != 'mast' else 1.15
        return to_return * m

    def stat_effect(self, stat: str):
        to_return = (1 + self.stat_to_percent(stat))*self.stat_increases[stat]
        return to_return

    def _init_abilities(self):
        h = 1 + self.stat_to_percent('haste')
        # Init abilities

        # PWS
        pws = DiscAbility('pws', cooldown=Discipline._PWS_COOLDOWN, cooldown_haste_scale=True,
                      haste_effect=h, heal_sp_coef=3.36*1.37, n_atonements_applied=1)
        pws_rapture = DiscAbility('pws_rapture', haste_effect=h, heal_sp_coef=3.36*1.37*1.4, n_atonements_applied=1)


        # Radiance
        pwr = DiscAbility('pwr', cast_time=Discipline._BASE_RADIANCE_CAST_TIME, haste_effect=h,
                      cooldown=15, charges=2, heal_sp_coef=4.095*5, n_atonements_applied=5,
                          atonement_duration=Discipline._BASE_RADIANCE_ATONEMENT_DURATION_MODIFIER*15)

        # Renew
        renew = DiscAbility('renew', haste_effect=h, heal_sp_coef=1.6)

        # Flash heal todo: self atonement proc
        flash_heal = DiscAbility('flash_heal', cast_time=1.5, haste_effect=h, heal_sp_coef=2.842*1.15*1.2, n_atonements_applied=1)

        # Penance
        penance_heal = Penance(haste_effect=h, heal_sp_coef=1.9)
        penance = Penance(haste_effect=h, dmg_sp_coef=0.53, procs_atonement=True)

        # Smite
        smite = DiscAbility('smite', cast_time=GCD, haste_effect=h, dmg_sp_coef=0.705, procs_atonement=True, throughput_type=ThroughputType.LIGHT)
        smite_4p = DiscAbility('smite_4p', cast_time=0, gcd=0, dmg_sp_coef=0.705, procs_atonement=True, throughput_type=ThroughputType.SHADOW)

        mind_blast = DiscAbility('mind_blast', cast_time=GCD, haste_effect=h, cooldown=24, cooldown_haste_scale=True,
                                 dmg_sp_coef=0.78336, procs_atonement=True)

        #todo sp coefs
        swd = DiscAbility('swd', dmg_sp_coef=1, cooldown=12, procs_atonement=True)
        swd_execute = DiscAbility('swd_execute', dmg_sp_coef=1, cooldown=12, charges=2, procs_atonement=True)

        #todo sp coefs
        bender = DiscTickingBuff('bender', cooldown=60, haste_effect=h, buff_duration=12, sp_coef=1, procs_atonement=True)
        sfiend = DiscTickingBuff('sfiend', cooldown=180, haste_effect=h, buff_duration=15, sp_coef=1, procs_atonement=True)
        ptw = DiscTickingBuff('ptw', haste_effect=h, buff_duration=24, sp_coef=1, procs_atonement=True) #todo own class for these

        self.abilities = {}
        for ability in [pws, pws_rapture, pwr, renew, flash_heal, penance_heal, penance, smite, mind_blast,
                        swd, swd_execute, bender, sfiend, ptw, smite_4p]:

            self.abilities[ability.name] = ability


        if self.talents["BT"] > 0:
            DiscTalents.BorrowedTime(self, pws, self.talents["BT"])
            DiscTalents.BorrowedTime(self, pws_rapture, self.talents["BT"])

        if self.talents["ToT"] > 0:
            DiscTalents.TrainOfThought_PWS(self)
            DiscTalents.TrainOfThought(self, smite, n_points=self.talents["ToT"])
            DiscTalents.TrainOfThought(self, smite_4p, n_points=self.talents["ToT"])

        if self.talents["Indemnity"] > 0:
            pws.atonement_duration = 17

        if self.talents["Schism"] > 0:
            DiscTalents.Schism(self)

        if self.talents["DI"] > 0:
            DiscTalents.DarkIndulgence(self)

        if self.talents["PP"] > 0:
            DiscTalents.PainfulPunishment(self)

        if self.talents["SC"] > 0:
            sc = DiscTalents.ShadowCovenant(self)
            self._buffs["SC"] = sc

        DiscTalents.Amirdrassil_4p(self)

        if self.talents["VS"] > 0:
            DiscTalents.VoidSummoner(self)
            DiscTalents.VoidSummoner(self)

        it = None
        if self.talents["IT"] > 0:
            it = DiscAbility("IT", gcd=0, dmg_sp_coef=1, throughput_type=ThroughputType.SHADOW, procs_atonement=True) #todo dmg_sp_coef
            self.abilities["IT"] = it
            DiscTalents.InescepableTorment(self)
            DiscTalents.InescepableTorment(self)
            DiscTalents.InescepableTorment(self)
            DiscTalents.InescepableTorment(self)

        if self.talents["BoL"] > 0:
            penance.dmg_sp_coef *= (1.08 if self.talents["BoL"] == 1 else 1.15)
            smite.dmg_sp_coef *= (1.08 if self.talents["BoL"] == 1 else 1.15)
            smite_4p.dmg_sp_coef *= (1.08 if self.talents["BoL"] == 1 else 1.15)

        if self.talents["HD"] > 0:
            DiscTalents.HarshDiscipline(self) #todo kaikki muutkin vain disc sisään

        if self.talents["Castigation"] > 0:
            self.abilities['penance'].n_bolts += 1
            self.abilities['penance_heal'].n_bolts += 1

    def set_haste(self):
        haste_effect = self.stat_effect("haste")
        self.gcd = GCD / haste_effect
        self.half_gcd = HALF_GCD / haste_effect
        self.radiance_cast = 2 / haste_effect
        for ability in self.abilities.values():
            ability.set_haste(haste_effect)
        pass

    def increase_haste(self, increase_amount: float):
        self.stat_increases["haste"] *= increase_amount
        self.set_haste()
        pass

    def cast(self, ability_name: str):
        to_return = []
        ability_to_cast = self.abilities[ability_name]

        if ability_to_cast.remaining_cooldown > 0 and ability_to_cast._charges == 0:
            self.progress_time(ability_to_cast.remaining_cooldown)

        cast_time = ability_to_cast.cast_time
        looped_events = self.loop_through_events_until(self.time + cast_time)
        to_return.extend(looped_events)

        next_event = ability_to_cast.cast(self.time)
        end_time = self.time + ability_to_cast.time_taken
        if isinstance(ability_to_cast, Buff):
            self.apply_buff(ability_to_cast)

        self.calculate_throughput(next_event)

        if isinstance(ability_to_cast, DiscAbility):
            if ability_to_cast.n_atonements_applied > 0:
                self.active_atonements.add_atonement(ability_to_cast.n_atonements_applied,
                                                     duration=ability_to_cast.atonement_duration + ability_to_cast.cast_time)

        looped_events2 = self.loop_through_events_until(self.time + ability_to_cast.time_taken)
        to_return.extend(looped_events2)
        self.progress_time(end_time - self.time)
        to_return.append(next_event)
        return to_return, self.time

    def loop_through_events_until(self, time_to_loop_to: float):
        to_return = []
        next_event_time, next_event = self.next_event
        while next_event is not None and next_event_time < time_to_loop_to:
            next_event_cast_result = next_event.cast(next_event_time)
            if next_event_cast_result is not None:
                self.calculate_throughput(next_event_cast_result)
                to_return.append(next_event_cast_result)
            self.progress_time(next_event_time - self.time)
            next_event_time, next_event = self.next_event
        return to_return

    @property
    def next_event(self):
        if self.active_buffs.size <= 0:
            return None, None
        min_event_times = self.active_buffs.loc[:, ['Next tick', 'Expiration time']].min(axis=1)
        next_event_time_ind = min_event_times.idxmin()
        next_event_time = min_event_times.loc[next_event_time_ind]
        event_ind = self.active_buffs.at[next_event_time_ind, 'ID']
        next_event = self._active_buffs[event_ind]
        return next_event_time, next_event

    def calculate_throughput(self, ability_event: DiscAbilityEvent):
        #todo käytä stat_effectiä
        crit_effect = 1 + self.stat_to_percent("crit")*(1.2 if "DA" in self.talents else 1)
        vers_effect = 1 + self.stat_to_percent("vers")
        throughput_type_effect_heal, throughput_type_effect_dmg = self.get_throughput_type_effect(ability_event.throughput_type)
        ability_event.dmg *= self.stats.main*crit_effect*vers_effect*throughput_type_effect_dmg
        ability_event.heal *= self.stats.main*crit_effect*vers_effect*throughput_type_effect_heal

        if ability_event.procs_atonement and ability_event.dmg > 0:
            mastery_effect = 1 + self.stat_to_percent("mast")
            n_atonements = self.active_atonements.n_atonements
            atonement_heal = ability_event.dmg*Discipline._BASE_ATONEMENT_TRANSFER*n_atonements*self.get_sins_multiplier(n_atonements)
            atonement_heal *= crit_effect*vers_effect*mastery_effect
            ability_event.heal += atonement_heal

    def get_sins_multiplier(self, n_atonements: int):
        return self._SINS_MULTIPLIERS[np.clip(n_atonements, 0, 20)]

    def apply_buff(self, ability: Buff):

        for buff_id, buff in self._active_buffs.items():
            if type(ability) == type(buff):
                self.refresh_buff(buff_id)
                return buff_id
        ability.apply(self.time + ability.cast_time)
        self.active_buffs.loc[self._next_buff_id, ['Expiration time', 'ID']] = self.time + ability.remaining_duration + ability.cast_time, self._next_buff_id

        if isinstance(ability, TickingBuff):
            self.active_buffs.loc[self._next_buff_id, ['Next tick']] = self.time + ability._tick_rate

        self._active_buffs[self._next_buff_id] = ability
        self._next_buff_id += 1
        return self._next_buff_id - 1

    def refresh_buff(self, buff_id: int):
        buff = self._active_buffs[buff_id]
        buff.refresh_duration()
        self.active_buffs.loc[self.active_buffs['ID'] == buff_id]['Expiration time'] = self.time + buff.remaining_duration
        pass

    def extend_buff(self, buff: Buff, t_amount: float):

        if not buff.buff_active:
            return

        buff_id = self.find_buff_id(buff)
        buff.extend_duration(amount=t_amount)
        self.active_buffs.loc[self.active_buffs['ID'] == buff_id, 'Expiration time'] += t_amount
        pass

    def consume_buff(self, buff_id: int=None, buff: Buff=None):
        assert not (buff_id is None and buff is None)

        if buff_id is not None:
            active_buff = self._active_buffs.pop(buff_id)
            active_buff.expire()
            self.active_buffs.drop((self.active_buffs['ID'] == buff_id).index, inplace=True)
            return

        buff_id = self.find_buff_id(buff)
        assert buff_id is not None, f'Could not consume buff {buff}, because such buff was not found.'
        buff.expire()
        self._active_buffs.pop(buff_id)
        self.active_buffs.drop((self.active_buffs['ID']==buff_id).index, inplace=True)
        pass

    def get_throughput_type_effect(self, type: ThroughputType):
        base_increase = self.throughput_type_effects[ThroughputType.NONE_TYPE]

        heal_increase = base_increase
        dmg_increase = base_increase

        if type != ThroughputType.NONE_TYPE:
            dmg_increase *= self.throughput_type_effects[type]
            heal_increase *= self.throughput_type_effects[type]

        return heal_increase, dmg_increase

    def find_buff_id(self, buff:Buff):

        for id, b in self._active_buffs.items():
            if type(b) == type(buff):
                return id
        return None

class AtonementHandler:

    def __init__(self, max_atonements: int = 20, base_atonement_duration: float = Discipline._BASE_ATONEMENT_DURATION):
        self.active_atonements = np.zeros((max_atonements,))
        self._next_ind = 0
        self._base_duration = base_atonement_duration

    def add_atonement(self, n: int, duration: float = None, player_ind: int=None):
        if n < 1:
            print(f'WARNING: attempted to add {n} atonements. Bypassing this')
            pass
        duration = duration if duration else self._base_duration

        for _ in range(n):
            ind = player_ind if player_ind is not None else self._next_ind
            self.active_atonements[ind] = duration
            self._update_index()

        pass

    def _update_index(self):
        self._next_ind = np.argmin(self.active_atonements)
        pass

    def progress_time(self, t: float):
        assert t >= 0, f'Time must be progressed by a non-negative amount. Was passed {t}'
        self.active_atonements -= t
        pass

    @property
    def min_atonement_duration(self):

        to_return = self.active_atonements[self.active_atonements > 0].min()
        return to_return

    @property
    def target_has_atonement(self):
        return self.active_atonements > 0

    @property
    def n_atonements(self):
        return (self.active_atonements > 0).astype('uint8').sum()


