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
cols = ['m','o','c','he','h', 'B','N'] 
data = pd.read_table("corsico.dat",sep = "  |   |    |\t", header = None, names=cols, skiprows=1, usecols = [0,1,2,3,4,5,6],dtype={'h':np.float64},engine="python")
#data_2 = pd.read_table("~/wdec2/wdec/output.dat",sep="  |   |    |\t", header = None, names=cols, skiprows=1, usecols = [0,1,2,3,4],engine="python")
#print(data_2)

#data.m = [ 10.0**x for x in data.m ]
'''
print(max(data.h))
print(max(data.he))

print(type(data.m[1]))
print(type(data.o[1]))
print(type(data.c[1]))
print(type(data.he[1]))
print(type(data.h[1]))
'''

for i in np.arange(0,len(data.N)):
    #print(data.N[i])
    if data.N[i] != -0.0:
        data.N[i] = math.log10(data.N[i])
    else:
        data.N[i] = -1000

#print(data.h)

plt.figure(100)
plt.plot(data.m,data.o,'r', label = '$X_O$')
plt.plot(data.m,data.c,'k',label = '$X_C$')
plt.plot(data.m,data.he,'b',label = '$X_{He}$')
plt.plot(data.m,data.h, 'g',label = '$X_H$')
plt.plot(data.m,data.N, 'r--', label = "log(N^2)")
'''
plt.plot(data_2.m,data_2.o,'r', label = '1')
plt.plot(data_2.m,data_2.c,'k',label = '2')
plt.plot(data_2.m,data_2.he,'b',label = '3')
plt.plot(data_2.m,data_2.h, 'g',label = '4')
'''
plt.text(-0.5,1.05, "O")
plt.text(1,1.05, "C")
plt.text(2.75,1.05, "He")
plt.text(6,1.05, "H")
plt.text(1.5,-2, "$log(N^2)$")
#plt.xlim([0,10])
plt.ylim([-5,3])
plt.xlabel('-log(1-Mr/M*)')
#plt.legend([9,-4])
plt.show()
