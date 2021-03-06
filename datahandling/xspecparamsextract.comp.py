"""
xspecparamsextract.py

Sam Connolly 27/02/2013

#===============================================================================
# extract the paramaters of multiple fits in xspec from a copy of the output
# and plot two for comparison. And save in column format if required.
#===============================================================================
"""

# Import packages

import pylab as plt
import matplotlib
import numpy as np

#================ PARAMETERS ===================================================

# read variables
header = 1 # number of header lines to ignore
specnum = 10 # number of spectra
paramnum = 14 #number of paramaters

single1 = False # plot single column of data? (x column, plot 1)
single2 = False # (x column, plot 2)

# plot 1
x1, y1 = 14, 6 # paramater numbers to plot, plot 1 (from 1st spectrum)

# plot 2
x2, y2 = 14, 8 # paramater numbers to plot, plot 2 (from 1st spectrum)

totfluxX1 = False # Or plot against total flux for each spectrum...
totfluxX2 = False 

totflux = [0.1873, 0.2725, 0.37165, 0.50975, 0.6437,\
				 0.8219, 1.12475, 1.33, 1.746, 2.3745]
totfluxerr = [0.0644,0.0174,0.02445,0.1051,0.1626,\
				0.1404,0.14825,0.082,0.343,0.2855]

labels1 = False		# numbered data labels?
labels2 = False

log1 = True			# log graph?
log2 = True

#   File routes
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/"\
						+ "spectra/binsum/"

# file names
infilename 	= 'absorifit.txt' #"fit.dat"


# saving?
save = True

savefname = 'fitparams.dat'

#===============================================================================

# create file routes
location  = route+infilename
savelocation = route+savefname

# read data intoarray

pnum, cnum, cname, pnam, unit, value, plusminus, error = 0,0,0,0,0,0,0,0
apnum, acnum, acname, apnam, aunit, avalue, aplusminus, aerror\
					 = [],[],[],[],[],[],[],[]
arrays = [apnum, acnum, acname, apnam, aunit, avalue, aplusminus, aerror]

labels = []

start =  - header
spec  = 1
infile= open(location, 'r')

for line in infile:
	if spec <= specnum:
	
		pnum, cnum, cname, pnam, unit, value, plusminus, error \
							= 0,0,'','','',0.0,'',0.0

		if start >= 0:
		
			if start != paramnum: 

				data = line.split()
								
				if len(data) == 7:

					if data[6] == "frozen":

						pnum, cnum, cname, pnam, unit,value, error = data
						error = 0.0
					else:

						pnum, cnum, cname, pnam, value, plusminus, error = data

				if len(data) == 8:
					
					pnum, cnum, cname, pnam, unit, value, plusminus, error = data


				if len(data) == 6:
		
					pnum, cnum, cname, pnam, value, error = data

					if data[5] == "frozen":

							error = 0.0

				values = [int(pnum), int(cnum), cname, pnam, unit,\
							 float(value), plusminus, float(error)]

				for val in range(len(values)):

					arrays[val].append(values[val])

				if spec == 1:

					labels.append(pnam)

			else:
				start = -1
				spec += 1

			


			
		start += 1

infile.close()

params = [[[] for i in range(paramnum)],[[] for i in range(paramnum)]]

i = 0
s = 0
p = 0

for val in range(len(arrays[5])):
	
	params[0][p].append(arrays[5][i])
	
	if arrays[6][i] == '=':
		params[1][p].append(arrays[7][p])

	else:
		params[1][p].append(arrays[7][i])

	i += paramnum
	s += 1

	if s == specnum:
		p += 1
		s = 0
		i = p

x1 -= 1 
y1 -= 1 

x2 -= 1 
y2 -= 1 

# total flux plot?

if totfluxX1:

	while x1 == y1:
		if x1 == paramnum:
			x1 = -1
		x1+=1

	params[0][x1] = totflux
	params[1][x1] = totfluxerr

if totfluxX2:

	while x1 == y1:
		if x1 == paramnum:
			x1 = -1
		x1+=1

	params[0][x2] = totflux
	params[1][x2] = totfluxerr

	labels[x1] = "total flux"
	labels[x2] = "total flux"

#======= save if required ======================================================

if save:

	out = open(savelocation, 'w')

	for l in range(len(params[0][0])):
		for p in range(paramnum):

			out.write(str(params[0][p][l]) + '\t')
			out.write(str(params[1][p][l]) + '\t')
		out.write('\n')

	out.close()

#================ plot with pylab ==============================================

axisrange1 = range(len(params[0][x1]))
axisrange2 = range(len(params[0][x2]))

lowerrx1 = min(params[0][x1])*0.5
lowerrx2 = min(params[0][x2])*0.5
lowerry1 = min(params[0][y1])*0.5
lowerry2 = min(params[0][y2])*0.5



# make sure lower error bars do not take the value to zero or below, 
# add lower limit error if so

berrorsx1 = []

for q in range(len(params[0][x1])):

	if (params[0][x1][q] - params[1][x1][q]) <= 0:

		berrorsx1.append(params[0][x1][q] - lowerrx1)

	else:

		berrorsx1.append(params[1][x1][q])

xerr1 = [berrorsx1,params[1][x1]]

berrorsx2 = []

for q in range(len(params[0][x2])):

	if (params[0][x2][q] - params[1][x2][q]) <= 0:

		berrorsx2.append(params[0][x2][q] - lowerrx2)

	else:

		berrorsx2.append(params[1][x2][q])

xerr2 = [berrorsx2,params[1][x2]]

berrorsy1 = []

for q in range(len(params[0][y1])):

	if (params[0][y1][q] - params[1][y1][q]) <= 0:

		berrorsy1.append(params[0][y1][q] - lowerry1)

	else:

		berrorsy1.append(params[1][y1][q])
	
yerr1 = [berrorsy1,params[1][y1]]

berrorsy2 = []

for q in range(len(params[0][y2])):

	if (params[0][y2][q] - params[1][y2][q]) <= 0:

		berrorsy2.append(params[0][y2][q] - lowerry2)

	else:

		berrorsy2.append(params[1][y1][q])

yerr2 = [berrorsy2,params[1][y2]]


# PLOT

fig = plt.figure()
ax = fig.add_subplot(1,2,1)


if single1 == False:

	plt.errorbar(params[0][x1],params[0][y1], xerr = xerr1, \
			yerr = yerr1, marker='.', color = 'red', \
				ecolor = 'grey', linestyle = 'none',capsize = 0)
else:
	
	plt.errorbar(axisrange1, params[0][x1], xerr = xerr1, \
					marker='.', color = 'red', \
						ecolor = 'grey', linestyle = 'none',capsize = 0)

if log1 == True:

	ax.set_yscale('log')
	ax.set_xscale('log')
	ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	labels[x1] = "log " + labels[x1]
	labels[y1] = "log " + labels[y1] 


plt.xlabel(labels[x1])
plt.ylabel(labels[y1])
plt.title(labels[x1] + " vs " + labels[y1])

if labels1:

	for index in range(len(params[0][0])):
		plt.annotate(index +1, 
				xy = (params[0][x1][index], params[0][y1][index]), 
				xytext = (-20,20),
				textcoords = 'offset points', ha = 'right', va = 'bottom',
				bbox = dict(boxstyle = 'round,pad=0.5', fc = 'blue', alpha = 0.5),
				arrowprops = dict(arrowstyle = '->', 
				connectionstyle = 'arc3,rad=0'))

ax = fig.add_subplot(1,2,2)

if single2 == False:

	plt.errorbar(params[0][x2],params[0][y2], xerr = xerr2, \
			yerr = yerr2, marker='.', color = 'red', \
				ecolor = 'grey', linestyle = 'none',capsize = 0)

else:
	
	plt.errorbar(axisrange2, params[0][x2], xerr = xerr2, \
					marker='.', color = 'red', \
						ecolor = 'grey', linestyle = 'none',capsize = 0)

if log2 == True:

	ax.set_yscale('log')
	ax.set_xscale('log')
	ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	labels[x2] = "log " + labels[x2]
	labels[y2] = "log " + labels[y2] 

plt.xlabel(labels[x2])
plt.ylabel(labels[y2])
plt.title(labels[x2] + " vs " + labels[y2])

if labels2:

	for index in range(len(params[0][0])):
		plt.annotate(index +1,
				xy = (params[0][x2][index], params[0][y2][index]), 
				xytext = (-20,20),
				textcoords = 'offset points', ha = 'right', va = 'bottom',
				bbox = dict(boxstyle = 'round,pad=0.5', fc = 'blue', alpha = 0.5),
				arrowprops = dict(arrowstyle = '->', 
				connectionstyle = 'arc3,rad=0'))

plt.show()



