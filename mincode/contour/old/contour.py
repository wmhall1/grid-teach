import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np

cols = ["temp","mass","env","helium","hydrogen","sigma","prob"]
data = pd.read_csv("minoutput", header = None, names = cols, sep ="    |\t")
binspace = np.linspace(10600,200,12600)

print(data.mass)
print(data.temp)
min_value = min(data.sigma)
sigmas = data.sigma.tolist()
print(type(sigmas))
min_index = sigmas.index(min_value)


'''
def grid(x, y, z, resX=100, resY=100):
    "Convert 3 column data to matplotlib grid"
    xi = linspace(min(x), max(x), resX)
    yi = linspace(min(y), max(y), resY)
    Z = griddata(x, y, z, xi, yi)
    X, Y = meshgrid(xi, yi)
    return X, Y, Z
'''

#X, Y, Z = plt.grid(data.temp,data.mass,data.sigma)
plt.scatter(data.temp,data.mass,c=data.sigma)
plt.xlabel("Temperature (K)")
plt.xticks(np.arange(10600,12800,200))
plt.ylabel("Mass ($M_o$ * 1000)")
plt.ylim(500,1000)
cbar = plt.colorbar()
cbar.set_label("Sigma Value")
plt.plot(data.temp[min_index],data.mass[min_index],'r.')
plt.text(12800,1025, 'Sigma cutoff = '+str(math.ceil(max(data.sigma))), fontsize = 10)
plt.show()
