# Programme to test how a changing amount of a hard spectral component, plus a # translated constant soft component changes the shape of the flux-flux diagram

import numpy as np
from pylab import *

# parameters

cindex = 2.0	# index of constant component
vindex = -2.0
normmin  = -122.0
normmax  = -120.0
nsteps   = 30.0

# constants

h = 6.63e-34	# planck
e = 1.6e-19		# electron charge

# energy axis

energy    = np.arange(0.5,10.0,0.01)	# energy range of spectrum in KeV
logenergy = np.log(energy)			# log of energy
freq      = (energy*e*1000.0)/h			# frequency range in Hz

# flux intergral function

def fluxint(cindex,vindex,norm):

	soft = ( ((2.0*e*1000.0)/h)**(1.0 - cindex) )/(1.0-cindex) \
			- ( ((0.5*e*1000.0)/h)**(1.0 - cindex) )/(1.0-cindex) \
\
			  + ( ( ((2.0*e*1000.0)/h)**(1.0 - vindex) )/(1.0-vindex) \
				- ( ((0.5*e*1000.0)/h)**(1.0 - vindex) )/(1.0-vindex) )\
				  *(1e50)*(10.0**norm)
			
	hard = ( ((10.0*e*1000.0)/h)**(1.0 - cindex) )/(1.0-cindex) \
		- ( ((2.0*e*1000.0)/h)**(1.0 - cindex) )/(1.0-cindex) \
\
		  + ( ( ((10.0*e*1000.0)/h)**(1.0 - vindex) )/(1.0-vindex) \
			- ( ((2.0*e*1000.0)/h)**(1.0 - vindex) )/(1.0-vindex) )\
				  *(1e50)*(10.0**norm)

	return soft, hard

# integration to find soft and hard components at each flux

stepsize = (normmax-normmin)/nsteps

intnormsoft, intnormhard = fluxint(cindex,vindex,normmax)
intnorm = intnormsoft + intnormhard

fluxflux = [[],[],[]]

for norm in np.arange(normmin,normmax,stepsize):
	soft, hard = fluxint(cindex,vindex,norm)
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
logcflux   = np.log10(cflux) 				# log of constant flux


# varying component and total spectrum

vflux	 = []
logvflux = []
tflux	 = []
logtflux = []

for norm in np.arange(normmin,normmax,stepsize):
	currvflux = (freq**(-vindex))*(1e50)*(10.0**(norm))
	vflux.append(currvflux)
	logcurrvflux = np.log10(currvflux)			# log thereof
	logvflux.append(logcurrvflux)
	tflux.append(cflux + currvflux)
	logtflux.append(log10(cflux + currvflux))


subplot(3,2,1)							# spectrum plot
title("spectrum components")
plot(energy,cflux,color="red")

for x in  range(len(vflux)):
	plot(energy,vflux[x],color="blue")

subplot(3,2,2)							# log spectrum plot
title("log spectrum components")
plot(logenergy,logcflux,color="red")

for x in range(len(logvflux)):
	plot(logenergy,logvflux[x],color="blue")

subplot(3,2,3)							# total spectrum
title("total spectrum")
for x in range(len(tflux)):
	plot(energy,tflux[x],color="blue")

subplot(3,2,4)							# log total spectrum
title("log total spectrum")
for x in range(len(logtflux)):
	plot(logenergy,logtflux[x],color="blue")

subplot(3,2,5)					# flux flux plot (H v S)

title("flux v flux")
plot(fluxflux[0],fluxflux[1])

subplot(3,2,6)					# hardness-flux plot (H flux)

title("hardness v flux")
plot(fluxflux[0],fluxflux[2])

show()
