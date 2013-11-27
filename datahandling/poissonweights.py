"""
poissonweights.py

Sam Connolly, sometime in 2013

Creates a file containing a list of the average poisson variance of a list of datasets
"""

import numpy as np

#===================== INPUT PARAMETERS ========================================

route   = "/data/saku10/sam/WorkingData/v926sco/chip4/molly06/"
listname   = "molly.in"

#===============================================================================

location = route+fname

flist = [] 

fin = open(location, 'r')

for y in fin:
	a, cfile, b,c,d,e,f,g,h = y.split
	flist.append(cfile)

fin.close()
	
for afile in flist:

	fcurr = open(route+afile,'r')

	time    = np.array([])
	flux    = np.array([])

	for x in fcurr:
		currtime, currflux = x.split()
		time = np.append(time,float(currtime))
		flux = np.append(flux,float(currflux))

	psigma = (np.sqrt(flux) )

	pstot = np.sqrt( 1.0 / np.sum(1.0 / psigma**2) )


