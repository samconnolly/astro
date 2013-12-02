# gaussian.py
import numpy as np
import pylab as plt

def gaussian(v,mean,sigma,p):

	val = ( 1.0/ ( sigma*np.sqrt(2.*np.pi) ) ) * \
						( np.exp( (-0.5)* (((v-mean)/sigma)**2) ) ) 

	if p:	 
		#print 	( 1.0/ ( sigma*np.sqrt(2.*np.pi) ) )
		#print   ( np.exp( (-0.5)* (((v-mean)/sigma)**2) ) )
		#print	np.exp( )
		print val

	return val

#mean = 0.000187218
#sigma = 1.81791e-05
#value = 0.000194616025551

mean = 0.
sigma = .25
value = .25

g = gaussian(value, mean, sigma, True)

gauss = []
#lim   = np.arange(0.0001,0.0003,0.000001)
lim   = np.arange(-10.,10.,0.01)

for x in lim:

	gauss.append(gaussian(x, mean, sigma,False))

print np.trapz(gauss)

plt.plot(lim,gauss)
plt.show()
