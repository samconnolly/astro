"""
multisimpeak.py

Sam Connolly, early 2013

#=====================================================================
# Cross correlation and confidence-simulation code, using peak values 
#=====================================================================

cross-correlate two signals, simulate lightcurves, create confidence curves.
Currently just takes the known parameters for the lightcurve simulation.
The notation assumes you're cross-correlatiing radio and x-ray data, but it
makes no difference of course. The 'X-ray' data set is simulated. Incorporates
errors. Incorporates errors, calculates stats binwise to account for trends in
lightcurves. Uses peak values instead of other shit... not as good, can't 
remember why.
"""

# Import packages

from lcsimulation import lcsim
from callxcor     import xcor
from pylab import *
import numpy as numpy

#   File routes
route      = "/disks/raid/raid1/xray/raid/sdc1g08/NetData"
radioroute = "/ami/refined/"
xrayroute  = "/xte+swift/"
outroute   = "/xcor/"

# file names
radiofname  = "5548_ami_r.qdp"
xrayfname   = "5548_xte_swift_r.qdp"
outfname    = "xcor5548.ami.xte+xrt.qdp"

# data arrays
rtime    = []
rflux    = []
xtime    = []
xflux    = []



# variables
tstart  = -150
tend    =  150
n_bins  =  100
ncurves =  10000
psdindexlow  = 2.40
psdindexhigh = 1.00 
psdbrkfreq   = 5.14e-5
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
	
	start = 1

radioin.close()

start = 0

xrayin= open(xraylocation, 'r')

for y in xrayin:
	currtime, currflux,currfluxerr = y.split()
	if start == 1:
		xtime.append(float(currtime))
		xflux.append(float(currflux))
		
	start = 1

xrayin.close()

# run xcor function on data
xc, xce, tl = xcor(rflux, rtime, xflux, xtime, tstart, tend, n_bins)

simtime = [[] for q in range(2)]

# create array of positions of discrete times 
# below each xray time and the time difference
 
for n in xtime:
	simtime[0].append( int(n) - xtime[0] )
	simtime[1].append( n - int(n) )	

# --- simulate and create array of xcor fns of simulated light curves ----------

simarray = [[] for h in range(n_bins)]
first = 1

for curve in range(ncurves):

	# -- simulate curves, applying the sampling pattern of the data curve --

	lc  = lcsim(psdindexlow, psdindexhigh, psdbrkfreq,curve)# simulate curve
	
	# interpolate values with data sampling pattern

	lcsamp = []
	
	for val in range(len(simtime[0])):
	
		intval= lc[int(simtime[0][val])] + ( lc[int(simtime[0][val]+1)]\
			-lc[int(simtime[0][val])] ) * ( simtime[1][val] )
		lcsamp.append(intval)
	
	# -- cross correlate with second data curve and add to sorted data array 
	
	sxc, sxce, stl = xcor(rflux, rtime, lcsamp, xtime, tstart, tend, n_bins)
	
	# find the peak 
	
	peak = 0
	
	for pk in range(len(sxc)):
	
		if sxc[pk] > peak:
			
			peak  = sxc[pk]
			pkpos = pk
			
	# sort into array
	
	if len(simarray[pkpos]) == 0:
		
		simarray[pkpos].append(sxc[pkpos])
			
	
	else:
	
		for d in range (len(simarray[pkpos])-1,-1,-1):
		
			if sxc[pkpos] >= simarray[pkpos][d]:
				simarray[pkpos].insert(int(d+1),sxc[pkpos])
				break
					
			if d == 0:
				simarray[pkpos].insert(0,sxc[pkpos])


# ---- calculate FWHMs of autocorrelation functions ----------------------------


# autocorrelate
rxc, rxce, rtl = xcor(rflux, rtime, rflux, rtime, tstart, tend, n_bins)
xxc, xxce, xtl = xcor(xflux, xtime, xflux, xtime, tstart, tend, n_bins)


# Find distance from half maximum
mrxc = []
for rpos in range(len(rxc)):

	if rxc[rpos] > 0:
		mrxc.append(rxc[rpos]-0.5)
	else:
		mrxc.append(0)

mxxc = []
for xpos in range(len(xxc)):

	if xxc[xpos] > 0:
		mxxc.append(xxc[xpos]-0.5)
	else:
		mxxc.append(0)
		
# find maximum and minimum values around crossing points

rhigh = 0
rlow = len(mrxc)
for rswitch in range(len(mrxc)-1):

	if mrxc[rswitch]*mrxc[rswitch+1] < 0:

		if rswitch <= rlow:

			rlow = rswitch
			
		if rswitch+1 >= rhigh:
		
			rhigh = rswitch+1



xhigh = 0
xlow = len(mxxc)
for xswitch in range(len(mxxc)-1):

	if mxxc[xswitch]*mxxc[xswitch+1] < 0:

		if xswitch <= xlow:

			xlow = xswitch
			
		if xswitch+1 >= xhigh:
		
			xhigh = xswitch+1
			
# Interpolate crossing values, calculate typical peak width
rlowv= rtl[rlow] + ( ((0.5 - rxc[rlow]) / \
	(rxc[rlow+1] - rxc[rlow])) * (rtl[rlow+1] - rtl[rlow]) )
rhighv=rtl[rhigh] - (rtl[rhigh] - rtl[rhigh-1]) + ( ((0.5 - rxc[rhigh-1]) / \
	(rxc[rhigh] - rxc[rhigh-1])) * (rtl[rhigh] - rtl[rhigh-1]) )

rfwhm = rhighv - rlowv

xlowv= xtl[xlow] + ( ((0.5 - xxc[xlow]) / \
	(xxc[xlow+1] - xxc[xlow])) * (xtl[xlow+1] - xtl[xlow]) )
xhighv=xtl[xhigh] - (xtl[xhigh] - xtl[xhigh-1]) + ( ((0.5 - xxc[xhigh-1]) / \
	(xxc[xhigh] - xxc[xhigh-1])) * (xtl[xhigh] - xtl[xhigh-1]) )

xfwhm = xhighv - xlowv

totfwhm  = numpy.sqrt(rfwhm**2 + xfwhm**2)
typwidth = (tend - tstart)/(totfwhm)

print "typical peak width:", typwidth

# ---- create confidence curves ------------------------

	
# determine confidence levels

lev90 = []

for nin in range(n_bins):
	level90 = int( len(simarray[nin])*(0.9**(typwidth**(-1)) ) )
	lev90.append(simarray[nin][level90]) 


lev75 = []
for sev in range(n_bins):
	level75 = int( len(simarray[sev])*(0.99**(typwidth**(-1)) ) )
	lev75.append(simarray[sev][level75])

print level90, level75
# -------------------------------

		

plot(tl,xc)
plot(tl,lev90)
plot(tl,lev75)
xlabel('Lag')
ylabel('Power')


show()









