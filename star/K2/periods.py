import matplotlib.pyplot as plt
from matplotlib.path import Path
import math
import sys
import pandas as pd
import numpy as np
#from function import get_plots
#from function import get_unc

def prop_mult(val_1, err_1, val_2, err_2):
    result = math.sqrt((err_1/val_1)**2 + (err_2/val_2)**2)
    return result

def prop_add(err_1, err_2):
    result = math.sqrt(err_1**2 + err_2**2)
    return result

def propogate_err(first, second):
    X = first["LLSper"] * first["LLSAmp"]
    Y = second["LLSper"] * second["LLSAmp"]
    #print(type(first["LLSAmp_err"]))
    Z = X+Y
    R = first["LLSAmp"] + second["LLSAmp"]
    Q = Z / R
    dQ = np.nan
    #print(type(first["LLSper_err"]), type(first["LLSAmp"]), type(first["LLSAmp_err"]))
    if type(first["LLSper_err"]) != str and type(second["LLSper_err"]) != str:
        dX = prop_mult(val_1 = first["LLSper"], err_1 = first["LLSper_err"], val_2 = first["LLSAmp"], err_2 = first["LLSAmp_err"])
        dY = prop_mult(val_1 = second["LLSper"], err_1 = second["LLSper_err"], val_2 = second["LLSAmp"], err_2 = second["LLSAmp_err"])
        dZ = prop_add(dX, dY)
        dR = prop_add(first["LLSAmp_err"], second["LLSAmp_err"])
        dQ = prop_mult(Z, dZ, R, dR)
    return Q, dQ

pd.set_option('mode.chained_assignment', None)

""" First create the dataframe from minoutput """
#cols = ["temp","mass","helium","hydrogen","sigma"]
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = input("Name:")

cols =  ["IC", "ID", "LLSper", "LLSper_err", "LLSFreq", "LLSFreq_err", "LLSAmp", "LLSAmp_err", "LLSPhase", "LLSPhase_err", "LorPer", "LorPer_err", "LorHWHM", "LorPower", "Splitting", "ell", "m"]
data = pd.read_table(filename, sep = "\s+|\t+|\s+\t+|\t+\s+", names=cols, header= None, skiprows = 1, engine="python")
#print(data)
data = data[data["Splitting"].str.contains("harm")==False]
data = data[data["LLSper"] != '...']
#data = data.reset_index()
#print(data)

data["LLSper"] = data["LLSper"].apply(pd.to_numeric)

if data["LLSAmp"][data.index[0]] != "...":
    data["LLSAmp"] = data["LLSAmp"].apply(pd.to_numeric)
data[["IC", "ID"]] = data[["IC", "ID"]].astype(str)


final_data = pd.DataFrame(columns =cols)

for i in np.arange(1,50):
    #print(i)
    string = "f_" + str(i) + "|f_" + str(i) + "a|f_" + str(i) + "b|f_" + str(i) + "c"
    tempdf = data[(data["ID"]=="f_"+str(i)) | (data["ID"]=="f_"+str(i)+"a") | (data["ID"]=="f_"+str(i)+"b") | (data["ID"]=="f_"+str(i)+"c")]
    tempdf = tempdf.reset_index()
    tempdf.is_copy = None
    """ 
    if len(tempdf) > 1:
        print("\n", "\n", i)
        string = "_" +  str(i) + "a|_" + str(i) + "b|_" + str(i) + "c"
        tempdf = tempdf[tempdf["ID"].str.contains(string)==True]
        tempdf = tempdf.reset_index()
        tempdf.is_copy = None
    """
    if tempdf.empty == False:
        #print(string)
        #print(len(tempdf))
        #print(tempdf) 
        if len(tempdf) == 3:
            #print(tempdf.loc[1])
            tempSeries = tempdf.loc[1]
            tempSeries.is_copy = None
            if tempSeries["LLSper_err"] == "...":
                tempSeries["LLSper_err"] = 0
            tempSeries["ID"] = tempSeries["ID"][:-1]
            final_data = final_data.append(tempSeries, ignore_index = True)
        
        elif len(tempdf) == 2:
            first = tempdf.loc[0]
            #print(first)
            second = tempdf.loc[1]
            if first["LLSper_err"] != "...":
                first["LLSper_err"] = float(first["LLSper_err"])
            else:
                first["LLSper_err"] = 0
            if second["LLSper_err"] != "...":
                second["LLSper_err"] = float(second["LLSper_err"])
            else:
                second["LLSper_err"] = 0
            if first["LLSAmp_err"] != "...":
                first["LLSAmp_err"] = float(first["LLSAmp_err"])
            if second["LLSAmp_err"] != "...":
                second["LLSAmp_err"] = float(second["LLSAmp_err"])
            new = pd.Series(dtype = 'float64').reindex_like(second)
            new["IC"] = str(first["IC"])
            new["ID"] = first["ID"][:-1]
            #new["LLSper"], new["LLSper_err"] = propogate_err(first,second)
            #final_data = final_data.append(new, ignore_index=True)
            if first["LLSper_err"] < second["LLSper_err"]:
                new = first
            else:
                new = second
            final_data = final_data.append(new, ignore_index=True)
        else:
            if tempdf["LLSper_err"][0] == "...":
                    tempdf["LLSper_err"][0] = 0
            final_data = final_data.append(tempdf, ignore_index=True)

print(final_data)


file_path = filename+".out"
sys.stdout = open(file_path, "w")
print(final_data[["LLSper", "LLSper_err"]].to_string(index = False, header=False))
'''
with open(filename + ".out", "a") as o:
    o.write(final_data)
'''


'''
plt.figure(100)
for Per, Amp in zip(data.LLSper, data.LLSAmp):
    plt.plot([Per, Per], [0, Amp])
plt.show()
'''
