import pylab as pl
from numpy import *

bwidth = 1.0

time   = arange(0,pi*8, 0.1)
flux   = 3*sin(time*0.5) #+ 2*sin(time) + 1*sin(time*2.0) 

def powcal(time, flux, bwidth):

	avflux = mean(flux)
	dt= time[-1]-time[0] 
	df= dt**(-1)

	ff=array([])
	freq=array([])
	npoints = len(flux)
	nhi= npoints #int(0.5*len(time))

	fr=zeros(nhi)
	fi=zeros(nhi)
      
	for k in range(nhi):
	      		
		a=2*pi*(k+1)*df

		for m in range(npoints):
        
			c=cos(a*time[m])
			s=sin(a*time[m])
			fr[k]+=((flux[m]-avflux)*c)
			fi[k]+=((flux[m]-avflux)*s)
        
		ff = append(ff, ( (((2.0*bwidth))/ ( (avflux**2)*(npoints) ) ) * (fr[k]**2+fi[k]**2))) #
		freq = append(freq,(((k+1)*df)))
	
        	 
	return ff, nhi, freq
# ---------------------------------------------------------------
def ipowcal(freq, ff, bwidth):

	avff = mean(ff)
	df= freq[-1]-freq[0] 
	dt= df**(-1)

	iflux=array([])
	itime=array([])	
	npoints = len(ff)
	nhi= npoints #int(0.5*len(freq))

	fr=zeros(nhi)
	fi=zeros(nhi)
      
	for k in range(nhi):
	      		
		a=2*pi*(k+1)*dt

		for m in range(npoints):
        
			c=cos(a*freq[m])
			s=sin(a*freq[m])
			fr[k]+=((ff[m]-avff)*c)
			fi[k]+=((ff[m]-avff)*s)
        
		iflux = append(iflux, ( (2.0*bwidth)/ ( (avff**2)*(npoints)) ) * (1.0/npoints)\
					* (fr[k]**2 - fi[k]**2) ) #
        	itime = append(itime,(((k+1)*dt)))

	 
	return iflux, nhi, itime

ff, n, freq = powcal(time, flux, bwidth)

iff, ni, itime = ipowcal(freq, ff, bwidth)

dff, dn, dfreq = powcal(itime, iff, bwidth)

ptime  = time/(2*pi)
iptime  = itime/(2*pi)
pfreq  = (2*pi)*(freq)
dpfreq  = (2*pi)*(dfreq)

pl.subplot(4,1,1)
pl.plot(ptime,flux)
pl.subplot(4,1,2)
pl.plot(pfreq,ff)
pl.subplot(4,1,3)
pl.plot(iptime,iff)
pl.subplot(4,1,4)
pl.plot(dpfreq,dff)

pl.show()


