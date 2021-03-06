from numpy import *
from pylab import *

freq         = arange(0.1,10,0.1)
brkfreq      = 7
psdindexLow  = 2
psdindexHigh = 4

pl = piecewise(freq,  [brkfreq>=freq, freq>=brkfreq], # define the power-law form of the PSD		
                [lambda freq: power(freq,-psdindexLow),
                 lambda freq: power(brkfreq,
                 (psdindexHigh-psdindexLow)) * power(freq,-psdindexHigh)])

#plot(freq,pl)
#show()
