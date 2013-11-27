# Creates a power spectrum from a lightcurve
# by Sam Connolly 
# Does not take into account sampling patterns (on purpose!)

# modules
import pylab as pl
from numpy import *

# power spectrum fourier transform function ----------------
      
def powcal(bsize, df, time, flux, avflux):

	ff=[]
	nhi=int(0.5/(bsize*df))+1
	npoints = len(flux)

	fr=zeros(nhi)
	fi=zeros(nhi)
      
	for k in range(0,nhi):
	      		
		a=2*pi*(k)*df

		for m in range(npoints):
        
			c=cos(a*time[m])
			s=sin(a*time[m])
			fr[k]+=((flux[m]-avflux)*c)
			fi[k]+=((flux[m]-avflux)*s)
        
		ff.append( ((1.0/df)) * (2.0/npoints**2) * (fr[k]**2+fi[k]**2))          
        	 
	return ff, nhi
# ---------------------------------------------------------------


# power spectrum fourier transform function ----------------
      
def spowcal(bsize, df, time, flux, avflux):

	ff=[]
	npoints = len(flux)

	fr=zeros(npoints)
	fi=zeros(npoints)
      
	for k in range(npoints):
	      		
		a=2*pi*(k)*df

		for m in range(npoints):
        
			c=cos(a*time[m])
			s=sin(a*time[m])
			fr[k]+=((flux[m]-avflux)*c)
			fi[k]+=((flux[m]-avflux)*s)
        
		ff.append((1.0/npoints**2) * (fr[k]**2+fi[k]**2) )
        	 
	return ff, npoints
# ---------------------------------------------------------------



# -- Binning function ----------------------------------------
      
def binps(nhi,freq,dff,minb,bfac):

	jj=0
	j1=0
	logftot=0.0
	ffav=0.0
	flast=bfac*freq[0]
	fprev=freq[0]  
	
	bff   = []
	bfreq = []

	for i1 in range(nhi):
	
		ffav=ffav+log10(dff[i1])+0.253
		j1=j1+1
		logftot=logftot+log10(freq[i1])

		if  i1 == nhi or freq[i1+1] >= flast:
			if  j1 >= minb:
		
				jj=jj+1
				bff.append( ffav/float(j1) )
				bfreq.append( logftot/float(j1) )
				fprev   =freq[i1]
				flast   =bfac*freq[i1]
				logftot =0.0
				ffav    =0.0
				j1      =0

	nbfreq=jj
        
	return bfreq, bff    

# -------------------------------------------------------------------     












