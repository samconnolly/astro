"""
# plot.py
# Sam Connolly 13/02/2013

#===============================================================================
# Simple, generic plotting programme
#===============================================================================

Capable of:
 	- Plotting any two columns from an ascii data table
	- Plotting a single column of data against integers
	- error bars if wanted
	- ignoring any header lines
	- stopping data input at a given line (if there is a footer)
	- data labels
	- Plot labels

"""

# Import packages

#import numpy as np
import pylab as plt
import matplotlib

#================ PARAMETERS ===================================================

# read variables
header = 0 		# number of header lines to ignore
plotend = False # stop plotting at a certain line?
endline = 177

single = False # plot sinlge column of data?
log = False # log plot?

xcolumn, ycolumn = 1,2  # column numbers to plot
xerrcolumn, yerrcolumn = None,3 # column numbers for errors ('None', for none)

labels = False		# data labels?
labelcolumn = 1		# data label column

xlabel = "MJD"
ylabel = "Count Rate"

#   File routes
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365/uvot/fix/"

# file names
infilename 	= "XCountsTrim.dat"

#===============================================================================

# create file route
location  = route+infilename

# read data into array


start = 0

infile= open(location, 'r')


if plotend == False:

	endline = 99999999999999999

for line in infile:
	
	linedata = line.split()
	
	if start == header:
		columns = len(linedata)
		data = [[] for x in range(columns)]

	if start >= header and start < endline:
		for column in range(columns):
			if len(linedata) == columns:
				
				try:
					data[column].append(float(linedata[column]))
				except ValueError:
					data[column].append(linedata[column])
		
	start += 1

infile.close()

# ------------------------------------------------------------------------------

# setup columns
xcolumn -= 1 
ycolumn -= 1 

if xerrcolumn:
	xerrcolumn -= 1 
	xerrs = data[xerrcolumn]

else:
	xerrs = None

if single == False:

	if yerrcolumn:
		yerrcolumn -= 1
		yerrs = data[yerrcolumn]

	else:
		yerrs = None

# plot with pylab

fig = plt.figure()

ax = fig.add_subplot(1,1,1)

if log == True:

	

	ax.set_yscale('log')
	ax.set_xscale('log')

	ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())


if single == False:

	plt.errorbar(data[xcolumn],data[ycolumn],xerr = xerrs, yerr= yerrs,\
			marker='.', color = 'red', \
			ecolor = 'grey', linestyle = 'none',capsize = 0)


else:

	axisrange = range(len(data[xcolumn]))
	plt.scatter(axisrange, data[xcolumn], yerr= xerrs,\
			marker='.', color = 'red', \
			ecolor = 'grey', linestyle = 'none',capsize = 0)

if labels:

	labelcolumn -= 1

	for index in range(len(data[0])):
		plt.annotate(data[labelcolumn][index], 
				xy = (data[xcolumn][index], data[ycolumn][index]), 
				xytext = (-20,20),
				textcoords = 'offset points', ha = 'right', va = 'bottom',
				bbox = dict(boxstyle = 'round,pad=0.5', fc = 'blue', alpha = 0.5),
				arrowprops = dict(arrowstyle = '->', 
				connectionstyle = 'arc3,rad=0'))


plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.show()





