# xspecmultispecfitdataout.py
# Sam Connolly 11/03/13

# Programme to extract xspec model fluxes and the corresponding energies of 
# multiple models fitted to real spectra in a saved xspec file of spectra and
# fits, or a seperate model file, ignoring ignored channels or chosen energies, 
# then calculate, save and plot hardness V count rate and hard, soft counts

import os
import pylab as plt
import matplotlib
import numpy as np

# ============== PARAMATERS ====================================================

# file route - directory containing spectra and to contain output
route    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/high/"

# output data file name
outfile 	= "multispecfithardness.dat"

# input xspec file(s)
infile = "normtestspec.xcm"			# spectrum file
modelfile = "normtestmodel.xcm"		# 'None' if same as infile

# energy range (overrides those ignored/noticed if choose == True) 
# (used for plots)

choose = True
cemin = 0.5
cemax = 2.0

hardnesssplit = 2.0

# graph?
graph = True

# ==============================================================================

# --- Run Xspec modelling macro and save results ---

# temporary file names
macrofile  		= "tmpmacro.tcl"
tmpfileenergy   = "tmpenergy"
tmpfilevalue   	= "tmpvalue"
tmpfilenotice   = "tmpnotice"
tmpfilegrpnum  	= "tmpgrpnum.dat"

# set file locations
macrolocation 		= route + macrofile
outlocation   		= route + outfile
tmplocationenergy  	= route + tmpfileenergy
tmplocationvalue  	= route + tmpfilevalue  
tmplocationnotice  	= route + tmpfilenotice   
tmplocationgrpnum  	= route + tmpfilegrpnum   

here = os.getcwd()

# tcl macro to run on spectra
tclmacro = \
'puts "Starting macro..."\n\
cpd null\n\
@{0}\n'.format(infile)

if modelfile:

	tclmacro = tclmacro + '@{0}\n'.format(modelfile)

tclmacro = tclmacro + \
'query yes \n\
fit \n\
set outfile [open {0} w]\n\
tclout datagrp\n\
set grpnum $xspec_tclout\n\
puts $outfile $grpnum\n'.format(tmpfilegrpnum)

tclmacro = tclmacro + \
'set i 1\n\
while {$i <= $grpnum} {;\n'

tclmacro = tclmacro + \
'puts "spectrum $i of $grpnum$"\n\
set outfile [open {0}$i.dat w]\n\
tclout energies $i\n\
puts $outfile $xspec_tclout\n\
set outfile [open {1}$i.dat w]\n\
tclout modval $i\n\
puts $outfile $xspec_tclout \n\
set outfile [open {2}$i.dat w]\n\
tclout noticed energy $i\n\
puts $outfile $xspec_tclout \n'\
.format(tmpfileenergy,tmpfilevalue,tmpfilenotice)

tclmacro = tclmacro + \
'; incr i;} \n\
quit\n'

#print tclmacro

# create temporary macro file
macrofile= open(macrolocation, 'w')
macrofile.write(str(tclmacro))
macrofile.close()

# run tcl script in xspec
os.chdir(route)
#os.system("headasinit") # personal macro to initialise headas software/xspec
os.system("xspec - tmpmacro.tcl")

# delete temporary macro
os.remove(macrolocation)

# ---- create output file from tmp data files ----

# extract number of spectra

grpnumfile = open(tmplocationgrpnum, 'r')

for line in grpnumfile:
	grpnum = int(line.split()[0])

grpnumfile.close()

# delete temporary data file
os.remove(tmplocationgrpnum)

# read in data from tmp data files

flux    = [[] for i in range(grpnum)]
energy  = [[] for i in range(grpnum)]
indices = [[] for i in range(grpnum)]

for spec in range(0,grpnum):

	tmplocation = tmplocationnotice + str(spec + 1) + ".dat"

	notice = open(tmplocation, 'r')

	for line in notice:
		noticed = line.split()[0]
		 
	notice.close()

	# delete temporary data file
	os.remove(tmplocation)

	emin = ""
	emax = ""
	dash = False

	for character in noticed:

		if dash == True:
			emax = emax + character

		if dash == False:
			if character == "-":
				dash = True

			else:
				emin = emin + character

	emin = float(emin)
	emax = float(emax)

	if choose == True:

		emin = cemin
		emax = cemax

	tmplocation = tmplocationenergy + str(spec + 1) + ".dat"

	energyf = open(tmplocation, 'r')

	for line in energyf:
		linedata = line.split()
	
		for index in range(len(linedata)):
		
			if float(linedata[index]) >= emin and float(linedata[index]) <= emax:	
				energy[spec].append(float(linedata[index]))
				indices[spec].append(index)

	energyf.close()

	# delete temporary data file
	os.remove(tmplocation)

	tmplocation = tmplocationvalue + str(spec + 1) + ".dat"

	fluxf = open(tmplocation, 'r')

	for line in fluxf:
		linedata = line.split()

		for index in indices[spec]:
			flux[spec].append(float(linedata[index])*200.0) # *200 converts from 
													 # cnts cm^-2 s^-1 bin^-1 to 
													 # cnts cm^-2 s^-1 keV^-1

	fluxf.close()

	# delete temporary data file
	os.remove(tmplocation)

#print grpnum
#print len(energy), len(flux), len(energy[0]), len(flux[0])

# create new, combined data file

output = open(outlocation, 'w')

for x in range(grpnum):
	output.write("Energy {0}\t".format(x +1) + "Flux {0}\t".format(x +1))	

output.write("\n")

for i in range(len(flux[0])):
	for j in range(grpnum):
		output.write(str(energy[j][i]))
		output.write("\t")
		output.write(str(flux[j][i]))
		output.write("\t")

	output.write("\n")

output.close()

#return to original directory
os.chdir(here)

# calculate hardness

splitindex = 0

for i in range(len(energy[0])):

	if energy[0][i] < hardnesssplit:
		if i > splitindex:

			splitindex = i

splitindex += 1

hard 		= []
soft 		= []
total		= []
hardness 	= []

for y in range(grpnum):
	s = sum(flux[y][:splitindex]) #np.trapz(flux[y][:splitindex])
	h = sum(flux[y][splitindex:]) #np.trapz(flux[y][splitindex:])
	t = sum(flux[y]) #np.trapz(flux[y])

	soft.append(s)
	hard.append(h)
	total.append(t)
	hardness.append((h - s) / (h + s))

# plot data (logplot)

if graph:

	# model spectra
	fig = plt.figure()

	ax = fig.add_subplot(3,1,1)

	ax.set_yscale('log')
	ax.set_xscale('log')

	ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	for p in range(grpnum):

		plt.plot(energy[p],flux[p])

	plt.xlim([cemin,cemax])

	# hardness v hard counts
	fig.add_subplot(3,1,2)

	plt.plot(hard, hardness, marker='.', color = 'red')

	# hardness v hard counts
	fig.add_subplot(3,1,3)

	plt.plot(hard, soft, marker='.', color = 'red')

	print hard, soft, total

	plt.show()




