# Programme to test how a pivoting spectral component, plus a
# constant soft component changes the shape of the flux-flux diagram

import numpy as np
from pylab import *

# parameters
epivot 	  = 2.0		# KeV pivot energy
pivmin	  = 2.0
pivmax	  = 10.0
cindex    = 2.0		# index of constant component
nsteps    = 10.0

# constants

h = 6.63	# planck
e = 1.6e-19		# electron charge

# energy axis

energy    = np.arange(0.5,10.0,0.01)	# energy range of spectrum in KeV
logenergy = np.log(energy)				# log of energy
freq      = (energy*e*1000.0)/h			# frequency range in Hz



stepsize = (pivmax-pivmin)/nsteps
pivnorm = ( ((epivot*e*1000.0)/h)**pivmin)


fluxflux = [[],[],[]]

# plotting the log spectrum components

# constant component

cflux      = freq**(-cindex)			# constant flux component
logcflux   = np.log10(cflux) 			# log of constant flux

logvflux = []

# varying component

for piv in np.arange(pivmin,pivmax,stepsize):
	currvflux = (freq**(-piv))
	pnorm = (((epivot*e*1000.0)/h)**piv)
	currvflux = (currvflux/pnorm)*pivnorm
	logcurrvflux = np.log10(currvflux)			# log thereof
	logvflux.append(logcurrvflux)



# soft/hard delineaters

low    = [np.log(0.5),np.log10(0.5)]
div    = [np.log(2.0),np.log10(2.0)]
high   = [np.log(10.0),np.log10(10.0)]
yrange = [logcflux[-1],logvflux[-1][0]]

subplot(1,2,1)					# log spectrum plot
#plot(logenergy,logcflux,color="red")
plot(logenergy,logvflux[0],color="blue")
plot(logenergy,logvflux[len(logvflux)/2],color="blue")
plot(logenergy,logvflux[-1],color="blue")

#plot(low,yrange)
#plot(div,yrange)
#plot(high,yrange)

# total spectrum

subplot(1,2,2)
for x in [0,len(logvflux)/2,-1]:
	logtotal = logvflux[x] + logcflux
	plot(logenergy,logtotal)

show()
