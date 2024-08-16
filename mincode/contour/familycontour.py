# Written by Weston Hall
# Makes the usual plots you will want
# Used in scripts

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

save = False
ifilename = "../minoutput"
nameit = False
name = False

""" READ ARGUMENTS """
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg == 's':
            save = True
            filename = sys.argv[sys.argv.index('s') + 1]
        if arg == 'n':
            name = True
        if arg == 'f':
            ifilename = "../minoutput_f"
            if save == True:
                filename = filename + "_f"
        if arg == 'l':
            nameit = True
            if save:
                perfile = filename
            else:
                perfile = sys.argv[sys.argv.index('l') + 1]
    """
    if sys.argv[1] == 's':
        save = True
        filename = "../../results/" + sys.argv[2]
    elif sys.argv[1] == 'n':
        ifilename = "../minoutput_n"
    """

""" First create the dataframe from minoutput """
cols = ["temp","mass","helium","hydrogen","sigma"]
data = pd.read_table(ifilename,sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float},engine="python")


#print(data.sigma)
max_S = max(data.sigma)

#threedee = input("3D plots (Y/N):")
threedee = "n"
if threedee == "y" or threedee == "Y":
    threedee = True
else:
    threedee = False


""" SELECT A H/HE """
selection = input("Select hydrogen(1) or helium(2) or Split (3) or  all(else)")
hyd = False
alt = False

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

#get minimum sigma and index
min_value = min(data.sigma)
sigmas = data.sigma.tolist()
min_index = sigmas.index(min_value)

[temps, masses, sigma_mins] = get_plots(data)


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

""" GETTING PERIODS """
if nameit:
    periods = pd.read_table("../../star/" + perfile, sep= ' ',  header = None, names = ["Period", "Weight"], engine = "python")
    #print(periods)


""" PLOTTING """
color_map = plt.cm.get_cmap('viridis')
reversed_color_map = color_map.reversed()
ranger = [12600,12400,12200,12000,11800,11600,11400,11200,11000,10800,10600]

plt.rc('font', size=10)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=10)    # legend fontsize
plt.rc('figure', titlesize=16)  # fontsize of the figure title

#print(max(temps))
#print(type(temps[1]))


[int_temp_err, int_mass_err] = get_unc(data, min_index) 
'''
print("Min Sig: ", data.temp[min_index], data.mass[min_index])
print("Between", data.temp[min_index]+ int_temp_err[0], "and", data.temp[min_index]-int_temp_err[1])
print("and", int_mass_err)
'''
if nameit:
    y = (1 + len(periods.index)/25)*5
    y = 6
    frac = 0.8
    if len(periods.index) > 7:
        y = 6
        frac = 0.7
else:
    y = 5

plt.figure(100, figsize=(6,y))

if nameit:
    x = 6
    #mpl.rc('text', usetex=True)
    col_labels=periods.columns
    row_labels=[i+1 for i in periods.index] 
    table_vals=periods.values
    the_table = plt.table(cellText=table_vals,
                  colWidths = [0.45]*3,
                  rowLabels=row_labels,
                  colLabels=col_labels,
                  loc = "top")
                  #bbox = [12650, 1000, 500 , 100])
    #plt.text(12,3.4,'Table Title',size=8)
    plt.subplots_adjust(top = frac)
else:
    x = 6

#plt.figure(100, figsize=(x,5))
#if nameit:
#    plt.subplot(1,2,1)
plt.scatter(temps,masses,cmap = reversed_color_map,c=sigma_mins, marker=path)
plt.xlabel("Temperature (K)")
plt.xlim([10550,12650])
plt.gca().invert_xaxis()
plt.ylabel("Mass ($M_\odot$ * 1000)")
plt.ylim(465,975)
plt.clim(0,max_S)
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.plot(data.temp[min_index],data.mass[min_index],'r.')
plt.errorbar(data.temp[min_index], data.mass[min_index],capsize = 5, ecolor = 'r', yerr = int_mass_err, xerr = int_temp_err)
plt.text(10500,995, 'S cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
if alt == True:
    alt = True
    #plt.text(11000,420, 'Red point is global minimum', fontsize = 10)
elif hyd == True:
    plt.text(11900,980, 'Hydrogen level = ' +str(float(hydro)*-0.01), fontsize = 12)
else:
    plt.text(11900,980, 'Helium level = '+str(float(helio)*-0.01),fontsize =12)

"""
if nameit:
    #plt.title(perfile)
    col_labels=periods.columns
    row_labels=periods.index
    table_vals=periods.values
    the_table = plt.table(cellText=table_vals,
                  colWidths = [0.1]*3,
                  rowLabels=row_labels,
                  colLabels=col_labels,
                  loc = "top left")
                  #bbox = [12650, 1000, 500 , 100])
    plt.text(12,3.4,'Table Title',size=8)
    #plt.subplot(1,2,2)
    #plt.table(cellText=periods.values, colLabels=periods.columns, loc='center')
"""

if name == True:
    plt.text(12550,950,filename, fontsize=10)

if save == True:
    plt.savefig("../../results/" + filename)
else:
    #plt.title(filename)
    plt.show()

'''
plt.figure(200, figsize=(8,6))
plt.scatter(temps,masses,c=freq, marker = path)
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
plt.text(10500,1025, 'Sigma cutoff = '+str(math.ceil(max(data.sigma * 100)) / 100), fontsize = 10)
#plt.show()
'''

## 3D Plotting
'''
ax = plt.axes(projection = '3d')
ax.scatter3D(data.temp,data.mass,data.hydrogen, c = data.sigma)
ax.set_xlabel("Temperature (K)")
ax.set_ylabel("Mass ($M_\odot$ * 1000)")
ax.set_zlabel('Hydrogen mass')
#ax.colorbar()
#ax.xlim([10550,12650])
#ax.gca().invert_xaxis()
if threedee == True:
    plt.show()

'''
'''
print("Min Sig: ", data.temp[min_index], data.mass[min_index])
print("Between", int_temp_err)
print("and", int_mass_err)
'''
#print("Max Freq: ", temps[max_index], masses[max_index])
