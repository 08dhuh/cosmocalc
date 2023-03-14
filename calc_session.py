import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
from cosmocalc import *

st.set_page_config(layout='wide')
st.title('University of Melbourne Astrophysics Department Cosmology Calculator')


cosmo = None
cosmo_params = ['H0', 'w', 'wa', 'omega_rad', 'omega_M', 'omega_Lambda']
cosmology_model_keys = cosmology_model.keys()

cosmo_description = {key: f'desc {key}' for key in cosmology_model_keys}
cosmo_param_description = {key: f'desc {key}' for key in cosmo_params}


def num_formatter(num, decimal=4): return round(num, decimal)


def update_param(obj, param, value):
    if param in dir(obj) and not callable(getattr(obj, param)):
        setattr(obj, param, value)


# initialisation
if 'cosmo_param_holder' not in st.session_state:
    st.session_state['cosmo_params'] = cosmo_params
    for param in cosmo_params:
        st.session_state[param] = cosmology_model['concordance'][param]
    st.session_state['z'] = 1
    st.session_state['cosmo'] = Cosmocalc(
        *arg_parser(cosmo_params, st.session_state))


# st.write(st.session_state)

col1, _, col2 = st.columns([2, 1, 2])
with col1:
    st.subheader('----this section chooses cosmology parameters')
    option = st.selectbox(
        'What is your cosmology?',
        cosmology_model_keys)
    with st.expander('Explanation of each cosmology'):
        option_desc = st.selectbox(
            'cosmology type',
            cosmology_model_keys
        )
        st.markdown(cosmo_description[option_desc])
    # Input widgets

    for param in cosmo_params:
        st.session_state[param] = st.number_input(f'{param}',
                                                  value=float(
                                                      st.session_state[param]),
                                                  format='%.4f',
                                                  step=None,
                                                  help=cosmo_param_description[param],
                                                  # on_change=lambda value: update_param(st.session_state['cosmo'],param,value)
                                                  )
        update_param(st.session_state['cosmo'], param, st.session_state[param])
        # st.session_state.update({param: item})
    # st.number_input()
    if st.button('make cosmo'):
        try:
            for param in cosmo_params:
                setattr(st.session_state['cosmo'],
                        param, st.session_state[param])
            st.session_state['cosmo']._update_cosmo_params()
        except Exception as e:
            st.write(e)

    # Add form validation algorithm

if (cosmo):

    # cosmo_methods = [getattr(cosmo, d) for d in dir(cosmo) if callable(getattr(cosmo, d)) and not d.startswith('_')]
    result_list = [
        "age_at_z",
        "age_today",
        "angular_diameter_distance",
        "comoving_distance",
        "comoving_volume",
        "comoving_volume_element",
        "distance_modulus",
        "light_travel_time",
        "luminosity_distance"
    ]


with col2:  # Explanation for the cosmology
    st.session_state['z'] = st.number_input('z', value=st.session_state['z'])
    st.session_state['cosmo_methods'] = [d for d in dir(st.session_state['cosmo']) if callable(
        getattr(st.session_state['cosmo'], d)) and not d.startswith('_')]
    st.session_state['result'] = {cm: getattr(st.session_state['cosmo'], cm)(
        st.session_state['z']) for cm in st.session_state['cosmo_methods']}

    st.dataframe(st.session_state['result'])


z_range = st.slider('range of redshift', 0, 100, (0, 10))
