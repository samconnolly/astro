import numpy as np
import pylab as pl
from fiddlepowerspec import *

dt = 8.0*np.pi
bsize = 0.1
time = np.arange(0.0,dt,bsize)
df    = 1.0/dt
minb  = 1

flux = np.sin(time) + 2*np.sin(time*3) + 3*np.sin(time*5) + 6	# test lightcurve
swindow = np.array([1 for n in range(int(dt/bsize))])		# test spectral window

avflux = np.mean(flux) # calculate average flux from test lightcurve
sdflux = np.std(flux)  # calculate standard deviation of flux from test lightcurve

# print mean, SD and fractional rms
print "lightcurve mean =", avflux
print "lightcurve variance =", sdflux**2
print "The fractional rms =", sdflux**2/avflux**2

# fourier transform test LC and spectral window
fourier, points    = powcal(bsize, df, time, flux, avflux)
swfourier, spoints = spowcal( bsize, df, time, swindow, 0)

freq     = []
sfreq     = []

# create frequency arrays
for j in range(points):
		
	freq.append(df*(j))

for k in range(spoints):
		
	sfreq.append(df*(k))

# calculate integrals of peaks and total function
totarea = 0

for n in range(1,len(fourier)):

	if fourier[n] > fourier[n-1]*2:

		base = freq[n+1]-freq[n-1]
		area = base * fourier[n] * 0.5
		totarea += area

		print "area of peak at freq", freq[n], "=", area
		print "height", fourier[n]

print "total area =", totarea
print "fractional rms / area =", (sdflux**2/avflux**2)/totarea

# plot
pl.subplot(1,2,1)
pl.plot(time, flux)

pl.subplot(1,2,2)
pl.plot(freq, fourier)

#pl.show()

