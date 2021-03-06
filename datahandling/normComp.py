
"""
normComp.py

Created on Wed Nov 13 11:26:49 2013

Author: Sam Connolly

Normalise data sets to mean and SD 1, for comparison of variability. X,Y and
Y errors in each data set. Then plots them all together with a legend.

"""


# Import packages

import pylab as plt
import numpy as np


# --------- PARAMETERS ----------------------------------------------------------

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365/uvot/fix/"  # general path

# array of data filenames
fnames  = ["UVW2.dat",	"UVM2.dat","UVW1.dat","U.dat","B.dat","V.dat","XCountsTrim.dat"]	
#["UVW1.dat"	,"UVW2.dat"	,"UVM2.dat"	,"U.dat"	,"V.dat"	,"B.dat"	,"XCountsTrim.dat"]	

# headers?
header = 0

# errors?
errors = False
line   = True
markers = False

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

#====================== Normalise ===============================================
# set mean = 0 and SD = 1	
	
for a in range(len(fnames)):
	
	av = np.mean(data[a][1])
	sd = np.std(data[a][1])
	
	data[a][1] = (data[a][1] - av)/sd
	data[a][2] = (data[a][2])/sd

#====================== Plot ====================================================
colours = ['red','blue','green','orange','purple','black','pink','yellow']

if line:				# lines on graph?
	line = '-'
else:
	line = 'none'

if markers:			# markers on graph?
	markers = 3
else:
	markers = 0

for p in range(len(fnames)):

	if errors:
		plt.errorbar(data[p][0],data[p][1],yerr = data[p][2],
			marker = '.',ms = markers,linestyle=line,color=colours[p],
				label = fnames[p])
	else:
		plt.errorbar(data[p][0],data[p][1],marker = '.',ms = markers,
			linestyle=line,color=colours[p],label = fnames[p])

plt.legend()		
plt.show()




