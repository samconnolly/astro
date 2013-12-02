# fluxflux relation

# Plots the flux flux and flux hardness graphs for a given flux flux relation:
# HardTotal = Gradient*(SoftTotal - SoftConst)^alpha + HardConst
# (see Taylor, Uttley McHardy, MNRAS, 2003, 342, 31)

import numpy as np
import pylab as pl

# variables

hconst = 0.0
sconst = 0.0
grad   = 1.25
alpha  = 0.707

# flux arrays

soft = np.arange(0.0608,0.61,0.002)
hard = grad*((soft-sconst)**alpha) + hconst

# calculate hardness (H-S/H+S)

hardness = (hard - soft) / (hard + soft)
althardness = (grad*((soft-sconst)**alpha) + hconst - soft)/ \
			(grad*((soft-sconst)**alpha) + hconst + soft)

# plotting
pl.subplot(2,1,1)
pl.title("flux v flux")
pl.plot(hard,soft)

pl.subplot(2,1,2)
pl.title("hardness v hard flux")
pl.plot(hard,hardness)
pl.plot(hard,althardness)

pl.show()
