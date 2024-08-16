import matplotlib.pyplot as plt
import math
import sys
import pandas as pd
import numpy as np
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from astropy.io.votable import parse
import os
import sys
import astroquery
import functions as fn
from astroquery.gaia import Gaia
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from astropy import units as u

def normalize(value, col):
    val = (value - min(col)) / (max(col) - min(col)) * 100
    #val = value
    return val



"""To get the data from GAIA"""
votable = VOTableFile()
resource = Resource()
votable.resources.append(resource)
table = Table(votable)
resource.tables.append(table)
table.fields.extend([
                Field(votable, name="ID", ucd="meta.id;phys.atmol.configuration", datatype="char", arraysize="13*"),
                Field(votable, name="RA", ucd="pos.eq.ra", ref="J2000", datatype="double", width="10", precision="6", unit="deg"),
                Field(votable, name="DEC", ucd="pos.eq.dec", ref="J2000", datatype="double", width="10", precision="6", unit="deg"),
                Field(votable, name="PM_RA", datatype="double", width="10", precision="6"),
                Field(votable, name="PM_DEC", datatype="double", width="10", precision="6"),
                Field(votable, name="PARALLAX", datatype="double", width="10", precision="6"),
                Field(votable, name="RADIAL_VELOCITY", datatype="double", width="10", precision="6")])

#FILL IN TABLE
#table.array[i] = (x, kRA[i], kDec[i], 0,0,0,0)

k2 = open("spec", "r")
lines = k2.readlines()

table.create_arrays(len(lines))
i = 0
for line in lines:
    temp_Series = pd.Series(line)
    temp_Series = temp_Series.str.split(pat = "\t")
    temp_List = temp_Series[0]
    
    print(temp_List[2])
    coord = SkyCoord(temp_List[2], unit=(u.hourangle, u.deg))
    print(coord)
    table.array[i] = (temp_List[0], coord.ra.degree, coord.dec.degree, 0,0,0,0)
    i += 1

votable.to_xml("new_votable.xml")
os.system("./curlcommand")
results = parse("gaiadata.vot")
worktable = results.get_first_table()
data = worktable.array
#print(type(data))

df = pd.DataFrame(columns = ["gID","ra","ra_error","dec","dec_error","parallax","parallax_error","g_mag","bp_mag","rp_mag","bp_rp","kID"])

for arr in data:
    #print(type(list(arr.tolist())))
    to_append=list(arr.tolist())
    to_append = to_append[:-7]
    a_series = pd.Series(to_append, index = df.columns)
    df = df.append(a_series, ignore_index=True)
    #print(arr[11],arr[7],arr[8],arr[9], arr[5], arr[6])

#print(df)




"""READING GAIA MODELS"""
models = fn.get_koester("models/SDSSGBRFN_DA_2020.amags")
#models = models[(models["Teff"] > 10600) & (models["Teff"] < 12600)]
models = models.reset_index()

gaiamodel = open("gaia_model_fit", "w")

for index, row in df.iterrows():
    Smin = 0
    if row["parallax"] is not None: 
        G_absmag  = row["g_mag"]  - 5.0 * math.log10(1.0 / abs(row["parallax"]) * 1000.0) + 5.0
        Bp_absmag = row["bp_mag"] - 5.0 * math.log10(1.0 / abs(row["parallax"]) * 1000.0) + 5.0
        Rp_absmag = row["rp_mag"] - 5.0 * math.log10(1.0 / abs(row["parallax"]) * 1000.0) + 5.0
        row_norm_G  = normalize(G_absmag,  models["G"])
        row_norm_Bp = normalize(Bp_absmag, models["Bp"])
        row_norm_Rp = normalize(Rp_absmag, models["Rp"])
        #print(row_norm_G, row_norm_Bp, row_norm_Rp)
        for modind, modrow in models.iterrows():
            mod_norm_G  = normalize(modrow["G"],  models["G"])
            mod_norm_Bp = normalize(modrow["Bp"], models["Bp"])
            mod_norm_Rp = normalize(modrow["Rp"], models["Rp"])
            #S = np.sqrt( (modrow["G"] - row["g_mag"])**2 + (modrow["Bp"] - row["bp_mag"])**2 + (modrow["Rp"] - row["rp_mag"])**2)
            #S = np.sqrt((mod_norm_G-row_norm_G)**2/row_norm_G + (mod_norm_Bp-row_norm_Bp)**2/row_norm_Bp + (mod_norm_Rp-row_norm_Rp)**2/row_norm_Rp)
            S = np.sqrt((mod_norm_G-row_norm_G)**2 + (mod_norm_Bp-row_norm_Bp)**2 + (mod_norm_Rp-row_norm_Rp)**2)
            if S < Smin or modind == 0:
                Smin = S
                ind = modind
                series = modrow
        print(row["kID"], Smin, series["Teff"], series["M/Msun"])
        gaiamodel.write(str(row["kID"]) + " " + str(Smin) + " " + str(series["Teff"]) + " " + str(series["M/Msun"]) + "\n")
    else:
        print(row["kID"], "parallax is NONE")
        gaiamodel.write(str(row["kID"]) + " " + " " + " " + "\n")

k2.close()



