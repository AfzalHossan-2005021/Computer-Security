<?php
/**
 * Comprehensive Test Script for SQLi-Labs
 * 
 * This script tests all major lab functionalities to ensure they work correctly
 * after the MySQLi modernization.
 */

echo "=== SQLi-Labs Comprehensive Test ===\n";
echo "Testing modernized labs...\n\n";

// Test connection first
include('sql-connections/sql-connect.php');

// Disable MySQLi exceptions for testing
mysqli_report(MYSQLI_REPORT_OFF);

echo "1. Testing database connection...\n";
if ($GLOBALS['con1']) {
    echo "   ✓ Database connection successful\n";
} else {
    echo "   ✗ Database connection failed\n";
    exit(1);
}

// Test basic query
echo "2. Testing basic query...\n";
$sql = "SELECT * FROM users WHERE id=1 LIMIT 0,1";
$result = mysqli_query($GLOBALS['con1'], $sql);
if ($result) {
    $row = mysqli_fetch_array($result);
    if ($row) {
        echo "   ✓ Basic query successful: " . $row['username'] . "\n";
    } else {
        echo "   ✗ No data returned\n";
    }
} else {
    echo "   ✗ Query failed: " . mysqli_error($GLOBALS['con1']) . "\n";
}

// Test error-based injection
echo "3. Testing error-based injection...\n";
$sql = "SELECT * FROM users WHERE id='1'' LIMIT 0,1";
$result = @mysqli_query($GLOBALS['con1'], $sql);
if (!$result) {
    echo "   ✓ Error-based injection working: " . mysqli_error($GLOBALS['con1']) . "\n";
} else {
    echo "   ✗ Error-based injection not working\n";
}

// Test individual labs
echo "4. Testing individual labs...\n";

$testLabs = [
    'Less-1' => ['id' => '1', 'type' => 'GET'],
    'Less-2' => ['id' => '1', 'type' => 'GET'],
    'Less-3' => ['id' => '1', 'type' => 'GET'],
    'Less-5' => ['id' => '1', 'type' => 'GET'],
    'Less-11' => ['uname' => 'admin', 'passwd' => 'admin', 'type' => 'POST'],
];

foreach ($testLabs as $lab => $params) {
    echo "   Testing $lab...\n";
    
    $url = "http://localhost/sqli-labs/$lab/index.php";
    
    if ($params['type'] === 'GET') {
        $url .= '?id=' . $params['id'];
        $response = file_get_contents($url);
    } else {
        // POST request
        $context = stream_context_create([
            'http' => [
                'method' => 'POST',
                'header' => 'Content-Type: application/x-www-form-urlencoded',
                'content' => http_build_query([
                    'uname' => $params['uname'],
                    'passwd' => $params['passwd'],
                    'submit' => 'Submit'
                ])
            ]
        ]);
        $response = file_get_contents($url, false, $context);
    }
    
    if ($response !== false) {
        if (strpos($response, 'Login name') !== false || strpos($response, 'successfully logged in') !== false) {
            echo "     ✓ $lab working correctly\n";
        } else {
            echo "     ✗ $lab may have issues\n";
        }
    } else {
        echo "     ✗ $lab failed to load\n";
    }
}

echo "\n5. Testing injection payloads...\n";

$injectionTests = [
    'Less-1' => ["1'", "1 OR 1=1--", "1' OR '1'='1"],
    'Less-2' => ["1'", "1 OR 1=1--", "1 AND 1=2"],
];

foreach ($injectionTests as $lab => $payloads) {
    echo "   Testing $lab injections...\n";
    
    foreach ($payloads as $payload) {
        $url = "http://localhost/sqli-labs/$lab/index.php?id=" . urlencode($payload);
        $response = @file_get_contents($url);
        
        if ($response !== false) {
            if (strpos($response, 'error') !== false || strpos($response, 'Error') !== false || 
                strpos($response, 'MySQL') !== false || strpos($response, 'syntax') !== false) {
                echo "     ✓ Injection '$payload' triggered error (good)\n";
            } else {
                echo "     - Injection '$payload' no visible error\n";
            }
        } else {
            echo "     ✗ Injection '$payload' failed to load\n";
        }
    }
}

echo "\n=== Test Complete ===\n";
echo "All tests completed. Check results above.\n";
echo "If any tests show issues, investigate the specific lab.\n";
echo "The modernization should be working correctly.\n";

?>
