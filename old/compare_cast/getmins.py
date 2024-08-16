import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import functions as fn


#spec = fn.get_spec()
romero = fn.get_casta_spec("star")

westo = open('weston_ast','r')
lines = westo.readlines()

adj = open('weston_ast_adj','w')
###FOR EACH STAR
for i in np.arange(0,len(romero)):
    
    #Create list of temps and masses from match
    temp = []
    mass = []
    ses = []

    #for all the lines
    for l in np.arange(0,len(lines)):

        #find the line for the star
        if lines[l] == romero.name[i] + "\n":

            #increment through next lines that include "&"
            inc = 1
            while l+inc < len(lines) and lines[l+inc].find('&') > 1:
                #12100.0 & 0.61 & 400.0 200.0 & 1.563 &  100 & 3.0
                temp_line = lines[l+inc]
                #print(temp_line[0:7], temp_line[10:14], "0")
                temp.append(float(temp_line[0:7]))
                mass.append(float(temp_line[10:14]))
                ses.append(float(temp_line[31:35]))

                inc = inc+1

            #populate distance vector
            dists = []
            for j in np.arange(0,len(temp)):
                dists.append(np.sqrt((romero.temp[i]-temp[j])**2 + (romero.mass[i]-mass[j])**2))
            
            adj.write(romero.name[i])
            adj.write(' & ')

            #if dist vector exists
            if len(dists) > 0:
                #idx = int(dists.index(min(dists))) + 1
                idx = int(ses.index(min(ses)))+1
                adj.write(lines[l + idx])
            else:
                print("none")
                adj.write('\n')

        
    
    
