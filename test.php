<!--tasks 
store variables
-->

<?php
session_start();
$cosmology_model = array(
    "concordance" => array("H0" => 70.0, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 0.3, "oL" => 0.7),
    "wmap7" => array("H0" => 70.2, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 0.272, "oL" => 0.728),
    "planck" => array("H0" => 67.3, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 0.315, "oL" => 0.685),
    "flatempty" => array("H0" => 70.0, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 0.0, "oL" => 1.0),
    "einsteindesitter" => array("H0" => 70.0, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 1.0, "oL" => 0.0)
);

$result_labels = ["Age at z=0", "Comoving distance", "Luminosity distance", "Angular Diameter distance", "Comoving volume", "Distance modulus", "Age at z", "Lookback time", "Comoving volume element"];

function validateFloat(float $input): bool
{
    return filter_var($input, FILTER_VALIDATE_FLOAT) !== false;
}

function set_cosmology($array)
{
    foreach ($array as $model => $params) {
        if (isset($_POST[$model])) {
            foreach ($params as $param => $param_value) {
                $_SESSION[$param] = $param_value;
            }
        }
    }
}

function combine_result($labels, $output_string)
{
    $array = explode(' ', $output_string);
    return array_combine($labels, $array);
}

?>
<!DOCTYPE html>
<html>

<head>
    <title>Help</title>
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
</head>

<body>
    <form action="" method="post">
        <input type="submit" name="submit" value="Submit">
    </form>
</body>


<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $H0 = 70;
    $omegaM = 0.3;
    $omegaL = 0.7;
    $omegaR = 0;
    $w = -1;
    $wa = 0;
    $z = 1;
    set_cosmology($cosmology_model);

    $params = array($H0, $omegaM, $omegaL, $omegaR, $w, $wa, $z);
    $escaped_params = array_map('escapeshellarg', $params);
    $command = "python3 testcalc.py " . implode(" ", $escaped_params) . " 2>&1";

    exec($command, $outputs, $return_var);
    echo "Return code: " . $return_var;
    echo "<br/>\nOutput:\n";
    foreach ($outputs as $key => $line) {
        if ($key % 3 !== 0) {
            $result = combine_result($result_labels, $line);
            print_r($result);
        } else {
            echo "[$key] : $line \n<br />";
        }
    }
    if ($return_var !== 0) {
        echo "Error: Python script failed to run. code: <br>" . $return_var;
    } // } else {
    //     echo implode("\n", $outputs);
    // }
}



?>

</html>
<!--
    // $python_path = "C:/Users/08dhu/AppData/Local/Programs/Python/Python39/python3.exe";
// $command = "$python_path --version 2>&1";
// $output = shell_exec($command);
// if (!empty($output)) {
//     echo "Python is installed on the server. version: " . $output;
// } else {
//     echo "Python is not installed on the server.";
// }
// ob_start();
// passthru($command);
// $output = ob_get_clean();
// print $output;

-->