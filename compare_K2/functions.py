import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
#from function import get_plots

def get_koester(filename):
    cols = ["Teff","log_g","M/Msun","u","g","r","i","z","G","Bp","Rp" ,"FUV" ,"NUV"] 
    data = pd.read_table(filename, skiprows=24, header=None, delim_whitespace=True, names = cols)
    data=data.reset_index()
    return data


def get_spec(filename):
    """ First create the dataframe from minoutput """
    data = pd.read_table(filename,sep = " ", header = None,dtype = str, engine="python")
    data = data.reset_index()
    run = data.loc[0]
    df = pd.DataFrame(index = data.index, columns = ["name", "temp", "logg", "mass", "ref"])
    for i in np.arange(0,len(data)):
        run = data.loc[i]
        df.name[i] = run[0]
        df.temp[i] = float(run[1]+run[2])
        df.logg[i] = float(run[5])
        df.mass[i] = float(run[8])
        df.ref[i] = int(run[11])
    return(df)

def get_romero(filename):
    data = pd.read_table(filename,sep = " ", header = None,dtype = str, engine="python")
    data = data.reset_index()
    run = data.loc[0]
    df = pd.DataFrame(index = data.index, columns = ["name", "temp", "logg", "mass"])
    for i in np.arange(0,len(data)):
        run = data.loc[i]
        df.name[i] = run[0]
        df.temp[i] = float(run[4]+run[5])
        df.logg[i] = float(run[1])
        df.mass[i] = float(run[8])
    return(df)

def get_westo(filename):
    data = pd.read_table(filename, sep = "&", header = None, dtype = str, engine = "python")
    data = data.reset_index()
    run = data.loc[0]
    df = pd.DataFrame(index = data.index, columns = ["name", "temp", "mass", "hydrogen", "helium", "S", "num","per"])
    for i in np.arange(0, len(data)):
        run = data.loc[i]
        if len(run[1]) > 1:
            df.name[i] = run[0].strip()
            df.temp[i] = float(run[1])
            df.mass[i] = float(run[2])
            df.hydrogen[i] = float(run[3][1:6]) *0.01
            df.helium[i] = float(run[3][7:12]) * 0.01
            df.S[i] = float(data[4][i])
            df.num[i] = float(run[5])
            df.per[i] = float(run[6])
    return(df)

def get_westo2(filename):
    data = pd.read_table(filename, sep = "&", header = None, dtype = str, engine = "python")
    data = data.reset_index()
    run = data.loc[0]
    df = pd.DataFrame(index = data.index, columns = ["name", "temp", "mass", "num","per"])
    for i in np.arange(0,len(data)):
        run = data.loc[i]
        if len(run[1]) > 1:
            df.name[i] = str(run[0].strip())
            df.temp[i] = float(run[1])
            df.mass[i] = float(run[2])
            df.num[i] = float(run[5])
            df.per[i] = float(run[6])
    #print(df.name)
    return(df)

def get_casta_spec(filename):
    data = pd.read_table(filename, sep = '\t', header = 0, dtype = str, engine = "python")
    df = pd.DataFrame(index = data.index, columns = ["name","temp","mass"])
    for i in np.arange(0,len(data)):
        df.name[i] = data.Name[i]
        df.temp[i] = float(data.SpecTemp[i])
        df.mass[i] = float(data.SpecMass[i])
    return(df)

def get_casta(filename):
    data = pd.read_table(filename, sep = "&", header = None, dtype =str, engine="python")
    df = pd.DataFrame(index = data.index, columns = ["name","temp","mass"])
    for i in np.arange(0,len(data)):
        run = data.loc[i]
        df.name[i] = str(run[0].strip())
        if float(run[1]) == 0:
            df.temp[i] = math.nan
        else:
            df.temp[i] = float(run[1])
        if float(run[2]) == 0:
            df.mass[i] = math.nan
        else:
            df.mass[i] = float(run[2])
    return(df)



def get_spec_K2(filename):
    """ First create the dataframe from minoutput """
    data = pd.read_table(filename,sep = "\t", header = None,dtype = str, engine="python")
    data = data.reset_index()
    run = data.loc[0]
    df = pd.DataFrame(index = data.index, columns = ["name", "temp", "mass"])
    for i in np.arange(0,len(data)):
        run = data.loc[i]
        df.name[i] = run[0].strip()
        df.temp[i] = float(run[15])
        #df.temp[i] = float(run[19])
        df.mass[i] = float(run[21])
    return(df)

def new_spec_K2(filename):
    """ First create the dataframe from minoutput """
    data = pd.read_table(filename,sep = "\t", header = None,dtype = str, engine="python")
    data = data.reset_index()
    run = data.loc[0]
    df = pd.DataFrame(index = data.index, columns = ["name", "temp1D","temp3D", "mass"])
    for i in np.arange(0,len(data)):
        run = data.loc[i]
        df.name[i] = run[0].strip()
        df.temp1D[i] = float(run[15])
        df.temp3D[i] = float(run[19])
        df.mass[i] = float(run[21])
    return(df)
