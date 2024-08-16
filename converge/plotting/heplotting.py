'''
Weston Hall
09/21/21

  10600.0    500.0    300.0    200.0    400.0     60.0     12.0     12.0     60.0     70.0     70.0     80.0     45.0     45.0     36.0
'''

import matplotlib.pyplot as plt
import sys
import numpy as np

if len(sys.argv) > 1:
    debug = True
    print("DEBUGGING MODE: writing output to screen")
else:
    debug = False

#with open("../calcperiods") as f:
    #lines = f.readlines()

f=open("../../calcperiods", 'r')

total = 0
titles = []
periods = []
mhe = []
t =[]
p1 = []
p2 = []
p3 = []
p4 = []
p5 = []

userTemp = input("Plot Temp (K): ")
userMass = input("Solar masses (ex. 0.6): ")
userMassH = input("Hydrogen mass -log (ex. 4, 9.5): ")

title = "T = " + str(userTemp) + "K, M = " + str(userMass) + "$M_o$, log($M_{H}$/$M_o$) = -" + str(userMassH) 

userMass = float(userMass) * 1000
userMassH = float(userMassH) * 100

if debug:
    print(userTemp)
    print(userMass)
    print(userMassH)

linenumber = 0
stop = False
while stop == False:
    line = f.readline()
    temp = mass = massh = masshe = 0
    if line[0:3] == "  1":
        temp = float(line[2:8])
        mass = float(line[13:17])
        masshe = float(line[30:35])
        massh = float(line[39:44])
    if temp == float(userTemp) and mass == float(userMass) and massh == float(userMassH):
        total = total+1
        titles.append(linenumber)
        periods.append([float(f.readline()[15:23]), float(f.readline()[15:23]), float(f.readline()[15:23]), float(f.readline()[15:23])])
        mhe.append(masshe)
        #t.append(temp)
        if debug:
            print(temp)
            print(mass)
            print(massh)
            print(masshe)
    linenumber = linenumber +1

    if not line:
        stop = True

"""
for index in titles:
    #mh.append(float(lines[index][40:45])/100)
    #p1.append(float(lines[index+1][15:23]))
    #p2.append(float(lines[index+2][15:23]))
    #p3.append(float(lines[index+3][15:23]))
    #p4.append(float(lines[index+4][15:23]))
    #p5.append(float(lines[index+5][15:23]))
"""

print(periods)
for per in periods:
    p1.append(per[0])
    p2.append(per[1])
    p3.append(per[2])
    p4.append(per[3])


plt.figure(100)
plt.plot(mhe,p1, "-", label = "k = 1")
plt.plot(mhe,p2, "--", label = "k = 2")
plt.plot(mhe,p3, "-.", label = "k = 3")
plt.plot(mhe,p4, ":", label = "k = 4")
plt.ylabel("Period (s)")
plt.xlabel("log($M_H$/$M_o$)")
#plt.title(title)
plt.legend(loc="lower right")
plt.show()
'''
plt.figure(200)
plt.plot(t,p1, label = "k=1")
plt.plot(t,p2, label = "k=2")
plt.plot(t,p3, label = "k=3")
plt.legend()
plt.show()
'''

if debug:
    print(p1)
    print(p2)
    #print(mh)
    #print(p1)

f.close()
