# Import packages

from pylab import *
import numpy as numpy
#
#===============================================================================
# Plot multiple flux-hardness graphs for different objects for comparison
# (and light curves if wanted - NOT YET)
# Sam Connolly December 2012
#===============================================================================

# ========================= PARAMETERS =========================================

# Object names

objectname1 = "NGC1365" 
objectname2 = "Mkn335" 
objectname3 = "PMNJ0948plus0022" 
objectname4 = "1H0707-495" 

#  Overall File route
route = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/"

# object file routes
oroute1 = "ngc1365/lightcurve"
oroute2 = "Mkn335/lightcurve"
oroute3 = "pmnj0948/lightcurve"
oroute4 = "1H0707-495/lightcurve"

energysoftroute  	= "/refined/"
energyhardroute  	= "/refined/"

errors = False		# plot errors?
single = True		# plot graphs individually?
lightcurves = False	# plot lightcurves?
size = 4                # plot marker size



# ==============================================================================



# Function to calculate hardness and error

def hardnessflux(objectname,oroute):


	# file names
	energysoftfname 	= objectname+"_lcurve_3_gti_0.5-2keV.qdp"
	energyhardfname		= objectname+"_lcurve_3_gti_2-10keV.qdp"

	# create file routes
	energysoftlocation 	= route+oroute+energysoftroute+energysoftfname
	energyhardlocation 	= route+oroute+energyhardroute+energyhardfname

	# read data into 2-D arrays
	start = 0

	softtime    = []
	softflux    = []
	softfluxerr = []
	# soft
	energysoftin= open(energysoftlocation, 'r')

	for x in energysoftin:
	
		currtime, currflux, currfluxerr = x.split()
		if start == 1:

			softtime.append(float(currtime))
			softflux.append(float(currflux))
			softfluxerr.append(float(currfluxerr))	

		start = 1

	energysoftin.close()
	# hard
	start = 0

	hardtime    = []
	hardflux    = []
	hardfluxerr = []

	energyhardin= open(energyhardlocation, 'r')

	for x in energyhardin:
	
		currtime, currflux, currfluxerr = x.split()
		if start == 1:

			hardtime.append(float(currtime))
			hardflux.append(float(currflux))
			hardfluxerr.append(float(currfluxerr))		

		start = 1

	energyhardin.close()

	# check equal timings, remove non-equal ones

	stime = 0
	htime = 0

	sremove = []
	hremove = []

	while stime < len(softtime) and htime < len(hardtime):

		if softtime[stime] != hardtime[htime]:

			if softtime[stime] > hardtime[htime]:

				hremove.append(htime)
				htime += 1

			elif softtime[stime] < hardtime[htime]:

				sremove.append(stime)
				stime += 1

		else:

			stime += 1
			htime += 1


	
	for index in sremove:
		print index
		del softtime[index]
		del softflux[index]
		del softfluxerr[index]	

	for index in hremove:
		del hardtime[index]
		del hardflux[index]	
		del hardfluxerr[index]

	# convert to numpy arrays

	softtime = numpy.array(softtime)
	softflux = numpy.array(softflux)
	softfluxerr = numpy.array(softfluxerr)
	hardtime = numpy.array(hardtime)
	hardflux = numpy.array(hardflux)
	hardfluxerr = numpy.array(hardfluxerr)

	# calculate hardness


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

modfluxhard1, totalflux1, time1 = hardnessflux(objectname1,oroute1)
modfluxhard2, totalflux2, time2 = hardnessflux(objectname2,oroute2)
modfluxhard3, totalflux3, time3 = hardnessflux(objectname3,oroute3)
modfluxhard4, totalflux4, time4 = hardnessflux(objectname4,oroute4)


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
		legend([p1,p2,p3,p4],  [objectname1,
								objectname2,
								objectname3,
								objectname4])
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
		legend([p1,p2,p3,p4],  [objectname1,
								objectname2,
								objectname3,
								objectname4])
	else:

		subplot(nplots,1,1)
		title("hard flux v hardness")
		p1 = scatter(modfluxhard1[0],modfluxhard1[4],s=size, color = "blue")
		p2 = scatter(modfluxhard2[0],modfluxhard2[4], s=size,color = "red")
		p3 = scatter(modfluxhard3[0],modfluxhard3[4], s=size,color = "green")
		p4 = scatter(modfluxhard4[0],modfluxhard4[4], s=size,color = "purple")
		legend([p1,p2,p3,p4],  [objectname1,
								objectname2,
								objectname3,
								objectname4])
		ylim([-1.2,1.2])
		xlim([-0.1,5.0])
		subplot(nplots,1,2)
		title("hard flux v soft flux")
		p1 = scatter(modfluxhard1[0],modfluxhard1[2],s=size, color = "blue")
		p2 = scatter(modfluxhard2[0],modfluxhard2[2],s=size, color = "red")
		p3 = scatter(modfluxhard3[0],modfluxhard3[2],s=size, color = "green")
		p4 = scatter(modfluxhard4[0],modfluxhard4[2],s=size, color = "purple")
		legend([p1,p2,p3,p4],  [objectname1,
								objectname2,
								objectname3,
								objectname4])

	if lightcurves:
		subplot(nplots,1,3)
		title("Lightcurve")
		p1 = scatter(time1,totalflux1, color = "blue")
		p2 = scatter(time2,totalflux2, color = "red")
		p3 = scatter(time3,totalflux3, color = "green")
		p4 = scatter(time4,totalflux4, color = "purple")
		legend([p1,p2,p3,p4],  [objectname1,
								objectname2,
								objectname3,
								objectname4])
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

	subplot(nplots+2,1,3)
	title("Lightcurve")
	p1 = scatter(time1,totalflux1, color = "blue")
	p2 = scatter(time2,totalflux2, color = "red")
	p3 = scatter(time3,totalflux3, color = "green")
	p4 = scatter(time4,totalflux4, color = "purple")
	legend([p1,p2,p3,p4],  [objectname1,
							objectname2,
							objectname3,
							objectname4])

show()





