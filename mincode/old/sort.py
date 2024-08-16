import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
#from function import get_plots


""" First create the dataframe from minoutput """
cols = ["temp","mass","helium","hydrogen","sigma"]
data = pd.read_table("minoutput",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float},engine="python")

data = data.sort_values('sigma')

max_val = input()
max_val = int(max_val)

data = data[0:max_val]
data = data.reset_index()

cols = ["temp", "mass", "helium", "hydrogen", "modecs"]
back_data = pd.read_table("../modecs", sep = "    |      |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float}, engine = "python")

sep = " & "

for i in np.arange(0,max_val):
    for j in np.arange(0,len(back_data)):
        sametemp = data.temp[i] == back_data.temp[j]
        samemass = data.mass[i] == back_data.mass[j]
        samehy = data.hydrogen[i] == back_data.hydrogen[j]
        samehe = data.helium[i] == back_data.helium[j]
        if sametemp and samemass and samehy and samehe:
            print(math.trunc(data.temp[i]), sep, "{:.2f}".format(data.mass[i]*0.001), sep, data.hydrogen[i]*0.01, sep, data.helium[i]*0.01, sep, "{:.3f}".format(data.sigma[i]), sep, back_data.modecs[j], " \\\\")
            #print(back_data.modecs[j])


