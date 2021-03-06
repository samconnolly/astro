"""
maxminpoints.py

Sam Connolly, Sometime in early 2013...

# Programme to identify a given number of maximum and minimum points from 
# a data set, with the associated data.
"""
import numpy as np

# ================= INPUT PARAMETERS ===========================================

header  = 1 # number of header lines before data starts
columns = 3 # number of data columns
sortcol = 2 # column from which the max and min data should be found
nsort   = 10 # number of min and max values to find

# file route
route    = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/mainlc/refined/"

# file name
fname 	= "NGC1365_lcurve_3_0.5-10keV.qdp"

# ==============================================================================

sortcol -= 1

# create file route
location  = route+fname

# read data into 2-D arrays
start = 0

data  = [[] for i in range(columns)]

infile= open(location, 'r')

for line in infile:
	
	if start >= header:								# once past header
		linedata = line.split()						# split line into columns
		for col in range(columns):					# add data to array columns
			data[col].append(linedata[col])
	start += 1

infile.close()

low  = [[max(data[sortcol])]*nsort,[0] * nsort]
high = [[min(data[sortcol])]*nsort,[0] * nsort]

for y in range(len(data[sortcol])):

# min values

	for z in low[0]:
		if data[sortcol][y] < z:			# if data is lower than current
			low[0].append(data[sortcol][y])	# add to array
			low[1].append(y)				# note position
			rm = max(low[0])				# find highest value in low array
			for n in range(len(low[0])):	# find equivalent position
				if low[0][n] == rm:
					rmp = low[1][n]
			low[0].remove(rm)				# remove this value
			low[1].remove(rmp)				# and its position
			break							# break loop, to prevent doubles

# min values

	for a in high[0]:
		if data[sortcol][y] > a:			# if data is higher than current
			high[0].append(data[sortcol][y])	# add to array
			high[1].append(y)				# note position
			rm = min(high[0])				# find lowest value in low array
			for n in range(len(high[0])):	# find equivalent position
				if high[0][n] == rm:
					rmp = high[1][n]
			high[0].remove(rm)				# remove this value
			high[1].remove(rmp)				# and its position
			break							# break loop, to prevent doubles

# print results

print "\nLowest values:\n"

for val in low[1]:
	string = ""
	for col in range(columns):
 		string = string + "	" + data[col][val]    
	print string

print "\n"

print "Highest values:\n"

for val in high[1]:
	string = ""
	for col in range(columns):
 		string = string + "	" + data[col][val]    
	print string

print "\n"




