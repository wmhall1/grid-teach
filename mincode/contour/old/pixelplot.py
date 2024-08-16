import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np


""" First create the dataframe from minoutput """
cols = ["temp","mass","env","helium","hydrogen","sigma","prob"]
data = pd.read_csv("minoutput", header = None, names = cols, sep ="    |\t", engine="python")

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
temps.append(data.temp[0])
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
        temps.append(data.temp[i])
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


""" PLOTTING """
color_map = plt.cm.get_cmap('viridis')
reversed_color_map = color_map.reversed()


arr=np.array(temps,masses)

plt.figure(300, figsize=(8,6))
plt.imshow(arr)
