import matplotlib.pyplot as plt
import math
import statistics
import sys
#from scipy.stats import nanmean
import pandas as pd
import numpy as np
import functions as fn

casta = fn.get_casta("compare_cast/casta_ast")
romero = fn.get_romero("compare_rom/romero_ast")
westo_cas = fn.get_westo("compare_cast/weston_ast_adj")
westo_rom = fn.get_westo("compare_rom/weston_ast_adj")

'''

print(casta.head())
print(romero.head())
'''

print(westo_cas.head())
print(westo_rom.head())
q = 0

for i in np.arange(0, len(westo_rom)):
    if math.isnan(westo_rom.temp[i]) == False:
        cas = westo_cas[westo_cas.name == westo_rom.name[i]]
        cas = cas.reset_index()
        title = str(westo_rom.name[i]) + " &"
        if len(cas) >0:
            print(cas.name[0], "& [1] &", int(cas.temp[0]), "&", cas.mass[0], "&", cas.hydrogen[0], "&", cas.helium[0], "&", cas.S[0], " \\\\")
            title = "     &"
        print(title,'[2] &', int(westo_rom.temp[i]), "&", westo_rom.mass[i], "&", westo_rom.hydrogen[i], "&", westo_rom.helium[i], "&", westo_rom.S[i], " \\\\" )
        print('\hline')
        q = q+1


#print("\n\n")
for i in np.arange(0, len(westo_cas)):
    if len(westo_rom[westo_rom.name == westo_cas.name[i]]) < 1 and math.isnan(westo_cas.temp[i])==False:
        print(westo_cas.name[i], "& [1] &", int(westo_cas.temp[i]), "&", westo_cas.mass[i], "&", westo_cas.hydrogen[i], "&", westo_cas.helium[i], "&", westo_cas.S[i], " \\\\" )
        print("\hline")
        q = q+1



print(q)




