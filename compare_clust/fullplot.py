import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import functions as fn

def add_axis():
    plt.plot([0,0],[-4000,4000], "r-", alpha = 0.5)
    plt.plot([-0.6,0.6],[0,0], "r-", alpha = 0.5)



spec = fn.get_spec_K2("spec")

gaia = pd.read_table("gaia_model_fit",sep = " ", header = None, names = ["ID", "S", "temp", "mass"], dtype={'temp':float,'mass':float})

westo = fn.get_westo("weston_ast_adj_S")

westospec = fn.get_westo("weston_ast_adj")
westogaia = fn.get_westo("weston_ast_adj_g")

westo_perspec = fn.get_westo("weston_ast_per_adj")
westo_pergaia = fn.get_westo("weston_ast_per_adj_g")

westo_wei = fn.get_wei("weston_ast_adj_wei")
westoper_wei = fn.get_wei("weston_ast_per_adj_wei")

print(len(westo.index), len(westospec.index), len(westogaia.index), len(gaia.index))

GD1212_idx = -1

#print(spec.name)
spec_adj = pd.DataFrame(index = westo.index, columns=spec.columns)
gaia_adj = pd.DataFrame(index = westo.index, columns=gaia.columns)
for i in np.arange(0, len(westo)):
    run = spec[spec['name'] == westo.name[i]]
    run_gaia = gaia[gaia["ID"] == westo.name[i]]
    #print(run)
    #print(run_gaia)
    if len(run.temp) > 0:
        spec_adj.name[i] = run.name
        spec_adj.temp[i] = run.temp
        #spec_adj.logg[i] = run.logg
        spec_adj.mass[i] = run.mass
        gaia_adj.ID[i] = run_gaia.ID
        gaia_adj.S[i] = run_gaia.S
        gaia_adj.temp[i] = run_gaia.temp
        gaia_adj.mass[i] = run_gaia.mass


    if westo.name[i] == "EPIC60017836":
        #print("foundit")
        GD1212_idx = i
#print("length", len(gaia_adj.index))
#print(gaia_adj)

full_spec_resid = []
full_gaia_resid = []
full_gaia_spec = []
full_swes_spec = []
full_gwes_spec = []
full_gwes_gaia = []

full_spec_residm = []
full_gaia_residm =[]
full_gaia_specm = []
full_swes_specm = []
full_gwes_specm = []
full_gwes_gaiam = []

per_swes_spec = []
per_gwes_spec = []
per_gwes_gaia = []

per_swes_specm = []
per_gwes_specm = []
per_gwes_gaiam = []

full_wei_spec = []
full_wei_specm = []
full_wei_gaia = []
full_wei_gaiam = []

per_wei_spec = []
per_wei_gaia = []
per_wei_specm =[]
per_wei_gaiam =[]


for i in np.arange(0,len(westo)):
    #print(spec_adj.name[i], casta.name[i], westo.name[i])
    full_spec_resid.append(float(spec_adj.temp[i] - westo.temp[i]))
    full_spec_residm.append(float(spec_adj.mass[i] - westo.mass[i]))
    full_gaia_resid.append(float(gaia_adj.temp[i] - westo.temp[i]))
    full_gaia_residm.append(float(gaia_adj.mass[i] - westo.mass[i]))
    full_gaia_spec.append(float(spec_adj.temp[i] - gaia_adj.temp[i]))
    full_gaia_specm.append(float(spec_adj.mass[i] - gaia_adj.mass[i]))
    full_swes_spec.append(float(spec_adj.temp[i] - westospec.temp[i]))
    full_swes_specm.append(float(spec_adj.mass[i] - westospec.mass[i]))
    full_gwes_spec.append(float(spec_adj.temp[i] - westogaia.temp[i]))
    full_gwes_specm.append(float(spec_adj.mass[i] - westogaia.mass[i]))
    full_gwes_gaia.append(float(gaia_adj.temp[i] - westogaia.temp[i]))
    full_gwes_gaiam.append(float(gaia_adj.mass[i] - westogaia.mass[i]))

    per_swes_spec.append(float(spec_adj.temp[i] - westo_perspec.temp[i]))
    per_swes_specm.append(float(spec_adj.mass[i] - westo_perspec.mass[i]))

    per_gwes_gaia.append(float(gaia_adj.temp[i] - westo_pergaia.temp[i]))
    per_gwes_gaiam.append(float(gaia_adj.mass[i] - westo_pergaia.mass[i]))

    full_wei_spec.append(float(spec_adj.temp[i]-westo_wei.temp[i]))
    full_wei_specm.append(float(spec_adj.mass[i]-westo_wei.mass[i]))
    full_wei_gaia.append(float(gaia_adj.temp[i]-westo_wei.temp[i]))
    full_wei_gaiam.append(float(gaia_adj.mass[i]-westo_wei.mass[i]))
    per_wei_spec.append(float(spec_adj.temp[i] - westoper_wei.temp[i]))
    per_wei_specm.append(float(spec_adj.mass[i] -westoper_wei.mass[i]))
    per_wei_gaia.append(float(gaia_adj.temp[i] - westoper_wei.temp[i]))
    per_wei_gaiam.append(float(gaia_adj.mass[i]- westoper_wei.mass[i]))

'''
for i in np.arange(0,len(spec_resid)):
    if abs(spec_resid[i]) > 400:
        print(westo.name[i])
'''
westo_temp = westo.temp.tolist()


plt.rc('font', size=10)          # controls default text sizes
plt.rc('axes', titlesize=10)     # fontsize of the axes title
plt.rc('axes', labelsize=10)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
plt.rc('ytick', labelsize=10)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize
plt.rc('figure', titlesize=16)  # fontsize of the figure title




plt.figure(100, figsize=(19, 10))

#plt.suptitle(filename)


plt.subplot(3,4,1)
add_axis()
plt.scatter(full_spec_residm, full_spec_resid, c = westo.S, cmap = 'viridis_r')
cbar=plt.colorbar()
cbar.set_label("S Value")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])
plt.title("SEISM. MIN S vs SPEC")

if GD1212_idx >= 0:
    plt.plot([full_spec_residm[GD1212_idx], 0.25], [full_spec_resid[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")

plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")

#plt.figure(200)
plt.subplot(3,4,2)
add_axis()
plt.scatter(full_gaia_residm, full_gaia_resid, c = westo.S, cmap = 'viridis_r')
cbar=plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{gaia} - T_{seism}$ (K)")
plt.xlabel("Mass residual $M_{Gaia} - M_{seism}$ ($M_\odot$)")
plt.title("SEISM. MIN S vs. GAIA")
plt.xlim([-0.51,0.51])
plt.ylim([-4050,2050])
if GD1212_idx >= 0:
    plt.plot([full_gaia_residm[GD1212_idx], 0.25], [full_gaia_resid[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")


plt.subplot(3,4,3)
add_axis()
plt.scatter(full_gaia_specm, full_gaia_spec, c = gaia_adj.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("Gaia S")
plt.ylabel("Temperature residual $T_{spec} - T_{gaia}$ (K)")
plt.xlabel("Mass residual $M_{spec} - M_{gaia}$ ($M_\odot$)")
plt.title("GAIA vs. SPEC")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,4050])
if GD1212_idx >= 0:
    plt.plot([full_gaia_specm[GD1212_idx], 0.25], [full_gaia_spec[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")


plt.subplot(3,4,4)
add_axis()
plt.scatter(full_swes_specm, full_swes_spec, c = westospec.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")
plt.title("SPEC SELECTED SEISM vs. SPEC")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])
if GD1212_idx >= 0:
    plt.plot([full_swes_specm[GD1212_idx], 0.25], [full_swes_spec[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")
'''
plt.subplot(2,4,5)
add_axis()
plt.scatter(full_gwes_specm, full_gwes_spec, c = westogaia.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")
plt.title("GAIA SELECTED SEISM vs. SPEC")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,3050])
if GD1212_idx >= 0:
    plt.plot([full_gwes_specm[GD1212_idx], 0.25], [full_gwes_spec[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")
'''


plt.subplot(3,4,5)
add_axis()
plt.scatter(full_gwes_gaiam, full_gwes_gaia, c = westogaia.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{gaia} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{gaia}-M_{seism}$  ($M_\odot$)")
plt.title("GAIA SELECTED SEISM vs. GAIA")
plt.xlim([-0.51,0.51])
plt.ylim([-4050,2050])
if GD1212_idx >= 0:
    plt.plot([full_gwes_gaiam[GD1212_idx], 0.25], [full_gwes_gaia[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")

plt.subplot(3,4,6)
add_axis()
plt.scatter(per_swes_specm, per_swes_spec, c = westo_perspec.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")
plt.title("Spec selected per seism vs spec")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])

plt.subplot(3,4,7)
add_axis()
plt.scatter(per_gwes_gaiam, per_gwes_gaia, c = westo_pergaia.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{gaia} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{gaia}-M_{seism}$  ($M_\odot$)")
plt.title("gaia selected per seism vs gaia")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])

plt.subplot(3,4,8)
add_axis()
plt.scatter(full_wei_specm, full_wei_spec, c = westo_wei.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")
plt.title("WEIGHTED MEAN seism vs spec")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])

plt.subplot(3,4,9)
add_axis()
plt.scatter(per_wei_specm, per_wei_spec, c = westoper_wei.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")
plt.title("weighted mean per seism vs spec")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])

plt.subplot(3,4,10)
add_axis()
plt.scatter(full_wei_gaiam, full_wei_gaia, c = westo_wei.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{gaia} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{gaia}-M_{seism}$  ($M_\odot$)")
plt.title("WEIGHTED MEAN full seism vs gaia")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])

plt.subplot(3,4,11)
add_axis()
plt.scatter(per_wei_gaiam, per_wei_gaia, c = westoper_wei.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{gaia} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{gaia}-M_{seism}$  ($M_\odot$)")
plt.title("weighted mean per seism vs gaia")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])

plt.subplots_adjust(left=0.125,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.35,
                    hspace=0.35)

plt.show()


print(np.mean(westo.temp), np.mean(westo.mass))
