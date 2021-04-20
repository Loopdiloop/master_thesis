import matplotlib.pyplot as plt
import numpy as np
import sys

import stylesheet

# Counting NLD


plt.figure(figsize=(11,7))

color_outer = "#d6eaf8"
color_inner = "#aed6f1"

def a_t():

    reaction = "t"
    l0 = 3  # First point of data array with actual data.
    l1 = l0+20 # Last point of data array with actual data. 23
    l2 = 30 # First error value at l0. Actual length for data array vs. error array.
    l3 = l2+20 # Last position with error value. 50
    
    n = 28
    n_long = 405

    a0 = -0.8875
    a1 = 0.2480

    Bn = 7.360000 
    Bnerr = 0.001

    #reduction factor 0.8:
    rho_Bn = 1.439E+07
    rho_Bnerr = 1.464E+06

    rho_Bn_sig06 = 1.090E+07
    rho_Bn_sig07 = 1.264E+07
    rho_Bn_sig08 = rho_Bn
    rho_Bn_sig09 = 1.613E+07
    rho_Bn_sig10 = 1.787E+07


    rholev = np.genfromtxt("../mama_t/recommended_values/rholev.cnt")
    rhopaw = np.genfromtxt("../mama_t/recommended_values/rhopaw.cnt")
    fermigas = np.genfromtxt("../mama_t/recommended_values/fermigas.cnt")

    #fermi = fermigas
    energy_full = a0 + a1*np.linspace(0,n_long-1,n_long)
    energy = energy_full[l0:l1]

    #rhopaw
    rho = rhopaw[l0:l1]
    rhoerr = rhopaw[l2:l3]

    levels = rholev


    data_D0_low = np.genfromtxt("../mama_t/D0_low/rhopaw.cnt")[l0:l1]
    data_D0_high = np.genfromtxt("../mama_t/D0_high/rhopaw.cnt")[l0:l1]

    data_sigma_06 = np.genfromtxt("../mama_t/sigma_06/rhopaw.cnt")[l0:l1]
    data_sigma_07 = np.genfromtxt("../mama_t/sigma_07/rhopaw.cnt")[l0:l1]
    data_sigma_09 = np.genfromtxt("../mama_t/sigma_09/rhopaw.cnt")[l0:l1]
    data_sigma_10 = np.genfromtxt("../mama_t/sigma_10/rhopaw.cnt")[l0:l1]


    STD_NLD_high = np.sqrt((rho**2 * (  ((data_D0_low-rho)/rho)**2 + ((data_sigma_09-rho)/rho)**2 + (rhoerr/rho)**2  )))

    STD_NLD_highest = np.sqrt((rho**2 * (  ((data_D0_low-rho)/rho)**2 + ((data_sigma_10-rho)/rho)**2 + (rhoerr/rho)**2  )))

    STD_NLD_low = np.sqrt((rho**2 * (  ((data_D0_high-rho)/rho)**2 + ((data_sigma_07-rho)/rho)**2 + (rhoerr/rho)**2  )))
    
    STD_NLD_lowest = np.sqrt((rho**2 * (  ((data_D0_high-rho)/rho)**2 + ((data_sigma_06-rho)/rho)**2 + (rhoerr/rho)**2  )))

    f_high_stk = rho + rhoerr
    f_low_stk = rho - rhoerr

    f_high = rho + STD_NLD_high
    f_low = rho - STD_NLD_low

    f_highest = rho + STD_NLD_highest
    f_lowest = rho - STD_NLD_lowest


    print("low", STD_NLD_low)
    print("rho", rho)

    # *************************************************************************** #
    # *****************   Plot               *************************************#

    plt.fill_between(energy[:-1], f_highest[:-1], f_lowest[:-1], color=color_outer, label="$\sigma(S_n)$ red. fact. $0.8\pm 0.2$") 
    plt.fill_between(energy[:-1], f_high[:-1], f_low[:-1], color=color_inner, label="$\sigma(S_n)$ red. fact. $0.8\pm 0.1$")
    #plt.plot(energy, f_high_stk, "--", color="slategrey", label="Statistical errors only")
    #plt.plot(energy, f_low_stk, "--", color="slategrey")
    #print(f_low[-1], rho[-1], STD_NLD_low[-1])

    # Normalisation point at Bn
    
    plt.plot(Bn, rho_Bn_sig06, "D", color=color_outer, label="$\\rho$ w/ $\sigma(S_n)$ red. fact. $0.8 \pm 0.2$")
    plt.plot(Bn, rho_Bn_sig10, "D", color=color_outer)#, label="rho from neutron res. data")
    plt.plot(Bn, rho_Bn_sig07, "D", color=color_inner, label="$\\rho$ w/ $\sigma(S_n)$ red. fact. $0.8 \pm 0.1$")
    plt.plot(Bn, rho_Bn_sig09, "D", color=color_inner)#, label="rho from neutron res. data")
    
    plt.errorbar(Bn, rho_Bn, yerr=rho_Bnerr, xerr=None, fmt="D", color=stylesheet.t_color_inter, label="rho from neutron res. data")

    """
    plt.plot(energy, data_D0_low, label="D0_low")
    plt.plot(energy, data_D0_high, label="D0_high")

    plt.plot(energy, data_sigma_06, label="sigma_06")
    plt.plot(energy, data_sigma_07, label="sigma_07")
    plt.plot(energy, data_sigma_09, label="sigma_09")
    plt.plot(energy, data_sigma_10, label="sigma_10")
    """

    # Previously known levels
    plt.plot(energy_full[:len(levels)], levels, color=stylesheet.t_color_inter, label="Known levels")

    # CT model for inerpolation ----
    n0_CT = np.argmin(abs(energy_full-3.0))
    n1_CT = np.argmin(abs(energy_full-Bn-0.5))
    plt.plot(energy_full[n0_CT:n1_CT], fermigas[n0_CT:n1_CT], "--", color=stylesheet.t_color_inter, label="CT interpolation")

    #This experiment!
    plt.errorbar(energy[:-1], rho[:-1], yerr=rhoerr[:-1], xerr=None, fmt="s", color=stylesheet.t_color_data, label="Oslo data for 187Re")


########################################################################################################

def a_d(): #color = green

    reaction = "d"
    l0 = 3
    l1 = 25
    l2 = 32
    l3 = 54

    n = 30
    n_long = 404

    a0 = -0.8875
    a1 = 0.2480

    Bn = 5.871000
    Bnerr = 0.001
    rho_Bn = 4.649E+06
    rho_Bnerr = 1.674E+05

    
    rho_Bn_sig06 = 3.613E+06
    rho_Bn_sig07 = 4.130E+06
    rho_Bn_sig08 = rho_Bn
    rho_Bn_sig09 = 5.168E+06
    rho_Bn_sig10 = 5.688E+06
    
    rholev = np.genfromtxt("../mama_d/recommended_values/rholev.cnt")
    rhopaw = np.genfromtxt("../mama_d/recommended_values/rhopaw.cnt")
    fermigas = np.genfromtxt("../mama_d/recommended_values/fermigas.cnt")

    #fermi = fermigas
    energy_full = a0 + a1*np.linspace(0,n_long-1,n_long)
    energy = energy_full[l0:l1]

    #rhopaw
    rho = rhopaw[l0:l1]
    rhoerr = rhopaw[l2:l3]
    levels = rholev

    data_D0_low = np.genfromtxt("../mama_d/D0_low/rhopaw.cnt")[l0:l1]
    data_D0_high = np.genfromtxt("../mama_d/D0_high/rhopaw.cnt")[l0:l1]

    data_sigma_06 = np.genfromtxt("../mama_d/sigma_06/rhopaw.cnt")[l0:l1]
    data_sigma_07 = np.genfromtxt("../mama_d/sigma_07/rhopaw.cnt")[l0:l1]
    data_sigma_09 = np.genfromtxt("../mama_d/sigma_09/rhopaw.cnt")[l0:l1]
    data_sigma_10 = np.genfromtxt("../mama_d/sigma_10/rhopaw.cnt")[l0:l1]

    def term(f):
        return ((f-rho)/rho)**2

    STD_NLD_high = np.sqrt((rho**2 * (  term(data_D0_low) + term(data_sigma_09) + (rhoerr/rho)**2  )))

    STD_NLD_highest = np.sqrt((rho**2 * (  term(data_D0_low) + term(data_sigma_10) + (rhoerr/rho)**2  )))

    STD_NLD_low = np.sqrt((rho**2 * (  term(data_D0_high) + term(data_sigma_07) + (rhoerr/rho)**2  )))

    STD_NLD_lowest = np.sqrt((rho**2 * (  term(data_D0_high) + term(data_sigma_06) + (rhoerr/rho)**2  )))

    f_high_stk = rho + rhoerr
    f_low_stk = rho - rhoerr

    f_high = rho + STD_NLD_high
    f_low = rho - STD_NLD_low
    

    f_highest = rho + STD_NLD_highest
    f_lowest = rho - STD_NLD_lowest

    # *************************************************************************** #
    # *****************   Plot               *************************************#

    plt.fill_between(energy, f_highest, f_lowest, color=color_outer)#, label="$\sigma(S_n)$ red. fact. $0.8\pm 0.2$") 
    plt.fill_between(energy, f_high, f_low, color=color_inner)#, label="$\sigma(S_n)$ red. fact. $0.8\pm 0.1$")
    #plt.plot(energy, f_high_stk, "--", color="slategrey")#, label="Statistical errors only")
    #plt.plot(energy, f_low_stk, "--", color="slategrey")



    # Normalisation point at Bn
    
    plt.plot(Bn, rho_Bn_sig06, "v", color=color_outer)#, label="rho from neutron res. data")
    plt.plot(Bn, rho_Bn_sig10, "v", color=color_outer)#, label="rho from neutron res. data")
    plt.plot(Bn, rho_Bn_sig07, "v", color=color_inner)#, label="rho from neutron res. data")
    plt.plot(Bn, rho_Bn_sig09, "v", color=color_inner)#, label="rho from neutron res. data")

    plt.plot(Bn, rho_Bn, "v", color=stylesheet.d_color_inter, label="rho from neutron res. data")

    """
    plt.plot(energy, data_D0_low, label="D0_low")
    plt.plot(energy, data_D0_high, label="D0_high")

    plt.plot(energy, data_sigma_06, label="sigma_06")
    plt.plot(energy, data_sigma_07, label="sigma_07")
    plt.plot(energy, data_sigma_09, label="sigma_09")
    plt.plot(energy, data_sigma_10, label="sigma_10")
    """

    # Previously known levels
    plt.plot(energy_full[:len(levels)], levels, "-", color=stylesheet.d_color_inter, label="Known levels")

    # CT model for inerpolation ----
    n0_CT = np.argmin(abs(energy_full-3.0))
    n1_CT = np.argmin(abs(energy_full-Bn-0.5))
    plt.plot(energy_full[n0_CT:n1_CT], fermigas[n0_CT:n1_CT], "--", color=stylesheet.d_color_inter, label="CT interpolation")

    #This experiment!
    plt.errorbar(energy, rho, yerr=rhoerr, x_err=None, fmt="^", color=stylesheet.d_color_data, label="Oslo data for 188Re")

a_t()
a_d()

#plt.title("Systematic and statistical error of NLD for (a,%s)." % reaction)
plt.ylabel(r'$\rho$ (E) [MeV$^{-1}$]', size=18)
plt.xlabel("E$_x$ [MeV]", size=18)
plt.legend()
plt.ylim(4., 1e8)
plt.xlim(-1., 8.)
plt.grid("on")
plt.yscale("log")
plt.savefig("png/NLD_systematic_errors.png")
plt.show()

