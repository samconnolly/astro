# Import packages

from pylab import *
import numpy as numpy
#
#===============================================================================
# Plot multiple flux-hardness graphs for different time periods for comparison
# (and light curve if wanted)
# Sam Connolly December 2012
#===============================================================================

# ========================= PARAMETERS =========================================

# Object name

objectname = "NGC1365" 

#   File routes
route           	= \
"/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/lightcurve"


errors = False
single = True
lightcurves = True

times = [[0,5200],	# tmin1,tmax1
		 [5200,5600],	# tmin2,tmax2
		 [5600,6000],		# tmin3,tmax3
		 [6000,7000]]			# tmin4,tmax4

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
				softflux    = numpy.append(softflux, float(currflux))
				softfluxerr = numpy.append(softfluxerr, float(currfluxerr))	
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
				hardflux    = numpy.append(hardflux, float(currflux))
				hardfluxerr = numpy.append(hardfluxerr, float(currfluxerr))		
		start = 1

	energyhardin.close()



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

	return modfluxhard, totalflux, hardtime



# ======= PLOTS TO MAKE ========================================================

modfluxhard1, totalflux1, time1 = hardnessflux(times[0][0],times[0][1])
modfluxhard2, totalflux2, time2 = hardnessflux(times[1][0],times[1][1])
modfluxhard3, totalflux3, time3 = hardnessflux(times[2][0],times[2][1])
modfluxhard4, totalflux4, time4 = hardnessflux(times[3][0],times[3][1])


# ==============================================================================

# lightcurves

if lightcurves:
	nplots = 3
else:
	nplots = 2

# plot with pylab

if single:

	if errors:

		hardplot = subplot(nplots,1,1)
		title("hard flux v hardness")
		p1 = errorbar(modfluxhard1[0],modfluxhard1[4],yerr=modfluxhard1[5])
		p2 = errorbar(modfluxhard2[0],modfluxhard2[4],yerr=modfluxhard2[5])
		p3 = errorbar(modfluxhard3[0],modfluxhard3[4],yerr=modfluxhard3[5])
		p4 = errorbar(modfluxhard4[0],modfluxhard4[4],yerr=modfluxhard4[5])
		pylab.ylim([-1.2,1.2])
		legend([p1,p2,p3,p4],  ["MJD: {0}".format(times[0]),
								"MJD: {0}".format(times[1]),
								"MJD: {0}".format(times[2]),
								"MJD: {0}".format(times[3]),])
		subplot(nplots,1,2)
		title("hard flux v soft flux")
		p1 = errorbar(modfluxhard1[0],modfluxhard1[2],xerr=modfluxhard1[1]\
					,yerr=modfluxhard1[3])
		p2 = errorbar(modfluxhard2[0],modfluxhard2[2],xerr=modfluxhard2[1]\
				,yerr=modfluxhard2[3])
		p3 = errorbar(modfluxhard3[0],modfluxhard3[2],xerr=modfluxhard3[1]\
				,yerr=modfluxhard3[3])
		p4 = errorbar(modfluxhard4[0],modfluxhard4[2],xerr=modfluxhard4[1]\
				,yerr=modfluxhard4[3])
		legend([p1,p2,p3,p4],  ["MJD: {0}".format(times[0]),
								"MJD: {0}".format(times[1]),
								"MJD: {0}".format(times[2]),
								"MJD: {0}".format(times[3]),])
	else:

		subplot(nplots,1,1)
		title("hard flux v hardness")
		p1 = scatter(modfluxhard1[0],modfluxhard1[4], color = "blue")
		p2 = scatter(modfluxhard2[0],modfluxhard2[4], color = "red")
		p3 = scatter(modfluxhard3[0],modfluxhard3[4], color = "green")
		p4 = scatter(modfluxhard4[0],modfluxhard4[4], color = "purple")
		legend([p1,p2,p3,p4],  ["MJD: {0}".format(times[0]),
								"MJD: {0}".format(times[1]),
								"MJD: {0}".format(times[2]),
								"MJD: {0}".format(times[3]),])
		ylim([-1.2,1.2])
		xlim([-0.1,4.0])
		subplot(nplots,1,2)
		title("hard flux v soft flux")
		p1 = scatter(modfluxhard1[0],modfluxhard1[2], color = "blue")
		p2 = scatter(modfluxhard2[0],modfluxhard2[2], color = "red")
		p3 = scatter(modfluxhard3[0],modfluxhard3[2], color = "green")
		p4 = scatter(modfluxhard4[0],modfluxhard4[2], color = "purple")
		legend([p1,p2,p3,p4],  ["MJD: {0}".format(times[0]),
								"MJD: {0}".format(times[1]),
								"MJD: {0}".format(times[2]),
								"MJD: {0}".format(times[3]),])

	if lightcurves:
		subplot(nplots,1,3)
		title("Lightcurve")
		p1 = scatter(time1,totalflux1, color = "blue")
		p2 = scatter(time2,totalflux2, color = "red")
		p3 = scatter(time3,totalflux3, color = "green")
		p4 = scatter(time4,totalflux4, color = "purple")
		legend([p1,p2,p3,p4],  ["MJD: {0}".format(times[0]),
								"MJD: {0}".format(times[1]),
								"MJD: {0}".format(times[2]),
								"MJD: {0}".format(times[3]),])
else:

	if errors:

		subplot(nplots+2,2,1)
		title("hard flux v hardness")
		errorbar(modfluxhard1[0],modfluxhard1[4],yerr=modfluxhard1[5])
		subplot(nplots+2,2,2)
		title("hard flux v soft flux")
		errorbar(modfluxhard1[0],modfluxhard1[2],xerr=modfluxhard1[1]\
					,yerr=modfluxhard1[3])
		subplot(nplots+2,2,3)
		errorbar(modfluxhard2[0],modfluxhard2[4],yerr=modfluxhard2[5])
		subplot(nplots+2,2,4)
		errorbar(modfluxhard2[0],modfluxhard2[2],xerr=modfluxhard2[1]\
				,yerr=modfluxhard2[3])
		subplot(nplots+2,2,5)
		errorbar(modfluxhard3[0],modfluxhard3[4],yerr=modfluxhard3[5])
		subplot(nplots+2,2,6)
		errorbar(modfluxhard3[0],modfluxhard3[2],xerr=modfluxhard3[1]\
				,yerr=modfluxhard3[3])
		subplot(nplots+2,2,7)
		errorbar(modfluxhard4[0],modfluxhard4[4],yerr=modfluxhard4[5])
		subplot(nplots+2,2,8)
		errorbar(modfluxhard4[0],modfluxhard4[2],xerr=modfluxhard4[1]\
				,yerr=modfluxhard4[3])

	else:

		subplot(nplots+2,2,1)
		title("hard flux v hardness")
		scatter(modfluxhard1[0],modfluxhard1[4])
		subplot(nplots+2,2,2)
		title("hard flux v soft flux")
		scatter(modfluxhard1[0],modfluxhard1[2])
		subplot(nplots+2,2,3)
		scatter(modfluxhard2[0],modfluxhard2[4])
		subplot(nplots+2,2,4)
		scatter(modfluxhard2[0],modfluxhard2[2])
		subplot(nplots+2,2,5)
		scatter(modfluxhard3[0],modfluxhard3[4])
		subplot(nplots+2,2,6)
		scatter(modfluxhard3[0],modfluxhard3[2])
		subplot(nplots+2,2,7)
		scatter(modfluxhard4[0],modfluxhard4[4])
		subplot(nplots+2,2,8)
		scatter(modfluxhard4[0],modfluxhard4[2])

	if lightcurves:
		subplot(nplots+2,1,3)
		title("Lightcurve")
		p1 = scatter(time1,totalflux1, color = "blue")
		p2 = scatter(time2,totalflux2, color = "red")
		p3 = scatter(time3,totalflux3, color = "green")
		p4 = scatter(time4,totalflux4, color = "purple")
		legend([p1,p2,p3,p4],  ["MJD: {0}".format(times[0]),
								"MJD: {0}".format(times[1]),
								"MJD: {0}".format(times[2]),
								"MJD: {0}".format(times[3]),])

show()





