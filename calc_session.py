import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import cosmocalc
from cosmocalc import *

# ---- configuration --------------------------------
st.set_page_config(layout='wide')

# ---------------------parameters-------------------------------------------

cosmo_input_params = ['H0', 'w', 'wa', 'omega_rad', 'omega_M', 'omega_Lambda']
cosmology_model_keys = list(cosmology_model.keys())

# to be updated------------- description
cosmo_description = {
    key: f'desc {key}' for key in cosmology_model_keys}  # to be updated
cosmo_param_description = {key: f'desc {key}' for key in cosmo_input_params}
# -------------------
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


# def update_cosmo_state()


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
    st.session_state['z'] = 1.0
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


    

with col1:
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
        'z', value=st.session_state['z'], format='%.4f', min_value=0.0, help='redshift')


@st.cache_data(experimental_allow_widgets=True, max_entries=1000)
def get_zs(max_z:int = 100, num_points:int = 100):
    z_range = st.slider('range of redshift', 0, max_z, (0, 10))
    if z_range[0] == z_range[1]:
        st.error('min and max values must be different')
        return None
    zs = np.linspace(z_range[0], z_range[1], num_points)
    if zs[0] == 0: #redshift should be greater than zero
        zs = np.append(zs[1:], zs[-1]+np.diff(zs)[0])
    return zs

@st.cache_data
def calculate_cosmo_attribute(_func_name:str, z:float=st.session_state['z']):
    try:
        cm = getattr(st.session_state['cosmo'], _func_name)
        return cm(z)
    except Exception as e:
        st.error(e)
        

@st.cache_data
def compute_cosmo_attributes():
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
