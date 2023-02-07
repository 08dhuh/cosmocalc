<?php
session_start();
// $python_path = "C:/Users/08dhu/AppData/Local/Programs/Python/Python39/python3.exe";
// $command = "$python_path --version 2>&1";
// $output = shell_exec($command);
// if (!empty($output)) {
//     echo "Python is installed on the server. version: " . $output;
// } else {
//     echo "Python is not installed on the server.";
// }
?>
<!DOCTYPE html>
<html>

<head>
    <title>Help</title>
</head>

<body>
    <form action="" method="post">
        <input type="submit" name="submit" value="Submit">
    </form>
</body>

</html>
<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $H0 = 70;
    $omegaM = 0.3;
    $omegaL = 0.7;
    $omegaR = 0;
    $w = -1;
    $wa = 0;
    $z = 1;

    $params = array($H0, $omegaM, $omegaL, $omegaR, $w, $wa, $z);
    $escaped_params = array_map('escapeshellarg', $params);
    $command = "python3 testcalc.py ". implode(" ", $escaped_params). " 2>&1";

    exec($command, $outputs, $return_var);
    echo "Return code: " . $return_var . "\n";
    echo "\nOutput:\n";
    foreach ($outputs as $line) {
        echo $line . "\n<br />";
    }
    if ($return_var !== 0) {
        echo "Error: Python script failed to run. code: <br>" . $return_var;
    } else {
        echo implode("\n", $outputs);
    }
}
?>

<!--
// ob_start();
// passthru($command);
// $output = ob_get_clean();
// print $output;

-->