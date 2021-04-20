""" Script for calulating gains and shifts of peaks in NaI for 
1.868MeV and 5.270 MeV in 15N. Output must be reformatted slightly 
before being copied into the gainshift-file of the sorting usersort.
"""

import numpy as np 

peaks = np.loadtxt('gammacalib_NaI_peaks.txt', dtype=None)

peaks_6k = peaks[:,2] /5
peaks_2k = peaks[:,1] /5
i = peaks[:,0]

actual_6k = 5270.
#actual_2k = 2582. # From experimentation
actual_2k = 1868.

gain = (actual_6k - actual_2k)/(peaks_6k - peaks_2k)
shift = actual_6k - peaks_6k*gain

print('i: ', i)
print('gain: ', gain)
print('shift: ', shift)

# Formatting for missing channels not in array i:

N = 32 #no. channels, 0 -> 31
gain_formatted = np.zeros(N)
shift_formatted = np.zeros(N)

for j in range(len(i)):
	I = int(i[j])
	gain_formatted[I] = gain[j]
	shift_formatted[I] = shift[j]

print('gain formatted: ', gain_formatted)
print('shift formatted: ', shift_formatted)
