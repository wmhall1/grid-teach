'''
Author: Weston Hall

These are functions that are used in some of the other plotting routines
in this directory.
'''

import math
import pandas as pd
import numpy as np


#
#Flattens a pandas DataFrame to 3 arrays temps/masses/sigmas for ease of plotting
#
# Inputs : pandas dataframe containing data from minoutput,
#           example: pd.read_table("../minoutput",sep = "   |    |\t", header = None, names = cols, usecols = [0,1,3,4,5],dtype={'temp':float},engine="python")
#
# Outputs : A list of lists containing [temps, masses, sigmas]
#
def get_plots(data):
    
    #get minimum sigma and index
    #print(data.mass)
    #print(data.temp)
    min_value = min(data.sigma)
    sigmas = data.sigma.tolist()
    #print(type(sigmas))
    min_index = sigmas.index(min_value)

    """ Get frequency (modes) of models with the same mass/temp """
    #initialize lists
    temps = []
    masses = []
    freq = []
    temps.append(float(data.temp[0]))
    masses.append(data.mass[0])
    freq.append(1)

    #For each row in the dataframe
    j = 1
    for i in range(1,len(data.temp)):
        #Check if its the same as previous, if it is then increment the freq for that point
        if data.temp[i] == temps[j-1] and data.mass[i] == masses[j-1]:
            freq[j-1] = freq[j-1] + 1
        #If it isn't the same, add new point, start new freq, and increment
        else:
            temps.append(float(data.temp[i]))
            masses.append(data.mass[i])
            freq.append(1)
            j = j + 1
    #find the max frequency
    max_index = freq.index(max(freq))


    """ FINDING MINIMUM SIGMAS """
    #Initialize a list of lists. For each point, it will store a list of
    #the sigmas associated with those points in the dataframe
    sigmas = [ [] for _ in range(len(temps)) ]

    data_mass = data.mass.tolist()
    data_temp = data.temp.tolist()

    i = 0
    #Assign each list in sigmas to be the list from the dataframe meeting
    #the condition for each point
    for i in range(0,len(sigmas)):
        sigmas[i] = data.sigma[ (data["mass"] == masses[i]) & (data["temp"] == temps[i]) ].tolist()
    #print(sigmas)

    #Create a new list of just the minimums
    sigma_mins = []
    for s in sigmas:
        sigma_mins.append(min(s))

    return [temps, masses, sigma_mins]

#
# Calculates the internal uncertainty on a point
#
# Inputs : pandas data and the index to calculate uncertainty at
#
# Outputs : List containing upper and lower errors [[temperature lower, temperature upper], [ mass lower, mass upper] ]
#
def get_unc(data, min_index):
    """ Calcualte Sigma error """

    int_s_temp_up = int_s_temp_do = int_s_mass_up = int_s_mass_do = 0

    for i in range(0, len(data.temp)):
        if data.temp[i] == data.temp[min_index]+50 and data.mass[i] == data.mass[min_index] and data.helium[i] == data.helium[min_index] and data.hydrogen[i] == data.hydrogen[min_index]:

            int_s_temp_up = math.sqrt(50**2 / (data.sigma[i] - data.sigma[min_index]))

        if data.temp[i] == data.temp[min_index]-50 and data.mass[i] == data.mass[min_index] and data.helium[i] == data.helium[min_index] and data.hydrogen[i] == data.hydrogen[min_index]:
            int_s_temp_do = math.sqrt(50**2 / (data.sigma[i] - data.sigma[min_index]))

        if data.temp[i] == data.temp[min_index] and data.mass[i] == data.mass[min_index]-5 and data.helium[i] == data.helium[min_index] and data.hydrogen[i] == data.hydrogen[min_index]:
            int_s_mass_do = math.sqrt(5**2 / (data.sigma[i] - data.sigma[min_index]))

        if data.temp[i] == data.temp[min_index] and data.mass[i] == data.mass[min_index]+5 and data.helium[i] == data.helium[min_index] and data.hydrogen[i] == data.hydrogen[min_index]:
            int_s_mass_up = math.sqrt(5**2 / abs(data.sigma[i] - data.sigma[min_index]))


    int_temp_err = [[int_s_temp_do], [int_s_temp_up]]
    int_mass_err = [[int_s_mass_do], [int_s_mass_up]]

    return [int_temp_err, int_mass_err]
#
# Same as above but for H and He instead of temp mass
#
def get_layer_unc(data, min_index):
    """ Calcualte Sigma error """

    int_s_h_up = int_s_h_do = int_s_he_up = int_s_he_do = 0

    for i in range(0, len(data.temp)):
        if data.hydrogen[i] == data.hydrogen[min_index]+25 and data.helium[i] == data.helium[min_index] and data.mass[i] == data.mass[min_index] and data.temp[i] == data.temp[min_index]:

            int_s_h_up = math.sqrt(25**2 / (data.sigma[i] - data.sigma[min_index]))

        if data.temp[i] == data.temp[min_index] and data.mass[i] == data.mass[min_index] and data.helium[i] == data.helium[min_index] and data.hydrogen[i] == data.hydrogen[min_index]-25:
            int_s_h_do = math.sqrt(25**2 / (data.sigma[i] - data.sigma[min_index]))

        if data.temp[i] == data.temp[min_index] and data.mass[i] == data.mass[min_index] and data.helium[i] == data.helium[min_index]-25 and data.hydrogen[i] == data.hydrogen[min_index]:
            int_s_he_do = math.sqrt(25**2 / (data.sigma[i] - data.sigma[min_index]))

        if data.temp[i] == data.temp[min_index] and data.mass[i] == data.mass[min_index] and data.helium[i] == data.helium[min_index]+25 and data.hydrogen[i] == data.hydrogen[min_index]:
            int_s_he_up = math.sqrt(25**2 / abs(data.sigma[i] - data.sigma[min_index]))


    int_h_err = [[int_s_h_do], [int_s_h_up]]
    int_he_err = [[int_s_he_do], [int_s_he_up]]

    return [int_h_err, int_he_err]

