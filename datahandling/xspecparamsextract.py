"""
xspecparamsextract.py
Sam Connolly 27/02/2013

#===============================================================================
# extract the paramaters of multiple fits in xspec from a copy of the output
# and plot. And save in column format if required.
#===============================================================================
"""

# Import packages

import pylab as plt
import matplotlib
import numpy as np

#================ PARAMETERS ===================================================

# read variables
header = 1 # number of header lines to ignore
specnum = 10 # number of spectra
paramnum = 11 #number of paramaters

plot = True # plot?

single = False # plot single column of data? (x column)


x, y = 11, 5 # paramater numbers to plot (from 1st spectrum)

totfluxX = False # Or plot against total flux for each spectrum...
totflux = [0.1873, 0.2725, 0.37165, 0.50975, 0.6437,\
				 0.8219, 1.12475, 1.33, 1.746, 2.3745]
totfluxerr = [0.0644,0.0174,0.02445,0.1051,0.1626,\
				0.1404,0.14825,0.082,0.343,0.2855]

labels = False		# data labels?

xlabel = "Absorbed Normalisation"
ylabel = "Absorbing Column (nH)" #Column (nH)


log = False			# log graph?

#   File routes
route            = "/disks/raid/raid1/xray/raid/sdc1g08/NetData/Ngc4395/"\
						+ "spectra/gtitotcntshardbin/fits/"

# file names
infilename 	= 'first.txt' #"fit.dat"


# saving?
save = False
saveerr = True # write errors to save file?
qdp = True # add error header for qdp?

savecol = np.array([6,14]) # param numbers to write to save file

savefname = 'PLfixednHfreeNorms.qdp'

#=== basic (log) straight line fit (least squares, errors not included) ========
# requires two points which are roughly in line with the fit...

fit = False # run fit?

fstart = 1  # distance from start (start = 1)
fend   = 1  # distance from end (end = 1)

resolution = 10.0 # fit resolution factor (lower is better, myabe.. must be > 1)

force = False # force intercept at...
fconst = 0.0

forceGrad = False # force grad to...
fgrad = -3.5

#===============================================================================

#

savecol -= 1

# create file routes
location  = route+infilename
savelocation = route+savefname

# read data intoarray

pnum, cnum, cname, pnam, unit, value, plusminus, error = 0,0,0,0,0,0,0,0
apnum, acnum, acname, apnam, aunit, avalue, aplusminus, aerror\
					 = [],[],[],[],[],[],[],[]
arrays = [apnum, acnum, acname, apnam, aunit, avalue, aplusminus, aerror]



start =  - header
spec  = 1
end = 0
infile= open(location, 'r')

for line in infile:
	if spec <= specnum:
	
		pnum, cnum, cname, pnam, unit, value, plusminus, error \
							= 0,0,'','','',0.0,'',0.0

		if start >= 0:
		
			if start != paramnum: 

				data = line.split()
								
				if len(data) == 7:

					if data[6] == "frozen":

						pnum, cnum, cname, pnam, unit,value, error = data
						error = 0.0
					else:

						pnum, cnum, cname, pnam, value, plusminus, error = data

				if len(data) == 8:
					
					pnum, cnum, cname, pnam, unit, value, plusminus, error = data


				if len(data) == 6:
		
					pnum, cnum, cname, pnam, value, error = data

					if data[5] == "frozen":

							error = 0.0

				values = [int(pnum), int(cnum), cname, pnam, unit,\
							 float(value), plusminus, float(error)]

				for val in range(len(values)):

					arrays[val].append(values[val])

			else:
				start = -1
				spec += 1

		start += 1

	else:
		end += 1

		if end == 4:
			chi2 = line.split()[3]

infile.close()

params = [[[] for i in range(paramnum)],[[] for i in range(paramnum)]]

i = 0
s = 0
p = 0

for val in range(len(arrays[5])):
	
	params[0][p].append(arrays[5][i])
	
	if arrays[6][i] == '=':
		params[1][p].append(arrays[7][p])

	else:
		params[1][p].append(arrays[7][i])

	i += paramnum
	s += 1

	if s == specnum:
		p += 1
		s = 0
		i = p

x -= 1 
y -= 1 

# total flux plot?

if totfluxX:

	params[0][x] = totflux
	params[1][x] = totfluxerr

#=========== line fit ==========================================================
if fit:

	# setup

	fstart -= 1

	fend -=1
	fend = -1 - fend

	if log:

		# initial grad
		grad = (np.log(params[0][y][fend]) - np.log(params[0][y][fstart]))/ \
				(np.log(params[0][x][fend]) - np.log(params[0][x][fstart]))

		# initial cnst
		if force:
			const = 0

		else:
			const = np.log(params[0][y][fstart]) - \
					grad*np.log(params[0][x][fstart])

		if force == True:

			const = np.log(fconst)

	else:

		# initial grad
		grad = ((params[0][y][fend]) - (params[0][y][fstart]))/ \
		((params[0][x][fend]) - (params[0][x][fstart]))

		# initial cnst
		if force:
			const = 0

		else:
			const = (params[0][y][fstart]) - \
					grad*(params[0][x][fstart])# initial cnst

		if force == True:

			const = fconst

	igrad = grad
	iconst = const
	ires = 0 # initial residuals

	

	for  a in range(len(params[0][x])):	

		if log:

			ires += (grad*np.log(params[0][x][a]) + const\
						 - np.log(params[0][y][a]))**2

		else:
		
			ires += (grad*(params[0][x][a]) + const\
						 - (params[0][y][a]))**2

	# fitting loops
	#-----------------
	
	# fit grad



	if forceGrad == False:

		factor = 1.0

		while factor > 0.00000000001:

			res  = 0
			resp = 0
			resm = 0

			for  a in range(len(params[0][x])):

				if log:

					res += (grad*np.log(params[0][x][a]) + const\
								 - np.log(params[0][y][a]))**2

					pgrad = grad+ 1.0*factor

					resp += (pgrad*np.log(params[0][x][a]) + const\
								 - np.log(params[0][y][a]))**2

					mgrad = grad - 1.0*factor

					resm += (mgrad*np.log(params[0][x][a]) + const\
								 - np.log(params[0][y][a]))**2



				else:

		
					res += (grad*(params[0][x][a]) + const\
								 - (params[0][y][a]))**2

					pgrad = grad+ 1.0*factor

					resp += (pgrad*(params[0][x][a]) + const\
								 - (params[0][y][a]))**2

					mgrad = grad - 1.0*factor

					resm += (mgrad*(params[0][x][a]) + const\
								 - (params[0][y][a]))**2

			if resp < res:

				grad = pgrad

			if resm < res:

				grad = mgrad 

			else:

				factor *= (1.0/resolution)

			#print res,resp,resm

	else:

		grad = fgrad

	# fit const loop

	factor = 1.0

	if force == False:
		while factor > 0.00000000001:

			res  = 0
			resp = 0
			resm = 0

			for  a in range(len(params[0][x])):

				if log:

					res += (grad*np.log(params[0][x][a]) + const\
								 - np.log(params[0][y][a]))**2

					pconst = const+ 1.0*factor

					resp += (grad*np.log(params[0][x][a]) + pconst\
								 - np.log(params[0][y][a]))**2

					mconst = const - 1.0*factor

					resm += (grad*np.log(params[0][x][a]) + mconst\
								 - np.log(params[0][y][a]))**2

				else:


					res += (grad*(params[0][x][a]) + const\
								 - (params[0][y][a]))**2

					pconst = const+ 1.0*factor

					resp += (grad*(params[0][x][a]) + pconst\
								 - (params[0][y][a]))**2

					mconst = const - 1.0*factor

					resm += (grad*(params[0][x][a]) + mconst\
								 - (params[0][y][a]))**2


			if resp < res:

				const = pconst

			if resm < res:

				const = mconst 

			else:

				factor *= (1.0/resolution)

			#print res,resp,resm

# calculate likelihood... NO WORK


#

#mean = 0
#sigma = 1
#hoop = np.arange(-10,10,0.01)

#gauss = []

#def gaussian(v,mean,sigma):

#	val = ( 1.0/ ( sigma*np.sqrt(2.*np.pi) ) ) * \
#						( np.exp(-0.5*(((v-mean)/sigma)**2)) ) 
#	print ( 1.0/ ( sigma*np.sqrt(2.*np.pi) ) ) 
#	return val

#for d in np.arange(-3,3,0.01):

#	gauss.append(gaussian(d,0,1))

#print np.trapz(gauss)

#print gaussian(0,0,1)

#probs = []

#for  s in range(len(params[0][y])):

#	mean  = params[0][y][s]
#	sigma = params[1][y][s]*2.0
#	v     = params[0][x][s]*grad + const

#	prob = gaussian(v,mean,sigma)
#	print mean,sigma,v,prob
#	probs.append(prob)

#print gaussian(1.14,1.87,0.18)

#======= save if required ======================================================

if save:

	out = open(savelocation, 'w')

	if qdp:

		out.write(str("READ Serr 1 2 \n"))

	for l in range(len(params[0][0])):

		pr = ''

		for p in range(len(savecol)):

			out.write(str(params[0][savecol[p]][l]) + '\t')

			pr = pr + str(params[0][savecol[p]][l]) + '\t'

			if saveerr:
				out.write(str(params[1][savecol[p]][l]) + '\t')
				pr = pr + str(params[1][savecol[p]][l]) + '\t'

		pr = pr + chi2

		print pr

		out.write('\n')

	out.close()



#================ plot with pylab ==============================================

if plot:

	font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}
	matplotlib.rcParams.update({'font.size': 22})
	matplotlib.rc('xtick', labelsize=20) 
	matplotlib.rc('ytick', labelsize=20)

	axisrange = range(len(params[0][x]))


	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

	if single == False:

		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.errorbar(params[0][x],params[0][y], xerr = params[1][x], \
			yerr = params[1][y], marker='o', color = 'red', \
				ecolor = 'grey', linestyle = 'none',linewidth=2, capsize = 0)

		#plt.xlim(0.003,0.0155)

	else:
	
		plt.errorbar(axisrange, params[0][x], xerr = params[1][x], \
						marker='.', color = 'red', \
							ecolor = 'grey', linestyle = 'none',capsize = 0)

	if log == True:

		ax.set_yscale('log')
		ax.set_xscale('log')
		ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

	else:

		plt.ticklabel_format(style='sci', scilimits=(0,0))

	if labels:

		for index in range(len(params[0][0])):
			plt.annotate(index +1, 
					xy = (params[0][x][index], params[0][y][index]), 
					xytext = (-20,20),
					textcoords = 'offset points', ha = 'right', va = 'bottom',
					bbox = dict(boxstyle = 'round,pad=0.5', fc = 'blue', alpha = 0.5),
					arrowprops = dict(arrowstyle = '->', 
					connectionstyle = 'arc3,rad=0'))


	#plt.ylim([-2.7,1.95])
	#plt.xlim([0.0,0.015])

	if fit:

		if log:

			fitx = [params[0][x][fstart]/2.0,params[0][x][fend]*2.0]
			fity = [np.exp(np.log(params[0][x][fstart]/2.0)*grad+const),\
					np.exp(np.log(params[0][x][fend]*2.0)*grad+const)]

		else:

			fitx = [0,params[0][x][fstart],params[0][x][fend],\
						(params[0][x][fend]*2.)]
			fity = [const,((params[0][x][fstart])*grad+const),\
					((params[0][x][fend])*grad+const),\
						((params[0][x][fend]*2.)*grad+const)]

		plt.plot(fitx,fity)

		# plot initial fit if log...

		print igrad,iconst
		#fiddle!
		#igrad = -2.9
		#iconst = -21.4

		#if log:
		#	ifitx = [params[0][x][fstart],params[0][x][fend]]
		#	ifity = [np.exp(np.log(params[0][x][fstart])*igrad+iconst),\
		#		np.exp(np.log(params[0][x][fend])*igrad+iconst)]

		#	plt.plot(ifitx,ifity)

		# plot model not in logs

		#if log:

		#	nlfitx = [params[0][x][fstart],params[0][x][fend]]
		#	nlfity = [(params[0][x][fstart]**grad)*np.exp(const),\
		#			(params[0][x][fend]**grad)*np.exp(const)]

		#	plt.plot(nlfitx,nlfity)

		print "initial square residual total: ", ires
		print "initial gradient: ",igrad,"initial intercept: ", iconst

		imodel = 'y = ' + str(np.exp(iconst)) + ' * x^(' + str(igrad) + ')'
		print "initial model: ",imodel

#		print "final square residual total: ", res
		print "gradient: ",grad,"intercept: ", const

		if log:
			model = 'y = ' + str(np.exp(const)) + ' * x^(' + str(grad) + ')'
		else:
			model = 'y = ' + str(grad) + ' x + '+ str(const)

		print model

		#print nlfitx,nlfity

		#print fstart, fend

	plt.show()

#plt.plot(probs)
#plt.show()

