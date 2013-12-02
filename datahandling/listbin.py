"""
# listbin.py
# Sam Connolly 04/03/2013

#===============================================================================
# bin data according a given column in an ascii file of column data, printing the
# bin of each data point as a LIST. Equal bin widths.
#===============================================================================
"""

# Import packages

import numpy as np

#================ PARAMETERS ===================================================

# read variables
header = 0 # number of header lines to ignore

outdata = [1, 2] # column numbers to output

bincolumn = 1 # column to bin along

nbins = 50 # number of bins

#   File route
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365/uvot/"
# file name
infilename 	= "U.dat"

#==================== Load data ================================================

# create file route
location  = route+infilename

# read data intoarray

start = 0

infile= open(location, 'r')

for line in infile:
	
	linedata = line.split()

	if start == header:
		columns = len(linedata)
		data = [[] for x in range(columns)]

	if start >= header:
		for column in range(columns):
			if len(linedata) == columns:
				data[column].append(float(linedata[column]))
		
	start += 1

infile.close()

outdata = np.array(outdata)	
outdata -= 1 
bincolumn -= 1


#========================= Bin =================================================

bmin = min(data[bincolumn])
bmax = max(data[bincolumn])
bwidth = (bmax - bmin)/ float(nbins)

bins =[[] for i in range(nbins)]

for index in range(len(data[0])):

	ibin = int(data[bincolumn][index] / bwidth)

	if data[bincolumn][index] == max(data[bincolumn]):

		ibin = nbins - 1
	
	bins[ibin].append(index)


#======================== print output =========================================


for b in range(len(bins)):

	low  = b*bwidth + bmin
	high = (b+1)*bwidth + bmin

	print low, " >= x > ", high, ":\n"

	output = ''

	for index in bins[b]:
		for dat in outdata:
			if dat != bincolumn:

				output = output + str(data[dat][index]) + '\t'

	print output, "\n"







