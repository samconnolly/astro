import numpy as numpy

time = [1,2,3,4,5,6,7,8,9,10]
data = [3,4,3,4,5,4,3,2,6,4]


binwidth = 2
nbins = int(time[-1]/binwidth)
binned = numpy.zeros(nbins+1)

for index in range(len(time)):
	timebin = int(time[index]/binwidth)
	binned[timebin] += data[index]

timearray = numpy.arange(0, nbins*binwidth,binwidth)

print  timearray, binned

