"""
powerspec.py

Sam Connolly, late 2012

Functions to create a power spectrum from a lightcurve, and to bin it.

Does not take into account sampling patterns (on purpose!)
"""
# modules
import numpy as np

# -------------- power spectrum fast fourier transform function ----------------
def powcalfast(flux):
	'''
	Creates a power spectrum from a lightcurve, using a fast Fourier transform.

	Args:
			flux		- array of flux values

	Returns:
		(array) ff 		- the power spectrum
	'''

	ff = np.fft.fft(flux)

	return ff
 
# -------------- power spectrum fourier transform function ---------------------
def powcal(time, flux, bwidth):
	'''
	Creates a power spectrum from a lightcurve, using a full Fourier transform.

	Args:
			time		- array of time values
			flux		- array of flux values
			bwidth		- bin width....

	Returns:
		(array) ff 		- the power spectrum
		(float) nhi		- Nyquist frequency
	'''
	avflux = np.mean(flux)
	dt= time[-1]-time[0] 
	df= dt**(-1)

	ff=np.array([])
	npoints = len(flux)
	nhi= int(0.5*len(time))

	fr=np.zeros(nhi)
	fi=np.zeros(nhi)
      
	for k in range(nhi):
	      		
		a=2*np.pi*(k+1)*df

		for m in range(npoints):
        
			c=np.cos(a*time[m])
			s=np.sin(a*time[m])
			fr[k]+=((flux[m]-avflux)*c)
			fi[k]+=((flux[m]-avflux)*s)
        
		ff = np.append(ff, ( (2.0*bwidth)/ ( (avflux**2)*(npoints) ) )* \
							(fr[k]**2+fi[k]**2))
        	 
	return ff, nhi

# -- Logarithmising function ----------------------------------------
      
def logps(nhi,freq,dff):
	'''
	changes your lovely power spectrum into a logarithmic one.

	Args:
		nhi		- Nyquist frequency
		freq	- Frequency array
		dff		- power spectrum array

	Returns:
		lfreq (array) - Logarithmic frequencies
		lff	  (array) - Logarithmic power spectrum values
	'''

	lff   = []
	lfreq = []

	for i1 in range(nhi):
	
		lff.append(np.log10(dff[i1]) )
		lfreq.append(np.log10(freq[i1]))

	return lfreq, lff       











