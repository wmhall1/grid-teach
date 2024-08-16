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

#adj = open('weston_ast_per','w')


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


cutoff = 0.05
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
                temp_line = lines[l+inc]
                #print(temp_line[0:7], temp_line[10:14], "0")
                temp.append(float(temp_line[0:7]))
                mass.append(float(temp_line[10:14]))
                sigma.append(float(temp_line[31:36]))
                inc = inc+1

            
            #adj.write(romero.name[i])
            #adj.write('\n')

            #if dist vector exists
            idx = 1
            #cutoff = np.mean(sigma) - np.std(sigma)
            nsigma = [ (x - min(sigma))/(max(sigma)-min(sigma)) for x in sigma]
            nsigma1 = [ x for x in nsigma if x < cutoff ]
            nsigma2 = [ x for x in nsigma if x > cutoff ]
            #y, x, _ = plt.hist(nsigma, bins=20)
            #print x.max()
            #print y.max()

            colo = "#1979a9"

            plt.figure(100, figsize=(10,5))
            plt.subplot(1,2,1)
            #plt.plot(np.arange(0,len(nsigma)), nsigma,'.', alpha=0.5)
            plt.plot(np.arange(0,len(nsigma1)), nsigma1, 'go', alpha=0.5)
            plt.plot(np.arange(len(nsigma1),len(nsigma1)+len(nsigma2)), nsigma2, '.', color = colo, alpha=0.5)
            #plt.plot(temp,nsigma, 'o')
            plt.plot([0,len(nsigma)], [0.05,0.05], 'r')
            plt.xlabel("Solution")
            plt.xticks([])
            plt.ylabel("Normalized S-value")


            plt.subplot(1,2,2)
            y,x, patches = plt.hist(nsigma,bins=20, facecolor=colo, edgecolor='black', linewidth=0.5)
            patches[0].set_fc('green')
            #plt.plot([0.05,0.05],[0,y.max()], 'r')
            plt.xlabel("Normalized S-value")
            plt.ylabel("Number of solutions")


            plt.suptitle(romero.name[i])

            ''' 
            plt.subplot(2,2,3)
            plt.plot(np.arange(0,len(sigma)), nsigma)

            plt.subplot(2,2,4)
            plt.hist(sigma, bins=10)
            '''
            plt.show()

            #if sigma[0] < 0.000001:
            #    cutoff = 0.01
            #for nsig in nsigma:
                #if nsig < 0.05:
                    #adj.write(lines[l + idx])
                #idx = idx+1

        
    
    
