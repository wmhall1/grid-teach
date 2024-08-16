# Written by Weston Hall
# 07-18-2022
# Makes a running converging plot with good colors
# for visibility


import matplotlib.pyplot as plt
from matplotlib.path import Path
import math
import sys
import pandas as pd
import numpy as np


""" First create the dataframe from minoutput """
cols = ["temp","mass","helium","hydrogen"]
data = pd.read_table("converging",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4],dtype={'temp':float},engine="python")

""" Get frequency (modes) of models with the same mass/temp """
#initialize lists
temps = []
masses = []
freq = []
temps.append(float(data.temp[0]))
masses.append(data.mass[0])
freq.append(1)

#For each row in the dataframe
j = 1
for i in range(1,len(data.temp)):
    #Check if its the same as previous, if it is then increment the freq for that point
    if data.temp[i] == temps[j-1] and data.mass[i] == masses[j-1]:
        freq[j-1] = freq[j-1] + 1
    #If it isn't the same, add new point, start new freq, and increment
    else:
        temps.append(float(data.temp[i]))
        masses.append(data.mass[i])
        freq.append(1)
        j = j + 1
#find the max frequency
max_index = freq.index(max(freq))
print("{:.2f}".format(len(data.temp) / 1109911 * 100.0), '% Finished')
print("{:.2f}".format(len(temps)/( ((12600-10600)/50) * ((1-0.47)/0.005))*100.0),'% Finished')

####MARKER#############
verts = [
    (10,-3.1), #lower right
    (-10,-3.1), #lower left
    (-10,3.1), #upper left
    (10,3.1), #upper right
    (10,-3.1), #lower right
]

codes = [
    Path.MOVETO, #begin the figure in the lower right
    Path.LINETO, #start a 3 point curve with the control point in lower left
    Path.LINETO, #end curve in the upper left
    Path.LINETO, #start a new 3 point curve with the upper right as a control point
    Path.LINETO, #end curve in lower right
]

path = Path(verts,codes)
x = [10600,10600,10650,10650]
y = [495, 500, 495, 500]
#plt.figure(3)
#plt.scatter(x,y,marker=path,s = 200)


##########PLOTTING############3
color_map = plt.cm.get_cmap('plasma')
reversed_color_map = color_map.reversed()


plt.figure(200, figsize=(6,5))
#ax = fig.add_subplot(111)
plt.scatter(temps,masses,c=freq,cmap = reversed_color_map, marker = path)
plt.xlabel("Temperature (K)")
plt.xlim([10550,12650])
plt.gca().invert_xaxis()
#plt.xticks(np.arange(12600,10800,200))
plt.ylabel("Mass ($M_\odot$ * 1000)")
plt.ylim(465,1005)
cbar = plt.colorbar()
cbar.set_label("# of Converging models in grid")
#plt.plot(temps[max_index], masses[max_index],'r.')
#plt.text(11000,450, 'Red point is global maximum', fontsize = 10)
#plt.text(10500,1025, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
'''
plt.text(10600,470, "1", color = 'r')
plt.text(10800,515, '2', color = 'r')
plt.text(11000,570, '3', color = 'r')
plt.text(11200,615, '4', color = 'r')
plt.text(11400,670, '5', color = 'r')
plt.text(11600,715, '6', color = 'r')
plt.text(11800,770, '7', color = 'r')
plt.text(12000,815, '8', color = 'r')
plt.text(12200,870, '9', color = 'r')
plt.text(12400,915, '10', color = 'r')
'''
#plt.text(10725,480, 'etc', color = 'r')
#plt.text(11325,480, 'etc', color = 'r')

#plt.text(12275,480, '9', color = 'r')
#plt.text(12375,480, '9', color = 'r')

#plt.text(12525,480, '10', color = 'r')
#plt.text(12625,480, '10', color = 'r')

#plt.text(11900,480, '7', color = 'r')

plt.show()
