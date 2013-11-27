# xspecmultispecfit.dataout.hardness.FluxDifference.py
# Sam Connolly 22/04/13

# Programme to extract xspec model fluxes and the corresponding energies of 
# a model fitted to a list of real spectra in a text file,
# ignoring ignored channels or chosen energies, 
# then calculate, save and plot hardness V count rate and hard, soft counts
# AND ALSO, extract the absorbed flux by dividing the absorbed powerlaw flux of
# a non-absorbed power law by the same normalisation,
# then plot this against the total unabsorbed flux

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

# check each fit before continuing?

fitcheck = False

# graph?
graph = True

logabs = False # log the absorption v unabsorbed flux graph?

#---- Initial Model parameters (STRING) ----------------------------------------
# + fix to fix

fix = ', -1'

# galactic absorption
gwabs 		= True
galnH 		= "1.39E-2" + fix

# power laws (2nd optional)
phindex		= "1.95" + fix
norm1		= "3.0E-04"
pow2		= True
norm2		= "5.0E-03"

# gaussian
gauss		= True
gaussE		= "0.8" + fix
gaussS		= "0.1" + fix
gaussnorm	= "1E-04"

# cold absorption
wabs 		= False
nH 			= '5' # 10^22

#absori
absori		= True
nH			= '5' # 10^22
Tabs		= "3E+4"
ion			= "5.0"
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
tmpparamval		= "tmpparamval"

# set file locations
macrolocation 		= specroute + macrofile
outlocation   		= specroute + outfile
tmplocationenergy  	= specroute + tmpfileenergy
tmplocationvalue  	= specroute + tmpfilevalue  
tmplocationparam	= specroute + tmpparamval

here = os.getcwd() # get current working directory to return to
os.chdir(specroute) # change to working directory

flux    = [[] for i in range(specnum)]
energy  = [[] for i in range(specnum)]
indices = [[] for i in range(specnum)]
paramlist	= [[],[],[],[],[]]

def macro(specfile, specnum):

	# set up loop values
	tclmacro = \
	'puts "Starting macro..."\n\
	cpd null\n\n\
	data {0}\n\
	ignore **-3\n\
	ignore 7.-**\n'.format(specfile)
	
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
	set outfile [open {2}.dat w]\n\
	tclout param 8 \n\
	puts $outfile $xspec_tclout \n\
	tclout param 10 \n\
	puts $outfile $xspec_tclout \n\
	tclout param 14 \n\
	puts $outfile $xspec_tclout \n\
	tclout param 3 \n\
	puts $outfile $xspec_tclout \n\
	'.format(tmpfileenergy,tmpfilevalue,tmpparamval)

	if fitcheck == False:
		tclmacro = tclmacro + 'quit'


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


	# param values...

	tmppar = tmpparamval + ".dat"

	par = open(tmppar,'r')

	npar = 0

	for line in par:

			linedata = line.split()	
			paramlist[npar].append(float(linedata[0]))
			npar += 1




#--- Run macro on spectrum list ------------------------------------------------

for s in range(len(spectra)):

	macro(spectra[s],s)

print paramlist

#--- Create models with same paramaters as each spectrum, but no absorption

#------ Model command construction ---------------------------------------------

energiesp	= [[] for i in range(len(spectra))]
indicesp	= [[] for i in range(len(spectra))]
fluxp		= [[] for i in range(len(spectra))]

energiesa	= [[] for i in range(len(spectra))]
indicesa	= [[] for i in range(len(spectra))]
fluxa		= [[] for i in range(len(spectra))]

energiesu	= [[] for i in range(len(spectra))]
indicesu	= [[] for i in range(len(spectra))]
fluxu		= [[] for i in range(len(spectra))]

def macro2(nspec,energiesm,indicesm,fluxm,no):

	norm2		= str(paramlist[no][nspec])
	nH			= str(paramlist[0][nspec])
	xi			= str(paramlist[1][nspec])

	model = "mo "
	params = ""

	if pow2:

		if absori:
			model = model + "absori*"
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

	# set up macro

	tclmacro = \
	'puts "Starting macro..."\n\
	cpd null\n\n\
	data {0}\n'.format(spectra[0])
	
	tclmacro = tclmacro + comm # insert model command

	# fit model, extract data to tmp files
	tclmacro = tclmacro + \
	'\nset outfile [open {0}.dat w]\n\
	tclout energies 1\n\
	puts $outfile $xspec_tclout\n\
	set outfile [open {1}.dat w]\n\
	tclout modval 1\n\
	puts $outfile $xspec_tclout \n\
	quit'.format(tmpfileenergy,tmpfilevalue,tmpparamval)

	#print tclmacro

	# create temporary macro file
	macrofile= open(macrolocation, 'w')
	macrofile.write(str(tclmacro))
	macrofile.close()

	# run tcl script in xspec

	os.system("xspec - tmpmacro.tcl")

	# delete temporary macro
	os.remove(macrolocation)

	tmplocation = tmplocationenergy + ".dat"

	energyf = open(tmplocation, 'r')

	for line in energyf:
		linedata = line.split()
	
		for index in range(len(linedata)):
		
			if float(linedata[index]) >= esoft \
					and float(linedata[index]) <= ehard:	

				energiesm[nspec].append(float(linedata[index]))
				indicesm[nspec].append(index)

	energyf.close()

	# delete temporary data file
	os.remove(tmplocation)

	tmplocation = tmplocationvalue + ".dat"

	fluxf = open(tmplocation, 'r')

	for line in fluxf:
		linedata = line.split()

		for index in indicesm[nspec]:
			fluxm[nspec].append(float(linedata[index])*200.0) # *200 converts  
													 # cnts cm^-2 s^-1 bin^-1 to 
													 # cnts cm^-2 s^-1 keV^-1

	fluxf.close()

	# delete temporary data file
	os.remove(tmplocation)

for v in range(len(spectra)):

	macro2(v,energiesa,indicesa,fluxa,2)

absori = False

for t in range(len(spectra)):

	macro2(t,energiesp,indicesp,fluxp,2)


for t in range(len(spectra)):

	macro2(t,energiesu,indicesu,fluxu,3)

################################################################################

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

################################################################################

# calculate Total fluxes

total		= []
totalp		= []
totala		= []
totalu		= []

for y in range(specnum):
	
	t  = sum(flux[y]) #np.trapz(flux[y])
	tp = sum(fluxp[y])
	ta = sum(fluxa[y])
	tu = sum(fluxu[y])

	total.append(t)
	totalp.append(tp)
	totala.append(ta)
	totalu.append(tu)

# calculate difference

absCoeff = np.array(fluxa)/np.array(fluxp)

diff = (1 - absCoeff)

absflux = diff*np.array(fluxp)
absflux2 = np.array(fluxp)-np.array(fluxa)

diffsum = []

for u in range(len(diff)):

	diffsum.append(sum(diff[u]))


# plot data (logplot)

colours = ['red','blue','green','yellow','orange','purple','darkblue',\
			 'darkgreen','pink','cyan'] 
			# to allow the spectra to be the same colour in each plot...

if graph:

	# model spectra
	fig = plt.figure()

	ax = fig.add_subplot(3,2,1)

	plt.title("fitted spectra")
	plt.xlabel("Energy (keV)")
	plt.ylabel("Flux")

	ax.set_yscale('log')
	ax.set_xscale('log')

	ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	for p in range(specnum):

		plt.plot(energy[p],flux[p], color = colours[p])

	plt.xlim([esoft,ehard])

	# absorption spectra

	ax2 = fig.add_subplot(3,2,2)

	plt.title("Absorbed Power law, with and without absorption")
	plt.xlabel("Energy (keV)")
	plt.ylabel("Flux")

	ax2.set_yscale('log')
	ax2.set_xscale('log')

	ax2.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	for p in range(specnum):

		plt.plot(energy[p],fluxa[p], color = colours[p])
		plt.plot(energy[p],fluxp[p], color = colours[p])

	plt.xlim([esoft,ehard])


	# absorption

	ax3 = fig.add_subplot(3,2,3)

	plt.title("relative fluxes, direct & absorbed, before absorption")
	plt.xlabel("Direct")
	plt.ylabel("Absorbed (pre-absorption)")

	plt.scatter(totalp, totalu, marker='.',color = 'red')

	plt.xlim([esoft,ehard])

	# total flux v absorption
	ax4 = fig.add_subplot(3,2,4)

	plt.title("Unabsorbed Flux v. Absorption")
	plt.xlabel("Unabsorbed Flux")
	plt.ylabel("Absorption")

	if logabs:

		ax4.set_yscale('log')
		ax4.set_xscale('log')

		ax4.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	plt.scatter( np.array(totalp) + np.array(totalu), diffsum, \
					marker='.', color = 'red')

	ax5 = fig.add_subplot(3,2,5)

	plt.title("Unabsorbed Flux v. nH")
	plt.xlabel("Unabsorbed Flux")
	plt.ylabel("nH")

	plt.scatter( np.array(totalp) + np.array(totalu), paramlist[0],\
					 marker='.', color = 'red')


	fig.add_subplot(3,2,6)

	#plt.title("Unabsorbed Flux v. Ionisation")
	#plt.xlabel("Unabsorbed Flux")
	#plt.ylabel("Ionisation")

	plt.title("Direct Flux v. Absorption")
	plt.xlabel("Direct Flux")
	plt.ylabel("Absorption")

	#plt.scatter( totalp, paramlist[1], marker='.', color = 'red')
	plt.scatter( totalu, diffsum, marker='.', color = 'red')

	plt.show()




