# jimDisk.py
"""
Created on Wed Oct 23 12:05:41 2013

Author: Sam Connolly
"""

# disk model using James Matthews' code... let's see if it's any different to mine.

from disk_ED import *
from disky_const import *
import pylab as plt

#freq, spec, allSpec,uv ,uvCum, radii = \
#spec_disk_more(1e15,1e18,1e6,mdot_from_edd(0.02,1e6),3.1*Schwarz(1e6),1000.*Schwarz(1e6),1000,100)

print mdot_from_edd(0.02,1e6)*2e33

freq, spec, allSpec,uv ,uvCum, radii = \
spec_disk_more(1e13,2e16,1e6,mdot_from_edd(0.02,1e6),3.1*Schwarz(1e6),1000.*Schwarz(1e6),1000,100)

temps  = []

td = tdisk(1e6,mdot_from_edd(0.02,1e6),3.*Schwarz(1e6))

radii /= Schwarz(1e6)

for r in radii: 
	temps.append(np.log10(teff(td,r/3.1)))
	
# plot all of this

fig = plt.figure()

ax1 = fig.add_subplot(3,2,1)
plt.plot(freq,spec)
plt.title("Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Flux")

#ax2 = fig.add_subplot(3,2,2)
#plt.plot(radii,maxTemps)
#plt.title("Peak emission wavelength")
#plt.xlabel("Radius (Rg)")
#plt.ylabel("Wavelength (m)")

ax3 = fig.add_subplot(3,2,3)
plt.plot(radii,temps)
plt.title("Disc temperature")
plt.xlabel("Radius (Rg)")
plt.ylabel("Log Temperature (K)")

ax3 = fig.add_subplot(3,2,4)
plt.plot(radii[:50],uv[:50])
plt.title("Disk UV emission")
plt.xlabel("Radius (Rg)")
plt.ylabel("UV fraction")

ax3 = fig.add_subplot(3,2,5)
plt.plot(radii[:50],uvCum[:50])
plt.title("Cumulative disk UV emission")
plt.xlabel("Radius (Rg)")
plt.ylabel("Cumulative UV fraction")

plt.subplots_adjust(hspace=.6)

plt.show()

plt.show()