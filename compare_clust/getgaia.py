import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import functions as fn


def normalize(lst, minimum, maximum):
    if isinstance(lst,float) == True:
        length = 1
        new_lst = (lst-minimum) / (maximum - minimum)
    else:
        new_lst = [(lst[x] - minimum) / (maximum - minimum) for x in np.arange(0,len(lst))]
    #new_listnorm = lstnorm - np.nanmean(lstnorm)
    #new_lst = [(x - min(new_lst)) / (max(new_lst) - min(new_lst)) for x in new_lst]
    return(new_lst)

if len(sys.argv) > 1:
    filename = sys.argv[1]
    print(sys.argv[1])
else:
    filename = 'weston_ast'

#spec = fn.get_spec()
#romero = fn.get_spec_K2("spec")

gaia = pd.read_table("gaia_model_fit",sep = " ", header = None, names = ["ID", "S", "temp", "mass"], dtype={'temp':float,'mass':float})


westo = open(filename,'r')
lines = westo.readlines()

adj = open(filename + '_adj_g','w')


#romero_mass = romero.mass.tolist()
#romero_temp = romero.temp.tolist()

#romero_mass = normalize(romero_mass)
#romero_temp = normalize(romero_temp)
'''
romero_mass = romero_mass - np.nanmean(romero_mass)
romero_mass = [(x - min(romero_mass)) / (max(romero_mass) - min(romero_mass)) for x in romero_mass]

romero_temp = romero_temp - np.nanmean(romero_temp)
romero_temp = [(x - min(romero_temp)) / (max(romero_temp) - min(romero_temp)) for x in romero_temp]
'''



###FOR EACH STAR
for index, row in gaia.iterrows():
    #Create list of temps and masses from match
    temp = []
    mass = []
    #romero_mass = romero.mass.tolist()
    #romero_temp = romero.temp.tolist()
    #for all the lines
    #print(ID)
    for l in np.arange(0,len(lines)):
        #find the line for the star
        if lines[l] == row["ID"] + "_final\n" or lines[l] == row["ID"] + "\n":
            #increment through next lines that include "&"
            inc = 1
            while l+inc < len(lines) and lines[l+inc].find('&') > 1:
                temp_line = lines[l+inc]
                #print(temp_line[0:7], temp_line[10:14], "0")
                temp.append(float(temp_line[0:7]))
                mass.append(float(temp_line[10:14]))
                inc = inc+1

            
            mass = normalize(mass,0.47,1.00)
            temp = normalize(temp,10600,12600)

            nspec_temp = normalize(row["temp"],10600,12600)
            nspec_mass = normalize(row["mass"],0.47,1.00)

            #populate distance vector
            dists = []
            for j in np.arange(0,len(temp)):
                #dists.append(nspec_temp-temp[j])
                dists.append(np.sqrt((nspec_temp - temp[j])**2 + (nspec_mass - mass[j])**2))
            
            adj.write(row["ID"])
            adj.write(' & ')

            #if dist vector exists
            if len(dists) > 0:
                idx = int(dists.index(min(dists))) + 1
                print(row["ID"], "originally at", lines[l+1], "now at", lines[l+idx])
                adj.write(lines[l + idx])
            else:
                print("none for", row["ID"])
                adj.write('\n')

        
    
    
