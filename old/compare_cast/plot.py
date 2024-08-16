import matplotlib.pyplot as plt
import matplotlib.colors as colors
import math
import statistics
import sys
#from scipy.stats import nanmean
import pandas as pd
import numpy as np
import functions as fn


westo = fn.get_westo("weston_ast_adj")
spec = fn.get_casta_spec("star")
casta = fn.get_casta("casta_ast")
#print(spec.head())
#print(westo.head())
#print(casta.head())

'''
for i in np.arange(0,len(spec)):
    print1(spec.name[i], spec.temp[i], spec.mass[i])

'''
#print(casta.name)
spec_adj = pd.DataFrame(index = spec.index, columns=spec.columns)
for i in np.arange(0, len(casta)):
    run = spec.loc[spec['name'] == casta.name[i]]
    if len(run.temp) > 0:
        spec_adj.name[i] = run.name
        spec_adj.temp[i] = run.temp
        #spec_adj.logg[i] = run.logg
        spec_adj.mass[i] = run.mass
    if casta.name[i] == "G117-B15A":
        G117_idx = i
        #print(casta.name[i], spec_adj.name[i], westo.name[i])
    if casta.name[i] == "R548":
        R548_idx = i

print(len(casta))
print(casta.name.tolist())
print(len(westo))
print(westo.name.tolist())

spec_resid = []
old_resid = []
casta_resid = []

spec_residm = []
old_residm =[]
casta_residm = []
for i in np.arange(0,len(westo)):
    #print(spec_adj.name[i], casta.name[i], westo.name[i])
    casta_resid.append(float(casta.temp[i] - westo.temp[i]))
    casta_residm.append(float(casta.mass[i] - westo.mass[i]))
    spec_resid.append(float(spec_adj.temp[i] - westo.temp[i]))
    old_resid.append(float(spec_adj.temp[i] - casta.temp[i]))
    spec_residm.append(float(spec_adj.mass[i] - westo.mass[i]))
    old_residm.append(float(spec_adj.mass[i] - casta.mass[i]))

westo_temp = westo.temp.tolist()
print(old_resid)

SSR = 0
SST = 0
for i in np.arange(0,len(spec_resid)):
    if math.isnan(spec_resid[i]) == False:
        SSR += (spec_resid[i]**2)
        SST+= (float(westo.temp[i]) - np.nanmean(westo_temp))**2
#rsq = math.sqrt(1-SSR/SST)
#print(spec_resid)
#print(np.nanmean(westo_temp))
#print(SSR)
#print(SST)
#print("Rsq for westo:", rsq)

#print(spec_resid)
print(G117_idx)


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

cmap_use = truncate_colormap(plt.get_cmap("Reds_r"), 0.0,0.8, len(westo.S))

############################################

plt.figure(400)
plt.scatter(westo.temp, spec_resid, c=westo.S, cmap=cmap_use,alpha=0.7,label="Hall 2022")
plt.scatter(casta.temp,old_resid, c= 'b', marker = '^', alpha = 0.5, label = "Castanheira et. el. 2009")

cbar=plt.colorbar()
cbar.set_label("S Value")

plt.plot([westo.temp[G117_idx],12000], [spec_resid[G117_idx], 300], 'k-')
plt.plot([casta.temp[G117_idx],12000], [old_resid[G117_idx], 300], 'k-')
plt.text(12000, 280, "G117-B15A")
plt.plot([westo.temp[R548_idx],12000], [spec_resid[R548_idx], -650], 'k-')
plt.plot([casta.temp[R548_idx],12000], [old_resid[R548_idx], -650], 'k-')
plt.text(12000, -730, "R548")

plt.ylabel("Temperature residual $T_{spec} - T_{astero}$  (K)")
plt.xlabel("Solution Temperature (K)")
#plt.xticks([],[])

plt.legend()
#plt.show
#plt.close()

############################################

plt.figure(500)
plt.scatter(westo.mass, spec_residm, c=westo.S, cmap=cmap_use,alpha=0.7,label="Hall 2022")
plt.scatter(casta.mass,old_residm, c= 'b', marker = '^', alpha = 0.5, label = "Castanheira et. el. 2009")
#plt.show()

cbar=plt.colorbar()
cbar.set_label("S Value")

plt.plot([westo.mass[G117_idx],0.6], [spec_residm[G117_idx], 0.2], 'k-')
plt.plot([casta.mass[G117_idx],0.6], [old_residm[G117_idx], 0.2], 'k-')
plt.text(0.6, 0.2, "G117-B15A")
plt.plot([westo.mass[R548_idx],0.6], [spec_residm[R548_idx], -0.2], 'k-')
plt.plot([casta.mass[R548_idx],0.6], [old_residm[R548_idx], -0.2], 'k-')
plt.text(0.6, -0.2, "R548")

plt.ylabel("Mass residual $M_{spec} - M_{astero}$  ($M_\odot$)")
plt.xlabel("Solution Mass ($M_\odot$)")

plt.legend()
#plt.show()
#plt.close()


#######################################################

plt.figure(100)
#plt.scatter(np.arange(0,len(old_resid)), old_resid, c = 'b', marker = "^", label = "Castanheira et al. 2011")
#plt.scatter(np.arange(0,len(spec_resid)), spec_resid, c = 'r', label = "Hall")
plt.scatter(old_residm, old_resid, c = 'b', marker = '^', alpha = 0.5, label= "Castanheira et al. 2009")
plt.scatter(spec_residm, spec_resid, c= westo.S, cmap=cmap_use,alpha = 0.7,label = "Hall 2022")
plt.xlim([-0.5,0.5])
plt.ylim([-2000,2000])


cbar=plt.colorbar()
cbar.set_label("S Value")

plt.plot([spec_residm[G117_idx],0.17], [spec_resid[G117_idx], 300], 'r-')
plt.plot([old_residm[G117_idx],0.17], [old_resid[G117_idx], 300], 'b-')
plt.text(0.17, 280, "G117-B15A")
plt.plot([spec_residm[R548_idx],-0.2], [spec_resid[R548_idx], -650], 'r-')
plt.plot([old_residm[R548_idx],-0.2], [old_resid[R548_idx], -650], 'b-')
plt.text(-0.26, -730, "R548")

plt.ylabel("Temperature residual $T_{spec} - T_{astero}$  (K)")
plt.xlabel("Mass residual $M_{spec}-M_{astero}$  ($M_\odot$)")
#plt.xticks([],[])

plt.legend()
#plt.show()
#plt.close()

##########################################################

plt.figure(200)
plt.scatter(casta_residm, casta_resid, c=westo.S, cmap = 'viridis_r', label = "Hall, 2022")
cbar=plt.colorbar()
cbar.set_label("S Value")
#plt.scatter(np.arange(0,len(westo_resid)), westo_resid)

plt.xlim([-0.5,0.5])
plt.ylim([-2000,2000])

plt.ylabel("Temperature residual $T_{Castanheira} - T_{Hall}$  (K)")
plt.xlabel("Mass residual $M_{Castanheira}-M_{Hall}$  ($M_\odot$)")

plt.plot([casta_residm[G117_idx],-0.1], [casta_resid[G117_idx], -900], 'k-')
plt.text(-0.2, -1000, "G117-B15A")

plt.plot([casta_residm[R548_idx], .2], [casta_resid[R548_idx], 500], 'k-')
plt.text(0.2, 630, "R548")

plt.show()
plt.close()

plt.figure(900)
plt.scatter(westo.hydrogen, westo.helium)
plt.show()



'''

for i in np.arange(0,len(spec)):
    print(spec.name[i], " & & [B] \\\\")


'''
