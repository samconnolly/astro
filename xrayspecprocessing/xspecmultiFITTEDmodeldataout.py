# xspecmultiFITTEDmodeldataout.py
# Sam Connolly 25/02/13

# Programme to extract xspec model fluxes, counts and the corresponding energies
# from a saved xspec file, and plot them

import os
import pylab as plt
import matplotlib
import numpy as np

# ============== PARAMATERS ====================================================

# file route - directory containing spectra and to contain output
route    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/countbin/"

# output file name
outfile 	= "modelfluxhard.dat"

# input xspec file
infile = "fixXiCountExtract.xcm"

# spectrum to extract
specnum = 10 # number of spectra to extract

# graph?
graph = True

# ==============================================================================

# --- Run Xspec modelling macro and save results ---

# temporary file names
macrofile  = "tmpmacro.tcl"
tmpfile1   = "tmpe"
tmpfile2   = "tmpv"
tmpfile4   = "tmpc"

# set file locations
macrolocation = route + macrofile
outlocation   = route + outfile
tmplocation1  = route + tmpfile1
tmplocation2  = route + tmpfile2
tmplocation4  = route + tmpfile4

here = os.getcwd()

# tcl macro to run on spectra #fit \n\
tclmacro = \
'puts "Starting macro..."\n\
@{0}\n\
puts "starting loop..."\n'.format(infile)

tclmacro = tclmacro + 'while {$i <='

tclmacro = tclmacro + str(specnum) # insert no. model spectra to create

tclmacro = tclmacro + '} {\n'

tclmacro = tclmacro + \
'puts "loop $i"\n\
ignore $i:**-0.5\n\
ignore $i:10.0-**\n\
notice $i:0.5-10.0\n\
set outfile [open {0}$i.dat w]\n\
tclout energies $i\n\
puts $outfile $xspec_tclout\n\
set outfile [open {1}$i.dat w]\n\
tclout modval $i\n\
puts $outfile $xspec_tclout\n\
set outfile [open {2}$i.dat w]\n'.format(tmpfile1,tmpfile2,tmpfile4)

tclmacro = tclmacro + \
'tclout rate $i\n\
puts $outfile $xspec_tclout \n\
puts $xspec_tclout \n\
ignore $i:0.5-2.0\n\
tclout rate $i\n\
puts $outfile $xspec_tclout \n\
puts $xspec_tclout \n\
notice $i:0.5-2.0\n\
ignore $i:2.0-10.0\n\
tclout rate $i\n\
puts $outfile $xspec_tclout \n\
puts $xspec_tclout \n\
incr i;}\n\
quit\n'

print tclmacro

#========================================================

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

flux    = [[] for x in range(specnum)]
energy  = [[] for x in range(specnum)]
counts  = [[],[],[]]

for s in range(specnum):

	# counts

	tmp4 = open(tmplocation4 + str(s+1) + '.dat', 'r')

	lineNumber = 1

	for line in tmp4:

		if lineNumber == 1:
			total = float(line.split()[2])
		 
		if lineNumber == 2:
			hard = float(line.split()[2])

		if lineNumber == 3:
			soft = float(line.split()[2])

		lineNumber += 1

	tmp4.close()

	counts[0].append(total)
	counts[1].append(soft)
	counts[2].append(hard)

	on = 0

	# energy

	tmp1 = open(tmplocation1 + str(s+1) + '.dat', 'r')

	for line in tmp1:
		linedata = line.split()
	
		for datum in linedata:

			if float(datum) >= 0.5:
		
				energy[s].append(float(datum))

			else:
				on += 1

	tmp1.close()

	count = 0

	# flux
	
	tmp2 = open(tmplocation2 + str(s+1) + '.dat', 'r')

	for line in tmp2:
		linedata = line.split()

		for datum in linedata:

			if count >= on:
				flux[s].append(float(datum)*200.0) # *200 converts from 
													  # cnts cm^-2 s^-1 bin^-1 to 
			count += 1								  # cnts cm^-2 s^-1 keV^-1

	tmp2.close()


# delete temporary data files
#os.system("unalias rm")
#os.system("rm tmp*")

for y in range(len(energy)):
	energy[y].pop(0)

hardness = []

for x in range(len(counts[1])):

	h = (counts[2][x]-counts[1][x])/(counts[2][x]+counts[1][x])
	hardness.append(h)

# plot data (logplot)

print counts[1]
print counts[2]
print hardness

if graph:

	fig = plt.figure()

	ax = fig.add_subplot(3,1,1)

	ax.set_yscale('log')
	ax.set_xscale('log')

	ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	for t in range(specnum):
	
		plt.plot(energy[t],flux[t])

	ax = fig.add_subplot(3,1,2)

	plt.scatter(counts[2],hardness)

	ax = fig.add_subplot(3,1,3)

	plt.scatter(counts[2],counts[1])

	plt.show()



















