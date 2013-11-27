route  = "/export/xray11/sdc1g08/Dropbox/Dropbox/V926Sco/"
froute = "ews/"
fname  = "textavs"

time    = []
flux    = []
fluxerr = []


i=0

location = route+froute+fname

print location


rin= open(location, 'r')

for x in rin:
	currtime, currflux,currfluxerr = x.split()
	time.append(currtime)
	flux.append(currflux)
	fluxerr.append(currfluxerr)	

print time[2], flux[7], fluxerr[9]
