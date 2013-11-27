from numpy import *
import pylab

f= open('data1.txt','r')


ea = array([])
na = array([])
dn = array([])

for x in f:
	e,a,d = x.split()
	ea = append(ea,float(e))
	na = append(na,float(a))
	dn = append(dn,float(d))

#--------------------------------------------
def n(E,w):

	x = 1.467e7/(w**2*0.25 + (E-1232)**2)

	return x
#------------------------------------------



def th(ea,w):

	nth = []

	for i in ea:

		nt = n(i,w)

		nth.append(nt)

	return nth

def diff(w,ea,na,dn):

	theory = th(ea,w)

	ri = (na - theory)
	res = (ri / dn)**2

	difference = sum(res)

	return difference

darr = []
warr = arange(100,140,0.1)

for i in warr:

	darr.append(diff(i,ea,na,dn))
	
print darr

thisth = th(ea,113)

pylab.errorbar(ea,na,yerr=dn)
pylab.plot(ea,thisth)

#pylab.plot(warr,darr)
pylab.show()



