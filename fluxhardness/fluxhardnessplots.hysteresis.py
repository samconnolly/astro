# Import packages

from pylab import *
import numpy as numpy
import matplotlib
#

#===============================================================================
# Plot flux-hardness graphs for a given time period and a model if wanted,
# with upward movement of flux in red, down in blue (or vice versa...), to
# check for hysteresis.
# Sam Connolly June 2012
#===============================================================================

# ========================= PARAMETERS =========================================

# Object name

objectname = "NGC4395" 

#   File routes
route           	= \
"/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc4395/lightcurve"

times = [0,7000]

hardnorm = 1. #.48065
softnorm = 1. #1.739

#-- model - Fh = k*(Fs -Cs)^a + Ch ---------------------------------------------

model 	= False 	# plot model?
k 		= 6.0
a		= 0.5
Cs		= 0.06
Ch		= 0.0

# ==============================================================================

energysoftroute  	= "/refinedCounts/"
energyhardroute  	= "/refinedCounts/"

# file names
energysoftfname 	= objectname+"_lcurve_3_gti_0.5-2keV.qdp"
energyhardfname		= objectname+"_lcurve_3_gti_2-10keV.qdp"
energytotfname		= objectname+"_lcurve_3_gti_0.5-10keV.qdp"

# create file routes
energysoftlocation 		= route+energysoftroute+energysoftfname
energyhardlocation 		= route+energyhardroute+energyhardfname
energytotlocation		= route+energyhardroute+energytotfname

# Function to calculate hardness and error

def hardnessflux(tmin,tmax):

	# read data into 2-D arrays
	start = 0

	softtime    = numpy.array([])
	softflux    = numpy.array([])
	softfluxerr = numpy.array([])
	# soft
	energysoftin= open(energysoftlocation, 'r')

	for x in energysoftin:
	
		currtime, currflux, currfluxerr = x.split()
		if start == 1:
			if float(currtime) >= tmin and float(currtime) <= tmax:
				softtime    = numpy.append(softtime, float(currtime))
				softflux    = numpy.append(softflux, float(currflux)*softnorm)
				softfluxerr = numpy.append(softfluxerr, float(currfluxerr)*softnorm)	
		start = 1

	energysoftin.close()

	# hard
	start = 0

	hardtime    = numpy.array([])
	hardflux    = numpy.array([])
	hardfluxerr = numpy.array([])

	energyhardin= open(energyhardlocation, 'r')

	for x in energyhardin:
	
		currtime, currflux, currfluxerr = x.split()
		if start == 1:
			if float(currtime) >= tmin and float(currtime) <= tmax:
				hardtime    = numpy.append(hardtime, float(currtime))
				hardflux    = numpy.append(hardflux, float(currflux)*hardnorm)
				hardfluxerr = numpy.append(hardfluxerr, float(currfluxerr)*hardnorm)		
		start = 1

	energyhardin.close()

	# hysteresis up/down check

	start = 0

	totflux = []

	energytotin= open(energytotlocation, 'r')

	for x in energytotin:
	
		currtime, currflux, currfluxerr = x.split()
		if start == 1:
			if float(currtime) >= tmin and float(currtime) <= tmax:
				totflux    = numpy.append(totflux, float(currflux))

		start = 1

	energytotin.close()

	print len(totflux), len(hardflux)

	hyst = []

	start = 0

	for f in range(len(totflux)):

		if start < 3:

			hyst.append(0.1)
			

		if start > (len(totflux) - 3):

			hyst.append(1.)

		if start <= (len(totflux) - 3) and start >= 3:

			if ((totflux[f]+totflux[f+1]+totflux[f+2])/3.) >= \
				((totflux[f-1]+totflux[f-2]+totflux[f-3])/3.):

				hyst.append(1.)

			else:

				hyst.append(0.1)

		start += 1

	hardness    = hardflux/softflux
	hardnesserr = hardness*(numpy.sqrt((hardfluxerr/hardflux)**2 + \
			(softfluxerr/softflux)**2))

	# Calculate modified hardness and error (H - S / H + S)

	modhardness = (hardflux-softflux)/(hardflux+softflux)
	sumerr = sqrt(hardfluxerr**2 + softfluxerr**2)
	modhardnesserr = modhardness*(numpy.sqrt(\
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

	return modfluxhard, totalflux, hardtime, hyst

# run!

modfluxhard, totalflux, time, hyst = hardnessflux(times[0],times[1])

#============= Model ===========================================================

if model:
	mosoft = ((np.array(modfluxhard[0]) - Ch) / k)**(1.0/a) + Cs
	mohardness = (np.array(modfluxhard[0]) - mosoft)/ \
						(np.array(modfluxhard[0]) + mosoft)

# ======= PLOTS ================================================================

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}
matplotlib.rcParams.update({'font.size': 22})
matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20)

fig = figure()  

fig.add_subplot(2,1,1)
#title("Hard Flux v Hardness")
xlabel("Hard Flux (cnts s^-1)")
ylabel("Hardness (H-S/H+S)")

#errorbar(modfluxhard[0],modfluxhard[4], xerr = modfluxhard[1], \
#			yerr = modfluxhard[5], marker='.', color = 'red', \
#				ecolor = 'grey', linestyle = 'none',capsize = 0)


cmap = matplotlib.cm.jet 
nx = matplotlib.colors.Normalize(vmin=0, vmax=1) 

scatter(modfluxhard[0],modfluxhard[4], c=hyst, cmap=cmap, norm=nx)


if model:
	plot(modfluxhard[0],mohardness, color="blue")

fig.add_subplot(2,1,2)
#title("hard flux v soft flux")
xlabel("Hard Flux (cnts s^-1)")
ylabel("Soft Flux (cnts s^-1)")

#errorbar(modfluxhard[0],modfluxhard[2],	xerr = modfluxhard[1],  \
#			yerr = modfluxhard[3], marker='.', color = 'red', \
#				ecolor = 'grey', linestyle = 'none',capsize = 0)

scatter(modfluxhard[0],modfluxhard[2], c=hyst, cmap=cmap, norm=nx)

if model:
	plot(modfluxhard[0],mosoft, color="blue")

show()






