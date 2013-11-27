"""
plot.py

Sam Connolly 28/05/2013

#===============================================================================
# Programme to put gaps into a data set and plot as a single plot with broken a 
# broken x-axis. plus y errors. #===============================================================================

"""

# Import packages

import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import numpy as np

#---- Input Parameters ---------------------------------------------------------

# read variables
header = 1 				# number of header lines to ignore

xcolumn, ycolumn = 1, 2 # column numbers to plot
yerrcolumn = 3 			# column numbers for errors ('None', for none)

xlabel = "MJD - 50,000"
ylabel = "Count Rate (counts s$^{-1}$)"
toplabel = ''

#   File routes
route            = "/net/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/lightcurve/refinedCounts/"

# file names
infilename 	= "NGC1365_lcurve_3_0.5-10keV.qdp"

# limits on plots
lims1 = [3900,3950] 
lims2 = [4950,5130]
lims3 = [6120,6380]

#===============================================================================

# create file route
location  = route+infilename

# read data intoarray

start = 0

infile= open(location, 'r')


for line in infile:
	
	linedata = line.split()
	
	if start == header:
		columns = len(linedata)
		data = [[] for x in range(columns)]

	if start >= header:
		for column in range(columns):
			if len(linedata) == columns:
				data[column].append(float(linedata[column]))
		
	start += 1

infile.close()
	
xcolumn -= 1 
ycolumn -= 1 
yerrcolumn -= 1

#-------------------------------------------------------------------------------

fig = plt.figure()

# plot widths...

width1 = lims1[1] - lims1[0]
width2 = lims2[1] - lims2[0]
width3 = lims3[1] - lims3[0]

ratio1 = 1.0
ratio2 = float(width2)/float(width1)
ratio3 = float(width3)/float(width1)


gs = gridspec.GridSpec(1, 3, width_ratios=[ratio1,ratio2,ratio3]) 


# fonts...

font = {'family' : 'normal',

        'weight' : 'bold',
        'size'   : 16}
plt.rcParams.update({'font.size': 16})
plt.rc('xtick', labelsize=14) 
plt.rc('ytick', labelsize=14)

# plot the same data on all axes

fig.text(.45, .02, xlabel, fontsize = 14, fontweight = 'bold')
fig.text(.02, .65, ylabel, fontsize = 14, fontweight = 'bold',rotation = 90)


ax = fig.add_subplot(gs[0])

plt.errorbar(data[xcolumn],data[ycolumn], yerr= data[yerrcolumn],\
			marker='o', color = 'red', \
			ecolor = 'grey', linestyle = 'none',capsize = 0,linewidth=2)

ax2 = fig.add_subplot(gs[1])

plt.errorbar(data[xcolumn],data[ycolumn], yerr= data[yerrcolumn],\
			marker='o', color = 'red', \
			ecolor = 'grey', linestyle = 'none',capsize = 0,linewidth=2)

ax3 = fig.add_subplot(gs[2])

plt.errorbar(data[xcolumn],data[ycolumn], yerr= data[yerrcolumn],\
			marker='o', color = 'red', \
			ecolor = 'grey', linestyle = 'none',capsize = 0,linewidth=2)

# zoom-in / limit the view to different portions of the data
ax.set_xlim(lims1) 
ax2.set_xlim(lims2)
ax3.set_xlim(lims3) 

ax.set_ylim(-0.01,0.81) 
ax2.set_ylim(-0.01,0.81)
ax3.set_ylim(-0.01,0.81)



# hide the spines between ax and ax2
#ax.spines['right'].set_visible(False)
ax.spines['right'].set_linestyle('dashed')

ax2.spines['left'].set_visible(False)
#ax2.spines['right'].set_visible(False)
ax2.spines['right'].set_linestyle('dashed')
ax2.axes.get_yaxis().set_visible(False)

ax3.spines['left'].set_visible(False)

ax.yaxis.tick_left()

ax3.yaxis.tick_right()

ax.xaxis.set_ticks([3900.,3950.])

d = .015 # how big to make the diagonal lines in axes coordinates
d2 = d/ratio2
d3 = d/ratio3

# arguments to pass plot, just so we don't keep repeating them

kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((1-d,1+d),(-d,+d), **kwargs)    # bottom right
ax.plot((1-d,1+d),(1-d,1+d), **kwargs)    # top right

kwargs.update(transform=ax2.transAxes)  # switch to the middle axes
ax2.plot((-d2,+d2),(-d,+d), **kwargs)    # top left
ax2.plot((-d2,+d2),(1-d,1+d), **kwargs)    # bottom left
ax2.plot((1-d2,1+d2),(-d,+d), **kwargs)    # bottom right
ax2.plot((1-d2,1+d2),(1-d,1+d), **kwargs)    # top right

kwargs.update(transform=ax3.transAxes)  # switch to the right axes
ax3.plot((-d3,+d3),(-d,+d), **kwargs)    # top left
ax3.plot((-d3,+d3),(1-d,1+d), **kwargs)    # bottom left


fig.suptitle(toplabel, fontsize=16, )

plt.show()
