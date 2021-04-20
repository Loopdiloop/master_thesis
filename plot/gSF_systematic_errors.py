
import matplotlib.pyplot as plt
import numpy as np
import json
import sys

import stylesheet
from loading_data_gSF import load_data as load


try:
    reaction = str(sys.argv[1])
except:
    reaction = "t"

if reaction == "d":
    path = "../mama_d/"

elif reaction == "t":
    path = "../mama_t/"
    data_altgamma = load(path+"alternative_gamma/", reaction)

else:
    raise ValueError("Lol, wrong input.")



data_rec = load(path+"recommended_values/", reaction) #Reccomended values.
#upper_data = load(path+"higher_estimate/", reaction)
#lower_data = load(path+"lower_estimate/", reaction)

data_D0_low = load(path+"D0_low/", reaction)
data_D0_high = load(path+"D0_high/", reaction)

data_gamma_low = load(path+"gamma_low/", reaction)
data_gamma_high = load(path+"gamma_high/", reaction)

data_sigma_06 = load(path+"sigma_06/", reaction)
data_sigma_07 = load(path+"sigma_07/", reaction)
data_sigma_09 = load(path+"sigma_09/", reaction)
data_sigma_10 = load(path+"sigma_10/", reaction)





def term(f):
    f_rec=data_rec[:,1]
    return ((f[:,1]-f_rec)/f_rec)**2

STD_gSF_high = np.sqrt((data_rec[:,1]**2 
    * (  term(data_D0_low) + term(data_gamma_high)  + term(data_sigma_09)
    + (data_rec[:,2]/data_rec[:,1])**2)))

STD_gSF_highest = np.sqrt((data_rec[:,1]**2 
    * (  term(data_D0_low) + term(data_gamma_high)  + term(data_sigma_10)
    + (data_rec[:,2]/data_rec[:,1])**2)))

STD_gSF_low = np.sqrt((data_rec[:,1]**2 
    * (term(data_D0_high) + term(data_gamma_low)  + term(data_sigma_07)
    + (data_rec[:,2]/data_rec[:,1])**2 )))

STD_gSF_lowest = np.sqrt((data_rec[:,1]**2 
    * (term(data_D0_high) + term(data_gamma_low)  + term(data_sigma_06)
    + (data_rec[:,2]/data_rec[:,1])**2 )))

f_high_stk = data_rec[:,1] + data_rec[:,2]
f_low_stk = data_rec[:,1] - data_rec[:,2]

f_high = data_rec[:,1] + STD_gSF_high
f_low = data_rec[:,1] - STD_gSF_low

f_highest = data_rec[:,1] + STD_gSF_highest
f_lowest = data_rec[:,1] - STD_gSF_lowest

# *************************************************************************** #
# *****************   Plot               *************************************#


plt.figure(figsize=(11,7))

# Recommended
energy = data_rec[:,0]
strength = data_rec[:,1]
strength_err = data_rec[:,2]

"""
# If you want to plot all approximations for visual control:
plt.plot(energy, data_D0_high[:,1],label="D0_high")
plt.plot(energy, data_D0_low[:,1],label="D0_low")
plt.plot(energy, data_gamma_low[:,1],label="Gamma_low")
plt.plot(energy,data_gamma_high[:,1],label="Gamma_high")
plt.plot(energy, data_sigma_06[:,1],label="Sigma_06")
plt.plot(energy, data_sigma_07[:,1],label="Sigma_07")
plt.plot(energy,data_sigma_09[:,1],label="Sigma_09")
plt.plot(energy,data_sigma_10[:,1],label="Sigma_10")
"""


color_outer = "#d6eaf8"
color_inner = "#aed6f1"

plt.fill_between(energy, f_highest, f_lowest, color=color_outer, label="$\sigma(S_n)$ reduction $0.8\pm 0.2$") 
plt.fill_between(energy, f_high, f_low, color=color_inner, label="$\sigma(S_n)$ reduction $0.8\pm 0.1$")#"lavender") 
#plt.plot(energy, f_high_stk, "--", color="slategrey", label="Statistical errors only")
#plt.plot(energy, f_low_stk, "--", color="slategrey")#, label="Statistical errors only")


if reaction == "t":
    # Altgamma
    energy_altgamma = data_altgamma[:,0]
    strength_altgamma = data_altgamma[:,1]
    strength_err_altgamma = data_altgamma[:,2]
    # Plotting the alternative gamma value (\approx 92)
    plt.errorbar(energy_altgamma, strength_altgamma, yerr=strength_err_altgamma, x_err=None, fmt="s", color="#547db6", label="Original recommended $<\Gamma_0>$.")

    plt.errorbar(energy, strength, yerr=strength_err, x_err=None, fmt="D", color="black", label="Data with recommended values")#, color=stylesheet.d_color_data, label="(a,d) 188Re")

elif reaction == "d":
    plt.errorbar(energy, strength, yerr=strength_err, x_err=None, fmt="D", color="black", label="Data with recommended values")#, color=stylesheet.d_color_data, label="(a,d) 188Re")

#plt.title("Systematic and statistical error of gSF for (a,%s)." % reaction)
plt.xlabel("E$_\gamma$ [MeV]", size=18) 
plt.ylabel(" $\gamma$-ray strength function [MeV$^{-3}$]", size=18)
plt.legend(loc="upper left")
#plt.xlim(-0.1, 6.5)
#plt.ylim(5e-9, 5e-6)
plt.grid("on")
plt.yscale("log")
plt.savefig("png/gSF_systematic_errors_%s.png"%reaction)
plt.show()

