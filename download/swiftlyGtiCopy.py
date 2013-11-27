"""
 swiftlyGtiCopy.py

 Sam Connolly 22/08/13

 Programme to copy over all the GTI spectra and relevant rmf,arf,background for
 a given object, then extract count rates etc. from their headers. Or one of the
 two.
"""

import pyfits
import os

#=============== PARAMETERS ====================================================

copy = True
read = True

# in and out file routes
dataroute  = "/net/aips/aips1/swiftly/dangerous_deep/NGC3516/swift/"
outroute   = "/net/raid/raid1/xray/raid/sdc1g08/NetData/Ngc3516/spectra/gti/"
# most are in e.g. /net/aips/aips1/swiftly/dangerous_deep/NGC1365/swift/
# some are in e.g. /net/raid/raid1/xray/raid/swiftly/deep/NGC1365/swift/

objectName = "NGC3516"
# Authorisation for download from swiftly website

username = "sconnolly"
password = "M81wibble00"

# file names

obsidfilename = "obsids.txt"
infofilename  = "info.txt"

#------------------ MAIN PROG --------------------------------------------------

originaldir = os.getcwd() # save directory to return to

# --- copy files over ----

if copy:

	# --- read in obsids for file system ---

	obsidfile = open(outroute+obsidfilename,'r')

	obsids = []

	for line in obsidfile:

		obsids.append(line.split()[0])

	
	obsnum = 1

	

	# download command
	command = "wget --user=" + username + " --password=" + password + " -nv "

	
	for obsid in obsids:

		# go to this obsid's folder
		print obsnum,"/",len(obsids)
		route = dataroute + "000" + obsid + "/products_{0}/".format(objectName)
		os.chdir(route)

		filenames = os.listdir(os.curdir)
	
		# check if the pha files are zipped, which they sometimes are...
		pha = False
		
		for filename in filenames:

		   if filename.startswith('src_spec_gti') and filename.endswith('.pha'):
				pha = True
				break

		# copy files across
		if pha == True:
			os.system("cp src_spec_gti*.pha " + outroute ) # copy files across
			os.system("cp back_spec_gti*.pha " + outroute)

		else:
			os.system("cp src_spec_gti*.pha.gz " + outroute ) # copy files across
			os.system("cp back_spec_gti*.pha.gz " + outroute)
			os.system("gunzip *.pha.gz")	# unzip data
		

		os.system("cp src_spec_gti*.arf " + outroute )
		#os.system("cp src_spec.rmf " + outroute) 

		os.chdir(outroute) # change to output folder

		# This was written because the rmf links were broken, so I was going to
		# download instead, but actually if you just go to the location they're
		# in the links will work:
		# /home/td/software/CALDB/data/swift/xrt/cpf/rmf/

		# rmf location url
		url = "http://www.astro.soton.ac.uk/~swiftly/swift/"+\
		"{1}/data_{1}/000{0}/products_{1}/src_spec.rmf".format(obsid,objectName)
				
		os.system(command + url)
		
		os.system("rm *grp*")			# remove grouped files	
		#os.system("gunzip *.pha.gz")	# unzip data

		# rename data
		findcommand = "find . -name 'src*' -printf " + '"' + "'%p' '%h/" +\
						 str(obsnum) + "_%f'\\n" + '"' + " | xargs -n2  mv"
		findcommand2 = "find . -name 'back*' -printf " + '"' + "'%p' '%h/" +\
						 str(obsnum) + "_%f'\\n" + '"' + " | xargs -n2  mv"

		os.system(findcommand)
		os.system(findcommand2)
		
		obsnum += 1

# --- Extract count rates etc. ---

if read:

	if copy == False:

		os.chdir(outroute) # change to output folder

	spectra = []

	for files in os.listdir("."):				# identify spectrum files

		if "src" in files and "pha" in files:

			spectra.append(files)
		

	# fill data arrays

	obsids	  = []
	counts    = []
	exposure  = []
	countrate = []

	for spectrum in spectra:

		header = pyfits.open(spectrum)

		obs   = header[0].header["OBS_ID"]
		cnts  = header[0].header["TOTCTS"]
		exp   = header[0].header["EXPOSURE"]
		cntrt = float(cnts)/float(exp)

		obsids.append(obs)
		counts.append(cnts)
		exposure.append(exp)
		countrate.append(cntrt)

	# write data to output data file

	outfile  = open(outroute+infofilename,'w')

	for n in range(len(spectra)):

		outfile.write(str(spectra[n]))
		outfile.write("\t")
		outfile.write(str(obsids[n]))
		outfile.write("\t")
		outfile.write(str(counts[n]))
		outfile.write("\t")
		outfile.write(str(exposure[n]))
		outfile.write("\t")
		outfile.write(str(countrate[n]))
		outfile.write("\n")


os.chdir(originaldir) # return to starting directory




