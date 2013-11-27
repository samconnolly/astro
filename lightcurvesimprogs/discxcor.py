
"""
callxcor.py

Created in November  2012

Author: Sam Connolly

#================================================================================
# 			Discrete cross-correlation code
#================================================================================

Cross-correlate two data sets and produces a the cross-correlation function for
a given range of time lags. Uses the discrete method, whereby every data point
is cross-correlated with every other and the time lag is the actual difference
in time between the measurements, then these coefficients are binned.

"""

# import modules
import numpy as np

#========= Cross-Correlation Function ===========================================

def xcor(r,rt,x,xt,nbins, t_lim = False,t_range = 300.):
                        
        '''
        Function:
            Calculates the cross-correlation function for two data sets with
		   non-simultaneous data, using the discrete method - every data point
		   is cross-correlated with every point in the other data set, the time
		   lag is taken as the actual time difference between the measurements
		   and the coefficients are binned.
        
        Arguments:
            
            r:       
                first data set - amplitudes (e.g. count rate or flux) - array
            rt:       
                first data set - times - array
            x:       
                second data set - amplitudes (e.g. count rate or flux) - array
            xt:       
                second data set - times - array
		   nbins:
			  number of bins to use across the time lag range - integer
                                                                                                                                                
        Returns:
                     ccf:        
                         (array)    Cross-correlation function
  				   tlag:        
                         (array)    time lags corresponding to the CCF
                                                                
        '''                                        


	# function arrays

	tlag    = []	# bin times
	ccx     = []	# CCF
	lag     = []	# time lags

	# find average value of each data set
	rav  = np.mean(r)
	xav  = np.mean(x)

	# find standard deviations of each data set

	rsd  = np.std(r)
	xsd  = np.std(x)
		
	# ----- calculate cross correlation coefficients (CCCs) ---------------------

	# create time grids, subtract to create lag grid
	rtime = np.array([rt for i in range(len(xt))])	# horizontal grid of radio times
	xtime = np.array([xt for j in range(len(rt))]).T	# vertical grid of xray times
	
	lag = rtime - xtime							# lag grid

	# create flux grids, calculate CCC grid
	rflux = np.array([r for i in range(len(x))])		# horizontal grid of radio flux
	xflux = np.array([x for j in range(len(r))]).T	# vertical grid of xray flux
	
	ccx = ( (rflux-rav)*(xflux-xav) ) / (rsd*xsd)		# ccc grid
	
	ccx = ccx.reshape([1,len(x)*len(r)])[0]			# change arrays to single
	lag = lag.reshape([1,len(x)*len(r)])[0]			# lists of values
	
	# ----- bin CCCs in time ----------------------------------------------------

	# find time range, set up bin arrays
	if t_lim:
		tmin 	= -t_range						# lowest lag
		trange 	= t_range	*2						# time range

	else	:	
		tmin 	= min(lag)						# lowest lag
		trange 	= max(lag) - tmin					# time range
	
	wbin   	= trange / float(nbins)			# bin width
	
	ccf    = np.zeros(nbins)					# CCC bin array
	ccfn   = np.zeros(nbins)					# number of counts in each bin

	# bin data
	
	b  = ((lag - tmin - 1) / wbin ).astype(int) 			# array of bin indices

	for i in range(len(ccx)):
		if 0 <= b[i] < nbins:						# check if inside desired range
			ccf[b[i]]  	+= ccx[i]						# add CCC to CCF bins
			ccfn[b[i]] 	+= 1							# add count to bin 
	
	# set empty bin counts to 1, to avoid "nan"
	
	empty = (ccfn == 0)		# boolean array with 1 for every empty bin
	ccfn  = ccfn + empty		# add to bin counts

	# average bins

	ccf /= ccfn

	# create time array corresponding to bins
	it = np.arange(nbins)
	tlag = it*wbin + tmin + 3
	
	# find lowest bin count
	binav = np.mean(ccfn)
			
	return ccf, tlag , binav

