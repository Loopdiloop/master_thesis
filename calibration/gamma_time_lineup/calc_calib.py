""" Script for calulating shifts of time alignment, assuming gain is of no signgificant relevance to the area we're interested in. 
"""

import numpy as np 

i, peaks = np.loadtxt('time_alignment_peaks.txt', unpack=True)#, delimiter=" ", 
#peaks = loaded_peaks[:,1]


actual = 200.

#gain = (actual_6k - actual_2k)/(peaks_6k - peaks_2k)
shift = actual - peaks

print('i: ', i)
#print('gain: ', gain)
print('shift: ', shift)

# Formatting for missing channels not in array i:

N = 32 #no. channels, 0 -> 31
#gain_formatted = np.zeros(N)
shift_formatted = np.zeros(N)

for j in range(len(i)):
	I = int(i[j])
	#gain_formatted[I] = gain[j]
	shift_formatted[I] = shift[j]

#print('gain formatted: ', gain_formatted)
print('shift formatted: ', shift_formatted)
