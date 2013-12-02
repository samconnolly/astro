"""
GTIfilenameAdd.py

Sam Connolly, sometime in late 2012...

Goes through each of the spectra in a folder and matches them to the obsids
in a data file. I'm not sure why this is useful anymore.

"""


import pyfits
import os

# ------------------- INPUT PARAMATERS -----------------------------------------

dataroute = "/net/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/gti/"

infofilename   = "NGC1365_lcurve_gti_0.5-10keV.txt"

outputfilename = "allinfo.txt"

save = False
 
#------------------ MAIN PROG --------------------------------------------------

here = os.getcwd()		# grab initial directory

os.chdir(dataroute)		# go to directory of spectra

# find all cource spectrum files in that folder and put them in a list
spectra = []

for files in os.listdir("."):
    if "src" in files and "pha" in files:
        spectra.append(files)

# open the data file and make a list of the OBSIDs, and put all data in a list
info = open(dataroute+infofilename)

obsids    = []
data	  = []

start = 0

for line in info:

	if start == 1:
		datum = line.split()

		data.append(datum)
		obsids.append(datum[0])

	start = 1

# open the headers of each spectrum file, match the OBSIDs, print them together
orderspectra = []

for spectrum in spectra:

	header = pyfits.open(spectrum)

	obsid  = header[0].header["OBS_ID"]

	for n in range(len(obsids)):

		if obsid == obsids[n]:

			print obsid, obsids[n]
			orderspectra.append(spectra[n])

# save the results if desired
if save:

	outfile  = open(dataroute+outputfilename,'w')

	for n in range(len(orderspectra)):

		outfile.write(data[n])
		outfile.write("\t")
		outfile.write(orderspectra[n])

		outfile.write("\n")


os.chdir(here)




