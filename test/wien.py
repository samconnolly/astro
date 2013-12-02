# ----Is Wien's Displacement Law True? (Probably) ----

from pylab import *
from math import exp
from numpy import *

temp = 5500

cplanck= 6.63e-34
clight = 3e8
cboltz  = 1.38e-23

bb    = []
larr  = []
wline = []
varr  = []

def planck(lam,temp):
	
	u = ( (8*pi*cplanck*clight) / (lam**5) ) * ( exp((cplanck*clight)/(lam*cboltz*temp)) - 1 )**(-1)
	
	return u


def wien(temp):

	maxlam = 2.89776829e-3*(temp**(-1))
	
	return maxlam
		
for i in arange(1e-7, 1e-5, 1e-8):

	bp = planck(i,temp)
	bb.append(bp)
	larr.append(i)

wmax = wien(temp)
print wmax

for i in arange(0,1000000,100):

	wline.append(wmax)
	varr.append(i)
	
plot(larr,bb)
plot(wline,varr)

show()
	

