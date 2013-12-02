# ------------------------------------------------------------------------------
# Light curve simulation programme, using the Timmer & Koenig method
# Including a real light curve input for comparison to data
# Sam Connolly
# ------------------------------------------------------------------------------

# Import packages

from pylab import *
import numpy as numpy

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"
xrayroute  = "/xte+swift/"

# file names
xrayfname   = "5548_xte_swift_r.qdp"

# data arrays
xray     = []
xtime    = []
xflux    = []

# variables
tstart  = -150
tend    =  150
n_bins  =  100
ncurves =  1
psdindexlow  = 1.00
psdindexhigh = 2.40 
psdbrkfreq   = 5.12e-5

# create file routes
xraylocation = route+xrayroute+xrayfname

# read data into 2-D arrays

start = 0

xrayin= open(xraylocation, 'r')

for y in xrayin:
	currtime, currflux,currfluxerr = y.split()
	if start == 1:
		xtime.append(float(currtime))
		xflux.append(float(currflux))
		
	start = 1

xrayin.close()

# define as a programme to allow external importing
# vals e.g. low = 0.00, High =2.00, brk=0.10

def lcsim(low,high,brk,seed):

	# Parameters

	length       =2048           # length of final light curve (ideally a power of 2)
	longlength   =length*10      # length of initial light curve (from which we 
			             # select a section of length ld)
	psdindexLow  =high            # PSD low-frequency index
	psdindexHigh =low           # PSD high-frequency index 
	breakfreq    =brk            # PSD break frequency
	meanCR       =3.27          # mean count rate of the light curve (if needed)
	sdCR         =0.80           # standard deviation of the light curve (if needed)
	randomSeed   =seed            # random seed

	# ================================================================================
	# --------- Main Programme -------------------------------------------------------
	# ================================================================================
	
	# --------- Create power spectrum ------------------------------------------------

	# Create frequency array for the initial light curve, up to the Nyquist frequency
	frequency = numpy.arange(1.0, longlength/2+1, 1.0)/longlength 

	# define the power-law form of the PSD, i.e. a two-part law with a break
	powerlaw = numpy.piecewise(frequency,  [breakfreq>=frequency, frequency>=breakfreq], 
        	   [lambda frequency: numpy.power(frequency,(-psdindexLow)), 		
        	    lambda frequency: numpy.power(breakfreq,(psdindexHigh-psdindexLow))
                             *numpy.power(frequency,(-psdindexHigh))])

	# -------- Create two arrays of gaussian-distributed random numbers for each frequency

	np.random.seed(32+randomSeed)                               
	random1 = numpy.random.normal(0,1,(longlength/2))
	np.random.seed(891+randomSeed) 
	random2 = numpy.random.normal(0,1,(longlength/2))

	# -------- Add noise to the power law (PL) using the random numbers ---------------
	# (Multiply random numbers by the square route of half the PL value at each freq)

	real = (numpy.sqrt(powerlaw*0.5))*random1
	imag = (numpy.sqrt(powerlaw*0.5))*random2

	# ----- create array of Fourier components ---------------------------------------------------
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

	inversefourier = numpy.fft.ifft(znoisypowerlaw)   # Inverse discrete Fourier transform
		       			         # \(should consist ONLY of real numbers)

	longlightcurve = inversefourier.real             # take real part of the transform

	# chop the light curve to the desired length, defined by 'length'

	lightcurve = numpy.take(longlightcurve,range(longlength/2,length+longlength/2))

	# ---------- Normalise output lightcurve ---------------------------------------------
	#  (To the desired mean and standard deviation, given by sdCR and meanCR)

	normlightcurve = numpy.zeros(length-1)  
                                      
	for i in range(length-1):                                       

		normlightcurve[i] = ( ( longlightcurve[i]-numpy.mean(longlightcurve) )
		                    /numpy.std(longlightcurve) )  *sdCR+meanCR     

	return normlightcurve


simtime = [[] for q in range(2)]

# create array of positions of discrete times below each xray time and the time difference
 
for n in xtime:
	simtime[0].append( int(n) - xtime[0] )
	simtime[1].append( n - int(n) )	

# --- simulate and create array of cross correlation functions of simulated ligth curves ------------

simarray = [[] for h in range(n_bins)]

lc1 = lcsim(psdindexlow, psdindexhigh, psdbrkfreq,1)

# interpolate values with data sampling pattern

lc1samp = []
	
for val in range(len(simtime[0])):
	
	intval= lc1[int(simtime[0][val])] + ( lc1[int(simtime[0][val]+1)]-lc1[int(simtime[0][val])] ) * ( simtime[1][val] )
	lc1samp.append(intval)

lc2 = lcsim(psdindexlow, psdindexhigh, psdbrkfreq,2)

# interpolate values with data sampling pattern

lc2samp = []
	
for val in range(len(simtime[0])):
	
	intval= lc2[int(simtime[0][val])] + ( lc2[int(simtime[0][val]+1)]-lc2[int(simtime[0][val])] ) * ( simtime[1][val] )
	lc2samp.append(intval)
	
lc3 = lcsim(psdindexlow, psdindexhigh, psdbrkfreq,3)

# interpolate values with data sampling pattern

lc3samp = []
	
for val in range(len(simtime[0])):
	
	intval= lc3[int(simtime[0][val])] + ( lc3[int(simtime[0][val]+1)]-lc3[int(simtime[0][val])] ) * ( simtime[1][val] )
	lc3samp.append(intval)
	
subplot(2,2,1)
plot(xtime,xflux)

subplot(2,2,2)
plot(xtime,lc1samp)

subplot(2,2,3)
plot(xtime,lc2samp)

subplot(2,2,4)
plot(xtime,lc3samp)

show()




