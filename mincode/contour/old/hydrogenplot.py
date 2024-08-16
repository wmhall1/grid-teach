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

""" Sort by Hydrogen and Helium """

sorted_data = data.sort_values(['helium','hydrogen'])
sorted_helium_list = sorted_data.helium.tolist()
sorted_hydrogen_list = sorted_data.hydrogen.tolist()
print(sorted_helium_list[0:15])
print(sorted_hydrogen_list[0:15])


""" Get same for helium and Hydrogen """
hydrogens = []
heliums = []
hfreq = []
heliums.append(sorted_helium_list[0])
hydrogens.append(sorted_hydrogen_list[0])
hfreq.append(1)
#FOr each row in data frame
j = 1
for i in range(1,len(sorted_data.helium)):
    if sorted_helium_list[i] == heliums[j-1] and sorted_hydrogen_list[i] == hydrogens[j-1]:
        hfreq[j-1] = hfreq[j-1]+1
    else:
        hydrogens.append(sorted_hydrogen_list[i])
        heliums.append(sorted_helium_list[i])
        hfreq.append(1)
        j = j+1
hmax_index = hfreq.index(max(hfreq))

print(heliums[0:15])
print(hydrogens[0:15])


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

""" Get the min sigmas for hydro helio """
h_sigmas = [ [] for _ in range(len(heliums)) ]
for i in range(0, len(h_sigmas)):
    h_sigmas[i] = sorted_data.sigma[ (sorted_data["helium"] == heliums[i]) & (sorted_data["hydrogen"] == hydrogens[i]) ].tolist()

h_sigma_mins = []
for s in h_sigmas:
    h_sigma_mins.append(min(s))




#
color_map = plt.cm.get_cmap('viridis')
reversed_color_map = color_map.reversed()


#X, Y, Z = plt.grid(data.temp,data.mass,data.sigma)
#plt.scatter(data.temp,data.mass,data.sigma)
plt.figure(100, figsize=(8,6))
#plt.scatter(data.temp,data.mass,c=data.sigma)
plt.scatter(heliums,hydrogens,cmap = reversed_color_map,c=h_sigma_mins, marker='s')
plt.xlabel("-log(Helium Mass) * 100")
#plt.xticks(np.arange(10600,12800,200))
plt.ylabel("-log(Hydrogen Mass) * 100")
#plt.ylim(500,1000)
cbar = plt.colorbar()
cbar.set_label("Minimum Sigma")
#plt.plot(data.helium[hmax_index],data.hydrogen[hmax_index],'r.')
plt.text(-20,-20, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
#plt.text(12800,475, 'Red point is global minimum', fontsize = 10)
plt.show()

