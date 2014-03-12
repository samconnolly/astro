
import numpy as np

#=================================================================================

def StarProfile(n,r,norm=1,offset = (50,50)):
    ''' create a 2-D star profile array, based on an inverted parabola
    
    inputs:
        int n                   - size of size of the array
        float r                 - radius of the star
        float norm (optional)   - peak brightness of the star
        tuple offset (optional) - offset of star from centre
    '''
   
    indices = np.indices((n,n)) - n/2
    
    width = norm/float(r)**2    
    
    v = norm - (width*((indices[0]-offset[0])**2 + (indices[1]-offset[1])**2))
    
    s = v*(v > 0)
    
    return s


def dGauss(n,sig,norm=1,offset = (0,0)):
    ''' create a 2-D Gaussian in an array

    inputs:
    int n - size of a side of the array
    float sig   - width of the Gaussian
	float norm (optional)	 - normalisation of gaussian
	tuple offset (optional) - offset of distribution from centre
	
    outputs:
    array g - the gaussian in an array!
    '''
           
    sig = float(sig)   
    
    mu = n/2
    
    indices = np.indices((n,n))
    expIndices =   (indices-mu + offset[0])**2 / (2*sig**2) # calculate indices
    expIndices =    expIndices[0] + expIndices[1]           # combine
    
    g = norm*np.exp(-expIndices) # calculate value at each point

    return g

def diskGauss(n,Rin,Rout,norm=1,offset = (0,0),fade = 5):
    ''' create a 2-D Gaussian with a central drop, in an array,
		for the purposes of disk simulation.

    inputs:
    int n - size of a side of the array
    int Rin   - inner edge of disk
	int Rout  - outer edge of disk (width of Gaussian)
	float norm (optional)	 - normalisation of gaussian
	tuple offset (optional) - offset of distribution from centre

    outputs:
    array g - the gaussian in an array!
    '''
        
    mu = n/2
    sig = 0.7*Rout    
    
    indices = np.indices((n,n))    
    
    expIndices =   (indices-mu + offset[0])**2 / (2*sig**2) # calculate indices
    expIndices =    expIndices[0] + expIndices[1]           # combine
    fadeIndex  =   (float(Rin)+ offset[1])**2 / (2*sig**2)  # brightness at disc edge
    
    radii =  np.sqrt((indices[0] + offset[0] - (n/2))**2 +\
                (indices[1] + offset[1] - (n/2))**2) # radii!
    
    fader = (radii > Rout)*(radii <= Rout + fade)   # fade away region outside disd
    outer = (radii > Rout + fade)                   # outside disc
    disk  = (radii > Rin)*(radii <= Rout)           # disc region
    inner = (radii <= Rin)                          # inside disc inner edge
    
    # calculate values Gaussian +/ exponential fall of
    disk  = disk*(norm*np.exp(-expIndices) + 0.2)
    fader = fader*(norm*np.exp(-expIndices) + norm*0.2*np.exp(-(radii-Rout)/fade))
    outer = outer*norm*np.exp(-expIndices) 
    inner = inner*norm*np.exp(-fadeIndex)*(np.exp(0.1*radii)/np.exp(0.1*Rin))
    
    g = disk + inner + outer + fader # combine
    
    return g

def Rotate(im, theta,centre = (0,0)):
    ''' rotate an image matrix by an angle theta. Avoids aliasing by sampling
		backwards to fill in the output image.

    input:
    array i                 - input image array (square)
    float theta             - angle to rotate through
    tuple centre (optional) - coordinates of point FROM CENTRE to rotate about

    output:
    array r - rotated image array
    '''

    N = len(im)
    
    n = centre[0]
    m = centre[1]

    rot = np.zeros([N,N])

    offset = ((N/2 + n)-int((N/2 + n)*np.cos(theta) + (N/2 + n)*np.sin(theta)),\
                  (N/2 + m) -int(-(N/2 + m)*np.sin(theta) + (N/2 + m)*np.cos(theta)))
       
    indices = np.indices((N,N))    
    
    rotIndicesX =  (indices[0]*np.cos(theta) + indices[1]*np.sin(theta)) + offset[0]
    rotIndicesY =  (-indices[0]*np.sin(theta) + indices[1]*np.cos(theta)) + offset[1]
    
    rotIndicesX = rotIndicesX.astype(int)    
    rotIndicesY = rotIndicesY.astype(int) 
    
    rotIndicesX =   rotIndicesX*(rotIndicesX >= 0)*(rotIndicesX <N)  
    rotIndicesY =   rotIndicesY*(rotIndicesY >= 0)*(rotIndicesY <N) 
    
    rot = im[rotIndicesX,rotIndicesY]    

    return rot

def RotatePosition(coords,angle, centre = (0,0)):
    '''
    Rotate a position vector by a given angle
    (in order to allow position specific velocity calculations)
    
    inputs:
        tuple coords    - coordinates of the position
        float angle     - angle through which to rotate
        tuple centre    - coordinate centre about which to rotate
        
    outputs:
        tuple rotCoords - rotated coordinates
    '''
    
    # calculate indices backwards, i.e. where on original image corresponds
    # to the rotated image coordines, to avoid aliasing
    rotIndexX =  (coords[0]*np.cos(angle) + coords[1]*np.sin(angle)) - centre[0]
    rotIndexY =  (-coords[0]*np.sin(angle) + coords[1]*np.cos(angle)) - centre[1]

    
    # map across to rotated image
    rotCoords = (rotIndexX,rotIndexY)

    return rotCoords
    

def backAngle(indices, offset = (0,0)):
    '''
    Calculates the angle from the y axis of an array of coordinates.

    input:
        indices	- array containing two arrays, of x & y coordinates		

    output:
        (array) theta - array of angles corresponding to each set of indices
        '''

    X = indices[0] + offset[0]
    Y = indices[1] + offset[1]

    ratio    = Y*(X != 0) / (X + (X == 0)).astype(float) # Y/X ratio where x != 0
    
    greaterTheta = (np.pi/2.0 - np.arctan(ratio))*(X > 0)   # angle when x > 0
    lesserTheta = ((3.0*np.pi)/2.0 - np.arctan(ratio))*(X < 0) # angle when x < 0
    zilch    = (X == 0)*(Y < 0)*np.pi   # set angle to pi when x == 0 and y < 0
                                        # (leave as 0 when x == 0 and y > 0)
    theta = greaterTheta + lesserTheta + zilch  # combine angles
			
    return theta 
    

def VelToRadialVelocity(im, M, offset,offsetM,rmin,rmax,Vmax):
    '''
    Create an array of radial velocities from a set of absolute velocities
    within a given disk space. WARNING! Pretty sure the offset stuff
    doesn't work....
    
    input:
    array im		- Input image (brightness profile) to convert
    float M		- Mass of central object, in units of G*kg
    tuple offset  - Offset of rotation from centre  
    float rmin    - minimum radius below which not to give velocities
    float rmax    - maximum radius above which not to give velocities
     
    output:
    array radVels		- Output image in velocity coordinates
    '''
				
    N = len(im)	
     
    scale = Vmax/float(N/2)      # scale to cover desired velocity range
	
    indices = np.indices((N,N)) 
    indices -= N/2              # centre indices
    
    indices[0] += offset[0]
    indices[1] += offset[1]    
    
    vels = np.sqrt(indices[0]**2 + indices[1]**2)    
    
    vmin = (M/float(rmax))/scale 
    vmax = (M/float(rmin))/scale 
    
    if offset != (0,0):
    
        # calculate Keplerian velocity in OUTPUT image

        radius      = np.sqrt((offset[0])**2 + (offset[1])**2)

        velocity    = np.sqrt(offsetM/radius)/scale

        try:
            angle = -backAngle(offset)
        except NameError:
            print "ERROR - backAngle function not imported"
            return []

        offY = np.around(velocity*np.sin(angle)).astype(int) #+(N/2)
        
        indices[1] = indices[1] - offY                


    # find equivalent radius in spacial paramater space

    radVels = indices[1]*( vels >= vmin)*( vels <= vmax)
			
    return radVels

def SpaceToRadialVelocity(im, M, offset,rmin,rmax):
    '''
    Create an array of radial velocities according to Keplerian
    orbits around the specified point.    
    
    input:
    array im		- Input image (brightness profile) to convert
    float M		- Mass of central object, in units of G*kg
    tuple offset  - Offset of rotation from centre  
    float rmin    - minimum radius below which not to give velocities
    float rmax    - maximum radius above which not to give velocities
     
    output:
    array radVels		- Output image in velocity coordinates
    '''
				
    N = len(im)	
    
    vmax  = np.sqrt(M/float(rmin))
 
    indices = np.indices((N,N)) 
    indices -= N/2              # centre indices
    
    # calculate Keplerian velocity
    radii = np.sqrt((indices[0] + offset[0])**2 + (indices[1] + offset[1])**2)
    radii = radii + (radii == 0)
    
    # find equivalent radius in spacial paramater space
    velocities = np.sqrt(M/radii.astype(float))

    velocities = velocities*(velocities <= vmax)
    #print velocities[N/2]
    # find equivalent angle in spacial param space
    angles = backAngle(indices,offset)
    
    # find indices corresponding to each angle/radius in original image

    radVels = velocities*np.cos(angles)*(radii<=rmax)
			
    return radVels

def SpaceToVelocityInvSolid(im, M,objCoords,vmax=0.1, centre=(0,0)):
    '''
    convert an image from spacial coordinates to velocity coordinates.
    Assumes circular, Keplerian velocity of a solid object, 
    about the centre of the image. Inverts the problem to avoid aliasing.
	
    input:
    array im		          - Input image (brightness profile) to convert
    float M		          - Mass of central object, in units of G*kg
    tuple objCoords         - Coordinates of object on image
    int vmax                - maximum velocity in image              
    tuple centre (optional) - Coordinates of rotation centre
    	
    output:
    array vim		- Output image in velocity coordinates
    '''
    N = len(im)		
			
    scale = vmax/float(N/2)      # scale to cover desired velocity range
	
    indices = np.indices((N,N)) 
    indices -= N/2              # centre indices

    # calculate Keplerian velocity in OUTPUT image
    radius      = np.sqrt((objCoords[0]-centre[0])**2 + (objCoords[1]-centre[1])**2)
    
    angVelocity = np.sqrt(M / radius**3)
    
    velocities = np.sqrt((indices[0]*scale)**2 + (indices[1]*scale)**2)
    velocities = velocities + (velocities == 0)

    # find equivalent radius in spacial paramater space
    radii = velocities.astype(float)/angVelocity 
    
    # find equivalent angle in spacial param space
    angles = backAngle(indices)
    
    # find indices corresponding to each angle/radius in original image
    velIndicesX = np.around(radii*np.cos(angles)).astype(int) +(N/2)
    velIndicesX = velIndicesX*(velIndicesX >= 0)*(velIndicesX < N)

    velIndicesY = np.around(radii*np.sin(angles)).astype(int) +(N/2)
    velIndicesY = velIndicesY*(velIndicesY >= 0)*(velIndicesY < N)
    
    # map to output velocity image
    vim = im[velIndicesX,velIndicesY]
				
    return vim

def SpaceToVelocityInv(im, M, offset = (0,0),offsetM = 0.01,vmax = 0.05):
    '''
    convert an image from spacial coordinates to velocity coordinates.
    Assumes circular, Keplerian velocities, hence differential rotation, 
    about the centre of the image. Inverts the problem to avoid aliasing.
    Can also involve a Keplerian orbit about the offset point, with a
    specified mass.
 
    input:
    array im		              - Input image (brightness profile) to convert
    float M		              - Mass of central object, in units of G*kg
    tuple offset  (optional)    - Offset of rotation from centre    	
    float offsetM (optional)    - Mass for offset orbit
     
    output:
    array vim		- Output image in velocity coordinates
    
    requires:
        backAngle (function)
    '''
    N = len(im)		
			
    scale = vmax/float(N/2)      # scale to cover desired velocity range
	
    indices = np.indices((N,N)) 
    indices -= N/2              # centre indices

    # calculate Keplerian velocity in OUTPUT image
    velocities = np.sqrt((indices[0]*scale)**2 + (indices[1]*scale)**2)
    velocities = velocities + (velocities == 0)

    # find equivalent radius in spacial paramater space
    radii = M/velocities.astype(float) 

    # find equivalent angle in spacial param space
    angles = backAngle(indices)

    # find indices corresponding to each angle/radius in original image
    velIndicesX = np.around(radii*np.cos(angles)).astype(int) +(N/2) - int(offset[0])
    velIndicesX = velIndicesX*(velIndicesX >= 0)*(velIndicesX < N)

    velIndicesY = np.around(radii*np.sin(angles)).astype(int) +(N/2) - int(offset[1])
    velIndicesY = velIndicesY*(velIndicesY >= 0)*(velIndicesY < N)
    
    # map to output velocity image
    vim = im[velIndicesX,velIndicesY]
    
    if offset != (0,0):
        	
        indicesO = np.indices((N,N)) 
    
        # calculate Keplerian velocity in OUTPUT image
        
        radius      = np.sqrt((offset[0])**2 + (offset[1])**2)
        
        velocity    = np.sqrt(offsetM/radius)/scale
        
        try:
            angle = backAngle(offset)
        except NameError:
            print "ERROR - backAngle function not imported"
            return []
            
        #print velocity
        offX = np.around(velocity*np.cos(angle)).astype(int) #+(N/2)
        offY = np.around(velocity*np.sin(angle)).astype(int) #+(N/2)
        
        #offX, offY = 30, 30
        
        indicesOX = indicesO[0] - offX#*10
        indicesOY = indicesO[1] - offY#*10 # bit of a cheat velocity factor here...
        
        indicesOX = indicesOX*(indicesOX >= 0)*(indicesOX < N)
        indicesOY = indicesOY*(indicesOY >= 0)*(indicesOY < N)
       
        vim = vim[indicesOX,indicesOY]
        
    return vim
 
class Trail(object):
    '''Spectral Trail Object

        creation inputs:
            
            N   - image side length
            res - no. trails in image at once
    
    '''
    
    def __init__(self,N,res):
        
        self.N = N                      # image side length
        self.t = int(N/res)             # spectral slice thickness
        self.array = np.zeros([N,N])    # data array
        
    def Next(self,spec):
        
        ''' add a spectrum to the top of the trail,
            move the rest down.'''
                
        Next = self.array[:(self.N-self.t)]                  # take all spectra but end
        
        strip = np.array([spec for i in range(self.t)]) # create new strip spec
    
        Next = np.append(strip,Next)                    # add to top of trail
        
        Next = np.reshape(Next,[self.N,self.N])                   # reshape to square
        self.array = Next 
 
 
