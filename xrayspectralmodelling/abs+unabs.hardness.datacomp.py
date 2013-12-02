# abs+unabs.hardness.datacomp.py
# Sam Connolly 20/02/2013

#===============================================================================
# create hardness plots according to variations in absorption, compare to real
# data set's hardness graphs
#===============================================================================

# Import packages

from pylab import *
import numpy as np

#================ PARAMETERS ===================================================
 
#--- Real Data -----------------------------------------------------------------

# Object name

objectname = "NGC1365" 

#   File routes
route           	= \
"/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/lightcurve"

times = [0,7000]

# ---- constant spectral parameters --------------------------------------------

# best tied fit to data - index = 1.9, norm = 1.07E-2, norm2 = 2.01E-4, nH 0.015-1.72

index = 1.8		 # Power law index for both power laws

norm = 1.0E-2	 # normalisation for absorbed power law
norm2 = 1.6E-4	 # normalisation for unabsorbed power law


#-------------------------------------------------------------------------------

nHmin = 0.00001 	# equivalent Hydrogen column densities in 10^24 cm^-2
nHmax = 10000.0			

softmin = 0.5   # bottom energy of soft energy range (keV)
divide  = 2.0	# dividing energy between soft and hard (keV)
hardmax = 10.0	# top energy of hard energy range (keV)

galabs = True # add galactic absorption?
gnH = 1.39E-4 # galactic column density in 10^24 cm^-2

gauss = True # add a gaussian?

gE = 0.776  # gaussian central energy
gS = 0.157	# gaussian line width
gN = 1.775E-04	# gaussian normalisation

specnum = 50    # number of spectra to generate

softdatanorm = 0.48		# normalisations to data count rate..
harddatanorm = 0.125

#-- model - Fh = k*(Fs -Cs)^a + Ch ---------------------------------------------

model 	= False 	# plot model?
k 		= 5.0
a		= 0.5
Cs		= 0.06
Ch		= 0.0

#========== Absorption parameter file ==========================================

# read variables
header = 1 # number of header lines to ignore

#   File routes
inroute            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/"\
						+"xraySpectralModelling/"

# file names
infilename 	= "absorptionXsections.dat"

#===============================================================================

# create file route
inlocation  = inroute+infilename

# read data intoarray

Emin = []
Emax = []
c0   = []
c1   = []
c2   = []

infile= open(inlocation, 'r')

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
	#print absorption
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
suptitle("Spectral variation for an absorped and scattered powerlaw\n \
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
	plt.xlim([0.5,10.0])

# ==============================================================================

#				Real Data

# ==============================================================================

energysoftroute  	= "/refined/"
energyhardroute  	= "/refined/"

# file names
energysoftfname 	= objectname+"_lcurve_3_gti_0.5-2keV.qdp"
energyhardfname		= objectname+"_lcurve_3_gti_2-10keV.qdp"


# create file routes
energysoftlocation 		= route+energysoftroute+energysoftfname
energyhardlocation 		= route+energyhardroute+energyhardfname


# Function to calculate hardness and error

def hardnessflux(tmin,tmax):

	# read data into 2-D arrays
	start = 0

	softtime    = np.array([])
	softflux    = np.array([])
	softfluxerr = np.array([])
	# soft
	energysoftin= open(energysoftlocation, 'r')

	for x in energysoftin:
	
		currtime, currflux, currfluxerr = x.split()
		if start == 1:
			if float(currtime) >= tmin and float(currtime) <= tmax:
				softtime    = np.append(softtime, float(currtime))
				softflux    = np.append(softflux, float(currflux)*softdatanorm)
				softfluxerr = np.append(softfluxerr, float(currfluxerr)*softdatanorm)	
		start = 1

	energysoftin.close()
	# hard
	start = 0

	hardtime    = np.array([])
	hardflux    = np.array([])
	hardfluxerr = np.array([])

	energyhardin= open(energyhardlocation, 'r')

	for x in energyhardin:
	
		currtime, currflux, currfluxerr = x.split()
		if start == 1:
			if float(currtime) >= tmin and float(currtime) <= tmax:
				hardtime    = np.append(hardtime, float(currtime))
				hardflux    = np.append(hardflux, float(currflux)*harddatanorm)
				hardfluxerr = np.append(hardfluxerr, float(currfluxerr)*harddatanorm)		
		start = 1

	energyhardin.close()



	hardness    = hardflux/softflux
	hardnesserr = hardness*(np.sqrt((hardfluxerr/hardflux)**2 + \
			(softfluxerr/softflux)**2))

	# Calculate modified hardness and error (H - S / H + S)

	modhardness = (hardflux-softflux)/(hardflux+softflux)
	sumerr = sqrt(hardfluxerr**2 + softfluxerr**2)
	modhardnesserr = modhardness*(np.sqrt(\
	(sumerr/(hardflux-softflux))**2 + (sumerr/(hardflux+softflux))**2 ) )

	# sort modified hardnesses and soft flux according to hard flux

	modfluxhard = [[],[],[],[],[],[]]
	start = 0

	for value in range(len(modhardness)):
		# if it isn't the first value...
		if start !=0:
			for comp in range(len(modfluxhard[0])): # for each value 
							# from the bottom up...
				if hardflux[value] <= modfluxhard[0][comp]:# add 
						     						 # below value if less/equal
					modfluxhard[0].insert(comp,hardflux[value])
					modfluxhard[1].insert(comp,hardfluxerr[value])
					modfluxhard[2].insert(comp,softflux[value])
					modfluxhard[3].insert(comp,softfluxerr[value])
					modfluxhard[4].insert(comp,modhardness[value])
					modfluxhard[5].insert(comp,modhardnesserr[value])
					break
				if comp == len(modfluxhard[0]) -1:  # add after last 
								 					# element if > than all
					modfluxhard[0].append(hardflux[value])
					modfluxhard[1].append(hardfluxerr[value])
					modfluxhard[2].append(softflux[value])
					modfluxhard[3].append(softfluxerr[value])
					modfluxhard[4].append(modhardness[value])
					modfluxhard[5].append(modhardnesserr[value])

		# if it is the first value, just fill that stuff in
		if start == 0:
			modfluxhard[0].append(hardflux[value])
			modfluxhard[1].append(hardfluxerr[value])
			modfluxhard[2].append(softflux[value])
			modfluxhard[3].append(softfluxerr[value])
			modfluxhard[4].append(modhardness[value])
			modfluxhard[5].append(modhardnesserr[value])
			start = 1
		
	totalflux = hardflux + softflux

	return modfluxhard, totalflux, hardtime

# run!

modfluxhard, totalflux, time = hardnessflux(times[0],times[1])



#============= Model ===========================================================

if model:
	mosoft = ((ahard - Ch) / k)**(1.0/a) + Cs
	mohardness = (ahard - mosoft)/(ahard + mosoft)

#============= Plotting ========================================================


fig.add_subplot (3,1,2)
plt.title("hard flux v hardness")
plt.scatter(modfluxhard[0],modfluxhard[4])
plt.plot(ahard,ahardness,color ="green")
if model:
	plt.plot(ahard,mohardness,color ="red")
plt.xlim([-0.01,0.51])

fig.add_subplot (3,1,3)
plt.title("hard flux v soft flux")
plt.scatter(modfluxhard[0],modfluxhard[2])
plt.plot(ahard,asoft,color ="green")
if model:
	plt.plot(ahard,mosoft,color ="red")
plt.xlim([-0.01,0.51])
plt.ylim([-0.1,0.35])

plt.show()



