
"""
2001secsToMJD.py

Created on Wed Nov  6 14:25:02 2013

Author: Sam Connolly

Seconds since 1st July 2001 - MJD... as the SWIFT data are in this format..

"""

def s2mjd(s):
	'''
	Convert from seconds since 1st July 2001 to MJD 
	(not very accurate, but within a second...)

	Args:
		s		seconds passes since  1st July 2001

	returns:
		(float) MJD

	'''

	DAY =  86400.0		# seconds in a day
	MJD2001 = 51910 		# MJD on 1st January 2001
	
	days = (s + 64.) / DAY  # number of days since 1/1/2001 at 
	
	return  MJD2001 + days
