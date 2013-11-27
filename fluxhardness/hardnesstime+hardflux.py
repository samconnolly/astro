# Import packages

from pylab import *
import numpy as numpy
#
#===============================================================================
# Create Hardness-time files of two formats and hardness-hard flux files, 
# with the lightcurve for comparison,
# from two lighcurves of different energies, and plots 
#===============================================================================

# ========================== PARAMATERS ========================================

# read variables
tmin = 0.0
tmax = 7000.0

objectname = "NGC1365"

# =========================== File Routes ======================================

#   File routes
route           	= \
"/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/lightcurve"
energysoftroute  	= "/refined/"
energyhardroute  	= "/refined/"
energytotalroute 	= "/refined/"
outroutehard     	= "/hardnessratio/"
outroutemodhard  	= "/modhardnessratio/"
outroutehardflux    	= "/hardnessratio/"
outroutemodhardflux 	= "/modhardnessratio/"

# file names
energysoftfname 	= objectname+"_lcurve_3_gti_0.5-2keV.qdp"
energyhardfname		= objectname+"_lcurve_3_gti_2-10keV.qdp"
energytotalfname    	= objectname+"_lcurve_3_gti_0.5-10keV.qdp"

outfnamehard   		= objectname+"_lcurve_gti_hard.qdp"
outfnamemodhard 	= objectname+"_lcurve_gti_modhard.qdp"
outfnamehardflux   	= objectname+"_flux_gti_hard.qdp"
outfnamemodhardflux	= objectname+"_flux_gti_modhard.qdp"

# ==============================================================================

# create file routes
energysoftlocation 		= route+energysoftroute+energysoftfname
energyhardlocation 		= route+energyhardroute+energyhardfname
energytotallocation 	= route+energytotalroute+energytotalfname
outlocationhard     	= route+outroutehard+outfnamehard
outlocationmodhard  	= route+outroutemodhard+outfnamemodhard
outlocationhardflux   	= route+outroutehardflux+outfnamehardflux
outlocationmodhardflux	= route+outroutemodhardflux+outfnamemodhardflux


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
sumerr = sqrt(hardfluxerr**2 + softfluxerr**2)
modhardnesserr = modhardness*(numpy.sqrt(\
(sumerr/(hardflux-softflux))**2 + (sumerr/(hardflux+softflux))**2 ) )

# sort hardnesses according to hard flux

fluxhard = [[],[],[]]
start = 0

for value in range(len(hardness)):
	# if it isn't the first value...
	if start !=0:
		for comp in range(len(fluxhard[0])): # for each value, 
						     # from the bottom up...
			if hardflux[value] <= fluxhard[0][comp]: # add below the
							   # value if less/equal
				fluxhard[0].insert(comp,hardflux[value])
				fluxhard[1].insert(comp,hardness[value])
				fluxhard[2].insert(comp,hardnesserr[value])
				break
			if comp == len(fluxhard[0]) -1: # add after last element
							# if > than all
				fluxhard[0].append(hardflux[value])
				fluxhard[1].append(hardness[value])			
				fluxhard[2].append(hardnesserr[value])
	# if it is the first value, just fill that stuff in
	if start == 0:
		fluxhard[0].append(hardflux[value])
		fluxhard[1].append(hardness[value])
		fluxhard[2].append(hardnesserr[value])
		start = 1

# sort modified hardnesses according to hard flux

modfluxhard = [[],[],[]]
start = 0

for value in range(len(modhardness)):
	# if it isn't the first value...
	if start !=0:
		for comp in range(len(modfluxhard[0])): # for each value, 
							# from the bottom up...
			if hardflux[value] <= modfluxhard[0][comp]: # add below 
							   # value if less/equal
				modfluxhard[0].insert(comp,hardflux[value])
				modfluxhard[1].insert(comp,modhardness[value])
				modfluxhard[2].insert(comp,modhardnesserr[value])
				break
			if comp == len(modfluxhard[0]) -1: # add after last 
							 # element if > than all
				modfluxhard[0].append(hardflux[value])
				modfluxhard[1].append(modhardness[value])			
				modfluxhard[2].append(modhardnesserr[value])

	# if it is the first value, just fill that stuff in
	if start == 0:
		modfluxhard[0].append(hardflux[value])
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
	outfile1.write(str(hardflux[o]))
	outfile1.write("     ")
	outfile1.write(str(hardfluxerr[o]))
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
	outfile2.write(str(hardflux[o]))
	outfile2.write("     ")
	outfile2.write(str(hardfluxerr[o]))	
	outfile2.write("\n")

outfile3= open(outlocationmodhardflux, 'w')

outfile3.write("READ serr 2 \n") # qdp error header

for o in range(len(modfluxhard[0])):		# data!
	outfile3.write(str(modfluxhard[0][o]))
	outfile3.write("     ")
	outfile3.write(str(modfluxhard[1][o]))
	outfile3.write("     ")
	outfile3.write(str(modfluxhard[2][o]))
	outfile3.write("\n")

outfile3.close()

outfile4= open(outlocationhardflux, 'w')

outfile4.write("READ serr 2 \n") # qdp error header

for o in range(len(fluxhard[0])):		# data!
	outfile4.write(str(fluxhard[0][o]))
	outfile4.write("     ")
	outfile4.write(str(fluxhard[1][o]))
	outfile4.write("     ")
	outfile4.write(str(fluxhard[2][o]))
	outfile4.write("\n")

outfile4.close()

# plot with pylab

#subplot(3,2,1)
#errorbar(totaltime,totalflux,yerr=totalfluxerr)
#title("H/S")
#ylabel("Lightcurve")
#subplot(1,2,1)
#scatter(totaltime,lc)

#subplot(3,2,3)
#errorbar(hardtime,hardness,yerr=hardnesserr)
#ylabel("Hardness Ratio")

#subplot(3,2,5)
#errorbar(fluxhard[0],fluxhard[1],yerr=fluxhard[2])
#ylabel("Hardness v. Flux")

subplot(3,1,1)
errorbar(totaltime,totalflux,yerr=totalfluxerr)
title("H-S/H+S")
ylabel("Lightcurve")
subplot(3,1,2)
errorbar(hardtime,modhardness,yerr=modhardnesserr)
ylabel("Hardness Ratio")
subplot(3,1,3)
errorbar(modfluxhard[0],modfluxhard[1],yerr=modfluxhard[2])
ylabel("Hardness v. Flux")
#subplot(1,2,2)
#scatter(modfluxhard[0],modfluxhard[1])

show()





