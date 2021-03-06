# ------------------------------------------------------------------------------
# Light curve simulation programme, using the Timmer & Koenig method
# Sam Connolly
# ------------------------------------------------------------------------------

# Import packages
from powerspeced import powcal
from pylab import *
import numpy as numpy

# define as a programme to allow external importing
# vals e.g. low = 0.00, High =2.00, brk=0.10

def lcsim(low,high,brk,seed):

	# Parameters

	length       =512           # length of final light curve (ideally a power of 2)
	longlength   =length*10      # length of initial light curve (from which we 
			             # select a section of length ld)
	psdindexLow  =low            # PSD low-frequency index
	psdindexHigh =high           # PSD high-frequency index 
	breakfreq    =brk            # PSD break frequency
	meanCR       =3.27          # mean count rate of the light curve (if needed)
	sdCR         =0.000403375  # standard deviation of the light curve (if needed)
	randomSeed   =seed            # random seed

	# ================================================================================
	# --------- Main Programme -------------------------------------------------------
	# ================================================================================
	
	# --------- Create power spectrum ------------------------------------------------

	# Create frequency array for the initial light curve, up to the Nyquist frequency
	frequency = numpy.arange(1.0, longlength/2+1, 1.0)/longlength 

	# define the power-law form of the PSD, i.e. a two-part law with a break
	powerlaw = numpy.piecewise(frequency,  [frequency<=breakfreq, frequency>breakfreq], 
        	   [lambda frequency: (frequency/breakfreq)**(-psdindexLow) , 		
        	    lambda frequency: (frequency/breakfreq)**(-psdindexHigh) ])

	# -------- Create two arrays of gaussian-distributed random numbers for each frequency

	np.random.seed(32+randomSeed)                               
	random1 = numpy.random.normal(0,1,(longlength/2))
	np.random.seed(891+randomSeed) 
	random2 = numpy.random.normal(0,1,(longlength/2))

	# -------- Add noise to the power law (PL) using the random numbers ---------------
	# (Multiply random numbers by the square route of half the PL value at each freq)

	real = (numpy.sqrt(powerlaw*0.5))*random1
	imag = (numpy.sqrt(powerlaw*0.5))*random2

	# ----- create array of Fourier components--------------------------------------------
	# (+ve values use arrays above, -ve values are conjugates of +ve ones each freq)

	positive = numpy.zeros(longlength/2,complex)  # declare complex array for +ve values
	negative = numpy.zeros(longlength/2,complex)  # declare complex array for -ve values
                             
	for i in range(longlength/2):                                    

 		positive[i]=complex(real[i],imag[i]) # read real & imaginary parts into +ve array
		negative[i]=positive[i].conjugate()  # read conjugates of these into -ve array 
 	                         
	revnegative = negative[::-1]       	     # reverse negative array

	# join negative and positive arrays
                             
	noisypowerlaw = numpy.append(positive[0:longlength/2-1],revnegative[1:longlength/2+1])
	znoisypowerlaw = numpy.insert(noisypowerlaw,0,complex(0.0,0.0)) # add a zero to start 

	# --------- Fourier transform the noisy power law -------------------------------------

	inversefourier = numpy.fft.ifft(znoisypowerlaw)*length   # Inverse discrete Fourier transform
		       			         # \(should consist ONLY of real numbers)

	longlightcurve = inversefourier.real             # take real part of the transform

	# chop the light curve to the desired length, defined by 'length'

	lightcurve = numpy.take(longlightcurve,range(longlength/2,length+longlength/2))

	# ---------- Normalise output lightcurve ---------------------------------------------
	#  (To the desired mean and standard deviation, given by sdCR and meanCR)

	normlightcurve = numpy.zeros(length-1)  
                                      
	for i in range(length-1):                                       

		normlightcurve[i] = ( ( lightcurve[i]-numpy.mean(lightcurve) )
		                    /numpy.std(lightcurve) )  *sdCR+meanCR     

	return frequency, powerlaw, real, imag, positive, negative, znoisypowerlaw, longlightcurve, lightcurve, normlightcurve


low  = 2.40
high = 1.00 
brk  = 5.14e-5
seed = 1

frequency, powerlaw, real, imag, positive, negative, znoisypowerlaw, longlightcurve, lightcurve, normlightcurve = lcsim(low,high,brk,seed)

nfreq = numpy.append(-frequency[::-1],frequency[1::])

# create comparison spectrum array
#powerlaw = numpy.piecewise(nfreq,  [nfreq<=breakfreq, nfreq>breakfreq], 
 #       	   [lambda nfreq: (nfreq/breakfreq)**(-psdindexlow) , 		
  #      	    lambda nfreq: (nfreq/breakfreq)**(-psdindexhigh) ])

#logpl    = []

#for plog in range(len(powerlaw)):

#	logpl.append((log10(powerlaw[plog])))


lfrequency = log10(frequency[-256::])
print frequency
#lpowerlaw  = log10(powerlaw[-256::])
#lpl        = log10(pl)

#subplot(1,2,1)
#plot(lfrequency, lpowerlaw)
#plot(lfrequency,lpl)
#plot(frequency, real)
#plot(frequency, imag)

#subplot(1,2,2)
#plot(dfreq, znoisypowerlaw)


show()


