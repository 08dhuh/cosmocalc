import numpy as np
import sys
import mpmath
import math
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
    # hubble distance
    DH = c/H0
    freidman_integral = float(mpmath.quad(
        freidman, [0, z]))  # comoving distance

    # The comoving distance, r, and the comoving volume, Vc, are dependant on the curvature of the universe
    # is it a flat universe?
    if omega_k >= -1.e-15 and omega_k <= 1.e-15:
        r = DH*freidman_integral                                # Comoving distance
        # Comoving volume (Gpc**3), true only in an omega_k=1 Universe
        Vc = 4./3.*np.pi * r**3. / (1.e9)
    # or is there curvature?
    elif omega_k < -1.e-15:
        r = DH / np.sqrt(abs(omega_k)) * np.sin(np.sqrt(abs(omega_k))
                                                * freidman_integral)        # Comoving distance
        Vc = ((4*np.pi*DH**3)/(2*omega_k))*(r/DH*np.sqrt(1+omega_k*(r/DH)**2)
                                            - 1/np.sqrt(abs(omega_k))*np.arcsin(np.sqrt(abs(omega_k))*r/DH))/(1.e9)                       # Comoving volume (Gpc**3), true only in an omega_k=1 Universe
    elif omega_k > 1.e-15:
        # Comoving distance
        r = DH / np.sqrt(omega_k) * np.sinh(np.sqrt(omega_k)*freidman_integral)
        Vc = ((4*np.pi*DH**3)/(2*omega_k))*((r/DH)*np.sqrt(1+omega_k*(r/DH)**2)
                                            - 1/np.sqrt(abs(omega_k))*np.arcsinh(np.sqrt(abs(omega_k))*r/DH))/(1.e9)                       # Comoving volume (Gpc**3), true only in an omega_k=1 Universe

    # The rest follows from the comoving distance
    # luminosity distance
    DL = r * (1.+z)
    # angular diameter distance
    DA = r / (1.+z)
    mu = 5. * np.log10(DL * 10**5)                          # distance modulus
    # Comoving volume (Gpc**3), true only in an omega_k=1 Universe
    Vc = 4./3.*np.pi * r**3. / (10.**9.)
    # Comoving volume element (Gpc**3), true only in an omega_k=1 Universe
    dVc_elt = DA**2.*DH*(1+z)**2./E(z)

    # The ages get their own integral, and don't change with curvature:
    age_today = 1./H0*float(mpmath.quad(tage_int, [0, float('inf')])) * (
        Mpc2km)/(seconds_in_a_year)/(1.e9)  # age at redshift zero (Gyr)
    tage = 1./H0*float(mpmath.quad(tage_int, [z, float('inf')])) * (Mpc2km)/(
        seconds_in_a_year)/(1.e9)             # age at redshift z (Gyr)
    # lookback time (Gyr)
    tlb = 1./H0 * \
        float(mpmath.quad(tage_int, [0, z])) * \
        (Mpc2km)/(seconds_in_a_year)/(1.e9)

    #return r, DL, DA, Vc, mu, tage, tlb, dVc_elt, age_today
    return age_today, r, DL, DA, Vc, mu, tage, tlb, dVc_elt


def nw_calc(z):
    WM = omega_M
    WV = omega_Lambda
    WR = 0.        # Omega(radiation)
    WK = 0.        # Omega curvaturve = 1-Omega(total)
    Tyr = 977.8    # coefficent for converting 1/H into Gyr
    DTT = 0.5      # time from z to now in units of 1/H0
    DTT_Gyr = 0.0  # value of DTT in Gyr
    age = 0.5      # age of Universe in units of 1/H0
    age_Gyr = 0.0  # value of age in Gyr
    zage = 0.1     # age of Universe at redshift z in units of 1/H0
    zage_Gyr = 0.0  # value of zage in Gyr
    DCMR = 0.0     # comoving radial distance in units of c/H0
    DCMR_Mpc = 0.0
    DCMR_Gyr = 0.0
    DA = 0.0       # angular size distance
    DA_Mpc = 0.0
    DA_Gyr = 0.0
    kpc_DA = 0.0
    DL = 0.0       # luminosity distance
    DL_Mpc = 0.0
    DL_Gyr = 0.0   # DL in units of billions of light years
    V_Gpc = 0.0
    a = 1.0        # 1/(1+z), the scale factor of the Universe
    az = 0.5       # 1/(1+z(object))

    h = H0/100.
    WR = 4.165E-5/(h*h)   # includes 3 massless neutrino species, T0 = 2.72528
    WK = 1-WM-WR-WV
    az = 1.0/(1+1.0*z)
    age = 0.
    n = 1000         # number of points in integrals
    for i in range(n):
        a = az*(i+0.5)/n
        adot = np.sqrt(WK+(WM/a)+(WR/(a*a))+(WV*a*a))
        age = age + 1./adot

    zage = az*age/n
    zage_Gyr = (Tyr/H0)*zage
    DTT = 0.0
    DCMR = 0.0

    # do integral over a=1/(1+z) from az to 1 in n steps, midpoint rule
    for i in range(n):
        a = az+(1-az)*(i+0.5)/n
        adot = np.sqrt(WK+(WM/a)+(WR/(a*a))+(WV*a*a))
        DTT = DTT + 1./adot
        DCMR = DCMR + 1./(a*adot)

    DTT = (1.-az)*DTT/n
    DCMR = (1.-az)*DCMR/n
    age = DTT+zage
    age_Gyr = age*(Tyr/H0)
    DTT_Gyr = (Tyr/H0)*DTT
    DCMR_Gyr = (Tyr/H0)*DCMR
    DCMR_Mpc = (c/H0)*DCMR

    # tangential comoving distance
    ratio = 1.00
    x = np.sqrt(abs(WK))*DCMR
    if x > 0.1:
        if WK > 0:
            ratio = 0.5*(np.exp(x)-np.exp(-x))/x
        else:
            ratio = np.sin(x)/x
    else:
        y = x*x
        if WK < 0:
            y = -y
        ratio = 1. + y/6. + y*y/120.
    DCMT = ratio*DCMR
    DA = az*DCMT
    DA_Mpc = (c/H0)*DA
    kpc_DA = DA_Mpc/206.264806
    DA_Gyr = (Tyr/H0)*DA
    DL = DA/(az*az)
    DL_Mpc = (c/H0)*DL
    DL_Gyr = (Tyr/H0)*DL
    # comoving volume computation
    ratio = 1.00
    x = np.sqrt(abs(WK))*DCMR
    if x > 0.1:
        if WK > 0:
            ratio = (0.125*(np.exp(2.*x)-np.exp(-2.*x))-x/2.)/(x*x*x/3.)
        else:
            ratio = (x/2. - np.sin(2.*x)/4.)/(x*x*x/3.)
    else:
        y = x*x
        if WK < 0:
            y = -y
        ratio = 1. + y/5. + (2./105.)*y*y
    VCM = ratio*DCMR*DCMR*DCMR/3.
    V_Gpc = 4.*np.pi*((0.001*c/H0)**3)*VCM

    #return DCMR_Mpc, DL_Mpc, DA_Mpc, V_Gpc, 5*np.log10(DL_Mpc*1e6)-5, zage_Gyr, DTT_Gyr, '-', age_Gyr
    return age_Gyr, DCMR_Mpc, DL_Mpc, DA_Mpc, V_Gpc, 5*np.log10(DL_Mpc*1e6)-5, zage_Gyr, DTT_Gyr, '-'

formatter = lambda array, dec=5: ' '.join([str(round(ele, dec)) if isinstance(ele, (int, float)) else ele for ele in array])

for z in zs:
    print(z)
    print(formatter(dm(z)))
    print(formatter(nw_calc(z)))

# args = ' '.join([str(float(a)) for a in arguments])
# print(args)
# print('hello')
# print(arguments[0])
# print(sys.argv[2])
# print(sys.argv)
