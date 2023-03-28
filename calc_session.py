import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import cosmocalc
from cosmocalc import *
import yaml


# ---- configuration --------------------------------
st.set_page_config(layout='wide')

# ---------------------parameters-------------------------------------------
with open('cosmo_params.yaml','r') as file:
    params = yaml.safe_load(file)

cosmology_model = {
    "concordance": {"H0": 70.0, "w": -1, "wa": 0, "omega_rad": 0, "omega_M": 0.3, "omega_Lambda": 0.7},
    "wmap7": {"H0": 70.2, "w": -1, "wa": 0, "omega_rad": 0, "omega_M": 0.272, "omega_Lambda": 0.728},
    "planck": {"H0": 67.3, "w": -1, "wa": 0, "omega_rad": 0, "omega_M": 0.315, "omega_Lambda": 0.685},
    "flatempty": {"H0": 70.0, "w": -1, "wa": 0, "omega_rad": 0, "omega_M": 0.0, "omega_Lambda": 1.0},
    "einsteindesitter": {"H0": 70.0, "w": -1, "wa": 0, "omega_rad": 0, "omega_M": 1.0, "omega_Lambda": 0.0}
}
cosmo_input_params = ['H0', 'w', 'wa', 'omega_rad', 'omega_M', 'omega_Lambda']
cosmology_model_keys = list(cosmology_model.keys())

cosmo_input_params_mask = {
    "H0": "H\u2080",
    "w": "w",
    "wa": "w\u2090",
    "omega_rad": "\u03A9\u209A",
    "omega_M": "\u03A9\u2098",
    "omega_Lambda": "\u03A9\u209B"
}
# to be updated------------- description # { key: f'desc {key}' for key in cosmology_model_keys}  # to be updated

cosmo_description= {
    
}
""""concordance": contains cosmological parameters from the concordance model, which assumes a flat universe with a constant dark energy density and a matter density dominated by cold dark matter.
"wmap7": contains cosmological parameters from the WMAP7 mission, which measured the cosmic microwave background radiation.
"planck": contains cosmological parameters from the Planck mission, which also measured the cosmic microwave background radiation.
"flatempty": contains cosmological parameters for a flat universe with no matter, only a cosmological constant (vacuum energy).
"einsteindesitter": contains cosmological parameters for the Einstein-de Sitter model, which assumes a universe filled with only matter and no dark energy."""

cosmo_param_description = {
    'H0': 'Hubble constant in km/s/Mpc',
    'w': 'This is the expansion term. In standard cosmologies it is equal to \u03A9=\u03A9\u2080=-1',
    'wa': 'This term allows you to let the expansion term evolve with redshift as \u03A9_CPL = \u03A9\u2080+\u03A9\u2090(z/1+z). This is the Chevalier-Polarski-Linder (CPL)',
    'omega_rad': 'This is the radiation density term. In standard cosmologies, radiation is only dominant at very high redshifts.',
    'omega_M': 'This is the matter density term.',
    'omega_Lambda': 'This is the dark energy density term.'
}
#cosmo_param_description = {key: f'desc {key}' for key in cosmo_input_params}

input_param_dict = {
    "H0": {"mask": "H\u2080", "description": "Hubble constant in km/s/Mpc"},
    "w": {"mask": "w", "description": "This is the expansion term. In standard cosmologies it is equal to \u03A9=\u03A9\u2080=-1"},
    "wa": {"mask": "w\u2090", "description": "This term allows you to let the expansion term evolve with redshift as \u03A9_CPL = \u03A9\u2080+\u03A9\u2090(z/1+z). This is the Chevalier-Polarski-Linder (CPL)"},
    "omega_rad": {"mask": "\u03A9\u209A", "description": "This is the radiation density term. In standard cosmologies, radiation is only dominant at very high redshifts."},
    "omega_M": {"mask": "\u03A9\u2098", "description": "This is the matter density term."},
    "omega_Lambda": {"mask": "\u03A9\u209B", "description": "This is the dark energy density term."}
}
# -------------------

result = ["age_at_z",
          "age_today",
          "angular_diameter_distance",
          "comoving_distance",
          "comoving_volume",
          "comoving_volume_element",
          "distance_modulus",
          "light_travel_time",
          "luminosity_distance"]
result_list = [  # masking names for cosmo_methods
    "Age at Z",
    "Age Today",
    "Angular Diameter Distance",
    "Comoving Distance",
    "Comoving Volume",
    "Comoving Volume Element",
    "Distance Modulus",
    "Light Travel Time",
    "Luminosity Distance"
]
unit_list = [
    r"Gyr",             # Age at Z
    r"Gyr",             # Age Today
    r"Mpc",             # Angular Diameter Distance
    r"Mpc",             # Comoving Distance
    r"Mpc$^3$",         # Comoving Volume
    r"Mpc$^3$",         # Comoving Volume Element
    r"mag",             # Distance Modulus
    r"Gyr",             # Light Travel Time
    r"Mpc"              # Luminosity Distance
]

result_dict = {}
for i, r in enumerate(result):
    result_dict[r] = {"name": result_list[i], "unit": unit_list[i]}


def arg_parser(arg: list, dict: dict):
    lst = [dict[i] for i in arg if i in dict]
    return lst if len(lst) == len(arg) else ValueError


def num_formatter(num: float, decimal=2): return round(num, decimal)


def update_cosmo_param(obj: Cosmocalc, param, value):
    if param in dir(obj) and not callable(getattr(obj, param)):
        setattr(obj, param, value)


def update_cosmo_params(obj: Cosmocalc, *args, **kwargs):
    if len(args) == len(cosmo_input_params):
        for key, value in zip(cosmo_input_params, args):
            setattr(obj, key, value)
    elif all(key in cosmo_input_params for key in kwargs):
        for key in kwargs:
            setattr(obj, key, kwargs[key])
    else:
        raise ValueError(
            'The number of arguments/ keyword arguments are not supported')


def change_cosmo(option):
    for param in cosmology_model[option]:
        st.session_state[param] = cosmology_model[option][param]


# ---------------- initialisation--------------------------------

if 'c' not in st.session_state:
    if 'cosmology_model' not in st.session_state:
        st.session_state['cosmology_model'] = 'concordance'
    change_cosmo(st.session_state['cosmology_model'])
    st.session_state['cosmo'] = Cosmocalc(
        *arg_parser(cosmo_input_params, st.session_state))
    st.session_state['z'] = [1.0]
    st.session_state['cosmo_methods'] = ["age_at_z",
                                         "age_today",
                                         "angular_diameter_distance",
                                         "comoving_distance",
                                         "comoving_volume",
                                         "comoving_volume_element",
                                         "distance_modulus",
                                         "light_travel_time",
                                         "luminosity_distance"]

    # update_cosmo_params(*arg_parser(cosmo_input_params, st.session_state))
    # [d for d in dir(st.session_state['cosmo']) if callable(
    #     getattr(st.session_state['cosmo'], d)) and not d.startswith('_')]

# ---------------------------------contents--------------------------------

st.title('University of Melbourne Astrophysics Department Cosmology Calculator')

#st.help(cosmocalc)

# -------------------preset cosmology--------------------
st.subheader('Choose a preset cosmology')
with st.expander('Explanation of each cosmology'):
    option_desc = st.selectbox(
        'cosmology type',
        cosmology_model_keys
    )
    st.markdown(cosmo_description[option_desc])
    st.write("""You can also access an exhaustive list of flat and non-flat cosmologies 
                 [here](http://lambda.gsfc.nasa.gov/product/map/dr5/parameters.cfm)""")

columnbuttons = st.columns([1 for i in range(len(cosmology_model))])
for i in range(len(cosmology_model)):
    with columnbuttons[i]:
        if st.button(f'{cosmology_model_keys[i]}',
                     help=cosmo_description[cosmology_model_keys[i]],
                     # disabled=True
                     ):
            st.session_state['cosmology_model'] = cosmology_model_keys[i]
            change_cosmo(cosmology_model_keys[i])
            update_cosmo_params(
                st.session_state['cosmo'], *arg_parser(cosmo_input_params, st.session_state))


col1, _, col2 = st.columns([2, 0.2, 4])


with col1: #accept multiple zs
    # ------------------------------------- Input widgets
    for param in cosmo_input_params:
        st.session_state[param] = st.number_input(f'{param}',
                                                  value=float(
                                                      st.session_state[param]),
                                                  format='%.4f',
                                                  step=None,
                                                  help=cosmo_param_description[param],
                                                  )
        update_cosmo_param(
            st.session_state['cosmo'], param, st.session_state[param])
    st.number_input('omega_k', value=st.session_state['cosmo'].omega_k,
                    format='%.4f', disabled=True, help='curvature')
    st.session_state['z'] = st.number_input(
        'z', value=st.session_state['z'][0], format='%.4f', min_value=0.0, help='redshift')


@st.cache_data(experimental_allow_widgets=True, max_entries=1000)
def get_zs(max_z: int = 100, num_points: int = 100):
    """
    Returns an array of redshift values between the given range.

    Args:
        max_z (int): The maximum value of the redshift range.
        num_points (int): The number of points to generate between the given range.

    Returns:
        np.ndarray: An array of redshift values between the given range.
    """
    z_range = st.slider('range of redshift', 0, max_z, (0, 10))
    if z_range[0] == z_range[1]:
        st.error('min and max values must be different')
        return None
    zs = np.linspace(z_range[0], z_range[1], num_points)
    if zs[0] == 0:  # redshift should be greater than zero
        zs = np.append(zs[1:], zs[-1]+np.diff(zs)[0])
    return zs


@st.cache_data
def calculate_cosmo_attribute(_func_name: str, z=st.session_state['z']):
    """
    Calculates the cosmological attribute specified by `_func_name` for redshift values `z`.

    Parameters:
    -----------
    _func_name: str
        The name of the cosmological attribute function to be calculated.
    z: np.ndarray or float
        The redshift values for which to calculate the cosmological attribute. Default value is `st.session_state['z']`.

    Returns:
    --------
    np.ndarray or float
        The calculated cosmological attribute values for the input redshift values.
    """
    try:
        cm = np.vectorize(getattr(st.session_state['cosmo'], _func_name))
        return cm(z)
    except Exception as e:
        st.error(e)


@st.cache_data
def calculate_cosmo_attributes_z(z):
    df = pd.DataFrame()
    columns=[]
    
    pass

def plot_cosmo_attributes(z):
    pass

with col2:  # -----------------------calculation results
    tab1, tab2 = st.tabs(['Results', 'Plots'])
    with tab1:
        st.session_state['result'] = {cm: getattr(st.session_state['cosmo'], cm)(
            st.session_state['z']) for cm in st.session_state['cosmo_methods']}
        st.dataframe(st.session_state['result'])

    with tab2:
        # _-------------------plots--------------------
        # z_range = st.slider('range of redshift', 0, 100, (0, 10))
        # zs = np.linspace(z_range[0], z_range[1], 100)[1:]
        zs = get_zs()

        titles = [cm for cm in st.session_state['cosmo_methods']
                  if cm != 'age_today']
        for cm in titles:
            func = getattr(st.session_state['cosmo'], cm)
            res = [func(z) for z in zs]
            df = pd.DataFrame(np.column_stack((zs, res)),
                              columns=['redshift', cm])
            fig = px.line(df,
                          x='redshift',
                          y=cm,
                          title=f'{cm} at redshift z',
                          log_x=True  # logscale
                          )
            st.plotly_chart(fig, use_container_width=True)
