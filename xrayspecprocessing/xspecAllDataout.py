# xspecAllDataout.py
# Sam Connolly 25/02/13

# Programme to extract xspec data, errors and model fluxes, save them and plot them

import os
import pylab as plt
import matplotlib
import numpy as np

# ============== PARAMATERS ====================================================

# file route - directory containing spectra and to contain output
route    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/gtihardbin/"

# input xspec files
infile  = "allspectra11.xcm"
modfile = "absoribinmodelfixXi.xcm"

# spectrum to extract
specnums = 11 # snumber of spectra to extract

# energies used
choose = True
emin = 0.5
emax = 10.0

# graphs?
modGraph  = True
dataGraph = True

# ==============================================================================

def Extract(specnum):

	# output file names
	outfile 	= "spec{0}.dat".format(specnum)
	modoutfile	= "spec{0}mod.dat".format(specnum)

	# --- Run Xspec modelling macro and save results ---

	# temporary file names
	macrofile  = "tmpmacro.tcl"
	tmpfile1   = "tmp1.dat"
	tmpfile2   = "tmp2.dat"
	tmpfile3   = "tmp3.dat"
	tmpfile4   = "tmp4.dat"
	tmpfile5   = "tmp5.dat"
	tmpfile6   = "tmp6.dat"


	# set file locations
	macrolocation  = route + macrofile
	outlocation    = route + outfile
	modoutlocation = route + modoutfile
	tmplocation1   = route + tmpfile1
	tmplocation2   = route + tmpfile2
	tmplocation3   = route + tmpfile3
	tmplocation4   = route + tmpfile4
	tmplocation5   = route + tmpfile5
	tmplocation6   = route + tmpfile6

	here = os.getcwd()

	# tcl macro to run on spectra
	tclmacro = \
	'puts "Starting macro..."\n\
	@{1}\n\
	@{8}\n\
	fit \n\
	set outfile [open {0} w]\n\
	tclout energies {2}\n\
	puts $outfile $xspec_tclout\n\
	set outfile [open {3} w]\n\
	tclout modval {2}\n\
	puts $outfile $xspec_tclout \n\
	set outfile [open {4} w]\n\
	tclout plot ufspec x {2}\n\
	puts $outfile $xspec_tclout \n\
	set outfile [open {5} w]\n\
	tclout plot ufspec xerr {2}\n\
	puts $outfile $xspec_tclout \n\
	set outfile [open {6} w]\n\
	tclout plot ufspec y {2}\n\
	puts $outfile $xspec_tclout \n\
	set outfile [open {7} w]\n\
	tclout plot ufspec yerr {2}\n\
	puts $outfile $xspec_tclout \n\
	quit\n'.format(tmpfile1,infile,specnum,tmpfile2,tmpfile3,tmpfile4,tmpfile5,tmpfile6,modfile)

	#print tclmacro

	# create temporary macro file
	macrofile= open(macrolocation, 'w')
	macrofile.write(str(tclmacro))
	macrofile.close()

	# run tcl script in xspec
	os.chdir(route)
	os.system("xspec - tmpmacro.tcl")

	# delete temporary macro
	os.remove(macrolocation)

	# ---- create output file from tmp data files ----

	# read in data from tmp data files

	tmp3 = open(tmplocation3, 'r')

	for line in tmp3:
		noticed = line.split()[0]
		 
	tmp3.close()

	flux    	= []
	energy 		= []
	indices		= []
	dEnergy 	= [[],[]]
	dFlux		= [[],[]]

	# model energy
	tmp1 = open(tmplocation1, 'r')

	for line in tmp1:
		linedata = line.split()
	
		for index in range(len(linedata)):
		
			if float(linedata[index]) >= emin and float(linedata[index]) <= emax:	
				energy.append(float(linedata[index]))
				indices.append(index)

	tmp1.close()

	# model flux
	tmp2 = open(tmplocation2, 'r')

	for line in tmp2:
		linedata = line.split()

		for index in indices:
			flux.append(float(linedata[index])*200.0) # *200 converts from 
													  # cnts cm^-2 s^-1 bin^-1 to 
													  # cnts cm^-2 s^-1 keV^-1

	tmp2.close()

	# data energy
	tmp3 = open(tmplocation3, 'r')

	for line in tmp3:
		linedata = line.split()

		for index in range(len(linedata)):
				dEnergy[0].append(float(linedata[index]))

	tmp3.close()

	# data energy error
	tmp4 = open(tmplocation4, 'r')

	for line in tmp4:
		linedata = line.split()

		for index in range(len(linedata)):
				dEnergy[1].append(float(linedata[index]))

	tmp4.close()

	# data flux
	tmp5 = open(tmplocation5, 'r')

	for line in tmp5:
		linedata = line.split()

		for index in range(len(linedata)):
				dFlux[0].append(float(linedata[index]))

	tmp5.close()

	# data flux error
	tmp6 = open(tmplocation6, 'r')

	for line in tmp6:
		linedata = line.split()

		for index in range(len(linedata)):
				dFlux[1].append(float(linedata[index]))

	tmp6.close()


	# delete temporary data files
	os.remove(tmplocation1)
	os.remove(tmplocation2)
	os.remove(tmplocation3)
	os.remove(tmplocation4)
	os.remove(tmplocation5)
	os.remove(tmplocation6)

	# create new, combined data files (model and data)

	# data
	output = open(outlocation, 'w')

	output.write("Model Energy\tModel Flux\tData Energy\tEnergy Error\tData Flux\n\tFlux Error")	


	for i in range(len(dFlux[0])):
		output.write(str(dEnergy[0][i]))
		output.write("\t")
		output.write(str(dEnergy[1][i]))
		output.write("\t")
		output.write(str(dFlux[0][i]))
		output.write("\t")
		output.write(str(dFlux[1][i]))
		output.write("\n")

	output.close()

	output2 = open(modoutlocation, 'w')

	output2.write("Model Energy\tModel Flux\tData Energy\tEnergy Error\tData Flux\n\tFlux Error")	

	for i in range(len(flux)):
		output2.write(str(energy[i]))
		output2.write("\t")
		output2.write(str(flux[i]))
		output2.write("\n")

	output2.close()

	#return to original directory
	os.chdir(here)


	# plot data (logplot)

	graphn = 0
	gnum   = 1

	if modGraph:

		graphn += 1

	if dataGraph:

		graphn += 1

	if graphn > 0:

		fig = plt.figure()

		if modGraph:

			ax = fig.add_subplot(graphn,1,1)

			ax.set_yscale('log')
			ax.set_xscale('log')

			ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

			plt.plot(energy,flux)

			gnum +=1

		if dataGraph:

			ax = fig.add_subplot(graphn,1,gnum)

			ax.set_yscale('log')
			ax.set_xscale('log')

			ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
	
			print len(dEnergy[0]), len(dFlux[0])

			plt.errorbar(dEnergy[0],dFlux[0], xerr = dEnergy[1], yerr = dFlux[1],
							marker = 'o', color = 'red',
				ecolor = 'grey',capsize = 0)

			plt.show()

for s in range(specnums):

	Extract(s + 1)

