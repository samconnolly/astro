# pivot contants finding test... Sam Connolly 08/04/13

import numpy as np
import pylab as plt


soft  = 0.5
split = 2.0
hard  = 10.0

x = np.arange(0.1, 20.1,0.1)

A = 2.0
alpha = -1.9

y =  A*(x**alpha)

#--------- pivot ---------------------------------------------------------------

Epiv  = 15.0
delta = 0.5

ypiv = y * ( (x / Epiv)**delta ) 


#--------- gradients -----------------------------------------------------------

grad = ( np.log(y[-1]) - np.log(y[0]) ) / ( np.log(x[-1]) - np.log(x[0]) )

pivgrad = ( np.log(ypiv[-1]) - np.log(ypiv[0]) ) / \
			 ( np.log(x[-1]) - np.log(x[0]) )

#----- multi pivot with hardness -----------------------------------------------


hardflux = np.array([])
softflux = np.array([])

start = soft/0.1
mid   = split/0.1 + 1
end   = hard/0.1  + 1

for d in np.arange(-1.0,1.0,0.1):

	piv = y * ( (x / Epiv)**d ) 

	softflux = np.append(softflux,sum(piv[start:mid]))
	hardflux = np.append(hardflux,sum(piv[mid:end]))


hardness = (hardflux - softflux) / (hardflux + softflux)
	

#-------- pivot model ----------------------------------------------------------

k 	 = 1.7614
beta = 0.4866

testhardflux = k*(softflux**beta)

#========= plot ================================================================

#print softflux, hardflux

kn = []
bn = []


for xi in range(len(softflux)-1):

	bi = np.log(hardflux[xi]/hardflux[xi+1])/np.log(softflux[xi]/softflux[xi+1])
	ki = (hardflux[xi])/((softflux[xi]**bi))

	kn.append(ki)
	bn.append(bi)

	print hardflux[xi], ki*(softflux**bi)

print np.mean(kn),np.mean(bn)


fig = plt.figure()

ax = fig.add_subplot(2,1,1)
ax.set_yscale('log')
ax.set_xscale('log')
                        
plt.plot(x,y)

plt.plot(x,ypiv)

ax2 = fig.add_subplot(2,1,2)

plt.plot(hardflux,softflux)

plt.plot(testhardflux,softflux)

plt.show()
