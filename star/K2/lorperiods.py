import matplotlib.pyplot as plt
from matplotlib.path import Path
import math
import sys
import pandas as pd
import numpy as np
import itertools as it
from contextlib import contextmanager
@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout

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

num_var = 0
num_dup = 0

for i in np.arange(1,50):
    string = "f_" + str(i) + "|f_" + str(i) + "a|f_" + str(i) + "b|f_" + str(i) + "c"
    tempdf = data[(data["ID"]=="f_"+str(i)) | (data["ID"]=="f_"+str(i)+"a") | (data["ID"]=="f_"+str(i)+"b") | (data["ID"]=="f_"+str(i)+"c")]
    tempdf = tempdf.reset_index()
    tempdf.is_copy = None
    if tempdf.empty == False:
        if len(tempdf) == 2:
            num_dup = num_dup+1
num_var = 2**num_dup
#print(num_var)

nonzero = True
if num_dup == 0:
    variations= np.array([1])
    nonzero = False
elif num_dup == 1:
    variations = np.array(list(it.product([1,2])))
elif num_dup == 2:
    variations = np.array(list(it.product([1,2],[1,2])))
elif num_dup == 3:
    variations = np.array(list(it.product([1,2],[1,2],[1,2])))
elif num_dup == 4:
    variations = np.array(list(it.product([1,2],[1,2],[1,2],[1,2])))
elif num_dup == 5:
    variations = np.array(list(it.product([1,2],[1,2],[1,2],[1,2],[1,2])))
else:
    print("YOU DONT HAVE THIS MANY DUPES YET:", num_dup)

#print(variations)
#print(np.array(list(it.product(lister))))

for num_arr in variations:
    print(num_arr)
    which_slot = 0
    final_data = pd.DataFrame(columns =cols)
    for i in np.arange(1,50):
        #print(i)
        string = "f_" + str(i) + "|f_" + str(i) + "a|f_" + str(i) + "b|f_" + str(i) + "c"
        tempdf = data[(data["ID"]=="f_"+str(i)) | (data["ID"]=="f_"+str(i)+"a") | (data["ID"]=="f_"+str(i)+"b") | (data["ID"]=="f_"+str(i)+"c")]
        tempdf = tempdf.reset_index()
        tempdf.is_copy = None
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
                if second["LLSper_err"] != "...":
                    second["LLSper_err"] = float(second["LLSper_err"])
                if first["LLSAmp_err"] != "...":
                    first["LLSAmp_err"] = float(first["LLSAmp_err"])
                if second["LLSAmp_err"] != "...":
                    second["LLSAmp_err"] = float(second["LLSAmp_err"])
                new = pd.Series(dtype = 'float64').reindex_like(second)
                
                if num_arr[which_slot] == 1:
                    new = first
                else:
                    new = second
                final_data = final_data.append(new, ignore_index=True)
                which_slot = which_slot + 1
            else:
                if tempdf["LLSper_err"][0] == "...":
                        tempdf["LLSper_err"][0] = 0
                final_data = final_data.append(tempdf, ignore_index=True)

    #print(final_data)

    if nonzero == True:
        file_path = filename+"_"
        j = 0
        while j < num_dup:
            file_path = file_path + str(num_arr[j])
            j = j+1
        file_path = file_path + ".out"
        #file_path = filename +"_" + str(num_arr[0]) + str(num_arr[1]) + str(num_arr[2]) + ".out"
    else:
        file_path = filename + ".out"
    #sys.stdout = open(file_path, "w")
    with open(file_path, "w") as f:
        with stdout_redirected(f):
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
