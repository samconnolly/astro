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
outroute = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/countbin/"

# output data file name
outfile  = "multimodelhardness.dat"
specfile = "0.197-0.3331.summed.pha"

# number of model spectra to extract
specnum = 100 # spectrum number of model to extract

# energy range 

emin 			= 0.5 
emax 			= 10.0 
hardnesssplit 	= 2.0

# graph the data?
graph = True

# fit total flux with straight line?
fit = False

fstart = 1 # distance from start of data to fit (1 = first value)
fend   = 1 # distance from end of data to fit	(1 = last value)

resolution = 5.0 # fitting resolution (low = better, usually...)

# paramater relation? -  relation between the investigated paramater and another

relation = False

#	y = a*( x**(b))  relation to use:

factor  = 0.0006 # b for unabs PL
index   = -.245  # a
factor2 = 0.016 # b for abs PL
index2  = -.245  # a

#--- Model parameters (STRING) -------------------------------------------------

# SET VARIABLE PARAMETER TO '[expr exp($var)]' if logvar, else $var

varstart  = 1.001 # lower value in range for variable parameter
varend    = 99.999 # upper value in range for variable parameter

logvar =  True # spread the varying paramter's values logorithmically?

# galactic absorption
gwabs 		= True
galnH 		= "1.39E-2"

# power laws (2nd optional)
phindex		= "1.95"		# unabsorbed
norm1		= '[expr pow([expr exp($var)],'+str(index)+')*'+str(factor)+']' #'3.81803E-04'#'[expr pow([expr exp($var)],'+str(index)+')*'+str(factor)+']'
pow2		= True			# absorbed
norm2		= '[expr pow([expr exp($var)],'+str(index2)+')*'+str(factor2)+']' #'1.45856E-02'#'[expr pow([expr exp($var)],'+str(index2)+')*'+str(factor2)+']'

# gaussian
gauss		= True
gaussE		= "0.8"
gaussS		= "0.1"
gaussnorm	= "7.76605E-05"

#ini
# cold absorption
wabs 		= False
nH 			= '[expr exp($var)]' # 10^22

#absori
absori		= True
nH			= '[expr exp($var)]'#'$var' # 
Tabs		= "3E+4"
ion			= "0.245696"
z			= "0.005569"
Fe			= "2.8"
#-- Pivot model - Fh = k*(Fs -Cs)^a + Ch ---------------------------------------------

domodel = False 	# plot model?
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

softdatanorm = 1. 	# normalisations to data count rate..
harddatanorm = 1.
#softdatanorm = 0.48		# normalisations to data count rate..
#harddatanorm = 0.125

#===============================================================================
#								MAIN PROGRAMME
#===============================================================================

# use logarithmic range for nH to ensure even spacing of spectra in log space

if logvar == True:
	increment = str((np.log(varend) - np.log(varstart))/float(specnum))
	varstart  = str(np.log(varstart))

else:
	increment = str((varend - varstart)/float(specnum))
	varstart  = str(varstart)

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
pparams = pparams + " Unabsorbed normalisation: " + norm1 + '\n'

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
tmpfilecounts   = "tmpcounts"

# set file locations
macrolocation 		= outroute + macrofile
outlocation   		= outroute + outfile
tmplocationcounts  	= outroute + tmpfilecounts

here = os.getcwd() # get current working directory to return to

# set up loop values
tclmacro = \
'puts "Starting macro..."\n\
cpd null\n\
data {0}\n\
set i 1\n\
set var {1}\n\
set increment {2}\n\
set outfile [open {3}.dat w]\n'.format(specfile, varstart,increment,tmpfilecounts)

tclmacro = tclmacro + \
'while {$i <= ' # loop start

tclmacro = tclmacro + str(specnum +1) # insert no. model spectra to create

tclmacro = tclmacro + \
'} {;\n'

tclmacro = tclmacro + comm # insert model command

# extract data to tmp files
tclmacro = tclmacro + \
'\nignore 0.-0.5\n\
ignore 10.-**\n\
notice 0.5-10.0\n\
tclout rate 1\n\
puts $outfile $xspec_tclout \n\
puts $xspec_tclout \n\
ignore 0.5-2.0\n\
tclout rate 1\n\
puts $outfile $xspec_tclout \n\
puts $xspec_tclout \n\
ignore 2.0-10.0\n\
notice 0.5-2.0\n\
tclout rate 1\n\
puts $outfile $xspec_tclout \n\
puts $xspec_tclout \n\
set var [expr $var + $increment]'

# loop end
tclmacro = tclmacro + \
'; incr i;}\n\
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

soft  = []
hard  = []
total = []

tmplocation = tmplocationcounts + ".dat"

counts = open(tmplocation, 'r')

l = 0
m = 0

for line in counts:

	linedata = line.split()

	if m > 2:
		if l==0:	
			total.append(float(linedata[2]))
			
		if l==1:
			hard.append(float(linedata[2]))

		if l==2:
			soft.append(float(linedata[2]))

		l+=1

		if l==3:
			l=0

	m += 1

counts.close()

# delete temporary data file
#os.remove(tmplocation)


# create new, combined data file

output = open(outlocation, 'w')

output.write("Total counts \t Soft Counts \t Hard Counts")	
output.write("\n")

for j in range(len(total)):

	output.write(str(total[j]))
	output.write("\t")

	output.write("\n")

output.close()



#return to original directory
os.chdir(here)

# calculate hardness

hardness = []

for h in range(len(hard)):

	hardness.append((hard[h]-soft[h])/(hard[h]+soft[h]))


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

if domodel:
	mosoft = ((ahard - Ch) / k)**(1.0/a) + Cs
	mohardness = (ahard - mosoft)/(ahard + mosoft)
	
#============= Plotting ========================================================

if graph:

	font = {'family' : 'normal',
		    'weight' : 'bold',
		    'size'   : 22}
	matplotlib.rcParams.update({'font.size': 22})
	matplotlib.rc('xtick', labelsize=20) 
	matplotlib.rc('ytick', labelsize=20)



	fig = plt.figure()

	# hardness v hard counts
	fig.add_subplot(2,1,1)
	plt.title("hard flux v hardness")
	plt.ylabel("Hardness Ratio")
	plt.xlabel("Hard Flux ($cm^{-2} s^{-1}$)")
	plt.errorbar(modfluxhard[0],modfluxhard[4],	xerr = modfluxhard[1],  \
			yerr = modfluxhard[5], marker='.', color = 'black', \
			ecolor = 'grey', linestyle = 'none',capsize = 0)
	plt.plot(hard, hardness, marker='.',linewidth = 2, color = 'blue')
	if domodel:
		plt.plot(ahard,mohardness,color ="green")

	# hardness v hard counts
	fig.add_subplot(2,1,2)
	plt.title("hard flux v soft flux")
	plt.ylabel("Soft Flux ($cm^{-2} s^{-1}$)")
	plt.xlabel("Hard Flux ($cm^{-2} s^{-1}$)")
	plt.errorbar(modfluxhard[0],modfluxhard[2],	xerr = modfluxhard[1],  \
			yerr = modfluxhard[3], marker='.', color = 'black', \
				ecolor = 'grey', linestyle = 'none',capsize = 0)
	plt.plot(hard, soft, marker='.',linewidth = 2, color = 'blue')
	if domodel:
		plt.plot(ahard,mosoft,color ="green")
	
	# nH v total flux
	#ax2 = fig.add_subplot(2,2,3)


	#ax2.set_yscale('log')
	#ax2.set_xscale('log')

	#ax2.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	#plt.title("total flux v nH")
	#plt.ylabel("nH 10^22 cm^-2")
	#plt.xlabel("photons cm^-2 s^-1")
	#plt.plot(total, tnH, marker='.', color = 'green')

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

