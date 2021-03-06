"""
# listbinmin.py
# Sam Connolly 04/03/2013

#===============================================================================
# bin data according a given column in an ascii file of column data, such that
# each bin has a minimum number of points, giving the bin of each data point as 
# a LIST. UNEVEN BINS.
#===============================================================================
"""

# Import packages

import numpy as np

#================ PARAMETERS ===================================================

# read variables
header = 0 # number of header lines to ignore

outdata = [1, 3] # column numbers to output

bincolumn = 3 # column to bin along
errorcolumn = 4
binmin = 18

#   File routes
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/"\
						+ "lightcurve/refinedCounts/"

# file name
infilename 	= "NGC1365_lcurve_4_0.5-10keV.qdp"


# Save output?

# histogram of binning?

hist = True

# Save output?

save = True
savefile = "binsout.dat"

outroute            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/"\
						#+ "spectra/"

# Highlighted lightcurve?

lc = True
timecolumn = 2
labels = False

#==================== Load data ================================================

# create file routes
location  = route+infilename
savelocation  = outroute+savefile

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
errorcolumn -= 1

#========================= Sort ================================================

start = True

for index in range(len(data[0])):

	if start == True:

		sortindex = [index]

		start = False
	
	else:

		i = 0

		if data[bincolumn][index] < data[bincolumn][sortindex[-1]]:
			while data[bincolumn][index] > data[bincolumn][sortindex[i]]:

				i += 1

			sortindex.insert(i,index)

		else:
			
			sortindex.append(index)

#======================== Bin ==================================================

bins = []

for index in np.arange(0,int(len(sortindex)),binmin):

	this = [[],0,0,0,0,0]
	err  = []
	total = 0

	for i in range(binmin):

		if index+i <= len(sortindex) - 1:
			this[0].append(sortindex[index+i]) 
			err.append(data[errorcolumn][sortindex[index+i]])

			total += data[countscolumn][sortindex[index+i]

	this[1] = data[bincolumn][sortindex[index]] # bin min

	if index+binmin-1 <= len(sortindex) - 1:	# bin max

		this[2] = data[bincolumn][sortindex[index+binmin-1]]
		
	else:
		this[2] = max(data[bincolumn])

	this[3] = (this[2]+this[1])/2.0

	err = np.array(err)

	this[4] = sum(err**2)

	this[5] = total

	bins.append(this)

print bins

#======================== print output =========================================
if save == True:

	out = open(savelocation,'w')

for b in range(len(bins)):

	low  = bins[b][1]
	high = bins[b][2]
	mid	 = bins[b][3]
	errs = bins[b][4]

	print low, " >= x > ", high, " ==> ",mid, ' +/- ', errs , " :\n"

	if save == True:

		out.write(str(low) + " >=x> " + str(high) + " :\n")

	output = ''

	for index in bins[b][0]:
		for dat in outdata:
			if dat != bincolumn:

				output = output + str(data[dat][index]) + '\t'

	print output, "\n"

	if save == True:

		out.write(output+"\n")


print "number of bins: ", len(bins)

if save == True:

	out.write("number of bins: " + str(len(bins)))

	out.close()

# plots

nplots = 0

if hist:

	nplots += 1

if lc:

	nplots += 1

if nplots == 1:

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)

if nplots == 2:

	fig = plt.figure()

# histogram

if hist:

	if nplots == 2:
		ax = fig.add_subplot(1,2,1)

	edges   = []
	counts  = []
	widths  = []

	for b in range(len(bins)):

		edges.append(bins[b][1])
		counts.append(bins[b][2])
		try:
			widths.append(data[bincolumn][bins[b+1][0][0]]-\
				data[bincolumn][bins[b][0][0]])
		except IndexError:
			widths.append(data[bincolumn][bins[b][0][-1]]-\
				data[bincolumn][bins[b][0][0]])

	plt.bar(edges,counts,widths)




# highlighted lightcurve

if lc:

	if nplots == 2:
		ax = fig.add_subplot(1,2,2)

	plt.scatter(data[timecolumn],data[bincolumn])

	for b in range(len(bins)):

		try:
			plt.axhspan(data[bincolumn][bins[b][0][0]], \
							data[bincolumn][bins[b+1][0][0]],alpha = 0.3)
		except IndexError:
			plt.axhspan(data[bincolumn][bins[b][0][0]], \
							data[bincolumn][bins[b][0][-1]],alpha = 0.3)

	if labels:
		for index in range(len(data[0])):
			plt.annotate(data[-1][index], 
					xy = (data[timecolumn][index],data[bincolumn][index]), 
					xytext = (-20,20),
					textcoords = 'offset points', ha = 'right', va = 'bottom',
					bbox = dict(boxstyle = 'round,pad=0.5', fc = 'blue', 
					alpha = 0.5), arrowprops = dict(arrowstyle = '->', 
					connectionstyle = 'arc3,rad=0'))	


if nplots > 0:

	plt.show()







