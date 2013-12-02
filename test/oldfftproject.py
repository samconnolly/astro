from numpy import *
import pylab

f= open("/disks/raid/raid1/xray/raid/sdc1g08/ami/refined/5548_ami_r.qdp","r") 
                                     # import file
x=[]
t=[]

flag=0

for line in f:

	time, flux, err = line.split()
	
	if flag == 1:
	
		t.append(float(time))
        	x.append(float(flux))

	flag=1

starttime=t[0]
      
for tp in range(len(t)):
	t[tp] = t[tp] - starttime + 1        




#--------Fourier function-----------

def fourier(k,x):

        N=len(x)
        U=zeros(N+2)
        theta=float(2*pi*k)/float(N)
        
        for i in range(N):
        
                n=(N-1)-i
                U[n]=x[n]+2*cos(theta)*U[n+1]-U[n+2]
                
        A=U[0]-U[1]*cos(theta)
        B=U[1]*sin(theta)
        power= A**2+B**2
        
        return power

#----Main programme - calculate and graph fourier frequency spectrum

P=[]
F=[]
N=len(x)

ki=10          #start k to ignore sample frequency
S=1           #step size
R=13000        #Number of steps


for i in range(len(x)):

        k=float(i)*S        #set k values
        f=k/(t[i])              #calculate frequency
        q=fourier(k,x)
        F.append(f)
        P.append(q)
pylab.subplot(2,1,1)
pylab.plot(t,x)                  # plot spectrum
pylab.subplot(2,1,2)
pylab.plot(F,P)                  # plot lightcurve

pylab.show()
        

