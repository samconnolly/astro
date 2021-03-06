# finding out about log interpolation

import numpy as np
import pylab as py

a = np.arange(1,11,1)

pl = np.power(a,2)

b = np.arange(1,11,0.5)

ipl = np.array([])
t = np.array([])
for x in b:

	for y in range(len(a)-1):

		if x >= a[y] and x < a[y+1]:

			t = np.append(t,( np.log(x) - np.log(a[y]) )  *( ( np.log(pl[y+1]) - np.log(pl[y]) ) \
									/ ( np.log(a[y+1]) - np.log(a[y]) ) ))

			ipl = np.append(ipl, np.exp( np.log(pl[y]) + ( \
						( np.log(x) - np.log(a[y]) )  * \
								( ( np.log(pl[y+1]) - np.log(pl[y]) ) \
									/ ( np.log(a[y+1]) - np.log(a[y]) ) ) ) ) )
b = np.arange(1,10,0.5)



la = np.log(a)
lb = np.log(b)

lpl = np.log(pl)
lipl = np.log(ipl)

print t, pl, ipl

py.plot(a,lpl)

py.plot(b,lipl)

py.show()

 
