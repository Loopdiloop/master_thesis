import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches
import numpy as np
from scipy.optimize import curve_fit
import json
import loading_data

import scipy.stats as stats


#from matplotlib.widgets import CheckButtons
#from matplotlib.axes.Axes import set_visible



# Python script to fit (nuclear) curves to data. Requires Scipy.
# Made by Joergen E. Midtboe, University of Oslo
# This version 9/11/2015


# == Define fitting functions ==
# Define the different types of functions
# that we want to fit the curve to. We typically
# sum together several instances of each.

def SLO(E, T, E0, Gamma0, sigma0):
	# Special Lorentzian,
	# adapted from Kopecky & Uhl (1989) eq. (2.1)
	f = 8.68e-8 * sigma0 * E * Gamma0**2 / ( (E**2 - E0**2)**2 + E**2 * Gamma0**2 )
	return f

def GLO_old(E, T, E0, Gamma0, sigma0):
	# Generalized Lorentzian,
	# adapted from Kopecky & Uhl (1989) eq. (2.2-2.3)
    Gamma = Gamma0 * (E**2 + 4* np.pi**2 * T**2) / E0**2
    funct = 8.68e-8 * sigma0 * E * Gamma0 * Gamma / ( (E**2 - E0**2)**2 + E**2 * Gamma**2 )
    return funct

def GLO(E, T, E0, Gamma0, sigma0):
    # Adapted from Kopecky & Uhl (1989) eq. (2.4)
    Gamma = Gamma0 * (E**2 + 4* np.pi**2 * T**2) / E0**2
    param1 = (E*Gamma)/( (E**2 - E0**2)**2 + E**2 * Gamma**2 )
    param2 = 0.7*Gamma*4*np.pi**2 *T**2 /E0**5
    funct = 8.68e-8 * (param1 + param2)*sigma0*Gamma0
    return funct


"""
    INPUT HERE :)
"""
# debug mode will plot the initial, optimised and bounds-values to evaluate input.
debug_mode = True

# d or t, to choose between which data to use.
reaction = "d"

plot_ARC = True

# p0 are the initial values used for the fit. 
# Values are T, E0, Gamma0, sigma0, E1, Gamma1, ... etc
# p0_functions are which function(s) to use. At least 1, and 5 is current maximum.
if reaction == "d":
    p0 = [0.9, 13.38, 4.2, 445, 15.9, 5.0, 664, 4.9, 1.0, 15, 8.8, 0.6, 20]
    p0_functions = [GLO, GLO, SLO, SLO]

elif reaction == "t":
    p0 = [0.9, 13.0, 3.0, 300, 15.9, 5.0, 664, 8.8, 0.6, 20, 5.33, 1.35, 6.0]#4.9, 0.4, 10]#, 0.8, 0.02, 0.4]
    p0_functions = [GLO, GLO, SLO, SLO]

else:
    raise Exception("Error, faulty input. Choose reaction = d or t.")

# Restrain values by adding limits :) Here, set 50% -> 140% of original value.
minimum = np.array(p0)*0.3
maximum = np.array(p0)*3.5 #2.4
bounds = [minimum, maximum]


# == Import data ==
# Import data as matrices

# Exfor and earlier data: (i.e. need either way)
data_re187_1, data_re187_2 = loading_data.load_data_187Re()
# I suspect some of the uncertanties are "too good." Boost them up here.
data_re187_1[:,2] = data_re187_1[:,2]*1.5
data_re187_2[:,2] = data_re187_2[:,2]*1.5

data_re185 = loading_data.load_data_185Re()
data_w186 = loading_data.load_data_186W()

## ARCDRC E1 strengths ##
data_arc_W184 = loading_data.load_data_ARCDRC("E", 74, 184)
data_arc_W185 = loading_data.load_data_ARCDRC("E", 74, 185)
data_arc_W187 = loading_data.load_data_ARCDRC("E", 74, 187)

data_arc_Os188 = loading_data.load_data_ARCDRC("E", 76, 188)
data_arc_Os189 = loading_data.load_data_ARCDRC("E", 76, 189)
data_arc_Os191 = loading_data.load_data_ARCDRC("E", 76, 191)
data_arc_Os193 = loading_data.load_data_ARCDRC("E", 76, 193)

data_arc_Ir192 = loading_data.load_data_ARCDRC("E", 77, 192)
data_arc_Ir194 = loading_data.load_data_ARCDRC("E", 77, 194)


## ARCDRC M1strengths ##
data_arc_M_W184 = loading_data.load_data_ARCDRC("M", 74, 184)
data_arc_M_W185 = loading_data.load_data_ARCDRC("M", 74, 185)
data_arc_M_W187 = loading_data.load_data_ARCDRC("M", 74, 187)

data_arc_M_Os188 = loading_data.load_data_ARCDRC("M", 76, 188)
data_arc_M_Os189 = loading_data.load_data_ARCDRC("M", 76, 189)
data_arc_M_Os191 = loading_data.load_data_ARCDRC("M", 76, 191)


#for k in range(1, len(data_arc_Eparam)):
#    data_arc = np.vstack((data_arc, loading_data.load_data_ARCDRC("E", data_arc_Eparam[k][0], data_arc_Eparam[k][1]) ))

if reaction == "d":
    # From this experiment:
    data = loading_data.load_a_d()
    
    # Stack everything together into one matrix for fitting.
    data_all = np.vstack((data, data_re187_1))
    data_all = np.vstack((data_all, data_re187_2))
    data_all = np.vstack((data_all, data_re185))
    data_all = np.vstack((data_all, data_w186))

elif reaction =="t":
    # From this experiment:
    data = loading_data.load_a_t()

    # Stack everything together into one matrix for fitting.
    data_all = np.vstack((data, data_re187_1))
    data_all = np.vstack((data_all, data_re187_2))

else:
    raise Exception("Error. This is not yet functionality.")


# The actual total function that is fitted. Uses a sum of p0_functions with the parameter from the initial p0.
# p0-parameters has bounds according to bounds.
def f(E, Temp, E0=1, Gamma0=1, sigma0=1, E1=1, Gamma1=1, sigma1=1, 
        E2=1, Gamma2=1, sigma2=1, E3=1, Gamma3=1, sigma3=1, 
        E4=1, Gamma4=1, sigma4=1,functions=p0_functions):
    """ make_fit currently supports up to 5 GLOs. To add more, continue the pattern. This 
    was, suprisingly, the best solution I found atm working with the scipy-syntax. """

    # For calling with an array when plotting:
    if type(Temp) == list:
        print("list!")
        T=Temp[0]
        EX = np.ones(5)
        Gamma = np.ones(5)
        sigma = np.ones(5)
        for j in range(int((len(Temp)-1)/3)):
            EX[j] = Temp[j+1]
            Gamma[j] = Temp[j+2]
            sigma[j] = Temp[j+3]
    
    # For the fitting algorithm
    else: 
        T = Temp
        EX = np.array([E0, E1, E2, E3, E4])
        Gamma = np.array([Gamma0, Gamma1, Gamma2, Gamma3, Gamma4])
        sigma = np.array([sigma0, sigma1, sigma2, sigma3, sigma4])

    # Calculating the sum of the singular GLOs
    output = np.zeros(len(E))
    for i in range(len(functions)):
        output += functions[i](E, T, EX[i], Gamma[i], sigma[i])
    return output



# popt is the optimal values for the parameters, in order of p0
# pcov is the estimated covariance of popt.
# Documentation of curve_fit from scipy:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html

popt, pcov = curve_fit(f=f, xdata=data_all[:,0], ydata=data_all[:,1], p0=p0, sigma=data_all[:,2], 
    maxfev=100000,bounds=bounds)

print("Fitted values: ", popt)

# Calc std. deviation from the covariance (from documentation):
perr = np.sqrt(np.diag(pcov))


# == Plotting ==
# Make x-axis array to plot from
Earray = np.linspace(0.1,20,300)

# Initialize figure!
plt.figure()
ax = plt.subplot(111)
#rax= plt.axes([0.05, 30, 1e-9, 1e-7])


# Actual best-fit curve
# Extract values from the fit

optimalized_tot = np.zeros(len(Earray))
for j in range(int((len(popt)-1)/3)):
    optimalized = p0_functions[j](Earray, popt[0], popt[j*3+1], popt[j*3+2], popt[j*3+3])
    # Plot the separate GLOs
    if "G" in list(str(p0_functions[j])):
        plot_LO = ax.plot(Earray, optimalized, '--', color="grey", label="GLO")
    elif "S" in list(str(p0_functions[j])):
        plot_LO = ax.plot(Earray, optimalized, '-.', color="grey", label="SLO")
    optimalized_tot += optimalized


# Plot the total optimalized fit
plot_fit = ax.plot(Earray, optimalized_tot, '-', color="magenta", label="Fitted")

# Plot the data from this experiment
oclplot = ax.errorbar(data[:,0], data[:,1], yerr=data[:,2], fmt='D', color="deeppink", label="This experiment")

# Plot dataset 1 and 2 from exfor.
plot_dataset1 = ax.errorbar(data_re187_1[:,0], data_re187_1[:,1], yerr=data_re187_1[:,2], fmt='X', color='darkviolet', label="Goryachev, 1973")
plot_dataset2 = ax.errorbar(data_re187_2[:,0], data_re187_2[:,1], yerr=data_re187_2[:,2], fmt='s', color='fuchsia', label="Shizuma, 2005")

Alpha = 0.8
#plot_Re185_dataset = ax.errorbar(data_re185[:,0], data_re185[:,1], yerr=data_re185[:,2], fmt='o', color='black', label="Re185", alpha=1)
#plot_W186_dataset = ax.errorbar(data_w186[:,0], data_w186[:,1], yerr=data_w186[:,2], fmt='o', color='black', label="W186", alpha=1)


if plot_ARC == True:
    ## ARC E1-data plot
    plot_ARC_W184 = ax.errorbar(data_arc_W184[:,0], data_arc_W184[:,1], yerr=data_arc_W184[:,2], fmt='s', color='blue', label="ARC E1, W184", alpha=Alpha)
    plot_ARC_W185 = ax.errorbar(data_arc_W185[:,0], data_arc_W185[:,1], yerr=data_arc_W185[:,2], fmt='^', color='blue', label="ARC E1, W185", alpha=Alpha)
    plot_ARC_W187 = ax.errorbar(data_arc_W187[:,0], data_arc_W187[:,1], yerr=data_arc_W187[:,2], fmt='v', color='blue', label="ARC E1, W187", alpha=Alpha)

    plot_ARC_Os188 = ax.errorbar(data_arc_Os188[:,0], data_arc_Os188[:,1], yerr=data_arc_Os188[:,2], fmt='s', color='cornflowerblue', label="ARC E1, Os188", alpha=Alpha)
    plot_ARC_Os189 = ax.errorbar(data_arc_Os189[:,0], data_arc_Os189[:,1], yerr=data_arc_Os189[:,2], fmt='^', color='cornflowerblue', label="ARC E1, Os189", alpha=Alpha)
    plot_ARC_Os191 = ax.errorbar(data_arc_Os191[:,0], data_arc_Os191[:,1], yerr=data_arc_Os191[:,2], fmt='v', color='cornflowerblue', label="ARC E1, Os191", alpha=Alpha)
    plot_ARC_Os193 = ax.errorbar(data_arc_Os193[:,0], data_arc_Os193[:,1], yerr=data_arc_Os193[:,2], fmt='<', color='cornflowerblue', label="ARC E1, Os193", alpha=Alpha)

    plot_ARC_Ir192 = ax.errorbar(data_arc_Ir192[:,0], data_arc_Ir192[:,1], yerr=data_arc_Ir192[:,2], fmt='s', color='cyan', label="ARC E1, Ir192", alpha=Alpha)
    plot_ARC_Ir193 = ax.errorbar(data_arc_Ir194[:,0], data_arc_Ir194[:,1], yerr=data_arc_Ir194[:,2], fmt='^', color='cyan', label="ARC E1, Ir194", alpha=Alpha)

    ## ARC M1-data plot
    plot_ARC_M_W184 = ax.errorbar(data_arc_M_W184[:,0], data_arc_M_W184[:,1], yerr=data_arc_M_W184[:,2], fmt='s', color='green', label="ARC M1, W184", alpha=Alpha)
    plot_ARC_M_W185 = ax.errorbar(data_arc_M_W185[:,0], data_arc_M_W185[:,1], yerr=data_arc_M_W185[:,2], fmt='^', color='green', label="ARC M1, W185", alpha=Alpha)
    plot_ARC_M_W187 = ax.errorbar(data_arc_M_W187[:,0], data_arc_M_W187[:,1], yerr=data_arc_M_W187[:,2], fmt='v', color='green', label="ARC M1, W187", alpha=Alpha)

    plot_ARC_M_Os188 = ax.errorbar(data_arc_M_Os188[:,0], data_arc_M_Os188[:,1], yerr=data_arc_M_Os188[:,2], fmt='s', color='lime', label="ARC M1, Os188", alpha=Alpha)
    plot_ARC_M_Os189 = ax.errorbar(data_arc_M_Os189[:,0], data_arc_M_Os189[:,1], yerr=data_arc_M_Os189[:,2], fmt='^', color='lime', label="ARC M1, Os189", alpha=Alpha)
    plot_ARC_M_Os191 = ax.errorbar(data_arc_M_Os191[:,0], data_arc_M_Os191[:,1], yerr=data_arc_M_Os191[:,2], fmt='v', color='lime', label="ARC M1, Os191", alpha=Alpha)


print("Os188", data_arc_Os188)


if reaction == "d":
    plt.title("Fit for $^{188}$Re from (a,d)")
elif reaction == "t":
    plt.title("Fit for $^{187}$Re from (a,t)")
elif reaction == "dt":
    plt.title("Rough fit, for both 187Re and 188Re")

plt.yscale("log")
#plt.ylim([1e-10, 1e-5]) # Set y-axis limits
plt.grid('on')
plt.legend(loc="lower right")

plt.xlabel("E$_\gamma$ [MeV]") 
plt.ylabel(" $\gamma$-ray strength function [MeV$^{-3}$]")
plt.show()



if debug_mode:
    plt.clf()

    X = range(len(popt))
    plt.plot(X, p0, label="Initial guess")
    plt.plot(X, popt,"*-", label="Best fit")
    plt.plot(X, minimum, color="grey", label="min")
    plt.plot(X, maximum, color="grey", label="max")

    x_ticks_labels=["T", "E0", "Gamma0", "sigma0"]
    if len(p0_functions) > 1:
        x_ticks_labels += ["E1", "Gamma1", "sigma1"]
    if len(p0_functions) > 2:
        x_ticks_labels += ["E2", "Gamma2", "sigma2"]
    if len(p0_functions) > 3:
        x_ticks_labels += ["E3", "Gamma3", "sigma3"]
    if len(p0_functions) > 4: # Fifth GLO
        x_ticks_labels += ["E2", "Gamma4", "sigma4"]

    plt.xticks(X, x_ticks_labels, rotation='vertical', fontsize=16)
    plt.yscale("log")
    plt.legend()
    plt.show()







"""
ax.legend()

rax = plt.axes([0.05, 0.4, 0.1, 0.35])
plt.subplots_adjust(left=0.2)
lines = [plot_ARC_W184, plot_ARC_W185, plot_ARC_W187, plot_ARC_Os188, plot_ARC_Os189, plot_ARC_Os191, plot_ARC_Os193, plot_ARC_Ir192, plot_ARC_Ir193]

#labels = ["ARC, W184", "ARC, W185", "ARC, W187", "ARC, Os188", "ARC, Os189", "ARC, Os191", "ARC, Os193", "ARC, Ir192","ARC, Ir194"]
#visibility = [True,True,True,True,True,True,True,False,True]
#[line.get_visible() for line in lines]
#check = CheckButtons(rax, labels, visibility)

labels = [str(line.get_label()) for line in lines]
visibility = [line.get_visible() for line in lines]
check = CheckButtons(rax, labels, visibility)


def func_update(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    plt.draw()

check.on_clicked(func_update)

"""