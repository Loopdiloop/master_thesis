import matplotlib.pyplot as plt
import matplotlib
import numpy as np
#from scipy.optimize import curve_fit
#from scipy.stats import chisquare
#from lmfit import Minimizer
import lmfit

import json

import loading_data_gSF as loading_data
import stylesheet

import scipy.stats as stats
import sys

from matplotlib.colors import LogNorm

"""
Python script to fit (nuclear) curves to data.
Requires Scipy, inspired by original which was made by Joergen E. Midtboe, University of Oslo 9/11/2015.

Heavily revised and specialised by Marianne M. Bjoroen, Jan 2021. """


# == Define fitting functions ==

def SLO(E, T, E0, Gamma0, sigma0):
	# Special Lorentzian, adapted from Kopecky & Uhl (1989) eq. (2.1)
	funct = 8.68e-8 * sigma0 * E * Gamma0**2 / ( (E**2 - E0**2)**2 + E**2 * Gamma0**2 )
	return funct

def GLO(E, T, E0, Gamma0, sigma0):
    # General Lorentzian, adapted from Kopecky & Uhl (1989) eq. (2.4)
    Gamma = Gamma0 * (E**2 + 4* np.pi**2 * T**2) / E0**2
    param1 = (E*Gamma)/( (E**2 - E0**2)**2 + E**2 * Gamma**2 )
    param2 = 0.7*Gamma*4*np.pi**2 *T**2 /E0**5
    funct = 8.68e-8 * (param1 + param2)*sigma0*Gamma0
    return funct


"""
    user INPUT here :)
"""
# debug mode will plot the initial, optimised and bounds-values to evaluate input.
debug_mode = 1
debug_mode_old = 0

# d or t, to choose between which data to use.
try:
    reaction = str(sys.argv[1])
except:
    reaction = "d"
print(reaction)

# Plot additional data?
plot_ARC = 0

# p0 are the initial values used for the fit. 
# Values are T, E0, Gamma0, sigma0, E1, Gamma1, ... etc
# p0_functions are which function(s) to use. At least 1, and 5 is current maximum.
if reaction == "d":
    p0 = [0.9,   5.3, 1.0, 15,   8.8, 0.6, 20,  13.38, 4.2, 445,  15.9, 5.0, 664]
    p0_functions = [GLO, GLO, GLO, GLO]
    p0_functions_names = ["SLO1", "SLO2", "GLO1", "GLO2"]
    nuclei = "188Re"

elif reaction == "t":
    p0 = [0.9,   5.034, 0.3944, 7.595,   8.8, 0.6, 20,  13.0, 3.0, 300,    15.9, 5.5, 664]#      5.33, 1.35, 6.0]#4.9, 0.4, 10]#, 0.8, 0.02, 0.4]
    p0_functions = [SLO, SLO, GLO, GLO]
    p0_functions_names = ["SLO1", "SLO2", "GLO1", "GLO2"]
    nuclei = "187Re"
else:
    raise Exception("Error, faulty input. Choose reaction = d or t.")


print("""
****************************
Running for %s
****************************
"""%reaction)


# Restrain values by adding limits :)
minimum = np.array(p0)*0.3
maximum = np.array(p0)*2.5

params = lmfit.Parameters()

if reaction == "t":
    params.add_many(("T", p0[0], True, minimum[0], maximum[0]),
        ("E0",     5.152, False, minimum[1], maximum[1]),
        ("Gamma0", 0.4257, False, minimum[2], maximum[2]),
        ("Sigma0", 12.25, False, minimum[3], maximum[3]),
        ("E1",     p0[4], True, minimum[4], maximum[4]),
        ("Gamma1", p0[5], True, minimum[5], maximum[5]),
        ("Sigma1", p0[6], True, minimum[6], maximum[6]),
        ("E2",     p0[7], True, minimum[7], maximum[7]),
        ("Gamma2", p0[8], True, minimum[8], maximum[8]),
        ("Sigma2", p0[9], True, minimum[9], maximum[9]),
        ("E3",     p0[10], True, minimum[10], maximum[10]),
        ("Gamma3", p0[11], True, minimum[11], maximum[11]),
        ("Sigma3", p0[12], True, minimum[12], maximum[12]))

elif reaction == "d":
    params.add_many(("T", p0[0], True, minimum[0], maximum[0]),
    ("E0",     p0[1], True, minimum[1], maximum[1]),
    ("Gamma0", p0[2], True, minimum[2], maximum[2]),
    ("Sigma0", p0[3], True, minimum[3], maximum[3]),
    ("E1",     p0[4], True, minimum[4], maximum[4]),
    ("Gamma1", p0[5], True, minimum[5], maximum[5]),
    ("Sigma1", p0[6], True, minimum[6], maximum[6]),
    ("E2",     p0[7], True, minimum[7], maximum[7]),
    ("Gamma2", p0[8], True, minimum[8], maximum[8]),
    ("Sigma2", p0[9], True, minimum[9], maximum[9]),
    ("E3",     p0[10], True, minimum[10], maximum[10]),
    ("Gamma3", p0[11], True, minimum[11], maximum[11]),
    ("Sigma3", p0[12], True, minimum[12], maximum[12]))

else: 
    print("errrrr")

print(params.pretty_print())



# ================= Import data ==
# Import data as matrices

# Exfor and earlier data: (i.e. need either way)
data_re187_1, data_re187_2 = loading_data.load_data_187Re()
# I suspect some of the uncertanties are "too good." Boost them up here.
data_re187_1[:,2] = data_re187_1[:,2]*1.5#1.6
data_re187_2[:,2] = data_re187_2[:,2]*1.5#1.6

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

# Fill data_all with data to use in fit function.
if reaction == "d":
    # From this experiment:
    data = loading_data.load_a_d()
    data=data[:-1]
    # Stack everything together into one matrix for fitting.
    data_all = np.vstack((data, data_re187_1))
    data_all = np.vstack((data_all, data_re187_2))
    #data_all = np.vstack((data_all, data_re185))
    #data_all = np.vstack((data_all, data_w186))

    #Consistent color coding.
    maincolor = stylesheet.d_color_data

    Sn = 5.871

elif reaction =="t":
    # From this experiment:
    data = loading_data.load_a_t()

    # Stack everything together into one matrix for fitting.
    data_all = np.vstack((data, data_re187_1))
    data_all = np.vstack((data_all, data_re187_2))

    #Consistent color coding.
    maincolor = stylesheet.t_color_data

    Sn = 7.360

else:
    raise Exception("Error. This is not yet functionality.")



# popt is the optimal values for the parameters, in order of p0
# pcov is the estimated covariance of popt.
# Documentation of curve_fit from scipy:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html


x_value = data_all[:,0]
y_value = data_all[:,1]
y_error = data_all[:,2]


# The actual total function that is fitted. Uses a sum of p0_functions with the parameter from the initial p0.
# p0-parameters has bounds according to bounds.
def f_fit_total(par, E = x_value):
    """ make_fit currently supports up to 5 GLO/SLOs. To add more, continue the pattern. This 
    was, suprisingly, the best solution I found atm working with the scipy-syntax. """

    functions = p0_functions

    T = par["T"]
    EX = np.array([par["E0"], par["E1"], par["E2"], par["E3"]])#, par["E4"])
    Gamma = np.array([par["Gamma0"], par["Gamma1"], par["Gamma2"], par["Gamma3"]])#, Gamma4])
    sigma = np.array([par["Sigma0"], par["Sigma1"], par["Sigma2"], par["Sigma3"]])#, sigma4])

    # Calculating the sum of the singular GLOs
    output = np.zeros(len(E))
    for i in range(len(functions)):
        output += functions[i](E, T, EX[i], Gamma[i], sigma[i])
    return output


def f_fit_plot_singular(par, E = x_value, j=0):
    """ make_fit currently supports up to 5 GLO/SLOs. To add more, continue the pattern. This 
    was, suprisingly, the best solution I found atm working with the scipy-syntax. """

    functions = p0_functions

    T = par["T"]
    EX = np.array([par["E0"], par["E1"], par["E2"], par["E3"]])#, par["E4"])
    Gamma = np.array([par["Gamma0"], par["Gamma1"], par["Gamma2"], par["Gamma3"]])#, Gamma4])
    sigma = np.array([par["Sigma0"], par["Sigma1"], par["Sigma2"], par["Sigma3"]])#, sigma4])

    return functions[j](E, T, EX[j], Gamma[j], sigma[j])



def f_residuals(parameters):
    return (f_fit_total(parameters) - y_value)**2/(y_error**2)


results = lmfit.minimize(fcn=f_residuals, params=params, method="least_squares")

print(results.success)
print(results.errorbars)
print(results.chisqr)
print(results.redchi)
print(results.params.pretty_print())


print("Chi square: ", results.redchi)

# Initialize figure!
plt.figure(figsize=(11,7))
ax = plt.subplot(111)


# Actual best-fit curve
# Extract values from the fit



# Plot the total optimalized fit
x_values_cont = np.linspace(0, 18, 1000)
plot_fit = ax.plot(x_values_cont, f_fit_total(results.params, E=x_values_cont), '-', color="cornflowerblue", label="Fitted")#, linewidth="5")

ax.plot(x_values_cont, f_fit_plot_singular(results.params, E=x_values_cont, j=0),':', color="lightgray", label=p0_functions_names[0])
ax.plot(x_values_cont, f_fit_plot_singular(results.params, E=x_values_cont, j=1),'-.', color="lightgray", label=p0_functions_names[1])
ax.plot(x_values_cont, f_fit_plot_singular(results.params, E=x_values_cont, j=2),'--', color="lightgray", label=p0_functions_names[2])
ax.plot(x_values_cont, f_fit_plot_singular(results.params, E=x_values_cont, j=3),'-', color="lightgray", label=p0_functions_names[3])


# Plot the data from this experiment
oclplot = ax.errorbar(data[:,0], data[:,1], yerr=data[:,2], fmt='D', color=maincolor, label="%s, this experiment"%nuclei) #"deeppink"

# Plot Sn for reference
plt.plot([Sn, Sn],[2e-9, 9e-7], "b--", label="Sn")

# Plot dataset 1 and 2 from exfor.
plot_dataset1 = ax.errorbar(data_re187_1[:,0], data_re187_1[:,1], yerr=data_re187_1[:,2], fmt='X', color='deeppink', label="Goryachev, 1973")
plot_dataset2 = ax.errorbar(data_re187_2[:,0], data_re187_2[:,1], yerr=data_re187_2[:,2], fmt='s', color='orange', label="Shizuma, 2005")
print(data_re187_2[:,2]/data_re187_2[:,1])
Alpha = 0.8
#plot_Re185_dataset = ax.errorbar(data_re185[:,0], data_re185[:,1], yerr=data_re185[:,2], fmt='o', color='black', label="Re185", alpha=1)
#plot_W186_dataset = ax.errorbar(data_w186[:,0], data_w186[:,1], yerr=data_w186[:,2], fmt='o', color='black', label="W186", alpha=1)


if plot_ARC == True:
    ## ARC E1-data plot
    plot_ARC_W184 = ax.errorbar(data_arc_W184[:,0], data_arc_W184[:,1], yerr=data_arc_W184[:,2], fmt='s', color='blue', label="ARC E1, W184", alpha=Alpha)
    plot_ARC_W185 = ax.errorbar(data_arc_W185[:,0], data_arc_W185[:,1], yerr=data_arc_W185[:,2], fmt='^', color='blue', label="ARC E1, W185", alpha=Alpha)
    plot_ARC_W187 = ax.errorbar(data_arc_W187[:,0], data_arc_W187[:,1], yerr=data_arc_W187[:,2], fmt='v', color='blue', label="ARC E1, W187", alpha=Alpha)

    plot_ARC_Os188 = ax.errorbar(data_arc_Os188[:,0], data_arc_Os188[:,1], yerr=data_arc_Os188[:,2], fmt='s', color='slateblue', label="ARC E1, Os188", alpha=Alpha)
    plot_ARC_Os189 = ax.errorbar(data_arc_Os189[:,0], data_arc_Os189[:,1], yerr=data_arc_Os189[:,2], fmt='^', color='slateblue', label="ARC E1, Os189", alpha=Alpha)
    plot_ARC_Os191 = ax.errorbar(data_arc_Os191[:,0], data_arc_Os191[:,1], yerr=data_arc_Os191[:,2], fmt='v', color='slateblue', label="ARC E1, Os191", alpha=Alpha)
    plot_ARC_Os193 = ax.errorbar(data_arc_Os193[:,0], data_arc_Os193[:,1], yerr=data_arc_Os193[:,2], fmt='<', color='slateblue', label="ARC E1, Os193", alpha=Alpha)

    plot_ARC_Ir192 = ax.errorbar(data_arc_Ir192[:,0], data_arc_Ir192[:,1], yerr=data_arc_Ir192[:,2], fmt='s', color='cyan', label="ARC E1, Ir192", alpha=Alpha)
    plot_ARC_Ir193 = ax.errorbar(data_arc_Ir194[:,0], data_arc_Ir194[:,1], yerr=data_arc_Ir194[:,2], fmt='^', color='cyan', label="ARC E1, Ir194", alpha=Alpha)

    ## ARC M1-data plot
    plot_ARC_M_W184 = ax.errorbar(data_arc_M_W184[:,0], data_arc_M_W184[:,1], yerr=data_arc_M_W184[:,2], fmt='s', color='darkviolet', label="ARC M1, W184", alpha=Alpha)
    plot_ARC_M_W185 = ax.errorbar(data_arc_M_W185[:,0], data_arc_M_W185[:,1], yerr=data_arc_M_W185[:,2], fmt='^', color='darkviolet', label="ARC M1, W185", alpha=Alpha)
    plot_ARC_M_W187 = ax.errorbar(data_arc_M_W187[:,0], data_arc_M_W187[:,1], yerr=data_arc_M_W187[:,2], fmt='v', color='darkviolet', label="ARC M1, W187", alpha=Alpha)

    plot_ARC_M_Os188 = ax.errorbar(data_arc_M_Os188[:,0], data_arc_M_Os188[:,1], yerr=data_arc_M_Os188[:,2], fmt='s', color='fuchsia', label="ARC M1, Os188", alpha=Alpha)
    plot_ARC_M_Os189 = ax.errorbar(data_arc_M_Os189[:,0], data_arc_M_Os189[:,1], yerr=data_arc_M_Os189[:,2], fmt='^', color='fuchsia', label="ARC M1, Os189", alpha=Alpha)
    plot_ARC_M_Os191 = ax.errorbar(data_arc_M_Os191[:,0], data_arc_M_Os191[:,1], yerr=data_arc_M_Os191[:,2], fmt='v', color='fuchsia', label="ARC M1, Os191", alpha=Alpha)



plt.yscale("log")
#plt.ylim([1e-10, 1e-5]) # Set y-axis limits
plt.grid('on')
plt.legend(loc="lower right")
plt.ylim([5e-10,8e-6])
plt.xlabel("E$_\gamma$ [MeV]", size=18) 
plt.ylabel(" $\gamma$-ray strength function [MeV$^{-3}$]", size=18)
if plot_ARC == True:
    plt.savefig("png/gSF_fit_ARC_%s.png"%reaction)
else:
    plt.savefig("png/gSF_fit_%s.png"%reaction)
plt.show()


par_names = []
par_values = []
par_stderr = []

for par, value in results.params.items():
    par_names.append(par)
    par_values.append(value.value)
    par_stderr.append(value.stderr) 

#print(par_names, par_values, par_stderr)
#print(p0_functions)


print("""

################################################



""")

print(results.params.pretty_print())

print("""

################################################



""")


print("""\\begin{tabular}{llrrr}
    \multicolumn{4}{l}{\\textbf{%s}} T = %3.3f \\\ \hline \hline 
    \multicolumn{1}{l}{} & E & $\Gamma$ & $\sigma_0$ \\\ """ %(nuclei, par_values[0]))

for j in range(1,5):
    print("""   %s & $ %2.2f \\pm  %2.2f $ & $ %2.2f \\pm %2.2f $ & $ %3.3f \\pm %3.3f $ \\\ \\hline """ 
    % (str(p0_functions_names[j-1]), par_values[j*3-2], par_stderr[j*3-2], par_values[j*3-1], par_stderr[j*3-1],par_values[j*3-0], par_stderr[j*3-0] )   ) 

print("\end{tabular}")




correlation_matrix = True
if correlation_matrix:

    plt.clf()
    plt.figure(figsize=(11,7))
    #plt.yscale("linear")
    
    R = results.params.valuesdict()
    X = np.linspace(0.5,len(R)-0.5, len(R))
    C = abs(results.covar)
    
    Keys = list(R.keys())
    print(Keys)
    if reaction == "t":
        Keys = list(Keys[0]) + Keys[4:]
        X = np.linspace(0.5,len(R)-3-0.5, len(R)-3)
    plt.pcolormesh(C, cmap="jet", norm=LogNorm(vmin=abs(C.min()), vmax=abs(C.max()) )) #cmap="jet", 
    plt.colorbar()#ticks=[1,5,10,50], format=LogFormatter(10))
    #plt.plot(np.linspace(0,))
    plt.xticks(X, list(Keys), rotation=-60, fontsize=12)
    plt.yticks(X, list(Keys), fontsize=12)
    plt.savefig("png/gSF_fit_covar_%s.png"%reaction)
    plt.show()




debug_mode=1
if debug_mode:
    """ This plots out the initial guess and optimised parameters and their min/max limits for the fit.
    This is meant to """
    plt.clf()
    plt.figure(figsize=(11,7))
    
    D = params.valuesdict()
    X = range(len(D))
    plt.plot(X, list(D.values()))#, align='center')
    plt.xticks(X, list(D.keys()))

    R = results.params.valuesdict()
    plt.plot(X, list(R.values()))#, align='center')
    plt.xticks(X, list(R.keys()))

    plt.plot(X, minimum, color="grey", label="min")
    plt.plot(X, maximum, color="grey", label="max")

    plt.yscale("log")
    plt.savefig("png/gSF_fit_parameterminmax_%s.png"%reaction)
    plt.show()

