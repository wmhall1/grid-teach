import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import functions as fn

stars = fn.get_spec_K2("spec")

if len(sys.argv) > 1:
    filename = sys.argv[1] 
else:
    filename = "weston_ast_adj"

westo = fn.get_adj(filename)
print(westo)
table = open('table','w')
for i in np.arange(0, len(westo)):
    f = open("../outputs/"+westo.name[i]+"_final.mode", "r")
    lines = f.readlines()
    #df = pd.read_table("../outputs/"+westo.name[i]+"_final.mode", sep = "   |    |     ", header=None, usecols =[0,1,3,4,5], names = ["temp", "mass", "he", "h", "modes"], dtype={'temp':float,'mass':float,'he':float,'h':float,"modes":str}, engine= "python")
    #temp_df = df[(abs(df["temp"]- westo["temp"][i]) < 0.00001) & (abs(df["mass"] *0.001 - westo["mass"][i]) < 0.00001) & (abs(df["h"] *0.01 -westo["h"][i]) < 0.00001) & (abs(df["he"] *0.01 - westo["he"][i]) < 0.00001)]
    #print(temp_df)
    print(westo.name[i])
    for l in np.arange(0,len(lines)):
        ttemp = float(lines[l][0:7])
        tmass = float(lines[l][10:16])
        the = float(lines[l][29:34])
        th = float(lines[l][38:43])
        if abs(ttemp - westo.temp[i]) < 0.0000001 and abs(tmass - westo.mass[i]*1000) < 0.0000001 and abs(the - westo.he[i]*100) < 0.000001 and abs(th - westo.h[i]*100) < 0.000001:
            print(ttemp, tmass, the, th)
            print(westo.temp[i], westo.mass[i]*1000, westo.he[i]*100, westo.h[i]*100)
            table.write(str(westo.name[i]) + " & " + str(westo.temp[i]) + " & " + str("{:.3f}".format(westo.mass[i])) + " & " + str("{:.2f}".format(westo.h[i])) + " & " + str("{:.2f}".format(westo.he[i])) + " & " + str(westo.S[i]) + " & "+  lines[l][49:-1] + " \\\\ \n")

    #print(lines[0][0:7])
    #print(lines[0][11:16])
    #print(lines[0][29:34])
    #print(lines[0][38:43])
    #print(lines[0][49:])
