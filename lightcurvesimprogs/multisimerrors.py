"""
multisimerrors.py

Created in November  2012

Author: Sam Connolly

#================================================================================
# Discrete cross correlation and confidence-simulation code
#================================================================================

cross-correlate two signals, simulate lightcurves, create confidence curves.
Currently just takes the known parameters for the lightcurve simulation.
The notation assumes you're cross-correlatiing radio and x-ray data, but it
makes no difference of course. The 'X-ray' data set is simulated. Incorporates
errors. Incorporates errors.

Requires: 
	lcsimulation	- light curve simulation code (Timmer & Koenig method)
	callxcorErr		- discrete cross-correlation code with errors
"""

# Import packages

from lcsimulation import lcsim
from callXcorErr     import xcor
from pylab import *
import numpy as np


# --------- PARAMETERS ----------------------------------------------------------

#   File routes
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
radiofname  = "V.dat"				# radio data filename
xrayfname   = "XCountsTrim.dat"		# xray data filename
outfname    = "xcor.dat"			# output data filename

# variables
n_bins  =  300			# number of bins to bin CCF
ncurves =  2				# number of simulated lightcurves
t_lim   = True			# limit time lag range?
t_range =  130			# time range (+ and -) for lags in days	

# ami data...
#psdindexlow  = 2.40		# PSD low frequecy spectral index...
#psdindexhigh = 1.00 		# ... and high frequency spectral iondex
#psdbrkfreq   = 5.14e-5		# PSD break frequency

psdindexhigh  = 0.1
psdindexlow   = 1.65
psdbrkfreq	= 0.1

# plots to show
autocorr = True	# autocorrelation functions of each dataset
lcomp	= False	# sample simulated lightcurve and data curve to compare
ccfs		= False	# cross correlation distribution of simulated data and real ccf
confccf	= True	# real ccf with confidence curves overplotted

#================================================================================

# declare data arrays
rtime    = np.array([])
rflux    = np.array([])
rfluxerr = np.array([])
xtime    = np.array([])
xflux    = np.array([])
xfluxerr = np.array([])

# create file routes
radiolocation = route+radioroute+radiofname
xraylocation = route+xrayroute+xrayfname
outlocation = route+outroute+outfname

# ============ read data into 2-D arrays ========================================
# open files and read in data

# radio
radioin= open(radiolocation, 'r')

start = 0

for x in radioin:
	
	currtime, currflux,currfluxerr = x.split()
	if start == 1:
		rtime 	= np.append(rtime,float(currtime))
		rflux 	= np.append(rflux,float(currflux))
		rfluxerr = np.append(rfluxerr,float(currfluxerr))
		
	start = 1

radioin.close()

# X-ray
xrayin= open(xraylocation, 'r')

start = 0

for y in xrayin:
	currtime, currflux,currfluxerr = y.split()
	if start == 1:
		xtime 	= np.append(xtime, float(currtime))
		xflux 	= np.append(xflux, float(currflux))
		xfluxerr = np.append(xfluxerr, float(currfluxerr))
		
	start = 1

xrayin.close()

# ========== Run xcor function on data ==========================================
# Create cross-correlation function for teh real data sets

xc, tl, nbin = xcor(rflux,rfluxerr, rtime, xflux,xfluxerr, xtime, n_bins,t_lim,t_range)

# ========= Simulate Light Curves ===============================================
# create artificial lighturves, interpolate curve with same sampling pattern
# as data, cross-correlate with one real data set

# --- simulated curve time arrays ---
# create array of integer times from X-ray timing values from the start of the 
# observations, to correspond to the integer time sampling in the simulated 
# lightcurve, and the difference in time between the integer value and the actual
# value, in order to interpolate a value for a simulated curve follwing the same
# sampling pattern as the data 
 
simtime = np.array([(xtime - xtime[0]).astype(int),xtime - xtime.astype(int)])

simarray = [[] for h in range(n_bins)] 		# binned, simulted CCF array

first = 1
shows = 0

# for n curves....
for curve in range(ncurves):

	# -- simulate curve --

	lc  = lcsim(xflux,xtime,psdindexlow, psdindexhigh, psdbrkfreq,
				np.mean(xflux),np.std(xflux),curve) 		# simulate curve
	
	# -- interpolate values with data sampling pattern --
	
	lcsamp = []
	for val in range(len(simtime[0])):
		index = simtime[0][val]		# index of nearest value in time (before)
		
		# interpolate amplitude from nearest two values & gradient between them
		intval= lc[index] + ( lc[index+1]-lc[index] ) * ( simtime[1][val] )
		
		lcsamp.append(intval) # sampled simulated lightcurve
	
	# -- cross correlate with 2nd data set --
	
	sxc, stl, sba = xcor(rflux,rfluxerr, rtime, lcsamp,np.zeros(len(lcsamp)), xtime,  n_bins,t_lim,t_range)
	
	# -- sort and put into array of sorted, simulated CCF values --	
	
	# if first CCF, just add to the values to each bin
	if first == 1:
		
		for sc in range(n_bins):
		
			simarray[sc].append(sxc[sc])
			
		first = 0
	
	# for each value in the CCF, working backwards, add the values into the bins
	# such that they are sorted in order from highest to lowest
	if first == 0:
	
		for sx in range(n_bins): # for each value...
				
			for d in range (len(simarray[sx])-1,-1,-1): # work backwards through
												   # the corresponding bin
   				if sxc[sx] >= simarray[sx][d]:
					simarray[sx].insert(int(d+1),sxc[sx]) # add in sorted place
					break
					
				if d == 0:
					simarray[sx].insert(0,sxc[sx])	# or at start if greatest

	shows += 1

	if shows == 100: # print progress every hundred curves

		print curve + 1
		shows = 0

# plot sample lightcurves and data lightcurve
if lcomp:
		
	subplot(2,1,1)
	plot(xtime,xflux)
	title("Lightcurve and sample artificial lightcurve")
	xlabel('MJD')
	ylabel('Data Flux (counts/s)')
	
	subplot(2,1,2)
	plot(xtime,lcsamp)
	xlabel('MJD')
	ylabel('Simulated Flux (counts/s)')
		
	show()

# plot ccfs of real and fake data
if ccfs:
		
	subplot(2,1,1)
	title("Cross correlation functions of real and artificial data")
	plot(tl,simarray)
	xlabel('Time Lag (s)')
	ylabel('Cross-Correlation Coefficient')	
	
	subplot(2,1,2)
	plot(tl,xc)
	xlabel('Time Lag (s)')
	ylabel('Cross-Correlation Coefficient')	
	
	show()

# ==== calculate FWHMs of autocorrelation functions of data =====================
# to calculate errors, the FWHM is needed...

# -- autocorrelate data ---

rxc, rtl, rbm = xcor(rflux,rfluxerr, rtime, rflux,rfluxerr, rtime, n_bins,t_lim,t_range)
xxc, xtl, xbm = xcor(xflux,xfluxerr, xtime, xflux,xfluxerr, xtime, n_bins,t_lim,t_range)

#  autocorrelation function
if autocorr:

	subplot(2,1,1)
	title("Autocorrelation functions")
	plot(rtl,rxc)
	ylabel('Radio CCF')
	xlabel('time delay (s)')
	subplot(2,1,2)
	plot(xtl,xxc)
	ylabel('X-ray CCF')
	xlabel('time delay (s)')
	show()

# --- identify full central peak widths and half maxima -------------------------
# by finding points beyond which at least one of  the next three points ar not 
# lower than any previous value in that direction

# - radio -
# right edge
rhigh = rxc.tolist().index(max(rxc)) # start from highest point
clow = max(rxc)					# set lowest value so far to highest value

# check if any of next three values are lower than lowest so far
while  (rxc[rhigh+1] < clow) or (rxc[rhigh+2] < clow) or (rxc[rhigh+3] < clow):

	m = rxc[rhigh+1:rhigh+4].tolist()	# create list of next three avlues
	clow = min(m)						# find minimum of next three values
	rhigh = m.index(clow) + rhigh + 1	# set new position to lowest value's


# left edge
rlow = rxc.tolist().index(max(rxc))
clow = max(rxc)

while  (rxc[rlow-1] < clow) or (rxc[rlow-2] < clow) or (rxc[rlow-3] < clow):

	m = rxc[rlow-3:rlow].tolist()
	clow = min(m)
	rlow = m.index(clow) + rlow - 3


# half maximum - using average low value and highest value - DISTANCE ABOVE ZERO
rhm = (max(rxc) - (rxc[rhigh] + rxc[rlow])*0.5)*0.5 +(rxc[rhigh] + rxc[rlow])*0.5

# - xray -
# right edge
xhigh = xxc.tolist().index(max(xxc))
clow = max(xxc)

while  (xxc[xhigh+1] < clow) or (xxc[xhigh+2] < clow) or (xxc[xhigh+3] < clow):

	m = xxc[xhigh+1:xhigh+4].tolist()
	clow = min(m)
	xhigh = m.index(clow) + xhigh + 1

# left edge
xlow = xxc.tolist().index(max(xxc))
clow = max(xxc)

while  (xxc[xlow-1] < clow) or (xxc[xlow-2] < clow) or (xxc[xlow-3] < clow):

	m = xxc[xlow-3:xlow].tolist()
	clow = min(m)
	xlow = m.index(clow) + xlow - 3

# half maximum - using average low value and highest value - DISTANCE ABOVE ZERO
xhm = (max(xxc) - (xxc[xhigh] + xxc[xlow])*0.5)*0.5 +(xxc[xhigh] + xxc[xlow])*0.5

# -------- interpolate FWHM ------------------------------------------------------
# find the two closest values to half maxima on each side and interpolate a value
# for FWHM

# - radio -

# lower half maximum position
lowhm = rxc.tolist().index(max(rxc))

while rxc[lowhm] > rhm:	# find closest values, starting in centre
	lowhm -= 1

# interpolate from two closest values
cdiff 	= rxc[lowhm + 1] - rxc[lowhm]	# difference in ccc
tdiff	= rtl[lowhm + 1] - rtl[lowhm]	# difference in time
hmdiff	= rhm - rxc[lowhm]				# distance of hm from lower value in ccc
grad		= tdiff/cdiff					# dt/dccc gradient
lfwhm	= rtl[lowhm] + grad*hmdiff	# interpolated time value

# upper half maximum position
highhm = rxc.tolist().index(max(rxc))

while rxc[highhm] > rhm:	# find closest values, starting in centre
	highhm += 1

# interpolate from two closest values
cdiff 	= rxc[highhm] - rxc[highhm - 1]		# difference in ccc
tdiff	= rtl[highhm] - rtl[highhm - 1]		# difference in time
hmdiff	= rhm - rxc[highhm -1]				# distance of hm from lower value in ccc
grad		= tdiff/cdiff						# dt/dccc gradient
hfwhm	= rtl[highhm - 1] + grad*hmdiff		# interpolated time value

rfwhm = hfwhm - lfwhm # fwhm!

# - xray -

# lower half maximum position
lowhm = xxc.tolist().index(max(xxc))

while xxc[lowhm] > xhm:	# find closest values, starting in centre
	lowhm -= 1

# interpolate from two closest values
cdiff 	= xxc[lowhm + 1] - xxc[lowhm]	# difference in ccc
tdiff	= xtl[lowhm + 1] - xtl[lowhm]	# difference in time
hmdiff	= xhm - xxc[lowhm]				# distance of hm from lower value in ccc
grad		= tdiff/cdiff					# dt/dccc gradient
lfwhm	= xtl[lowhm] + grad*hmdiff	# interpolated time value

# upper half maximum position
highhm = xxc.tolist().index(max(xxc))

while xxc[highhm] > xhm:	# find closest values, starting in centre
	highhm += 1

# interpolate from two closest values
cdiff 	= xxc[highhm] - xxc[highhm - 1]		# difference in ccc
tdiff	= xtl[highhm] - xtl[highhm - 1]		# difference in time
hmdiff	= xhm - xxc[highhm -1]				# distance of hm from lower value in ccc
grad		= tdiff/cdiff						# dt/dccc gradient
hfwhm	= xtl[highhm - 1] + grad*hmdiff		# interpolated time value

xfwhm = hfwhm - lfwhm	# fwhm!

totfwhm  = np.sqrt(rfwhm**2 + xfwhm**2)	# combined fwhm of both acfs
typwidth = (tl[-1] - tl[0])/(totfwhm)			# typical peak width in ccf

print "typical peak width:", totfwhm
print "confidence correction:", typwidth

# ============ create confidence curves =========================================

	
# determine confidence levels

nc = 0.9**(1.0/typwidth)

lev90 = []
level90 = int( ncurves*(nc) )
for nin in range(n_bins):
	lev90.append(simarray[nin][level90]) 

sc = 0.99**(1.0/typwidth)

lev75 = []
level75 = int(ncurves*(sc) )
for sev in range(n_bins):
	lev75.append(simarray[sev][level75])

tc = 1.-nc

lev10 = []
level10 = int( ncurves*(tc) )
for ten in range(n_bins):
	lev10.append(simarray[ten][level10]) 

fc = 1.-sc

lev25 = []
level25 = int(ncurves*(fc) )
for twy in range(n_bins):
	lev25.append(simarray[twy][level25])

print nc,sc,tc,fc
print "confidence levels:",level90, level75, level10, level25

# plot data ccf with confidence curves
if confccf:
		
	title("Cross correlation function fo data with confidence curves")

	subplot(2,1,1)
#	plot(tl,lev90, color='grey')
#	plot(tl,lev75, color='grey')
#	plot(tl,lev10, color='grey')
#	plot(tl,lev25, color='grey')

	plot(tl,xc, color = 'red')

	xlabel('Time Lag (s)')
	ylabel('Cross-Correlation Coefficient')

	subplot(2,1,2)	
	plot(tl,nbin, color = 'blue')
		
	show()









