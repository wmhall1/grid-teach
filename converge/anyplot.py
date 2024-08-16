import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math
import sys
import pandas as pd
import numpy as np


""" First create the dataframe from minoutput """
#cols = ["temp","mass","env","helium","hydrogen","sigma","prob"]
#data = pd.read_csv("../minoutput", header = None, names = cols, sep ="   |    |\t", engine="python")
cols = ["temp","mass","helium","hydrogen"]
data = pd.read_table("diverging",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4],dtype={'temp':float},engine="python")


#Get minimum sigma and index
#print(data.mass)
#print(data.temp)
#min_value = min(data.sigma)
#sigmas = data.sigma.tolist()
#print(type(sigmas))
#min_index = sigmas.index(min_value)


""" USER INPUT X AXIS """
x_axis = input("Input x-axis: ")
if x_axis == "temp":
    x_axis_index = 0
    x_label = "Temperature (K)"
elif x_axis == "mass":
    x_axis_index = 1
    x_label = "Mass ($M_\odot$ * 1000)"
elif x_axis == "helium" or x_axis == "he":
    x_axis_index = 2
    x_axis = "helium"
    x_label = "-log(He mass ($M_\odot$)) * 1000"
elif x_axis == "hydrogen" or x_axis == "h":
    x_axis_index = 3
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
    y_axis_index = 2
    y_axis = "helium"
    y_label = "-log(He mass ($M_\odot$)) * 1000"
elif y_axis == "hydrogen" or y_axis == "h":
    y_axis_index = 3
    y_axis = "hydrogen"
    y_label = "-log(H mass ($M_\odot$)) * 1000"
else:
    print("invalid entry")
    exit()

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
"""
sigmas = [ [] for _ in range(len(x_axis_list)) ]

for i in range(0,len(sigmas)):
    sigmas[i] = sorted_data.sigma[ (sorted_data[x_axis] == x_axis_list[i]) & (sorted_data[y_axis] == y_axis_list[i]) ].tolist()

#print(sigmas)

#Create a new list of just the minimums
sigma_mins = []
for s in sigmas:
    sigma_mins.append(min(s))
"""
#color_map = plt.cm.get_cmap('viridis')
#reversed_color_map = color_map.reversed()
color_map = plt.cm.get_cmap('hot_r')
reversed_color_map = color_map.reversed()

#colors1 = plt.cm.ocean(np.linspace(0.2, 1, 100))
colors1 = plt.cm.bone(np.linspace(0, 1, 80))
colors2 = plt.cm.hot_r(np.linspace(0.6, 1, 176))
#colors1 = colors1.reversed()


# combine them and build a new colormap
colors = np.vstack((colors2, colors1))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)



""" PLOT YOUR AXES """
"""
plt.figure(100, figsize=(8,6))
plt.scatter(x_axis_list, y_axis_list, cmap = reversed_color_map, c=sigma_mins, marker='s')
plt.xlabel(x_label)
plt.ylabel(y_label)
if x_axis == "temp":
    plt.gca().invert_xaxis()
#plt.ylim(500,1000)
cbar = plt.colorbar()
cbar.set_label("Minimum Sigma")
#plt.plot(data.helium[hmax_index],data.hydrogen[hmax_index],'r.')
plt.text(-20,-20, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
#plt.text(12800,475, 'Red point is global minimum', fontsize = 10)
plt.show()
"""
if x_axis_index + y_axis_index == 5:
    size = 300
    if x_axis_index > y_axis_index:
        fig_x = 9.5
        fig_y = 3.5
    else:
        fig_x=4.3
        fig_y=7.75
else:
    size = 100
    fig_x = 8
    fig_y = 6


freq_rate = [ (100 - i/600*100) for i in freq ]
#freq_rate = [ i for i in freq ]

plt.figure(200, figsize=(fig_x,fig_y))
plt.scatter(x_axis_list, y_axis_list, cmap = mymap, s = size, c = freq_rate, marker = 's', vmin = 0, vmax = 100)
plt.xlabel(x_label)
plt.ylabel(y_label)
if x_axis == "temp":
    plt.gca().invert_xaxis()
cbar = plt.colorbar()
cbar.set_label("% of models diverging")
plt.show()
##########################################################################################

