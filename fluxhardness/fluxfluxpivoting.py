# Programme to test how a pivoting spectral component, plus a
# constant soft component changes the shape of the flux-flux diagram

import numpy as np
from pylab import *

# parameters
epivot 	  = 20.0	# KeV pivot energy
pivmin	  = -1.0		# min. pivot gradient
pivmax	  = -5.0	# max. pivot gradient
cindex    = 5.0		# index of constant component
nsteps    = 30.0	# no. steps
nom 	  = 7e+69

stepsize = (pivmax-pivmin)/nsteps	# calculate stepsize

# constants

h = 6.63		# planck (WRONG)
e = 1.6e-19		# electron charge

# energy axis

energy    = np.arange(0.5,10.01,0.01)	# energy range of spectrum in KeV
logenergy = np.log(energy)				# log of energy
freq      = (energy*e*1000.0)/h			# frequency range in Hz

# flux intergral function

def fluxint(cindex,vindex,norm):

	pnorm = (((epivot*e*1000.0)/h)**(-vindex))	# keep pivot flux constant

	soft = ( ( ((2.0*e*1000.0)/h)**(1.0 - cindex) )/(1.0-cindex) \
			- ( ((0.5*e*1000.0)/h)**(1.0 - cindex) )/(1.0-cindex) ) \
\
			  + ( ( ((2.0*e*1000.0)/h)**(1.0 - vindex) )/(1.0-vindex) \
				- ( ((0.5*e*1000.0)/h)**(1.0 - vindex) )/(1.0-vindex) )\
				  *(pivnorm/pnorm)

				
			
	hard = ((((10.0*e*1000.0)/h)**(1.0 - cindex))/(1.0-cindex) \
		- (((2.0*e*1000.0)/h)**(1.0 - cindex))/(1.0-cindex)) \
\
		  + ((((10.0*e*1000.0)/h)**(1.0 - vindex))/(1.0-vindex) \
			- (((2.0*e*1000.0)/h)**(1.0 - vindex))/(1.0-vindex))\
				  *(pivnorm/pnorm)

	return soft, hard

# some normalisation to make numbers less silly

pivnorm = ( ((epivot*e*1000.0)/h)**pivmin)*nom # easy-numbers normalisation

intnormsoft, intnormhard = fluxint(cindex,pivmax,pivnorm) # more normalisation..
intnorm = intnormsoft + intnormhard

# integration to find soft and hard components at each flux 

fluxflux = [[],[],[]]

for piv in np.arange(pivmin,pivmax + stepsize,stepsize):
	soft, hard = fluxint(cindex,piv,pivnorm)
	soft = soft/intnorm
	hard = hard/intnorm
	fluxflux[0].append(hard)
	fluxflux[1].append(soft)

# calculate hardness (H-S/H+S)

for flux in range(len(fluxflux[0])):
	hardness = (fluxflux[0][flux]-fluxflux[1][flux])/ \
				(fluxflux[0][flux]+fluxflux[1][flux])						
	fluxflux[2].append(hardness)



# plotting the log spectrum components

# constant component

cflux      = freq**(-cindex)			# constant flux component
logcflux   = np.log10(cflux) 			# log of constant flux

# varying component

logvflux = []
vflux = []
tflux = []
testhard = [[],[]]

for piv in np.arange(pivmin,pivmax + stepsize,stepsize):
	currvflux = (freq**(-piv))
	pnorm = (((epivot*e*1000.0)/h)**(-piv))
	currvflux = currvflux*(pivnorm/pnorm)
	vflux.append(currvflux)
	currtflux = cflux + currvflux
	tflux.append(currtflux)				# total flux
	ts = np.trapz(currtflux[:150])
	th = np.trapz(currtflux[150:])
	testhard[0].append(th)
	thardness = (th-ts)/(th+ts) 
	testhard[1].append(thardness)
	logcurrvflux = np.log10(currvflux)			# log thereof
	logvflux.append(logcurrvflux)

logfluxflux = np.log(fluxflux)

# plots

# Overall plots title
suptitle("Spectral variation for a pivoting powerlaw\n \
Pivot energy: {0}    Min./max. gradient of varying component: {1}/{2}\
     Gradient of constant component: {3}".format(epivot,pivmin,pivmax,cindex) )

subplot(3,2,1)					#  spectrum plot
title("spectrum components")
plot(energy,cflux,color="red")

for n in range(len(logvflux)):
	plot(energy,vflux[n],color="blue")

subplot(3,2,2)					# log spectrum plot
title("log spectrum componenets")
plot(logenergy,logcflux,color="red")

for n in range(len(vflux)):
	plot(logenergy,logvflux[n],color="blue")

subplot(3,2,3)					# total spectrum
title("total spectrum")
for x in range(len(tflux)):
	plot(energy,tflux[x],color="blue")


subplot(3,2,4)					# log total spectrum
title("log total spectrum")
for x in range(len(tflux)):
	logtotal = np.log10(tflux[x])
	plot(logenergy,logtotal,color="blue")

subplot(3,2,5)					# flux flux plot (H v S)
title("flux v. flux")
plot(fluxflux[0],fluxflux[1])

subplot(3,2,6)					# hardness-flux plot (H flux)
title("Hardness v. flux")
plot(fluxflux[0],fluxflux[2])
#plot(testhard[0],testhard[1])

show()
