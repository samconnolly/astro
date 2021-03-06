"""
multisimfinal.py

Created in November  2012

Author: Sam Connolly


#=====================================================================
# interpolating cross-correlation programme
#=====================================================================

cross-correlate two signals, using interpolation.

"""

# modules
import numpy as np
import pylab as plt

#================================================================================

##   File routes
#route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"
#radioroute = "/amidat/refined/"
#xrayroute  = "/xte+swiftdat/"
#outroute   = "/xcordat/"
#
## file names
#radiofname  = "5548_ami_r.qdp"
#xrayfname   = "5548_xte_swift_r.qdp"
#outfname    = "xcor5548.ami.xte+xrt.qdp"

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc1365"  # general path
radioroute = "/uvot/fix/"											# radio path
xrayroute  = "/uvot/fix/"											# xray path
outroute   = "/uvot/fix/"											# output path

# file names
radiofname  = "V.dat"		# radio data filename
xrayfname   = "U.dat" #"XCounts.dat"		# xray data filename
outfname    = "xcor.dat"	# output data filename

t_range     = 200 			# time range to correlate over

save 	   = False		# save?
plot 	   = True			# plot?

#================================================================================

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

# interpolating cross-correlation function, requiring values for the start and end of a time lag range and arrays of time, flux and flux error, creating an array of correlation values and array of corresponding time lag values

#----------------------------------------------------------------------

def xcor(r,rt,x,xt,t_start,t_end):

	# function arrays
	ccf      = []
	tlag     = []
	npoints	= []

	# averages
	rav  = np.mean(r)
	xav  = np.mean(x)

	# standard deviations

	rsd  = np.std(r)
	xsd  = np.std(x)

	#-----calculate cross correlation function-------------


	for t in range(t_start, t_end):

		ccx   = 0.
		n     = 0.

		for e in range(len(xt)):

			# check for values outside the time range of the radio data
			if (xt[e] + t) < rt[-1] and  (xt[e] + t) > rt[1]:

				# find two closest radio times to the xray time 

				postdif= ( xt[e] + t ) - rt[ 1] 
				negtdif= ( xt[e] + t ) - rt[-1] 
				low  = 0
				high = 0

				for f in range(len(rt)):
	
					dif= (xt[e] + t) - rt[f]

					if dif >= 0:
						if dif <= postdif:
							low = f
							postdif=rt[f]

					if dif < 0:

						if dif >= negtdif:
							high = f
							negtdif=rt[f]

	
				# interpolate single value

				intval= r[low] + ( (r[high] - r[low]) \
					/ (rt[high] - rt[low]))*((xt[e] + t) - rt[low])


				# calculate correlation value

				ccx += ( (intval-rav)*(x[e]-xav) ) / (rsd*xsd) 
	
				# counts points used
				n += 1.
	

		# append final arrays with normalised correlation values
		if ccx!= 0:
			ccf.append(ccx/n)
			npoints.append(n)
			tlag.append(t)
		
	return ccf,tlag, npoints


# run xcor function on data
xc, tl, npoints =xcor(rflux,rtime,xflux,xtime, -t_range, t_range)

# write to file
	
if save:	
	outfile= open(outlocation, 'w')
	
	outfile.write("READ serr 2 \n") # qdp error header
	
	for o in range(len(xc)):		# data!
		outfile.write(str(tl[o]))
		outfile.write("     ")
		outfile.write(str(xc[o]))
		outfile.write("\n")
	
	outfile.close()

# plot
if plot:
	
	plt.subplot(2,1,1)
	plt.plot(tl,xc)
	plt.subplot(2,1,2)
	plt.plot(tl,npoints)
	plt.show()
	
	