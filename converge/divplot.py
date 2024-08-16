import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np


""" First create the dataframe from minoutput """
cols = ["temp","mass","helium","hydrogen"]
data = pd.read_table("diverging",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4],dtype={'temp':float},engine="python")

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

print(max(data.temp))



##########PLOTTING############3
color_map = plt.cm.get_cmap('hot_r')
reversed_color_map = color_map.reversed()

plt.figure(300, figsize=(12,10))
plt.subplot(1,2,1)
plt.scatter(data.helium, data.hydrogen)
plt.xlim(125,425)
plt.ylim(375,975)
plt.subplot(2,2,2)
plt.scatter(data.mass, data.hydrogen)
plt.subplot(2,2,4)
plt.scatter(data.mass, data.helium)

plt.show()



'''
plt.figure(200, figsize=(6,5))
#ax = fig.subplots(1,1,1)
plt.rcParams['axes.facecolor']='white'
plt.scatter(temps,masses,c=freq,cmap = color_map,  marker = 's')
#ax = plt.gca()
#ax.set_facecolor('black')
plt.xlabel("Temperature (K)")
plt.xlim([10570,12620])
plt.gca().invert_xaxis()
#plt.xticks(np.arange(12600,10800,200))
plt.ylabel("Mass ($M_\odot$ * 1000)")
plt.ylim(465,975)
cbar = plt.colorbar()
cbar.set_label("# of Converging models in grid")
#plt.plot(temps[max_index], masses[max_index],'r.')
#plt.text(11000,450, 'Red point is global maximum', fontsize = 10)
#plt.text(10500,1025, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
plt.show()
'''
