# ------------------------------------------------------------------------------
# Light curve simulation programme, using the Timmer & Koenig method
# Sam Connolly
# ------------------------------------------------------------------------------

# Import packages

from pylab import *
import numpy as numpy

# define as a programme to allow external importing
# vals e.g. low = 0.00, High =2.00, brk=0.10

def lcsim(low,high,brk,seed):

	# Parameters

	length       =1024           # length of final light curve (ideally 2^x)
	longlength   =length*10      # length of initial light curve (from which 
			             # we select a section of length ld)
	psdindexLow  =low            # PSD low-frequency index
	psdindexHigh =high           # PSD high-frequency index 
	breakfreq    =brk            # PSD break frequency
	meanCR       =3.27           # mean cnt rate of light curve (if needed)
	sdCR         =0.80           # standard dev of light curve (if needed)
	randomSeed   =seed           # random seed

	# ======================================================================
	# --------- Main Programme ---------------------------------------------
	# ======================================================================
	
	# --------- Create power spectrum --------------------------------------

	# Create frequency array for initial light curve, up to the Nyquist freq
	frequency = numpy.arange(1.0, longlength/2+1, 1.0)/longlength 

	# define the power-law form of the PSD, i.e. a two-part law with a break
	powerlaw = numpy.piecewise(
		   frequency,  [breakfreq>=frequency, frequency>=breakfreq], 
            [lambda frequency: numpy.power(frequency,(-psdindexLow)), 		
       	     lambda frequency: numpy.power(breakfreq,(psdindexHigh-psdindexLow))
                             *numpy.power(frequency,(-psdindexHigh))])

	# -------- Create two arrays of gaussian-dist numbers for each freq

	np.random.seed(32+randomSeed)                               
	random1 = numpy.random.normal(0,1,(longlength/2))
	np.random.seed(891+randomSeed) 
	random2 = numpy.random.normal(0,1,(longlength/2))

	# -------- Add noise to the power law (PL) using the random numbers ----
	# (Multiply random no.s by the sqrt of half the PL value at each freq)

	real = (numpy.sqrt(powerlaw*0.5))*random1
	imag = (numpy.sqrt(powerlaw*0.5))*random2

	# ----- create array of Fourier components -----------------------------
	# (+ve values use arrays above, -ve values are conjugates of +ve ones)

	positive = numpy.zeros(longlength/2,complex)  # complex array +ve values
	negative = numpy.zeros(longlength/2,complex)  # complex array -ve values
                             
	for i in range(longlength/2):                                    

 		positive[i]=complex(real[i],imag[i]) # put values into +ve array
		negative[i]=positive[i].conjugate()  # put conjugates into -ve  
 	                         
	revnegative = negative[::-1]       	     # reverse negative array

	# join negative and positive arrays
                             
	noisypowerlaw = numpy.append(
		positive[0:longlength/2-1],revnegative[1:longlength/2+1])
	znoisypowerlaw = numpy.insert(noisypowerlaw,0,complex(0.0,0.0)) # add 0

	# --------- Fourier transform the noisy power law ----------------------

	inversefourier = numpy.fft.ifft(znoisypowerlaw)   
		       		# \(should consist ONLY of real numbers)

	longlightcurve = inversefourier.real  # take real part of the transform

	# chop the light curve to the desired length, defined by 'length'

	lightcurve = numpy.take(longlightcurve,
					range(longlength/2,length+longlength/2))

	# ---------- Normalise output lightcurve -------------------------------
	#  (To desired mean and standard deviation, given by sdCR and meanCR)

	normlightcurve = numpy.zeros(length-1)  
                                      
	for i in range(length-1):                                       

		normlightcurve[i] = ((longlightcurve[i]
	  -numpy.mean(longlightcurve))/numpy.std(longlightcurve) )  *sdCR+meanCR     

	return normlightcurve







