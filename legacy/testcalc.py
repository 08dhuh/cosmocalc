import numpy as np
import sys
import mpmath
import math
import matplotlib.pyplot as plt
import os
# import astropy

# ---------------------------------------------------------
arguments = sys.argv[1:]
H0 = float(arguments[0])
omega_M = float(arguments[1])
omega_Lambda = float(arguments[2])
omega_rad = float(arguments[3])
w = float(arguments[4])
wa = float(arguments[5])
z = arguments[6]
zs = np.array([float(i) for i in z.split(',')])

#params = [float(a) for a in arguments]
#arg_names = ['H0', 'omega_M', 'omega_Lambda', 'omega_rad', 'w', 'wa', 'z']

# ---------------------------------------------------------
c = 2.99792458e5   # in units of km
Mpc2km = 3.08567758147e+19     # converts Mpc to km
seconds_in_a_year = 31557600.   # julian
omega_k = 1. - omega_M - omega_Lambda - omega_rad  # curvature term

# The integrals
def E(z): return np.sqrt(omega_M*(1.+z)**3. + omega_k*(1.+z)**2. + omega_rad *
                         (1.+z)**4. + omega_Lambda*(1.+z)**(3.*(1.+w+wa))*
                         math.exp(-3.*wa*(1.-1./(1.+z))))
def freidman(z): return 1./E(z)
def tage_int(z): return 1./((1+z)*E(z))

# ---------------------------------------------------------
def dm(z):
        DH = c/H0                                                                                 # hubble distance
        freidman_integral = float(mpmath.quad(freidman,[0,z]))  # comoving distance

        # The comoving distance, r, and the comoving volume, Vc, are dependant on the curvature of the universe
        # is it a flat universe?
        if omega_k >= -1.e-15 and omega_k <= 1.e-15:
                r = DH*freidman_integral                                # Comoving distance
                Vc = 4./3.*np.pi * r**3. /(1.e9)                # Comoving volume (Gpc**3), true only in an omega_k=1 Universe
        # or is there curvature?
        elif omega_k < -1.e-15:
                r = DH / np.sqrt(abs(omega_k)) * np.sin(np.sqrt(abs(omega_k))*freidman_integral)        # Comoving distance
                Vc = ((4*np.pi*DH**3)/(2*omega_k))*(  r/DH*np.sqrt(1+omega_k*(r/DH)**2)\
                -1/np.sqrt(abs(omega_k))*np.arcsin(np.sqrt(abs(omega_k))*r/DH)   )/(1.e9)                       # Comoving volume (Gpc**3), true only in an omega_k=1 Universe
        elif omega_k > 1.e-15:
                r = DH / np.sqrt(omega_k) * np.sinh(np.sqrt(omega_k)*freidman_integral)                         # Comoving distance
                Vc = ((4*np.pi*DH**3)/(2*omega_k))*(  (r/DH)*np.sqrt(1+omega_k*(r/DH)**2)\
                -1/np.sqrt(abs(omega_k))*np.arcsinh(np.sqrt(abs(omega_k))*r/DH)  )/(1.e9)                       # Comoving volume (Gpc**3), true only in an omega_k=1 Universe

        # The rest follows from the comoving distance
        DL = r * (1.+z)                                                         # luminosity distance
        DA = r / (1.+z)                                                         # angular diameter distance
        mu = 5. * np.log10(DL * 10**5)                          # distance modulus
        Vc = 4./3.*np.pi * r**3.        / (10.**9.)             # Comoving volume (Gpc**3), true only in an omega_k=1 Universe
        dVc_elt = DA**2.*DH*(1+z)**2./E(z)                      # Comoving volume element (Gpc**3), true only in an omega_k=1 Universe

        # The ages get their own integral, and don't change with curvature:
        age_today = 1./H0*float( mpmath.quad(tage_int, [0,float('inf')]) ) * (Mpc2km)/(seconds_in_a_year)/(1.e9) # age at redshift zero (Gyr)
        tage = 1./H0*float( mpmath.quad(tage_int, [z,float('inf')]) ) * (Mpc2km)/(seconds_in_a_year)/(1.e9)             # age at redshift z (Gyr)
        tlb = 1./H0*float( mpmath.quad(tage_int, [0,z]) ) * (Mpc2km)/(seconds_in_a_year)/(1.e9)                                 # lookback time (Gyr)

        return r, DL, DA, Vc, mu, tage, tlb, dVc_elt, age_today



x = np.linspace(0,5,100)[1:]
calc_results = np.transpose([dm(z) for z in x])
label = [
 "Comoving distance", 
 "Luminosity distance", 
 "Angular Diameter distance", 
 "Comoving volume", 
 "Distance modulus", 
 "Age at z", 
 "Lookback time", 
 "Comoving volume element","Age at z=0", ]
unit = ['Mpc','Mpc','Mpc','Gpc3','','Gyr','Gyr','(dVC / dz)']
fig, axs = plt.subplots(nrows=8, ncols=1, figsize=(7,49))
for i in range(8):
    axs[i].plot(x,calc_results[i], )
    axs[i].set_title(label[i])
    axs[i].set_xlabel('redshift')
    axs[i].set_ylabel(label[i]+' /'+unit[i])
    
fig.savefig('assets/plot.png')

# buffer = io.BytesIO()
# plt.savefig(buffer, format='png')
# buffer.seek(0)
# plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

formatter = lambda array, dec=5: ' '.join([str(round(ele, dec)) if isinstance(ele, (int, float)) else ele for ele in array])

for z in zs:
    print(z)
    print(formatter(dm(z)))
    #print(plot_data)
    #print(formatter(nw_calc(z)))
    

# args = ' '.join([str(float(a)) for a in arguments])
# print(args)
# print('hello')
# print(arguments[0])
# print(sys.argv[2])
# print(sys.argv)
