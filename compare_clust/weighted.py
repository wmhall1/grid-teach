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
romero = fn.get_spec_K2("spec")

westo = open(filename,'r')
lines = westo.readlines()

"""
print(romero.name)

for l in np.arange(0,len(lines)):
    #print(l, ": ", lines[l])
    for i in np.arange(0,len(romero)):
        if lines[l] == romero.name[i] + "\n":
            print(romero.name[i])
"""

#print(len(lines))
adj = open(filename+'_adj_wei','w')


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
    hy = []
    he = []
    sigma = []
    #romero_mass = romero.mass.tolist()
    #romero_temp = romero.temp.tolist()
    #for all the lines
    for l in np.arange(0,len(lines)):
        #find the line for the star
        if lines[l] == romero.name[i] + "_final\n" or lines[l] == romero.name[i] + "\n":
            #increment through next lines that include "&"
            inc = 1
            while l+inc < len(lines) and lines[l+inc].find('&') > 1:
                temp_line = lines[l+inc]
                #print(temp_line[0:7], temp_line[10:14], "0")
                temp.append(float(temp_line[0:7]))
                mass.append(float(temp_line[10:14]))
                hy.append(float(temp_line[18:22]))
                he.append(float(temp_line[24:28]))
                sigma.append(float(temp_line[31:36]))
                inc = inc+1
#12600.0 & 0.720 & 600.0 350.0 & 0.369 & 55.0 & 1
            
            #mass = normalize(mass,0.47,1.00)
            #temp = normalize(temp,10600,12600)
            
            #nspec_temp = normalize(romero_temp[i],10600,12600)
            #nspec_mass = normalize(romero_mass[i],0.47,1.00)

            #populate distance vector
            #dists = []
            #for j in np.arange(0,len(temp)):
                #dists.append(np.sqrt((nspec_temp - temp[j])**2 + (nspec_mass - mass[j])**2))
            
            adj.write(romero.name[i])
            adj.write(' & ')
            #nsigma = [ (max(sigma)-min(sigma))/(x - min(sigma)) for x in sigma]
            nsigma = []
            for sig in sigma:
                if sig == min(sigma):
                    nsigma.append(1)
                else:
                    nsigma.append((max(sigma)-min(sigma))/(sig - min(sigma)))
            #if dist vector exists
            avtemp = 0
            avmass = 0
            avhy = 0
            avhe = 0
            for j in np.arange(0,len(temp)):
                avtemp = avtemp + nsigma[j] * temp[j]
                avmass = avmass + nsigma[j] * mass[j]
                avhy = avhy + nsigma[j] * hy[j]
                avhe = avhe + nsigma[j] * he[j]
            avtemp = avtemp/sum(nsigma)
            avmass = avmass/sum(nsigma)
            avhy = avhy/sum(nsigma)
            avhe = avhe/sum(nsigma)

            adj.write(str(avtemp) + " & " + str(avmass) + " & " + str(avhy) + " & " + str(avhe) + " & " + str(sum(nsigma)) + "\n")
            '''
            if len(dists) > 0:
                idx = int(dists.index(min(dists))) + 1
                print(romero.name[i], "originally at", lines[l+1], "now at", lines[l+idx])
                adj.write(lines[l + idx])
            else:
                print("none for", romero.name[i])
                adj.write('\n')
            '''
        
    
    
