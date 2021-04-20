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


def plot_matrix(filename, reaction="d", log=True, axis_limits = [0,8,0,8]):
    filepath = "../mama_%s/matrices_plotting/"%reaction
    print("   *********")
    print("     Loading ", reaction+" "+filename)
    #M = np.zeros((Ex, Eg))
    i = 0

    with open(filepath+filename) as csvfile:
        filereader = csv.reader(csvfile, delimiter = " ")
        """ See error exception description at start of file(!) If not fixed manually, run this while-loop instead of for-loop. """
        while filereader:
            try:
                row = next(filereader)
            except UnicodeDecodeError:
                print("Error")
                row = next(filereader)
                row = next(filereader)
                continue
            # ALTERNATIVE:
            #for row in filereader:
            row = list(filter(None, row)) #Remove all empty objects in list. E.g. ["", "", ""].
            element = list(row[0])[0]
            if element == "!" or element == " ": # Not actual data but pre/post data.
                #print(row)
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

    MM = M.copy()
    mask = M==0
    mask = abs(M)<=1e-1
    M=M.astype(np.float64)
    M[mask] = np.nan
    
    Ex_axis = (np.linspace(0, Ex-1, Ex) * Ex_a + Ex_b)*1e-3 - 0.5*Ex_a*1e-3
    Eg_axis = (np.linspace(0, Eg-1, Eg) * Eg_a + Eg_b)*1e-3 - 0.5*Eg_a*1e-3
    #print(Eg_axis[0:10])
    #Eg_axis = (np.linspace(0, Eg-1, Eg) * Eg_a + Eg_b)*1e-3 - 0.5*Eg_a*1e-3
    #print(Eg_axis[0:10])
    #print(Eg_a)

    if reaction == "d":
        Sn = 5.87
    elif reaction == "t":
        Sn = 7.360

    plt.figure(figsize=(8,5)) #(11,7))
    
    if log == True:
        if "cofinal" in filename:
            plt.pcolormesh(Eg_axis,Ex_axis, M, cmap="jet",norm=matplotlib.colors.LogNorm(), vmin=1, vmax=2400)#, vmax=400)#np.log(M))
        else:
            plt.pcolormesh(Eg_axis,Ex_axis, M, cmap="jet",norm=matplotlib.colors.LogNorm(), vmin=1, vmax=6e1)
    else: 
        plt.pcolormesh(Eg_axis,Ex_axis, M, cmap="jet")#,norm=matplotlib.colors.LogNorm())

    plt.plot(np.linspace(-1,11,2), [Sn,Sn],  color="black", label="Sn, horisontal", linewidth=2)
    plt.plot([-1,11], [-1,11], color="black", label="Ex = Eg, diagonal", linewidth=2)

    plt.legend(loc="lower right")
    
    plt.axis(axis_limits)
    #plt.title(plot_title, fontsize=18)
    plt.xlabel("E$\gamma$ [MeV]", fontsize=15)
    plt.ylabel("Ex [MeV]", fontsize=15)
    plt.colorbar()
    
    plt.savefig("matrices/plot_"+reaction+"_"+filename+".png")
    print("plot_"+reaction+"_"+filename+".png saved sucsessfully.")
    #plt.show()
    plt.clf()


    return MM, Eg_axis, Ex_axis


if __name__ == "__main__":
    reaction= str(sys.argv[1])
    filename = str(sys.argv[2])

    print("Plotting %s for (a,%s)"%(reaction,filename))

    plot_matrix(filename, reaction)
