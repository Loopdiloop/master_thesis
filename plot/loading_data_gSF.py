import matplotlib.pyplot as plt
import numpy as np
import json
import sys




def cs_to_gsf(Eg, data):
    # input in MeV and milibarn -> use this conversion factor.
    exp = 8.674e-8
    return data*exp/Eg

def extract_dataset(data, x_i,y_i,yerror_i):
    """ Extracting data from input files from MAMA, adding them to useful arrays."""
    x = []; y = [] ; yerror = []
    
    for j in range(len(data)):
        y.append(data[j][y_i]) # MeV
        yerror.append(data[j][yerror_i]) # MeV
        x.append(data[j][x_i])

    x = np.array(x) ; y = np.array(y) ; yerror = np.array(yerror)
    return x,y,yerror



# *************************************************************************** #
# *****************    (a,d) data points    **********************************#


def load_a_d(path="../mama_d/"):
    a0_d = -0.8875
    a1_d = 0.2480

    strength_nrm_d = np.genfromtxt(path+"strength.nrm")
    strength_d = strength_nrm_d[:28]
    strength_err_d = strength_nrm_d[29:]
    n_d = len(strength_d)

    energy_d = np.zeros(n_d)
    for i in range(n_d):
        energy_d[i] = a0_d + a1_d*i

    # (a,d) extrapolation
    trans_raw_d = np.genfromtxt(path+"transext.nrm")
    n_d_t=len(trans_raw_d)
    trans_d=np.zeros(n_d_t)
    energy_trans_d=np.zeros(n_d_t)
    for i in range(n_d_t):
        energy_trans_d[i] = a0_d + a1_d*i
        trans_d[i] = trans_raw_d[i]/(2*3.14*energy_trans_d[i]**3)

    #number of data points to ignore
    n_ign = 7 #ignore
    a_d_data = np.zeros((len(energy_d)-n_ign,3))
    a_d_data[:,0] = energy_d[n_ign:]
    a_d_data[:,1] = strength_d[n_ign:]
    a_d_data[:,2] = strength_err_d[n_ign:-1]
    
    return a_d_data



# *************************************************************************** #
# *****************    (a,t) data points    **********************************#

def load_a_t(path="../mama_t/recommended_values/"):
    a0_t = -0.8875
    a1_t = 0.2480

    strength_nrm_t = np.genfromtxt(path+"strength.nrm")
    strength_t = strength_nrm_t[:26]
    strength_err_t = strength_nrm_t[27:]
    n_t = len(strength_t)
    energy_t = np.zeros(n_t)

    for i in range(n_t):
        energy_t[i] = a0_t + a1_t*i

    # (a,t) extrapolation
    trans_raw_t = np.genfromtxt(path+"transext.nrm")
    n_d_t = len(trans_raw_t)
    trans_t = np.zeros(n_d_t)
    energy_trans_t = np.zeros(n_d_t)
    for i in range(n_d_t):
        energy_trans_t[i] = a0_t + a1_t*i
        trans_t[i] = trans_raw_t[i]/(2*3.14*energy_trans_t[i]**3)

    #number of data points to ignore
    n_ign = 7 #ignore
    a_t_data = np.zeros((len(energy_t)-n_ign,3))
    a_t_data[:,0] = energy_t[n_ign:]
    a_t_data[:,1] = strength_t[n_ign:]
    a_t_data[:,2] = strength_err_t[n_ign:-1]
    return a_t_data
    
    

# *************************************************************************** #
# *****************    GENERAL data points    **********************************#

def load_data(path="../mama_d/recommended_values/", reaction="d", return_trans=False):
    
    if reaction == "d":
        arr_cut = 28    # From strength.cpp -> int i=0 -> i++ -> if(i<29): .... the rest is statistical error est.
        n_ign = 7 #ignore
        
    elif reaction == "t":
        arr_cut = 26
        n_ign = 7 #ignore
    a0 = -0.8875
    a1 = 0.2480
    
    strength_nrm = np.genfromtxt(path+"strength.nrm")
    strength = strength_nrm[:arr_cut]
    strength_err = strength_nrm[arr_cut+1:]
    n = len(strength)
    energy = np.zeros(n)

    for i in range(n):
        energy[i] = a0 + a1*i

    # (a,t) extrapolation
    trans_raw = np.genfromtxt(path+"transext.nrm")
    n_trans = len(trans_raw)
    trans = np.zeros(n_trans)
    energy_trans = np.zeros(n_trans)
    for i in range(n_trans):
        energy_trans[i] = a0 + a1*i
        trans[i] = trans_raw[i]/(2*3.14*energy_trans[i]**3)

    #number of data points to ignore
    data = np.zeros((len(energy)-n_ign,3))
    data[:,0] = energy[n_ign:]
    data[:,1] = strength[n_ign:]
    data[:,2] = strength_err[n_ign:-1]
    if return_trans == True:
        return data, energy_trans, trans
    else: # don't return trans, i.e. extrapolation
        return data


















def load_data_187Re():
    with open("data/187Re.json") as K:
        data_187Re = json.load(K)
    datasets_187Re=data_187Re["datasets"]


    # Dataset 1
    Eg_dataset1, gsf_dataset1, gsf_err_dataset1 =  extract_dataset(datasets_187Re[0]["data"], 2, 0, 1)

    gsf_dataset1 = cs_to_gsf(Eg_dataset1, gsf_dataset1)
    gsf_err_dataset1 = cs_to_gsf(Eg_dataset1, gsf_err_dataset1)

    #plt.errorbar(Eg_dataset1, gsf_dataset1, yerr=gsf_err_dataset1, x_err=None, fmt="*-", color="#CA5518", label="187Re(g,x)")

    #number of data points to ignore
    n_ign = 0 #ignore
    re187_data1 = np.zeros((len(Eg_dataset1)-n_ign,3))
    re187_data1[:,0] = Eg_dataset1[n_ign:]
    re187_data1[:,1] = gsf_dataset1[n_ign:]
    re187_data1[:,2] = gsf_err_dataset1[n_ign:]
    

    # Dataset 2

    Eg_dataset2, gsf_dataset2, gsf_err_dataset2 =  extract_dataset(datasets_187Re[1]["data"], 3, 0, 1)

    gsf_dataset2 = cs_to_gsf(Eg_dataset2, gsf_dataset2)
    gsf_err_dataset2 = cs_to_gsf(Eg_dataset2, gsf_err_dataset2)

    #plt.errorbar(Eg_dataset2, gsf_dataset2, yerr=gsf_err_dataset2, x_err=None, fmt="*-", color="#1A1118", label="187Re(g,x)")
    #number of data points to ignore
    n_ign = 1 #ignore
    re187_data2 = np.zeros((len(Eg_dataset2)-n_ign,3))
    re187_data2[:,0] = Eg_dataset2[n_ign:]
    re187_data2[:,1] = gsf_dataset2[n_ign:]
    re187_data2[:,2] = gsf_err_dataset2[n_ign:]


    return re187_data1, re187_data2



# ***************** Dataset 185Re ***************************
def load_data_185Re():
    with open("data/185Re.json") as J:
        data_185Re = json.load(J)
    dataset_185Re=data_185Re["datasets"]


    Eg_185Re, gsf_185Re, gsf_err_185Re =  extract_dataset(dataset_185Re[0]["data"], 2, 0, 1)

    gsf_185Re= cs_to_gsf(Eg_185Re, gsf_185Re)
    gsf_err_185Re = cs_to_gsf(Eg_185Re, gsf_err_185Re)

    re185_data = np.zeros((len(Eg_185Re),3))
    re185_data[:,0] = Eg_185Re
    re185_data[:,1] = gsf_185Re
    re185_data[:,2] = gsf_err_185Re

    return re185_data


# ***************** Dataset 186W ***************************
def load_data_186W():
    with open("data/186W.json") as J:
        data_186W = json.load(J)
    dataset_186W=data_186W["datasets"]


    Eg_186W, gsf_186W, gsf_err_186W =  extract_dataset(dataset_186W[0]["data"], 2, 0, 1)

    gsf_186W= cs_to_gsf(Eg_186W, gsf_186W)
    gsf_err_186W = cs_to_gsf(Eg_186W, gsf_err_186W)

    w185_data = np.zeros((len(Eg_186W),3))
    w185_data[:,0] = Eg_186W
    w185_data[:,1] = gsf_186W
    w185_data[:,2] = gsf_err_186W

    return w185_data


# ***************** Dataset ARCDRC ***************************
def load_data_ARCDRC(EorM, Z, A):
    """ EorM is a one character string of wether you want the M1 or E1
    Recommended input for the relevant data here:
    ALL E of Z-1 and Z+1 :
    #### -rw-rw-r-- 1 marianne marianne  1371 juni  18  2019 fE1_exp_074_183_drc.dat
    -rw-rw-r-- 1 marianne marianne  1821 juni  18  2019 fE1_exp_074_184_arc.dat
    -rw-rw-r-- 1 marianne marianne  1371 juni  18  2019 fE1_exp_074_185_arc.dat
    -rw-rw-r-- 1 marianne marianne  1326 juni  18  2019 fE1_exp_074_187_arc.dat

    -rw-rw-r-- 1 marianne marianne  1371 juni  18  2019 fE1_exp_076_188_arc.dat
    -rw-rw-r-- 1 marianne marianne  1956 juni  18  2019 fE1_exp_076_189_arc.dat
    -rw-rw-r-- 1 marianne marianne  1686 juni  18  2019 fE1_exp_076_191_arc.dat
    -rw-rw-r-- 1 marianne marianne  1281 juni  18  2019 fE1_exp_076_193_arc.dat

    -rw-rw-r-- 1 marianne marianne  1551 juni  18  2019 fE1_exp_077_192_arc.dat
    -rw-rw-r-- 1 marianne marianne  1551 juni  18  2019 fE1_exp_077_194_arc.dat



    ALL M of Z +- 1: -------------------------
    #### -rw-rw-r-- 1 marianne marianne   606 juni  18  2019 fM1_exp_074_183_drc.dat
    -rw-rw-r-- 1 marianne marianne   831 juni  18  2019 fM1_exp_074_184_arc.dat
    -rw-rw-r-- 1 marianne marianne   606 juni  18  2019 fM1_exp_074_185_arc.dat
    -rw-rw-r-- 1 marianne marianne   876 juni  18  2019 fM1_exp_074_187_arc.dat

    -rw-rw-r-- 1 marianne marianne   606 juni  18  2019 fM1_exp_076_188_arc.dat
    -rw-rw-r-- 1 marianne marianne   786 juni  18  2019 fM1_exp_076_189_arc.dat
    -rw-rw-r-- 1 marianne marianne   786 juni  18  2019 fM1_exp_076_191_arc.dat
    """
    with open("arcdrc/f%s1_exp_0%s_%s_arc.dat"%(EorM, Z, A),"r") as J:
        readit = J.read()

    X1 = readit.split("\n")[11:]
    data_arcdrc = np.zeros((len(X1)-1, 3))
    for i in range(len(X1)-1):
        d = X1[i].split()
        if len(d) > 1:
            data_arcdrc[i,0] = float(d[0])
            data_arcdrc[i,1] = float(d[2])
            data_arcdrc[i,2] = float(d[3])

    return data_arcdrc
