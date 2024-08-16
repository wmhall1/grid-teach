# Written by Weston Hall
# 07-18-2022
# Makes single converging heat map


import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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

#print(max(data.temp))

freq = [ i/max(freq)*100 for i in freq ]


##########PLOTTING############3
color_map = plt.cm.get_cmap('hot_r')
reversed_color_map = color_map.reversed()

#colors1 = plt.cm.ocean(np.linspace(0.2, 1, 100))
colors1 = plt.cm.bone(np.linspace(0, 1, 80))
colors2 = plt.cm.hot_r(np.linspace(0.6, 1, 176))
#colors1 = colors1.reversed()


# combine them and build a new colormap
colors = np.vstack((colors2, colors1))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)

print(colors[0])

plt.figure(200, figsize=(6,5))
#ax = fig.subplots(1,1,1)
plt.rcParams['axes.facecolor']=colors[0]
plt.scatter(temps,masses, c=freq, cmap = mymap, marker='s', vmin = 0, vmax=100)
#plt.scatter(temps,masses,c=freq,cmap = reversed_color_map,  marker = 's', vmin=200, vmax=250)
#plt.clim(150,250)
#ax = plt.gca()
#ax.set_facecolor('black')
plt.xlabel("Temperature (K)")
plt.xlim([10570,12620])
plt.gca().invert_xaxis()
#plt.xticks(np.arange(12600,10800,200))
plt.ylabel("Mass ($M_\odot$ * 1000)")
plt.ylim(465,975)
cbar = plt.colorbar()
cbar.set_label("Percent of models converging in grid")
#plt.clim(0,250)
#plt.plot(temps[max_index], masses[max_index],'r.')
#plt.text(11000,450, 'Red point is global maximum', fontsize = 10)
#plt.text(10500,1025, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
plt.show()
