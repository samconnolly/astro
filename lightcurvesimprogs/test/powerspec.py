"""
powerspec.py

Sam Connolly, late 2012

Functions to create a power spectrum from a lightcurve, and to bin it.

Does not take into account sampling patterns (on purpose!)
"""

# modules
from numpy import *


# power spectrum fourier transform function ----------------
      
def powcal(df, time, flux, avflux):
	'''
	Creates a power spectrum from a lightcurve. Otherwise known as a full
	Fourier transform.

	Args:
			df			- not sure...
			time		- array of time values
			flux		- array of flux values

	Returns:
		(array) ff 		- the power spectrum
		(float) nhi		- the nyquist frequency
	'''

	ff=[]
	nhi=int(0.5*len(time))
	npoints = len(flux)

	fr=zeros(nhi)
	fi=zeros(nhi)

	avflux = np.mean(flux)
      
	for k in range(nhi):
	      		
		a=2*pi*(k+1)*df

		for m in range(npoints):
        
			c=cos(a*time[m])
			s=sin(a*time[m])
			fr[k]+=((flux[m]-avflux)*c)
			fi[k]+=((flux[m]-avflux)*s)
        
        	ff.append( (1.0/df) * (2.0/npoints**2) * (fr[k]**2+fi[k]**2))

	return ff, nhi
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
	bperr = []

	for i1 in range(nhi):
	
		ffav=ffav+log10(dff[i1])+0.253
		j1=j1+1
		logftot=logftot+log10(freq[i1])

		if  i1 == nhi or freq[i1+1] >= flast:
			if  j1 >= minb:
		
				jj=jj+1
				bff.append( ffav/float(j1) )
				bfreq.append( logftot/float(j1) )
				bperr.append(0.0)
					
				for k1 in range(i1-(j1-1),i1):
				
					bperr[-1]=bperr[-1]+(log10(dff[k1])\
							+0.253-bff[-1])**2
			
				bperr[-1]=sqrt(bperr[-1]/(j1*float(j1-1)))
	
				fprev   =freq[i1]
				flast   =bfac*freq[i1]
				logftot =0.0
				ffav    =0.0
				j1      =0

	nbfreq=jj
        
	return bfreq, bff, bperr       

# -------------------------------------------------------------------     
      










