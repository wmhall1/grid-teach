import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import functions as fn


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "weston_ast_adj"


spec = fn.get_spec_K2("spec")
westo = fn.get_westo(filename) 

GD1212_idx = -1

print(westo)
spec_adj = pd.DataFrame(index = westo.index, columns=spec.columns)
for i in np.arange(0, len(westo)):
    run = spec[spec['name'] == westo.name[i]]
    #print(run)
    if len(run.temp) > 0:
        spec_adj.name[i] = run.name
        spec_adj.temp[i] = run.temp
        #spec_adj.logg[i] = run.logg
        spec_adj.mass[i] = run.mass
    if westo.name[i] == "EPIC60017836":
        #print("foundit")
        GD1212_idx = i

spec_resid = []
old_resid = []

spec_residm = []
old_residm =[]
for i in np.arange(0,len(westo)):
    #print(spec_adj.name[i], casta.name[i], westo.name[i])
    spec_resid.append(float(spec_adj.temp[i] - westo.temp[i]))
    spec_residm.append(float(spec_adj.mass[i] - westo.mass[i]))

for i in np.arange(0,len(spec_resid)):
    if abs(spec_resid[i]) > 400:
        print(westo.name[i])

westo_temp = westo.temp.tolist()


plt.rc('font', size=10)          # controls default text sizes
plt.rc('axes', titlesize=10)     # fontsize of the axes title
plt.rc('axes', labelsize=10)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
plt.rc('ytick', labelsize=10)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize
plt.rc('figure', titlesize=16)  # fontsize of the figure title




plt.figure(100, figsize=(7,5))
plt.scatter(spec_residm, spec_resid, c = westo.S, cmap = 'viridis_r')
cbar=plt.colorbar()
cbar.set_label("S Value")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])

'''if GD1212_idx >= 0:
    plt.plot([spec_residm[GD1212_idx], 0.1], [spec_resid[GD1212_idx], 500], 'k-')
    plt.text(0.1,500, "GD 1212")
'''
plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")

plt.plot([0,0],[-4000,4000], "r-", alpha = 0.5)
plt.plot([-0.6,0.6],[0,0], "r-", alpha = 0.5)

plt.show()


print(np.mean(westo.temp), np.mean(westo.mass))

print("List here to check:")
idx = 0
for resid, residm in zip(spec_resid, spec_residm):
    if (abs(resid) > 1000) or (abs(residm) > 0.2):
        print(westo.name[idx])
    if (abs(resid) < 200) and (abs(residm) < 0.1):
        print("Good", westo.name[idx])
    idx = idx+1
