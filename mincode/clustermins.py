'''
Written by Weston Hall
03-30-2022

clustermins.py
To be used in conjunction with program matchstick and ajusteh

Takes "minoutput" from matchstick output and identifies
families of solutions. Instead of saving to file, it displays
to screen.

To be used in bash shell wrapper, where output is saved as:
    python3 clustermins.py $STAR > ../results/$STAR
and STAR is the name of the star period file used for ajusteh
'''
import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import sys


""" First create the dataframe from minoutput """
cols = ["temp","mass","helium","hydrogen","sigma"]
data = pd.read_table("minoutput",sep = "   |    |\t", 
        header = None, names = cols, 
        usecols = [0,1,3,4,5],
        dtype={'temp':float},engine="python")


"""Get number of periods"""
file = open("../star/" + sys.argv[1])
star = file.read()
peri=len(star.split())/2

line = []
family = []
sigma = []

""" Loop through each family """
for hydro in np.arange(400,950,25):
    for helio in np.arange(150,400,25):
        #temp=temporary in this case not temperature
        temp = data[(data["hydrogen"] == hydro) & (data["helium"] == helio)]
        if(len(temp) >0):
            #sort by lowest sigma
            temp = temp.sort_values("sigma")
            temp = temp.reset_index()
            #print(temp.head(1))  #debugging
            #take first in row
            line.append(str(temp.temp[0]) + " & " + 
                    str("{:.3f}".format(0.001*temp.mass[0])) + " & " + 
                    str(temp.hydrogen[0]) + " "+ str(temp.helium[0]) + 
                    " & " + str(temp.sigma[0]) + " & ")
            family.append(int(len(temp)))
            sigma.append(temp.sigma[0])
            #print(str(temp.temp[0]) + " & " + str("{:.2f}".format(0.001*temp.mass[0])) + " & " + str(temp.hydrogen[0]) + " "+ str(temp.helium[0]) + " & " + str(temp.sigma[0]) + " & " + str(len(temp)) + " & " + str(peri))

#debugging
#print(np.mean(family))
#print(np.mean(family) - np.std(family))

#print(line[0], sigma[0], family[0])
line = [x for _, x in sorted(zip(sigma, line))]
family = [x for _, x in sorted(zip(sigma, family))]
sigma.sort()
#print(line[0], sigma[0], family[0])

#If family membership is above 1std less than mean, print to screen
#print(np.mean(family), np.std(family))
for i in np.arange(0,len(line)):
    if family[i] > np.mean(family) - np.std(family):
        print(line[i], family[i], "&", peri)

#plt.figure(100)
#plt.hist(family, bins=20)
#plt.show()


