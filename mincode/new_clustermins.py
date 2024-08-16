'''
Does clustermins but with modecs for tabling
'''

import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import sys
#from function import get_plots


""" First create the dataframe from minoutput """
cols = ["temp","mass","helium","hydrogen","sigma"]
data = pd.read_table("minoutput",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float},engine="python")


cols = ["temp", "mass", "helium", "hydrogen", "modecs"]
back_data = pd.read_table("../modecs", sep = "    |   |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float, 'mass':float, 'helium':float, 'hydrogen':float, 'modecs':str}, engine="python")
#for mass in back_data["mass"]:
    #print(mass)
#print(back_data)

#print(data[(data["hydrogen"] == 600) & (data["helium"] == 200)])

"""Get number of periods"""
file = open("../star/" + sys.argv[1])
star = file.read()
peri=len(star.split())/2

temps = []
masses = []
hydros = []
helios = []
modecs = []
sigmas = []

line = []
family = []


for hydro in np.arange(400,950,25):
    for helio in np.arange(150,400,25):
        temp = data[(data["hydrogen"] == hydro) & (data["helium"] == helio)]
        if temp.empty == False:
            temp = temp.sort_values("sigma")
            temp = temp.reset_index()
            #print(temp)
            
            '''
            temps.append(temp.temp[0])
            masses.append(str("{:.2f}".format(0.001*temp.mass[0])))
            hydros.append(temp.hydrogen[0])
            helios.append(temp.helium[0])
            sigmas.append(temp.sigma[0])
            '''

            temp_modecs = back_data[(back_data["temp"] == temp['temp'][0]) & (back_data["mass"] == temp['mass'][0]) & (back_data["hydrogen"] == temp['hydrogen'][0]) & (back_data["helium"] == temp['helium'][0])]
            temp_modecs = temp_modecs.reset_index()
            #print(temp_modecs)
            #if(len(temp_modecs.modecs[0]) > 0):
            modecs.append(temp_modecs['modecs'][0])
            #print(temp_modecs)
            sigmas.append(temp.sigma[0])

            '''
            for j in np.arange(0,len(back_data)):
                sametemp = temp.temp[0] == back_data.temp[j]
                samemass = temp.mass[0] == back_data.mass[j]
                samehy = temp.hydrogen[0] == back_data.hydrogen[j]
                samehe = temp.helium[0] == back_data.helium[j]
                if sametemp and samemass and samehy and samehe:
                    modecs.append(back_data.modecs[j])
                    #print(math.trunc(data.temp[i]), sep, "{:.2f}".format(data.mass[i]*0.001), sep, data.hydrogen[i]*0.01, sep, data.helium[i]*0.01, sep, "{:.3f}".format(data.sigma[i]), sep, back_data.modecs[j], " \\\\")
            '''

            line.append(str("{:.0f}".format(temp.temp[0])) + " & " + str("{:.3f}".format(0.001*temp.mass[0])) + " & " + str("{:.2f}".format(0.01*temp.hydrogen[0])) + " & "+ str("{:.2f}".format(0.01*temp.helium[0])) + " & " + str(temp.sigma[0]) + " & " + temp_modecs.modecs[0] + " \\\\")
            family.append(int(len(temp)))
            
            #print(str("{:.0f}".format(temp.temp[0])) + " & " + str("{:.2f}".format(0.001*temp.mass[0])) + " & " + str("{:.1f}".format(0.01*temp.hydrogen[0])) + " & "+ str("{:.1f}".format(0.01*temp.helium[0])) + " & " + str(temp.sigma[0]) + " & " + temp_modecs.modecs[0] + " \\\\")

line = [x for _, x in sorted(zip(sigmas, line))]
family = [x for _, x in sorted(zip(sigmas, family))]
sigmas.sort()

for i in np.arange(0,len(line)):
    if family[i] > np.mean(family) - np.std(family):
        print(line[i])

#print(temps)
#print(back_data.head())
