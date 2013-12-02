"""
fluxsum.py

Simple programme to sum the flux in a flux file output from xspec. Not sure why
this is useful anymore.

Sam Connolly 29/04/13

"""

import numpy as np

#======== INPUT PARAMATERS =====================================================

# Flux file location 
location = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra\
/binsum/flux.dat"

# energy range to include
emin = 0.5
emax = 10.0

#===============================================================================

imin = int(emin/0.005)
imax = int(emax/0.005) + 1

fluxf = open(location, 'r')

flux = []

for line in fluxf:

	linedata = line.split()

	for datum in linedata:

		flux.append(float(datum)*200.0) # *200 converts  
												 # cnts cm^-2 s^-1 bin^-1 to 
												 # cnts cm^-2 s^-1 keV^-1
fluxf.close()

print np.array(flux[imin:imax])/200
print sum(flux[imin:imax])
