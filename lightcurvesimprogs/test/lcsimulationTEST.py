"""
lcsimulation.py

Created in November  2012

Author: Sam Connolly

TESTING - IS THE PSD OF THE OUTPUT CURVE THE SAME AS THE INPUT CURVE?

#================================================================================
# 			Light Curve Simulation Code
#================================================================================

Produce an artificial lightcurve with the a given power spectral density in
frequency space, using the Timmer & Koenig (1995) method, assuming a broken
power law PSD.

"""

# Import packages
import numpy as np
import pylab as plt
import matplotlib
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
		lightcurve:
			(array)    array of amplitude values (cnts/flux) with the same
					  timing properties as entered, length 1024 seconds,
					  sampled once per second.

                                                                
        '''                                  

	# lightcurve length

	length       = 1024     	# length of final light curve (ideally 2^x)
	longlength   = length*10	# length of initial light curve  
	
	# --------- Create power spectrum -------------------------------------------

	# Create frequency array for initial light curve, up to the Nyquist freq
	frequency = np.arange(1.0, longlength/2+1, 1.0)/longlength 

	# define the power-law form of the PSD, i.e. a two-part law with a break
	powerlaw = np.piecewise(
		   frequency,  [breakfreq>=frequency, frequency>=breakfreq], 
            [lambda frequency: np.power(frequency,(-psdindexLow)), 		
       	     lambda frequency: np.power(breakfreq,(psdindexHigh-psdindexLow))
                             *np.power(frequency,(-psdindexHigh))])

	# -------- Create two arrays of gaussian-dist numbers for each freq ---------

	np.random.seed(32+randomSeed)                               
	random1 = np.random.normal(0,1,(longlength/2))
	np.random.seed(891+randomSeed) 
	random2 = np.random.normal(0,1,(longlength/2))

	# -------- Add noise to the power law (PL) using the random numbers ----
	# (Multiply random no.s by the sqrt of half the PL value at each freq)

	real = (np.sqrt(powerlaw*0.5))*random1
	imag = (np.sqrt(powerlaw*0.5))*random2

	# ----- create array of Fourier components ----------------------------------
	# (+ve values use arrays above, -ve values are conjugates of +ve ones)


	positive = np.vectorize(complex)(real,imag) # array of positive, complex no.s
	negative = positive.conjugate()             # array of negative complex no.s
	
	revnegative = negative[::-1]       	        # reverse negative array

	# join negative and positive arrays
                             
	noisypowerlaw = np.append(
		positive[0:longlength/2-1],revnegative[1:longlength/2+1])
	znoisypowerlaw = np.insert(noisypowerlaw,0,complex(0.0,0.0)) # add 0

	# --------- Fourier transform the noisy power law ---------------------------

	inversefourier = np.fft.ifft(znoisypowerlaw)   
		       		# \(should consist ONLY of real numbers)

	fig = plt.figure()
	
	ax = fig.add_subplot(1,1,1)
	#ax.set_yscale('log')
	ax.set_xscale('log')

	print np.append(-frequency[::-1],0),frequency
	zfreq =  np.append(np.append(-frequency[::-1],0), frequency)
	print zfreq
	print len(zfreq),len(znoisypowerlaw)
	plt.plot(zfreq,znoisypowerlaw)
	#plt.plot(frequency,powerlaw)
	plt.show()


	longlightcurve = inversefourier.real  # take real part of the transform

	# chop the light curve to the desired length, defined by 'length'

	lightcurve = np.take(longlightcurve,
					range(longlength/2,length+longlength/2)) # take from middle

	# ---------- Normalise output lightcurve ------------------------------------
	#  (To desired mean and standard deviation, given by sd and mean)

	lightcurve = (lightcurve-np.mean(lightcurve))/np.std(lightcurve)*sd+mean
	
	return lightcurve,longlightcurve,frequency,powerlaw
	
#psdindexlow  = 2.40		# PSD low frequecy spectral index...
#psdindexhigh = 1.00 		# ... and high frequency spectral index
#psdbrkfreq   = 5.14e-5

breakfreq     = 0.1
psdindexLow   = 1.0
psdindexHigh  = 2.0

lightcurve,longlc,frequency,powerlawout = \
 lcsim(psdindexLow,psdindexHigh,breakfreq,1.0,1.0,3)
	
#longlc = np.fft.fft(np.take(longlc,range( len(longlc)/4 -1,3*(len(longlc)/4) + 1) ) )
#
#fig = plt.figure()
#
#ax = fig.add_subplot(1,1,1)
##ax.set_yscale('log')
#ax.set_xscale('log')
#
#plt.plot(frequency,longlc)
#plt.plot(frequency,powerlawout)
#plt.show()
#
## shorten frequency range to same length as sim lightcurve
#
#frequency   = np.take(frequency,range(0,len(lightcurve)))
#powerlawout = np.take(powerlawout,range(0,len(lightcurve)))
#
## define the power-law form of the PSD, i.e. a two-part law with a break
#powerlaw = np.piecewise(
#	frequency,  [breakfreq>=frequency, frequency>=breakfreq], 
#	[lambda frequency: np.power(frequency,(-psdindexLow)), 		
#	lambda frequency: np.power(breakfreq,(psdindexHigh-psdindexLow))
#            *np.power(frequency,(-psdindexHigh))])
#
## plot
#fig = plt.figure()
#
#ax = fig.add_subplot(1,1,1)
##ax.set_yscale('log')
#ax.set_xscale('log')
#
#psd = np.fft.fft(lightcurve)
#
#for x in range(99):
#	psd += np.fft.fft(lightcurve)
#
#psd /= x+2
#
#ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
#
#print len(frequency),len(psd)
#plt.plot(frequency,psd)
#plt.plot(frequency,powerlaw)
#plt.plot(frequency,powerlawout)
#plt.show()






