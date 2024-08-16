import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np

cols = ["temp","mass","env","helium","hydrogen","sigma","prob"]
data = pd.read_csv("minoutput", header = None, names = cols, sep ="    |\t")
binspace = np.linspace(10600,200,12600)
plt.hist(data.mass)
plt.show()
