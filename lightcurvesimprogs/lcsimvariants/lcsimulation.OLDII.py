"""
lcsimulation.py

Created in November  2012

Author: Sam Connolly

#================================================================================
# 			Light Curve Simulation Code
#================================================================================

Produce an artificial lightcurve with the a given power spectral density in
frequency space, using the Timmer & Koenig (1995) method, assuming a broken
power law PSD.

"""

# Import packages

from pylab import *
import numpy as numpy

# ==================== Light Curve Simulation Function ==========================

def lcsim(psdindexLow,psdindexHigh,breakfreq,mean,sd,randomSeed):
	
	'''
	Function:
		Generates an artificial lightcurve with the a given power spectral 
		density in frequency space, using the Timmer & Koenig (1995) method,
		assuming a broken power law PSD.

	Arguments:
		psdindexLow:
			spectral index of low frequency end of PSD
		psdindexHigh:
			spectral index of high frequency end of PSD
		breakfreq:
			break frequency of PSD
		mean:
			mean amplitude (cnts/flux) of lightcurve to generate
		std:
			standard deviation of amplitude of lightcurve to generate
		randomSeed:
			random number seed

	Returns:
		normlightcurve:
			(array)    array of amplitude values (cnts/flux) with the same
					  timing properties as entered, length 1024 seconds,
					  sampled once per second.

                                                                
        '''                                  

	# lightcurve length

	length       =1024     	# length of final light curve (ideally 2^x)
	longlength   =length*10	# length of initial light curve (from which 
	
	# --------- Create power spectrum --------------------------------------

	# Create frequency array for initial light curve, up to the Nyquist freq
	frequency = numpy.arange(1.0, longlength/2+1, 1.0)/longlength 

	# define the power-law form of the PSD, i.e. a two-part law with a break
	powerlaw = numpy.piecewise(
		   frequency,  [breakfreq>=frequency, frequency>=breakfreq], 
            [lambda frequency: numpy.power(frequency,(-psdindexLow)), 		
       	     lambda frequency: numpy.power(breakfreq,(psdindexHigh-psdindexLow))
                             *numpy.power(frequency,(-psdindexHigh))])

	# -------- Create two arrays of gaussian-dist numbers for each freq

	np.random.seed(32+randomSeed)                               
	random1 = numpy.random.normal(0,1,(longlength/2))
	np.random.seed(891+randomSeed) 
	random2 = numpy.random.normal(0,1,(longlength/2))

	# -------- Add noise to the power law (PL) using the random numbers ----
	# (Multiply random no.s by the sqrt of half the PL value at each freq)

	real = (numpy.sqrt(powerlaw*0.5))*random1
	imag = (numpy.sqrt(powerlaw*0.5))*random2

	# ----- create array of Fourier components -----------------------------
	# (+ve values use arrays above, -ve values are conjugates of +ve ones)

	positive = numpy.zeros(longlength/2,complex)  # complex array +ve values
	negative = numpy.zeros(longlength/2,complex)  # complex array -ve values
                             
	for i in range(longlength/2):                                    

 		positive[i]=complex(real[i],imag[i]) # put values into +ve array
		negative[i]=positive[i].conjugate()  # put conjugates into -ve  
 	                         
	revnegative = negative[::-1]       	     # reverse negative array

	# join negative and positive arrays
                             
	noisypowerlaw = numpy.append(
		positive[0:longlength/2-1],revnegative[1:longlength/2+1])
	znoisypowerlaw = numpy.insert(noisypowerlaw,0,complex(0.0,0.0)) # add 0

	# --------- Fourier transform the noisy power law ----------------------

	inversefourier = numpy.fft.ifft(znoisypowerlaw)   
		       		# \(should consist ONLY of real numbers)

	longlightcurve = inversefourier.real  # take real part of the transform

	# chop the light curve to the desired length, defined by 'length'

	lightcurve = numpy.take(longlightcurve,
					range(longlength/2,length+longlength/2))

	# ---------- Normalise output lightcurve -------------------------------
	#  (To desired mean and standard deviation, given by sdCR and meanCR)

	normlightcurve = numpy.zeros(length-1)  
                                      
	for i in range(length-1):                                       

		normlightcurve[i] = ((longlightcurve[i]
	  -numpy.mean(longlightcurve))/numpy.std(longlightcurve) )  *sd+mean     

	return normlightcurve







