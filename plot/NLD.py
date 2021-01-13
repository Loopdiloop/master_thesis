import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(1, '../')
import colors_stylesheet as stylesheet

# Counting NLD

def a_t():
    n = 28
    n_long = 405

    a0 = -0.8875
    a1 = 0.2480

    rholev = np.genfromtxt("../t_mama/rholev.cnt")
    rhopaw = np.genfromtxt("../t_mama/rhopaw.cnt")
    fermigas = np.genfromtxt("../t_mama/fermigas.cnt")

    Bn = 7.360000
    Bnerr = 0.001
    rho_Bn = 17870000.0
    rho_Bnerr = 1818000.0

    #fermi = fermigas
    energy = a0 + a1*np.linspace(0,n_long-1,n_long)
    energyerr = np.zeros(n_long)

    #rhopaw
    rho = rhopaw[:26]
    rhoerr = rhopaw[27:]

    #rholev
    levels = rholev

    # Normalisation point at Bn
    plt.plot(Bn, rho_Bn, "D", color=stylesheet.t_color_inter, label="rho from neutron res. data")

    # Previously known levels
    plt.plot(energy[:len(levels)], levels, color=stylesheet.t_color_inter, label="Known levels")

    # CT model for inerpolation ----
    n0_CT = np.argmin(abs(energy-3.0))
    n1_CT = np.argmin(abs(energy-Bn-0.5))
    plt.plot(energy[n0_CT:n1_CT], fermigas[n0_CT:n1_CT], "--", color=stylesheet.t_color_inter, label="CT interpolation")

    #This experiment!
    plt.errorbar(energy[:len(rho)], rho, yerr=rhoerr[:-1], x_err=None, fmt="s", color=stylesheet.t_color_data, label="Oslo data for 187Re")


def a_d(): #color = green
    n = 30
    n_long = 404

    a0 = -0.8875
    a1 = 0.2480

    rholev = np.genfromtxt("../d_mama/rholev.cnt")
    rhopaw = np.genfromtxt("../d_mama/rhopaw.cnt")
    fermigas = np.genfromtxt("../d_mama/fermigas.cnt")

    Bn = 5.871000
    Bnerr = 0.001
    rho_Bn = 5688000.0
    rho_Bnerr = 204800.0

    #fermi = fermigas
    energy = a0 + a1*np.linspace(0,n_long-1,n_long)
    energyerr = np.zeros(n_long)

    #rhopaw
    rho = rhopaw[:28]
    rhoerr = rhopaw[29:]

    #rholev
    levels = rholev

    # Normalisation point at Bn
    plt.plot(Bn, rho_Bn, "v", color=stylesheet.d_color_inter, label="rho from neutron res. data")

    # Previously known levels
    plt.plot(energy[:len(levels)], levels, "-", color=stylesheet.d_color_inter, label="Known levels")

    # CT model for inerpolation ----
    n0_CT = np.argmin(abs(energy-3.0))
    n1_CT = np.argmin(abs(energy-Bn-0.5))
    plt.plot(energy[n0_CT:n1_CT], fermigas[n0_CT:n1_CT], "--", color=stylesheet.d_color_inter, label="CT interpolation")

    #This experiment!
    plt.errorbar(energy[:len(rho)], rho, yerr=rhoerr[:-1], x_err=None, fmt="^", color=stylesheet.d_color_data, label="Oslo data for 188Re")

a_t()
a_d()

plt.title("NLD for 187 and 188 Re.", size=14)
plt.ylabel("rho(E) [1/MeV]", size=12)
plt.xlabel("Ex [MeV]", size=12)
plt.legend()
plt.ylim(4., 1e8)
plt.xlim(-1., 8.)
plt.grid("on")
plt.yscale("log")
plt.show()
