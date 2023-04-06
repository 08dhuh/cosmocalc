import streamlit as st
import numpy as np
import pandas as pd
import yaml
import plotly.express as px
from cosmocalc import cosmo_input_params, Cosmocalc


# ---- configuration --------------------------------
st.set_page_config(layout='wide')

# ---------------------load parameters-------------------------------------------
with open('cosmo_params.yaml', 'r', encoding='utf-8') as file:
    params = yaml.safe_load(file)

cosmology_model_dict = params['model_dict']
input_param_dict = params['input_param_dict']
result_dict = params['result_dict']

# ----------------------utilities------------------------------------


def arg_parser(arg: list, session_state: dict):
    """
    This function takes a list of arguments 'arg' and a dictionary 'dict' and returns
    a list of values in the dictionary corresponding to the arguments in 'arg'.
    If an argument in 'arg' is not present in 'dict', it raises a ValueError.

    Args:
    - arg (list): List of arguments
    - dict (dict): Dictionary containing the arguments as keys and their values

    Returns:
    - list: List of values in the dictionary corresponding to the arguments in 'arg'

    Raises:
    - ValueError: If an argument in 'arg' is not present in 'dict'
    """
    lst = [session_state[i] for i in arg if i in session_state]
    return lst if len(lst) == len(arg) else ValueError


def num_formatter(num: float or np.ndarray, decimal=2):
    """
    This function formats a given float 'num' to a specific number of decimal places.

    Args:
    - num (float): The float number to format
    - decimal (int): Number of decimal places to round to (default: 2)

    Returns:
    - float: Formatted number with the specified number of decimal places
    """
    try:
        if type(num) is float:
            return round(num, decimal)
        if type(num) is np.ndarray:
            return np.around(num, decimal)
        else:
            raise TypeError
    except TypeError as e:
        return st.error(e)


def update_cosmo_param(obj: Cosmocalc, param, value):
    """
    This function updates a parameter 'param' of an object 'obj' with the given 'value'.

    Args:
    - obj (Cosmocalc): Object whose parameter needs to be updated
    - param (str): Name of the parameter to update
    - value (Any): Value to be assigned to the parameter

    Returns:
    - None
    """
    if param in dir(obj) and not callable(getattr(obj, param)):
        setattr(obj, param, value)


def update_cosmo_params(obj: Cosmocalc, *args, **kwargs):
    """
    This function updates multiple parameters of an object 'obj' using positional and/or
    keyword arguments. The number and order of positional arguments must match the
    parameters defined in 'cosmo_input_params' (a list of parameter names).
    Alternatively, keyword arguments can be used, where the argument name matches a
    parameter name.

    Args:
    - obj (Cosmocalc): Object whose parameters need to be updated
    - *args (Any): Positional arguments representing values of parameters
    - **kwargs (Any): Keyword arguments representing values of parameters

    Returns:
    - None

    Raises:
    - ValueError: If the number of positional/keyword arguments do not match the
                  parameters defined in 'cosmo_input_params'
    """
    if len(args) == len(cosmo_input_params):
        for key, value in zip(cosmo_input_params, args):
            setattr(obj, key, value)
    elif all(key in cosmo_input_params for key in kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
    else:
        raise ValueError(
            'The number of arguments/ keyword arguments are not supported')


def change_cosmo(option: str):
    """
    This function updates the values of specific parameters in the current session
    state based on the selected 'option' (a string representing a cosmology model).

    Args:
    - option (str): The selected cosmology model option

    Returns:
    - None
    """
    for param in cosmology_model_dict[option]['param']:
        st.session_state[param] = cosmology_model_dict[option]['param'][param]


def clear_result_chart(cond:bool=True):
    """
    initialises the result chart
    """
    if 'result' not in st.session_state or cond: 
        st.session_state['result'] = None

# -----------------------Output --------------------------------


def calculate_cosmo_attribute(_func_name: str, z, rounding=True):
    """
    Calculates the cosmological attribute specified by `_func_name` for redshift values `z`.

    Parameters:
    -----------
    _func_name: str
        The name of the cosmological attribute function to be calculated.
    z: np.ndarray or float
        The redshift values for which to calculate the cosmological attribute. 
        Default value is `st.session_state['z']`.

    Returns:
    --------
    np.ndarray or float
        The calculated cosmological attribute values for the input redshift values.
    """
    try:
        cm = np.vectorize(getattr(st.session_state['cosmo'], _func_name))
        return num_formatter(cm(z))
    except AttributeError as e:
        return st.error(e)


# @st.cache_data
# for the result of the calculation
def calculate_cosmo_attributes_z(z, df=None):
    """
    This function calculates the values of various cosmological parameters \
        at a given redshift value 'z'.

    Parameters:
    z (float): 
    df (pandas.DataFrame, optional): A pandas dataframe.
                                      If not provided, a new dataframe will be created.

    Returns:
    pandas.DataFrame: A pandas dataframe.                      
    """
    try:
        attributes = [result_dict[c]['mask'] for c in result_dict]
        values = [
            f'{calculate_cosmo_attribute(c,z)} {result_dict[c]["unit"]}' for c in result_dict]
        if df is None:
            df = pd.DataFrame({f'Values at {num_formatter(z)}': values}, index=attributes)
        else:
            df[f'Values at {num_formatter(z)}'] = values
        return df
    except Exception as e:
        st.error(e)


@st.cache_data(experimental_allow_widgets=True, max_entries=1000)
def get_zs(z_range,num_points: int = 100, diverging_value=5, offset=1e-1):
    """
    Returns an array of redshift values between the given range.
    If the redshift range is greater than 5, np.logspace is used instead of np.linspace

    Args:
        z_range(tuple): The redshift range.
        num_points (int): The number of points to generate between the given range.

    Returns:
        np.ndarray: An array of redshift values between the given range.
    """    
    try:
        z_min, z_max = z_range
        if abs(z_max-z_min) <= diverging_value:
            zs = np.linspace(z_min, z_max, num_points)
            if zs[0] == 0:  # redshift should be greater than zero
                zs = np.append(zs[1:], zs[-1]+np.diff(zs)[0])            
        else:            
            if z_min <=0:
                z_min += offset    
            zs = np.geomspace(z_min, z_max, num_points)       
        return zs
    except TypeError as e:
        if z_range[0] == z_range[1]:
            st.error('min and max values must be different')
        st.error(e)    


# @st.cache_data


def plot_cosmo_attribute(funcname: str, z: np.ndarray, result_dict: dict = result_dict):
    """
    Plot the variation of a given cosmological attribute with redshift.

    Args:
    - funcname (str): Name of the cosmological attribute to be plotted.
    - z (numpy.ndarray): Redshift values.
    - **kwargs: Keyword arguments to be passed to the plot.

    Returns:
    - fig (plotly.graph_objs._figure.Figure): A plotly figure object.
    """
    values = calculate_cosmo_attribute(funcname, z)
    df = pd.DataFrame(np.column_stack((z, values)),
                      columns=['redshift', funcname])
    fig = px.line(df,
                  x='redshift',
                  y=funcname,
                  title=f'{result_dict[funcname]["mask"]} ({result_dict[funcname]["unit"]})',
                  labels={
                      funcname: f'{result_dict[funcname]["mask"]} ({result_dict[funcname]["unit"]})',
                      'redshift': 'redshift z'},
                  log_x=True,
                  template='plotly_white',
                  )
    fig.update_xaxes(exponentformat='power')
    fig.update_yaxes(exponentformat='power')
    return fig
# ---------------------flow---------------------
# ---------------- initialisation--------------------------------


def initialize_session_data():
    """
    Initializes the session data for the Streamlit app.

    If the 'c' key is not present in the session state, it initializes the following keys:
    - 'cosmology_model': The default cosmology model ('concordance')
    - 'cosmo': An instance of the Cosmocalc class initialized with the cosmology input parameters
              retrieved from the session state dictionary using the 'arg_parser' function
    - 'z': The redshift value set to 1.0

    Returns:
    None
    """
    if 'c' not in st.session_state:
        if 'cosmology_model' not in st.session_state:
            st.session_state['cosmology_model'] = 'concordance'
        change_cosmo(st.session_state['cosmology_model'])
        st.session_state['cosmo'] = Cosmocalc(
            *arg_parser(cosmo_input_params, st.session_state))
        st.session_state['z'] = 1.0
        #st.session_state['max_z']=100        
        clear_result_chart(False)

# -------------------preset cosmology--------------------


def display_cosmology_section():
    """
    Displays the preset cosmology options and their explanations. 
    Allows the user to choose a cosmology model from the \
        available options.

    Returns:
        None
    """
    st.subheader('Choose a preset cosmology')
    # with st.expander('Explanation of each cosmology'):
    #     option_desc = st.selectbox(
    #         'cosmology type',
    #         list(cosmology_model_dict)
    #     )
    #     st.markdown(cosmology_model_dict[option_desc]['description'])
    #

    # columnbuttons = st.columns([1 for i in range(len(cosmology_model_dict))])
    st.write("""You can also access an exhaustive list of flat and non-flat cosmologies \
                    [here](http://lambda.gsfc.nasa.gov/product/map/dr5/parameters.cfm)""")
    columnbuttons = st.columns(len(cosmology_model_dict))
    for i, r in enumerate(cosmology_model_dict):
        with columnbuttons[i]:
            if st.button(f'{r}',
                         help=cosmology_model_dict[r]['description'],
                         # disabled=True
                         ):
                st.session_state['cosmology_model'] = r
                change_cosmo(r)
                update_cosmo_params(
                    st.session_state['cosmo'], *arg_parser(cosmo_input_params, st.session_state))

# ------------------------------------- Input widgets------------------
# trying sidebar approach


def display_input_control():
    """
    Displays the input controls for the cosmological parameters in the sidebar.

    For each parameter in the input_param_dict, a number input control is shown in the sidebar
    with a label, a default value, and minimum and maximum values (if applicable).
    The current value of the parameter is set in the session state.
    If the parameter is included in cosmo_input_params, the corresponding parameter
    value in the cosmology calculator object is updated with the new value.

    Returns:
        None
    """
    st.sidebar.header('Adjust the input parameters below')
    for param in input_param_dict:
        min_val = float(input_param_dict[param]['min'])
        max_val = float(input_param_dict[param]['max'])
        st.session_state[param] = st.sidebar.number_input(f'{input_param_dict[param]["mask"]}',
                                                          value=float(
                                                              st.session_state[param]) if param in st.session_state
                                                          else st.session_state['cosmo'].omega_k,
                                                          format='%.4f',
                                                          step=None,
                                                          disabled=(
                                                              param == 'omega_k'),
                                                          min_value=min_val,
                                                          max_value=max_val,
                                                          help=input_param_dict[param]['description'],
                                                          on_change=(lambda param=param: clear_result_chart() \
                                                                     if param!='z' else None) ,
                                                          #args=(param,)
                                                          )
        if param in cosmo_input_params:
            update_cosmo_param(
                st.session_state['cosmo'], param, st.session_state[param])


def display_results():
    """
    Displays the results of the cosmological calculation as a Pandas dataframe.
    """
    st.caption("""By default, when a cosmological input parameter other than z changes,\
                    the result table will be refreshed""")
        
    # if 'result' not in st.session_state or st.button('Clear'):
    #     st.session_state['result'] = None
    st.session_state['result'] = calculate_cosmo_attributes_z(
        st.session_state['z'], st.session_state['result'])
    st.dataframe(st.session_state['result'])
    if st.button('Clear Table'):
        clear_result_chart()
        #st.session_state['result'] = None
        st.experimental_rerun()


def display_cosmo_plots():
    """
    Display cosmology plots for various attributes.
    """
    c1,c2 = st.columns([1,2])
    with c1:        
        st.number_input('Adjust the maximum range of z (min=5)', value=100, min_value=5, key='max_z')
    with c2:
        z_range = st.slider('range of redshift', 0, st.session_state['max_z'], (0, 5), )
    
    zs = get_zs(z_range)
    col1, _, col2 = st.columns([2, 0.2, 2])
    for i, att in enumerate(result_dict):
        if att == 'age_today':
            continue
        fig = plot_cosmo_attribute(att, zs)
        # if 'time' in att or 'age' in att:
        if i % 2 == 0:
            with col1:
                st.plotly_chart(fig, use_container_width=True)
        else:
            with col2:
                st.plotly_chart(fig, use_container_width=True)


def main():
    """
    main program for the University of Melbourne Astrophysics Department Cosmology Calculator.
    """
    st.title('University of Melbourne Astrophysics Department Cosmology Calculator')
    # ------------initialisation------------------------
    initialize_session_data()
    # -------------input------------------------
    display_cosmology_section()
    display_input_control()
    # ------------output------------------------
    tab1, tab2 = st.tabs(['Results', 'Plots'])
    with tab1:
        display_results()
    with tab2:
        display_cosmo_plots()

    st.markdown('')
    st.caption('(1) M. Chevallier and D. Polarski, Int. J. Mod. Phys. D 10, 213 (2001),\
        \n(2) E.V. Linder, Phys. Rev. Lett. 90, 091301 (2003) \
            \nContributors: Doran Huh, 2023 \
            \nRobert L. Barone-Nugent, \
            Catherine O. de Burgh-Day and Jaehong Park, 2014\
                ')
    st.caption(
        'For reporting errors and suggestions, please contact huhd@unimelb.edu.au or r.webster@unimelb.edu.au')


if __name__ == '__main__':
    main()
