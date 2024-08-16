import matplotlib.pyplot as plt
from matplotlib.path import Path
import math
import sys
import pandas as pd
import numpy as np
from function import get_layer_unc
from function import get_plots

""" First create the dataframe from minoutput """
cols = ["temp","mass","env","helium","hydrogen","sigma","prob"]
data = pd.read_csv("../minoutput", header = None, names = cols, sep ="   |    |\t", engine="python")

print(min(data["mass"]), max(data["mass"]))
mass_sel = float(input("Select mass: "))

#print(data)

data = data[data["mass"] == mass_sel]
data = data.reset_index()

#print(data)

#Get minimum sigma and index
#print(data.mass)
#print(data.temp)
min_value = min(data.sigma)
sigmas = data.sigma.tolist()
#print(type(sigmas))
min_index = sigmas.index(min_value)


""" USER INPUT X AXIS """
'''
x_axis = input("Input x-axis: ")
if x_axis == "temp":
    x_axis_index = 0
    x_label = "Temperature (K)"
elif x_axis == "mass":
    x_axis_index = 1
    x_label = "Mass ($M_\odot$ * 1000)"
elif x_axis == "helium" or x_axis == "he":
    x_axis_index = 3
    x_axis = "helium"
    x_label = "-log(He mass ($M_\odot$)) * 1000"
elif x_axis == "hydrogen" or x_axis == "h":
    x_axis_index = 4
    x_axis = "hydrogen"
    x_label = "-log(H mass ($M_\odot$)) * 1000"
else:
    print("invalid entry")
    exit()

""" USER INPUT Y AXIS """
y_axis = input("Input y-axis: ")
if y_axis == "temp":
    y_axis_index = 0
    y_label = "Temperature (K)"
elif y_axis == "mass":
    y_axis_index = 1
    y_label = "Mass ($M_\odot$ * 1000)"
elif y_axis == "helium" or y_axis == "he":
    y_axis_index = 3
    y_axis = "helium"
    y_label = "-log(He mass ($M_\odot$)) * 1000"
elif y_axis == "hydrogen" or y_axis == "h":
    y_axis_index = 4
    y_axis = "hydrogen"
    y_label = "-log(H mass ($M_\odot$)) * 1000"
else:
    print("invalid entry")
    exit()
'''
x_axis_index = 4
x_axis = "hydrogen"
x_label = "-log(H mass ($M_\odot$)) * 1000"

y_axis_index = 3
y_axis = "helium"
y_label = "-log(He mass ($M_\odot$)) * 1000"

""" SORT THE DATA """
sorted_data = data.sort_values([x_axis, y_axis])

sorted_x_axis=sorted_data[x_axis].tolist()
sorted_y_axis=sorted_data[y_axis].tolist()

""" MAKE THE PLOTTING LISTS """
x_axis_list = []
y_axis_list = []
freq = []
x_axis_list.append(sorted_x_axis[0])
y_axis_list.append(sorted_y_axis[0])
freq.append(1)

j = 1
for i in range(1,len(sorted_x_axis)):
    if sorted_x_axis[i] == x_axis_list[j - 1] and sorted_y_axis[i] == y_axis_list[j - 1]:
        freq[j - 1] = freq[j - 1] + 1
    else:
        x_axis_list.append(sorted_x_axis[i])
        y_axis_list.append(sorted_y_axis[i])
        freq.append(1)
        j = j + 1
#print(x_axis_list[0:15])
#print(y_axis_list[0:15])
#print(freq[0:15])


""" FIND MINIMUM SIGMAS """
sigmas = [ [] for _ in range(len(x_axis_list)) ]

for i in range(0,len(sigmas)):
    sigmas[i] = sorted_data.sigma[ (sorted_data[x_axis] == x_axis_list[i]) & (sorted_data[y_axis] == y_axis_list[i]) ].tolist()

#print(sigmas)


x_v=22
####MARKER#############
verts = [
    (10,-x_v), #lower right
    (-10,-x_v), #lower left
    (-10,x_v), #upper left
    (10,x_v), #upper right
    (10,-x_v), #lower right
]

codes = [
    Path.MOVETO, #begin the figure in the lower right
    Path.LINETO, #start a 3 point curve with the control point in lower left
    Path.LINETO, #end curve in the upper left
    Path.LINETO, #start a new 3 point curve with the upper right as a control point
    Path.LINETO, #end curve in lower right
]

path = Path(verts,codes)

#Create errors
#min_value = min(data.sigma)
#min_index = data['sigma'].index(min_value)
[int_h_err, int_he_err] = get_layer_unc(data, min_index)

#Create a new list of just the minimums
sigma_mins = []
for s in sigmas:
    sigma_mins.append(min(s))

color_map = plt.cm.get_cmap('viridis')
reversed_color_map = color_map.reversed()

""" PLOT YOUR AXES """
plt.figure(100, figsize=(7.75,6))
plt.scatter(x_axis_list, y_axis_list, cmap = reversed_color_map, c=sigma_mins, marker=path, s = 900)
plt.errorbar(data.hydrogen[min_index], data.helium[min_index],capsize = 5, ecolor = 'k', yerr = int_he_err, xerr = int_h_err)
plt.xlabel(x_label)
plt.ylabel(y_label)
if x_axis == "temp":
    plt.gca().invert_xaxis()
#plt.ylim(500,1000)
plt.xlim(375,975)
cbar = plt.colorbar()
cbar.set_label("Minimum Sigma")
#plt.plot(data.helium[hmax_index],data.hydrogen[hmax_index],'r.')
plt.text(-20,-20, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
#plt.text(12800,475, 'Red point is global minimum', fontsize = 10)
#plt.show()


plt.figure(200, figsize=(7.75,6))
plt.scatter(x_axis_list, y_axis_list, cmap = color_map, c = freq, marker = path, s =900)
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.xlim([375,975])
if x_axis == "temp":
    plt.gca().invert_xaxis()
cbar = plt.colorbar()
cbar.set_label("Frequency")
plt.text(-20,-20, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
plt.show()
##########################################################################################




# OLD CODE


"""

 "" Get frequency (modes) of models with the same mass/temp ""
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

"" Sort by Hydrogen and Helium ""

sorted_data = data.sort_values(['helium','hydrogen'])
sorted_helium_list = sorted_data.helium.tolist()
sorted_hydrogen_list = sorted_data.hydrogen.tolist()
#print(sorted_helium_list[0:15])
#print(sorted_hydrogen_list[0:15])


"" Get same for helium and Hydrogen""
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

#print(heliums[0:15])
#print(hydrogens[0:15])


"" FINDING MINIMUM SIGMAS ""
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

"" Get the min sigmas for hydro helio ""
h_sigmas = [ [] for _ in range(len(heliums)) ]
for i in range(0, len(h_sigmas)):
    h_sigmas[i] = sorted_data.sigma[ (sorted_data["helium"] == heliums[i]) & (sorted_data["hydrogen"] == hydrogens[i]) ].tolist()

h_sigma_mins = []
for s in h_sigmas:
    h_sigma_mins.append(min(s))




#
color_map = plt.cm.get_cmap('viridis')
reversed_color_map = color_map.reversed()

""
#X, Y, Z = plt.grid(data.temp,data.mass,data.sigma)
#plt.scatter(data.temp,data.mass,data.sigma)
plt.figure(100, figsize=(8,6))
#plt.scatter(data.temp,data.mass,c=data.sigma)
plt.scatter(heliums,hydrogens,cmap = reversed_color_map,c=h_sigma_mins, marker='s')
plt.xlabel("-log(Helium Mass)")
#plt.xticks(np.arange(10600,12800,200))
plt.ylabel("-log(Hydrogen Mass)")
#plt.ylim(500,1000)
cbar = plt.colorbar()
cbar.set_label("Minimum Sigma")
#plt.plot(data.helium[hmax_index],data.hydrogen[hmax_index],'r.')
plt.text(-20,-20, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
#plt.text(12800,475, 'Red point is global minimum', fontsize = 10)
plt.show()
"""
