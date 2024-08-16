import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import functions as fn



spec = fn.get_spec_K2("spec")

spec = spec.dropna()
spec = spec.reset_index()

for i in np.arange(0,len(spec),2):
    if i != len(spec)-1:
        print(spec.name[i], " & ", spec.temp[i], " & ", "{:.2f}".format(spec.mass[i]),"&", spec.name[i+1], "&", spec.temp[i+1], "&", "{:.2f}".format(spec.mass[i+1]), "\\\\")
    else:
        print(spec.name[i], "&",spec.temp[i],"&","{:.2f}".format(spec.mass[i]), "&","&","&","\\\\")
