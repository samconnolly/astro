"""
dataTimeDifference.py

Sam Connolly 13/02/2013

#===============================================================================
# Find the time differences between consecutive data points in a text file
#===============================================================================

"""

# -------- Input variables -----------------------------------------------------

header = 1 # number of header lines to ignore
plotend = False # stop plotting at a certain line?
endline = 46

timecolumn = 2 # column containing time data taken

#   File routes
route            = \
 "/net/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/lightcurve/refinedCounts/"

# file names
infilename 	= "NGC1365_lcurve_4_0.5-10keV.qdp"

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
	
timecolumn -= 1 

for t in range(len(data[timecolumn])-1):
    
    print data[timecolumn][t+1]-data[timecolumn][t]
    
    







