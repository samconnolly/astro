
"""
callXcorErrBinwise.py

Created in November  2012

Author: Sam Connolly

#================================================================================
# 			Discrete cross-correlation code for real data with errors
#================================================================================

Cross-correlate two data sets and produces a the cross-correlation function for
a given range of time lags. Uses the discrete method, whereby every data point
is cross-correlated with every other and the time lag is the actual difference
in time between the measurements, then these coefficients are binned. The cross-
correlation coefficents are calculated taking into account the poisson noise
error on each point on top of the intrinsic variation of the lightcurve.
Calculates SD and mean binwise.

"""

# import modules
import numpy as np

#========= Cross-Correlation Function ===========================================

def xcor(r,re,rt,x,xe,xt,nbins, t_lim = False,t_range = 300.):

        '''
        Function:
            Calculates the cross-correlation function for two data sets with
		   non-simultaneous data, using the discrete method - every data point
		   is cross-correlated with every point in the other data set, the time
		   lag is taken as the actual time difference between the measurements
		   and the coefficients are binned. Incorporates errors to remove
			non-intrisic variation. Works out stats binwise to avoid artefacts
			due to a trend in the ligthcurve.
        
        Arguments:
            
            r:       
                first data set - amplitudes (e.g. count rate or flux) - array
		   re:
		       first data set - errors on amplitudes
            rt:       
                first data set - times - array
            x:       
                second data set - amplitudes (e.g. count rate or flux) - array
		   xe:
		       second data set - errors on amplitudes
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
		
	# ----- calculate cross correlation coefficients (CCCs) ---------------------
	
	# create flux grids
	rflux 	= np.array([r for i in range(len(x))])	 # horizontal grid, radio flux
	rfluxerr = np.array([re for i in range(len(x))])	 # horizontal grid, radio errors
	xflux 	= np.array([x for j in range(len(r))]).T	 # vertical grid, xray flux
	xfluxerr 	= np.array([xe for j in range(len(r))]).T # vertical grid, xray flux	
	
	# create time grids, subtract to create lag grid
	rtime = np.array([rt for i in range(len(xt))])	# horizontal grid of radio times
	xtime = np.array([xt for j in range(len(rt))]).T	# vertical grid of xray times
	
	lag = rtime - xtime							# lag grid

	# ----- bin data in time ----------------------------------------------------

	# find time range, set up bin arrays
	if t_lim:
		tmin 	= -t_range						# lowest lag
		trange 	= t_range	*2						# time range

	else	:	
		tmin 	= min(lag)						# lowest lag
		trange 	= max(lag) - tmin					# time range
	
	wbin   	= trange / float(nbins)			# bin width

	# array for binned flux data - [[[rf],[re]],[[xf],[xe]]]] for each bin
	bfa    = [[[[],[]],[[],[]]] for i in range(nbins)]	
	ccxn   = np.zeros(nbins)					# number of points in each bin

	# bin data
	
	b  = ((lag - tmin - 1) / wbin ).astype(int) 			# array of bin indices
	b = b.reshape([1,len(x)*len(r)])[0]
	rflux = rflux.reshape([1,len(x)*len(r)])[0]
	xflux = xflux.reshape([1,len(x)*len(r)])[0]
	rfluxerr = rfluxerr.reshape([1,len(x)*len(r)])[0]
	xfluxerr = xfluxerr.reshape([1,len(x)*len(r)])[0]	
	
	for i in range(len(b)):
		if 0 <= b[i] < nbins:						# check if inside desired range

			bfa[b[i]][0][0].append(rflux[i])
			bfa[b[i]][0][1].append(rfluxerr[i])
			bfa[b[i]][1][0].append(xflux[i])
			bfa[b[i]][1][1] .append(xfluxerr[i])
			ccxn[b[i]] 	+= 1							# add count to bin 
	
	ccx = []
	
	bfa = np.array(bfa)		
	
	# calculate ccc array
	
	for j in range(nbins):
		if (ccxn[j] > 5):			
			rmean	= np.mean(bfa[j,0,0])
			rstd 	= np.std(bfa[j,0,0])
			rerrav	= np.mean(bfa[j,0,1])
			xmean 	= np.mean(bfa[j,1,0])
			xstd 	= np.std(bfa[j,1,0])
			xerrav	= np.mean(bfa[j,1,1])
			
			xerrav   = 0
			rerrav   = 0
						
#			if rstd < rerrav:
#				print "radio",rstd, rerrav
#			if xstd < xerrav: 
#				print "xray",xstd, xerrav
			xc = 0.		
			n  = 0.
			
			for k in range(len(bfa[j,0,0])):
				xc +=   ( (bfa[j,0,0][k]-rmean)*(bfa[j,1,0][k]-xmean) ) / \
					np.sqrt((rstd**2 - rerrav**2)*(xstd**2 - xerrav**2))		
			
				n += 1.		
			
			ccx.append(xc/n)
			
		else:
			ccx.append(0)
			ccxn[j] = 0

	# create time array corresponding to bins
	it = np.arange(nbins)
	tlag = it*wbin + tmin + 3
					
	return ccx, tlag , ccxn

