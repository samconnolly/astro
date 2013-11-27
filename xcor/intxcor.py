"""
intxcorcall.py

Created in November  2012

Author: Sam Connolly


#=====================================================================
# interpolating cross-correlation programme
#=====================================================================

cross-correlate two signals, using interpolation.

"""

def xcor(r,rt,x,xt,t_start,t_end):

                        
        '''
        Function:
            Calculates the cross-correlation function for two data sets with
		   	non-simultaneous data, using the interpolative method - one data set
			has a range of time lags applied and is cross-correlated with the
			second data set, by interpolating a value at equivalent times.
        
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
				lower limit of lags to apply (usually negative)
			t_end:
				upper limit of lags to apply
                                                                                                                                                
        Returns:
                	ccf:        
                         (array)    Cross-correlation function
  					tlag:        
                         (array)    time lags corresponding to the CCF
					npoints
                         (array)    array of the number of data points 
									used for a given lag
	     '''    

	# function arrays
	ccf      = []
	tlag     = []
	npoints	= []

	# averages
	rav  = np.mean(r)
	xav  = np.mean(x)

	# standard deviations

	rsd  = np.std(r)
	xsd  = np.std(x)

	#-----calculate cross correlation function-------------


	for t in range(t_start, t_end):

		ccx   = 0.
		n     = 0.

		for e in range(len(xt)):

			# check for values outside the time range of the radio data
			if (xt[e] + t) < rt[-1] and  (xt[e] + t) > rt[1]:

				# find two closest radio times to the xray time 

				postdif= ( xt[e] + t ) - rt[ 1] 
				negtdif= ( xt[e] + t ) - rt[-1] 
				low  = 0
				high = 0

				for f in range(len(rt)):
	
					dif= (xt[e] + t) - rt[f]

					if dif >= 0:
						if dif <= postdif:
							low = f
							postdif=rt[f]

					if dif < 0:

						if dif >= negtdif:
							high = f
							negtdif=rt[f]

	
				# interpolate single value

				intval= r[low] + ( (r[high] - r[low]) \
					/ (rt[high] - rt[low]))*((xt[e] + t) - rt[low])


				# calculate correlation value

				ccx += ( (intval-rav)*(x[e]-xav) ) / (rsd*xsd) 
	
				# counts points used
				n += 1.
	

		# append final arrays with normalised correlation values
		if ccx!= 0:
			ccf.append(ccx/n)
			npoints.append(n)
			tlag.append(t)
		
	return ccf,tlag, npoints

