# xspecmultimodeldataout.py
# Sam Connolly 12/03/13

# Programme to extract xspec model fluxes and the corresponding energies of 
# multiple models created automatically within xspec, with one varying parameter 
# then calculate, save and plot hardness V count rate and hard, soft counts
# (so far allows 2 power laws, one with neutral or ionised absorption, galactic
# absorption, and a gaussian 
# (requires an arbitrary spectrum file)

import os
import pylab as plt
import matplotlib
import numpy as np

# ============== PARAMATERS ====================================================

# file route - directory containing spectra and to contain output
outroute = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/binsum/"

# output data file name
outfile  = "multimodelhardness.dat"
specfile = "0.1229-0.2517.summed.pha"

# number of model spectra to extract
specnum = 50 # spectrum number of model to extract

# energy range 

emin 			= 0.5 #0.5
emax 			= 10.0 #0.8
hardnesssplit 	= 2.0

# graph the data?
graph = True

# Log range? necessary if the dependance of the varied parameter is logorithmic,
#for even 'sampling'
logrange = True

#--- Model parameters (STRING) -------------------------------------------------

# SET VARIABLE PARAMETER TO '$var' if logrange = false, else '[expr exp($var)]'

varstart  = 4.0 # lower value in range for variable parameter NOT ZERO!
varend    = 99.999 # upper value in range for variable parameter

# galactic absorption
gwabs 		= True
galnH 		= "1.39E-2"

# power laws (2nd optional)
phindex		= "1.9"
norm1		= "2.0E-04"
pow2		= True
norm2		= "1.07E-02"

# gaussian
gauss		= True
gaussE		= "0.776"
gaussS		= "0.157"
gaussnorm	= "1.775E-04"

# cold absorption
wabs 		= False
nH 			= '[expr exp($var)]'

#absori
absori		= True
nH			= '[expr exp($var)]'
Tabs		= "3E+4"
ion			= "10"
z			= "0.005569"
Fe			= "3.5"

#===============================================================================


if logrange == True:
	# logarithmic range to ensure even spacing of spectra in log space

	increment = str((np.log(varend) - np.log(varstart))/float(specnum))
	varstart  = str(np.log(varstart))

if logrange == False:

	increment = str((varend - varstart)/float(specnum))
	varstart  = str(varstart)

#------ Model command construction ---------------------------------------------

model = "mo "
params = ""

if gwabs:
	model = model + "wabs*"
	params = params + " & " + galnH	

model = model + "pow"
params = params + " & " + phindex
params = params + " & " + norm1

if gauss:
	model = model + " + gauss"
	params = params + " & " + gaussE
	params = params + " & " + gaussS
	params = params + " & " + gaussnorm

if pow2:

	if wabs:
		model = model + " + wabs*"
		params = params + " & " + nH

	if absori:
		model = model + " + absori*"
		params = params + " & " + phindex
		params = params + " & " + nH
		params = params + " & " + Tabs
		params = params + " & " + ion
		params = params + " & " + z
		params = params + " & " + Fe
	 
	model = model + "pow"
	params = params + " & " + phindex
	params = params + " & " + norm2

comm = model + params


#----------- Create xspec macro ------------------------------------------------

# temporary file names
macrofile  		= "tmpmacro.tcl"
tmpfileenergy   = "tmpenergy"
tmpfilevalue   	= "tmpvalue"

# set file locations
macrolocation 		= outroute + macrofile
outlocation   		= outroute + outfile
tmplocationenergy  	= outroute + tmpfileenergy
tmplocationvalue  	= outroute + tmpfilevalue  

here = os.getcwd() # get current working directory to return to

# set up loop values
tclmacro = \
'puts "Starting macro..."\n\
cpd null\n\
data {0}\n\
set i 1\n\
set var {1}\n\
set increment {2}\n'.format(specfile, varstart,increment)

tclmacro = tclmacro + \
'while {$i <= ' # loop start

tclmacro = tclmacro + str(specnum +1) # insert no. model spectra to create

tclmacro = tclmacro + \
'} {;\n'

tclmacro = tclmacro + comm # insert model command

# extract data to tmp files
tclmacro = tclmacro + \
'\nset outfile [open {0}$i.dat w]\n\
tclout energies 1\n\
puts $outfile $xspec_tclout\n\
set outfile [open {1}$i.dat w]\n\
tclout modval 1\n\
puts $outfile $xspec_tclout \n\
set var [expr $var + $increment]'\
.format(tmpfileenergy,tmpfilevalue)

# loop end
tclmacro = tclmacro + \
'; incr i;} \n\
quit'

#print tclmacro

# create temporary macro file
macrofile= open(macrolocation, 'w')
macrofile.write(str(tclmacro))
macrofile.close()

# run tcl script in xspec
os.chdir(outroute)
os.system("xspec - tmpmacro.tcl")

# delete temporary macro
os.remove(macrolocation)


# ---- create output file from tmp data files ----

# read in data from tmp data files

flux    = [[] for i in range(specnum)]
energy  = [[] for i in range(specnum)]
indices = [[] for i in range(specnum)]

for spec in range(specnum):

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


# create new, combined data file

output = open(outlocation, 'w')

for x in range(specnum):
	output.write("Energy {0}\t".format(x +1) + "Flux {0}\t".format(x +1))	

output.write("\n")

for i in range(len(flux[0])):
	for j in range(specnum):
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
hardness 	= []

for y in range(specnum):
	s = np.trapz(flux[y][:splitindex])
	h = np.trapz(flux[y][splitindex:])

	soft.append(s)
	hard.append(h)
	hardness.append((h - s) / (h + s))

print comm

# plot data (logplot)

if graph:

	# model spectra
	fig = plt.figure()

	ax = fig.add_subplot(3,1,1)

	ax.set_yscale('log')
	ax.set_xscale('log')

	ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	for p in range(specnum):

		plt.plot(energy[p],flux[p])

	plt.xlim([emin,emax])

	# hardness v hard counts
	fig.add_subplot(3,1,2)

	plt.plot(hard, hardness, marker='.', color = 'red')

	# hardness v hard counts
	fig.add_subplot(3,1,3)

	plt.plot(hard, soft, marker='.', color = 'red')

	plt.show()

