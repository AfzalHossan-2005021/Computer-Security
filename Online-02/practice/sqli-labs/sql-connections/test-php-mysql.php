<?php
// Simple test to check if PHP and MySQL are working
echo "<h1>PHP and MySQL Test</h1>";

// Check PHP version
echo "<p>PHP Version: " . phpversion() . "</p>";

// Check MySQL connection
include("../sql-connections/db-creds.inc");

try {
    $con = new mysqli($host, $dbuser, $dbpass);
    if ($con->connect_error) {
        echo "<p style='color: red;'>MySQL Connection Failed: " . $con->connect_error . "</p>";
    } else {
        echo "<p style='color: green;'>MySQL Connection Successful!</p>";
        
        // Test security database
        $result = $con->query("SHOW DATABASES LIKE 'security'");
        if ($result && $result->num_rows > 0) {
            echo "<p style='color: green;'>Security database found!</p>";
            
            // Count users
            $con->select_db('security');
            $result = $con->query("SELECT COUNT(*) as count FROM users");
            $row = $result->fetch_assoc();
            echo "<p>Users in database: " . $row['count'] . "</p>";
        } else {
            echo "<p style='color: orange;'>Security database not found. Run setup script first.</p>";
        }
        
        $con->close();
    }
} catch (Exception $e) {
    echo "<p style='color: red;'>Error: " . $e->getMessage() . "</p>";
}
?>
