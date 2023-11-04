from Discipline.Disc import DiscAbility, DiscTickingBuff, Discipline
from General.ThroughputTracker import ThroughputTracker
from General.Stats import Stats
from Plotting.ThroughputPlotting import plot_throughputs
from typing import Union

def pws_2_renews(disc: Union[Discipline, ThroughputTracker]):
    disc.cast("pws")
    disc.cast("renew")
    disc.cast("renew")
    pass

def pws_3_renews(disc: Union[Discipline, ThroughputTracker]):
    pws_2_renews(disc)
    disc.cast("renew")
    pass

def cast_renew_until_pws_up(disc: Union[Discipline, ThroughputTracker]):
    pws = disc.disc.abilities["pws"]

    while pws.remaining_cooldown > 0:
        disc.cast("renew")

def penance_4_smites(disc: Union[Discipline, ThroughputTracker]):
    disc.cast("penance")
    for _ in range(4):
        disc.cast("smite")
    pass

def cast_smite_until_penance_is_up(disc: Union[Discipline, ThroughputTracker]):

    penance = disc.disc.abilities["penance"]

    while penance.remaining_cooldown > 0:
        disc.cast("smite")

    pass

def cast_rapture_pws(disc: Union[Discipline, ThroughputTracker]):

    rapture_pws = disc.disc.abilities["pws_rapture"]

    disc.cast("pws_rapture")
    n_casts_left = max(int((9 - rapture_pws.gcd)/rapture_pws.gcd), 9)

    for _ in range(n_casts_left):
        disc.cast("pws_rapture")

    pass

def evangelism_ramp(disc: Union[Discipline, ThroughputTracker]):


    # 4 atonements
    pws_3_renews(disc)
    # 7 atonements
    pws_2_renews(disc)

    #9 atonements
    disc.cast("flash_heal")

    #10 atonements
    disc.cast("pws")

    #20 atonements
    disc.cast("pwr")
    disc.cast("pwr")
    disc.cast("evangelism")

def rad_1_ramp(disc: Discipline):

    pws_2_renews(disc)
    disc.cast("flash_heal")
    disc.cast("pws")
    disc.cast("pwr")

def rad_2_ramp(disc: Discipline):
    pws_2_renews(disc)
    disc.cast("flash_heal")
    disc.cast("pws")
    disc.cast("pwr")
    disc.cast("pwr")
    pass

def DiscSim_test(disc: Discipline, disc2: Discipline):

    disc = ThroughputTracker(disc)
    disc2 = ThroughputTracker(disc2)
    pet = "sfiend" if disc.disc.talents["Bender"] == 0 else "bender"

    disc.cast("smite")
    disc.cast("pws_rapture")
    disc.cast("pws")
    disc.cast("ptw")
    disc.cast("renew")
    disc.cast("flash_heal")
    disc.cast("pwr")
    disc.cast("pwr")
    disc.cast(pet)
    while disc.disc.active_atonements.n_atonements > 2:
        disc.cast("smite")

    disc2.cast("ptw")
    disc2.cast("pws")
    disc2.cast("renew")
    disc2.cast("renew")
    disc2.cast("renew")
    disc2.cast("pws")
    disc2.cast("flash_heal")
    disc2.cast("pwr")
    disc2.cast("pwr")
    disc2.cast("evangelism")
    disc2.cast(pet)
    disc2.cast("mind_blast")
    disc2.cast("penance")
    for _ in range(4):
        disc2.cast("smite")
    disc2.cast("penance")
    for _ in range(4):
        disc2.cast("smite")

    plot_throughputs([disc, disc2])

def sim_eva_into_up(discs: list):

    trackers = []

    for i, disc in enumerate(discs):
        trackers.append(ThroughputTracker(disc))
        sc = disc._buffs["SC"]
        #disc.cast("pi")
        disc.cast("ptw")
        disc.cast("ptw")
        evangelism_ramp(disc)
        disc.cast("sfiend")
        prev_sfiend_cast = disc.time
        disc.cast("mind_blast")
        penance_4_smites(disc)
        penance_4_smites(disc)
        rad_1_ramp(disc)
        disc.cast("mind_blast")
        disc.cast("up")
        penance_4_smites(disc)
        penance_4_smites(disc)

        print(f'Radiance remaining cooldown and available charges:')
        print(disc.abilities['pwr'].remaining_cooldown, disc.abilities['pwr']._charges)
        print(f'Sfiend remaining cooldown and time from last cast: ')
        print(disc.abilities['sfiend'].remaining_cooldown, disc.time - prev_sfiend_cast)
        print(f'Mind blast remaining cooldown: ')
        print(disc.abilities['mind_blast'].remaining_cooldown)

    plot_throughputs(trackers)

def taikki_8650_no_buffs(disc: Discipline):

    tracker = ThroughputTracker(disc)

    disc.cast("mind_blast")
    disc.cast("ptw")
    disc.cast("ptw")
    disc.cast("pws")
    disc.cast("flash_heal")
    disc.cast("flash_heal")
    disc.cast("pws")
    disc.cast("renew")
    disc.cast("renew")
    disc.cast("renew")
    disc.cast("flash_heal")
    disc.cast("pws")
    disc.cast("pwr")
    disc.cast("pwr")
    disc.cast("evangelism")
    sfiend1_time = disc.time
    disc.cast("sfiend")
    disc.cast("penance")
    disc.cast("mind_blast")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    penance_4_smites(disc)
    penance_4_smites(disc)
    disc.cast("penance")
    disc.cast("mind_blast")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("ptw")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("flash_heal")
    disc.cast("pws_rapture")
    disc.cast("pwr")
    disc.cast("pwr")
    sfiend2_time = disc.time
    disc.cast("sfiend")
    disc.cast("penance")
    disc.cast("mind_blast")
    disc.cast("swd")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    penance_4_smites(disc)
    penance_4_smites(disc)
    disc.cast("penance")
    disc.cast("smite")
    disc.cast("mind_blast")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("penance")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("flash_heal")
    disc.cast("pws")
    disc.cast("flash_heal")
    disc.cast("renew")
    disc.cast("pws")
    disc.cast("renew")
    disc.cast("flash_heal")
    disc.cast("pws")
    disc.cast("pwr")
    disc.cast("pwr")
    disc.cast("sfiend")
    disc.cast("penance")
    disc.cast("mind_blast")
    disc.cast("swd")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    penance_4_smites(disc)
    penance_4_smites(disc)
    disc.cast("penance")
    disc.cast("smite")
    disc.cast("mind_blast")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("smite")

    return tracker

def eva_mini_rapture_mini(disc: Discipline, extra_casts: bool=False):

    tracker = ThroughputTracker(disc)

    disc.cast("ptw")
    disc.cast("ptw")
    evangelism_ramp(disc)
    disc.cast("sfiend")
    disc.cast("mind_blast")
    penance_4_smites(disc)
    penance_4_smites(disc)
    penance_4_smites(disc)
    rad_1_ramp(disc)
    disc.cast("mind_blast")
    penance_4_smites(disc)
    if extra_casts:
        disc.cast("penance")
        disc.cast("smite")
    disc.cast("smite")
    disc.cast("ptw")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("flash_heal")
    disc.cast("pwr")
    disc.cast("pwr")
    disc.cast("sfiend")
    disc.cast("mind_blast")
    penance_4_smites(disc)
    penance_4_smites(disc)
    penance_4_smites(disc)
    rad_1_ramp(disc)
    disc.cast("mind_blast")
    penance_4_smites(disc)
    disc.cast("smite")

    return tracker

def forced_30s_ramp(disc: Discipline):

    tracker = ThroughputTracker(disc)
    pwr = disc.abilities["pwr"]
    penance = disc.abilities["penance"]
    pet_name = "sfiend" if disc.talents['Bender'] == 0 else 'bender'
    pet = disc.abilities[pet_name]
    disc.cast("ptw")
    disc.cast("ptw")
    evangelism_ramp(disc)
    gcd = disc.gcd
    rad_cast = disc.radiance_cast
    ramp_time = 2*rad_cast + 10*gcd
    disc.cast(pet_name)
    disc.cast("mind_blast")

    while (1 - pwr._charges)*15 + pwr.remaining_cooldown > ramp_time:
        if penance.remaining_cooldown > 0:
            disc.cast("smite")
        else:
            disc.cast("penance")
    disc.cast("smite")
    disc.cast("smite")
    disc.cast("ptw")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("flash_heal")
    disc.cast("pws_rapture")
    disc.cast("pwr")
    disc.cast("pwr")
    if pet.remaining_cooldown <= 0:
        disc.cast(pet_name)
    disc.cast("mind_blast")
    print(pwr.remaining_cooldown, pwr._charges)
    print(pet.remaining_cooldown)

    while (1 - pwr._charges)*15 + pwr.remaining_cooldown > ramp_time:
        if penance.remaining_cooldown > 0:
            disc.cast("smite")
        else:
            disc.cast("penance")

    disc.cast("smite")
    disc.cast("smite")
    disc.cast("ptw")
    pws_3_renews(disc)
    rad_2_ramp(disc)
    disc.cast(pet_name)
    disc.cast("mind_blast")

    while (1 - pwr._charges)*15 + pwr.remaining_cooldown > ramp_time:
        if penance.remaining_cooldown > 0:
            disc.cast("smite")
        else:
            disc.cast("penance")

    return tracker

def start_new_ramp_when_sfiend_and_2_rads_ready(disc: Discipline):

    tracker = ThroughputTracker(disc)
    sfiend = disc.abilities["sfiend"]
    pwr = disc.abilities["pwr"]
    penance = disc.abilities["penance"]

    disc.cast("ptw")
    disc.cast("ptw")
    evangelism_ramp(disc)
    disc.cast("sfiend")
    disc.cast("mind_blast")

    while (1 - pwr._charges)*15 + pwr.remaining_cooldown > 10 or sfiend.remaining_cooldown > 10:
        if penance.remaining_cooldown > 0:
            disc.cast("smite")
        else:
            disc.cast("penance")

    disc.cast("ptw")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("flash_heal")
    disc.cast("pws_rapture")
    disc.cast("pwr")
    disc.cast("pwr")
    disc.cast("sfiend")
    disc.cast("mind_blast")

    while (1 - pwr._charges)*15 + pwr.remaining_cooldown > 10 or sfiend.remaining_cooldown > 10:
        if penance.remaining_cooldown > 0.1:
            disc.cast("smite")
        else:
            disc.cast("penance")

    return tracker

talents1 = {
    "Schism": 1,
    "PP": 1,
    "DI": 1,
    "SC": 1,
    "VS": 1,
    "Castigation": 1,
    "Bender": 0,
    "HD": 1,
    "BoL": 2,
    "IT": 1,
    "AR": 2,
    "BT": 2,
    "Evangelism": 1,
    "Indemnity": 1,
    "ToT": 1,
    "WotP": 1,
    "TE": 1,
    'HW': 2,
    'OwL': 1,
    'ED': 1,
    'UW': 2
}
talents_taikki1 = {
"Schism": 1,
    "PP": 1,
    "DI": 1,
    "DA": 1,
    "SC": 1,
    "VS": 1,
    "Castigation": 1,
    "Bender": 0,
    "HD": 2,
    "BoL": 2,
    "IT": 1,
    "AR": 2,
    "BT": 2,
    "Evangelism": 1,
    "Indemnity": 1,
    "ToT": 1,
    "WotP": 1,
    'ED': 1,
    'UW': 2
}
stats1 = Stats(main=13000, crit=5400, haste=5400, mast=1780, vers=1780)
disc1 = Discipline(talents_taikki1, stats1)

stats2 = Stats(main=13000, crit=4000, haste=8000, mast=1560, vers=800)
disc2 = Discipline(talents1, stats2)

stats3 = Stats(main=13000, crit=4000, haste=8560, mast=1000, vers=800)
disc3 = Discipline(talents_taikki1, stats3)
disc3_taikki = Discipline(talents_taikki1, stats3)
disc1_taikki = Discipline(talents_taikki1, stats1)
#tracker1 = forced_30s_ramp(disc1)
#tracker3 = forced_30s_ramp(disc3)
#sim_eva_into_up([disc1, disc2, disc3])
#tracker3_taikki = taikki_8650_no_buffs(disc3_taikki)
#tracker1_taikki = taikki_8650_no_buffs(disc1_taikki)
#tracker3 = eva_mini_rapture_mini(disc3, extra_casts=True)
#tracker1 = eva_mini_rapture_mini(disc1)
tracker1 = start_new_ramp_when_sfiend_and_2_rads_ready(disc1)
tracker3 = start_new_ramp_when_sfiend_and_2_rads_ready(disc3)
plot_throughputs([tracker1, tracker3], labels=['Norm haste, \nForced sfiend double rad', 'High haste, \nForced sfiend double rad'])



