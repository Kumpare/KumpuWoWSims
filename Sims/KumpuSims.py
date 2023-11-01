from Discipline.Disc import DiscAbility, DiscTickingBuff, Discipline
from General.ThroughputTracker import ThroughputTracker
from General.Stats import Stats
from Plotting.ThroughputPlotting import plot_throughputs

def DiscSim_test(disc: Discipline):

    disc = ThroughputTracker(disc)
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
    disc.cast("mind_blast")
    disc.cast("penance")
    disc.cast("smite")

    result = disc.data
    plot_throughputs([disc])
    print(result)

talents1 = {
    "Schism": 1,
    "PP": 1,
    "DI": 1,
    "SC": 1,
    "VS": 1,
    "Bender": 1,
    "HD": 1,
    "BoL": 2,
    "IT": 1,
    "AR": 2,
}
stats1 = Stats(main=10000, crit=4000, haste=5000, mast=2000, vers=2000)
disc1 = Discipline(talents1, stats1)
DiscSim_test(disc1)

print()



