

import matplotlib.pyplot as plt
import numpy as np
import json

import stylesheet
from loading_data_gSF import load_data as load

"""
Plotting the gSF from this experiment. Both (a,t) and (a,d).
"""


data_d, energy_trans_d, trans_d = load("../mama_d/recommended_values/", "d", return_trans=True)
energy_d = data_d[:,0]
strength_d = data_d[:,1]
strength_err_d = data_d[:,2]

data_t, energy_trans_t, trans_t = load("../mama_t/recommended_values/", "t", return_trans=True)
energy_t = data_t[:,0]
strength_t = data_t[:,1]
strength_err_t = data_t[:,2]


# *************************************************************************** #
# *****************   Plot               *************************************#

n_trans = 82

plt.figure(figsize=(11,7))

# Draw data and errorbars
plt.errorbar(energy_d, strength_d, yerr=strength_err_d, x_err=None, fmt="D", color=stylesheet.d_color_data, label="(a,d) 188Re")
plt.plot(energy_trans_d[:n_trans], trans_d[:n_trans], color=stylesheet.d_color_inter)

plt.errorbar(energy_t, strength_t, yerr=strength_err_t, x_err=None, fmt="s", color=stylesheet.t_color_data, label="(a,t) 187Re")
plt.plot(energy_trans_t[:n_trans], trans_t[:n_trans], color=stylesheet.t_color_inter)


plt.xlabel("E$_\gamma$ [MeV]", size=18) 
plt.ylabel(" $\gamma$-ray strength function [MeV$^{-3}$]", size=18)
plt.legend(loc="upper left", prop={"size":16})
plt.xlim(-0.1, 6.5)
plt.ylim(5e-9, 2e-6)
plt.grid("on")
plt.yscale("log")
plt.savefig("png/gSF_both.png")
plt.show()

