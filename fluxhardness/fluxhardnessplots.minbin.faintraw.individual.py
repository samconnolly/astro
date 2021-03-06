# Import packages

from pylab import *
import numpy as np
#
#===============================================================================
# Plot flux-hardness graphs for a given time period and a model if wanted,
# binning the data according to a minimum number of points per bin
# Sam Connolly March 2012
#===============================================================================

# ========================= PARAMETERS =========================================

# Object name

objectname = "NGC5548" 

#   File routes
route           	= \
"/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc5548/lightcurve"

times = [0,7000]

# binning

binmin = 5 # min points per bin
plotub = False # plot unbinned data?

#-- model - Fh = k*(Fs -Cs)^a + Ch ---------------------------------------------

model 	= False 	# plot model?
k 		= 5.5
a		= 0.5
Cs		= 0.06
Ch		= 0.0

# ==============================================================================

energysoftroute  	= "/refinedCounts/"
energyhardroute  	= "/refinedCounts/"

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
				softflux    = np.append(softflux, float(currflux))
				softfluxerr = np.append(softfluxerr, float(currfluxerr))	
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
				hardflux    = np.append(hardflux, float(currflux))
				hardfluxerr = np.append(hardfluxerr, float(currfluxerr))		
		start = 1

	energyhardin.close()



	hardness    = hardflux/softflux
	hardnesserr = hardness*(np.sqrt((hardfluxerr/hardflux)**2 + \
			(softfluxerr/softflux)**2))

	# Calculate modified hardness and error (H - S / H + S)

	modhardness = (hardflux-softflux)/(hardflux+softflux)
	sumerr = np.sqrt(hardfluxerr**2 + softfluxerr**2)
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

#============= Bin =============================================================

hbins = [[],[[],[]],[],[[],[]],[],[[],[]]]
ebins = [[],[],[]]
nbins = []

value = 0

while value < len(modfluxhard[2]):
	
	count = 0
	
	hbins[0].append(0)
	hbins[2].append(0)
	hbins[4].append(0)
	ebins[0].append([])
	ebins[1].append([])	
	ebins[2].append([])
	nbins.append(0)

	while count < binmin:

		hbins[0][-1] += modfluxhard[0][value]
		ebins[0][-1].append(modfluxhard[0][value])
	
		hbins[2][-1] += modfluxhard[2][value]
		ebins[1][-1].append(modfluxhard[2][value])

		hbins[4][-1] += modfluxhard[4][value]
		ebins[2][-1].append(modfluxhard[4][value])

		nbins[-1] += 1

		value += 1
		

		if (len(modfluxhard[2]) - value) > binmin:

			count += 1

		if value == len(modfluxhard[2]):

			break


for n in range(len(nbins)):
	if nbins[n] == 0:
		nbins[n] = 1

nbins = np.array(nbins)


hbins[0] /= nbins
hbins[2] /= nbins
hbins[4] /= nbins


#============= Model ===========================================================

if model:
	mosoft = ((np.array(modfluxhard[0]) - Ch) / k)**(1.0/a) + Cs
	mohardness = (np.array(modfluxhard[0]) - mosoft)/ \
						(np.array(modfluxhard[0]) + mosoft)

#============= Errors ==========================================================

herr = [[0,0],[0,0],[0,0]]

for i in range(len(ebins[1])):
	
	herr[0] = np.array(np.percentile(ebins[0][i],[15.9,84.1]))
	herr[1] = np.array(np.percentile(ebins[1][i],[15.9,84.1]))
	herr[2] = np.array(np.percentile(ebins[2][i],[15.9,84.1]))
	
	herr[0] = np.abs(herr[0] - [hbins[0][i],hbins[0][i]])
	herr[1] = np.abs(herr[1] - [hbins[2][i],hbins[2][i]])
	herr[2] = np.abs(herr[2] - [hbins[4][i],hbins[4][i]])
		
	hbins[1][0].append(herr[0][0])
	hbins[1][1].append(herr[0][1])
	hbins[3][0].append(herr[1][0])
	hbins[3][1].append(herr[1][1])
	hbins[5][0].append(herr[2][0])
	hbins[5][1].append(herr[2][1])
	
	#print 'bin -> low: ', min(ebins[2][i]), 'high: ', max(ebins[2][i])
	#print 'err -> low: ', hbins[5][0][-1], 'high: ', hbins[5][1][-1]
# ======= PLOTS ================================================================


print "number of bins: ", len(ebins[0]), \
		"min. points per bin: ", len(ebins[0][0]),\
			"points in final bin: ", len(ebins[0][-1])

fig = figure()

n = 1


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}
matplotlib.rcParams.update({'font.size': 22})
matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20)

if plotub:

	n = 2

	fig.add_subplot(2,2,1)
	#title("hard flux v hardness")
	errorbar(modfluxhard[0],modfluxhard[4], xerr = modfluxhard[1], \
				yerr = modfluxhard[5], marker='.', color = 'red', \
					ecolor = 'grey', linestyle = 'none',capsize = 0)
	if model:
		plot(modfluxhard[0],mohardness, color="blue")

	fig.add_subplot(2,2,3)
	#title("hard flux v soft flux")
	errorbar(modfluxhard[0],modfluxhard[2],	xerr = modfluxhard[1],  \
				yerr = modfluxhard[3], marker='.', color = 'red', \
					ecolor = 'grey', linestyle = 'none',capsize = 0)

	if model:
		plot(modfluxhard[0],mosoft, color="blue")

#fig.add_subplot(1,1,1)
#title("Binned Hard Flux v Hardness")
xlabel("Hard (2.0-10.0 keV) Count Rate ($s^{-1}$)")
ylabel("Hardness Ratio (H - S/ H + S)")

errorbar(modfluxhard[0],modfluxhard[4], \
			marker='.', color = 'grey', \
				ecolor = 'lightgrey', linestyle = 'none',linewidth=2,capsize = 0,
					alpha = 0.6,zorder = 1)

errorbar(hbins[0],hbins[4], xerr = hbins[1], \
			yerr = hbins[5], marker='o', color = 'red', \
				ecolor = 'black', linestyle = 'none',linewidth=2,capsize = 0,\
					zorder = 10)




if model:

	plot(modfluxhard[0],mohardness, color="blue")

show()

#fig.add_subplot(1,1,1)
fig = figure()
#title("binned hard flux v soft flux")
xlabel("Hard (2.0-10.0 keV) Count Rate ($s^{-1}$)")
ylabel("Soft (0.5-2.0 keV) Count Rate ($s^{-1}$)")

errorbar(modfluxhard[0],modfluxhard[2], \
			marker='.', color = 'grey', \
				ecolor = 'lightgrey', linestyle = 'none',linewidth=2,capsize = 0,
					alpha = 0.6,zorder = 1)



errorbar(hbins[0],hbins[2],	xerr = hbins[1],  \
			yerr = hbins[3], marker='o', color = 'red', \
				ecolor = 'black', linestyle = 'none',linewidth = 2,capsize = 0,\
					zorder = 10)

if model:
	plot(modfluxhard[0],mosoft, color="blue")

show()


# plot bin distributions


#for i in range(len(ebins[2])):
#	
#	subplot(2,int((len(ebins[2])/2.0)+0.5),i+1)
#	
#	hist(ebins[2][i], 8)

#show()
