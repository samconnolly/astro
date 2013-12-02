
"""
Created on Fri Oct 25 12:01:30 2013

Author: Sam Connolly

Test the uvfraction function. Plot the result.

"""

from uvfraction import *
import pylab

uv, uvCum, radii, rFraction = uv_fraction(1e6,mdot_from_edd(0.01,1e6),3.1*Schwarz(1e6),
								1000*Schwarz(1e6),1000,1000)

radii /= Schwarz(1e6)

pylab.subplot(2,1,1)								
pylab.plot(radii,uvCum)
pylab.subplot(2,1,2)						
pylab.plot(radii,uv)
pylab.show()