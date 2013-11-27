"""
order.py

Sam Connolly 29/01/13


Programme sort a set of data according to one of the data columns,
creating an output file with a label of the original position as a column

"""

import numpy as np

# =========================== PARAMATERS =======================================

# file description/ reading preferences...

header  = 1 # number of header lines before data starts
columns = 14 # number of data columns
sortcol = 6 # column with which to sort data


# file route
route    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/mainlc/raw/"

# file names
fin 	= "NGC1365_lcurve_0.5-10keV.txt"
fout = "all.counts-sorted.data.0.5-10keV.dat"

# ==============================================================================

sortcol -= 1

# create file route
location     = route+fin
outlocation  = route+fout

# read data into 2-D arrays
start = 0

data  = [[] for i in range(columns)]

infile= open(location, 'r')

for line in infile:
	
	if start >= header:								# once past header
		linedata = line.split()						# split line into columns
		for col in range(columns):					# add data to array columns
			data[col].append(linedata[col])
	start += 1

infile.close()

# sort chosen column into decending order, recording the original index of each

sort = [[data[sortcol][0]],[0]]
done = 0

for n in range(1,len(data[sortcol])):
	for m in range(len(sort[0])):
		if data[sortcol][n] > sort[0][m]:
			sort[0].insert(m,data[sortcol][n])
			sort[1].insert(m,n)
			done = 1
			break
	if done == 0:
		sort[0].append(data[sortcol][n])
		sort[1].append(n)
	done = 0

# write all of the data out in the new order using the indexes, also printed

outfile = open(outlocation, 'w')

outfile.write("#OBSID\t\tMJD-OBS\tTEXP\tMET_START\tMET_STOP\tRATE\t\tRATE_ERR\t\
FLUX\tFLUX_ERR\tFLAG\tQUAL\tNCTS\tRATE_68LO\tRATE_68HI\n")

#outfile.write("MJD\t\t\tFLUX\t\tFLUX ERROR\tN (swift)\n")

for x in sort[1]:
	for y in range(columns):
		outfile.write(str(data[y][x]))
		outfile.write("\t")
	outfile.write(str(x + 1))
	outfile.write("\n")

outfile.close()








