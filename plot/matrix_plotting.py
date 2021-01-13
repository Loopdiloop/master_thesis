import csv 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys


def plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits, reaction="d", log=True):
    print("Loading ", filename)
    M = np.zeros((Ex, Eg))#, dtype=np.int64)
    i = 0

    with open(filepath+filename) as csvfile:
        filereader = csv.reader(csvfile, delimiter = " ")
        #while filereader:
        #    try:
        #        row = next(filereader)
        #    except UnicodeDecodeError:
        #        print("Error")
        #        continue
        for row in filereader:
            #print("This one fucked up: ",list(row[0]))
            #try: 
            row = list(filter(None, row))
            element = list(row[0])[0]
            #except:
            #    print(row)
            #    k += 1
            #    if k<= 5:
            #        continue
            #    else:
            #        break
            if element == "!" or element == " ":
                if row[0] == "!CALIBRATION": # Linear calibration, assume ax+b / ay+b 
                    row_bug=row[4].split(',') # Theres a bug of a missing space...........(!)
                    print(row)
                    Ex_b = float(row_bug[1].strip(","))
                    Ex_a = float(row[5].strip(","))
                    Eg_b = float(row[2].strip(","))
                    Eg_a = float(row[3].strip(","))
                elif row[0] == "!IDEND=":
                    break
                else:
                    continue
            else:
                for j in range(len(row)):
                    if row[j] == "":
                        row[j] = 0
                    M[i,j] = float(row[j]) #np.int64(row[j])
                i += 1
                
    print("i: ", i, " j:",j)
    print(Ex_a, Ex_b, Eg_a, Eg_b)

    mask = M==0
    mask = abs(M)<=1e-1
    M=M.astype(np.float64)
    M[mask] = np.nan
    
    Ex_axis = (np.linspace(0, Ex, Ex) * Ex_a + Ex_b)*1e-3
    Eg_axis = (np.linspace(0, Eg, Eg) * Eg_a + Eg_b)*1e-3

    if log == True:
        plt.pcolormesh(Eg_axis,Ex_axis, M, cmap="jet",norm=matplotlib.colors.LogNorm())#np.log(M))
    else: 
        plt.pcolormesh(Eg_axis,Ex_axis, M, cmap="jet")#,norm=matplotlib.colors.LogNorm())
    plt.axis(axis_limits)
    plt.title(plot_title, fontsize=18)
    plt.xlabel("E$\gamma$ [MeV]", fontsize=15)
    plt.ylabel("Ex [MeV]", fontsize=15)


    plt.colorbar()
    #plt.show()
    plt.savefig("plot_"+reaction+"_"+filename+".png")
    print("plot_"+reaction+"_"+filename+".png saved sucsessfully.")
    plt.clf()
    return None




filepath = "../d_mama_janplot/"
axis_limits = [0,10,0,10]

show_alfna = True
if show_alfna:
    filename = "alfna"
    plot_title = "Alfna matrix"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits)

show_alfna_fnrn = True
if show_alfna_fnrn:
    filename = "alfna_fnrn"
    plot_title = "Alfna matrix, negative removed"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits)

show_alfna_fnrn_co2 = True
if show_alfna_fnrn_co2:
    filename = "alfna_fnrn_co2"
    plot_title = "Alfna matrix, negative removed_compressed"
    Ex = 251
    Eg = 1001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits)

show_alfna_fnrn_co4 = True
if show_alfna_fnrn_co4:
    filename = "alfna_fnrn_co4"
    plot_title = "Alfna matrix, negative removed_compressed"
    Ex = 126
    Eg = 501
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits)

# okkk

show_un = True
if show_un:
    filename = "unfolded_writing"
    plot_title = "Unfolded"
    Ex = 501
    Eg = 2001
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits)#, log=False)

show_un_co = True
if show_un_co:
    # 500x500  280 keV x 248 keV
    # E_{x}|RE:alfnaFN:RN:UN:FN:RN:CO:4-8
    filename = "unfolded_co_writing"
    plot_title = "Unfolded_co"
    Ex = 62
    Eg = 501
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits)#, log=False)

#ok
show_fg_fnrn = True
if show_fg_fnrn:
    filename = "fg_fnrn"
    plot_title = "fg fgrn matrix"
    Ex = 62
    Eg = 501
    plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits)#, log=False)




#plot_matrix(filepath, filename, plot_title, Ex, Eg, axis_limits)


filepath = "../t_mama/"




print("Done! :)")
print("\a")

