<?php
session_start();
?>
<html>
<title>University of Melbourne Astrophysics Department Cosmology Calculator</title>
<script>
    function checkForm() {
        var r = true;
        var H0 = document.forms["cosmocalcform"]["H0"].value;
        var oL = document.forms["cosmocalcform"]["oL"].value;
        var oM = document.forms["cosmocalcform"]["oM"].value;
        var oR = document.forms["cosmocalcform"]["oR"].value;
        var w = document.forms["cosmocalcform"]["w"].value;
        var wa = document.forms["cosmocalcform"]["wa"].value;
        var z = document.forms["cosmocalcform"]["z"].value;
        var regex_z = /(^[,])|(([^\d,.\s])+)|(\d+(\.[\d ]+)(\.[\d ]+)+)|([^\d. ][,]+)|([^\d][.]+[^\d])|([, ]$)/g;
        var regex_cosm = /(^[, ])|(([^\d.\t])+)|(\d+(\.\d+)(\.\d+)+)|([^\d.][,]+)|([^\d][.]+[^\d])|([, ]$)/g;
        var regex_w = /(^[, ])|(([^\d.\t\-])+)|(\d+(\.\d+)(\.\d+)+)|([^\d.\-][,]+)|([^\d\-][.]+[^\d\-])|([, ]$)/g;
        var z_t = regex_z.test(z);
        var oM_t = regex_cosm.test(oM);
        var oL_t = regex_cosm.test(oL);
        var oR_t = regex_cosm.test(oR);
        var H0_t = regex_cosm.test(H0);
        var w_t = regex_w.test(w);
        var wa_t = regex_w.test(wa);
        if (w == "") {
            alert("Please enter \u03C9_0!\n(it's usually -1)");
            r = false;
            return r;
        }
        if (wa == "") {
            alert("Please enter \u03C9_a!\n(it's usually 0)");
            r = false;
            return r;
        }
        if (oR == "") {
            alert("Please enter \u03A9_R!\n(it's usually zero)");
            r = false;
            return r;
        }
        if (oM == "") {
            alert("Please enter \u03A9_M!");
            r = false;
            return r;
        }
        if (oL == "") {
            alert("Please enter \u03A9_\u039B!");
            r = false;
            return r;
        }
        if (H0 == "") {
            alert("Please enter H_0!");
            r = false;
            return r;
        }
        if (z == "") {
            alert("Please enter a redshift!");
            r = false;
            return r;
        }
        if (w_t) {
            alert("Bad input for \u03C9_0! \n\nAccepted input: A single number.\n(also make sure there's no extra whitespace...)");
            r = false;
            return r;
        }
        if (wa_t) {
            alert("Bad input for \u03C9_a! \n\nAccepted input: A single number.\n(also make sure there's no extra whitespace...)");
            r = false;
            return r;
        }
        if (oR_t) {
            alert("Bad input for \u03A9_R! \n\nAccepted input: A single positive number.\n(also make sure there's no extra whitespace...)");
            r = false;
            return r;
        }
        if (oM_t) {
            alert("Bad input for \u03A9_M! \n\nAccepted input: A single positive number.\n(also make sure there's no extra whitespace...)");
            r = false;
            return r;
        }
        if (oL_t) {
            alert("Bad input for \u03A9_\u039B! \n\nAccepted input: A single positive number.\n(also make sure there's no extra whitespace...)");
            r = false;
            return r;
        }
        if (H0_t) {
            alert("Bad input for H_0! \n\nAccepted input: A single positive number.\n(also make sure there's no extra whitespace...)");
            r = false;
            return r;
        }
        if (z_t) {
            alert("Bad input for z! \n\nAccepted inputs: A single positive number, or a list of single positive numbers, separated by commas.");
            r = false;
            return r;
        }

        return r;
    }
</script>
<?php
$message = "";
$count = 0;
$submit = $_POST['submit'];
if ($submit == "Update") {
    $H0 = $_POST['H0'];
    $oM = $_POST['oM'];
    $oL = $_POST['oL'];
    $oR = $_POST['oR'];
    $w = $_POST['w'];
    $wa = $_POST['wa'];
    $z = $_POST['z'];
    $_SESSION['H0'] = $H0;
    $_SESSION['w']  = $w;
    $_SESSION['wa'] = $wa;
    $_SESSION['oR'] = $oR;
    $_SESSION['oM'] = $oM;
    $_SESSION['oL'] = $oL;
    $_SESSION['z']  = $z;
    $message = "Updated";
    $count++;
}
if ($submit == "Clear Form") {
    $_SESSION['H0'] = '';
    $_SESSION['w']  = '';
    $_SESSION['wa'] = '';
    $_SESSION['oR'] = '';
    $_SESSION['oM'] = '';
    $_SESSION['oL'] = '';
    $_SESSION['z']  = '';
    $message = "Cleared";
    $count++;
}
$H0 = $_SESSION['H0'];
$w  = $_SESSION['w'];
$wa = $_SESSION['wa'];
$oR = $_SESSION['oR'];
$oM = $_SESSION['oM'];
$oL = $_SESSION['oL'];
$z = $_SESSION['z'];
//echo "$message has been called $count times. <br /><br />";

if ($submit == "Submit") {
    $H0 = $_POST['H0'];
    $omegaM = $_POST['oM'];
    $omegaL = $_POST['oL'];
    $omegaR = $_POST['oR'];
    $w = $_POST['w'];
    $wa = $_POST['wa'];
    $z = $_POST['z'];
    $z = preg_replace('#\s+#', ',', trim($z));
    $z = preg_replace('#,,#', ',', trim($z));
    $_SESSION['H0'] = $H0;
    $_SESSION['w']  = $w;
    $_SESSION['wa'] = $wa;
    $_SESSION['oR'] = $oR;
    $_SESSION['oM'] = $oM;
    $_SESSION['oL'] = $oL;
    $_SESSION['z']  = $z;

    ob_start();
    $searchterm = trim($searchterm);
    $params = "$H0 $omegaM $omegaL $omegaR $w $wa $z";
    $command = "python calc.py $params";
    passthru($command);
    $output = ob_get_clean();
    print $output;
} else {
    if (isset($_POST['concordance'])) {
        $H0 = (string)70.0;
        $w = (string)-1;
        $wa = (string)0;
        $oR = (string)0;
        $oM = (string)0.3;
        $oL = (string)0.7;
        $message = "concordance";
        $count++;
    } else if (isset($_POST['wmap7'])) {
        $H0 = (string)70.2;
        $w = (string)-1;
        $wa = (string)0;
        $oR = (string)0;
        $oM = (string)0.272;
        $oL = (string)0.728;
        $message = 'wmap7';
        $count++;
    } else if (isset($_POST['planck'])) {
        $H0 = (string)67.3;
        $w = (string)-1;
        $wa = (string)0;
        $oR = (string)0;
        $oM = (string)0.315;
        $oL = (string)0.685;
        $message = 'planck';
        $count++;
    } else if (isset($_POST['flatempty'])) {
        $H0 = (string)70.0;
        $w = (string)-1;
        $wa = (string)0;
        $oR = (string)0;
        $oM = (string)0.0;
        $oL = (string)1.0;
        $message = 'flatempty';
        $count++;
    } else if (isset($_POST['einsteindesitter'])) {
        $H0 = (string)70.0;
        $w = (string)-1;
        $wa = (string)0;
        $oR = (string)0;
        $oM = (string)1.0;
        $oL = (string)0.0;
        $message = 'edisitter';
        $count++;
    } else {
        $H0 = $_SESSION['H0'];
        $w  = $_SESSION['w'];
        $wa = $_SESSION['wa'];
        $oR = $_SESSION['oR'];
        $oM = $_SESSION['oM'];
        $oL = $_SESSION['oL'];
        $z = $_SESSION['z'];
    }
    $printthing = <<<STR
  <font size=5>Thank you for using the <b><a href="http://astro.physics.unimelb.edu.au/"">University of Melbourne, School of Physics, Astrophysics Group</a>'s (UMSPAG) cosmology calculator>
  <br><br>
  Please change the cosmology and enter a redshift to calculate the comoving distance, angular diameter distance, luminosity distance, distance modulus, volume within z, comoving volume el>
  To calculate the cosmology at multiple redshifts, enter each z separated by a comma. If you enter a lot of redshifts it may take a minute or two to complete.
  <br><br>
  For fun, you can compare to <a href="http://www.astro.ucla.edu/~wright/CosmoCalc.html">Ned Wright</a>'s values if you input one value for z, however his values won't be printed if you in>
  <br>
  Note that Ned Wright's values always assume &#969=-1 and are a little less accurate.

  <hr>
  <h3>Choose a preset cosmology:</h3>
  <form name='cosmochooseform' method='POST' onkeypress="return event.keyCode != 13">
  <td><input type='submit' name='concordance' value='Concordance', style='height:50px; width:100px',  onclick='return true'></td>
  <td><input type='submit' name='wmap7' value='WMAP7', style='height:50px; width:100px',  onclick='return true'></td>
  <td><input type='submit' name='planck' value='Planck', style='height:50px; width:100px',  onclick='return true'></td>
  <td><input type='submit' name='flatempty' value='Flat Empty', style='height:50px; width:100px',  onclick='return true'></td>
  <td><input type='submit' name='einsteindesitter' value='Einstein de Sitter', style='height:50px; width:140px', onclick='return true'></td>
  </form>
  You can also access an exhaustive list of flat and non-flat cosmologies <a href="http://lambda.gsfc.nasa.gov/product/map/dr5/parameters.cfm">here</a>.
  <h3>Or enter your own cosmology:</h3>
  <form name='cosmocalcform' method='POST'>
  <div style="height:0px; width:0px; position:absolute; overflow:hidden">
    <input type='submit', name='submit', value='Update', onclick='return true' hidden >
  </div>
  <div>
  <table cellpadding='5' cellspacing='0' align='left'>
  <tr>
  <td><b>&#969<sub>0</sub>:</b></td>
  <td><input id='w' name='w' value='$w' style='width:40px'></td>
  <td>This is the expansion term. In standard cosmologies it is equal to &#969=&#969<sub>0</sub>=-1.</td>
  </tr>
  <tr>
  <td><b>&#969<sub>a</sub>:</b></td>
  <td><input id='wa' name='wa' value='$wa' style='width:40px'></td>
  <td>This term allows you to let the expansion term evolve with redshift as &#969<sub>CPL</sub> = &#969<sub>0</sub>+&#969<sub>a</sub>(z/1+z). This is the Chevalier-Polarski-Linder (CPL) p>
  </tr>
  <tr>
  <td><b>&#937<sub>R</sub>:</b></td>
  <td><input id='oR' name='oR' value='$oR' style='width:40px'></td>
  <td>This is the radiation density term. In standard cosmologies, radiation is only dominant at very high redshifts.</td>
  </tr>
  <tr>
  <td><b>&#937<sub>M</sub>:</b></td>
  <td><input id='oM' name='oM' value='$oM' style='width:40px'></td>
  <td>This is the matter density term.</td>
  </tr>
  <tr>
  <td><b>&#937<sub>&#923</sub>:</b></td>
  <td><input id='oL' name='oL' value='$oL' style='width:40px'></td>
  <td>This is the dark energy density term.</td>
  </tr>
  <tr>
  <td><b>H<sub>0</sub>:</b></td>
  <td><input id='H0' name='H0' value='$H0' style='width:40px'></td>
  <td>This is the Hubble constant.</td>
  </tr>
  <tr></tr>
  </table>
  </div>
  <div style="clear:both"> </div>
  <div>
  <h3>... and enter a redshift (or list of redshifts):</h3>
  <table>
  <tr>
  <td><b>z:</b></td>
  <td><textarea id='z' name='z' value='$z' style='height:50px; width:100px'>$z</textarea></td>
  </tr>
  <tr><td></td></tr>
  <tr><td></td></tr>
  <tr><td></td></tr>
  <tr>
  <td></td>
  <td><input type='submit' name='submit' value='Submit', style='height:50px; width:80px', onclick='return checkForm()' ></td>
  </tr>
  <tr>
  <td></td>
  <td><input type='submit' name='submit' value='Clear Form', style='height:50px; width:100px', onclick='return true' ></td>
  </tr>
  </div>
  </table>
  </form>
  <hr>
  <font size=2><b><sup>[1]</sup></b> M. Chevallier and D. Polarski, Int. J. Mod. Phys. D 10, 213 (2001), <b><sup>[2]</sup></b> E.V. Linder, Phys. Rev. Lett. 90, 091301 (2003)</font><br><br>
  Made by: <b>Robert L. Barone-Nugent</b>, <b>Catherine O. de Burgh-Day</b> and <b>Jaehong Park</b>, 2014.<br>
STR;
    echo $printthing;
    echo "$message has been called $count times. <br /><br />";
}
$_SESSION['H0'] = $H0;
$_SESSION['w']  = $w;
$_SESSION['wa'] = $wa;
$_SESSION['oR'] = $oR;
$_SESSION['oM'] = $oM;
$_SESSION['oL'] = $oL;
$_SESSION['z']  = $z;


?>

</html>