# KumpuWoWSims
Some libraries for simming throughput of healers in WoW. Currently only supports Disc priest.
Use the DiscAbilityNames.py to see how each ability is cast, KumpuSims.py has examples how to easily make use of this mess.

TODO:


Missing features:

Holy Nova, Divine Star, Shadow Word: Pain (purge the wicked is implemented), PTW and SW:P on-cast damage application, Mind games, PW:L, Throes of Pain, Benevolence (redundant), Expiation, Weal and Woe, Enduring Luminescense,
Sanctuary, Malicious Intent, Exaltation, Contrition, Leech in its entirety (redundant), Crystalline Reflection

Known bugs:

Words of the Pious will increase the damage of smite if cast started when buff was active but finished after the buff expired.
Divine Aegis increases the damage done of spells in addition to healing.
Twilight Equilibrium does not snapshot DoTs at the moment, but works dynamically, e.g. when the light buff is on, the ticks on PtW are increased.
It was less of a hassle to make sw:d have 2 charges when in execution and some workaround magic was done for it to make it work pretty much how it works in the game. Surely some bugs can be found with this.

Other improvements:

Move the buff handling from Discipline class to BuffManager for the sake of anyone working on this.
Move functionality from Disc to Specialization for modularity.
Implement the Ability's cast function as a generator system, with member variables
_effects_before and _effects_after so that different effects are applied at the correct times
and removes the need of decorators for effects.

