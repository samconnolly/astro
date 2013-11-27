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
	''' calculate the disk temperature at a given radius (R) for a given mass (M)
		and accretion rate (Mdot)'''

	return	(3.5e7) * (Mdot**(0.25)) * (M)**(-0.25) \
				* (R)**(-0.75) *(1.0 - ((3.0)/R))**(0.25)
				
# black body spectrum for a given temperature				
def planck(L, T):
	'''calculate the emission at a given wavelength (L) of a black body
	at given temperature (T)''' 
	
	return ((2.0*h*(c**2.0)) / (L**5.0)) * (1.0 / (np.exp((h*c)/(L*Kb*T)) - 1.0))

# peak emission at a given temp
def wien(T):
	'''calculate the wavelength of peak emission for a black body of a given
	temperature (T)'''
	
	return 2.89776829e-6 / T

	
# calculate total spectrum by adding black bodies at each radius*area,
# and find the UV emitted from each radius

indSpec		= []

wavelengths	= np.arange(1.0e-9,2.0e-7,1.0e-9)
spec	 		= np.zeros(len(wavelengths))

radii 		= np.arange(3.1,1000.0,0.1)
uv	 		= np.zeros(len(radii))
uvTot		= 0


for r in range(len(radii)):	# for each radius

	t = temp(Mass,Macc,radii[r])			# calculate temp

	each = np.array([])			

	for a in range(len(wavelengths)):
		
		# calculate intensity at this wavelength, multiply by area of anulus
		value = planck(wavelengths[a],t)*2*np.pi*radii[r]*1.0  
		each = np.append(each,value) 				   

		if 10e-8 < wavelengths[a] < 4e-7:
			
			uv[r] += value	# Add UV emission at each radius
			uvTot += value    # Add to total UV emission
		
	indSpec.append(each)		  

	spec += each # add to total
	
uv /= uvTot # divide UV emission, to give a fraction of total UV

# Calculate the cumulative UV fraction at each radius

uvCum = np.zeros(len(radii))

uvCum[0] = uv[0]
found90 = False

for i in range(1,len(uv)):
	
	uvCum[i] = uv[i]+uvCum[i-1] # cumulatively add UV emission fraction
	
	if uvCum[i] > 0.9 and found90 == False:
		
		found90 = True
		print "90% of UV emission from within {0} Rg".format(radii[i])

# calculate the temperature profile of the disk	
	
temps 	= []
maxTemps = []	

	
for r in radii:
	
	t = temp(Mass,Macc,r)
	temps.append(np.log10(t))
	maxTemps.append(wien(t))

# plot all of this

fig = plt.figure()

ax1 = fig.add_subplot(3,2,1)
plt.plot(wavelengths,spec)
plt.plot(wavelengths,indSpec[0])
plt.plot(wavelengths,indSpec[10])
plt.plot(wavelengths,indSpec[50])
plt.title("Spectrum")
plt.xlabel("Wavelength (m)")
plt.ylabel("Flux")

ax2 = fig.add_subplot(3,2,2)
plt.plot(radii,maxTemps)
plt.title("Peak emission wavelength")
plt.xlabel("Radius (Rg)")
plt.ylabel("Wavelength (m)")

ax3 = fig.add_subplot(3,2,3)
plt.plot(radii,temps)
plt.title("Disc temperature")
plt.xlabel("Radius (Rg)")
plt.ylabel("Log Temperature (K)")

ax3 = fig.add_subplot(3,2,4)
plt.plot(radii[:100],uv[:100])
plt.title("Disk UV emission")
plt.xlabel("Radius (Rg)")
plt.ylabel("UV fraction")

ax3 = fig.add_subplot(3,2,5)
plt.plot(radii[:500],uvCum[:500])
plt.title("Cumulative disk UV emission")
plt.xlabel("Radius (Rg)")
plt.ylabel("Cumulative UV fraction")

plt.subplots_adjust(hspace=.6)

plt.show()











