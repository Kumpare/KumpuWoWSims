from Discipline.Disc import DiscAbility, DiscTickingBuff, Discipline
from General.ThroughputTracker import ThroughputTracker
from General.Stats import Stats

def DiscSim_test(disc: Discipline):

    disc = ThroughputTracker(disc)

    disc.cast("pws_rapture")
    disc.cast("pws_rapture")
    disc.cast("ptw")
    disc.cast("renew")
    disc.cast("flash_heal")

    result = disc.data
    print(result)

talents1 = {
    "Schism": 1,
    "PP": 1,
    "DI": 1
}
stats1 = Stats(main=10000, crit=4000, haste=5000, mast=2000, vers=2000)
disc1 = Discipline(talents1, stats1)
DiscSim_test(disc1)



