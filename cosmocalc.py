import numpy as np
import math
from scipy.integrate import quad
from astropy import constants as const
from functools import cached_property

# -------------------------------constants
c = const.c.to('km/s').value
mpc = const.kpc.value
seconds_in_a_year = 31557600  # julian
# c = 2.99792458e5   # in units of km
# Mpc2km = 3.08567758147e+19     # converts Mpc to km


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
        E(z):
            Calculates the value of the E(z) function at the given redshift z.
            Parameters:
                z : float
                    Redshift.
            Returns:
                float : The value of E(z). 

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
                float : The comoving volume element in Mpc^3.

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

        calculate_age_universe(t_i, t_f):
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

    def __init__(self, H0, w, wa, omega_rad, omega_M, omega_Lambda):
        # if z < 0:
        #     raise ValueError
        # add error handling method
        self._H0 = H0
        self._w = w
        self._wa = wa
        self._omega_rad = omega_rad
        self._omega_M = omega_M
        self._omega_Lambda = omega_Lambda
        # self._z = z
        self._DH = c/H0
        self._omega_k = 1 - omega_M - omega_Lambda - omega_rad  # curvature
        self._update_cosmo_params()

    def _update_cosmo_params(self):
        self._omega_k = 1 - self.omega_M - self.omega_Lambda - self.omega_rad  # curvature
        self._cosmo_params = {
            'H0': self.H0,
            'DH': self._DH,
            'w': self.w,
            'wa': self.wa,
            'omega_rad': self.omega_rad,
            'omega_M': self.omega_M,
            'omega_Lambda': self.omega_Lambda,
            'omega_k': self.omega_k,
            # 'z': self.z
        }

    @property
    def cosmo_params(self):
        return self.__dict__

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

    # @property
    # def z(self):
    #     return self._z

    # @z.setter
    # def z(self, value):
    #     self._z = value if value >= 0 else self._z
    #     self._update_cosmo_params()

    @cached_property
    def E(self, z):
        return np.sqrt(self.omega_M*(1+z)**3 + self.omega_k*(1+z)**2 + self.omega_rad*(1+z)**4
                       + self.omega_Lambda*(1+z)**(3*(1+self.w+self.wa))*math.exp(-3*self.wa*(1-1/(1+z))))

    @cached_property
    def freidman(self, z):
        return 1/self.E(z)

    @cached_property
    def tage_int(self, z):
        return 1/((1+z)*self.E(z))

    @cached_property
    def tage_int(self, z):
        return 1/((1+z)*self.E(z))

    @cached_property
    def comoving_distance(self, z):
        freidman_integral = float(quad(self.freidman, 0, z, args=(
            self.omega_M, self.omega_k, self.omega_rad, self.omega_Lambda, self.w, self.wa)))
        if self.omega_k < -1.e-15:  # closed universe
            r = self.DH / np.sqrt(abs(self.omega_k)) * \
                np.sin(np.sqrt(abs(self.omega_k))*freidman_integral)
        elif self.omega_k <= 1.e-15:  # flat universe
            r = self.DH*freidman_integral
        else:  # open universe
            r = self.DH / np.sqrt(self.omega_k) * \
                np.sinh(np.sqrt(self.omega_k)*freidman_integral)
        return r

    @cached_property
    def luminosity_distance(self, z):
        return self.comoving_distance(z) * (1+z)

    @cached_property
    def angular_diameter_distance(self, z):
        return self.comoving_distance(z) / (1+z)

    @cached_property
    def comoving_volume_element(self, z):
        Vc_elt = self.DH * \
            (self.angular_diameter_distance(z)**2 * (1+z)**2 / self.E(z))
        return Vc_elt

    @cached_property
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

    @cached_property
    def distance_modulus(self, z):
        return 5 * np.log10(self.luminosity_distance(z) * 10**5)

    @cached_property
    def calculate_age_universe(self, t_i, t_f):
        return 1/self.H0*quad(tage_int, [t_i, t_f], args=(self.omega_M, self.omega_k, self.omega_rad, self.omega_Lambda, self.w, self.wa))*(mpc)/(seconds_in_a_year)/(1e9)

    @cached_property
    def light_travel_time(self, z):
        return self.calculate_age_universe(0, z)

    @cached_property
    def age_at_z(self, z):
        return self.calculate_age_universe(z, np.inf)

    @cached_property
    def age_today(self):
        return self.calculate_age_universe(0, np.inf)


@cached_property
def E(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return np.sqrt(omega_M*(1+z)**3 + omega_k*(1+z)**2 + omega_rad*(1+z)**4
                   + omega_Lambda*(1+z)**(3*(1+w+wa))*math.exp(-3*wa*(1-1/(1+z))))


@cached_property
def freidman(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return 1/E(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa)


@cached_property
def tage_int(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return 1/((1+z)*E(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa))


@cached_property
def comoving_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa, DH):
    freidman_integral = float(quad(freidman, 0, z, args=(
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


@cached_property
def luminosity_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return comoving_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa) * (1+z)


@cached_property
def angular_diameter_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return comoving_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa) / (1+z)


@cached_property
def comoving_volume_element(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa, DH):
    Vc_elt = DH * \
        (angular_diameter_distance(z, omega_M, omega_k, omega_rad, omega_Lambda, w,
         wa)**2 * (1+z)**2 / E(z, omega_M, omega_k, omega_rad, omega_Lambda, w, wa))
    return Vc_elt


@cached_property
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


@cached_property
def distance_modulus(z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return 5 * np.log10(luminosity_distance(z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa) * 10**5)


@cached_property
def calculate_age_universe(t_i, t_f, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return 1/H0*quad(tage_int, [t_i, t_f], args=(omega_M, omega_k, omega_rad, omega_Lambda, w, wa))*(mpc)/(seconds_in_a_year)/(1e9)


@cached_property
# lookback time, Gyr
def light_travel_time(z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):
    return calculate_age_universe(0, z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa)


@cached_property
def age_at_z(z, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):  # age at z, Gyr
    return calculate_age_universe(z, np.inf, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa)


@cached_property
def age_today(H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa):  # age today, Gyr
    return calculate_age_universe(0, np.inf, H0, omega_M, omega_k, omega_rad, omega_Lambda, w, wa)
