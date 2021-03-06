#=====================================================================
# Callable Discrete cross-correlation function
#=====================================================================


# modules
from numpy import zeros, sqrt
from pylab import *
#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"
radioroute = "/ami/refined/"
xrayroute  = "/xte+swift/"
outroute   = "/xcor/"

# file names
radiofname  = "5548_ami_r.qdp"
xrayfname   = "5548_xte_swift_r.qdp"
outfname    = "dxcor5548.ami.xte+xrt.qdp"


# data arrays
radio    = []
rtime    = []
rflux    = []
rfluxerr = []
xray     = []
xtime    = []
xflux    = []
xfluxerr = []


# variables
tstart = -150
tend   =  150
n_bins =  100

# create file routes
radiolocation = route+radioroute+radiofname
xraylocation = route+xrayroute+xrayfname
outlocation = route+outroute+outfname

# read data into 2-D arrays

radioin= open(radiolocation, 'r')

start = 0

for x in radioin:
	
	currtime, currflux,currfluxerr = x.split()
	if start == 1:
		rtime.append(float(currtime))
		rflux.append(float(currflux))
		rfluxerr.append(float(currfluxerr))	
	start = 1

radioin.close()

start = 0

xrayin= open(xraylocation, 'r')

for y in xrayin:
	currtime, currflux,currfluxerr = y.split()
	if start == 1:
		xtime.append(float(currtime))
		xflux.append(float(currflux))
		xfluxerr.append(float(currfluxerr))	
	start = 1

xrayin.close()

#-----------------------------------------------------------------------

# discreet cross-correlation function, requiring values for the start and end of a time lag range and arrays of time, flux and flux error, creating an array of correlation values and array of corresponding time lag values

#----------------------------------------------------------------------

def xcor(r,re,rt,x,xe,xt,t_start,t_end,nbins):


	# function arrays

	tlag    = []
	ccx     = []
	lag     = []

	# find averages
	rav  = sum(r)/len(r)
	xav  = sum(x)/len(x)

	# find standard deviations

	sd = []

	for h in range(len(r)):

		sd.append((r[h]-rav)**2)

	rsd  = sqrt( sum(sd) / len(r) )


	sd = []

	for j in range(len(x)):

		sd.append((x[j]-xav)**2)

	xsd  = sqrt( sum(sd) / len(x) )


	#-----calculate cross correlation function-------------


	for e in range(len(x)):
		
		for f in range(len(r)):

			# check for values outside the time range of the radio data
			if (rt[f]-xt[e]) < t_end and  (rt[f]-xt[e]) >= t_start:

				# calculate correlation value and equivalent lag

				ccx.append( ( (r[f]-rav)*(x[e]-xav) ) / (rsd*xsd) )
				lag.append( rt[f]-xt[e] )


	# ----- bin data in time -----------------

	# find time range, divide into bins

	tmin=lag[1]
	tmax=lag[1]

	for time in lag:
		if time <= tmin:
			tmin = time
		if time >= tmax:
			tmax = time

	trange = tmax - tmin
	wbin   = trange / nbins 
	print "bin width:", wbin

	ccf    = zeros(nbins)
	ccfe   = zeros(nbins)
	ccfn   = zeros(nbins)

	# bin data, create bin array

	binarray  = [[]for i in range(nbins)]

	for bt in range(len(lag)):


		bin       = int( (lag[bt] - tmin - 1) / wbin )
		ccf[bin]  = ccf[bin]  + ccx[bt]
		ccfn[bin] = ccfn[bin] + 1
		binarray[bin].append(ccx[bt])

	# set empty bin counts to 1, to avoid "nan", calculate normalising value

	for empty in range(len(ccfn)):

		if ccfn[empty] == 0:
			ccfn[empty] = 1

	# calculate errors from bin SDs


	binsd   = zeros(nbins)

	for bins in range(nbins):

		sdtotal = 0

		total = sum(binarray[bins])
		bav = total / ccfn[bins]

		for bvalue2 in range(int(ccfn[bins])):

			sdtotal += (binarray[bins][bvalue2] - bav)**2

		binsd[bins] = sqrt(sdtotal / ccfn[bins])

	# average bins

	for count in range(len(ccfn)):
		ccf[count]   = ccf[count]   / ccfn[count]
		binsd[count] = binsd[count] / ccfn[count]

	# create time array corresponding to bins

	for tl in range(nbins):
		tlag.append(tmin + tl*wbin -2)

		
	return ccf, binsd, tlag

# ----- run xcor function on data -------------------------

xc, xe, tl =xcor(rflux,rfluxerr,rtime,xflux,xfluxerr,xtime,tstart,tend,n_bins)

# ----- write to file -------------------------------------

outfile= open(outlocation, 'w')

outfile.write("READ serr 2 \n") # qdp error header

for o in range(len(xc)):		# data!
	outfile.write(str(tl[o]))
	outfile.write("     ")
	outfile.write(str(xc[o]))
	outfile.write("     ")
	outfile.write(str(xe[o]))
	outfile.write("\n")


outfile.close()

plot(tl,xc)
axis([-155, 150, -0.7, 1])

show()

