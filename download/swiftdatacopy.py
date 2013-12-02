# swiftdatacopy.py
# Sam Connolly 26/06/13

#===============================================================================
# Programme to automatically copy data from the swift data folders,
# rename appropriately and assign background and response files
#===============================================================================

import os
from callgroupxspec import *

# -------- PARAMATERS ----------------------------------------------------------
obj = "NGC4395" # object

copyfolder = "/disks/raid/raid1/xray/raid/sdc1g08/NetData" \
					+ "/Ngc4395/spectra/copy/"

obsidfile = "obsid.txt"

# files to copy

spec = True 	# Spectrum
back = True		# Background
resp = True		# response
arf  = True		# auxiliary response

# Grouping

grouping = True					# produce group spectrum?
groupcommand = "group min 15"	# group command to use (grppha)

#-------------------------------------------------------------------------------

location = copyfolder + obsidfile

command    = "cp "
commandend = " " + copyfolder

originaldir = os.getcwd()

os.chdir(copyfolder)

infile= open(location, 'r')

numbers = []
obsids  = []

for line in infile:
	
	#print line
	numbers.append(str(line.split()[0]))
	obsids.append(str(line.split()[1]))

infile.close()

n = 0

for obsid in obsids:

	num = numbers[n]

	fileroute = "/net/raid/raid1/xray/raid/swiftly/deep/"\
				+ "{0}/swift/000{1}/products_{0}/".format(obj,obsid)

	print "\n\n" + fileroute + "\n\n"

	if spec:

		filename = fileroute + "src_spec.pha.gz"

		copycommand = command + filename + commandend

		print copycommand

		os.system(copycommand)
		os.system("gunzip src_spec.pha.gz")
		os.system("mv src_spec.pha " + num + "_src_spec.pha")
		
	if back:

		filename = fileroute + "back_spec.pha.gz"

		copycommand = command + filename + commandend

		os.system(copycommand)
		os.system("gunzip back_spec.pha.gz")
		os.system("mv back_spec.pha " + num + "_back_spec.pha")


	if resp:

		filename = fileroute + "src_spec.rmf"

		copycommand = command + filename + commandend

		os.system(copycommand)
		os.system("mv src_spec.rmf " + num + "_src_spec.rmf")

	if arf:

		filename = fileroute + "src_spec.arf"

		copycommand = command + filename + commandend

		os.system(copycommand)
		os.system("mv src_spec.arf " + num + "_src_spec.arf")


	n += 1

	# assign background and response files

	group(num + "_src_spec.pha",num + "_src_spec.pha",copyfolder,"")

	# group spectra

	group(num + "_src_spec.pha",num + "_src_spec_grp.pha",\
					copyfolder,groupcommand)

# switch back to original directory

os.chdir(originaldir)
