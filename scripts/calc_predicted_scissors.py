
import numpy as np


def Ex_beta(A, beta2):
    return 66*beta2*np.sqrt(0.8952)* A**(-1/3)
    
def Ex_delta(A, delta):
    return 66*delta* A**(-1/3)

print("hfb, 187: ", Ex_beta(187, 0.23))
print("hfb, 188: ", Ex_beta(188, 0.21))

hfb_187 = Ex_beta(187, 0.23)
hfb_188 = Ex_beta(188, 0.21)

print("hfb1m, 187: ", Ex_beta(187, 0.23))
print("hfb1m, 188: ", Ex_beta(188, 0.22))

hfb1m_187 = Ex_beta(187, 0.23)
hfb1m_188 = Ex_beta(188, 0.22)

print(" **************** ")

deltas=[0.110, 0.115, 0.132, 0.171, 0.233, 0.124, 0.165, 0.249, 0.273, 0.253, 0.271, 0.278, 0.282, 
    0.271, 0.274, 0.278, 0.274, 0.274, 0.274, 0.265, 0.262, 0.249, 0.241, 0.230, 0.225, 0.208, 
    0.196, 0.188, 0.151, 0.143, 0.125, 0.115]

omegas=[3.00, 3.15, 3.46, 3.49, 3.12, 3.07,3.18, 2.97,3.26,
    2.91, 3.06, 3.10, 3.11, 2.87, 2.93, 2.97, 2.99, 3.24, 3.22, 3.03, 3.15,
    3.33, 3.28, 3.21, 3.19, 3.25, 3.37, 3.19, 2.87, 3.00, 3.25, 3.01]

masses=[142,144,146,148,150, 148, 150, 152, 154, 154, 156,
    158, 160, 160,162, 164, 166, 168, 
    170, 172, 174, 176, 176, 178, 180, 182, 184, 186, 190, 192, 194, 196]

strengths=[0.55, 0.72,
    0.94, 1.05, 1.83, 
    0.51, 0.97, 2.41, 2.44,
    2.99, 2.73, 3.71, 3.26,
    2.42, 2.85, 3.25, 2.55,
    3.68, 3.42, 1.83, 2.70,
    2.56, 3.11, 2.38, 2.04,
    1.34, 1.04, 0.82, 0.85,
    0.93, 1.38, 0.81]

Ex_predicted = []
for i in range(len(deltas)):
    Ex_predicted.append(Ex_delta(masses[i], deltas[i]))
    print(Ex_predicted[i], omegas[i])


import matplotlib.pyplot as plt


plt.plot(masses, omegas, linestyle="None", color="black", marker="o", label="J. Enders et al. (2005)")
plt.plot(masses, Ex_predicted, "g*", label="Formulae by A. Richter (1995)")

plt.plot(187, hfb_187, "^", label="$^{187}$Re hfb+hfb1m")
plt.plot(188, hfb_188, "v", label="$^{188}$Re hfb")
#plt.plot(187, hfb1m_187, "*")
plt.plot(188, hfb1m_188, "s", label="$^{188}$Re hfb1m")


plt.ylabel("$\omega_{M1}$ or $E_x$ [MeV]", fontsize=14)
plt.xlabel("Mass Number A", fontsize=14)
plt.grid(linestyle="--")
plt.yticks(range(0,6))
plt.xticks([140, 160, 180, 200])
plt.legend()

plt.show()

plt.clf()


plt.plot([0.23*np.sqrt(0.8952), 0.23*np.sqrt(0.8952)], [0.5,3.5] , "--", label="Pred. $\delta$ $^{187}$Re hfb+hfb1m")
plt.plot([0.21*np.sqrt(0.8952), 0.21*np.sqrt(0.8952)], [0.5,3.5], "-.", label="Pred. $\delta$ $^{188}$Re hfb")
plt.plot([0.22*np.sqrt(0.8952),0.22*np.sqrt(0.8952)], [0.5,3.5], "-", label="Pred. $\delta$ $^{188}$Re hfb1m")

plt.plot(deltas, strengths, "*", linestyle="None", color="black", marker="o", label="J.Enders et al. (2005)")


plt.ylabel("$\sum B(M1)$ [MeV]", fontsize=14)
plt.xlabel("Deformation $\delta$", fontsize=14)
plt.grid(linestyle="--")
#plt.yticks(range(0,5))
plt.legend()


plt.show()

