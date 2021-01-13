

import matplotlib.pyplot as plt
import numpy as np
import json

def cs_to_gsf(Eg, data):
    # input in MeV and milibarn -> use this conversion factor.
    exp = 8.674e-8
    return data*exp/Eg

def extract_dataset(data, x_i,y_i,yerror_i):
    """ Extracting data from input files from MAMA, adding them to useful arrays."""
    x = []; y = [] ; yerror = []
    
    for j in range(len(data)):
        y.append(data[j][y_i]) # MeV
        yerror.append(data[j][yerror_i]) # MeV
        x.append(data[j][x_i])

    x = np.array(x) ; y = np.array(y) ; yerror = np.array(yerror)
    return x,y,yerror

def quickplot(data,x_i,y_i,yerror_i, millibarn=True):
    """ To quickly plot JSON files from exfor. If c.s. given in barns (instead of mb), add millibarn=False.""" 
    x = []; y = [] ; yerror = []
    if millibarn==True:
        conv = 1e0
    else:
        conv = 1e3
    for j in range(len(data)):
        y.append(data[j][y_i]*conv)
        yerror.append(data[j][yerror_i]*conv)
        x.append(data[j][x_i])

    x = np.array(x) ; y = np.array(y) ; yerror = np.array(yerror)
    gsf = cs_to_gsf(x, y)
    gsf_err = cs_to_gsf(x,yerror)
    plt.errorbar(x, gsf, yerr=gsf_err, x_err=None, fmt="*-", label="186W(g,x)")


#  MY DATA extracted:
# *************************************************************************** #
# *****************    (a,d) data points    **********************************#

a0_d = -0.8875
a1_d = 0.2480

strength_nrm_d = np.genfromtxt("../d_mama/strength.nrm")
strength_d = strength_nrm_d[:28]
strength_err_d = strength_nrm_d[29:]
n_d = len(strength_d)

energy_d = np.zeros(n_d)
for i in range(n_d):
    energy_d[i] = a0_d + a1_d*i

# (a,d) extrapolation
trans_raw_d = np.genfromtxt("../d_mama/transext.nrm")
n_d_t=len(trans_raw_d)
trans_d=np.zeros(n_d_t)
energy_trans_d=np.zeros(n_d_t)
for i in range(n_d_t):
    energy_trans_d[i] = a0_d + a1_d*i
    trans_d[i] = trans_raw_d[i]/(2*3.14*energy_trans_d[i]**3)



# *************************************************************************** #
# *****************    (a,t) data points    **********************************#

a0_t = -0.8875
a1_t = 0.2480

strength_nrm_t = np.genfromtxt("../t_mama/strength.nrm")
strength_t = strength_nrm_t[:26]
strength_err_t = strength_nrm_t[27:]
n_t = len(strength_t)
energy_t = np.zeros(n_t)

for i in range(n_t):
    energy_t[i] = a0_t + a1_t*i

# (a,t) extrapolation
trans_raw_t = np.genfromtxt("../t_mama/transext.nrm")
n_d_t = len(trans_raw_t)
trans_t = np.zeros(n_d_t)
energy_trans_t = np.zeros(n_d_t)
for i in range(n_d_t):
    energy_trans_t[i] = a0_t + a1_t*i
    trans_t[i] = trans_raw_t[i]/(2*3.14*energy_trans_t[i]**3)




# *************************************************************************** #
# *****************    External data     *************************************#


# Quickplot!



"""
with open("186W_load1.json") as L:
    data_186W = json.load(L)
datasets_186W=data_186W["datasets"]

quickplot(datasets_186W[0]["data"], 2,0,1)
quickplot(datasets_186W[1]["data"], 2,0,1)
quickplot(datasets_186W[2]["data"], 2,0,1)

#barns:
quickplot(datasets_186W[3]["data"], 2,0,1, millibarn=False)

quickplot(datasets_186W[4]["data"], 2,0,1)
quickplot(datasets_186W[5]["data"], 2,0,1)
quickplot(datasets_186W[6]["data"], 3,0,1)
"""


### DATAAA from Exfor. 187Re(g,x) to plot with my data.


with open("187Re_photo_load1.json") as K:
    data_187Re = json.load(K)
datasets_187Re=data_187Re["datasets"]


# Dataset 1
Eg_dataset1, gsf_dataset1, gsf_err_dataset1 =  extract_dataset(datasets_187Re[0]["data"], 2, 0, 1)

gsf_dataset1 = cs_to_gsf(Eg_dataset1, gsf_dataset1)
gsf_err_dataset1 = cs_to_gsf(Eg_dataset1, gsf_err_dataset1)

plt.errorbar(Eg_dataset1, gsf_dataset1, yerr=gsf_err_dataset1, x_err=None, fmt="*-", color="#CA5518", label="187Re(g,x)")


# Dataset 2

Eg_dataset2, gsf_dataset2, gsf_err_dataset2 =  extract_dataset(datasets_187Re[1]["data"], 3, 0, 1)

gsf_dataset2 = cs_to_gsf(Eg_dataset2, gsf_dataset2)
gsf_err_dataset2 = cs_to_gsf(Eg_dataset2, gsf_err_dataset2)

plt.errorbar(Eg_dataset2, gsf_dataset2, yerr=gsf_err_dataset2, x_err=None, fmt="*-", color="#1A1118", label="187Re(g,x)")

# ***************** Dataset 185Re ***************************

with open("185Re.json") as J:
    data_185Re = json.load(J)
dataset_185Re=data_185Re["datasets"]


Eg_185Re, gsf_185Re, gsf_err_185Re =  extract_dataset(dataset_185Re[0]["data"], 2, 0, 1)

gsf_185Re= cs_to_gsf(Eg_185Re, gsf_185Re)
gsf_err_185Re = cs_to_gsf(Eg_185Re, gsf_err_185Re)

plt.errorbar(Eg_185Re, gsf_185Re, yerr=gsf_err_185Re, x_err=None, fmt="*-", color="#F494cc", label="185Re(g,x)")




# *************************************************************************** #
# *****************   Plot               *************************************#

# Draw data and errorbars
plt.errorbar(energy_d, strength_d, yerr=strength_err_d[:-1], x_err=None, fmt="*", color="#3B5249", label="(a,d)188Re")
plt.plot(energy_trans_d[:80], trans_d[:80], color="#75FF33")

plt.errorbar(energy_t, strength_t, yerr=strength_err_t[:-1], x_err=None, fmt="*", color="#D65108", label="(a,t)187Re")
plt.plot(energy_trans_t[:80], trans_t[:80], color="#FFBD33")

plt.title("gamma-ray SF for both (a,d) and (a,t) with extrapolations.")
plt.ylabel("gSF [1/MeV]")
plt.xlabel("gamma energy [MeV]")
plt.legend()
#plt.ylim(5e-9, 5e-5) #np.min(strength_d)*0.1, np.max(strength_d)*10)
plt.grid("on")
plt.yscale("log")
plt.show()

