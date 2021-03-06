import pyfits
import os

dataroute = "/net/aips/aips1/swiftly/dangerous_deep/NGC1365/swift/"
outroute  = "/net/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/gti/"

# Authorisation

username = "sconnolly"
password = "M81wibble00"

# files
obsidfilename = "obsids.txt"
infofilename  = "info.txt"

#------------------ MAIN PROG --------------------------------------------------

obsidfile = open(outroute+obsidfilename,'r')

obsids = []

for line in obsidfile:

	obsids.append(line.split()[0])

obsnum = 1


originaldir = os.getcwd()
command = "wget --user=" + username + " --password=" + password + " -nv "

for obsid in obsids:

	route = dataroute + obsid + "/products_NGC1365/"
	os.chdir(route)
	os.system("cp src_spec_gti*.pha.gz " + outroute )
	os.system("cp src_spec_gti*.arf " + outroute )
	os.system("cp back_spec_gti*.pha.gz " + outroute)
	#os.system("cp src_spec.rmf " + outroute) # links broken... so download instead
	os.chdir(outroute)

	url = "http://www.astro.soton.ac.uk/~swiftly/swift/"\
		+ "NGC1365/data_NGC1365/{0}/products_NGC1365/src_spec.rmf".format(obsid)

	os.system(command + url)

	os.system("rm *grp*")
	os.system("gunzip *.pha.gz")

	findcommand = "find . -name 'src*' -printf " + '"' + "'%p' '%h/" +\
					 str(obsnum) + "_%f'\\n" + '"' + " | xargs -n2  mv"
	findcommand2 = "find . -name 'back*' -printf " + '"' + "'%p' '%h/" +\
					 str(obsnum) + "_%f'\\n" + '"' + " | xargs -n2  mv"

	os.system(findcommand)
	os.system(findcommand2)

	obsnum += 1

spectra = []

for files in os.listdir("."):
    if "src" in files and "pha" in files:
        spectra.append(files)

counts    = []
exposure  = []
countrate = []

for spectrum in spectra:

	header = pyfits.open(spectrum)

	cnts  = header[0].header["TOTCTS"]
	exp   = header[0].header["EXPOSURE"]
	cntrt = float(cnts)/float(exp)

	counts.append(cnts)
	exposure.append(exp)
	countrate.append(cntrt)

print spectra, counts, exposure, countrate

outfile  = open(outroute+infofilename,'w')

for n in range(len(spectra)):

	outfile.write(str(spectra[n]))
	outfile.write("\t")
	outfile.write(str(counts[n]))
	outfile.write("\t")
	outfile.write(str(exposure[n]))
	outfile.write("\t")
	outfile.write(str(countrate[n]))
	outfile.write("\n")


os.chdir(originaldir)




