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

    pwr = disc.abilities["pwr"]
    scov = disc._buffs["SC"]
    penance = disc.abilities["penance"]
    mind_blast = disc.abilities["mind_blast"]
    pet_name = "sfiend" if disc.talents['Bender'] == 0 else 'bender'
    pet = disc.abilities[pet_name]
    potds = disc.abilities["PotDS"]

    disc.cast("ptw")
    disc.cast("ptw")
    evangelism_ramp(disc)
    disc.cast(pet_name)

    disc.cast("mind_blast")
    penance_4_smites(disc)
    penance_4_smites(disc)

    mini_ramp_time = 5*disc.gcd + disc.radiance_cast
    mini_ramp_time /= (1 + 0.04*disc.talents["BT"])
    time_until_ramp_ready = max((0 -pwr._charges)*15 + pwr.remaining_cooldown, pet.remaining_cooldown*disc.talents["Bender"])
    while time_until_ramp_ready > mini_ramp_time or scov.buff_active:
        if mind_blast.remaining_cooldown > 0:
            disc.cast("smite")
        else:
            disc.cast("mind_blast")

        time_until_ramp_ready = max((1 - pwr._charges)*15 + pwr.remaining_cooldown, pet.remaining_cooldown*disc.talents["Bender"])

    rad_1_ramp(disc)
    if pet.remaining_cooldown <= 0:
        disc.cast(pet_name)

    if potds.buff_active:
        disc.cast("penance")
        if mind_blast.remaining_cooldown <= 0:
            disc.cast("mind_blast")
    else:
        if mind_blast.remaining_cooldown <= 0:
            disc.cast("mind_blast")
        disc.cast("penance")

    for _ in range(4):
        disc.cast("smite")

    if penance.remaining_cooldown <= 0:
        disc.cast("penance")

    rapture_ramp_time = 7*disc.gcd + disc.radiance_cast
    rapture_ramp_time /= 1 + 0.04*disc.talents["BT"]

    time_until_ramp_ready = max((1 -pwr._charges)*15 + pwr.remaining_cooldown, pet.remaining_cooldown)

    while time_until_ramp_ready > rapture_ramp_time:

        if mind_blast.remaining_cooldown > 0:
            disc.cast("smite")
        else:
            disc.cast("mind_blast")


        time_until_ramp_ready = max((1 -pwr._charges)*15 + pwr.remaining_cooldown, pet.remaining_cooldown)

    disc.cast("ptw")
    for _ in range(5):
        disc.cast("pws_rapture")
    disc.cast("flash_heal")
    disc.cast("pws_rapture")
    disc.cast("pwr")
    disc.cast("pwr")
    disc.cast(pet_name)

    if potds.buff_active:
        disc.cast("penance")
        if mind_blast.remaining_cooldown <= 0:
            disc.cast("mind_blast")
    else:
        if mind_blast.remaining_cooldown <= 0:
            disc.cast("mind_blast")
        disc.cast("penance")

    time_until_ramp_ready = max((0 - pwr._charges) * 15 + pwr.remaining_cooldown, pet.remaining_cooldown * disc.talents["Bender"])
    while time_until_ramp_ready > mini_ramp_time or scov.buff_active:
        if mind_blast.remaining_cooldown > 0:
            disc.cast("smite")
        else:
            disc.cast("mind_blast")

        time_until_ramp_ready = max((1 - pwr._charges) * 15 + pwr.remaining_cooldown, pet.remaining_cooldown * disc.talents["Bender"])

    rad_1_ramp(disc)
    if pet.remaining_cooldown <= 0:
        disc.cast(pet_name)

    if potds.buff_active:
        disc.cast("penance")
        if mind_blast.remaining_cooldown <= 0:
            disc.cast("mind_blast")
    else:
        if mind_blast.remaining_cooldown <= 0:
            disc.cast("mind_blast")
        disc.cast("penance")

    for _ in range(4):
        disc.cast("smite")

    evangelism_ramp_time = 9 * disc.gcd + disc.radiance_cast
    evangelism_ramp_time /= 1 + 0.04 * disc.talents["BT"]

    time_until_ramp_ready = max((1 - pwr._charges) * 15 + pwr.remaining_cooldown, pet.remaining_cooldown)

    while time_until_ramp_ready > evangelism_ramp_time:

        if mind_blast.remaining_cooldown > 0:
            disc.cast("smite")
        else:
            disc.cast("mind_blast")

        time_until_ramp_ready = max((1 - pwr._charges) * 15 + pwr.remaining_cooldown, pet.remaining_cooldown)

    print('#####################################')
    print(f'Remaining pet cooldown: {pet.remaining_cooldown}')
    print(f'PWR charges and cd: {pwr._charges, pwr.remaining_cooldown}')
    print(f'Mind blast cd: {mind_blast.remaining_cooldown}')
    print(f'Scov remaining duration: {scov.remaining_duration}')
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
    pet_name = 'bender' if disc.talents["Bender"] > 0 else 'sfiend'
    pet = disc.abilities[pet_name]
    pwr = disc.abilities["pwr"]
    penance = disc.abilities["penance"]
    scov = disc._buffs["SC"]
    potds = disc.abilities["PotDS"]
    mind_blast = disc.abilities["mind_blast"]

    disc.cast("ptw")
    disc.cast("ptw")
    evangelism_ramp(disc)
    disc.cast(pet_name)
    if disc.gcd <= 1:
        disc.cast("penance")

    disc.cast("mind_blast")
    if disc.gcd <= 1:
        disc.cast("swd")
    else:
        disc.cast("penance")

    ramp_time = (7*disc.gcd + disc.radiance_cast)/(1 + 0.04*disc.talents["BT"])
    radiance_cast = disc.radiance_cast/(1 + 0.04*disc.talents["BT"])
    time_until_ramp_start = max((1 - pwr._charges)*15 + pwr.remaining_cooldown, pet.remaining_cooldown - radiance_cast)
    while time_until_ramp_start > ramp_time:

        if mind_blast.ready and pwr.remaining_cooldown > mind_blast.cooldown:
            disc.cast("mind_blast")
        else:
            disc.cast("smite")

        time_until_ramp_start = max((1 - pwr._charges)*15 + pwr.remaining_cooldown, pet.remaining_cooldown - radiance_cast)

    disc.cast("ptw")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("flash_heal")
    disc.cast("pws_rapture")
    disc.cast("pwr")
    disc.cast("pwr")
    disc.cast(pet_name)
    disc.cast("mind_blast")

    while (1 - pwr._charges)*15 + pwr.remaining_cooldown > 10 or pet.remaining_cooldown > 10:
        if penance.ready:
            disc.cast("penance")
        else:
            disc.cast("smite")

    return tracker

def eva_up_rapture_2_rads_ready(disc: Discipline):

    tracker = ThroughputTracker(disc)

    scov = disc._buffs["SC"]
    sfiend = disc.abilities["sfiend"]
    pwr = disc.abilities["pwr"]
    penance = disc.abilities["penance"]

    disc.cast("ptw")
    disc.cast("ptw")
    evangelism_ramp(disc)
    disc.cast("sfiend")
    disc.cast("mind_blast")

    while scov.buff_active and (1 - pwr._charges)*15 + pwr.remaining_cooldown > 8:
        if penance.remaining_cooldown > 0.1:
            disc.cast("smite")
        else:
            disc.cast("penance")

    disc.cast("ptw")
    disc.cast("pws")
    disc.cast("renew")
    disc.cast("flash_heal")
    disc.cast("pws")
    disc.cast("pwr")

    if disc.abilities["mind_blast"].cooldown < 15 + pwr.remaining_cooldown + 0.25:
        disc.cast("mind_blast")
    disc.cast("up")
    disc.cast("penance")

    while sfiend.remaining_cooldown > 10 or (1 - pwr._charges)*15 + pwr.remaining_cooldown > 10:
        if penance.remaining_cooldown > 0.1:
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
    disc.cast("pws_rapture")
    disc.cast("flash_heal")
    disc.cast("pws_rapture")
    disc.cast("pwr")
    disc.cast("pwr")
    disc.cast("sfiend")
    disc.cast("mind_blast")

    while scov.buff_active:
        if penance.remaining_cooldown > 0.1:
            disc.cast("smite")
        else:
            disc.cast("penance")

    rad_1_ramp(disc)
    disc.cast("mind_blast")
    disc.cast("penance")

    while sfiend.remaining_cooldown > 10 or (1 - pwr._charges)*15 + pwr.remaining_cooldown > 10:
        if penance.remaining_cooldown > 0.1:
            disc.cast("smite")
        else:
            disc.cast("penance")

    print(disc.abilities["up"].remaining_cooldown)
    return tracker

def sfiend_2_rads(disc: Discipline):

    tracker = ThroughputTracker(disc)

    disc.cast("ptw")
    evangelism_ramp(disc)
    disc.cast("sfiend")
    disc.cast("mind_blast")
    disc.cast("swd")

    penance_4_smites(disc)
    penance_4_smites(disc)
    penance_4_smites(disc)
    penance_4_smites(disc)
    disc.cast("smite")
    disc.cast("smite")
    #disc.cast("smite")

    print(f'{disc.abilities["sfiend"].remaining_cooldown}')
    print(f'{disc.abilities["pwr"].remaining_cooldown}')
    quit()



talents_bender = {
    "WotP": 1,
    'UW': 2,
    'ED': 1,
    "Schism": 1,
    "PP": 1,
    "DI": 1,
    "SC": 1,
    "Castigation": 1,
    "AR": 2,
    "BT": 0,
    "Indemnity": 1,

    # tot
    "ToT": 1,
    'DA': 1,
    "BoL": 2,

    #up
    'HW': 0,
    'OwL': 0,

    #vs
    "VS": 1,
    "IT": 1,
    "Bender": 1,

    #eva
    "Evangelism": 1,
    "HD": 2,
    "TE": 0
}

talents_sfiend = {
    "WotP": 1,
    'UW': 2,
    'ED': 1,
    "Schism": 1,
    "PP": 1,
    "DI": 1,
    "SC": 1,
    "Castigation": 1,
    "AR": 2,
    "BT": 2,
    "Indemnity": 1,

    # tot
    "ToT": 1,
    'DA': 1,
    "BoL": 2,

    # up
    'HW': 0,
    'OwL': 0,

    # vs
    "VS": 1,
    "IT": 1,
    "Bender": 0,

    # eva
    "Evangelism": 1,
    "HD": 2,
    "TE": 0
}

stats1 = Stats(main=13000, crit=5400, haste=5400, mast=1780, vers=1780)
stats_taikki = Stats(main=13000, crit=4000, haste=8650, mast=1000, vers=800)
stats2 = Stats(main=13000, crit=5400, haste=5400, mast=1780, vers=1780)

disc1 = Discipline(talents_bender, stats1)
disc2 = Discipline(talents_sfiend, stats_taikki)

tracker1 = start_new_ramp_when_sfiend_and_2_rads_ready(disc1)
tracker2 = start_new_ramp_when_sfiend_and_2_rads_ready(disc2)


plot_throughputs([tracker1, tracker2], labels=['Bender - low haste', 'Sfiend - high haste'])
print("test")


