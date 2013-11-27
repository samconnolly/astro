from numpy import *

a= range(1000)

inCount = 0
totCount = 0

for x in a:

	r = random.normal()

	totCount += 1

	if r >= -2 and r <= 2:

		inCount += 1


print inCount, totCount

print 1 - (float(inCount)/float(totCount))
