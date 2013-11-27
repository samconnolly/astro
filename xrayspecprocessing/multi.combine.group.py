# multi.combine.group.py

# Uses the HEADAS tool addspec and grppha to sum sets of spectra, assign their
# summed background and response files and produce a grouped spectrum
# Uses a text file of input spectra. Does so from output file from listbinmin.py
# Sam Connolly 4/3/13

import os

# ====================== PARAMATERS ============================================

# file route - directory containing spectra and spectrum list
inroute    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"\
					+"/ngc1365/spectra/all/"

outroute   = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"\
					+"/ngc1365/spectra/summed/"

# file names
fname 	= "speclist.txt"
outname = "13.14.25.summed"

# Grouping command (e.g. "group min 15" for min of 15 counts per bin,
#						 "group 25 150 4" to group channels 25-150 into groups of 4
#						 [Swift XRT has 1024 channels] )

groupcommand = 'group min 15'
# overwrite existing files?

overwrite = False

# ==============================================================================

# get current directory, to return to

originaldir = os.getcwd()

# change to directory of spectra

os.chdir(inroute)

#===============================================================================
#  sum spectra
#===============================================================================

# creat sum command

sumcommand = "addspec " + fname + " " + outname + " qaddrmf = yes"\
					+ " qsubback = yes" + " clobber = " + str(overwrite)

# add spectra

os.system(sumcommand) 

#===============================================================================
#  group spectra
#===============================================================================

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

gcommand = 	'grppha ' + spectrum + ' ' + over + output + ' comm = "' + \
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

#-------------------------------------------------------------------------------

# switch back to original directory

os.chdir(originaldir)
