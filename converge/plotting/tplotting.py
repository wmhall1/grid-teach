'''
Weston Hall
09/21/21

  10600.0    500.0    300.0    200.0    400.0     60.0     12.0     12.0     60.0     70.0     70.0     80.0     45.0     45.0     36.0
'''

import matplotlib.pyplot as plt
import sys

if len(sys.argv) > 1:
    debug = True
    print("DEBUGGING MODE: writing output to screen")
else:
    debug = False

with open("../../calcperiods") as f:
    lines = f.readlines()

total = 0
titles = []
mh = []
t =[]
p1 = []
p2 = []
p3 = []
p4 = []
p5 = []

#userTemp = input("Plot Temp (K): ")
userMass = input("Solar masses (ex. 0.6): ")
userMassHe = input("Helium mass -log (ex. 2, 4): ")
userMassH = input("Hydrogen mass -log: ")
title = "log($M_{H}$/$M_o$) = -" + str(userMassH) + ", M = " + str(userMass) + "$M_o$, log($M_{He}$/$M_o$) = -" + str(userMassHe) 

userMass = float(userMass) * 1000
userMassHe = float(userMassHe) * 100
userMassH = float(userMassH) * 100

if debug:
    print(userMassH)
    print(userMass)
    print(userMassHe)

linenumber = 0
for line in lines:
    temp = mass = massh = masshe = 0
    if line[0:3] == "  1":
        temp = float(line[2:8])
        mass = float(line[13:17])
        masshe = float(line[30:35])
        massh = float(line[39:44])
    if massh == float(userMassH) and mass == float(userMass) and masshe == float(userMassHe):
        total = total+1
        titles.append(linenumber)
        t.append(temp)
        if debug:
            print(temp)
            print(mass)
            print(massh)
            print(masshe)
    linenumber = linenumber +1


for index in titles:
    #mh.append(float(lines[index][40:45])/100)
    p1.append(float(lines[index+1][15:23]))
    p2.append(float(lines[index+2][15:23]))
    p3.append(float(lines[index+3][15:23]))
    p4.append(float(lines[index+4][15:23]))
    p5.append(float(lines[index+5][15:23]))

zipped_lists = zip(t,p1,p2,p3,p4,p5)
sorted_lists = sorted(zipped_lists)
tuples = zip(*sorted_lists)
t,p1,p2,p3,p4,p5 =(list(q) for q in tuples)




plt.figure(100)
plt.plot(t,p1,'-', label = "k = 1")
plt.plot(t,p2,'--', label = "k = 2")
plt.plot(t,p3,'-.', label = "k = 3")
plt.plot(t,p4,':', label = "k = 4")
plt.gca().invert_xaxis()
plt.ylabel("Period (s)")
plt.xlabel("Temperature (K)")
#plt.title(title)
plt.legend()
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
