
"""
multiplot.py

Created on Wed Nov 13 11:26:49 2013

Author: Sam Connolly

Takes a load of data files and plots them below one another as subplots.

"""


# Import packages

import pylab as plt
import numpy as np


# --------- PARAMETERS ----------------------------------------------------------

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365/uvot/fix/"  # general path

# array of data filenames
fnames  = ["UVW2.dat",	"UVM2.dat","UVW1.dat","U.dat","B.dat","V.dat"]	
#["UVW1.dat"	,"UVW2.dat"	,"UVM2.dat"	,"U.dat"	,"V.dat"	,"B.dat"	,"XCountsTrim.dat"]	

# headers?
header = 0

# errors?
errors = True

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

#====================== Plot ====================================================
colours = ['red','blue','green','orange','purple','black','pink','yellow']

fig = plt.figure()

for p in range(len(fnames)):

	plt.subplot(len(fnames),1,p+1)

	if errors:
		plt.errorbar(data[p][0],data[p][1],yerr = data[p][2],
			marker = '.',linestyle='none',color=colours[p])
		plt.ylabel(fnames[p])
	else:
		plt.errorbar(data[p][0],data[p][1],marker = '.',
			linestyle='none',color=colours[p])
		plt.ylabel(fnames[p])

#fig.tight_layout(hspace=0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                    wspace=None, hspace=0)
plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

plt.show()




