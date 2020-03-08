""" All the coeffs ready for calculating """

import numpy as np
import sys

peaks_pro = open("peaks_186W_Pro.csv", "r")
peaks_tri = open("peaks_186W_Tri.csv", "r")
a = True
n = 8

print_calc = True


# Separate files for the two peaks :)
# Format assumed to be same as for peaks2D.C

# As there are two kinds of approximations made, 
# one parallell on the axes and one shaped like a "X".
# I chose to use the average of these two approximations.

peaks_pro_E_2D = np.zeros((n,n))
peaks_pro_dE_2D = np.zeros((n,n))
peaks_pro_E_proj = np.zeros((n,n))
peaks_pro_dE_proj = np.zeros((n,n))
    
peaks_tri_E_2D = np.zeros((n,n))
peaks_tri_dE_2D = np.zeros((n,n)) 
peaks_tri_E_proj = np.zeros((n,n))
peaks_tri_dE_proj = np.zeros((n,n))


peaks_pro.readline() #Reads header
peaks_tri.readline() #Reads header

while a == True:
    header_pro = peaks_pro.readline()
    header_tri = peaks_tri.readline()
    pro_line_from_file = peaks_pro.readline()
    tri_line_from_file = peaks_tri.readline()

		# Read header
    header_pro = header_pro.split()
    
    # If files are not of same size, break.
    if len(header_pro) < 2:
        print "Error. Broke off as files are of incorrect size. "
        break

		# Read out which detector and stripe you are working with
    detector = int(list(header_pro[0])[-1])
    stripe = int(list(header_pro[1])[-1])
    
    #TEST IF THEY ARE ALIGNED :)
    header_tri = header_tri.split()
    if detector != int(list(header_tri[0])[-1]):
        sys.exit("ERROR. Detector no. not equal!")
    elif stripe != int(list(header_tri[1])[-1]):
        sys.exit("ERROR. Stripe no. not equal!")
    # Detector/stripe system seems to work perfecly..
    # Loading of data seems to work well!

    # Will be on the form ['28Si_0', '9605.68', '1415.1', '9605.68', '1416.12']
    #                       not needed, x-axis/E, FWHM(x), y/dE, FWHM(y) (??)
    pro_line_from_file = pro_line_from_file.split()
    peaks_pro_E_2D[detector,stripe] = pro_line_from_file[1]
    peaks_pro_dE_2D[detector,stripe] = pro_line_from_file[2]
    peaks_pro_E_proj[detector,stripe] = pro_line_from_file[3]
    peaks_pro_dE_proj[detector,stripe] = pro_line_from_file[4]


    tri_line_from_file = tri_line_from_file.split()
    peaks_tri_E_2D[detector,stripe] = tri_line_from_file[1]
    peaks_tri_dE_2D[detector,stripe] = tri_line_from_file[2]
    peaks_tri_E_proj[detector,stripe] = tri_line_from_file[3]
    peaks_tri_dE_proj[detector,stripe] = tri_line_from_file[4]
 


#Qkinz:
# dE - E . Stripes, assume spherical symmetrical for all detectors
# Tri from Qkinz is for g.s. in tritons
tri0 = np.array([1964.098946, 12552.415561])
tri1 = np.array([1954.532228, 12579.878028])
tri2 = np.array([1947.486839, 12605.306198])
tri3 = np.array([1942.923699, 12628.720307])
tri4 = np.array([1940.820342, 12650.121475])
tri5 = np.array([1941.170584, 12669.491970])
tri6 = np.array([1943.984462, 12686.795134])
tri7 = np.array([1949.288440, 12701.974994])

# Pro from Qkinz is for excitation 2779.8 keV in 16O(alpha,p)19F
pro0 = np.array([1200.699159, 8207.715311])
pro1 = np.array([1188.615373, 8289.474159])
pro2 = np.array([1177.915492, 8373.019176])
pro3 = np.array([1168.562060, 8458.370646])
pro4 = np.array([1160.526585, 8545.536295])
pro5 = np.array([1153.789151, 8634.511443])
pro6 = np.array([1148.338168, 8725.279003])
pro7 = np.array([1144.170257, 8817.809331])

# DEU/TRI/PRO_Qkinz_peak[strip, dE/E]
Tri_Qkinz_peak = np.array([tri0, tri1, tri2, tri3, tri4, tri5, tri6, tri7])
Pro_Qkinz_peak = np.array([pro0, pro1, pro2, pro3, pro4, pro5, pro6, pro7])


gain_dE = np.zeros((n,n))
shift_dE = np.zeros((n,n))

gain_E = np.zeros((n,n))
shift_E = np.zeros((n,n))

shift_E_extra = np.zeros((n,n))
shift_dE_extra = np.zeros((n,n))

peaks_pro_E = (peaks_pro_E_2D + peaks_pro_E_proj)/2.
peaks_tri_E = (peaks_tri_E_2D + peaks_tri_E_proj)/2.

peaks_pro_dE = (peaks_pro_dE_2D + peaks_pro_dE_proj)/2.
peaks_tri_dE = (peaks_tri_dE_2D + peaks_tri_dE_proj)/2.

for i in range(n): #detectors
    for j in range(n): #strips
        gain_dE_raw = (Tri_Qkinz_peak[j,0] - Pro_Qkinz_peak[j,0])/(peaks_tri_dE[i,j] - peaks_pro_dE[i,j])
        gain_E_raw  = (Tri_Qkinz_peak[j,1] - Pro_Qkinz_peak[j,1])/(peaks_tri_E[i,j]  - peaks_pro_E[i,j])

        # 2.5 and 5  in the gain is from compansating for the initial gain and shift used when sorting,
        # i.e. the raw values found already had an initial gain and shift.
        gain_dE[i,j] = 2.5*gain_dE_raw
        gain_E[i,j] = 5*gain_E_raw

        shift_dE[i,j] = abs(Pro_Qkinz_peak[j,0]) - abs(gain_dE_raw*peaks_pro_dE[i,j])
        shift_E[i,j]  = abs(Pro_Qkinz_peak[j,1]) - abs(gain_E_raw* peaks_pro_E[i,j])

# Formatting to have a formatting which can be copy-pasted 
# into the gainshift file of usersort.

print "\nGains, E, gain:"
for k in range(n):
    print "%f %f %f %f %f %f %f %f " % (gain_E[k,0], gain_E[k,1], 
        gain_E[k,2], gain_E[k,3], gain_E[k,4], gain_E[k,5], gain_E[k,6], gain_E[k,7])

print "\nGains, dE, gain: "
for k in range(n):
    print "%f %f %f %f %f %f %f %f " % (gain_dE[k,0], gain_dE[k,1], 
        gain_dE[k,2], gain_dE[k,3], gain_dE[k,4], gain_dE[k,5], gain_dE[k,6], gain_dE[k,7])

print "\nShift, E, shift: "
for k in range(n):
    print "%f %f %f %f %f %f %f %f " % (shift_E[k,0], shift_E[k,1], 
        shift_E[k,2], shift_E[k,3], shift_E[k,4], shift_E[k,5], shift_E[k,6], shift_E[k,7])

print "\nShift, dE, shift: "
for k in range(n):
    print "%f %f %f %f %f %f %f %f " % (shift_dE[k,0], shift_dE[k,1], 
        shift_dE[k,2], shift_dE[k,3], shift_dE[k,4], shift_dE[k,5], shift_dE[k,6], shift_dE[k,7])
