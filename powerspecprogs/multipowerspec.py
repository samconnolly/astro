"""
multipowerlaw.py

Created Nov 2012

Author: Sam Connolly

Creates a power spectrum from a lightcurve.
Does not take into account sampling patterns (on purpose!)

Also, it's basically rubbish unless the lightcurve is evenly sampled.

"""

#

# modules
import pylab as pl
from numpy import *


#======================= Input Parameters =======================================

# Parameters 

bsize    = 0.1              # bin width
bfac     = 1.3              # PDS bin factor
minb     = 4                # minimum points per bin

# filenames
#infname      = "5548_ami_r.qdp" # lightcurve filename
#outfname     = "lctest.dat"           # output power spectrum file name
#
##   File route
#route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"
#inroute    = "/amidat/refined/"
#outroute   = "/pythonprogs/powerspecprogs/"

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365"  # general path
inroute = "/uvot/"											
outroute   = "/uvot/"											# output path

# file names
infname   = "XCounts.dat"		# lightcurve filename
outfname  = "lctest.dat"           # output power spectrum file name

header = 0

#================================================================================

# data arrays
time    = []
flux    = []
fluxerr = []

# variables
tstart = -150
tend   =  150
n_bins =  100

# create file routes
inlocation  = route+inroute+infname
outlocation = route+outroute+outfname

# read data into arrays

start = 0
npoints = -1

indat= open(inlocation, 'r')

for y in indat:
	currtime, currflux, currfluxerr = y.split()
	if start >= header:
		time.append(float(currtime))
		flux.append(float(currflux))
		fluxerr.append(float(currfluxerr))	
		npoints  += 1
	start = 1

indat.close()

# ------- make power spectrum ----------------------

# declare arrays & values

dff   = []
freq  = []

# find average flux
avflux     = mean(flux)

# calculate time range and frequency max
dt=time[npoints]-time[0]    
df=1.0*(dt**(-1))

# power spectrum fourier transform function ----------------
      
def powcal(bsize, df, time, flux, avflux):

	ff=[]
	nhi=int(0.5/(bsize*df))
	npoints = len(flux)

	fr=zeros(nhi)
	fi=zeros(nhi)
      
	for k in range(nhi):
	      		
		a=2*pi*(k+1)*df

		for m in range(npoints):
        
			c=cos(a*time[m])
			s=sin(a*time[m])
			fr[k]+=((flux[m]-avflux)*c)
			fi[k]+=((flux[m]-avflux)*s)
        
		ff.append( ( (2.0*bsize)/ ((avflux**2)*(npoints**0.5) ) )*(fr[k]**2+fi[k]**2) )
	 
	return ff, nhi
# ---------------------------------------------------------------

# calculate power spectrum

ff, nhi = powcal(bsize, df, time, flux, avflux)

# normalise power spectrum, create frequency array

for j in range(nhi):
		
	dff.append(ff[j]/avflux**2)
	freq.append(df*(j+1))

freq.append(freq[-1])
 
# sort the resulting array of power spectra 

#sort2(nhi,freq,dff)

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
      
#  bin the sorted array

bfreq, bff, bperr = binps(nhi,freq,dff,minb,bfac)
      


# ----- write to file -------------------------------------

outfile= open(outlocation, 'w')

outfile.write("READ serr 2 \n") # qdp error header

for o in range(len(bff)):		# data!

	outfile.write(str(bfreq[o]))
	outfile.write("     ")
	outfile.write(str(bff[o]))
	outfile.write("     ")
	outfile.write(str(bperr[o]))
	outfile.write("\n")

outfile.close() 

      
#  Print average count rate of lightcurve used to make PS

print "Average count rate = ", avflux


# plot power spectrum
pl.errorbar(bfreq,bff,bperr)
#pl.axis([-2.4, 0.8, -2.6, -0.5])

pl.show()