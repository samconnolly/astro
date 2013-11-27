# xspecmultimodeldataout.hardness.data+pivotcomp.py
# Sam Connolly 28/03/13

# Programme to extract xspec model fluxes and the corresponding energies of 
# multiple models created automatically within xspec, with one varying parameter 
# then calculate, save and plot hardness V count rate and hard, soft counts
# AND compare to REAL DATA and a PIVOT model
# (so far allows 2 power laws, one with neutral or ionised absorption, galactic
# absorption, and a gaussian) 
# (requires an arbitrary spectrum file)
# USES NORM VALUES PROPORTIONAL TO nH - PLOTS TOTAL FLUX V nH, with fit (option)

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
specnum = 20 # spectrum number of model to extract

# energy range 

emin 			= 0.5 
emax 			= 10.0 
hardnesssplit 	= 2.0

# graph the data?
graph = True

# fit total flux with straight line?
fit = True

fstart = 1 # distance from start of data to fit (1 = first value)
fend   = 1 # distance from end of data to fit	(1 = last value)

resolution = 5.0 # fitting resolution (low = better, usually...)

# paramater relation? -  relation between the investigated paramater and another

relation = True

#	y = a*( x**(b))  relation to use:

factor  = 0.00057
index   = -0.287
factor2 = 0.0153
index2  = index

#--- Model parameters (STRING) -------------------------------------------------

# SET VARIABLE PARAMETER TO '[expr exp($var)]'

varstart  = 1.01 # lower value in range for variable parameter
varend    = 99.0 # upper value in range for variable parameter

# galactic absorption
gwabs 		= True
galnH 		= "1.39E-2"

# power laws (2nd optional)
phindex		= "1.45"
norm1		= '[expr pow($var,'+str(index)+')*'+str(factor)+']'
pow2		= True
norm2		= '[expr pow($var,'+str(index2)+')*'+str(factor2)+']'

# gaussian
gauss		= True
gaussE		= "0.8"
gaussS		= "0.1"
gaussnorm	= "1.21E-04"

# cold absorption
wabs 		= False
nH 			= '[expr exp($var)]' # 10^22

#absori
absori		= True
nH			= '[expr exp($var)]'
Tabs		= "3E+4"
ion			= "100.0"
z			= "0.005569"
Fe			= "3.5"
#-- Pivot model - Fh = k*(Fs -Cs)^a + Ch ---------------------------------------------

model 	= False 	# plot model?
k 		= 1.9
a		= 0.3
Cs		= 0.13
Ch		= 0.0

#--- Real Data -----------------------------------------------------------------

# Object name

objectname = "NGC1365" 

#   File routes
route           	= \
"/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/lightcurve"

times = [0,7000]

softdatanorm = 40.	# normalisations to data count rate..
harddatanorm = 20.
#softdatanorm = 0.48		# normalisations to data count rate..
#harddatanorm = 0.125
#===============================================================================

# use logarithmic range for nH to ensure even spacing of spectra in log space

increment = str((np.log(varend) - np.log(varstart))/float(specnum))
varstart  = str(np.log(varstart))

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
quit;'

#print tclmacro

# create temporary macro file
macrofile= open(macrolocation, 'w')
macrofile.write(str(tclmacro))
macrofile.close()

# run tcl script in xspec
os.chdir(outroute)
#os.system("headasinit") # initialise headas software, for xspec (personal alias)
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
	#os.remove(tmplocation)

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
	#os.remove(tmplocation)


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
total		= []
hardness 	= []

for y in range(specnum):
	s = np.trapz(flux[y][:splitindex])
	h = np.trapz(flux[y][splitindex:])
	t = np.trapz(flux[y])

	soft.append(s)
	hard.append(h)
	total.append(t)
	hardness.append((h - s) / (h + s))

#print comm

# create nH variation array

tnH = []

for sp in range(specnum):

	tnH.append(np.exp(float(varstart) + sp*float(increment))) 

#=========== line fit ==========================================================
if fit:

	fstart -= 1

	fend -=1
	fend = -1 - fend

	grad = (np.log(tnH[fend]) - np.log(tnH[fstart]))/ \
			(np.log(total[fend]) - np.log(total[fstart]))# initial grad

	const = np.log(tnH[fstart]) - \
				grad*np.log(total[fstart])# initial cnst


	igrad = grad
	iconst = const
	ires = 0 # initial residuals

	for  q in range(len(total)):	

		ires += (grad*np.log(total[q]) + const\
					 - np.log(tnH[q]))**2

	# fit grad

	factor = 1.0

	while factor > 0.00000000001:

		res  = 0
		resp = 0
		resm = 0

		for  q in range(len(total)):

			res += (grad*np.log(total[q]) + const\
						 - np.log(tnH[q]))**2

			pgrad = grad+ 1.0*factor

			resp += (pgrad*np.log(total[q]) + const\
						 - np.log(tnH[q]))**2

			mgrad = grad - 1.0*factor

			resm += (mgrad*np.log(total[q]) + const\
						 - np.log(tnH[q]))**2

		if resp < res:

			grad = pgrad

		if resm < res:

			grad = mgrad 

		else:

			factor *= (1.0/resolution)

		#print res,resp,resm

	# fit const

	factor = 1.0

	while factor > 0.00000000001:

		res  = 0
		resp = 0
		resm = 0

		for  q in range(len(total)):

			res += (grad*np.log(total[q]) + const\
						 - np.log(tnH[q]))**2

			pconst = const+ 1.0*factor

			resp += (grad*np.log(total[q]) + pconst\
						 - np.log(tnH[q]))**2

			mconst = const - 1.0*factor

			resm += (grad*np.log(total[q]) + mconst\
						 - np.log(tnH[q]))**2

		if resp < res:

			const = pconst

		if resm < res:

			const = mconst 

		else:

			factor *= (1.0/resolution)

		#print res,resp,resm

# ==============================================================================

#				Real Data

# ==============================================================================

energysoftroute  	= "/refinedCounts/"
energyhardroute  	= "/refinedCounts/"

# file names
energysoftfname 	= objectname+"_lcurve_3_gti_0.5-2keV.qdp"
energyhardfname		= objectname+"_lcurve_3_gti_2-10keV.qdp"


# create file routes
energysoftlocation 		= route+energysoftroute+energysoftfname
energyhardlocation 		= route+energyhardroute+energyhardfname


# Function to calculate hardness and error

def hardnessflux(tmin,tmax):

	# read data into 2-D arrays
	start = 0

	softtime    = np.array([])
	softflux    = np.array([])
	softfluxerr = np.array([])
	# soft
	energysoftin= open(energysoftlocation, 'r')

	for x in energysoftin:
	
		currtime, currflux, currfluxerr = x.split()
		if start == 1:
			if float(currtime) >= tmin and float(currtime) <= tmax:
				softtime    = np.append(softtime, float(currtime))
				softflux    = np.append(softflux, float(currflux)*softdatanorm)
				softfluxerr = np.append(softfluxerr, \
												float(currfluxerr)*softdatanorm)	
		start = 1

	energysoftin.close()
	# hard
	start = 0

	hardtime    = np.array([])
	hardflux    = np.array([])
	hardfluxerr = np.array([])

	energyhardin= open(energyhardlocation, 'r')

	for x in energyhardin:
	
		currtime, currflux, currfluxerr = x.split()
		if start == 1:
			if float(currtime) >= tmin and float(currtime) <= tmax:
				hardtime    = np.append(hardtime, float(currtime))
				hardflux    = np.append(hardflux, float(currflux)*harddatanorm)
				hardfluxerr = np.append(hardfluxerr, \
											float(currfluxerr)*harddatanorm)		
		start = 1

	energyhardin.close()



	hardness    = hardflux/softflux
	hardnesserr = hardness*(np.sqrt((hardfluxerr/hardflux)**2 + \
			(softfluxerr/softflux)**2))

	# Calculate modified hardness and error (H - S / H + S)

	modhardness = (hardflux-softflux)/(hardflux+softflux)
	sumerr = np.sqrt(hardfluxerr**2 + softfluxerr**2)
	modhardnesserr = modhardness*(np.sqrt(\
	(sumerr/(hardflux-softflux))**2 + (sumerr/(hardflux+softflux))**2 ) )

	# sort modified hardnesses and soft flux according to hard flux

	modfluxhard = [[],[],[],[],[],[]]
	start = 0

	for value in range(len(modhardness)):
		# if it isn't the first value...
		if start !=0:
			for comp in range(len(modfluxhard[0])): # for each value 
							# from the bottom up...
				if hardflux[value] <= modfluxhard[0][comp]:# add 
						     						 # below value if less/equal
					modfluxhard[0].insert(comp,hardflux[value])
					modfluxhard[1].insert(comp,hardfluxerr[value])
					modfluxhard[2].insert(comp,softflux[value])
					modfluxhard[3].insert(comp,softfluxerr[value])
					modfluxhard[4].insert(comp,modhardness[value])
					modfluxhard[5].insert(comp,modhardnesserr[value])
					break
				if comp == len(modfluxhard[0]) -1:  # add after last 
								 					# element if > than all
					modfluxhard[0].append(hardflux[value])
					modfluxhard[1].append(hardfluxerr[value])
					modfluxhard[2].append(softflux[value])
					modfluxhard[3].append(softfluxerr[value])
					modfluxhard[4].append(modhardness[value])
					modfluxhard[5].append(modhardnesserr[value])

		# if it is the first value, just fill that stuff in
		if start == 0:
			modfluxhard[0].append(hardflux[value])
			modfluxhard[1].append(hardfluxerr[value])
			modfluxhard[2].append(softflux[value])
			modfluxhard[3].append(softfluxerr[value])
			modfluxhard[4].append(modhardness[value])
			modfluxhard[5].append(modhardnesserr[value])
			start = 1
		
	totalflux = hardflux + softflux

	return modfluxhard, totalflux, hardtime

# run!

modfluxhard, totalflux, time = hardnessflux(times[0],times[1])

#============= Model ===========================================================
ahard = np.array(modfluxhard[0])

if model:
	mosoft = ((ahard - Ch) / k)**(1.0/a) + Cs
	mohardness = (ahard - mosoft)/(ahard + mosoft)
	
#============= Plotting ========================================================

if graph:

	# model spectra
	fig = plt.figure()

	ax = fig.add_subplot(2,2,1)

	ax.set_yscale('log')
	ax.set_xscale('log')

	ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
	plt.title("modelled spectra")
	plt.ylabel("photons cm^-2 s^-1 keV^-1")
	plt.xlabel("Energy (keV)")

	for p in range(specnum):

		plt.plot(energy[p],flux[p])

	plt.xlim([emin,8.0])

	# hardness v hard counts
	fig.add_subplot(2,2,2)
	plt.title("hard flux v hardness")
	plt.ylabel("Hardness")
	plt.xlabel("Hard photons cm^-2 s^-1")
	plt.errorbar(modfluxhard[0],modfluxhard[4],	xerr = modfluxhard[1],  \
			yerr = modfluxhard[5], marker='.', color = 'red', \
				ecolor = 'grey', linestyle = 'none',capsize = 0)
	plt.plot(hard, hardness, marker='.', color = 'blue')
	if model:
		plt.plot(ahard,mohardness,color ="green")

	# hardness v hard counts
	fig.add_subplot(2,2,4)
	plt.title("hard flux v soft flux")
	plt.ylabel("Soft photons cm^-2 s^-1")
	plt.xlabel("Hard photons cm^-2 s^-1")
	plt.errorbar(modfluxhard[0],modfluxhard[2],	xerr = modfluxhard[1],  \
			yerr = modfluxhard[3], marker='.', color = 'red', \
				ecolor = 'grey', linestyle = 'none',capsize = 0)
	plt.plot(hard, soft, marker='.', color = 'blue')
	if model:
		plt.plot(ahard,mosoft,color ="green")
	
	# nH v total flux
	ax2 = fig.add_subplot(2,2,3)


	ax2.set_yscale('log')
	ax2.set_xscale('log')

	ax2.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	plt.title("total flux v nH")
	plt.ylabel("nH 10^22 cm^-2")
	plt.xlabel("photons cm^-2 s^-1")
	plt.plot(total, tnH, marker='.', color = 'green')

if fit:

	fitx = [total[fstart],total[fend]]
	fity = [np.exp(np.log(total[fstart])*grad+const),\
			np.exp(np.log(total[fend])*grad+const)]

	plt.plot(fitx,fity)


	print "initial square residual total: ", ires
	#print "initial gradient: ",igrad,"initial intercept: ", iconst

	print "final square residual total: ", res
	print "gradient: ",grad,"intercept: ", const


	model = 'y = ' + str(np.exp(const)) + ' * x^(' + str(grad) + ')'

	print model


	print pparams

	plt.show()

