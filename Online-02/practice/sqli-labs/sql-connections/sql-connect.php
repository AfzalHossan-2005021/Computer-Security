<?php

//including the Mysql connect parameters.
include("db-creds.inc");
@error_reporting(0);

// Disable MySQLi exceptions for compatibility with old error handling
mysqli_report(MYSQLI_REPORT_OFF);

// Updated to use MySQLi
$con = new mysqli($host, $dbuser, $dbpass, $dbname);
// Check connection
if ($con->connect_error) {
    echo "Failed to connect to MySQL: " . $con->connect_error;
}

// Make connection available globally for labs
$GLOBALS['con1'] = $con;

$sql_connect = "SQL Connect included";
############################################
# For Less-24
$form_title_in="Please Login to Continue";
$form_title_ns="New User";
$feedback_title_ns="New User";
$form_title_ns= "Less-24";

############################################
# For Challenge series--- Randomizing the Table names.

?>




 
