# download.py
# Sam Connolly 13/02/13

#===============================================================================
# Programme to automatically download data from the swift data website,
# rename appropriately and assign background and response files
#===============================================================================

import os
from callgroupxspec import *

# -------- PARAMATERS ----------------------------------------------------------
obj = "NGC4395" # object


downloadfolder = "/disks/raid/raid1/xray/raid/sdc1g08/NetData" \
					+ "/Ngc4395/spectra/download/"
obsidfile = "obsid.txt"

# Authorisation

username = "sconnolly"
password = "M81wibble00"

# files to download

spec = False 	# Spectrum
back = False		# Background
resp = True		# response
arf  = False		# auxiliary response

# Grouping

grouping = True					# produce group spectrum?
groupcommand = "group min 15"	# group command to use (grppha)

#-------------------------------------------------------------------------------

location = downloadfolder + obsidfile



command = "wget --user=" + username + " --password=" + password + " -nv "

originaldir = os.getcwd()

os.chdir(downloadfolder)

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

	urlroute = "http://www.astro.soton.ac.uk/~swiftly/swift/"\
				+ "{0}/data_{0}/000{1}/products_{0}/".format(obj,obsid)

	print "\n\n" + urlroute + "\n\n"

	if spec:

		url = urlroute + "src_spec.pha.gz"

		downloadcommand = command + url

		os.system(downloadcommand)
		os.system("gunzip src_spec.pha.gz")
		os.system("mv src_spec.pha " + num + "_src_spec.pha")
		#os.system("rm src_spec.pha")

	if back:

		url = urlroute + "back_spec.pha.gz"

		downloadcommand = command + url

		os.system(downloadcommand)
		os.system("gunzip back_spec.pha.gz")
		os.system("mv back_spec.pha " + num + "_back_spec.pha")


	if resp:

		url = urlroute + "src_spec.rmf"

		downloadcommand = command + url

		os.system(downloadcommand)
		os.system("mv src_spec.rmf " + num + "_src_spec.rmf")
		print downloadcommand

	if arf:

		url = urlroute + "src_spec.arf"

		downloadcommand = command + url

		os.system(downloadcommand)
		os.system("mv src_spec.arf " + num + "_src_spec.arf")


	n += 1

	# assign background and response files

	group(num + "_src_spec.pha",num + "_src_spec.pha",downloadfolder,"")

	# group spectra

	group(num + "_src_spec.pha",num + "_src_spec_grp.pha",\
					downloadfolder,groupcommand)

# switch back to original directory

os.chdir(originaldir)
