import matplotlib.pyplot as plt
from matplotlib.path import Path
import math
import sys
import pandas as pd
import numpy as np


""" First create the dataframe from minoutput """
cols = ["temp","mass","helium","hydrogen","sigma"]
data = pd.read_table("../minoutput",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float},engine="python")


""" SELECT A H/HE
data = data[data['hydrogen'] == 200]
"""


#Get minimum sigma and index
#print(data.mass)
#print(data.temp)
min_value = min(data.sigma)
sigmas = data.sigma.tolist()
#print(type(sigmas))
min_index = sigmas.index(min_value)

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


""" FINDING MINIMUM SIGMAS """
#Initialize a list of lists. For each point, it will store a list of
#the sigmas associated with those points in the dataframe
sigmas = [ [] for _ in range(len(temps)) ]

data_mass = data.mass.tolist()
data_temp = data.temp.tolist()

i = 0
#Assign each list in sigmas to be the list from the dataframe meeting
#the condition for each point
for i in range(0,len(sigmas)):
    sigmas[i] = data.sigma[ (data["mass"] == masses[i]) & (data["temp"] == temps[i]) ].tolist()
#print(sigmas)

#Create a new list of just the minimums
sigma_mins = []
for s in sigmas:
    sigma_mins.append(min(s))
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

""" PLOTTING """
color_map = plt.cm.get_cmap('viridis')
reversed_color_map = color_map.reversed()
ranger = [12600,12400,12200,12000,11800,11600,11400,11200,11000,10800,10600]

plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize
plt.rc('figure', titlesize=16)  # fontsize of the figure title

#print(max(temps))
#print(type(temps[1]))

#X, Y, Z = plt.grid(data.temp,data.mass,data.sigma)
#plt.scatter(data.temp,data.mass,data.sigma)
plt.figure(100, figsize=(8,6))
#plt.scatter(data.temp,data.mass,c=data.sigma)
plt.scatter(temps,masses,cmap = reversed_color_map,c=sigma_mins, marker=path)
plt.xlabel("Temperature (K)")
#plt.xticks(np.arange(float(min(temps)), float(max(temps)),200))
plt.xlim([10550,12650])
plt.gca().invert_xaxis()
#plt.xlim(12600,10800)
#plt.xticks(ranger)
plt.ylabel("Mass ($M_\odot$ * 1000)")
plt.ylim(495,1005)
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.plot(data.temp[min_index],data.mass[min_index],'r.')
plt.text(10500,1025, 'S cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
plt.text(11000,450, 'Red point is global minimum', fontsize = 10)
#plt.show()


plt.figure(200, figsize=(8,6))
plt.scatter(temps,masses,c=freq, marker = 's')
plt.xlabel("Temperature (K)")
plt.xlim([10550,12650])
plt.gca().invert_xaxis()
#plt.xticks(np.arange(12600,10800,200))
plt.ylabel("Mass ($M_\odot$ * 1000)")
plt.ylim(495,1005)
cbar = plt.colorbar()
cbar.set_label("Frequency Value")
plt.plot(temps[max_index], masses[max_index],'r.')
plt.text(11000,450, 'Red point is global maximum', fontsize = 10)
plt.text(10500,1025, 'S cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
plt.show()



print("Min Sig: ", data.temp[min_index], data.mass[min_index])
print("Max Freq: ", temps[max_index], masses[max_index])
"""
plt.figure(100, figsize=(8,6))
#plt.scatter(data.temp,data.mass,c=data.sigma)
plt.scatter(temps,masses, s=[x + 5 for x in freq], cmap = reversed_color_map,c=sigma_mins)
plt.xlabel("Temperature (K)")
plt.gca().invert_xaxis()
#plt.xticks(np.arange(10600,12800,200))
plt.ylabel("Mass ($M_o$ * 1000)")
plt.ylim(500,1000)
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.plot(data.temp[min_index],data.mass[min_index],'r.')
plt.plot(temps[max_index], masses[max_index],'r.')
plt.text(12800,1025, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
plt.text(12800,475, 'Red point is global minimum', fontsize = 10)
plt.show()
"""
