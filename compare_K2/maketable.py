import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
import functions as fn


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "weston_ast_adj"

table = open('k2_solutions', 'r')
tablelines = table.readlines()


df = pd.read_table(filename, header = None, sep= "&", names = ["ID", "temp", "mass","vals", "S", "etc", "erc"])
print(df)
table = open("table", "w")
for index, row in df.iterrows():
    hydro = float(row[3][0:6]) * 0.01
    helio = float(row[3][6:]) * 0.01
    temp = []
    mass = []

    for l in np.arange(0,len(tablelines)):
        if tablelines[l] == row[0].strip() + "\n" or tablelines[l] == row[0].strip()+"_final\n":
            inc = 1
            while l+inc < len(tablelines) and tablelines[l+inc].find('&') > 1:
                temp_Series = pd.Series(tablelines[l+inc], )
                temp_Series = temp_Series.str.split(pat = "&")
                temp_List = temp_Series[0]
                #print(temp_List)
                #print(float(temp_List[0]), float(temp_List[1]), float(temp_List[2]), float(temp_List[3]))
                #print(row["temp"], row["mass"], hydro, helio)
                if float(temp_List[0]) == row["temp"] and float(temp_List[1]) == row["mass"] and float(temp_List[2]) == hydro and float(temp_List[3]) == helio:
                    #print("temp")
                    modecs = temp_List[5]


                inc = inc+1
    table.write(str(row[0]) + " & " + str(row[1]) + " & " + str(row[2]) + " & " + str(format(hydro,".3f")) + " & " + str(format(helio,".3f")) + " & " + str(modecs) + "\n")







