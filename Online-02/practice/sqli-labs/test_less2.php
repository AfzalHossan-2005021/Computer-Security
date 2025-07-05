<?php
// Quick test of Less-2
include('/home/afzal/sqli-labs/sql-connections/sql-connect.php');

$id = 1;
$sql = "SELECT * FROM users WHERE id=$id LIMIT 0,1";
$result = mysqli_query($GLOBALS["con1"], $sql);
$row = mysqli_fetch_array($result);

if($row) {
    echo "SUCCESS: Found user data\n";
    echo "Username: " . $row['username'] . "\n";
    echo "Password: " . $row['password'] . "\n";
} else {
    echo "ERROR: " . mysqli_error($GLOBALS["con1"]) . "\n";
}
?>
