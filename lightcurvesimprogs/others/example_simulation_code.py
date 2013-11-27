#Example of Python program written by Dimitrios Emmanoulopoulos for the production of artificial light curves with a given underlying PSD function.
#The code is produced based on Timmer&Koenig: On generating power law noise (Astron.Astrophys. 300, 707-710 (1995)).
#This code is intended for training purposes only and may contain errors.  

####################################### Load the packages ##############################################################################
import numpy as np
import numpy.random as ra
import scipy.fftpack as scfft
from pylab import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
####################################### INPUT PARAMETERS ##############################################################################
ld=2048                     #length of the final light curve (it is good to be power of 2)
lds=ld*10                   #length of the initial long-light curve (from which we are going to select a part of length ld)
psdindexLow=0.00            #PSD low-frequency index
psdindexHigh=2.00           #PSD high-frequency index 
brkfreq=0.10                #PSD break frequency
meanCR=15.00                #mean count rate of the light curve (if needed)
sdvCR=2.00                  #standard deviation of the light curve (if needed)
randomSeed=234              #random seed for the simulations  (change it if you wish to produce different light curves with the same PSD


                             ################################################################################
                             #################  Timmer and Koenig A&A 300, 707-710 (1995)  ##################
                             ################################################################################

freq = np.arange(1.0, lds/2+1, 1.0)/lds                     #define the frequency grid for the initial light curve (up to the Nyquist frequency)
pl=np.piecewise(freq, [brkfreq>=freq, freq>=brkfreq],
                [lambda freq: np.power(freq,-psdindexLow),
                 lambda freq:np.power(brkfreq,(psdindexHigh-psdindexLow))*
                np.power(freq,-psdindexHigh)])              #define the power-law form of the PSD 
np.random.seed(32+randomSeed)                               ###
ran1=ra.normal(0,1,(1,lds/2))                               ###
np.random.seed(891+randomSeed)                              ###
ran2=ra.normal(0,1,(1,lds/2))                               #two Gaussian distributed random numbers
re=np.multiply(np.sqrt(np.multiply(pl,0.5)),np.reshape(ran1,lds/2))  
im=np.multiply(np.sqrt(np.multiply(pl,0.5)),np.reshape(ran2,lds/2))
reimpos=np.zeros(lds/2,complex)                             ###
for i in range(lds/2):                                      ###
  reimpos[i]=complex(re[i],im[i])                           ###
reimneg=np.zeros(lds/2,complex)                             ###
for i in range(lds/2):                                      ###
  reimneg[i]=reimpos[i].conjugate()                         ###
negreimneg=reimneg[::-1]                                    ###
reim=np.append(reimpos[0:lds/2-1],negreimneg[1:lds/2+1])    ###
reimzero=np.insert(reim,0,complex(0.0,0.0))                 #list of complex numbers with real and imaginary part with zero in the zero frequency
ifourtrans=np.fft.ifft(reimzero)                            #inverse discrete Fourier transform of the list (should consist ONLY from real numbers)
lc=ifourtrans.real                                          #drop the zeros from the imaginary part
lcfin=np.take(lc,range(lds/2,ld+lds/2))                     #chop the light curve to the desired length defined by ld

modlc=np.zeros(ld-1)                                        ###
for i in range(ld-1):                                       ###
 modlc[i]=((lc[i]-np.mean(lc))/np.std(lc))*sdvCR+meanCR     ### Normalised light curve to the desired mean and standard deviation

#Plot the results
plot(modlc)
aspect=90
axis([0.0, ld, 0.95*amin(modlc), 1.1*amax(modlc)])
xlabel('Time')
ylabel('Flux')
show()



