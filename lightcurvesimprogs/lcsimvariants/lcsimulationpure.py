# ------------------------------------------------------------------------------
# Light curve simulation programme, using the Timmer & Koenig method
# Sam Connolly
# ------------------------------------------------------------------------------

# Import packages

from pylab import *
import numpy as numpy

# define as a programme to allow external importing
# vals e.g. low = 0.00, High =2.00, brk=0.10

def lcsim(low,high,brk,seed,sd,mean,lg):

	# Parameters

	length       =lg             # length of final light curve (ideally a ^2)
	longlength   =length*10      # length of initial light curve (from which we 
			             		 # select a section of length ld)
	psdindexLow  =low            # PSD low-frequency index
	psdindexHigh =high           # PSD high-frequency index 
	breakfreq    =brk            # PSD break frequency
	meanCR       =mean           # mean count rate of light curve (if needed)
	sdCR         =sd             # standard deviation of light curve (if needed)
	randomSeed   =seed           # random seed

	# ================================================================================
	# --------- Main Programme -------------------------------------------------
	# ================================================================================
	
	# --------- Create power spectrum ------------------------------------------------

	# Create frequency array for initial light curve, up to Nyquist frequency
	frequency = numpy.arange(1.0, longlength/2+1, 1.0)/longlength 

	# define the power-law form of the PSD, i.e. a two-part law with a break
	powerlaw = numpy.piecewise(frequency,  [frequency<=breakfreq, frequency>breakfreq], 
        	   [lambda frequency: (frequency/breakfreq)**(-psdindexLow) , 		
        	    lambda frequency: (frequency/breakfreq)**(-psdindexHigh) ])

	# --- Create two arrays of gaussian random numbers for each frequency

	np.random.seed(32+randomSeed)                               
	random1 = numpy.random.normal(0,1,(longlength/2))
	np.random.seed(891+randomSeed) 
	random2 = numpy.random.normal(0,1,(longlength/2))

	# -------- Add noise to the power law (PL) using the random numbers --------
	# (Multiply random numbers by the sqrt of half the PL value at each freq)

	real = (numpy.sqrt(powerlaw*0.5))*random1
	imag = (numpy.sqrt(powerlaw*0.5))*random2

	# ----- create array of Fourier components ---------------------------------
	# (+ve values use arrays above, -ve values are conjugates of +ves each freq)

	positive = numpy.zeros(longlength/2,complex) # complex array for +ve values
	negative = numpy.zeros(longlength/2,complex) # complex array for -ve values
                             
	for i in range(longlength/2):                                    

 		positive[i]=complex(real[i],imag[i]) # read real & imag into +ve array
		negative[i]=positive[i].conjugate()  # read conjugates into -ve array 
 	                         
	revnegative = negative[::-1]       	     # reverse negative array

	# join negative and positive arrays
                             
	noisypowerlaw = numpy.append(positive[0:longlength/2-1],revnegative[1:longlength/2+1])
	znoisypowerlaw = numpy.insert(noisypowerlaw,0,complex(0.0,0.0)) # add a zero

	# --------- Fourier transform the noisy power law --------------------------

	inversefourier = numpy.fft.ifft(znoisypowerlaw)*length # Inverse discrete 															   # Fourier transform
		   								# \(should consist ONLY of real numbers)

	longlightcurve = inversefourier.real       # take real part of the transform

	# chop the light curve to the desired length, defined by 'length'

	lightcurve = numpy.take(longlightcurve,\
					range(longlength/2,length+longlength/2))

	# ---------- Normalise output lightcurve -----------------------------------
	#  (To the desired mean and standard deviation, given by sdCR and meanCR)

	normlightcurve = numpy.zeros(length-1)  
                                      
	for i in range(length-1):                                       

		normlightcurve[i] = ( ( lightcurve[i]-numpy.mean(lightcurve) )
                   /numpy.std(lightcurve) )  *(sqrt(sdCR*(meanCR**2))) +meanCR     

	return normlightcurve







