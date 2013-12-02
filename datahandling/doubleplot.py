"""
plot.py

Sam Connolly 13/02/2013

#===============================================================================
# Plot two simulataneous data sets with different y-axes (e.g. multiwavelength)
# on different plots if wanted. And add a time-lag to one data set. 
# And a y adjustment.
#===============================================================================

"""

# Import packages

import numpy as np
import pylab as plt
import matplotlib

#================ PARAMETERS ===================================================

# read variables
header = 1 # number of header lines to ignore

xcolumn, ycolumn = 1, 2 # column numbers to plot
xerrcolumn, yerrcolumn = None,None # column numbers for errors ('None', for none)
xcolumn2, ycolumn2 = 1, 2 # column numbers to plot
xerrcolumn2, yerrcolumn2 = None,None # column numbers for errors ('None', for none)

timelag = -40. # set time lag for data set 2
adjustment = -2.5 # set y-axis adjustment to align plots if desired

sameplot = True

xlabel = "MJD"
ylabel = "Flux"

#   File routes
route            = "/net/raid/raid1/xray/raid/sdc1g08/NetData/xte+swiftdat/"
route2           = "/net/raid/raid1/xray/raid/sdc1g08/NetData/amidat/refined/"

# file names
infilename 	= "5548_xte_swift_r.qdp"
infilename2 	= "5548_ami_r.qdp"

#===============================================================================

# create file route
location  = route+infilename
location2  = route2+infilename2

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

start = 0

infile2= open(location2, 'r')

for line in infile2:
	
	linedata = line.split()
	
	if start == header:
		columns = len(linedata)
		data2 = [[] for x in range(columns)]

	if start >= header:
		for column in range(columns):
			if len(linedata) == columns:
				data2[column].append(float(linedata[column]))
		
	start += 1

infile2.close()

# set up correct columns for plotting, errors
	
xcolumn -= 1 
ycolumn -= 1
xcolumn2 -= 1 
ycolumn2 -= 1 

if xerrcolumn == None:

	xerrs = xerrcolumn

else:

	xerrs = data[xerrcolumn]


if yerrcolumn == None:

	yerrs = yerrcolumn

else:

	yerrs = data[yerrcolumn]


if xerrcolumn2 == None:

	xerrs2 = xerrcolumn2

else:

	xerrs2 = data[xerrcolumn2]


if yerrcolumn2 == None:

	yerrs2 = yerrcolumn2

else:

	yerrs2 = data[yerrcolumn2]

# add time lag & flux adjustment to 2nd data set

for x in range(len(data2[xcolumn])):

	data2[xcolumn][x] += timelag

for y in range(len(data2[ycolumn])):

	data2[ycolumn][y] += adjustment

# plot with pylab

fig = plt.figure()

if sameplot == True:
	ax = fig.add_subplot(1,1,1)
else:
	ax = fig.add_subplot(2,1,1)


plt.errorbar(data[xcolumn],data[ycolumn],xerr = xerrs, yerr= yerrs,\
	marker='.', color = 'red', \
	ecolor = 'grey', linestyle = '-',capsize = 0)



if sameplot == False:

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

	ax2 = fig.add_subplot(2,1,2)



plt.errorbar(data2[xcolumn2],data2[ycolumn2],xerr = xerrs2, yerr= yerrs2,\
	marker='.', color = 'blue', \
	ecolor = 'grey', linestyle = '-',capsize = 0)


plt.xlabel(xlabel)
plt.ylabel(ylabel)

lims = [5500,6200]

ax.set_xlim(lims) 

if sameplot == False:
	ax2.set_xlim(lims)

plt.show()





