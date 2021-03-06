#=====================================================================
# Discrete cross-correlation programme
#=====================================================================


# modules
from numpy import zeros, sqrt
from pylab import *

#==================== Input Variables ==========================================

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365"
radioroute = "/uvot/"
xrayroute  = "/uvot/"
outroute   = "/uvot/"

# file names
radiofname  = "V.dat"
xrayfname   = "XS.dat"
outfname    = "xcor.dat"

#===============================================================================

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
i=0
start = 0

# create file routes
radiolocation = route+radioroute+radiofname
xraylocation = route+xrayroute+xrayfname
outlocation = route+outroute+outfname

# read data into 2-D arrays

radioin= open(radiolocation, 'r')

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

	tlag  = []
	ccx   = []
	ccxe  = []
	lag   = []
	filled= []
	vfilled= []

	# find averages
	rav  = sum(r)/len(r)
	xav  = sum(x)/len(x)
	reav = sum(re)/len(re)
	xeav = sum(xe)/len(xe)

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

				# calculate related error

				ccxe.append( sqrt( ( (re[f]-reav)**2)*\
						( (xe[e]-xeav)**2) ) / (rsd*xsd) )


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

	# bin data

	for bt in range(len(lag)):


		bin       = int( (lag[bt] - tmin - 1) / wbin )
		ccf[bin]  = ccf[bin]  + ccx[bt]
		ccfe[bin] = ccfe[bin] + ccxe[bt]
		ccfn[bin] = ccfn[bin] + 1
	
	# set empty bin counts to 1, to avoid "nan", calculate normalising value

	for empty in range(len(ccfn)):

		if ccfn[empty] == 0:
			ccfn[empty] = 1

		if ccf[empty] !=0:
			filled.append(ccf[empty]*ccfn[empty])
			
	average = sum(filled)/(len(filled))

	# average bins

	ccf   = ccf  /average
	ccfe  = ccfe /average
	ccfnn = ccfn /average

	# create time array corresponding to bins

	for tl in range(nbins):
		tlag.append(tmin + tl*wbin + 1)

		
	return ccf,ccfe, tlag

# run xcor function on data
xc, xce, tl =xcor(rflux,rfluxerr,rtime,xflux,xfluxerr,xtime,-500, 200, 100)

# write to file
outfile= open(outlocation, 'w')

outfile.write("READ serr 2 \n") # qdp error header

for o in range(len(xc)):		# data!
	outfile.write(str(tl[o]))
	outfile.write("     ")
	outfile.write(str(xc[o]))
	outfile.write("     ")
	outfile.write(str(xce[o]))
	outfile.write("\n")


outfile.close()

outfile.close()

plot(tl,xc)
axis([-155, 150, -0.7, 1])

show()

