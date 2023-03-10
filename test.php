<!--tasks 
Use more descriptive function and variable names: 
Function and variable names should be descriptive and self-explanatory, such as combineResult instead of combine_result and cosmologyModel instead of cosmology_model.

Remove unnecessary functions: 
Some functions, such as validate_numeric_array, are not being used and can be removed.

Use type hints: 
Type hints can be added to functions to make their expected inputs and outputs more explicit, such as function combineResult(array $labels, string $outputString): array.

Use exceptions for error handling: 
    Instead of using a simple return value to indicate the success or failure of a function, exceptions can be used to handle errors and make the code more readable, for example by throwing an exception in the case of invalid inputs to the combineResult function.

Refactor repetitive code: 
Repetitive code, such as the code in update_params_from_session and update_params_from_post, can be refactored into a single function with an additional parameter indicating the source of the parameters.

Store configuration values in a separate file: 
Configuration values, such as the $calc_labels and $result_labels arrays, should be stored in a separate file, such as a config.php file, to make it easier to maintain and reuse the code.

Use a database for storing session data: 
    Storing session data in a database can improve the reliability and scalability of the application, and make it easier to manage session data.

Replace the hardcoded arrays with a database query: 
The $cosmology_model array can be replaced with a database query to retrieve the information, making it easier to update and maintain the data.

store variables

To display a temporary file on a PHP website and then automatically delete it so that you don't overload the server storage, 
you can use the following steps:

Generate the file: In your Python script, generate the file that you want to display on the PHP website. 
For example, you could generate a plot as a PNG image file.

Save the file: Save the file to a temporary directory on the server. 
You can use the tempfile module in Python to generate a unique temporary file name.

Display the file on the PHP website: On the PHP side, use the <img> tag to display the file. 
You'll need to specify the URL of the file on the server.

Delete the file: After a certain amount of time or after the file has been displayed a certain number of times, 
you can use the unlink() function in PHP to delete the file from the server.

Cron Job:
-->
<!-- /
Calculates the results based on the given input parameters and cosmology model.

@param array 
@param string $cosmology_model The name of the cosmology model to use.
@return array An associative array with the result labels as keys and their calculated values as values.
 / -->
<?php

use JetBrains\PhpStorm\NoReturn;

session_start();
//store the session ID
$session_id = session_id();

$cosmology_model = array(
    "concordance" => array("H0" => 70.0, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 0.3, "oL" => 0.7),
    "wmap7" => array("H0" => 70.2, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 0.272, "oL" => 0.728),
    "planck" => array("H0" => 67.3, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 0.315, "oL" => 0.685),
    "flatempty" => array("H0" => 70.0, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 0.0, "oL" => 1.0),
    "einsteindesitter" => array("H0" => 70.0, "w" => -1, "wa" => 0, "oR" => 0, "oM" => 1.0, "oL" => 0.0)
);

$calc_labels = ['H0', 'oM', 'oL', 'oR', 'w', 'wa', 'z'];
$result_labels = ["Age at z=0", "Comoving distance", "Luminosity distance", "Angular Diameter distance", "Comoving volume", "Distance modulus", "Age at z", "Lookback time", "Comoving volume element"];

#$calc_params is an associative array with the input parameters as keys and their values as values.
$calc_param_container = clear_form($calc_labels);
#result_param is an associative array with the result labels as keys and their calculated values as values.
$result_param_container = clear_form($result_labels);

//print_r($calc_param_container);

function validate_numeric_array(array $inputs): bool //finish later
{
    foreach ($inputs as $key => $value) {
        if (gettype($value) === "array") {
            return validate_numeric_array($value);
        } else {
        }
    }
    $filtered = array_filter($inputs, function ($input) {
        return filter_var($input, FILTER_VALIDATE_FLOAT) ||
            filter_var($input, FILTER_VALIDATE_INT);
    });
    return count($filtered) === count($inputs);
}

function set_cosmology(array $array): void
{
    foreach ($array as $model => $params) {
        if (isset($_POST[$model])) {
            foreach ($params as $param => $param_value) {
                $_SESSION[$param] = $param_value;
            }
        }
    }
}

function combine_result(array $labels, string $output_string): array
{
    $array = explode(' ', $output_string);
    return array_combine($labels, $array);
}

function clear_form(array $labels): array #initializes the array
{
    return array_fill_keys($labels, 0);
}

function sync_session_with_params(array $params): void
{
    foreach ($params as $label => $value) {
        $_SESSION[$label] = $value;
    }
}

function update_params(array $params, bool $isSessionRequest): array
{
    foreach ($params as $key => $value) {
        if (isset($_SESSION[$key])) {
            $params[$key] = $isSessionRequest ? $_SESSION[$key] : $_POST[$key];
        }
    }
    return $params;
}



?>


<!DOCTYPE html>
<html>

<head>
    <title>NEW COSMOCALC PROTO</title>
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
    <hr>
    <h3>Choose a preset cosmology:</h3>
    <form name='cosmochooseform' method='POST'>
        <td><input type='submit' name='concordance' value='Concordance' , style='height:50px; width:120px'></td>
        <td><input type='submit' name='wmap7' value='WMAP7' , style='height:50px; width:100px'></td>
        <td><input type='submit' name='planck' value='Planck' , style='height:50px; width:100px'></td>
        <td><input type='submit' name='flatempty' value='Flat Empty' , style='height:50px; width:100px'></td>
        <td><input type='submit' name='einsteindesitter' value='Einstein de Sitter' , style='height:50px; width:140px'></td>
    </form>
    <form name='cosmocalcform' method='POST'>
        <div style="height:0px; width:0px; position:absolute; overflow:hidden">
            <input type='submit' , name='submit' , value='Update' , onclick='return true' hidden>
        </div>
        <div>
            <table cellpadding='5' cellspacing='0' align='left'>
                <tr>
                    <td><b>&#969<sub>0</sub>:</b></td>
                    <td><input id='w' name='w' value='<?php echo $_SESSION['w']; ?>' style='width:40px'></td>
                    <td>This is the expansion term. In standard cosmologies it is equal to &#969=&#969<sub>0</sub>=-1.</td>
                </tr>
                <tr>
                    <td><b>&#969<sub>a</sub>:</b></td>
                    <td><input id='wa' name='wa' value='<?php echo $_SESSION['wa']; ?>' style='width:40px'></td>
                    <td>This term allows you to let the expansion term evolve with redshift as &#969<sub>CPL</sub> = &#969<sub>0</sub>+&#969<sub>a</sub>(z/1+z). This is the Chevalier-Polarski-Linder (CPL) p>
                </tr>
                <tr>
                    <td><b>&#937<sub>R</sub>:</b></td>
                    <td><input id='oR' name='oR' value='<?php echo $_SESSION['oR']; ?>' style='width:40px'></td>
                    <td>This is the radiation density term. In standard cosmologies, radiation is only dominant at very high redshifts.</td>
                </tr>
                <tr>
                    <td><b>&#937<sub>M</sub>:</b></td>
                    <td><input id='oM' name='oM' value='<?php echo $_SESSION['oM']; ?>' style='width:40px'></td>
                    <td>This is the matter density term.</td>
                </tr>
                <tr>
                    <td><b>&#937<sub>&#923</sub>:</b></td>
                    <td><input id='oL' name='oL' value='<?php echo $_SESSION['oL']; ?>' style='width:40px'></td>
                    <td>This is the dark energy density term.</td>
                </tr>
                <tr>
                    <td><b>H<sub>0</sub>:</b></td>
                    <td><input id='H0' name='H0' value='<?php echo $_SESSION['H0']; ?>' style='width:40px'></td>
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
                    <td><textarea id='z' name='z' value='<?php echo $_SESSION['z']; ?>' style='height:50px; width:100px'><?php echo $_SESSION['z']; ?></textarea></td>
                </tr>
                <tr>
                    <td></td>
                </tr>
                <tr>
                    <td></td>
                </tr>
                <tr>
                    <td></td>
                </tr>
                <tr>
                    <td></td>
                    <td><input type='submit' name='submit' value='Submit' , style='height:50px; width:80px' , onclick='return checkForm()'></td>
                </tr>
                <tr>
                    <td></td>
                    <td><input type='submit' name='submit' value='Clear Form' , style='height:50px; width:100px' , onclick='return true'></td>
                </tr>
        </div>
        </table>
    </form>
    <!-- <form action="" method="post">
        <input type="submit" name="submit" value="Submit">
    </form> -->
</body>


<?php
if (isset($_POST['submit']) && $_POST['submit'] == 'Submit') {
    $calc_param_container = update_params($calc_param_container, $isSessionRequest=false);
    #$calc_param_container = update_params_from_post($calc_param_container);
    sync_session_with_params($calc_param_container);
    #relay data to calc.py
    $escaped_params = array_map('escapeshellarg', $calc_param_container);
    $command = "python3 testcalc.py " . implode(" ", $escaped_params) . " 2>&1";
    exec($command, $outputs, $return_var);

    #handle outputs
    echo "Return code: " . $return_var;
    echo "<br/>\nOutput:\n";
    #$outputs is an array that stores calculation results in groups of 3 lines for each redshift
    foreach ($outputs as $key => $line) {
        #when the script failed  to run
        if ($return_var !== 0) {
            echo "Error: Python script failed to run. code: <br>" . $return_var;
            echo "[$key] : $line \n<br />";
        } else {
            #successful calculation
            if ($key % 3 !== 0) { #1 for UoM calculation, #2 for Ned Wright calculation, #3
                $result = combine_result($result_labels, $line);
                print_r($result);
            } else {
                echo "[$key] : $line \n<br />"; #redshift
            }
        }
    }
}
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    set_cosmology($cosmology_model);
    $calc_param_container = update_params($calc_param_containe, $isSessionRequest=false);
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