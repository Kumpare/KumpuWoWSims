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

def sim_eva_rotation(discs: list):

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
        penance_4_smites(disc)
        rad_1_ramp(disc)
        disc.cast("up")
        penance_4_smites(disc)
            #rad_2_ramp(disc)

        print(f'Radiance remaining cooldown and available charges:')
        print(disc.abilities['pwr'].remaining_cooldown, disc.abilities['pwr']._charges)
        print(f'Sfiend remaining cooldown and time from last cast: ')
        print(disc.abilities['sfiend'].remaining_cooldown, disc.time - prev_sfiend_cast)

    plot_throughputs(trackers)

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
stats1 = Stats(main=13000, crit=5400, haste=7000, mast=1780, vers=1780)
disc1 = Discipline(talents1, stats1)

stats2 = Stats(main=13000, crit=4000, haste=8000, mast=1560, vers=800)
disc2 = Discipline(talents1, stats2)

stats3 = Stats(main=13000, crit=4000, haste=8560, mast=1000, vers=800)
disc3 = Discipline(talents1, stats3)
sim_eva_rotation([disc1, disc2, disc3])




