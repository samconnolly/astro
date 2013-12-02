# Creates a power spectrum from a lightcurve
# by Sam Connolly (currently just converted from multpowg to a point, that'll change though...
# Does not take into account sampling patterns (on purpose!)

# modules
import pylab as pl
from numpy import *

# Parameters 

bsize    = 0.1              # bin width
bfac     = 1.3              # bin factor...?
minb     = 4                # minimum number of bins

# filenames
infname      = "5548_ami_r.qdp" # lightcurve filename
outfname     = "prebin.dat"           # output power spectrum file name

#   File route
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"
inroute    = "/ami/refined/"
outroute   = "/powerspecprogs/"

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
	if start == 1:
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
      
def powcal(bsize, df, time, flux, npoints, avflux):

	ff=[]
	nhi=int(0.5/(bsize*df))

	fr=zeros(nhi)
	fi=zeros(nhi)
      
	for k in range(nhi):
	      		
		a=2*pi*(k+1)*df

		for m in range(npoints):
        
			c=cos(a*time[m])
			s=sin(a*time[m])
			fr[k]+=((flux[m]-avflux)*c)
			fi[k]+=((flux[m]-avflux)*s)
        
		ff.append( ((nhi*df)**(-1)) * (fr[k]**2+fi[k]**2)/float(npoints) )
        	 
	return ff, nhi
# ---------------------------------------------------------------

# calculate power spectrum

ff, nhi = powcal(bsize, df, time, flux, npoints, avflux)

# normalise power spectrum, create frequency array

for j in range(nhi):
		
	dff.append(ff[j]/avflux**2)
	freq.append(df*j)
 
# sort the resulting array of power spectra 

#sort2(nhi,freq,dff)

# -- Binning function ----------------------------------------
      
def binps(nhi,freq,dff,minb,bfac):

	jj=0
	j1=0
	logftot=0.0
	ffav=0.0
	flast=bfac*freq[1]
	fprev=freq[1]  
	
	bff   = []
	bfreq = []
        bperr = []
        
	for i1 in range(nhi-1):
	
		ffav=ffav+log10(dff[i1])+0.253
		j1=j1+1
		logftot=logftot+log10(freq[i1])
		
		if ( freq[i1+1] > flast or i1 == nhi) and ( j1 >= minb):
		
			jj=jj+1
			bff.append( ffav/float(j1) )
			bfreq.append( logftot/float(j1) )
			bperr.append(0.0)
			
			for k1 in range(i1-(j1-1),i1):
			
				bperr[-1]=bperr[-1]+(log10(dff[k1])+0.253-bff[-1])**2
			
			bperr[-1]=sqrt(bperr[-1]/(j1*float(j1-1)))

			fprev=freq[i1]
			flast=bfac*freq[i1]
			logftot=0.0
			ffav=0.0
			j1=0  

	nbfreq=jj
        
	return bfreq, bff, bperr       

# -------------------------------------------------------------------     
      
#  bin the sorted array

bfreq, bff, bperr = binps(nhi,freq,dff,minb,bfac)
      
# ----- write to file -------------------------------------

f = range(len(ff))

outfile= open(outlocation, 'w')

for o in range(len(ff)):		# data!

	outfile.write(str(f[o]))
	outfile.write("    ")
	outfile.write(str(ff[o]))
	outfile.write("\n")

outfile.close() 

      
#  Print average count rate of lightcurve used to make PS

print "Average count rate = ", avflux


# plot power spectrum
pl.errorbar(bfreq,bff,bperr)
pl.axis([-2.4, 0.8, -2.6, -0.5])

#pl.show()











