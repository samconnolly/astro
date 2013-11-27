
"""
multiXcor.py

Created on Wed Nov 13 11:51:11 2013

Author: Sam Connolly

cross-correlate a load of different lightcurves with a particular one.

requires : callxcor.py

"""


# Import packages

from callxcor     import xcor
import pylab as plt
import numpy as np


# --------- PARAMETERS ----------------------------------------------------------

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365/uvot/fix/"  # general path

# array of data filenames
fnames  = ["UVW2.dat"	,"UVM2.dat"	,"UVW1.dat"	,"U.dat"	,"B.dat"	,"V.dat","XS.dat","XH.dat"]

xcord = 5 # array index of xcor data set

# headers?
header = 0

# bins in xcor
n_bins = 200
trange = 150

#====================== Read in data ============================================

# declare data array
data = [[[],[],[]] for i in range(len(fnames))]

for i in range(len(fnames)):
	
	location = route+fnames[i]			# create file route
	infile= open(location, 'r')			# open file
	
	start = 0
	
	for x in infile:
		
		currtime, currflux,currfluxerr = x.split()
		
		if start >= header:
			data[i][0].append(float(currtime))
			data[i][1].append(float(currflux))
			data[i][2].append(float(currfluxerr))
			
		start = 1	
	
	infile.close()

data = np.array(data)


# ========== Run xcor function on data ==========================================
# Create array of cross-correlation functions for the data sets

xca = [[] for i in range(len(data))]

for x in range(len(data)):

		xc,tl,nb = xcor(data[x][1], data[x][0],data[xcord][1], data[xcord][0],\
					n_bins, True,trange)
		
		xca[x].append(tl)
		xca[x].append(xc)


# ======= Plots =================================================================
# plot any figures requested by input params

xp     = 1
yp     = len(data)

fig = plt.figure()

for x in range(len(data)):

	plt.subplot(yp,xp,x + 1)
	plt.ylabel(fnames[x])
	
	plt.plot(xca[x][0],xca[x][1])

	plt.legend()

	plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
	#plt.setp([a.get_yticklabels() for a in fig.axes], visible=False)
	plt.axis([-trange, trange, -1, 1])

plt.show()
		
		
		
		
		
		
		
		
		
		
		
		
