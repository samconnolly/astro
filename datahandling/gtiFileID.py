"""

 gtiFileID.py

 Sam Connolly 30/08/13

 Programme to add the woefully missing file name to the swift data tables
 by associating the obsID of files in the same directory with an obs name,
 then adding GTI numbers.

"""

import os
import pyfits

# ============= INPUT PARAMETERS ===============================================

route  = "/net/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/gti/"
infile = "NGC1365_lcurve_gti_0.5-10keV.txt"
outfile = "spectra.txt"

# ==============================================================================

here = os.getcwd()

os.chdir(route)

spectra = [[],[],[]]

for sfile in os.listdir("."):
    if "src_spec_gti01.pha" in sfile:
        spectra[0].append(sfile)


for spectrum in spectra[0]:

	header = pyfits.open(spectrum)

	obsid  = header[0].header["OBS_ID"]

	spectra[1].append(obsid)

for name in spectra[0]:

	if name[1] == "_":
		num = name[0]

	else:
		num = name[0] + name[1]

	spectra[2].append(num)

#for t in range(len(spectra[0])):

#	print spectra[0][t],spectra[1][t],spectra[2][t]

this = open(route+infile,'r')
that = open(route+outfile,'w')

start = 0

for line in this:

	if start == 1:
		obs = line.split()[0]
		
		for o in range(len(spectra[0])):

			print obs, spectra[1][o]
			if obs is spectra[1][o]:
	
				data = line + spectra[2]
				print data
				that.write(data)
	start = 1

this.close()
that.close()


os.chdir(here)






