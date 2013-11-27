# Import packages

from pylab import *
import numpy as numpy

#============================================================================
# Creates many light curves and an average PSD and plots against a test curve 
#============================================================================


# variables
psdindexlow  = 2.00
psdindexhigh = 4.00 
breakfreq    = 5.14e-3

# create frequency array
freq = numpy.arange(1.0e-5, 0.5,1.0e-5)

# create comparison spectrum array
powerlaw = numpy.piecewise(freq,  [freq<=breakfreq, freq>breakfreq], 
        	   [lambda freq: (freq/breakfreq)**(-psdindexlow) , 		
        	    lambda freq: (freq/breakfreq)**(-psdindexhigh) ])

lfreq     = numpy.log10(freq)
lpowerlaw = numpy.log10(powerlaw)

# create comparison spectrum array 2
powerlaw2 = numpy.piecewise(freq,  [freq<=breakfreq, freq>breakfreq], 
        	   [lambda freq: (freq)**(-psdindexlow) , 		
        	    lambda freq: ((freq)**(-psdindexhigh))*(breakfreq**(-psdindexlow+psdindexhigh)) ])

lpowerlaw2 = numpy.log10(powerlaw2)

plot(lfreq,lpowerlaw,color="red")
plot(lfreq,lpowerlaw2,color="blue")

show()


