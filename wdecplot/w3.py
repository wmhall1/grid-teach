import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np

"""
 -log(1-Mr/M*)    X_O        X_C        X_He       X_H         B          N^2
     0.000000   0.697253   0.302747   0.000000   0.000000   0.000000   0.10961E-05
"""


""" First create the dataframe from minoutput """
cols = ['m','o','c','he','h'] 
data = pd.read_table("corsico.dat",sep = "  |   |    |\t", header = None, names=cols, skiprows=1, usecols = [0,1,2,3,4],dtype={'h':np.float64},engine="python")
print(data)

#data.m = [ 10.0**x for x in data.m ]

print(max(data.h))
print(max(data.he))

print(type(data.m[1]))
print(type(data.o[1]))
print(type(data.c[1]))
print(type(data.he[1]))
print(type(data.h[1]))


#print(data.h)

plt.figure(100)
plt.plot(1-np.exp(-data.m),data.o,'r', label = '$X_O$')
#plt.plot([0,0.5],[0.5,0.5],'k-')
#plt.plot(data.m,data.c,'k',label = '$X_C$')
#plt.plot(data.m,data.he,'b',label = '$X_{He}$')
#plt.plot(data.m,data.h, 'g',label = '$X_H$')
#plt.xlim([0,10])
plt.ylim([0,1])
plt.xlabel('$M_r/M_*$')
#plt.xlabel('-log(1-Mr/M*)')
plt.legend()
plt.show()
