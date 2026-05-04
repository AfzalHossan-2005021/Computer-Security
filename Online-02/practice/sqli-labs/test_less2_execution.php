<?php
// Test the actual Less-2 file execution
echo "Testing Less-2 file execution...\n";

// Set up error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Simulate the exact environment
$_GET['id'] = "1'";

// Include the connection
include('sql-connections/sql-connect.php');

// Disable MySQLi exceptions
mysqli_report(MYSQLI_REPORT_OFF);

echo "Connection established: " . (isset($GLOBALS['con1']) ? "YES" : "NO") . "\n";

// Test the exact code from Less-2
$id = $_GET['id'];
echo "ID parameter: $id\n";

// Test file logging
$fp = @fopen('result.txt', 'a');
if ($fp) {
    fwrite($fp, 'ID:' . $id . "\n");
    fclose($fp);
    echo "File logging: SUCCESS\n";
} else {
    echo "File logging: FAILED\n";
}

// Test query
$sql = "SELECT * FROM users WHERE id=$id LIMIT 0,1";
echo "SQL: $sql\n";

$result = mysqli_query($GLOBALS["con1"], $sql);
echo "Query result: " . ($result ? "SUCCESS" : "FAILED") . "\n";

if ($result) {
    $row = mysqli_fetch_array($result);
    if ($row) {
        echo "Data found: " . $row['username'] . "\n";
    } else {
        echo "No data returned\n";
    }
} else {
    echo "Error: " . mysqli_error($GLOBALS["con1"]) . "\n";
}

echo "Test complete.\n";
?>
