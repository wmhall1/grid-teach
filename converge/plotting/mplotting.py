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

with open("output") as f:
    lines = f.readlines()

total = 0
titles = []
mh = []
m =[]
p1 = []
p2 = []
p3 = []
p4 = []
p5 = []

#userTemp = input("Plot Temp (K): ")
userTemp = input("Temp K (ex: 12000): ")
userMassHe = input("Helium mass -log (ex. 2, 4): ")
userMassH = input("Hydrogen mass -log: ")
title = "log($M_{H}$/$M_o$) = -" + str(userMassH) + ", T = " + str(userTemp) + "$M_o$, log($M_{He}$/$M_o$) = -" + str(userMassHe) 

userTemp = float(userTemp)
userMassHe = float(userMassHe) * 100
userMassH = float(userMassH) * 100

if debug:
    print(userMassH)
    print(userTemp)
    print(userMassHe)

linenumber = 0
for line in lines:
    temp = mass = massh = masshe = 0
    if line[0:3] == "  1":
        temp = float(line[2:8])
        mass = float(line[12:17])
        masshe = float(line[30:35])
        massh = float(line[39:44])
    if massh == float(userMassH) and temp == float(userTemp) and masshe == float(userMassHe):
        total = total+1
        titles.append(linenumber)
        m.append(float(mass))
        if debug:
            print(temp)
            print(mass)
            print(massh)
            print(masshe)
            print(lines[linenumber+1])
    linenumber = linenumber +1

switch = False
switch2 = False
num = 0
for index in titles:
    #mh.append(float(lines[index][40:45])/100)
    l = float(lines[index+1][11:12])
   
    
    if num > 5 and switch == False and p1[num-1] != 0 and p1[num-1] < float(lines[index+1][15:23]):
        switch = True
        print('switched1')
    if switch == True and float(lines[index+1][15:23]) > p2[num-1] and switch2 == False:
        switch2 = True
        print("switched")
        
    if(l == 1.0):
        if switch2 == True:
            p3.append(float(lines[index+1][15:23]))
            p4.append(float(lines[index+2][15:23]))
            p5.append(float(lines[index+3][15:23]))
        elif switch == True:
            p2.append(float(lines[index+1][15:23]))
            p3.append(float(lines[index+2][15:23]))
            p4.append(float(lines[index+3][15:23]))
            p5.append(float(lines[index+4][15:23]))
        else:
            p1.append(float(lines[index+1][15:23]))
            p2.append(float(lines[index+2][15:23]))
            p3.append(float(lines[index+3][15:23]))
            p4.append(float(lines[index+4][15:23]))
            p5.append(float(lines[index+5][15:23]))

        """
        if switch != True and switch2 != True:
            p1.append(float(lines[index+1][15:23]))
            p2.append(float(lines[index+2][15:23]))
            p3.append(float(lines[index+3][15:23]))
            p4.append(float(lines[index+4][15:23]))
            p5.append(float(lines[index+5][15:23]))
        elif switch2 == True:
            p3.append(float(lines[index+1][15:23]))
            p4.append(float(lines[index+1][15:23]))
            p5.append(float(lines[index+1][15:23]))
        else:
            p2.append(float(lines[index+1][15:23]))
            pp1.append(float(lines[index+1][15:23]))
            p2.append(float(lines[index+2][15:23]))
            p3.append(float(lines[index+3][15:23]))
            p4.append(float(lines[index+4][15:23]))
            p5.append(float(lines[index+5][15:23]))3.append(float(lines[index+2][15:23]))
            p4.append(float(lines[index+3][15:23]))
            p5.append(float(lines[index+4][15:23]))
        """
    else:
        m.remove(m[len(p1)-1])
            
    
    num = len(p2)


print(p2)


m = [element * 0.001 for element in m]

p1 = [i for _,i in sorted(zip(m,p1))]
p2 = [i for _,i in sorted(zip(m,p2))]
p3 = [i for _,i in sorted(zip(m,p3))]
p4 = [i for _,i in sorted(zip(m,p4))]


#print(m)


plt.figure(100)
plt.plot(m[0:len(p1)],p1,"-", label = "k = 1")
plt.plot(m[0:len(p2)],p2,"--", label = "k = 2")
plt.plot(m,p3,"-.", label = "k = 3")
plt.plot(m,p4,":", label = "k = 4")
plt.ylabel("Period (s)")
plt.xlabel("Mass ($M/M_\odot$)")
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
