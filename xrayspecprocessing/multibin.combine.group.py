# multibin.combine.group.py

# Uses the HEADAS tool addspec and grppha to sum sets of spectra, assign their
# summed background and response files and produce a grouped spectrum
# Uses a text file of input spectra. Does so from output file from listbinmin.py
# Sam Connolly 4/3/13

import os

# ====================== PARAMATERS ============================================

# file route - directory containing spectra and spectrum list
inroute    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"\
					+"/ngc1365/spectra/gti/"

outroute   = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"\
					+"/ngc1365/spectra/gtibin/"

# file names

binfile = 'binsout.dat'

# Grouping command (e.g. "group min 15" for min of 15 counts per bin,
#						 "group 25 150 4" to group channels 25-150 into groups of 4
#						 [Swift XRT has 1024 channels] )

groupcommand = 'group min 15'

# overwrite existing files?

overwrite = True

#================ Grouping Function ============================================

def combinegroup(outname):

	#===========================================================================
	#  sum spectra
	#===========================================================================

	# creat sum command

	sumcommand = "addspec " + fname + " " + outname + " qaddrmf = yes"\
						+ " qsubback = yes" + " clobber = " + str(overwrite)\
							+ ' chatter = 0'
	# add spectra

	os.system(sumcommand) 

	#===========================================================================
	#  group spectra
	#===========================================================================

	#  file names

	spectrum = outname + ".pha"
	back     = outname + ".bak"
	rmf      = outname + ".rsp"
	output   = outname + "_grp.pha"

	# overwriting or not

	if overwrite == True:
		over = '!'
	else:
		over = ''

	# generate grppha command

	gcommand = 	'grppha ' + spectrum + ' ' + over + output + ' chatter = 0' + \
				' comm = "' + \
				'chkey BACKFILE ' + back + \
				' & chkey RESPFILE ' + rmf + \
				' & ' + groupcommand + ' & exit"'

	# execute command

	os.system(gcommand)

	# move files to output folder

	movecommand = "mv " + spectrum + " " + outroute \
					+ " & mv " + back + " " + outroute \
						+ " & mv " + rmf + " " + outroute\
							+ " & mv " + output + " " + outroute 

	os.system(movecommand)

	#---------------------------------------------------------------------------

#============== Grouping Loop ==================================================


# tmp input file name/location
fname 	= "speclist.txt"
tmplocation = inroute + fname

# get current directory, to return to

originaldir = os.getcwd()

# change to directory of spectra

os.chdir(inroute)

# load list of grouping lists...

location  = outroute+binfile

# read data intoarray

start = 0

infile= open(location, 'r')

groups = []


for line in infile:
	
	linedata = line.split()

	if linedata[0] != 'number':

		if start == 0:
		
			groups.append([])
			groups[-1].append(linedata[0])
			groups[-1].append(linedata[2])
			groups[-1].append([])

		if start == 1:
		
			for n in linedata:

				groups[-1][2].append(str(int(float(n))))
		
			start = -1

		start += 1

infile.close()

for g in range(len(groups)):

	outname = str(groups[g][0])+'-'+str(groups[g][1])+".summed"
	
	tmp = open(tmplocation,'w')

	for spec in groups[g][2]:

		tmp.write(spec+'_src_spec.pha\n')

	tmp.close()

	combinegroup(outname)

	os.remove(tmplocation)

# switch back to original directory

os.chdir(originaldir)
