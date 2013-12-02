# xspecfitting.py
# Sam Connolly 28/01/13

# Programme to generate an xspec macro to fit a power law with absorption to 
# a set a spectra, create and sort an output file

import os

# ============== PARAMATERS ====================================================

# file route - directory containing spectra and to contain output
route    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/longexposure/"

# output file name
outfile 	= "modelparameters.dat"

# input spectra
filepre = "11 9 15 10 25 14 36 8 3 1 2" # number prefixes
fileend = "_src_spec_grp.pha"	# common suffix

# MODEL STARTING PARAMATERS (,-1 to freeze)

absorption = "1.39E-2,-1"
phindex    = "2.0"
plnorm     = "1.0"

# ==============================================================================

# --- Run Xspec modelling macro and save results ---

# temporary macro name
macrofile  = "tmpmacro.tcl"

# set file locations
macrolocation = route + macrofile
outlocation = route + outfile

here = os.getcwd()

# tcl macro to run on spectra
tclmacro = \
'puts "Starting macro..."\n\
set outfile [open {0} w]\n'.format(outfile) + \
'foreach i {' + filepre + \
'} {\n ' + \
'set filename "{0}"\n\
data $i$filename\n\
ignore **-25 9.-**\n\
query yes\n\
mo wa*pow & {1} & {2} & {3}\n\
fit \n\
puts $outfile $i$filename\n\
tclout param 1\n\
puts $outfile $xspec_tclout\n\
tclout param 2\n\
puts $outfile $xspec_tclout\n\
tclout param 3\n\
puts $outfile $xspec_tclout\n'.format(fileend,absorption,phindex,plnorm) \
+ '}\nquit'

# create temporary macro file
macrofile= open(macrolocation, 'w')
macrofile.write(str(tclmacro))
macrofile.close()

# run tcl script in xspec
os.chdir(route)
os.system("xspec - tmpmacro.tcl")

# ---- sort output file ----

# read in data
output = open(outlocation, 'r+')

data    = []

for line in output:
	linedata = line.split()
	data.append(linedata)

output.close()

# delete original data file
os.remove(outlocation)

# create new, sorted data file
output = open(outlocation, 'w')

output.write(\
"Spectrum\t\t\t\tnH (*10^20)\tPhoton Index\tPower Law Normalisation\n")	

for i in range(0,len(data),4):
	output.write(str(data[i ][0]))
	output.write("\t\t")
	output.write("%.4f"%(float(data[i + 1][0])))
	output.write("\t\t")
	output.write("%.6f"%(float(data[i + 2][0])))
	output.write("\t\t")
	output.write("%.10f"%(float(data[i + 3][0])))
	output.write("\n")

output.close()

# delete temporary macro
os.remove(macrolocation)

#return to original directory
os.chdir(here)


