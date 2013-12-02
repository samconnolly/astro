# colourplot.py

#
# A lovely example of how to make colour maps in python
#

# import packages

from matplotlib import mpl,pyplot
import numpy as np

# -------- DATA ----------------------------------------------------------------

# create random values
zvals = np.random.rand(100,100)*10-5

#   File route

route            = "/net/raid/raid1/xray/raid/sdc1g08/NetData/Ngc4395/lightcurve/refinedCounts/"

# file name

infilename 	= "NGC4395_lcurve_3_gti_0.5-10keV.qdp"

# header and footer

header  = 1         # length of any header in lines
dataend = False	  # footer?
endline = 999	  # length of footer in lines	

# lines to plot

x = 1    # x axis
y = 2    # y axis
c = 3    # colour values

#===============================================================================
#						Main Programme
#===============================================================================

#----------------------- Load Data ---------------------------------------------

# create file route

location  = route+infilename

# read data into array

start = 0

infile= open(location, 'r')


if dataend == False:

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

# ----------------------- Plotting ---------------------------------------------

fig = pyplot.figure()

# make a color map of the colour gradient, choosing the colours used
cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['red','yellow','green'],
                                           256)

# tell imshow about colour map so that only set colors are used
img2 = pyplot.imshow(zvals,interpolation='nearest',
                    cmap = cmap2,
                    origin='lower')

# make a color bar
pyplot.colorbar(img2,cmap=cmap2)

pyplot.show()
