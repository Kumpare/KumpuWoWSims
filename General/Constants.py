# GCD constants
GCD = 1.5  # Baseline GCD
GCD_CAP = GCD / 2.  # GCD can not be reduced below this value through haste
HALF_GCD = GCD / 2.  # Half GCD, used for some spells instead of the regular.
HALF_GCD_CAP = HALF_GCD / 2.

# Secondary stats
SECONDARY_STATS = ['crit', 'haste', 'mast', 'vers']

# Secondary stat conversions
# How much effect a single point of stat gives
STAT_CONVERSIONS = {i:1./j/100 if j else None for i,j in zip(SECONDARY_STATS, [180., 170., 133.3, 205.])}

# How much stat a single percent is worth
STAT_INVERSE = {i:1./j/100 if j else None for i,j in STAT_CONVERSIONS.items()}

# Secondary stat percent breakpoints
STAT_DR_BREAKPOINTS = (0.3, 0.39, 0.47, 0.54, 0.66, 1.26)
STAT_DR_PENALTIES = (1, 0.9, 0.8, 0.7, 0.6, 0.5, 0)
