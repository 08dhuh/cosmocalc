#!/usr/bin/python
# -------------------------------
import numpy as np
import sys
import mpmath
import math
# ----------------------------------------------------------------
import astropy
# arguments = " ".join(sys.argv[1:]).split('#')
arguments = sys.argv[1:]
H0 = float(arguments[0])
omega_M = float(arguments[1])
omega_Lambda = float(arguments[2])
omega_rad = float(arguments[3])
w = float(arguments[4])
wa = float(arguments[5])
z = arguments[6]
z = [float(i) for i in z.split(',')]
# -------------------------------

c = 2.99792458e5                                        # in units of km
Mpc2km = 3.08567758147e+19                      # converts Mpc to km
seconds_in_a_year = 31557600.           # julian

omega_k = 1. - omega_M - omega_Lambda - omega_rad  # curvature term

# The integrals


def E(z): return np.sqrt(omega_M*(1.+z)**3. + omega_k*(1.+z)**2. + omega_rad *
                         (1.+z)**4. + omega_Lambda*(1.+z)**(3.*(1.+w+wa))*math.exp(-3.*wa*(1.-1./(1.+z))))
# ( w_CPL(z) = w + wa*(1./(1.+z)) )
def freidman(z): return 1./E(z)
def tage_int(z): return 1./((1+z)*E(z))


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

    return r, DL, DA, Vc, mu, tage, tlb, dVc_elt, age_today

# ned wright calculator


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

    return DCMR_Mpc, DL_Mpc, DA_Mpc, V_Gpc, 5*np.log10(DL_Mpc*1e6)-5, zage_Gyr, DTT_Gyr, '-', age_Gyr


htmlstr = """
        <html>
        <head><title>
        Cosmology Calculator Results
        </title></head>

        <style type="text/css">
         .bb td, .bb th {
         border-bottom: 1px solid black;
         }
        </style>

        <b>Here are your super-accurate results!</b><br>
        You can copy/paste this entire table into any spreadsheet application and it will fill the cells in a well-behaved manner.<br><br>
        For H<sub>0</sub>=<b>{}</b> km.s<sup>-1</sup>Mpc<sup>-1</sup>,&nbsp;&nbsp;&#937<sub>M</sub>=<b>{}</b>,&nbsp;&nbsp;&#937<sub>&#923</sub>=<b>{}</b>,&nbsp;&nbsp;&#937<sub>R</sub>=<b>{}</b>,&nbsp;&nbsp;w=<b>{}</b>,&nbsp;&nbsp;wa=<b>{}</b>
        """.format(H0, omega_M, omega_Lambda, omega_rad, w, wa)

if len(z) == 1:
    z = z[0]
    # Run the calculator
    r, DL, DA, Vc, mu, tage, tlb, dVc_elt, age_today = dm(z)

    # Run Ned Wright's calculator
    r_nw, DL_nw, DA_nw, Vc_nw, mu_nw, tage_nw, tlb_nw, dVc_elt_nw, age_today_nw = nw_calc(
        z)

    # make html output

    htmlstr += f"""At <b>z={z}:</b><br>
<table cellpadding='5' cellspacing='0' align='left'>
<tr class="bb"><td></td><td><b>UniMelb Calculator</b></td><td><b>Ned Wright Calculator*</b></td></tr>
<tr><td><b>Age at z=0:</b></td><td>{age_today:0.5f} <b>Gyr</b></td><td>{age_today_nw:0.5f} <b>Gyr</b></td></tr>
<tr><td><b>Comoving distance:</b></td><td>{r:0.5f} <b>Mpc</b></td><td>{r_nw:0.5f} <b>Mpc</b></td></tr>
<tr><td><b>Luminosity distance:</b></td><td>{DL:0.5f} <b>Mpc</b></td><td>{DL_nw:0.5f} <b>Mpc</b></td></tr>
<tr><td><b>Angular Diameter distance:</b></td><td>{DA:0.5f} <b>Mpc</b></td><td>{DA_nw:0.5f} <b>Mpc</b></td></tr>
<tr><td><b>Comoving volume:</b></td><td>{Vc:0.5f} <b>Mpc<sup>3</sup></b></td><td>{Vc_nw:0.5f} <b>Mpc<sup>3</sup></b></td></tr>
<tr><td><b>Distance modulus:</b></td><td>{mu:0.5f} <b>mag</b></td><td>{mu_nw:0.5f} <b>mag</b></td></tr>
<tr><td><b>Age at z:</b></td><td>{tage:0.5f} <b>Gyr</b></td><td>{tage_nw:0.5f} <b>Gyr</b></td></tr>
<tr><td><b>Lookback time:</b></td><td>{tlb:0.5f} <b>Gyr</b></td><td>{tlb_nw:0.5f} <b>Gyr</b></td></tr>
<tr class="bb"><td><b>Comoving volume element:</b></td><td>{dVc_elt:0.5e} <b>Mpc<sup>3</sup>dw<sup>-1</sup>dz<sup>-1</sup></b></td><td>---</td></tr>
</table>
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
*Ned Wright values use a cruder integrator than the UniMelb values, and assume &#969=-1 always, so are slightly less accurate.<br>
        Made by: <b>Robert L. Barone-Nugent</b>, <b>Catherine O. de Burgh-Day</b> and <b>Jaehong Park</b>, 2014.
        """

    print(htmlstr)  # python3

else:
    # make html output
    htmlstr += """
        <table cellpadding='5' cellspacing='0' align='left'>

        <tr class="bb"><td><b>z</b></td><td><b>Age at z=0 (Gyr)</b></td><td><b>Comoving Distance (Mpc)</b></td><td><b>Luminosity Distance (Mpc)</b></td><td><b>Angular Diameter Distance (Mp>
        """

    for z_iter in z:
        # Run the calculator
        r, DL, DA, Vc, mu, tage, tlb, dVc_elt, age_today = dm(z_iter)

        htmlstr += """
                <tr><td>%s</td><td>%0.5f</td><td>%0.5f</td><td>%0.5f</td><td>%0.5f</td> <td>%0.5f</td><td>%0.5f</td><td>%0.5f</td><td>%0.5f</td><td>%0.5e</td></tr>
                """ % (z_iter, age_today, r, DL, DA, Vc, mu, tage, tlb, dVc_elt)

    htmlstr += """
        <tr class="bb"><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"""
    # htmlstr += """<br>"""*(5)
    htmlstr += """</table>"""
    htmlstr += """Made by: <b>Robert L. Barone-Nugent</b>, <b>Catherine O. de Burgh-Day</b> and <b>Jaehong Park</b>, 2014."""

    print(htmlstr)  # python3
