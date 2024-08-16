import matplotlib.pyplot as plt
from matplotlib.path import Path
import math
import sys
import pandas as pd
import numpy as np

""" First create the dataframe from minoutput """
cols = ["temp","mass","helium","hydrogen","sigma"]
df_orig = pd.read_table("minoutput",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float},engine="python")
df_new= pd.read_table("minoutput_n",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float},engine="python")

o=open("minoutput_f", "w")


for ind in df_new.index:
    #print(df_new['sigma'][ind])
    #print(df_orig[(df_orig['temp'] == df_new['temp'][ind]) & (df_orig['mass'] == df_new['mass'][ind]) & (df_orig['hydrogen'] == df_new['hydrogen'][ind]) & (df_orig['helium'] == df_new['helium'][ind])]["sigma"])
    df_new['sigma'][ind] = df_new['sigma'][ind] + df_orig[(df_orig['temp'] == df_new['temp'][ind]) & (df_orig['mass'] == df_new['mass'][ind]) & (df_orig['hydrogen'] == df_new['hydrogen'][ind]) & (df_orig['helium'] == df_new['helium'][ind])]["sigma"]
    o.write(str(df_new['temp'][ind]) + "    " + str(df_new['mass'][ind]) + "    200.0    " + str(df_new['helium'][ind]) + "    " + str(df_new['hydrogen'][ind]) + "    " + str(df_new['sigma'][ind]) + "\n")

o.close()
