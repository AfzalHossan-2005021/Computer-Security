<html>
<head>
</head>
<body bgcolor="#000000">
<?php
//including the Mysql connect parameters
include '../sql-connections/db-creds.inc';

@error_reporting(0);
if(isset($_GET['id']))
    $id = $_GET['id'];
//echo $id;

// Check connection - Updated to use MySQLi
$con = new mysqli($host, $dbuser, $dbpass);
if ($con->connect_error) {
    echo "Failed to connect to MySQL: " . $con->connect_error;
    exit;
}

// Function to execute query and display result for challenges
function executeChallengeQuery($connection, $sql, $successMessage, $errorMessage) {
    if ($connection->query($sql)) {
        echo "[*]...................$successMessage";
        echo "<br><br>\n";
    } else {
        echo "[*]...................$errorMessage: " . $connection->error;
        echo "<br><br>\n";
    }
}

//purging Old Database for challenges	
$sql = "DROP DATABASE IF EXISTS $dbname1";
executeChallengeQuery($con, $sql, "Old database purged if exists", "Error purging database");

//Creating new database for challenges
$sql = "CREATE DATABASE $dbname1 CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`";
executeChallengeQuery($con, $sql, "Creating New database successfully", "Error creating database");

include '../sql-connections/functions.php';

// Creating table 
$sql = "CREATE TABLE IF NOT EXISTS $dbname1.$table (
    id INT(2) UNSIGNED NOT NULL DEFAULT 1,
    sessid CHAR(32) PRIMARY KEY NOT NULL,
    $secret_key CHAR(32) NOT NULL,
    tryy INT(11) UNSIGNED NOT NULL DEFAULT 0 
)";
executeChallengeQuery($con, $sql, "Creating New Table '$table' successfully", "Error creating Table");

// creating random key
$characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'; //characterset for generating random data
$sec_key = num_gen(24, $characters);
$hash = md5(rand(0,100000));

//inserting Dummy data into table
$sql = "INSERT INTO $dbname1.$table VALUES (1, '$hash', '$sec_key', 0)";
executeChallengeQuery($con, $sql, "Inserted data correctly into table '$table'", "Error inserting data");

echo "[*]...................Inserted secret key '$secret_key' into table ";
echo "<br><br>\n";

// Close connection
$con->close();

if(isset($id))
    header("refresh:0;url=$id");
?>
</body>
</html>
