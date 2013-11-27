# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 17:08:58 2013

@author: sdc1g08
"""
#import numpy as np
import pylab as plt
import matplotlib
import numpy as np

wavelengths = range(10)
BB1         = np.array([1,2,3,4,5,4,3,2,1,0])
BB2 = BB1 + 2
BB3 = BB2 + 2

fig = plt.figure()

ax1 = fig.add_subplot(4,1,1)

plt.plot(wavelengths,BB1)
plt.plot(wavelengths,BB2)
plt.plot(wavelengths,BB3)

ax2 = fig.add_subplot(4,1,2)
#plt.plot(radii,temps)
plt.plot(wavelengths,BB2)
ax3 = fig.add_subplot(4,1,3)
#plt.plot(radii,maxTemps)
plt.plot(wavelengths,BB3)
ax4 = fig.add_subplot(4,1,4)

plt.show()