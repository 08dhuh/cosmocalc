<h2>Requirements</h2>
<p>This app requires the following Python packages:</p>
<ul>
<li>streamlit</li>
<li>numpy</li>
<li>pandas</li>
<li>yaml</li>
<li>plotly.express</li>
<li>cosmocalc</li>
</ul>

<p>To install these packages, run the following command on the directory containing requirements.txt</p>:

```
pip install -r requirements.txt
```

<p>To run the app, naviate to the directory containing calc_session.py and run the following command</p>

```
streamlit run app.py
```

<p>Once the app is running, follow the on-screen instructions to input the necessary parameters and calculate the desired cosmological parameters.</p>

<h2>Usage</h2>
The app consists of the following modules:

<h3>Input Parameters</h3>
Users can input the parameters:

<ul>
H0: Hubble constant in units of km/s/Mpc
Om0: Density parameter for matter
Ode0: Density parameter for dark energy
Ogamma0: Density parameter for gamma radiation
Onu0: Density parameter for neutrinos
TCMB: Cosmic Microwave Background temperature in Kelvin
z: Redshift value for which to calculate the cosmological parameters
</ul>
<p>Users can also choose from a list of predefined cosmological models by selecting the Cosmology Model dropdown. Once a model is selected, the input parameters will be updated to the values for that model.</p>

<h3>Calculations</h3>
The following cosmological parameters can be calculated:
<ul>
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
</ul>

<h3>Output</h3>
<p>The app displays the calculated cosmological parameters in a table and a plot. The table shows the parameter values for the input redshift value and for redshift values spaced equally between 0 and the input redshift value. The plot shows the calculated parameter values as a function of redshift.</p>
