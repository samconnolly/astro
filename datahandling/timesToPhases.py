"""
timesToPhases.py 

Sam Connolly 19/8/13

Convert your exposure times to orbital phases!

!!! THIS IS ALL IN HJD !!! 
Apparently that's a good thing to use for ephemerides - to calculate it, use: 
http://www.physics.sfasu.edu/astro/javascript/hjd.html

"""

import numpy as np

def TimeToPhase(HJD,eph,period):
	'''
	Convert from HJD and period to a phase!
	(not very accurate, but within a second...)

	Args:
		HJD		Time you want a phase for in HJD format
		eph		Ephemeris, also in HJD format (0 phase...)
		period	period, in DAYS

	returns:
		(float) phase at time HJD

	'''

	# calculate phase...

	elapsed = obs - eph

	orbits = int(elapsed/period)

	phase = (elapsed/period) - orbits

	return phase


