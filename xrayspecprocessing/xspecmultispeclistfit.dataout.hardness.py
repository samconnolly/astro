# xspecmultispecfitdataout.py
# Sam Connolly 11/03/13

# Programme to extract xspec model fluxes and the corresponding energies of 
# a model fitted to a list of real spectra in a text file,
# ignoring ignored channels or chosen energies, 
# then calculate, save and plot hardness V count rate and hard, soft counts

import os
import pylab as plt
import matplotlib
import numpy as np

# ============== PARAMATERS ====================================================

# file route - directory containing spectra and speclist, and to contain output
specroute = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/binsum/"

# output data file name
outfile 	= "multispeclistfithardness.dat"

# input text file (list of spectral file names)
infile = "speclist.txt"			

# energy range to use

choose = True
esoft = 0.5
emid  = 2.0
ehard = 10.0

hardnesssplit = 2.0

# graph?
graph = True

#---- Initial Model parameters (STRING) ----------------------------------------
# + fix to fix

fix = ', -1'

# galactic absorption
gwabs 		= True
galnH 		= "1.39E-2" + fix

# power laws (2nd optional)
phindex		= "1.95" + fix
norm1		= "3.0E-05"
pow2		= True
norm2		= "1.07E-02"

# gaussian
gauss		= True
gaussE		= "0.8" + fix
gaussS		= "0.1" + fix
gaussnorm	= "1E-06"

# cold absorption
wabs 		= False
nH 			= '5' # 10^22

#absori
absori		= True
nH			= '5' # 10^22
Tabs		= "3E+4"
ion			= "10.0"
z			= "0.005569"
Fe			= "3.5"

#===============================================================================

#------ Model command construction ---------------------------------------------

model = "mo "
params = ""
pparams = ''

if gwabs:
	model = model + "wabs*"
	params = params + " & " + galnH	
	pparams = pparams + " Galactic column density: " + galnH + '\n'

model = model + "pow"
params = params + " & " + phindex
params = params + " & " + norm1
pparams = pparams + " Photon index: " + phindex + '\n'
pparams = pparams + " Unabsorbed normalisation: " + galnH + '\n'
if gauss:
	model = model + " + gauss"
	params = params + " & " + gaussE
	params = params + " & " + gaussS
	params = params + " & " + gaussnorm
	pparams = pparams + " Gaussian Energy: " + gaussE + '\n'
	pparams = pparams + " Gaussian FWHM: " + gaussS + '\n'
	pparams = pparams + " Gaussian normalisation: " + gaussnorm + '\n'

if pow2:

	if wabs:
		model = model + " + wabs*"
		params = params + " & " + nH
		pparams = pparams + " Absorption nH: " + nH + '\n'

	if absori:
		model = model + " + absori*"
		params = params + " & " + phindex
		params = params + " & " + nH
		params = params + " & " + Tabs
		params = params + " & " + ion
		params = params + " & " + z
		params = params + " & " + Fe
		pparams = pparams + " Absorption nH: " + nH + '\n'
		pparams = pparams + " Absorber temperature: " + Tabs + '\n'
		pparams = pparams + " Absorber ionisation paramater: " + ion + '\n'
		pparams = pparams + " Redshift: " + z + '\n'
		pparams = pparams + " Iron abundance: " + Fe + '\n'
	 
	model = model + "pow"
	params = params + " & " + phindex
	params = params + " & " + norm2
	pparams = pparams + " Absorbed normalisation: " + norm2 + '\n'

comm = model + params

#-- read in spectrum files -----------------------------------------------------
speclocation = specroute+infile

spectra = []

specfile = open(speclocation, 'r')

specnum = 0

for line in specfile:

	spectra.append(line)
	specnum += 1

specfile.close()



#----------- Create xspec macro ------------------------------------------------

# temporary file names
macrofile  		= "tmpmacro.tcl"
tmpfileenergy   = "tmpenergy"
tmpfilevalue   	= "tmpvalue"

# set file locations
macrolocation 		= specroute + macrofile
outlocation   		= specroute + outfile
tmplocationenergy  	= specroute + tmpfileenergy
tmplocationvalue  	= specroute + tmpfilevalue  

here = os.getcwd() # get current working directory to return to
os.chdir(specroute) # change to working directory

flux    = [[] for i in range(specnum)]
energy  = [[] for i in range(specnum)]
indices = [[] for i in range(specnum)]

def macro(specfile, specnum):

	# set up loop values
	tclmacro = \
	'puts "Starting macro..."\n\
	cpd null\n\n\
	data {0}\n\
	ignore **-3\n\
	ignore 8.-**\n'.format(specfile)
	
	tclmacro = tclmacro + comm # insert model command

	# fit model, extract data to tmp files
	tclmacro = tclmacro + \
	'\nquery yes\n\
	fit\n\
	set outfile [open {0}.dat w]\n\
	tclout energies 1\n\
	puts $outfile $xspec_tclout\n\
	set outfile [open {1}.dat w]\n\
	tclout modval 1\n\
	puts $outfile $xspec_tclout \n\
	quit'.format(tmpfileenergy,tmpfilevalue)

	#print tclmacro

	# create temporary macro file
	macrofile= open(macrolocation, 'w')
	macrofile.write(str(tclmacro))
	macrofile.close()

	# run tcl script in xspec

	os.system("xspec - tmpmacro.tcl")

	# delete temporary macro
	os.remove(macrolocation)


	# read in data from tmp data files

	emin = esoft
	emax = ehard

	tmplocation = tmplocationenergy + ".dat"

	energyf = open(tmplocation, 'r')

	for line in energyf:
		linedata = line.split()
	
		for index in range(len(linedata)):
		
			if float(linedata[index]) >= emin and float(linedata[index]) <= emax:	
				energy[specnum].append(float(linedata[index]))
				indices[specnum].append(index)

	energyf.close()

	# delete temporary data file
	os.remove(tmplocation)

	tmplocation = tmplocationvalue + ".dat"

	fluxf = open(tmplocation, 'r')

	for line in fluxf:
		linedata = line.split()

		for index in indices[specnum]:
			flux[specnum].append(float(linedata[index])*200.0) # *200 converts  
													 # cnts cm^-2 s^-1 bin^-1 to 
													 # cnts cm^-2 s^-1 keV^-1

	fluxf.close()

	# delete temporary data file
	os.remove(tmplocation)

#--- Run macro on spectrum list ------------------------------------------------

for s in range(len(spectra)):

	macro(spectra[s],s)

#print specnum
#print len(energy), len(flux), len(energy[0]), len(flux[0])
####################################################

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

	if energy[0][i] < emid:
		if i > splitindex:

			splitindex = i

splitindex += 1

hard 		= []
soft 		= []
total		= []
hardness 	= []

for y in range(specnum):
	print sum(flux[y])
	s = sum(flux[y][:splitindex]) #np.trapz(flux[y][:splitindex])
	h = sum(flux[y][splitindex:]) #np.trapz(flux[y][splitindex:])
	t = sum(flux[y]) #np.trapz(flux[y])

	soft.append(s)
	hard.append(h)
	total.append(t)

	#print s,h,t

	if (s + h) != 0:
		hardness.append((h - s) / (h + s))
	else:
		hardness.append(0)

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

	plt.xlim([esoft,ehard])

	# hardness v hard counts
	fig.add_subplot(3,1,2)

	plt.scatter(hard, hardness, marker='.', color = 'red')

	# hardness v hard counts
	fig.add_subplot(3,1,3)

	plt.scatter(hard, soft, marker='.', color = 'red')

	plt.show()




