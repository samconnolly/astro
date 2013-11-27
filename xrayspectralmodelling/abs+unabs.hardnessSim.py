# abs+unabs.hardnessSim.py
# Sam Connolly 19/02/2013

#===============================================================================
# calculate hardness of a spectrum with given parameters (abs + unabs PL)
#===============================================================================

# Import packages

from pylab import *
import matplotlib
import numpy as np

#================ PARAMETERS ===================================================

index = 1.566		 # Power law index for both power laws

norm = 7.58E-3	 # normalisation for absorbed power law
norm2 = 4.3E-4	 # normalisation for unabsorbed power law

nH = 0.0138	     # equivalent Hydrogen column density in 10^24 cm^-2
		

softmin = 0.5    # bottom energy of soft energy range (keV)
divide  = 2.0	 # dividing energy between soft and hard (keV)
hardmax = 10.0	 # top energy of hard energy range (keV)

galabs = True # add galactic absorption?
gnH = 1.39E-4 # galactic column density in 10^24 cm^-2

gauss = True # add a gaussian?

gE = 0.776  # gaussian central energy
gS = 0.157	# gaussian line width
gN = 1.775E-04	# gaussian normalisation
  
comp = True # compare to Xspec model data?

#========== Comparison file paramaters =========================================

mroute            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/"\
						+"ngc1365/spectra/summed/"

mfilename = "modeldata1.dat"

#========== Absorption parameter file ==========================================

# read variables
header = 1 # number of header lines to ignore
mheader = 1 # number of model header lines to ignore

#   File routes
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/"\
						+"xraySpectralModelling/"

# file names
infilename 	= "absorptionXsections.dat"

#===============================================================================

# create file routes
location  = route+infilename
mlocation  = mroute+mfilename
# read data intoarray

Emin = []
Emax = []
c0   = []
c1   = []
c2   = []

infile= open(location, 'r')

start = 0

for line in infile:
	
	if start >= header:

		cEmin, cEmax, cc0, cc1, cc2 = line.split()

		Emin.append(float(cEmin))
		Emax.append(float(cEmax))
		c0.append(float(cc0))
		c1.append(float(cc1))
		c2.append(float(cc2))

	start += 1

infile.close()

print 'Energy range: ',Emin[0], ' --> ',Emax[-1]

mfile= open(mlocation, 'r')

start = 0

menergy = []
mflux 	= []

for line in mfile:
	
	if start >= mheader:

		energy, flux = line.split()

		menergy.append(float(energy))
		mflux.append(float(flux))


	start += 1

mfile.close()

#============ Energy range =====================================================

energy = np.arange(softmin,hardmax,0.01)

#============= Cross sections - (c0 + c1*E + c2*E^2)*E^-3 ======================

xsec = np.array([])

for e in range(len(energy)):

	i = 0
	high = len(Emax)-1

	if energy[e] <= Emax[high]:
		while energy[e] > Emax[i]:
			i += 1

		xsec = np.append(xsec, ( c0[i] + c1[i]*energy[e]\
						 + c2[i]*(energy[e]**2) ) * (energy[e]**(-3)) )
		
	else:
		i = high
		xsec = np.append(xsec, ( c0[i] + c1[i]*energy[e]\
						 + c2[i]*(energy[e]**2) ) * (energy[e]**(-3)) )

	

#============= Absorption ======================================================


absorption = np.exp(-nH*xsec) # array of multiplicative absorption coefficents

if galabs:
	galabsorption = np.exp(-gnH*xsec)	# same, for galactic absorption 

#============== Create Power Laws ==============================================


abspower = norm*(energy**(-index))*absorption

unabspower = norm2*(energy**(-index))

#============== create Gaussian ================================================

if gauss:
	
	gaussian =  (gN * ( (gS * np.sqrt(2*pi) )**(-1) ) ) *\
					 np.exp( - ( ( (energy - gE)**2)/(2*(gS**2)) ) )
			

#============ Create total spectrum  ===========================================


total = abspower + unabspower

if gauss:

	total += gaussian

if galabs:

	total *= galabsorption

#============ Integrate total spectrum, find hardnesses, print params ==========

divideindex = (2.0-0.5)/0.01

print 'Hard counts: ',np.trapz(total[:divideindex])
print 'Soft counts: ',np.trapz(total[divideindex:])
print 'Hardnes: ',np.trapz(total)

print 'Spectral index: ', index 
print 'unabsorbed normalisation', norm 
print 'absorbed normalisation',norm2

print 'nH', nH 

print 'Galactic nH', gnH 

print 'Gaussian energy', gE 
print 'Gaussian FWHM', gS,
print 'Gaussian normalisation', gN   


#============= Plotting ========================================================

fig = plt.figure()

ax = fig.add_subplot(1,1,1)
ax.set_yscale('log')
ax.set_xscale('log')
ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

locs,labels = xticks()
xticks(locs, map(lambda x: "%g" % x, locs-min(locs)))

plot(energy, total)
#plot(energy,gaussian)
#plot(energy, abspower)
#plot(energy, unabspower)
plot(menergy, mflux)

show()





