<?php
/**
 * Debug Less-2 with direct PHP execution
 */
echo "=== Less-2 Debug Test ===\n";

// Include connection
include('sql-connections/sql-connect.php');

// Disable MySQLi exceptions
mysqli_report(MYSQLI_REPORT_OFF);

// Test the exact query from Less-2
$id = "1'";
$sql = "SELECT * FROM users WHERE id=$id LIMIT 0,1";

echo "Query: $sql\n";
echo "Testing query execution...\n";

$result = mysqli_query($GLOBALS["con1"], $sql);

if ($result) {
    echo "Query succeeded\n";
    $row = mysqli_fetch_array($result);
    if ($row) {
        echo "Data: " . print_r($row, true) . "\n";
    } else {
        echo "No data returned\n";
    }
} else {
    echo "Query failed\n";
    echo "Error: " . mysqli_error($GLOBALS["con1"]) . "\n";
}

echo "=== Debug Complete ===\n";
?>
