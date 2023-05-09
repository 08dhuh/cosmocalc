<h1>Requirements</h1>
<p>This app requires the following Python packages:</p>
<ul>
<li>streamlit</li>
<li>numpy</li>
<li>pandas</li>
<li>yaml</li>
<li>plotly.express</li>
<li>cosmocalc</li>
</ul>
To install these packages, please run the following command:

sh
Copy code
pip install streamlit numpy pandas yaml plotly.express cosmocalc
How to Run
To run the app, navigate to the directory containing the app.py file in your terminal and run the following command:

sh
Copy code
streamlit run app.py
Once the app is running, follow the on-screen instructions to input the necessary parameters and calculate the desired cosmological parameters.

Usage
The app consists of the following modules:

Input Parameters
Users can input the following parameters:

H0: Hubble constant in units of km/s/Mpc
Om0: Density parameter for matter
Ode0: Density parameter for dark energy
Ogamma0: Density parameter for gamma radiation
Onu0: Density parameter for neutrinos
TCMB: Cosmic Microwave Background temperature in Kelvin
z: Redshift value for which to calculate the cosmological parameters
Users can also choose from a list of predefined cosmological models by selecting the Cosmology Model dropdown. Once a model is selected, the input parameters will be updated to the values for that model.

Calculations
The following cosmological parameters can be calculated:

Age of the Universe: Age of the universe in years
Angular Diameter Distance: Angular diameter distance in Mpc
Luminosity Distance: Luminosity distance in Mpc
Comoving Volume: Comoving volume in Mpc^3
Comoving Distance: Comoving distance in Mpc
Hubble Parameter: Hubble parameter in km/s/Mpc
Lookback Time: Lookback time in Gyr
Critical Density: Critical density in units of the critical density at present
Density Parameter: Density parameter for matter, dark energy, gamma radiation, and neutrinos
Redshift: Calculates the redshift value at which the age of the universe is equal to the input value for Age of the Universe
Output
The app displays the calculated cosmological parameters in a table and a plot. The table shows the parameter values for the input redshift value and for redshift values spaced equally between 0 and the input redshift value. The plot shows the calculated parameter values as a function of redshift.
