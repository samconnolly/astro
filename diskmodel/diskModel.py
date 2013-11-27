# diskModel.py
"""
Created on Fri Oct 18 15:07:47 2013

author: Sam Connolly
"""
# Let's try and work out where the emission from the disk is coming from.
# Define UV as 100-400 nm and work out the radius within which 90% of it arises

# PARAMETERS ====================================================================

Mass	= 2e6	# Black hole mass in units of Msun
Macc	= 3.5e-2	# Mass accretion rate in units of Msun per year

#================================================================================

# modules
import numpy as np
import pylab as plt

# constants
Msun = 1.99e30
G	= 1.67e-11
c	= 3.0e8
h	= 6.67e-34
Kb	= 1.38e-23

Rg = (2.0*G*Mass)/c**2.0 # gravitational radii

# temperature at a given radius
def temp(M,Mdot,R): 

	return	(3.5e7) * (Mdot**(0.25)) * (M)**(-0.25) \
				* (R)**(-0.75) *(1.0 - ((3.0)/R))**(0.25)
				
# black body spectrum for a given temperature				
def planck(L, T):
	
	return ((2.0*h*(c**2.0)) / (L**5.0)) * (1.0 / (np.exp((h*c)/(L*Kb*T)) - 1.0))

# peak emission at a given temp
def wien(T):
	
	return 2.89776829e-6 / T

# work out the black body near the BH for reference

BB	 		= []
wavelengths	= []

for l in np.arange(1.0e-9,2.0e-7,1.0e-9):
	
	BB.append(planck(l,temp(Mass,Macc,3.8)))	# peak temp

	wavelengths.append(l)
	
# calculate total spectrum by adding black bodies at each radius*area,
# and find the UV emitted from each radius

indSpec= []
spec	 = np.zeros(len(wavelengths))
uv	 = np.zeros(len(wavelengths))

for r in np.arange(4.0,1000.0,1.0):	# for each radius

	t = temp(Mass,Macc,r)			# calculate temp

	each = np.array([])			

	for a in range(len(wavelengths)):
		value = planck(wavelengths[a],t)*2*np.pi*r*1.0  # multiply by area of anulus
		each = np.append(each,value) 				   # calculate intensity
		
	indSpec.append(each)		  

	spec += each # add to total
	
# calculate the temperature profile of the disk	
	
temps 	= []
maxTemps = []	
radii 	= []
	
for r in np.arange(3.1,1000.0,0.1):
	
	t = temp(Mass,Macc,r)
	temps.append(np.log10(t))
	maxTemps.append(wien(t))
	radii.append(r)

# work out where most of the UV comes from




# plot all of this

fig = plt.figure()

ax1 = fig.add_subplot(3,1,1)
#plt.plot(wavelengths,spec)
#plt.plot(wavelengths,indSpec[0])
plt.plot(wavelengths,indSpec[100])
plt.plot(wavelengths,indSpec[500])
plt.title("Spectrum")
plt.xlabel("Wavelength (m)")
plt.ylabel("Flux")

ax2 = fig.add_subplot(3,1,2)
plt.plot(radii,maxTemps)
plt.title("Peak emission wavelength")
plt.xlabel("Radius (Rg)")
plt.ylabel("Wavelength (m)")

ax3 = fig.add_subplot(3,1,3)
plt.plot(radii,temps)
plt.title("Disc temperature")
plt.xlabel("Radius (Rg)")
plt.ylabel("Log Temperature (K)")

plt.subplots_adjust(hspace=.6)

plt.show()











