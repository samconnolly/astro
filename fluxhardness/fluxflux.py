# Import packages

from pylab import *
import numpy as numpy
#
#===============================================================================
# Create flux-flux plots and a QDP file from two bands over a given time range 
# (log and linear)
#===============================================================================

# read variables
tmin = 0.0
tmax = 7000.0

#   File routes
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/mainlc"
energysoftroute  = "/refined/"
energyhardroute  = "/refined/"

outroute         = "/fluxflux/"

# file names
energysoftfname 	= "NGC1365_lcurve_3_gti_0.5-2keV.qdp"
energyhardfname		= "NGC1365_lcurve_3_gti_2-10keV.qdp"
outfname     		= "NGC1365_lcurve_gti_fluxflux.qdp"
logoutfname    		= "NGC1365_lcurve_gti_logfluxflux.qdp"

# create file routes
energysoftlocation  = route+energysoftroute+energysoftfname
energyhardlocation  = route+energyhardroute+energyhardfname
outlocation         = route+outroute+outfname
logoutlocation        = route+outroute+logoutfname

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

# flux-flux.... sort in order of hard flux

fluxflux = [[],[],[]]
start = 0

for value in range(len(hardflux)):
	# if it isn't the first value...
	if start !=0:
		for comp in range(len(fluxflux[0])): # for each value, from bottom up...
			if hardflux[value] <= fluxflux[0][comp]: # add below value if <=
				fluxflux[0].insert(comp,hardflux[value])
				fluxflux[1].insert(comp,softflux[value])
				fluxflux[2].insert(comp,softfluxerr[value])
				break
			if comp == len(fluxflux[0]) - 1: # add above final element if > all
				fluxflux[0].append(hardflux[value])
				fluxflux[1].append(softflux[value])			
				fluxflux[2].append(softfluxerr[value])

	# if it is the first value, just fill that stuff in
	if start == 0:
		fluxflux[0].append(hardflux[value])
		fluxflux[1].append(softflux[value])
		fluxflux[2].append(hardfluxerr[value])
		start = 1

# find the log flux flux values

logfluxflux = numpy.log(fluxflux)

# write to file
outfile= open(outlocation, 'w')

outfile.write("READ serr 2 \n") # qdp error header

for o in range(len(fluxflux[0])):		# data!
	outfile.write(str(fluxflux[0][o]))
	outfile.write("     ")
	outfile.write(str(fluxflux[1][o]))
	outfile.write("     ")
	outfile.write(str(fluxflux[2][o]))
	outfile.write("\n")

outfile.close()

logoutfile= open(logoutlocation, 'w')

logoutfile.write("READ serr 2 \n") # qdp error header

for o in range(len(logfluxflux[0])):		# data!
	logoutfile.write(str(logfluxflux[0][o]))
	logoutfile.write("     ")
	logoutfile.write(str(logfluxflux[1][o]))
	logoutfile.write("     ")
	logoutfile.write(str(logfluxflux[2][o]))
	logoutfile.write("\n")

logoutfile.close()

# plot with pylab
subplot(2,1,1)
errorbar(fluxflux[0],fluxflux[1],yerr=fluxflux[2])
subplot(2,1,2)
errorbar(logfluxflux[0],logfluxflux[1],yerr=logfluxflux[2])

show()





