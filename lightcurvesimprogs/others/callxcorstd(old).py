
"""
multisimfinal.py

Created in November  2012

Author: Sam Connolly

#================================================================================
# 			Discrete cross-correlation programme
#================================================================================

Cross-correlate two data sets and produces a the cross-correlation function for
a given range of time lags. Uses the discrete method, whereby every data point
is cross-correlated with every other and the time lag is the actual difference
in time between the measurements, then these coefficients are binned.

"""

# import modules
from numpy import zeros, sqrt
from pylab import *
xcor()
#========= Cross-Correlation Function ===========================================

def xcor(r,rt,x,xt,t_start,t_end,nbins):
                        
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
		   t_start:
		       lower end of time lag range to bin - float (seconds)
		   t_end:
		       upper end of time lag range to bin - float (seconds)
		   nbins:
			  number of bins to use across the time lag range - integer
                                                                                                                                                
        Returns:
                     ccf:        
                         (array)    Cross-correlation function
                     binsd:        
                         (array)    Standard deviations of each bin (= error...)
  				   tlag:        
                         (array)    time lags corresponding to the CCF
                                                                
        '''                                        


	# function arrays

	tlag    = []	# time lags
	ccx     = []	# CCF
	lag     = []	# time lags...

	# find average value of each data set
	rav  = np.mean(r)
	xav  = np.mean(x)

	# find standard deviations of each data set

	rsd  = np.std(r)
	xsd  = np.std(x)


	# ----- calculate cross correlation coefficients (CCCs) ---------------------

	for e in range(len(x)):		# for every data point in the first data point
		
		for f in range(len(r)):	# with every data point in the second data set

			# check for lags outside the time range of the first data set
			if (rt[f]-xt[e]) < t_end and (rt[f]-xt[e]) >= t_start:

				# calculate correlation value and equivalent lag

				ccx.append( ( (r[f]-rav)*(x[e]-xav) ) / (rsd*xsd) ) 	# CCC
				lag.append( rt[f]-xt[e] )							# lag

	# ----- bin CCCs in time ----------------------------------------------------

	# find time range, divide into bins

	trange = max(lag) - min(lag)	# time range
	wbin   = trange / nbins 		# bin width

	ccf    = zeros(nbins)					# CCC bin array
	ccfn   = zeros(nbins)					# number of counts in each bin
	binarray  = [[]for i in range(nbins)]	# array for values in each bin
	
	# bin data
	for l in lag:

		b         	= int( (l - tmin - 1) / wbin ) 	# index of bin for lag
		ccf[b]  		+= l							# add CCC to CCF bins
		ccfn[b] 		+= 1							# add count to bin 
		binarray[b].append(ccx[bt])					# add CCC to bin array

	# set empty bin counts to 1, to avoid "nan"

	for empty in range(len(ccfn)):

		if ccfn[empty] == 0:
			ccfn[empty] = 1

	# calculate errors from bin SDs

	binsd   = zeros(nbins)

	for bins in range(nbins):

		binsd[bins] = np.std(binarray[bins])

	# average bins

	for count in range(len(ccfn)):
		ccf[count]   = ccf[count]   / ccfn[count]
		binsd[count] = binsd[count] / ccfn[count]

	# create time array corresponding to bins

	for tl in range(nbins):
		tlag.append(tmin + tl*wbin +3)

		
	return ccf, binsd, tlag

