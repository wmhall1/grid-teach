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
    i#new_lst = [(x - min(new_lst)) / (max(new_lst) - min(new_lst)) for x in new_lst]
    return(new_lst)

#spec = fn.get_spec()
romero = fn.get_spec("spectral")

westo = open('rom_solutions','r')
lines = westo.readlines()

adj = open('table','w')


romero_mass = romero.mass.tolist()
romero_temp = romero.temp.tolist()

#romero_mass = normalize(romero_mass)
#romero_temp = normalize(romero_temp)
'''
romero_mass = romero_mass - np.nanmean(romero_mass)
romero_mass = [(x - min(romero_mass)) / (max(romero_mass) - min(romero_mass)) for x in romero_mass]

romero_temp = romero_temp - np.nanmean(romero_temp)
romero_temp = [(x - min(romero_temp)) / (max(romero_temp) - min(romero_temp)) for x in romero_temp]
'''



###FOR EACH STAR
for i in np.arange(0,len(romero)):
    #Create list of temps and masses from match
    temp = []
    mass = []
    #romero_mass = romero.mass.tolist()
    #romero_temp = romero.temp.tolist()
    #for all the lines
    for l in np.arange(0,len(lines)):
        #find the line for the star
        if lines[l] == romero.name[i] + "\n":
            #increment through next lines that include "&"
            inc = 1
            while l+inc < len(lines) and lines[l+inc].find('&') > 1:
                temp_line = lines[l+inc]
                #print(temp_line[0:7], temp_line[10:14], "0")
                temp.append(float(temp_line[0:6]))
                mass.append(float(temp_line[9:13]))
                inc = inc+1

            
            mass = normalize(mass,0.47,0.97)
            temp = normalize(temp,10600,12600)


            
            nspec_temp = normalize(romero_temp[i],10600,12600)
            nspec_mass = normalize(romero_mass[i],0.47,0.97)

            #populate distance vector
            dists = []
            for j in np.arange(0,len(temp)):
                dists.append(np.sqrt((nspec_temp - temp[j])**2 + (nspec_mass - mass[j])**2))
            
            #print(romero.name[i])
            adj.write(romero.name[i])
            adj.write(' & [2] & ')

            #if dist vector exists
            if len(dists) > 0:
                idx = int(dists.index(min(dists))) +1
                print(romero.name[i], " & ", lines[l+idx])
                adj.write(lines[l + idx])
               # adj.write("\\hline \n")
            else:
                #print("none")
                adj.write('\n')

        
    
    
