import matplotlib.pyplot as plt
import matplotlib.colors as colors
import math
import sys
import pandas as pd
import numpy as np
import functions as fn


spec = fn.get_spec("spectral")
romero = fn.get_romero("romero_ast")
westo = fn.get_westo("weston_ast_adj")

spec_adj = pd.DataFrame(index = spec.index, columns = spec.columns)
#westo_adj = pd.DataFrame(index = westo.index, columns = westo.columns)
westo_adj = westo
#print(westo.name)
#spec_adj = spec[spec['name'] == romero.name]
#print(westo_adj)

#print(spec_adj)
for i in np.arange(0, len(spec)):
    #print("romero: ", romero.name[i])
    run = spec.loc[spec['name'] == romero.name[i]]
    wrun = westo.loc[westo['name'] == romero.name[i]]
    #print(wrun.name)
    if len(run.temp) > 0:
        spec_adj.name[i] = run.name
        spec_adj.temp[i] = run.temp
        spec_adj.logg[i] = run.logg
        spec_adj.mass[i] = run.mass
    if romero.name[i] == "G117-B15A":
        G117_idx = i
    if romero.name[i] == "R548":
        R548_idx = i
'''    
    if len(wrun.temp) > 0:
        westo_adj.name[i] = wrun.name
        westo_adj.temp[i] = wrun.temp
        westo_adj.mass[i] = wrun.mass
        westo_adj.num[i] = wrun.num
        westo_adj.per[i] = wrun.per
'''    
#print(westo_adj)
#print(romero)
romero_resid = []
spec_resid = []
old_resid = []

romero_residm = []
spec_residm = []
old_residm =[]
for i in np.arange(0,len(westo_adj)):
    #print(spec_adj.name[i], romero.name[i], westo_adj.name[i])
    romero_resid.append(romero.temp[i] - westo_adj.temp[i])
    spec_resid.append(spec.temp[i] - westo_adj.temp[i])
    old_resid.append(spec.temp[i] - romero.temp[i])
    romero_residm.append(romero.mass[i] - westo_adj.mass[i])
    spec_residm.append(spec.mass[i] - westo_adj.mass[i])
    old_residm.append(spec.mass[i] - romero.mass[i])


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

cmap_use = truncate_colormap(plt.get_cmap("Reds_r"), 0.0,0.8, len(westo_adj.S))

plt.figure(300)
plt.scatter(spec_residm, spec_resid, c = westo_adj.S, cmap = cmap_use, alpha=0.7, label = "Hall 2022")

plt.xlim([-0.5,0.5])
plt.ylim([-2000,2000])

cbar = plt.colorbar()
cbar.set_label("S Value")

plt.scatter(old_residm, old_resid, c = "b", alpha = 0.5,marker ="^", label = "Romero et al. 2011")

plt.plot([spec_residm[G117_idx],0.17], [spec_resid[G117_idx], 850], 'r-')
plt.plot([old_residm[G117_idx],0.17], [old_resid[G117_idx], 850], 'b-')
plt.text(0.12, 830, "G117-B15A")

plt.ylabel("Temperature residual $T_{spec} - T_{astero}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{astero}$  ($M_\odot$)")

plt.plot([spec_residm[R548_idx],0.12], [spec_resid[R548_idx], 500], 'r-')
plt.plot([old_residm[R548_idx],0.12], [old_resid[R548_idx], 500], 'b-')
plt.text(0.12, 500, "R548")

plt.legend()
#plt.show()


plt.figure(100)
plt.scatter(romero_residm, romero_resid, c=westo_adj.S, cmap = 'viridis_r', label = "Hall, 2022")
cbar=plt.colorbar()
cbar.set_label("S Value")
#plt.scatter(np.arange(0,len(westo_resid)), westo_resid)

plt.xlim([-0.5,0.5])
plt.ylim([-2000,2000])


plt.ylabel("Temperature residual $T_{Romero} - T_{Hall}$  (K)")
plt.xlabel("Mass residual $M_{Romero}-M_{Hall}$  ($M_\odot$)")
#plt.legend()

plt.plot([romero_residm[G117_idx],romero_residm[G117_idx]], [romero_resid[G117_idx], romero_resid[G117_idx]+500], 'k-')
plt.text(romero_residm[G117_idx], romero_resid[G117_idx]+520, "G117-B15A")

plt.plot([romero_residm[R548_idx], romero_residm[R548_idx]], [romero_resid[R548_idx], romero_resid[R548_idx]+500], 'k-')
plt.text(romero_residm[R548_idx], romero_resid[R548_idx]+520, "R548")

#plt.show()

plt.figure(200)
plt.scatter(westo_adj.temp, spec_resid)
plt.show()

plt.figure(150)
plt.scatter(westo_adj.per, spec_residm)
#plt.scatter(westo_adj.per, old_resid)
#plt.show()

'''
for i in np.arange(0,len(romero)):
    print(romero.name[i], " &  & [C] \\\\")
'''
print(westo_adj.name[R548_idx], romero.name[R548_idx])
