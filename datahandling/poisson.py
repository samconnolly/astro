"""
poisson.py

Sam Connolly, sometime in early 2013

Calculates average poisson variance in a dataset, between set limits
"""

import numpy as np
from pylab import *

# ================= INPUT PARAMETERS ===========================================

# limits (e.g. in time)
tmin = 4600.0
tmax = 4800.0

# file routes
route   = "/export/xray11/sdc1g08/Dropbox/Dropbox/V926Sco paper/"
froute  = "avspec/"
fname   = "textav"

# ==============================================================================

# --------------- Import data --------------------------------------------------

time    = np.array([])
flux    = np.array([])

location    = route+froute+fname

fin = open(location, 'r')

for x in fin:
	currtime, currflux = x.split()

	if float(currtime) >= tmin and float(currtime) <= tmax:
		time = np.append(time,float(currtime))
		flux = np.append(flux,float(currflux))

fin.close()


# --------------- Find Poisson variation ---------------------------------------

pstot = np.sqrt( len(flux) / np.sum(1.0 / flux) )

cmin   = int(min(flux))
cmax   = int(max(flux))+1
crange = int(cmax-cmin)
nbins  = 50
bwidth = crange/float(nbins)
bins  = np.zeros(nbins)

# bin data
for counts in flux:
	nbin = int( (counts-cmin)/(bwidth) )
	bins[nbin] += 1

corrbins = (arange(len(bins))*(bwidth)) + cmin

# calculate stats
av   = np.mean(flux)
stdv = np.std(flux)

avg  = [av,av]
line = [0,60]

std1 = [av+stdv,av+stdv]
std2 = [av-stdv,av-stdv]

# print results to compare
print "Calculated SD:",pstot, "Estimated SD:",np.sqrt(np.mean(flux)), "SD of distribution:", stdv,"Mean:", av

# plot
plot(corrbins, bins)
plot(avg,line)
plot(std1,line)
plot(std2,line)
show()

