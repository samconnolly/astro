# groupxspec.py

# Uses the HEADAS tool grppha to group a list of x-ray spectra uninteractively
# Uses a text file of input spectra to create output filenames and assign
# background and response files, using commands of the format:
# 'grppha spec.pha !out.pha comm = "chkey BACKFILE back.pha & chkey RESPFILE 
# file.rmf & chkey ANCRFILE file.arf & group min 15 & exit" '
 
# Sam Connolly 28/01/13

import os

# ====================== PARAMATERS ============================================

# file route - directory containing spectra and spectrum list
route    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/all/"

# file name
fname 	= "spec.txt"

# Grouping command (e.g. "group min 15" for min of 15 counts per bin,
#						 "group 25 150 4" to group channels 25-150 into groups of 4
#						 [Swift XRT has 1024 channels] )

groupcommand = 'group min 15'
# overwrite existing files?

overwrite = True

# ==============================================================================

# get current directory, to return to

originaldir = os.getcwd()

# create file route
location  = route+fname

# read data into an array

speclist  = [] # list of spectra to populate

infile= open(location, 'r')

for line in infile:

	linedata = line.split()		# split line into columns

	if linedata:
		speclist.append(linedata[0])	# append filename to array

infile.close()

# change to directory of spectra

os.chdir(route)
print os.getcwd()
# generate file names, group spectra

for spectrum in speclist:

	# determine spectrum prefix

	prefix = ""
	for character in spectrum:
		if character == "_":
			break
		prefix = prefix + character

	# generate filenames

	back   = prefix + "_back_spec.pha"
	rmf    = prefix + "_src_spec.rmf"
	arf    = prefix + "_src_spec.arf"
	output = prefix + "_src_spec_grp.pha"

	# overwriting or not

	if overwrite == True:
		over = '!'
	else:
		over = ''

	# generate grppha command

	command = 	'grppha ' + spectrum + ' ' + over + output + ' comm = "' + \
				'chkey BACKFILE ' + back + \
				' & chkey RESPFILE ' + rmf + \
				' & chkey ANCRFILE ' + arf + \
				' & ' + groupcommand + ' & exit"'

	# execute command

	os.system(command)


# switch back to original directory

os.chdir(originaldir)
