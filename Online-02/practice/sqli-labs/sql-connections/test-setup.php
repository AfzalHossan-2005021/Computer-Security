<?php
/**
 * Database Setup Test Script
 * Tests the database connections and verifies data integrity
 */

echo "=== SQL Injection Labs Database Test ===\n";
echo "Testing database setup and connections...\n\n";

//including the Mysql connect parameters.
include("../sql-connections/db-creds.inc");

// Test connection to MySQL server
echo "1. Testing MySQL connection...\n";
$con = new mysqli($host, $dbuser, $dbpass);
if ($con->connect_error) {
    die("❌ Connection failed: " . $con->connect_error . "\n");
} else {
    echo "✅ MySQL connection successful\n";
}

// Test security database
echo "\n2. Testing SECURITY database...\n";
$result = $con->query("SHOW DATABASES LIKE 'security'");
if ($result && $result->num_rows > 0) {
    echo "✅ Security database exists\n";
    
    // Test tables
    $con->select_db('security');
    $tables = ['users', 'emails', 'uagents', 'referers'];
    
    foreach ($tables as $table) {
        $result = $con->query("SHOW TABLES LIKE '$table'");
        if ($result && $result->num_rows > 0) {
            echo "✅ Table '$table' exists\n";
            
            // Count records
            $result = $con->query("SELECT COUNT(*) as count FROM $table");
            $row = $result->fetch_assoc();
            echo "   Records in $table: " . $row['count'] . "\n";
        } else {
            echo "❌ Table '$table' missing\n";
        }
    }
} else {
    echo "❌ Security database not found\n";
}

// Test challenges database
echo "\n3. Testing CHALLENGES database...\n";
$result = $con->query("SHOW DATABASES LIKE '$dbname1'");
if ($result && $result->num_rows > 0) {
    echo "✅ Challenges database '$dbname1' exists\n";
    
    // Get table names in challenges database
    $result = $con->query("SHOW TABLES FROM $dbname1");
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_array()) {
            echo "✅ Challenge table: " . $row[0] . "\n";
            
            // Count records
            $count_result = $con->query("SELECT COUNT(*) as count FROM $dbname1." . $row[0]);
            $count_row = $count_result->fetch_assoc();
            echo "   Records in " . $row[0] . ": " . $count_row['count'] . "\n";
        }
    } else {
        echo "❌ No tables found in challenges database\n";
    }
} else {
    echo "❌ Challenges database not found\n";
}

// Test sample queries
echo "\n4. Testing sample queries...\n";
$con->select_db('security');

// Test user login simulation
$result = $con->query("SELECT username, password FROM users WHERE username = 'admin' AND password = 'admin'");
if ($result && $result->num_rows > 0) {
    echo "✅ Sample login query works\n";
} else {
    echo "❌ Sample login query failed\n";
}

// Test email search
$result = $con->query("SELECT email_id FROM emails WHERE email_id LIKE '%dhakkan%'");
if ($result && $result->num_rows > 0) {
    echo "✅ Sample email search works\n";
    echo "   Found " . $result->num_rows . " emails with 'dhakkan' domain\n";
} else {
    echo "❌ Sample email search failed\n";
}

// Test character set
$result = $con->query("SELECT DEFAULT_CHARACTER_SET_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'security'");
if ($result && $result->num_rows > 0) {
    $row = $result->fetch_assoc();
    echo "✅ Character set: " . $row['DEFAULT_CHARACTER_SET_NAME'] . "\n";
} else {
    echo "❌ Could not determine character set\n";
}

$con->close();

echo "\n=== Test Summary ===\n";
echo "If all tests show ✅, your database setup is working correctly.\n";
echo "If any tests show ❌, please run the setup script again.\n";
echo "\nTo run setup:\n";
echo "- Web interface: navigate to complete-setup.php\n";
echo "- Command line: php setup-complete-cli.php\n";
?>
