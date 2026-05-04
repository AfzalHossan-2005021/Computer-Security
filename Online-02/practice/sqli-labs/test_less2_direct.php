<?php
/**
 * Direct test of Less-2 functionality
 */
echo "=== Testing Less-2 Directly ===\n";

// Include the connection
include('sql-connections/sql-connect.php');

// Test normal query
echo "1. Normal query test (id=1):\n";
$id = 1;
$sql = "SELECT * FROM users WHERE id=$id LIMIT 0,1";
$result = mysqli_query($GLOBALS["con1"], $sql);
$row = mysqli_fetch_array($result);
if ($row) {
    echo "   ✓ Success: " . $row['username'] . " / " . $row['password'] . "\n";
} else {
    echo "   ✗ Failed: " . mysqli_error($GLOBALS["con1"]) . "\n";
}

// Test injection
echo "\n2. Injection test (id=1'):\n";
$id = "1'";
$sql = "SELECT * FROM users WHERE id=$id LIMIT 0,1";
$result = mysqli_query($GLOBALS["con1"], $sql);
if ($result) {
    $row = mysqli_fetch_array($result);
    if ($row) {
        echo "   - Query succeeded (unexpected)\n";
    } else {
        echo "   - Query returned no results\n";
    }
} else {
    echo "   ✓ SQL Error (expected): " . mysqli_error($GLOBALS["con1"]) . "\n";
}

// Test union injection
echo "\n3. Union injection test (id=1 UNION SELECT 1,2,3):\n";
$id = "1 UNION SELECT 1,2,3";
$sql = "SELECT * FROM users WHERE id=$id LIMIT 0,1";
$result = mysqli_query($GLOBALS["con1"], $sql);
if ($result) {
    $row = mysqli_fetch_array($result);
    if ($row) {
        echo "   ✓ Union worked: " . $row['username'] . " / " . $row['password'] . "\n";
    } else {
        echo "   - Union returned no results\n";
    }
} else {
    echo "   ✗ Union error: " . mysqli_error($GLOBALS["con1"]) . "\n";
}

echo "\n=== Less-2 Test Complete ===\n";
?>
