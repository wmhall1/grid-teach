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

#spec = fn.get_spec()
romero = fn.get_spec_K2("spec")

westo = open('weston_ast','r')
lines = westo.readlines()

#table = open('k2_solutions', 'r')
#tablelines = table.readlines()

adj = open('weston_ast_little','w')
outtable = open('table','w')


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
    sigma = []
    #romero_mass = romero.mass.tolist()
    #romero_temp = romero.temp.tolist()
    #for all the lines
    for l in np.arange(0,len(lines)):
        #find the line for the star
        if lines[l] == romero.name[i] + "_final\n":
            #increment through next lines that include "&"
            inc = 1
            while l+inc < len(lines) and lines[l+inc].find('&') > 1:
                temp_Series = pd.Series(lines[l+inc], )
                temp_Series = temp_Series.str.split(pat = "&")
                temp_List = temp_Series[0]                
                #print(temp_List[3])
                
                #table_templine = tablelines[l+inc]
                temp_line = lines[l+inc]
                #print(temp_line[0:7], temp_line[10:14], "0")
                temp.append(float(temp_line[0:7]))
                mass.append(float(temp_line[10:14]))
                sigma.append(float(temp_List[3]))
                inc = inc+1

            
            adj.write(romero.name[i])
            adj.write('\n')
            #adj.write(' & ')
            #outtable.write(romero.name[i])
            #outtable.write(' & ')

            #if dist vector exists
            for idx in np.arange(1,inc-1):
                if sigma[idx-1] < min(sigma)*2:
                    #print(mass[idx-1])
                    adj.write(lines[l + idx])
            '''
            if len(sigma) > 0:
                idx = int(sigma.index(min(sigma))) + 1
                #print(idx)
                adj.write(lines[l + idx])
                #outtable.write(tablelines[l+idx])

            else:
                print("none for", romero.name[i])
                adj.write("\n")
                #outtable.write("\n")
            '''
        
    
    
