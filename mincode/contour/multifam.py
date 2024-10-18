# Written by Weston Hall
# Makes comparison plots for different He, H



import matplotlib.pyplot as plt
from matplotlib.path import Path
import math
import sys
import pandas as pd
import numpy as np
from function import get_plots
from function import get_unc

""" First create the dataframe from minoutput """
cols = ["temp","mass","helium","hydrogen","sigma"]
data = pd.read_table("../minoutput",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float},engine="python")

max_S = round(max(data.sigma))

#print(data.temp)

#Streamlined, removed this section
'''
""" SELECT A H/HE """
selection = input("Select hydrogen(1) or helium(2) or Split (3) or  all(else)")
'''
hyd = False
alt = False

selection = '1'
'''
if selection == "hy" or selection == "1" or selection == "hydrogen":
    print("Hydrogen Level", min(data.hydrogen), "to", max(data.hydrogen), ":")
    hydro = input()
    data = data.loc[data['hydrogen'] == float(hydro)]
    data = data.reset_index()
    hyd = True
elif selection == "he" or selection == "2" or selection == "helium":
    print("Helium Level", min(data.helium), "to", max(data.helium), ":")
    helio = input()
    data = data.loc[data['helium'] == float(helio)]
    data = data.reset_index()
elif selection == "Splitting" or selection == "3":
    print("Select Hydrogen level", min(data.hydrogen), "to", max(data.hydrogen), ":")
    hydro = input()
    print("Select Helium level", min(data.helium), "to", min(data.helium), ":")
    helio = input()
    data = data.loc[data['hydrogen'] == float(hydro)]
    data = data.reset_index()
    data = data.loc[data['helium'] == float(helio)]
    data = data.reset_index()
else:
    alt = True
'''
#
# Get user input for what levels to plot from and retrieve that data from the DataFrame
#
print("Hydrogen Level", min(data.hydrogen), "to", max(data.hydrogen), ":")
hydro = input()
data = data.loc[data['hydrogen'] == float(hydro)]
data = data.reset_index()
hyd = True

he_1 = input("Helium 1: ")
he_2 = input("Helium 2: ")

#
# Retrieve data
#
data_1 = data.loc[data['helium'] == float(he_1)]
data_1 = data_1.reset_index()

data_2 = data.loc[data['helium'] == float(he_2)]
data_2 = data_2.reset_index()

data_3 = data.loc[data['helium'] != float(he_1)]
data_3 = data_3.loc[data['helium'] != float(he_2)]
data_3 = data_3.reset_index()

#
# Calculate minimum sigma and find its location
#
min_value_1 = min(data_1.sigma)
sigmas_1 = data_1.sigma.tolist()
min_index_1 = sigmas_1.index(min_value_1)

min_value_2 = min(data_2.sigma)
sigmas_2 = data_2.sigma.tolist()
min_index_2 = sigmas_2.index(min_value_2)

#
#Flatten the data for plotting, acquire uncertainties for minimums
#
[temps1, masses1, sigma_mins1] = get_plots(data_1)
[temps2, masses2, sigma_mins2] = get_plots(data_2)
[int_temp_err_1, int_mass_err_1] = get_unc(data_1, min_index_1)
[int_temp_err_2, int_mass_err_2] = get_unc(data_2, min_index_2)

[temps3, masses3, sigma_mins3] = get_plots(data_3)


####MARKER#############
verts = [
    (10,-4), #lower right
    (-10,-4), #lower left
    (-10,4), #upper left
    (10,4), #upper right
    (10,-4), #lower right
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

#Set up color maps (this is probably going to give a warning)
color_map = plt.cm.get_cmap('winter_r')

color_map2 = plt.cm.get_cmap('autumn_r')

color_map3 = plt.cm.get_cmap('binary_r')

#
#Plot settings
#
plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize
plt.rc('figure', titlesize=16)  # fontsize of the figure title

s_val = 40

#Initialize
plt.figure(100, figsize=(8,6))

#
#Scatter the background in grey
#
pc = plt.scatter(temps3,masses3,cmap = color_map3, c=sigma_mins3,s=s_val, marker =path)
#cbc = plt.colorbar(pc)
plt.clim(0,max_S)

#
# Scatter the first choice in blue
#
pa = plt.scatter(temps1,masses1,cmap = color_map,  c=sigma_mins1, s=s_val, marker=path)
cba = plt.colorbar(pa)
plt.clim(0,max_S)
cba.set_label("S Value for $-log(M_{He})=$"+str(float(he_1)/100), fontsize = 15)
#cba.ax.tick_params(labelsize=10)

#
# Scatter the second choice in red
#
pb = plt.scatter(temps2,masses2,cmap = color_map2, c=sigma_mins2, s=s_val, marker=path)
cbb = plt.colorbar(pb)
plt.clim(0,max_S)
cbb.set_label("S Value for $-log(M_{He})=$ "+str(float(he_2)/100), fontsize = 15)

#Axes options
plt.xlabel("Temperature (K)")
plt.xlim([10550,12650])
plt.gca().invert_xaxis()

plt.ylabel("Mass ($M_\odot$ * 1000)")
plt.ylim(465,975)

#Add the minimums for each family
plt.plot(data_1.temp[min_index_1],data_1.mass[min_index_1],'b.')
plt.errorbar(data_1.temp[min_index_1], data_1.mass[min_index_1],capsize = 5, ecolor = 'k', yerr = int_mass_err_1, xerr = int_temp_err_1)

plt.plot(data_2.temp[min_index_2],data_2.mass[min_index_2],'r.')
plt.errorbar(data_2.temp[min_index_2], data_2.mass[min_index_2],capsize = 5, ecolor = 'k', yerr = int_mass_err_2, xerr = int_temp_err_2)


#Add some descriptive text
#plt.text(10250,985, 'S cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 12)
if alt == True:
    plt.text(11000,420, 'Red point is global minimum', fontsize = 10)
elif hyd == True:
    plt.text(11900,980, '$log(M_H)$ = ' +str(float(hydro)*-0.01), fontsize = 12)
else:
    plt.text(11000,405, 'Helium level = '+str(float(helio)*-0.01),fontsize =12)

plt.text(12500, 950, '$log(M_{He})$ = '+str(float(he_1)*-0.01), fontsize = 10, color = 'blue')
plt.text(12500, 925, '$log(M_{He})$ = '+str(float(he_2)*-0.01), fontsize = 10, color = 'red')
plt.show()

'''
plt.figure(200, figsize=(8,6))
plt.scatter(temps,masses,c=freq, marker = path)
plt.xlabel("Temperature (K)")
plt.xlim([10550,140])
plt.gca().invert_xaxis()
#plt.xticks(np.arange(12600,10800,200))
plt.ylabel("Mass ($M_\odot$ * 1000)")
plt.ylim(495,1005)
cbar = plt.colorbar()
cbar.set_label("Frequency Value")
plt.plot(temps[max_index], masses[max_index],'r.')
plt.text(11000,450, 'Red point is global maximum', fontsize = 10)
plt.text(10500,1025, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
#plt.show()
'''


# This has deprecated, but left in cause the errors it can cause are useful to know about
## 3D Plotting
ax = plt.axes(projection = '3d')
ax.scatter3D(data.temp,data.mass,data.hydrogen, c = data.sigma)
ax.set_xlabel("Temperature (K)")
ax.set_ylabel("Mass ($M_\odot$ * 1000)")
ax.set_zlabel('Hydrogen mass')
#ax.colorbar()
#ax.xlim([10550,140])
#ax.gca().invert_xaxis()
#plt.show()


#print("Min Sig: ", data.temp[min_index], data.mass[min_index])
#print("Max Freq: ", temps[max_index], masses[max_index])

