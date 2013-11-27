import numpy as numpy
import pylab as pylab

longlength   = 5120
psdindexLow  = 2.40
psdindexHigh = 1.00 
breakfreq    = 5.14e-5

# Create frequency array for the initial light curve, up to the Nyquist frequency
frequency = numpy.arange(1.0, longlength/2+1, 1.0)/longlength 

# define the power-law form of the PSD, i.e. a two-part law with a break
powerlaw = numpy.piecewise(frequency,  [frequency<=breakfreq, frequency>breakfreq], 
        	  [lambda frequency: (frequency/breakfreq)**(-psdindexLow) , 		
        	   lambda frequency: (frequency/breakfreq)**(-psdindexHigh) ])

pylab.plot(frequency,powerlaw)

pylab.show()
