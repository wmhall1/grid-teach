import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import functions as fn

def add_axis():
    plt.plot([0,0],[-4000,4000], "r-", alpha = 0.5)
    plt.plot([-0.6,0.6],[0,0], "r-", alpha = 0.5)


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "weston_ast_adj"


spec = fn.get_spec_K2("spec")
#westo = fn.get_westo(filename) 
gaia = pd.read_table("gaia_model_fit",sep = " ", header = None, names = ["ID", "S", "temp", "mass"], dtype={'temp':float,'mass':float})

westo = fn.get_westo("weston_ast_adj_S")
westospec = fn.get_westo("weston_ast_adj")
westogaia = fn.get_westo("weston_ast_adj_g")


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

spec_resid = []
gaia_resid = []
gaia_spec = []
swes_spec = []
gwes_spec = []
gwes_gaia = []


spec_residm = []
gaia_residm =[]
gaia_specm = []
swes_specm = []
gwes_specm = []
gwes_gaiam = []
for i in np.arange(0,len(westo)):
    #print(spec_adj.name[i], casta.name[i], westo.name[i])
    spec_resid.append(float(spec_adj.temp[i] - westo.temp[i]))
    spec_residm.append(float(spec_adj.mass[i] - westo.mass[i]))
    gaia_resid.append(float(gaia_adj.temp[i] - westo.temp[i]))
    gaia_residm.append(float(gaia_adj.mass[i] - westo.mass[i]))
    gaia_spec.append(float(spec_adj.temp[i] - gaia_adj.temp[i]))
    gaia_specm.append(float(spec_adj.mass[i] - gaia_adj.mass[i]))
    swes_spec.append(float(spec_adj.temp[i] - westospec.temp[i]))
    swes_specm.append(float(spec_adj.mass[i] - westospec.mass[i]))
    gwes_spec.append(float(spec_adj.temp[i] - westogaia.temp[i]))
    gwes_specm.append(float(spec_adj.mass[i] - westogaia.mass[i]))
    gwes_gaia.append(float(gaia_adj.temp[i] - westogaia.temp[i]))
    gwes_gaiam.append(float(gaia_adj.mass[i] - westogaia.mass[i]))


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




plt.figure(100, figsize=(16, 10))
plt.subplot(2,3,1)
add_axis()
plt.scatter(spec_residm, spec_resid, c = westo.S, cmap = 'viridis_r')
cbar=plt.colorbar()
cbar.set_label("S Value")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])
plt.title("SEISM. MIN S vs SPEC")

if GD1212_idx >= 0:
    plt.plot([spec_residm[GD1212_idx], 0.25], [spec_resid[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")

plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")

#plt.figure(200)
plt.subplot(2,3,2)
add_axis()
plt.scatter(gaia_residm, gaia_resid, c = westo.S, cmap = 'viridis_r')
cbar=plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{gaia} - T_{seism}$ (K)")
plt.xlabel("Mass residual $M_{Gaia} - M_{seism}$ ($M_\odot$)")
plt.title("SEISM. MIN S vs. GAIA")
plt.xlim([-0.51,0.51])
plt.ylim([-4050,2050])
if GD1212_idx >= 0:
    plt.plot([gaia_residm[GD1212_idx], 0.25], [gaia_resid[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")


plt.subplot(2,3,3)
add_axis()
plt.scatter(gaia_specm, gaia_spec, c = gaia_adj.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("Gaia S")
plt.ylabel("Temperature residual $T_{spec} - T_{gaia}$ (K)")
plt.xlabel("Mass residual $M_{spec} - M_{gaia}$ ($M_\odot$)")
plt.title("GAIA vs. SPEC")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,4050])
if GD1212_idx >= 0:
    plt.plot([gaia_specm[GD1212_idx], 0.25], [gaia_spec[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")


plt.subplot(2,3,4)
add_axis()
plt.scatter(swes_specm, swes_spec, c = westo.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")
plt.title("SPEC SELECTED SEISM vs. SPEC")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,2050])
if GD1212_idx >= 0:
    plt.plot([swes_specm[GD1212_idx], 0.25], [swes_spec[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")

plt.subplot(2,3,5)
add_axis()
plt.scatter(gwes_specm, gwes_spec, c = westo.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{spec} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{seism}$  ($M_\odot$)")
plt.title("GAIA SELECTED SEISM vs. SPEC")
plt.xlim([-0.51,0.51])
plt.ylim([-2050,3050])
if GD1212_idx >= 0:
    plt.plot([gwes_specm[GD1212_idx], 0.25], [gwes_spec[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")



plt.subplot(2,3,6)
add_axis()
plt.scatter(gwes_gaiam, gwes_gaia, c = westo.S, cmap = 'viridis_r')
cbar = plt.colorbar()
cbar.set_label("S Value")
plt.ylabel("Temperature residual $T_{gaia} - T_{seism}$  (K)")
plt.xlabel("Mass residual $M_{gaia}-M_{seism}$  ($M_\odot$)")
plt.title("GAIA SELECTED SEISM vs. GAIA")
plt.xlim([-0.51,0.51])
plt.ylim([-4050,2050])
if GD1212_idx >= 0:
    plt.plot([gwes_gaiam[GD1212_idx], 0.25], [gwes_gaia[GD1212_idx], -1850], 'k-')
    plt.text(0.25,-1900, "GD 1212")



plt.show()


print(np.mean(westo.temp), np.mean(westo.mass))
