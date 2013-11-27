from numpy import *
import pylab

def wait():
        raw_input("press enter")
        return

f= open("pulsar.dat","r")                                      # import file
x=[]
dT=0.004  #time between measurements (in seconds)
for line in f:
        x.append(float(line))
t=arange(len(x))
t=t*dT
        
        


pylab.plot(t,x)                  # plot lightcurve
pylab.show()
wait()                           # wait for key press

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

ki=100          #start k to ignore sample frequency
S=0.1           #step size
R=1000         #Number of steps

for i in range(ki,int(R+ki)):
        k=float(i)*S        #set k values
        f=k/(float(N)*float(dT))              #calculate frequency
        q=fourier(k,x)
        F.append(f)
        P.append(q)

pylab.plot(F,P)                  # plot spectrum

pylab.show()
        

