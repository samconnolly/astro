
from numpy import *

inputfile= open("lc_filtered_t1.txt", 'r') # open input file

data = []	#create empty arrays
time = []
error= []
	
for x in inputfile:					# read data into arrays from file
	cdata,ctime,cerror = x.split() 
	data.append(cdata)
	time.append(ctime)
	error.append(cerror)

inputfile.close()	#close input file

avg = mean(data)	# average data

outputfile= open("output.txt.", 'w')	# create output file

for y in data:
	outputfile.write(time[y], data[y] - avg, error[y])	# write new data to output file

outputfile.close()	# close output file
