import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np

cols = ["temp","mass","env","helium","hydrogen","sigma","prob"]
data = pd.read_csv("minoutput", header = None, names = cols, sep ="    |\t")
binspace = np.linspace(10600,200,12600)

print(data.mass)
print(data.temp)
plt.plot(data.temp, data.mass, ".")
plt.xlabel("Temperature (K)")
plt.ylabel("Mass ($M_o$ * 1000")
plt.ylim(500,800)
plt.show()
