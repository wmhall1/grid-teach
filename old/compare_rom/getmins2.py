'''
Written by Weston Hall
03-30-2022

getmins
to be used in conjunction with output from clustermins

input is screen output saved from clustermins:
    echo $STAR >> weston_ast
    python3 clustermins.py $STAR >> weston_ast
Can be many star clusters outputted concatenated on each other
which can be set up in bash shell script, or looped over for $STAR

Output is file containing the best fitting family for each star in
weston_ast that matches one in the Romero/Castanheira/K2 datasets
(adjust input as needed for other datasets)
'''
import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import functions as fn


#Define the normalization function
def normalize(lst, minimum, maximum):
    if isinstance(lst,float) == True:
        length = 1
        new_lst = (lst-minimum) / (maximum - minimum)
    else:
        new_lst = [(lst[x] - minimum) / (maximum - minimum) for x in np.arange(0,len(lst))]
    return(new_lst)

#Get input of spectral data Romero et. al uses
#Function defined in functions.py file and depends on personal formatting of data.
#function output needs to be a pd.DataFrame with columns for:
#   name, temp, mass
#at minimum.
'''
Example function to retrieve spectroscopy data:

def get_romero(filename):
    data = pd.read_table(filename,sep = " ", header = None,dtype = str, engine="python")
    data = data.reset_index()
    run = data.loc[0]
    df = pd.DataFrame(index = data.index, columns = ["name", "temp", "logg", "mass"])
    for i in np.arange(0,len(data)):
        run = data.loc[i]
        df.name[i] = run[0]
        df.temp[i] = float(run[4]+run[5])
        df.logg[i] = float(run[1])
        df.mass[i] = float(run[8])
    return(df)
'''
#"spectral" is name of file containing spectroscopic solutions
romero = fn.get_spec("spectral")

westo = open('weston_ast','r')
lines = westo.readlines()

#Open output
adj = open('weston_ast_adj','w')

#Lists are easier to iterate
romero_mass = romero.mass.tolist()
romero_temp = romero.temp.tolist()

###FOR EACH STAR
for i in np.arange(0,len(romero)):
    
    #Create list of temps and masses from match
    temp = []
    mass = []
    
    #for all the lines
    for l in np.arange(0,len(lines)):

        #find the line for the star
        if lines[l] == romero.name[i] + "\n":

            #increment through next lines that include "&"
            inc = 1
            while l+inc < len(lines) and lines[l+inc].find('&') > 1:
                temp_line = lines[l+inc]
                #print(temp_line[0:7], temp_line[10:14], "0") #debugging
                temp.append(float(temp_line[0:7]))
                mass.append(float(temp_line[10:14]))
                inc = inc+1
            
            #Normalize everything
            mass = normalize(mass,0.47,0.97)
            temp = normalize(temp,10600,12600)

            nspec_temp = normalize(romero_temp[i],10600,12600)
            nspec_mass = normalize(romero_mass[i],0.47,0.97)

            #populate distance vector
            dists = []
            for j in np.arange(0,len(temp)):
                dists.append(np.sqrt((nspec_temp - temp[j])**2 + (nspec_mass - mass[j])**2))
            
            #Write to output
            adj.write(romero.name[i])
            adj.write(' & ')

            #if dist vector exists
            if len(dists) > 0:
                idx = int(dists.index(min(dists))) + 1
                adj.write(lines[l + idx])
            else:
                print("none")
                adj.write('\n')

        
    
    
