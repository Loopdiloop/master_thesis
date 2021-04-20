These scripts were used for plotting and fitting data of the thesis. They assume there is one folder here with arcdrc-data (PSF) for plotting of gSF w/arcdrc, and a folder called data with .json files of external experimental data for the gSF comparisons.

The scripst are not particurarly nice, but thay are, at the time of writing, very functional. No judgement please, I have limited time.

Everything runs in python 3.8+. Curvefit dependent on lmfit.


Python scripts of this folder:

* Supporting files

    loading_data_gSF.py - Loads gSF data for other scripts.

    loading_data_NLD.py - Loads NLD data for other scripts.

    stylesheet.py - when you don't bother remembering the plotting colors of different plots and just import them instead.

* gSF

    gSF.py - Plot both gSF from 187+188Re.

    gSF_systematic_errors.py - Plots both gSF with systematic error estimates from subfolders of mama_x.

    curve_fit_gSF.py - Plots and fits the data to external data with the given Lorentz functions.

* NLD
    
    NLD.py - Plots both NLDs.

    NLD_systematic_errors.py - calculates and plots systematic errors from subfolders of mama_x

* matrix

    matrix_plot.py - Loads and plots the alfna-matrices. 

    run_matrix_plot.py - Good at plotting several of the matrixes in matrix_plot.py, or plot cross sections of several matrices.

