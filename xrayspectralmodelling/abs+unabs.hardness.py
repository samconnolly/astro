# abs+unabs.hardness.py
# Sam Connolly 19/02/2013

#===============================================================================
# create hardness plots according to variations in absorption
#===============================================================================

# Import packages

import pylab as plt
import numpy as np
import matplotlib

#================ PARAMETERS ===================================================

# ---- constant spectral parameters --------------------------------------------

# best tied fit to data - index = 1.9, norm = 1.07E-2, norm2 = 2.01E-4, nH 0.015-1.72

index = 1.9		 # Power law index for both power laws

norm = 1.07E-2	 # normalisation for absorbed power law
norm2 = 2E-4	 # normalisation for unabsorbed power law


#-------------------------------------------------------------------------------

nHmin = 0.015 	# equivalent Hydrogen column densities in 10^24 cm^-2
nHmax = 2.0	

specnum = 30    # number of spectra to generate

softmin = 0.1   # bottom energy of soft energy range (keV)
divide  = 2.0	# dividing energy between soft and hard (keV)
hardmax = 10.0	# top energy of hard energy range (keV)

galabs = True # add galactic absorption?
gnH = 1.39E-4 # galactic column density in 10^24 cm^-2

gauss = True # add a gaussian?

gE = 0.776  # gaussian central energy
gS = 0.157	# gaussian line width
gN = 1.775E-04	# gaussian normalisation

#-- model - Fh = k*(Fs -Cs)^a + Ch ---------------------------------------------

model 	= True 	# plot model?
k 		= 5.0
a		= 0.5
Cs		= 0.06
Ch		= 0.0

#========== Absorption parameter file ==========================================

# read variables
header = 1 # number of header lines to ignore

#   File routes
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/"\
						+"xraySpectralModelling/"

# file names
infilename 	= "absorptionXsections.dat"

#===============================================================================

# create file route
location  = route+infilename

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

# energy array
	
energy = np.arange(softmin,hardmax,0.01)

# cross section array

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

# extra components

# galactic absorption

if galabs:
	galabsorption = np.exp(-gnH*xsec)	# same, for galactic absorption 

# Gaussian 

if gauss:
	
	gaussian =  (gN * ( (gS * np.sqrt(2*np.pi) )**(-1) ) ) *\
					 np.exp( - ( ( (energy - gE)**2)/(2*(gS**2)) ) )

#-------------------------------------------------------------------------------
#============ SPECTRUM GENERATION AND HARDNESS CALCULATION =====================
#-------------------------------------------------------------------------------

def Hard(nH):


	#============= Absorption ======================================================


	absorption = np.exp(-nH*xsec) # array of multiplicative absorption coefficents
	
	#==============  Power Laws ==============================================


	abspower = norm*(energy**(-index))*absorption

	unabspower = norm2*(energy**(-index))

	#============ Create total spectrum  ===========================================

	total = abspower + unabspower

	if gauss:

		total += gaussian

	if galabs:

		total *= galabsorption

	#============ Integrate total spectrum, find hardnesses ========================


	divideindex = (2.0-0.5)/0.01

	soft =  np.trapz(total[:divideindex])
	hard =  np.trapz(total[divideindex:])
	hardness = (hard - soft) / (hard + soft)

	return soft, hard, hardness, total 

#====== carry out many simulation to create graph of hardness v hard counts ====

asoft 		= np.array([])
ahard 		= np.array([])
ahardness 	= np.array([])

fig = plt.figure()

# Overall plots title
plt.suptitle("Spectral variation for an absorped and scattered powerlaw\n \
spectral index: {0} unabsorbed norm: {1} absorbed norm: {2}\
   Min./max. nH: {3}/{4}".format(index,norm2,norm,nHmin, nHmax) )

ax = fig.add_subplot(3,1,1)
ax.set_yscale('log')
ax.set_xscale('log')
ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

# use logarithmic range for nH to ensure even spacing
nrange = (np.log(nHmax)-np.log(nHmin))/specnum

for n in np.arange(np.log(nHmin),np.log(nHmax),nrange):
	
	nH = np.exp(n)

	soft,hard,hardness,total = Hard(nH)

	asoft = np.append(asoft,soft)
	ahard = np.append(ahard,hard)
	ahardness = np.append(ahardness, hardness)

	plt.plot(energy,total)
	plt.xlim([0.3,hardmax])

#============= Model ===========================================================

if model:
	mosoft = ((ahard - Ch) / k)**(1.0/a) + Cs
	mohardness = (ahard - mosoft)/(ahard + mosoft)

#============= Plotting ========================================================


fig.add_subplot (3,1,2)
plt.plot(ahard,ahardness)
if model:
	plt.plot(ahard,mohardness,color ="red")

fig.add_subplot (3,1,3)
plt.plot(ahard,asoft)
if model:
	plt.plot(ahard,mosoft,color ="red")

plt.show()





