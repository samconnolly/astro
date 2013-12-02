"""
gtiSpecListSort.py
 
Sam Connolly, Fri Oct  4 13:03:33 2013
 
Programme to sort a list of gti spectrum file names into their actual order,
instead of the stupid one the computer likes to put them in. And save the output.
It'll sort any other rows with the spec names too.

"""

# ============== PARAMATERS ====================================================

# file route - directory containing spectra and to contain output
route    = "/net/raid/raid1/xray/raid/sdc1g08/NetData/Ngc3516/spectra/gti/"

infilename  = "info.txt" 
outfilename = "sortInfo.txt"

# ==============================================================================

# import file list
fname = route + infilename
file1 = open(fname, 'r')

spectra = [[],[],[],[]]

for line in file1:
	linedata = line.split()
	spectra[0].append(linedata[0])
	spectra[3].append(linedata[1:])
	
file1.close()

# extract gti and spectrum numbers

for s in range(len(spectra[0])):
	specnum = ""
	gtinum  = ""
	
	n = 0	

	while spectra[0][s][n] != "_":
		
		specnum = specnum + spectra[0][s][n]
		n += 1
		
	while spectra[0][s][n] != "i":

		n += 1
		
	n += 1
		
	while spectra[0][s][n] != ".":
		
		gtinum = gtinum + spectra[0][s][n]
		n +=1
		
	#print int(specnum), int(gtinum)
	spectra[1].append(int(specnum))
	spectra[2].append(int(gtinum))
	#print int(specnum),int(gtinum)
	
	
# sort spec names and put in new array, along qith any other data in input

sortSpectra = [[],[],[],[]]

start = 0

for s in range(len(spectra[0])):
	
	if start > 0:
		
		for t in range(len(sortSpectra[0])):
			
			# add to end if largest 
			if t == len(sortSpectra[0]) - 1:
				
				sortSpectra[0].append(spectra[0][s])
				sortSpectra[1].append(spectra[1][s])
				sortSpectra[2].append(spectra[2][s])	
				sortSpectra[3].append(spectra[3][s])
								
				break
				
			# add before if equal and gti number is less
			if spectra[1][s] == sortSpectra[1][t]:
				
				if spectra[2][s] < sortSpectra[2][t]:
						
					sortSpectra[0].insert(t,spectra[0][s])
					sortSpectra[1].insert(t,spectra[1][s])
					sortSpectra[2].insert(t,spectra[2][s])
					sortSpectra[3].insert(t,spectra[3][s])
					
					break
								
			# add between if between two
			if spectra[1][s] >= sortSpectra[1][t] and \
				spectra[1][s] < sortSpectra[1][t+1]:
			
				sortSpectra[0].insert(t+1,spectra[0][s])
				sortSpectra[1].insert(t+1,spectra[1][s])
				sortSpectra[2].insert(t+1,spectra[2][s])
				sortSpectra[3].insert(t+1,spectra[3][s])
				
				break

			# add at start if smallest
			if t == 0 and spectra[1][s] < sortSpectra[1][t]:
				
				sortSpectra[0].insert(0,spectra[0][s])
				sortSpectra[1].insert(0,spectra[1][s])
				sortSpectra[2].insert(0,spectra[2][s])
				sortSpectra[3].insert(0,spectra[3][s])

	# add first element if list is empty				
	if start == 0:
		
		sortSpectra[0].append(spectra[0][s])
		sortSpectra[1].append(spectra[1][s])
		sortSpectra[2].append(spectra[2][s])
		sortSpectra[3].append(spectra[3][s])
		
	start += 1

# print list	
#for s in range(len(sortSpectra[0])):
	
#	print sortSpectra[0][s],sortSpectra[1][s],sortSpectra[2][s]

# save list as new file

fname2 = route + outfilename
file2 = open(fname2, 'w')

for s in range(len(sortSpectra[0])):

	file2.write(sortSpectra[0][s])
	
	for t in sortSpectra[3][s]:

		file2.write("\t")
		file2.write(str(t))
		
	file2.write("\n")
	
file2.close()





