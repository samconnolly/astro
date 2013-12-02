# Import packages

from powerspeced import powcaled, binps
from lcsimulationpureNONOISE import lcsim
from pylab import *
import numpy as numpy
import scipy.integrate

#==========================================================================================
# Creates many light curves and an average PSD and plots against a test curve [and real data]
#==========================================================================================


# variables

ncurves      = 20     # number of curves to simulate
psdindexlow  = 1.00	# low frequency power spectral index
psdindexhigh = 5.00 	# high frequency power spectral index
breakfreq    = 0.75e-1  # break frequency
bwidth       = 1.0	# bin width
mean         = 1.0	# lightcurve mean
length       = 512	# number of points in lightcurve

# --- simulate and create an average powerspectrum from simulated light curves ------------

first = 1
print "Go!"

ofreq = numpy.arange(1.0, (length*10)/2+1, 1.0)/(length*10)

ipl = numpy.piecewise(ofreq,  [ofreq<=breakfreq, ofreq>breakfreq], 
        	   [lambda ofreq: (ofreq)**(-psdindexlow) , 		
        	    lambda ofreq: ((ofreq)**(-psdindexhigh)) * ( (breakfreq)**(psdindexhigh-psdindexlow) ) ])

ologpl    = []
olf       = []

for oplog in range(len(ipl)):

	ologpl.append((log10(ipl[oplog])))
	olf.append((log10(ofreq[oplog])))

# integrate powerlaw to find requires standard deviation for lightcurve

if psdindexlow != 1.0:
	int1 = ( ( (breakfreq)**(1.0-psdindexlow) ) / (1.0 - psdindexlow) ) - ( ( (1.0/(length*10) )**(1.0-psdindexlow) )/(1.0 - psdindexlow) )

if psdindexhigh != 1.0:
	int2 = (( ( (1.0/2.0)**(1.0-psdindexhigh) )/(1.0 - psdindexhigh) ) - ( ( (breakfreq)**(1.0-psdindexhigh) )/(1.0 - psdindexhigh) ))\
		* (breakfreq**(psdindexhigh-psdindexlow))

if psdindexlow == 1.0:
	int1 = ( numpy.log(breakfreq) - numpy.log(1.0/(length*10)) )

if psdindexhigh == 1.0:
	int2 = ( numpy.log(1.0/2.0) - numpy.log(breakfreq) )


sd1= scipy.integrate.simps(ipl,ofreq) # compare to simpsons rule numerical integration
sd= int1 +int2
print sd, sd1

for curve in range(ncurves):

	# ------------ simulate curves -----------------------------

	lc, testpl,pos  = lcsim(psdindexlow, psdindexhigh, breakfreq,curve, sd, mean,length) # simulate curve
	print np.std(lc), np.mean(lc)
	# ------------- calculate powerlaws -------------------------

	time = arange(1.0,float(len(lc)+1))

	dff   = []
	freq = []
	dt= time[-1]-time[0]
	df= dt**(-1)
	avflux = numpy.mean(lc)
 

	pl, npoints = powcaled(lc)	

	for j in range(npoints):
		
		dff.append(pl[j])
		freq.append(df*(j+1))

	freq.append(freq[-1])

	lfreq, blff = binps(npoints,freq,dff)

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
        	    [lambda nfreq: (nfreq)**(-psdindexlow) , 		
        	    lambda nfreq: ((nfreq)**(-psdindexhigh))*((breakfreq)**(-psdindexlow+psdindexhigh)) ])

logpl    = []

for plog in range(len(powerlaw)):

	logpl.append((log10(powerlaw[plog])))

ltestpl       = []
lpos	      = []

for lplog in range(len(testpl)):

	ltestpl.append(log10(testpl[lplog]))
	lpos.append(log10(pos[lplog]))

residuals = np.array([])

for res in range(len(logpl)):
	
	residuals = np.append(residuals, logpl[res] - lcpl[res])

rav = np.mean(residuals)
print rav	 
subplot(3,1,1)
plot(lfreq,logpl)
plot(lfreq,lcpl)
subplot(3,1,2)
plot(lfreq,residuals)
subplot(3,1,3)
plot(olf,ltestpl)
plot(lfreq,lcpl)
plot(olf,lpos)
show()









