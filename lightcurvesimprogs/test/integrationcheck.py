import numpy as numpy
import scipy.integrate

#==========================================================================================
# check integration of powerlaw is valid
#==========================================================================================


# variables


psdindexlow  = 3.00	# low frequency power spectral index
psdindexhigh = 2.00 	# high frequency power spectral index
breakfreq    = 0.75e-2  # break frequency
length       = 512	# number of points in lightcurve

# frequency and powerlaw arrays

ofreq = numpy.arange(1.0, (length*10)/2+1, 1.0)/(length*10)

ipl = numpy.piecewise(ofreq,  [ofreq<=breakfreq, ofreq>breakfreq], 
        	   [lambda ofreq: (ofreq)**(-psdindexlow) , 		
        	    lambda ofreq: ((ofreq)**(-psdindexhigh))*((breakfreq)**(-psdindexlow+psdindexhigh)) ])

sd = scipy.integrate.simps(ipl,ofreq)
sd2 = numpy.trapz(ipl,ofreq)

if psdindexlow != 1.0:
	int1 = ( ( (breakfreq)**(1.0-psdindexlow) ) / (1.0 - psdindexlow) ) - ( ( (1.0/(length*10) )**(1.0-psdindexlow) )/(1.0 - psdindexlow) )

if psdindexhigh != 1.0:
	int2 = (( ( (1.0/2.0)**(1.0-psdindexhigh) )/(1.0 - psdindexhigh) ) - ( ( (breakfreq)**(1.0-psdindexhigh) )/(1.0 - psdindexhigh) ))\
		* (breakfreq**(psdindexhigh-psdindexlow))

if psdindexlow == 1.0:
	int1 = ( numpy.log(breakfreq) - numpy.log(1.0/(length*10)) )

if psdindexhigh == 1.0:
	int2 = ( numpy.log(1.0/2.0) - numpy.log(breakfreq) )

sd3 = int1+int2
print int1, int2
print sd, sd2, sd3

