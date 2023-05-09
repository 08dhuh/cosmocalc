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

<p>To install these packages, run the following command on the directory containing requirements.txt</p>

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
<li>H0: Hubble constant in units of km/s/Mpc</li>
<li>w: expansion term</li>
<li>wa: this term allows you to let the expansion term evolve with redshift</li>
<li>omega_lambda: dark energy density</li>
<li>omega_M: matter density</li>
<li>omega_rad: radiation density</li>
<li>omega_k: Spatial curvature of the universe</li>
<li>z: Redshift value for which to calculate the cosmological parameters</li>
</ul>

<p>Users can also choose from a list of predefined cosmological models by selecting the Cosmology Model dropdown. Once a model is selected, the input parameters will be updated to the values for that model.</p>

<h3>Output</h3>
<p>The app displays the calculated cosmological parameters in a table and a plot. The table shows the parameter values for the input redshift value. The plot shows the calculated parameter values as a function of redshift.</p>

<h4>Results</h4>
The following cosmological parameters can be calculated:
<ul>
<li>Age of the Universe: Age of the universe in Gyr</li>
<li>Angular Diameter Distance: Angular diameter distance in Mpc</li>
<li>Luminosity Distance: Luminosity distance in Mpc</li>
<li>Comoving Volume: Comoving volume in Mpc^3</li>
<li>Comoving Distance: Comoving distance in Mpc</li>
<li>Distance Modulus: Difference between the apparent and absolute magnitude(unitless)</li>
<li>Light Travel Time: Lookback time in Gyr</li>
<li>Age Today: Age at z=0 in Gyr</li>
</ul>


