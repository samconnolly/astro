
# diskModel.py
"""
Created on Fri Oct 18 15:07:47 2013

author: sdc1g08
"""
# Let's try and work out where the emission from the disk is coming from

# PARAMETERS ====================================================================

Mass	= 2e6	# Black hole mass in units of Msun
Macc	= 3.5e-2	# Mass accretion rate in units of Msun per year

#================================================================================

import numpy as np
import pylab as plt

# set up temperature calculation
#Msun = 1.99e30
G	= 1.67e-11
c	= 3.0e8
h	= 6.67e-34
Kb	= 1.38e-23

Rg = (2.0*G*Mass)/c**2.0

def temp(M,Mdot,R): 

	return	(3.5e7) * (Mdot**(0.25)) * (M)**(-0.25) \
				* (R)**(-0.75) *(1.0 - ((3.0)/R))**(0.25)
				
def planck(L, T):
	
	return ((2.0*h*(c**2.0)) / (L**5.0)) * (1.0 / (np.exp((h*c)/(L*Kb*T)) - 1.0))

def wien(T):
	
	return 2.89776829e-6 / T




BB1	 		= []
BB2	 		= []
BB3	 		= []
wavelengths	= []

for l in np.arange(1.0e-9,5.0e-6,1.0e-9):
	
	BB1.append(planck(l,temp(Mass,Macc,3.8)))	# peak temp
	BB2.append(planck(l,temp(Mass,Macc,100.0)))	# mid temp
	BB3.append(planck(l,temp(Mass,Macc,1000.0)))	# low temp
	wavelengths.append(l)
	

	
temps 	= []
maxTemps = []	
radii 	= []
	
for r in np.arange(3.1,1000.0,0.1):
	
	t = temp(Mass,Macc,r)
	temps.append(np.log10(t))
	maxTemps.append(wien(t))
	radii.append(r)



fig = plt.figure()

ax1 = fig.add_subplot(4,1,1)

plt.plot(wavelengths,BB1)
plt.plot(wavelengths,BB2)
plt.plot(wavelengths,BB3)

ax2 = fig.add_subplot(4,1,2)
#plt.plot(radii,temps)
plt.plot(wavelengths,BB2)
ax3 = fig.add_subplot(4,1,3)
#plt.plot(radii,maxTemps)
plt.plot(wavelengths,BB3)
ax4 = fig.add_subplot(4,1,4)

plt.show()