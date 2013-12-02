import pyfits
import os

route  = "/net/raid/raid1/xray/raid/sdc1g08/NetData/ngc1365/spectra/test/"

# file
spectrum = "0tmpout.bak"


#------------------ MAIN PROG --------------------------------------------------

here = os.getcwd()

os.chdir(route)

head = pyfits.open(spectrum, mode = 'update')

change = head[0].header

change.set('EXPOSURE',5.0E+02)

#print change

head.writeto('E'+spectrum)

head.close()

os.chdir(here)




