import pandas as pd
import sys

data = pd.read_csv(sys.argv[1])

f = open("weston_ast", "a")

f.write(sys.argv[1][15:(len(sys.argv[1])-4)])
f.write('\n')


for index, row in data.iterrows():
    f.write(str(row.temp) + " & " + "{:.3f}".format(row.mass * 0.001) + " & " + str(row.h) + " " + str(row.he) + " & " + str(row.s) + " & " +str(row.members) + " & 1 \n")

f.close()
