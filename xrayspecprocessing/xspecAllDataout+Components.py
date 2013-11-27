# xspecAllDataout+Components.py
# Sam Connolly 19/09/13

# Programme to extract xspec data, errors and model fluxes, save them and plot them
# Also, the components of each model are exracted. This has to be the particular
# model I use at the moment.

# USE PLOTSPECTRA>PY TO PLOT THE RESULTS!

import os
import pylab as plt
import matplotlib

# ============== PARAMATERS ====================================================

# file route - directory containing spectra and to contain output
route    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365/spectra/gtihardbin/"

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
compGraph = True

# ==============================================================================

def Extract(specnum):

	# output file names
	outfile 	= "spec{0}.dat".format(specnum)
	modoutfile	= "spec{0}mod.dat".format(specnum)
	comp1outfile	= "spec{0}comp1.dat".format(specnum)
	comp2outfile	= "spec{0}comp2.dat".format(specnum)
	comp3outfile	= "spec{0}comp3.dat".format(specnum)

	# --- Run Xspec modelling macro and save results ---

	# temporary file names
	macrofile  = "tmpmacro.tcl"
	tmpfile1   = "tmp1.dat"
	tmpfile2   = "tmp2.dat"
	tmpfile3   = "tmp3.dat"
	tmpfile4   = "tmp4.dat"
	tmpfile5   = "tmp5.dat"
	tmpfile6   = "tmp6.dat"
	tmpfile7   = "tmp7.dat"

	# set file locations
	macrolocation  = route + macrofile
	outlocation    = route + outfile
	modoutlocation = route + modoutfile
	comp1outlocation = route + comp1outfile
	comp2outlocation = route + comp2outfile
	comp3outlocation = route + comp3outfile
	tmplocation1   = route + tmpfile1
	tmplocation2   = route + tmpfile2
	tmplocation3   = route + tmpfile3
	tmplocation4   = route + tmpfile4
	tmplocation5   = route + tmpfile5
	tmplocation6   = route + tmpfile6
	tmplocation7   = route + tmpfile7

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
	set outfile [open {9} w]\n\
	set params ""\n'.format(tmpfile1,infile,specnum,tmpfile2,tmpfile3,tmpfile4,\
					tmpfile5,tmpfile6,modfile,tmpfile7)

	tclmacro = tclmacro +\
 	'for {set i 1} {$i<=14} {incr i} {\n'

	tclmacro = tclmacro +\
 	'set index [expr $i + [expr 14 * [expr {0} - 1]]]\n\
	tclout param $index\n\
    append params $xspec_tclout "\\n"\n'.format(specnum)

 	tclmacro = tclmacro +\
 	'}\n\
	puts $outfile $params \n\
	quit\n'

	print tclmacro

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
	params		= []

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

	# parameter values
	tmp7 = open(tmplocation7, 'r')

	for line in tmp7:
		linedata = line.split()

		if len(linedata) > 0:
			params.append(float(linedata[0]))

	tmp7.close()


	# delete temporary data files
	os.remove(tmplocation1)
	os.remove(tmplocation2)
	os.remove(tmplocation3)
	os.remove(tmplocation4)
	os.remove(tmplocation5)
	os.remove(tmplocation6)
	os.remove(tmplocation7)

	# create individual components in xspec to extract them

	tclmacro2 = \
	'@{1}\n\
	set outfile [open {0} w]\n\
	mo wabs*pow & {5} & {9} & {10}\n\
	tclout modval {2}\n\
	puts $outfile $xspec_tclout\n\
	set outfile [open {3} w]\n\
	mo wabs*absori*pow & {5} & {11} & {12} & {13} & \
							{14} & {15} & {16} & {17} & {18}\n\
	tclout modval {2}\n\
	puts $outfile $xspec_tclout \n\
	set outfile [open {4} w]\n\
	mo wabs*gauss & {5} & {6} & {7} & {8}\n\
	tclout modval {2}\n\
	puts $outfile $xspec_tclout \n\
	quit\n'.format(tmpfile1,infile,specnum,tmpfile2,tmpfile3,params[0],\
					params[1],params[2],params[3],params[4],params[5],params[6],\
						params[7],params[8],params[9],params[10],params[12],\
							params[12],params[13])

	# create temporary macro file
	macrofile= open(macrolocation, 'w')
	macrofile.write(str(tclmacro2))
	macrofile.close()

	# run macro
	os.system("xspec - tmpmacro.tcl")

	# delete temporary macro
	os.remove(macrolocation)

	# read component data out

	Cunabs = []
	Cabs   = []
	Cgauss = []

	# parameter values

	# unabsorbed component
	tmp1 = open(tmplocation1, 'r')

	for line in tmp1:
		linedata = line.split()

		for index in indices:
				Cunabs.append(float(linedata[index])*200.)

	tmp1.close()

	# absorbed component
	tmp2 = open(tmplocation2, 'r')

	for line in tmp2:
		linedata = line.split()

		for index in indices:
				Cabs.append(float(linedata[index])*200.)

	tmp2.close()


	# unabsorbed component
	tmp3 = open(tmplocation3, 'r')

	for line in tmp3:
		linedata = line.split()

		for index in indices:
				Cgauss.append(float(linedata[index])*200.)

	tmp3.close()

	print len(Cunabs),len(Cabs),len(Cgauss)

	# delete temporary data files
	os.remove(tmplocation1)
	os.remove(tmplocation2)
	os.remove(tmplocation3)

	# create new, combined data files (model, data, components)

	# data
	output = open(outlocation, 'w')

	output.write("Energy\tEnergy Error\tFlux\tFlux Error\n")	


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

	# model
	output2 = open(modoutlocation, 'w')

	output2.write("Energy\tFlux\n")	

	for i in range(len(flux)):
		output2.write(str(energy[i]))
		output2.write("\t")
		output2.write(str(flux[i]))
		output2.write("\n")

	output2.close()

	# component 1
	output3 = open(comp1outlocation, 'w')

	output3.write("Energy\tFlux\t\n")	

	for i in range(len(flux)):
		output3.write(str(energy[i]))
		output3.write("\t")
		output3.write(str(Cunabs[i]))
		output3.write("\n")

	output3.close()

	# component 2
	output4 = open(comp2outlocation, 'w')

	output4.write("Energy\tFlux\t\n")	

	for i in range(len(flux)):
		output4.write(str(energy[i]))
		output4.write("\t")
		output4.write(str(Cabs[i]))
		output4.write("\n")

	output4.close()

	# component 3
	output5 = open(comp3outlocation, 'w')

	output5.write("Energy\tFlux\t\n")	

	for i in range(len(flux)):
		output5.write(str(energy[i]))
		output5.write("\t")
		output5.write(str(Cgauss[i]))
		output5.write("\n")

	output5.close()

	#return to original directory
	os.chdir(here)


	# plot data (logplot)

	graphn = 0
	gnum   = 1

	if modGraph:

		graphn += 1

	if dataGraph:

		graphn += 1

	if compGraph:

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
	
			plt.errorbar(dEnergy[0],dFlux[0], xerr = dEnergy[1], yerr = dFlux[1],
							marker = 'o', color = 'red',
				ecolor = 'grey',capsize = 0)

			gnum +=1

		if compGraph:

			ax = fig.add_subplot(graphn,1,gnum)

			ax.set_yscale('log')
			ax.set_xscale('log')

			ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
	
			plt.plot(energy,Cunabs)
			plt.plot(energy,Cabs)
			plt.plot(energy,Cgauss)

		#plt.show()

for s in range(specnums):

	Extract(s + 1)

