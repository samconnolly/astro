"""
uvotDataOut.py

Created on Tue Nov  5 13:30:21 2013

Author: Sam Connolly

re-jig uvot data into something more useful. And plot it if wanted. And compare
to X-ray if wanted. Extract flux and time data as a txt file.

"""

import pylab
import numpy as np

#================================================================================

route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365/uvot/"

# file names
infilename 	= "infile_main.dat"

header = 1

T_start = 56200  	# start and end times in MJD 
T_end   = 70000

plot = False

multiplot = True

xray = True

xheader = 2

softxrayfilename = "infile_xs.dat"
hardxrayfilename = "infile_xh.dat"

names  = ["UVW2"	,"UVM2"	,"UVW1"	,"U"	,"B"	,"V", "Soft X-ray", "Hard X-ray"]

# extract MJD and flux data as txt files... W2,M2,W1,U,B,V, soft-Xray, hard-Xray
#extract = [True,True,True,True,True,True,True,True]
extract = [False,False,False,False,False,False,False,False]
plotf = [True,True,True,True,True,True,True,True] # and which ones to plot...



#================================================================================

def s2mjd(s):
	'''
	Convert from seconds since 1st July 2001 to MJD 
	(not very accurate, but within a second...)
	'''

	DAY =  86400.0		# seconds in a day
	MJD2001 = 51910 		# MJD on 1st January 2001
	
	days = (s + 64.) / DAY  # number of days since 1/1/2001 at 
	
	return  MJD2001 + days

# create file routes
location  = route+infilename
xslocation  = route+softxrayfilename
xhlocation  = route+hardxrayfilename

# read UV data into array ---------

data = [[[] for i in range(5)] for j in range(6)] # array for each filter

start = 0			# line count
f =0				# filter number
filt = "none"		# current filter

infile= open(location, 'r')

for line in infile:
	
	linedata = line.split()
	
	if start == header:		# start when line count is past header 
		filt = linedata[8]

	if start >= header:		

		if linedata[8] != filt:	# change filter array if filter changes
			f += 1
			filt = linedata[8]

		mjd = s2mjd(float(linedata[1])) # find MJD...

		if T_start <= mjd <= T_end: # check if within time range
	
			# fill data array with data!
			data[f][0].append(mjd)	# MJD
			data[f][1].append(float(linedata[3]))		# Exposure Time
			data[f][2].append(float(linedata[4]))		# Flux
			data[f][3].append(float(linedata[5]))		# Flux Error
			data[f][4].append(linedata[8])				# Filter


	start += 1

infile.close()

# X-ray data if wanted ==========================================================

if xray:
	
	# read soft xray data into array --------------
	
	xsdata = [[] for i in range(4)]
	
	start = 0			# line count
	
	xsinfile= open(xslocation, 'r')
	
	for line in xsinfile:
		
		linedata = line.split()
	
		if start >= xheader:		
	
			if linedata[8] == 'a1':	# check quality
			
				mjd = float(linedata[0])			
			
				if T_start <= mjd <= T_end: # check if within time range			
					# fill data array with data!
					xsdata[0].append(mjd)		# MJD
					xsdata[1].append(float(linedata[3])) 	# Exposure time
					xsdata[2].append(float(linedata[4]))		# Flux
					xsdata[3].append(float(linedata[5]))		# Flux error

	
		start += 1
	
	xsinfile.close()
	
	# read hard xray data into array --------------
	
	xhdata = [[] for i in range(6)]
	
	start = 0			# line count
	
	xhinfile= open(xhlocation, 'r')
	
	for line in xhinfile:
		
		linedata = line.split()
	
		if start >= xheader:		
	
			if linedata[8] == 'a1':	# check quality
		
				mjd = float(linedata[0])			
			
				if T_start <= mjd <= T_end: # check if within time range	
				
					# fill data array with data!
					xhdata[0].append(float(linedata[0]))
					xhdata[1].append(float(linedata[3]))
					xhdata[2].append(float(linedata[4]))
					xhdata[3].append(float(linedata[5]))
		
		start += 1
	
	xhinfile.close()

# save as data files if wanted ==================================================

# UV filters
for f in range(6):
	
	if extract[f] == True:	
		
		fname = data[f][4][0] + ".dat"
		location = route + fname
		
		out = open(location, 'w')
		
		for i in range(len(data[f][0])):
			
			for j in [0,2,3]:
	
				out.write(str(data[f][j][i]) + '\t')
	
			out.write('\n')
	
		out.close()

# xray data

# soft
if extract[6] == True:
	
	fname = "XS.dat"
	location = route + fname
	
	out = open(location, 'w')
	
	for i in range(len(xsdata[0])):
		
		for j in [0,2,3]:

			out.write(str(xsdata[j][i]) + '\t')

		out.write('\n')

	out.close()
	
# hard
if extract[6] == True:
	
	fname = "XH.dat"
	location = route + fname
	
	out = open(location, 'w')
	
	for i in range(len(xhdata[0])):
		
		for j in [0,2,3]:

			out.write(str(xhdata[j][i]) + '\t')

		out.write('\n')

	out.close()

# plot if wanted ================================================================

if plot:
	
	colours = ["red","green","yellow","blue","orange","purple"]	
	

	# uv data for each filter	
	
	for f in range(6):
		
		# flux
		pylab.subplot(2,1,1)
		pylab.title("UV")		
		pylab.errorbar(data[f][0],data[f][2],yerr=data[f][3],color = colours[f],\
			marker='.', linestyle = 'none',capsize = 0)
		
	# x-ray data if wanted
	
	if xray:	
		
		pylab.subplot(2,1,2)
		pylab.title("XRAY")
		pylab.errorbar(xsdata[0],xsdata[2],yerr=xsdata[3],color = colours[0],\
			marker='.', linestyle = 'none',capsize = 0)
		pylab.errorbar(xhdata[0],xhdata[2],yerr=xhdata[3],color = colours[1],\
			marker='.', linestyle = 'none',capsize = 0)		
			
		
			
	pylab.show()
	
if multiplot:
	
	colours = ["red","green","black","blue","orange","purple","black","blue"]	
	

	
	nplots =  np.sum(plotf)		# total number of subplots
#	xp     = int(np.sqrt(nplots))	# x width
#	yp     = nplots/xp				# y width
	xp     = 1
	yp     = nplots
	pn     = 1  					# plot number
	# uv data for each filter	

	s = 0
	
	while plotf[s] == False:
		s += 1
		
	fig = pylab.figure()
	ax1 = pylab.subplot(yp,xp,pn)
	pylab.ylabel(names[s])
	pylab.errorbar(data[s][0],data[s][2],yerr=data[s][3],color = colours[s],\
		marker='.', linestyle = 'none',capsize = 0)

	pn +=1		

	
	for f in range(s+1,6):
		
		# flux
		if plotf[f] == True:
			pylab.subplot(yp,xp,pn,sharex=ax1)
			pylab.ylabel(names[f])
			pylab.errorbar(data[f][0],data[f][2],yerr=data[f][3],color = colours[f],\
				marker='.', linestyle = 'none',capsize = 0)
			
			pn +=1
		
	# x-ray hard and soft data 
	
	if plotf[f+1] == True:
		
		pylab.subplot(yp,xp,pn,sharex=ax1)
		pylab.ylabel(names[f+1])
		pylab.errorbar(xsdata[0],xsdata[2],yerr=xsdata[3],color = colours[f+1],\
			marker='.', linestyle = 'none',capsize = 0)
			
		pn += 1
		
	if plotf[f+2] == True:
		
		pylab.subplot(yp,xp,pn,sharex=ax1)	
		pylab.ylabel(names[f+2])
		pylab.errorbar(xhdata[0],xhdata[2],yerr=xhdata[3],color = colours[f+2],\
			marker='.', linestyle = 'none',capsize = 0)		
			
		pn +=1
		

	pylab.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
	pylab.setp([a.get_yticklabels() for a in fig.axes], visible=False)
	
	pylab.show()
	
	
	
	
	
	
	
	
	
	
