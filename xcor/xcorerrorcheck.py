"""
xcorerrorcheck.py

Sam Connolly, some time in 2012...

#=====================================================================
# Programme plotting spectra against one another and finding the 
# gradient and scatter of a straight line fit in order to find errors
#=====================================================================

"""

# modules
from numpy import zeros, tan, sqrt

#===================== INPUT PARAMETERS ========================================

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"
radioroute = "/amidat/refined/"
xrayroute  = "/xte+swiftdat/"
outroute   = "/xcordat/errors/"

# file names
radiofname  = "5548_ami_r.qdp"
xrayfname   = "5548_xte_swift_r.qdp"
outfname    = "xcor5548errors.qdp"

# variables
t_start = -150
t_end   =  150

#===============================================================================

trange = t_end-t_start

# data arrays
tlag       = []
radio      = []
rtime      = []
rflux      = []
rfluxerr   = []
xray       = []
xtime      = []
xflux      = []
xfluxerr   = []
xfluxshort = []
xtimeshort = []
iprflux    = [[] for rows in range(trange)]
fitgrads   = [[] for rows in range(trange)]
sqmins     = [[] for rows in range(trange)]
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

# ---- create lagged interpolated radio flux arrays ----------------------------

flag  = 0
flag2 = 0

for lag in range(t_start,t_end):

	for time in range(len(xtime)):
			
	
		# check for values outside the time range
		# of the radio data

		if (xtime[time] + lag) < rtime[-1] \
		and  (xtime[time] + lag) > rtime[1]:

			flag2 = 1

			# find two closest radio times to the xray time 

			postdif= ( xtime[time] + lag ) - rtime[ 1] 
			negtdif= ( xtime[time] + lag ) - rtime[-1] 
			low  = 0
			high = 0

			for f in range(len(rtime)):
	
				dif= (xtime[time] + lag) - rtime[f]

				if dif >= 0:
					if dif <= postdif:
						low = f
						postdif=rtime[f]

				if dif < 0:

					if dif >= negtdif:
						high = f
						negtdif=rtime[f]

			# interpolate single value

			intval= rflux[low] + ( (rflux[high] - rflux[low]) \
				/ (rtime[high] - rtime[low]))*((xtime[time] \
				+ lag) - rtime[low])

			# add to radio array equivalent to x-ray times
			
			iprflux[lag+150].append(intval)

			if flag == 0:
			
				xfluxshort.append(xflux[time])
				xtimeshort.append(xtime[time])
	if flag2 == 1:
		flag = 1


# ---- fitting ---------------------------------------------------------

for lags in range(trange):
	
	# --- standard deviation -------------
	
	iprav = sum(iprflux[lags]) / len(iprflux[lags])
	
	sd       = []

	for h in range(len(iprflux[lags])):

		sd.append((iprflux[lags][h]-iprav)**2)

	iprsd  = sqrt( sum(sd) / len(iprflux[lags]) )
	
	# ---- find best gradient ----------
	
	fitgrad    = []
	lsquare    = []
	
	for grad in range(200,700):
	
		sqdif = 0	

		for value in range(len(xfluxshort)):
		
			predicted    = (tan(grad/10)) * xfluxshort[value]
			sqdif += ((iprflux[lags][value] - predicted)**2)/iprsd

		lsquare.append(sqdif)
		fitgrad.append(tan(grad/10))
		
	smin = lsquare[1]
	
	for square in range(len(lsquare)):
	
		if lsquare[square] < smin:
			
			smin = lsquare[square]
			gmin = fitgrad[square]

	fitgrads[lags] = gmin*400
	sqmins[lags]   = smin
	
# create time array corresponding to lags

for tl in range(t_start, t_end):
	tlag.append(tl)


# write to file

outfile= open(outlocation, 'w')

for o in range(len(tlag)):		# data!
	outfile.write(str(tlag[o]))
	outfile.write("     ")
	outfile.write(str(fitgrads[o]))
	outfile.write("     ")
	outfile.write(str(sqmins[o]))
	outfile.write("\n")


outfile.close()
