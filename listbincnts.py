# listbincnts.py
# Sam Connolly 27/06/2013

#===============================================================================
# bin data according in an ascii file of column data, such that
# each bin has a minimum total from one column, ordered according to another
# giving the bin of each data point as a LIST. Also, a minwidth is available.
# UNEVEN BINS.
#===============================================================================

# Import packages

import pylab as plt

#================ PARAMETERS ===================================================

# read variables
header = 1 # number of header lines to ignore

bincolumn = 6 # column to bin along

exposurecolumn = 3 # exposure time column

mincount = True # minimum total for some value in each bin?
mincolumn = 12
binmin = 1000

minnum = False # minimum number of points in each bin?
countmin = 5

minwidth = True # minimum bin width?
widthmin = 0.025

#   File routes
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc4395/"\
						+ "lightcurve/raw/"

# file name
infilename 	= "NGC4395_lcurve_gti_2-10keV.txt"

# quality check?

check = True

# histogram of binning?

hist = True

# Save output?

save = True
savefile = "binsout.dat"

outroute            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc4395/"\
						+ "spectra/gtihardbin/"

print outroute

# Highlighted lightcurve?

lc = True
timecolumn = 2
labels = True

#==================== Load data ================================================


# create file routes
location  = route+infilename
savelocation  = outroute+savefile

# read data intoarray

start = 0

infile= open(location, 'r')

num = 1

for line in infile:
	
	linedata = line.split()

	if start == header:
		columns = len(linedata)
		data = [[] for x in range(columns + 1)]

	if start >= header:

		if check == False:

			linedata[10] = 'a1'

		if linedata[10] == 'a1':

			for column in range(columns):
				if len(linedata) == columns:

					try:
						data[column].append(float(linedata[column]))
					except ValueError:
						data[column].append(linedata[column])

			data[-1].append(num)

		num   += 1

	start += 1

infile.close()

bincolumn  -= 1
mincolumn  -= 1
timecolumn -= 1
exposurecolumn -= 1

if minwidth == False:  # turn off minimum width if required

	widthmin = 0

if minnum == False:

	countmin = 0

#========================= Sort according to bincolumn =========================

# create array of location indices for sorted list

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
end = False
index = 0
total = 0
nbin = 0
nbinned = 0

this = [[],[],0]

for index in range(len(sortindex)):

	this[0].append(sortindex[index]) # add index to bin
	this[1].append(data[-1][sortindex[index]]) # add actual index to bin

	nbinned += 1

	total += data[mincolumn][sortindex[index]] # add counts

	if mincount == False:

		if (data[bincolumn][this[0][-1]] - \
					data[bincolumn][this[0][0]]) >= widthmin:

			if len(this[0]) >= countmin:
					
					this[2] = total
					bins.append(this)
					nbin += 1
					this = [[],[],0]
					total = 0

	if mincount == True:

		if total > binmin:			# change bin at sufficient counts

			if (data[bincolumn][this[0][-1]] - \
					data[bincolumn][this[0][0]]) >= widthmin:

				if len(this[0]) >= countmin:
					
					this[2] = total
					bins.append(this)
					nbin += 1
					this = [[],[],0]
					total = 0

this[2] = total

print bins[-1]

if this[2] > binmin and mincount == True and mincount == False:

	bins.append(this)
	nbin += 1

elif len(this[0]) > binmin and mincount == False and mincount == True:

	bins.append(this)
	nbin += 1

elif len(this[0]) > binmin and this[2] > binmin \
			and mincount == True and mincount == True:

	bins.append(this)
	nbin += 1

else:

	for p in range(len(this[0])):

		bins[-1][0].append(this[0][p])
		bins[-1][1].append(this[1][p])

	bins[-1][2] += this[2]

print bins[-1]

#======================== print & save output ==================================

totcnts = 0

if save == True:

	out = open(savelocation,'w')

for b in range(len(bins)):

	low  = data[bincolumn][bins[b][0][0]]
	try:
		high = data[bincolumn][bins[b+1][0][0]]
	except IndexError:
		high = data[bincolumn][bins[b][0][-1]]
	mid	 = (low+high)/2.0
	cnts = bins[b][2]
	totcnts += cnts

	print low, " >= x > ", high, " ==> ",mid, "counts:", str(cnts), " :\n"

	if save == True:

		out.write(str(low) + " >=x> " + str(high) + " :\n")

	output = ''

	for index in bins[b][1]:
	
				output = output + str(index) + '\t'

	print output, "\n"

	if save == True:

		out.write(output+"\n")

print "Number of binned points:", nbinned
print "Number of bins: ", len(bins)
print "Total counts: ", totcnts
print "Total exposure time: "

if save == True:

	out.write("number of bins: " + str(len(bins)))

	out.close()

	print "Saved as:" + savefile + "in:" + outroute

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

		edges.append(data[bincolumn][bins[b][0][0]])
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







