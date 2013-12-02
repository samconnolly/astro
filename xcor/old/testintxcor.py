#=====================================================================
# Test interpolating cross-correlation programme
#=====================================================================


# modules
from math import sqrt
from numpy import zeros

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08"
radioroute = "/swift-xrt/ngc5548/refined/"
xrayroute  = "/swift-xrt/ngc5548/refined/"
outroute   = "/xcor/"

# file names
radiofname  = "ngc5548_3_0.5-10keV.qdp"
xrayfname   = "ngc5548_3_0.5-10keV.qdp"
outfname    = "test.qdp"

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

def xcor(r,re,rt,x,xe,xt,t_start,t_end):


	# function arrays
	ccf      = []
	ccfe     = []
	tlag     = []



	# find averages
	rav  = sum(r)/len(r)
	xav  = sum(x)/len(x)
	reav = sum(re)/len(re)
	xeav = sum(xe)/len(xe)

	# find standard deviations

	sd       = []

	for h in range(len(r)):

		sd.append((r[h]-rav)**2)

	rsd  = sqrt( sum(sd) / len(r) )



	sd       = []

	for j in range(len(x)):

		sd.append((x[j]-xav)**2)

	xsd  = sqrt( sum(sd) / len(x) )



	#-----calculate cross correlation function-------------


	for t in range(t_start, t_end):

		ccx   = []
		ccxe  = []

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

				ccx.append( ( (intval-rav)*(x[e]-xav) ) / (rsd*xsd) )
	
				# calculate related error

				intvale= re[low] + ((re[high] - re[low]) \
					/ (rt[high] - rt[low]))*((xt[e] + t) - rt[low])

				ccxe.append(  sqrt( ((intvale-reav)**2)*\
						((xe[e]-xeav)**2) ) / (rsd*xsd)  )
		

		# append final arrays with normalised correlation values
		if len(ccx)!= 0:
			ccf.append(sum(ccx)/len(ccx))
			ccfe.append(sum(ccxe)/len(ccxe))
			tlag.append(t)
		
	return ccf,ccfe, tlag

# run xcor function on data
xc, xce, tl =xcor(rflux,rfluxerr,rtime,xflux,xfluxerr,xtime, -500, 500)

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


