import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

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
def change_cosmo(option):
    for param in cosmology_model[option]:
        st.session_state[param] = cosmology_model[option][param]

col1, _, col2 = st.columns([2, 1, 2])
with col1:
    st.subheader('Choose a preset cosmology')
    option = st.selectbox(
        'What is your cosmology?',
        cosmology_model_keys,
        on_change=change_cosmo)
    with st.expander('Explanation of each cosmology'):
        st.write('You can also access an exhaustive list of flat and non-flat cosmologies <a href="http://lambda.gsfc.nasa.gov/product/map/dr5/parameters.cfm">here</a>'
                 , unsafe_allow_html=True)
        option_desc = st.selectbox(
            'cosmology type',
            cosmology_model_keys
        )
        st.markdown(cosmo_description[option_desc])
    # Input widgets
    st.subheader('Or enter your own cosmology')
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
    # if st.button('make cosmo'):
    #     try:
    #         for param in cosmo_params:
    #             setattr(st.session_state['cosmo'],
    #                     param, st.session_state[param])
    #         st.session_state['cosmo']._update_cosmo_params()
    #     except Exception as e:
    #         st.write(e)

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
    
    #_-------------------plots--------------------
    z_range = st.slider('range of redshift', 0, 100, (0, 10))
    zs = np.linspace(z_range[0], z_range[1],100)[1:]

    titles = [cm for cm in st.session_state['cosmo_methods'] if cm!='age_today']
    for cm in titles:
        func = getattr(st.session_state['cosmo'], cm)
        res = [func(z) for z in zs]    
        df = pd.DataFrame(np.column_stack((zs,res)), columns=['redshift', cm])
        fig = px.line(df, x='redshift', y=cm, title=f'{cm} at redshift z')
        st.plotly_chart(fig, use_container_width=True)

#st.write(z_range[0],z_range[1])

# st.write(st.session_state['cosmo_methods'])
# s1 = getattr(st.session_state['cosmo'],st.session_state['cosmo_methods'][0])
# ys = [s1(z) for z in zs]
# #st.line_chart(np.column_stack((zs,ys)))
# df = pd.DataFrame(np.column_stack((zs,ys)),columns=['redshift','age at z'])
# fig = px.line(df, x='redshift', y='age at z', title='Age of the Universe at Redshift z')
# st.plotly_chart(fig,use_container_width=True)
#data = np.column_stack([zs,s1(zs)])
#st.line_chart(data)