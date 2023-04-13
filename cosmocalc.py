import math
import numpy as np
from scipy.integrate import quad
from astropy import constants as const

# -------------------------------constants
c = const.c.to('km/s').value
mpc = 3.08567758147e+19
seconds_in_a_year = 31557600  # julian


cosmo_input_params = ['H0', 'w', 'wa', 'omega_rad', 'omega_M', 'omega_Lambda']


class Cosmocalc:
    """
    A class for calculating various cosmological parameters.

    Attributes:
        H0: Hubble constant in units of km/s/Mpc
        w: dark energy equation of state parameter
        wa: dark energy evolution parameter
        omega_rad: radiation density parameter
        omega_M: matter density parameter
        omega_Lambda: dark energy density parameter
        z: redshift
        DH: the comoving distance to the horizon at the present epoch

    Methods:
        _E(z):
            Calculates the value of the _E(z) function at the given redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The value of _E(z). 

        comoving_distance(z):
            Calculates the comoving distance to a redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The comoving distance in Mpc.

        luminosity_distance(z):
            Calculates the luminosity distance to a redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The luminosity distance in Mpc.

        angular_diameter_distance(z):
            Calculates the angular diameter distance to a redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The angular diameter distance in Mpc.

        comoving_volume_element(z):
            Calculates the comoving volume element at a redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The comoving volume element in Gpc^3.

        comoving_volume(z):
            Calculates the comoving volume out to a redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The comoving volume in Gpc^3.

        distance_modulus(z):
            Calculates the distance modulus to a redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The distance modulus.

        _calculate_age_universe(t_i, t_f):
            Calculates the age of the universe between t_i and t_f.
            Parameters:
                t_i : float
                    Initial time in Gyr.
                t_f : float
                    Final time in Gyr.
            Returns:
                float : The age of the universe in Gyr.

        light_travel_time(z):
            Calculates the light travel time to a redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The light travel time in Gyr.

        age_at_z(z):
            Calculates the age of the universe at a redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The age of the universe in Gyr at redshift z.

        age_today():
            Calculates the age of the universe today.
            Returns:
                float : The age of the universe in Gyr.
    """

    def __init__(self, H0: float, w: float, wa: float, omega_rad: float, omega_M: float, omega_Lambda: float):
        self._H0 = H0
        self._w = w
        self._wa = wa
        self._omega_rad = omega_rad
        self._omega_M = omega_M
        self._omega_Lambda = omega_Lambda
        self._DH = c/H0
        #self._omega_k = 1 - omega_M - omega_Lambda - omega_rad  # curvature
        self._update_cosmo_params()

    def _update_cosmo_params(self):
        self._omega_k = 1 - self.omega_M - self.omega_Lambda - self.omega_rad  # curvature
        self._cosmo_params = {
            'H0': self.H0,
            'DH': self.DH,
            'w': self.w,
            'wa': self.wa,
            'omega_rad': self.omega_rad,
            'omega_M': self.omega_M,
            'omega_Lambda': self.omega_Lambda,
            'omega_k': self.omega_k,
            # 'z': self.z
        }
    
                 

    @property
    def H0(self):
        return self._H0

    @H0.setter
    def H0(self, value):
        self._H0 = value
        self._DH = c/value
        self._update_cosmo_params()

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value
        self._update_cosmo_params()

    @property
    def wa(self):
        return self._wa

    @wa.setter
    def wa(self, value):
        self._wa = value
        self._update_cosmo_params()

    @property
    def omega_rad(self):
        return self._omega_rad

    @omega_rad.setter
    def omega_rad(self, value):
        self._omega_rad = value
        self._update_cosmo_params()

    @property
    def omega_M(self):
        return self._omega_M

    @omega_M.setter
    def omega_M(self, value):
        self._omega_M = value
        self._update_cosmo_params()

    @property
    def omega_Lambda(self):
        return self._omega_Lambda

    @omega_Lambda.setter
    def omega_Lambda(self, value):
        self._omega_Lambda = value
        self._update_cosmo_params()

    @property
    def omega_k(self):
        return self._omega_k

    @property
    def DH(self):
        return self._DH

    
    def _E(self, z):
        return np.sqrt(self.omega_M*(1+z)**3 + self.omega_k*(1+z)**2 + self.omega_rad*(1+z)**4
                       + self.omega_Lambda*(1+z)**(3*(1+self.w+self.wa))*math.exp(-3*self.wa*(1-1/(1+z))))

    def _freidman(self, z):
        return 1/self._E(z)

    def _tage_int(self, z):
        return 1/((1+z)*self._E(z))

    def comoving_distance(self, z):
        freidman_integral = float(quad(self._freidman, 0, z)[0])
        if self.omega_k < -1.e-15:  # closed universe
            r = self.DH / np.sqrt(abs(self.omega_k)) * \
                np.sin(np.sqrt(abs(self.omega_k))*freidman_integral)
        elif self.omega_k <= 1.e-15:  # flat universe
            r = self.DH*freidman_integral
        else:  # open universe
            r = self.DH / np.sqrt(self.omega_k) * \
                np.sinh(np.sqrt(self.omega_k)*freidman_integral)
        return r

    def luminosity_distance(self, z):
        return self.comoving_distance(z) * (1+z)

    def angular_diameter_distance(self, z):
        return self.comoving_distance(z) / (1+z)

    def comoving_volume_element(self, z):
        Vc_elt = self.DH * \
            (self.angular_diameter_distance(z)**2 * (1+z)**2 / self._E(z))
        return Vc_elt *1e-9

    def comoving_volume(self, z):
        r = self.comoving_distance(z)
        if self.omega_k < -1.e-15:  # closed universe
            Vc = ((4*np.pi*self.DH**3)/(2*self.omega_k))*(r/self.DH*np.sqrt(1+self.omega_k*(r/self.DH)**2)
                                                          - 1/np.sqrt(abs(self.omega_k))*np.arcsin(np.sqrt(abs(self.omega_k))*r/self.DH))/(1e9)
        elif self.omega_k <= 1.e-15:  # flat universe
            Vc = 4/3*np.pi * r**3 / (1.e9)
        else:
            Vc = ((4*np.pi*self.DH**3)/(2*self.omega_k))*((r/self.DH)*np.sqrt(1+self.omega_k*(r/self.DH)**2)
                                                          - 1/np.sqrt(abs(self.omega_k))*np.arcsinh(np.sqrt(abs(self.omega_k))*r/self.DH))/(1e9)
        return Vc

    def distance_modulus(self, z):
        return 5 * np.log10(self.luminosity_distance(z) * 10**5)

    def _calculate_age_universe(self, t_i, t_f):
        return 1/self.H0*quad(_tage_int, t_i, t_f, args=(self.omega_M, self.omega_k, self.omega_rad, self.omega_Lambda, self.w, self.wa))[0]\
            * float(mpc)/float(seconds_in_a_year)/(1e9)

    def light_travel_time(self, z):
        return self._calculate_age_universe(0, z)

    def age_at_z(self, z):
        return self._calculate_age_universe(z, np.inf)

    def age_today(self, z):
        return self._calculate_age_universe(0, np.inf)


def _E(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return np.sqrt(omega_M*(1+z)**3 + omega_k*(1+z)**2 + omega_rad*(1+z)**4
                   + omega_Lambda*(1+z)**(3*(1+w+wa))*math.exp(-3*wa*(1-1/(1+z))))


def _freidman(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return 1/_E(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa)



def _tage_int(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return 1/((1+z)*_E(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa))



def comoving_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa, DH):
    freidman_integral = float(quad(_freidman, 0, z, args=(
        omega_M, omega_k, omega_rad, omega_Lambda, w, wa)))
    if omega_k < -1.e-15:  # closed universe
        r = DH / np.sqrt(abs(omega_k)) * \
            np.sin(np.sqrt(abs(omega_k))*freidman_integral)
    elif omega_k <= 1.e-15:  # flat universe
        r = DH*freidman_integral
    else:  # open universe
        r = DH / np.sqrt(omega_k) * \
            np.sinh(np.sqrt(omega_k)*freidman_integral)
    return r



def luminosity_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return comoving_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa) * (1+z)



def angular_diameter_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return comoving_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa) / (1+z)



def comoving_volume_element(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa, DH):
    Vc_elt = DH * \
        (angular_diameter_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w,
         wa)**2 * (1+z)**2 / _E(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa))
    return Vc_elt



def comoving_volume(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa, DH):
    r = comoving_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa)
    if omega_k < -1.e-15:  # closed universe
        Vc = ((4*np.pi*DH**3)/(2*omega_k))*(r/DH*np.sqrt(1+omega_k*(r/DH)**2)
                                            - 1/np.sqrt(abs(omega_k))*np.arcsin(np.sqrt(abs(omega_k))*r/DH))/(1e9)
    elif omega_k <= 1.e-15:  # flat universe
        Vc = 4/3*np.pi * r**3 / (1.e9)
    else:
        Vc = ((4*np.pi*DH**3)/(2*omega_k))*((r/DH)*np.sqrt(1+omega_k*(r/DH)**2)
                                            - 1/np.sqrt(abs(omega_k))*np.arcsinh(np.sqrt(abs(omega_k))*r/DH))/(1e9)
    return Vc



def distance_modulus(z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return 5 * np.log10(luminosity_distance(z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa) * 10**5)



def _calculate_age_universe(t_i, t_f, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return 1/H0*quad(_tage_int, a=t_i, b=t_f, args=(omega_M, omega_k, omega_rad, omega_Lambda, w, wa))*(mpc)/(seconds_in_a_year)/(1e9)


# lookback time, Gyr

def light_travel_time(z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return _calculate_age_universe(0, z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa)



def age_at_z(z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):  # age at z, Gyr
    return _calculate_age_universe(z, np.inf, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa)



def age_today(H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):  # age today, Gyr
    return _calculate_age_universe(0, np.inf, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa)
