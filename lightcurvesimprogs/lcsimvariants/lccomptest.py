# Import packages

from powerspeced import powcal, binps
from lcsimulationpure import lcsim
from pylab import *
import numpy as numpy

#============================================================================
# Creates many light curves and an average PSD and plots against a test curve 
#============================================================================


# variables
minb    =  4
ncurves =  10
bfac         = 1.0
psdindexlow  = 2.40
psdindexhigh = 1.00 
breakfreq    = 5.14e-5


# --- simulate and create an average powerspectrum from simulated light curves ------------

first = 1
print "Go!"

for curve in range(ncurves):

	# ------------ simulate curves -----------------------------

	lc  = lcsim(psdindexlow, psdindexhigh, breakfreq,curve) # simulate curve
	

	# ------------- calculate powerlaws -------------------------

	time = arange(1.0,float(len(lc)+1))
	dt=time[-1]-time[0] 
	df=1.0*(dt**(-1))
	avflux = numpy.mean(lc)
	dff   = []
	freq = []
	
	pl, npoints = powcal( df, time, lc, avflux)	

	for j in range(npoints):
		
		dff.append(pl[j])
		freq.append(df*(j+1))

	freq.append(freq[-1])

	lfreq, blff, blperr = binps(npoints,freq,dff,minb,bfac)
	print len(blff)
	if first == 1:

		lcpl  = zeros(len(blff))
		first = 0

	for data in range(len(lcpl)):

		lcpl[data] += blff[data]
	print "done", curve+1, "of", ncurves

lcpl = lcpl / ncurves

nfreq    = numpy.array([])
powerlaw = []

for n in range(len(lfreq)):

	nfreq= numpy.append(nfreq,10**lfreq[n]) 

# create comparison spectrum array
powerlaw = numpy.piecewise(nfreq,  [nfreq<=breakfreq, nfreq>breakfreq], 
        	   [lambda nfreq: (nfreq/breakfreq)**(-psdindexlow) , 		
        	    lambda nfreq: (nfreq/breakfreq)**(-psdindexhigh) ])

logpl    = []

for plog in range(len(powerlaw)):

	logpl.append((log10(powerlaw[plog])))
	 

plot(lfreq,logpl)
plot(lfreq,lcpl)


show()









