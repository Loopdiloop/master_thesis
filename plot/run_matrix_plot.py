
import sys
import matplotlib.pyplot as plt
import numpy as np

from matrix_plot import plot_matrix


"""
reaction= str(sys.argv[1])
filename = str(sys.argv[2])

print("Plotting %s for (a,%s)"%(reaction,filename))

plot_matrix(filename, reaction)

"""

#return M, Eg_axis, Ex_axis

#plot_matrix("alfna","d")
#plot_matrix("alfna_fnrn","d")
#plot_matrix("alfna_un_fnrn","d")
#plot_matrix("alfna_fg","d")
#plot_matrix("alfna_fg_cofinal","d")

#sys.exit()

"""
plot_matrix("alfna","t")
plot_matrix("alfna_fnrn","t")
plot_matrix("alfna_un_fnrn","t")
plot_matrix("alfna_fg","t")
plot_matrix("alfna_fg_cofinal","t")
"""
# For plotting: co a little
M_d_raw, Eg_d_raw, Ex_d_raw = plot_matrix("alfna_fnrn_co41","d")
M_d_un, Eg_d_un, Ex_d_un = plot_matrix("alfna_un_fnrn_co41","d")
M_d_fg, Eg_d_fg, Ex_d_fg = plot_matrix("alfna_fg_co41","d")


plot_evolution = False
if plot_evolution:
    # Plot how the oxygen peak changes? :) 

    Ex_min = 4#6.2
    Ex_max = 5#7.2

    bin_Ex_min = np.argmin(abs(Ex_min-abs(Ex_d_raw)))
    bin_Ex_max = np.argmin(abs(Ex_max-abs(Ex_d_raw)))

    print(bin_Ex_min, bin_Ex_max)


    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    """
    y_raw=(M_d_raw[bin_Ex_min:bin_Ex_max, :]).sum(axis=0)
    ax1.plot(Eg_d_raw,y_raw, label="Raw", linewidth=2, color="green")


    y_un=(M_d_un[bin_Ex_min:bin_Ex_max, :]).sum(axis=0)
    ax2.plot(Eg_d_un,y_un, label="Unfolded", linewidth=2, color="green")


    y_fg=(M_d_fg[bin_Ex_min:bin_Ex_max, :]).sum(axis=0)
    ax3.plot(Eg_d_fg,y_fg, label="First generation", linewidth=2, color="green")


    ax1.axis(xmin=0, xmax=7, ymin=0, ymax=1150)
    ax2.axis(xmin=0, xmax=7, ymin=0, ymax=1150)
    ax3.axis(xmin=0, xmax=7, ymin=0, ymax=1150)
    """

    y_raw=(M_d_raw[bin_Ex_min:bin_Ex_max, :]).sum(axis=0)
    ax1.plot(Eg_d_raw,y_raw, label="Raw", linewidth=2, color="green")


    y_un=(M_d_un[bin_Ex_min:bin_Ex_max, :]).sum(axis=0)
    ax2.plot(Eg_d_un,y_un, label="Unfolded", linewidth=2, color="green")


    y_fg=(M_d_fg[bin_Ex_min:bin_Ex_max, :]).sum(axis=0)
    ax3.plot(Eg_d_fg,y_fg, label="First generation", linewidth=2, color="green")


    ax1.axis(xmin=0, xmax=5.1, ymin=0, ymax=950)
    ax2.axis(xmin=0, xmax=5.1, ymin=0, ymax=950)
    ax3.axis(xmin=0, xmax=5.1, ymin=0, ymax=950)


    #########################3

    ax1.text(2,600,"a) Raw spectra", fontsize=15)
    ax2.text(2,600,"b) Unfolded spectra", fontsize=15)
    ax3.text(2,600,"c) First generation matrix", fontsize=15)


    ax3.set_xlabel("E$\gamma$ [MeV]", fontsize=15)
    ax2.set_ylabel("Counts", fontsize=15)
    fig.subplots_adjust(hspace=0,wspace=0)

    plt.show()
    plt.clf()

test_Brink_d = True
if test_Brink_d:
    # Plot how the oxygen peak changes? :) 
    
    Ex_d_raw = Ex_d_fg
    Eg_d_raw = Eg_d_fg
    M_d_raw = M_d_fg

    Ex0_min = 4.5
    Ex0_max = 5.0
    
    Ex1_min = 3.5
    Ex1_max = 4.0

    Ex2_min = 2.5
    Ex2_max = 3.0

    bin_Ex0_min = np.argmin(abs(Ex0_min-abs(Ex_d_raw)))
    bin_Ex0_max = np.argmin(abs(Ex0_max-abs(Ex_d_raw)))

    bin_Ex1_min = np.argmin(abs(Ex1_min-abs(Ex_d_raw)))
    bin_Ex1_max = np.argmin(abs(Ex1_max-abs(Ex_d_raw)))

    bin_Ex2_min = np.argmin(abs(Ex2_min-abs(Ex_d_raw)))
    bin_Ex2_max = np.argmin(abs(Ex2_max-abs(Ex_d_raw)))

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    y_raw0=(M_d_raw[bin_Ex0_min:bin_Ex0_max, :]).sum(axis=0)
    ax1.plot(Eg_d_raw,y_raw0, label="Raw", linewidth=2, color="green")

    y_raw1=(M_d_raw[bin_Ex1_min:bin_Ex1_max, :]).sum(axis=0)
    ax2.plot(Eg_d_raw,y_raw1, label="Raw", linewidth=2, color="green")

    y_raw2=(M_d_raw[bin_Ex2_min:bin_Ex2_max, :]).sum(axis=0)
    ax3.plot(Eg_d_raw,y_raw2, label="Raw", linewidth=2, color="green")

    y_max = np.max([y_raw0, y_raw1, y_raw2]) + 20
    x_min = -0.2
    ax1.axis(xmin=x_min, xmax=5, ymin=0, ymax=y_max)
    ax2.axis(xmin=x_min, xmax=5, ymin=0, ymax=y_max)
    ax3.axis(xmin=x_min, xmax=5, ymin=0, ymax=y_max)


    #########################3
    y_text = int(0.7* y_max)
    
    ax1.text(2,y_text,"a) $E_x \in [4.5,5]$ MeV", fontsize=15)
    ax2.text(2,y_text,"b) $E_x \in [3.5,4]$ MeV", fontsize=15)
    ax3.text(2,y_text,"c) $E_x \in [2.5,3]$ MeV", fontsize=15)


    ax3.set_xlabel("E$\gamma$ [MeV]", fontsize=15)
    ax2.set_ylabel("Counts", fontsize=15)
    fig.subplots_adjust(hspace=0,wspace=0)

    plt.show()
    plt.clf()





print("Done! :)")
print("\a")