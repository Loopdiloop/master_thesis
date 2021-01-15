import csv 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys

""" 
Script for plotting different mama matrices.

ERROR WARNING AND HANDLING:
There is an encoding bug(?) in mama, rendering an unknown/broken symbol in line 6 with the prefix !TIME=DATE...
I fixed this by either manually open the file (e.g. in VSC, gedit did not handle this), despite the warnings and manually delete this line.
Otherwise you can run the script and switch the for-loop for the while-loop shown in the beginning og def plot_matrix.

"""


def plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="d", log=True):
    print("   *********")
    print("     Loading ", reaction+" "+filename)
    #M = np.zeros((Ex, Eg))
    i = 0

    with open(filepath+filename) as csvfile:
        filereader = csv.reader(csvfile, delimiter = " ")
        """ See error exception description at start of file(!) If not fixed manually, run this while-loop instead of for-loop. """
        #while filereader:
        #    try:
        #        row = next(filereader)
        #    except UnicodeDecodeError:
        #        print("Error")
        #        continue
        for row in filereader:
            row = list(filter(None, row)) #Remove all empty objects in list. E.g. ["", "", ""].
            element = list(row[0])[0]
            if element == "!" or element == " ": # Not actual data but pre/post data.
                if row[0] == "!CALIBRATION": # Linear calibration coeff., assume ax+b / ay+b 
                    row_bug=row[4].split(',') # Theres a bug of a missing space. Manually accounted for.
                    Ex_b = float(row_bug[1].strip(","))
                    Ex_a = float(row[5].strip(","))
                    Eg_b = float(row[2].strip(","))
                    Eg_a = float(row[3].strip(","))
                elif row[0] == "!COMMENT=E(NaI)":
                    print("      -- Manipulation history: ", row)
                elif row[0].split("=")[0] == "!DIMENSION":
                    row_total = "".join(row)
                    dimm = row_total.split(",0:")
                    dimm = list(filter(None, dimm))
                    Ex = int(dimm[2])+1
                    Eg = int(dimm[1])+1
                    M = np.zeros((Ex, Eg))
                    print("Dimensions: ", Ex, Eg)
                elif row[0] == "!IDEND=": # End of datafile. Next row is empty. 
                    break
                else: # If line contains other non-data I'm not interested in.
                    continue
                
            else: # If the row contains actual data
                for j in range(len(row)):
                    M[i,j] = float(row[j]) # Fill M with data.
                i += 1
    print("     Binsizes. X, Ex: ", Ex_a,"  Y/gamma: ", Eg_a)

    mask = M==0
    mask = abs(M)<=1e-1
    M=M.astype(np.float64)
    M[mask] = np.nan
    
    Ex_axis = (np.linspace(0, Ex-1, Ex) * Ex_a + Ex_b)*1e-3 - 0.5*Ex_a*1e-3
    Eg_axis = (np.linspace(0, Eg-1, Eg) * Eg_a + Eg_b)*1e-3 - 0.5*Eg_a*1e-3

    print(Ex_axis)
    if reaction == "d":
        Sn = 5.87
    elif reaction == "t":
        Sn = 7.360

    
    if log == True:
        plt.pcolormesh(Eg_axis,Ex_axis, M, cmap="jet",norm=matplotlib.colors.LogNorm())#np.log(M))
    else: 
        plt.pcolormesh(Eg_axis,Ex_axis, M, cmap="jet")#,norm=matplotlib.colors.LogNorm())

    plt.plot(np.linspace(-1,11,2), [Sn,Sn], '--', label="Sn")
    plt.plot([-1,11], [-1,11], '--', label="Ex = Eg")

    plt.legend(loc="lower right")
    
    plt.axis(axis_limits)
    #plt.title(plot_title, fontsize=18)
    plt.xlabel("E$\gamma$ [MeV]", fontsize=15)
    plt.ylabel("Ex [MeV]", fontsize=15)


    plt.colorbar()
    plt.show()
    plt.savefig("plot_"+reaction+"_"+filename+".png")
    print("plot_"+reaction+"_"+filename+".png saved sucsessfully.")
    plt.clf()

    sys.exit()
    return M


"""

filepath = "../mama_d/"
axis_limits = [0,10,0,10]

show_alfna = True
if show_alfna:
    filename = "alfna"
    plot_title = "Alfna matrix"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="d")

show_alfna_fnrn = True
if show_alfna_fnrn:
    filename = "alfna_fnrn"
    plot_title = "Alfna matrix, negative removed"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="d")

show_alfna_fnrn_co2 = True
if show_alfna_fnrn_co2:
    filename = "alfna_fnrn_co2"
    plot_title = "Alfna matrix, negative removed_compressed"
    Ex = 251
    Eg = 1001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="d")

show_alfna_fnrn_co4 = True
if show_alfna_fnrn_co4:
    filename = "alfna_fnrn_co4"
    plot_title = "Alfna matrix, negative removed_compressed"
    Ex = 126
    Eg = 501
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="d")

show_un = True
if show_un:
    filename = "alfna_unfolded"
    plot_title = "Unfolded"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="d")

show_un_co = True
if show_un_co:
    # 500x500  280 keV x 248 keV
    # E_{x}|RE:alfnaFN:RN:UN:FN:RN:CO:4-8
    filename = "alfna_unfolded_co"
    plot_title = "Unfolded_co"
    Ex = 62
    Eg = 501
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="d")

show_fg_fnrn = True
if show_fg_fnrn:
    filename = "alfna_fg_fnrn"
    plot_title = "fg fgrn matrix"
    Ex = 62
    Eg = 501
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="d")

### Generate 2D plot to compare the alfna, un and fg.
## Final binning(!)

"""
##################################
filepath = "../mama_t/"
axis_limits = [-0.5,9,-0.5,9]
"""
show_alfna = True
if show_alfna:
    filename = "alfna"
    plot_title = "Alfna matrix"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="t")
"""

"""
show_alfna_fnrn = True
if show_alfna_fnrn:
    filename = "alfna_fnrn"
    plot_title = "Alfna matrix, negative removed"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="t")
"""

"""
show_alfna_fnrn_co2 = True
if show_alfna_fnrn_co2:
    filename = "alfna_fnrn_co2"
    plot_title = "Alfna matrix, negative removed_compressed"
    Ex = 251
    Eg = 1001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="t")


show_alfna_fnrn_co4 = True
if show_alfna_fnrn_co4:
    filename = "alfna_fnrn_co4"
    plot_title = "Alfna matrix, negative removed_compressed"
    Ex = 126
    Eg = 501
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="t")

show_un = True
if show_un:
    filename = "alfna_un"
    plot_title = "Unfolded"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="t")

show_un_co = True
if show_un_co:
    # 500 x 62. x 28 keV, y 248 keV. 
    filename = "alfna_un_co48"
    plot_title = "Unfolded_co"
    Ex = 63
    Eg = 501
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="t")

show_fg_fnrn = True
if show_fg_fnrn:
    filename = "alfna_fg"
    plot_title = "fg fgrn matrix"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="t")
"""
show_fg_fnrn_co = True
if show_fg_fnrn_co:
    filename = "alfna_fg_co"
    plot_title = "fg fgrn matrix"
    Ex = 62
    Eg = 501
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="t")


print("Done! :)")
print("\a")

