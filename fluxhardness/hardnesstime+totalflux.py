# Import packages

from pylab import *
import numpy as numpy
#
#===============================================================================
# Create Hardness-time files of two formats and hardness-total flux files, 
# with the lightcurve for comparison,
# from two lighcurves of different energies, and plots 
#===============================================================================

# read variables
tmin = 6200.0
tmax = 7000.0

#   File routes
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/mainlc"
energysoftroute  = "/refined/"
energyhardroute  = "/refined/"
energytotalroute = "/refined/"
outroutehard     = "/hardnessratio/"
outroutemodhard  = "/modhardnessratio/"
outroutehard     = "/hardnessratio/"
outroutemodhard  = "/modhardnessratio/"

# file names
energysoftfname 	= "NGC1365_lcurve_3_gti_0.5-2keV.qdp"
energyhardfname		= "NGC1365_lcurve_3_gti_2-10keV.qdp"
energytotalfname    = "NGC1365_lcurve_3_gti_0.5-10keV.qdp"
outfnamehard   		= "NGC1365_lcurve_gti_hard.qdp"
outfnamemodhard 	= "NGC1365_lcurve_gti_modhard.qdp"
outfnamehardflux   	= "NGC1365_flux_gti_hard.qdp"
outfnamemodhardflux	= "NGC1365_flux_gti_modhard.qdp"

# create file routes
energysoftlocation  = route+energysoftroute+energysoftfname
energyhardlocation  = route+energyhardroute+energyhardfname
energytotallocation = route+energytotalroute+energytotalfname
outlocationhard     = route+outroutehard+outfnamehard
outlocationmodhard  = route+outroutemodhard+outfnamemodhard

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
# total
start = 0

totaltime    = numpy.array([])
totalflux    = numpy.array([])
totalfluxerr = numpy.array([])

energytotalin= open(energytotallocation, 'r')

for x in energytotalin:
	
	currtime, currflux, currfluxerr = x.split()
	if start == 1:
		if float(currtime) >= tmin and float(currtime) <= tmax:
			totaltime    = numpy.append(totaltime, float(currtime))
			totalflux    = numpy.append(totalflux, float(currflux))
			totalfluxerr = numpy.append(totalfluxerr, float(currfluxerr))		
	start = 1

energytotalin.close()

# Calculate hardness and error

hardness    = hardflux/softflux
hardnesserr = hardness*(numpy.sqrt((hardfluxerr/hardflux)**2 + (softfluxerr/softflux)**2))

# Calculate modified hardness and error (H - S / H + S)

modhardness = (hardflux-softflux)/(hardflux+softflux)
modhardnesserr = modhardness*(numpy.sqrt(\
(sqrt(hardfluxerr**2 + softfluxerr**2)/(hardflux-softflux))**2 + \
(sqrt(hardfluxerr**2 + softfluxerr**2)/(hardflux+softflux))**2) **2)


# sort hardnesses according to total flux

fluxhard = [[],[],[]]
start = 0

for value in range(len(hardness)):
	# if it isn't the first value...
	if start !=0:
		for comp in range(len(fluxhard[0])): # for each value, from the bottom up...
			if hardflux[value] <= fluxhard[0][comp]: # add below the value if less/equal
				fluxhard[0].insert(comp,totalflux[value])
				fluxhard[1].insert(comp,hardness[value])
				fluxhard[2].insert(comp,hardnesserr[value])
				break
			if comp == len(fluxhard[0]) - 1: # add above final element if > than all
				fluxhard[0].append(totalflux[value])
				fluxhard[1].append(hardness[value])			
				fluxhard[2].append(hardnesserr[value])
	# if it is the first value, just fill that stuff in
	if start == 0:
		fluxhard[0].append(totalflux[value])
		fluxhard[1].append(hardness[value])
		fluxhard[2].append(hardnesserr[value])
		start = 1

# sort modified hardnesses according to hard flux

modfluxhard = [[],[],[]]
start = 0

for value in range(len(modhardness)):
	# if it isn't the first value...
	if start !=0:
		for comp in range(len(modfluxhard[0])): # for each value, from the bottom up...
			if hardflux[value] <= modfluxhard[0][comp]: # add below value if less/equal
				modfluxhard[0].insert(comp,totalflux[value])
				modfluxhard[1].insert(comp,modhardness[value])
				modfluxhard[2].insert(comp,modhardnesserr[value])
				break
			if comp == len(modfluxhard[0]) - 1: # add above final element if > than all
				modfluxhard[0].append(totalflux[value])
				modfluxhard[1].append(modhardness[value])			
				modfluxhard[2].append(modhardnesserr[value])

	# if it is the first value, just fill that stuff in
	if start == 0:
		modfluxhard[0].append(totalflux[value])
		modfluxhard[1].append(modhardness[value])
		modfluxhard[2].append(modhardnesserr[value])
		start = 1


# write to file
outfile1= open(outlocationhard, 'w')

outfile1.write("READ serr 2 \n") # qdp error header

for o in range(len(hardtime)):		# data!
	outfile1.write(str(hardtime[o]))
	outfile1.write("     ")
	outfile1.write(str(hardness[o]))
	outfile1.write("     ")
	outfile1.write(str(hardnesserr[o]))
	outfile1.write("     ")
	outfile1.write(str(totalflux[o]))
	outfile1.write("     ")
	outfile1.write(str(totalfluxerr[o]))
	outfile1.write("\n")


outfile1.close()

outfile2= open(outlocationmodhard, 'w')

outfile2.write("READ serr 2 \n") # qdp error header

for o in range(len(hardtime)):		# data!
	outfile2.write(str(hardtime[o]))
	outfile2.write("     ")
	outfile2.write(str(modhardness[o]))
	outfile2.write("     ")
	outfile2.write(str(modhardnesserr[o]))
	outfile2.write("     ")
	outfile2.write(str(totalflux[o]))
	outfile2.write("     ")
	outfile2.write(str(totalfluxerr[o]))	
	outfile2.write("\n")


outfile2.close()

# plot with pylab

subplot(3,2,1)
errorbar(totaltime,totalflux,yerr=totalfluxerr)
title("H/S")
ylabel("Lightcurve")
#subplot(1,2,1)
#scatter(totaltime,lc)

subplot(3,2,3)
errorbar(hardtime,hardness,yerr=hardnesserr)
ylabel("Hardness Ratio")

subplot(3,2,5)
scatter(fluxhard[0],fluxhard[1])
ylabel("Hardness v. Flux")

subplot(3,2,2)
errorbar(totaltime,totalflux,yerr=totalfluxerr)
title("H-S/H+S")

subplot(3,2,4)
errorbar(hardtime,modhardness,yerr=modhardnesserr)

subplot(3,2,6)
#errorbar(modfluxhard[0],modfluxhard[1],yerr=modfluxhard[2])
#subplot(1,2,2)
scatter(modfluxhard[0],modfluxhard[1])

show()





