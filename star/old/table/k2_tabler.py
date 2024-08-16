import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np


data = pd.read_table("periods_k2", names = ['name', 'period', 'amp'], sep = "&",header = None, engine="python")

names = data[data.name != " "]

name_list = names.index.tolist()

print(len(data))
new_df = pd.DataFrame(columns=['name','period','amp'])
spacer = pd.Series([' ', ' ', ' '])

for i in np.arange(0,len(data)):
    size = len(data.amp[i])
    data.amp[i] = data.amp[i][:size-2]
    
    new_df = new_df.append(data.iloc[i], ignore_index=True)
    if i!= 184 and data.name[i+1] != " ":
        new_df = new_df.append(spacer, ignore_index=True)


print(new_df)

data = new_df

first = data.iloc[0:92]

second = data.iloc[92:185]
second = second.reset_index()

print(first)
print(second)
for i in np.arange(0,len(second)):
    if i < len(first):
        first_title = str(first.name[i]) + " & "+ str(first.period[i]) + " & "+ str(first.amp[i])
        second_title = str(second.name[i]) + " & "+ str(second.period[i]) + " & "+ str(second.amp[i])
        print(first_title, "&", second_title, "\\\\")
