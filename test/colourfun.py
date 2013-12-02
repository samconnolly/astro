from matplotlib import mpl,pyplot
import numpy as np

# create array
zvals = np.array([np.zeros(100) for i in range(100)])*10-5

# initial values
nsteps      = 40000			  # number of steps
start       = [50,50]			  # start position
directions  = [[0,-1],[-1,0],[1,0],[1,0]] # direction transforms (u,l,d,r)
direc       = 0   			  # start direction
add         = 100

#run steps
cpos  = start

for step in range(nsteps):

	tcpos = (cpos[0],cpos[1])          # convert current position to tuple
	comp = np.add(cpos,directions[direc]) # set comparison cell to left of direction of motion

	if comp[0] == -1:	   # check for edge
		comp[0] = 99	   # change position to opposite edge if at edge

	if comp[0] == 100:	   # check for edge
		comp[0] = 0	   # change position to opposite edge if at edge

	if comp[1] == -1:	   # check for edge
		comp[1] = 99	   # change position to opposite edge if at edge

	if comp[1] == 100:	   # check for edge
		comp[1] = 0	   # change position to opposite edge if at edge

	tcomp = (comp[0],comp[1])	   # convert comparison cell position to tuple

	if zvals[tcpos] > zvals[tcomp]:    # if the value in the comparison cell is less than
	   				   # the current cell...
		zvals[tcomp] += add	   # add to the comparison cell
		cpos = np.add(cpos,directions[direc]) # update position to comparison cell's

		if cpos[0] == -1:	   # check for edge
			cpos[0] = 99	   # change position to opposite edge if at edge

		if cpos[0] == 100:	   # check for edge
			cpos[0] = 0	   # change position to opposite edge if at edge

		if cpos[1] == -1:	   # check for edge
			cpos[1] = 99	   # change position to opposite edge if at edge

		if cpos[1] == 100:	   # check for edge
			cpos[1] = 0	   # change position to opposite edge if at edge

	if zvals[tcpos] <= zvals[tcomp]:   # if the value in the comparison cell is more than
					   # the current cell...
		direc += 2                 # change direction to oppoite, i.e. turning right

		if direc > 3:		   # return to start of direction array if at end
			direc -= 4

		comp = np.add(cpos,directions[direc]) # change the comparison cell to the cell
						      # to the right

		if comp[0] == -1:	   # check for edge
			comp[0] = 99	   # change position to opposite edge if at edge

		if comp[0] == 100:	   # check for edge
			comp[0] = 0	   # change position to opposite edge if at edge

		if comp[1] == -1:	   # check for edge
			comp[1] = 99	   # change position to opposite edge if at edge

		if comp[1] == 100:	   # check for edge
			comp[1] = 0	   # change position to opposite edge if at edge

		tcomp = (comp[0],comp[1])          # convert new comparison cell position to tuple
		zvals[tcomp] += add		   # add to the comparison cell
		cpos = np.add(cpos,directions[direc]) # change position to that of the comparison cell

		if cpos[0] == -1:	   # check for edge
			cpos[0] = 99	   # change position to opposite edge if at edge

		if cpos[0] == 100:	   # check for edge
			cpos[0] = 0	   # change position to opposite edge if at edge

		if cpos[1] == -1:	   # check for edge
			cpos[1] = 99	   # change position to opposite edge if at edge

		if cpos[1] == 100:	   # check for edge
			cpos[1] = 0	   # change position to opposite edge if at edge

	direc += 1			   # turn left
		
	if direc > 3:
		direc -= 4

# make a color map of the colour gradient
cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['red','yellow','green'],
                                           256)
# tell imshow about colour map so that only set colors are used
img2 = pyplot.imshow(zvals,interpolation='nearest',
                    cmap = cmap2,
                    origin='lower')

# make a color bar
pyplot.colorbar(img2,cmap=cmap2)

pyplot.show()
