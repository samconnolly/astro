# plot.py
# Sam Connolly 13/02/2013

#===============================================================================
# Simple, generic plotting programme to plot any two columns from an ascii data
# table, with errors, ignoring any header
#===============================================================================

# Import packages

#import numpy as np
import pylab as plt
import matplotlib

#================ PARAMETERS ===================================================

# read variables
header = 1 # number of header lines to ignore
plotend = False # stop plotting at a certain line?
endline = 46

single = False # plot sinlge column of data?
log = False # log plot?

xcolumn, ycolumn = 2,3  # column numbers to plot
xerrcolumn, yerrcolumn = None,None # column numbers for errors ('None', for none)

labels = True		# data labels?
labelcolumn = 1		# data label column

xlabel = "MJD"
ylabel = "Count Rate"

#   File routes
route            = "/net/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365/lightcurve/refinedCounts/"

# file names
infilename 	= "NGC1365_lcurve_4_gti_2-10keV.qdp"

#===============================================================================

# create file route
location  = route+infilename

# read data intoarray


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
				data[column].append(float(linedata[column]))
		
	start += 1

infile.close()
	
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

# fiddle

#data[xcolumn] = np.array(data[xcolumn]) - np.array(data[ycolumn])


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

	#plt.plot(data[xcolumn],data[ycolumn])


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

# line?
#lx, ly = [0.1875,2.38],[46.6,1.37]                                   
#plt.plot(lx,ly)



plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.show()





