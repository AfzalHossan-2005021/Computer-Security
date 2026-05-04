<?php
/**
 * Modern Database Setup Script for SQL Injection Labs
 * Updated to use MySQLi instead of deprecated mysql_* functions
 * Includes proper error handling and security improvements
 */

// Include database credentials
include("../sql-connections/db-creds.inc");

// Set error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Function to create database connection
function createConnection($host, $dbuser, $dbpass, $dbname = null) {
    $conn = new mysqli($host, $dbuser, $dbpass, $dbname);
    
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    
    return $conn;
}

// Function to execute query with error handling
function executeQuery($conn, $sql, $description) {
    echo "<div style='color: #FFFF00; font-size: 14px; margin: 10px 0;'>";
    
    if ($conn->query($sql) === TRUE) {
        echo "[*]...................{$description} - SUCCESS<br>";
        echo "<span style='color: #00FF00;'>✓ Query executed successfully</span>";
    } else {
        echo "[*]...................{$description} - ERROR<br>";
        echo "<span style='color: #FF0000;'>✗ Error: " . $conn->error . "</span>";
    }
    
    echo "</div>";
}

// Function to setup main security database
function setupSecurityDatabase($host, $dbuser, $dbpass) {
    // Create connection without database selection
    $conn = createConnection($host, $dbuser, $dbpass);
    
    echo "<h2 style='color: #00FF00; margin: 20px 0;'>Setting up SECURITY Database</h2>";
    
    // Drop existing database if exists
    $sql = "DROP DATABASE IF EXISTS security";
    executeQuery($conn, $sql, "Dropping existing 'security' database");
    
    // Create new database
    $sql = "CREATE DATABASE security CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci";
    executeQuery($conn, $sql, "Creating new 'security' database");
    
    // Select the database
    $conn->select_db('security');
    
    // Create users table
    $sql = "CREATE TABLE users (
        id INT(3) NOT NULL AUTO_INCREMENT,
        username VARCHAR(20) NOT NULL,
        password VARCHAR(20) NOT NULL,
        PRIMARY KEY (id)
    )";
    executeQuery($conn, $sql, "Creating 'users' table");
    
    // Create emails table
    $sql = "CREATE TABLE emails (
        id INT(3) NOT NULL AUTO_INCREMENT,
        email_id VARCHAR(30) NOT NULL,
        PRIMARY KEY (id)
    )";
    executeQuery($conn, $sql, "Creating 'emails' table");
    
    // Create uagents table
    $sql = "CREATE TABLE uagents (
        id INT(3) NOT NULL AUTO_INCREMENT,
        uagent VARCHAR(256) NOT NULL,
        ip_address VARCHAR(35) NOT NULL,
        username VARCHAR(20) NOT NULL,
        PRIMARY KEY (id)
    )";
    executeQuery($conn, $sql, "Creating 'uagents' table");
    
    // Create referers table
    $sql = "CREATE TABLE referers (
        id INT(3) NOT NULL AUTO_INCREMENT,
        referer VARCHAR(256) NOT NULL,
        ip_address VARCHAR(35) NOT NULL,
        PRIMARY KEY (id)
    )";
    executeQuery($conn, $sql, "Creating 'referers' table");
    
    // Insert data into users table
    $sql = "INSERT INTO users (id, username, password) VALUES 
        (1, 'Dumb', 'Dumb'),
        (2, 'Angelina', 'I-kill-you'),
        (3, 'Dummy', 'p@ssword'),
        (4, 'secure', 'crappy'),
        (5, 'stupid', 'stupidity'),
        (6, 'superman', 'genious'),
        (7, 'batman', 'mob!le'),
        (8, 'admin', 'admin'),
        (9, 'admin1', 'admin1'),
        (10, 'admin2', 'admin2'),
        (11, 'admin3', 'admin3'),
        (12, 'dhakkan', 'dumbo'),
        (14, 'admin4', 'admin4')";
    executeQuery($conn, $sql, "Inserting data into 'users' table");
    
    // Insert data into emails table
    $sql = "INSERT INTO emails (id, email_id) VALUES 
        (1, 'Dumb@dhakkan.com'),
        (2, 'Angel@iloveu.com'),
        (3, 'Dummy@dhakkan.local'),
        (4, 'secure@dhakkan.local'),
        (5, 'stupid@dhakkan.local'),
        (6, 'superman@dhakkan.local'),
        (7, 'batman@dhakkan.local'),
        (8, 'admin@dhakkan.com')";
    executeQuery($conn, $sql, "Inserting data into 'emails' table");
    
    $conn->close();
    
    echo "<div style='color: #00FF00; font-size: 16px; margin: 20px 0; padding: 10px; border: 1px solid #00FF00;'>";
    echo "✓ Security database setup completed successfully!";
    echo "</div>";
}

// Function to setup challenges database
function setupChallengesDatabase($host, $dbuser, $dbpass, $dbname1) {
    $conn = createConnection($host, $dbuser, $dbpass);
    
    echo "<h2 style='color: #00FF00; margin: 20px 0;'>Setting up CHALLENGES Database</h2>";
    
    // Drop existing database if exists
    $sql = "DROP DATABASE IF EXISTS $dbname1";
    executeQuery($conn, $sql, "Dropping existing '{$dbname1}' database");
    
    // Create new database
    $sql = "CREATE DATABASE $dbname1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci";
    executeQuery($conn, $sql, "Creating new '{$dbname1}' database");
    
    // Select the database
    $conn->select_db($dbname1);
    
    // Generate random table name and secret key
    $characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $table = generateRandomString(10, $characters);
    $secret_key = "secret_" . generateRandomString(4, $characters);
    
    // Create challenges table
    $sql = "CREATE TABLE $table (
        id INT(2) UNSIGNED NOT NULL DEFAULT 1,
        sessid CHAR(32) PRIMARY KEY NOT NULL,
        $secret_key CHAR(32) NOT NULL,
        tryy INT(11) UNSIGNED NOT NULL DEFAULT 0
    )";
    executeQuery($conn, $sql, "Creating challenges table '$table'");
    
    // Insert dummy data
    $sec_key = generateRandomString(24, $characters);
    $hash = md5(rand(0, 100000));
    
    $sql = "INSERT INTO $table VALUES (1, '$hash', '$sec_key', 0)";
    executeQuery($conn, $sql, "Inserting dummy data into '$table'");
    
    echo "<div style='color: #FFFF00; margin: 10px 0;'>";
    echo "[*]...................Secret key '$secret_key' inserted into table '$table'";
    echo "</div>";
    
    $conn->close();
    
    echo "<div style='color: #00FF00; font-size: 16px; margin: 20px 0; padding: 10px; border: 1px solid #00FF00;'>";
    echo "✓ Challenges database setup completed successfully!";
    echo "</div>";
}

// Function to generate random string
function generateRandomString($length, $characters) {
    $string = '';
    for ($i = 0; $i < $length; $i++) {
        $string .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $string;
}

// Function to test database connection
function testConnection($host, $dbuser, $dbpass) {
    echo "<h2 style='color: #00FF00; margin: 20px 0;'>Testing Database Connection</h2>";
    
    $conn = new mysqli($host, $dbuser, $dbpass);
    
    if ($conn->connect_error) {
        echo "<div style='color: #FF0000; font-size: 16px; margin: 10px 0;'>";
        echo "✗ Connection failed: " . $conn->connect_error;
        echo "</div>";
        return false;
    } else {
        echo "<div style='color: #00FF00; font-size: 16px; margin: 10px 0;'>";
        echo "✓ Database connection successful!";
        echo "</div>";
        $conn->close();
        return true;
    }
}

// Main execution starts here
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Modern SQL Injection Labs - Database Setup</title>
    <style>
        body {
            background-color: #000000;
            color: #FFFFFF;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            border: 2px solid #00FF00;
            background-color: #001100;
        }
        .section {
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #333333;
            background-color: #111111;
        }
        .success {
            color: #00FF00;
        }
        .error {
            color: #FF0000;
        }
        .warning {
            color: #FFFF00;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="color: #00FF00; font-size: 28px;">Welcome <span style="color: #FF0000;">Dhakkan</span></h1>
            <h2 style="color: #FFFF00; font-size: 20px;">MODERN DATABASE SETUP FOR SQL INJECTION LABS</h2>
            <p style="color: #CCCCCC;">Updated with MySQLi, proper error handling, and security improvements</p>
        </div>

        <div class="section">
            <?php
            // Test database connection first
            if (testConnection($host, $dbuser, $dbpass)) {
                echo "<div style='margin: 20px 0;'>";
                echo "<h3 style='color: #FFFF00;'>Database Credentials:</h3>";
                echo "<ul style='color: #CCCCCC;'>";
                echo "<li>Host: $host</li>";
                echo "<li>Username: $dbuser</li>";
                echo "<li>Password: " . (empty($dbpass) ? '[empty]' : '[set]') . "</li>";
                echo "<li>Main Database: $dbname</li>";
                echo "<li>Challenges Database: $dbname1</li>";
                echo "</ul>";
                echo "</div>";
                
                // Setup security database
                setupSecurityDatabase($host, $dbuser, $dbpass);
                
                // Setup challenges database
                setupChallengesDatabase($host, $dbuser, $dbpass, $dbname1);
                
                echo "<div style='color: #00FF00; font-size: 18px; margin: 30px 0; padding: 20px; border: 2px solid #00FF00; text-align: center;'>";
                echo "🎉 ALL DATABASES SETUP COMPLETED SUCCESSFULLY! 🎉<br>";
                echo "You can now proceed with the SQL injection labs.";
                echo "</div>";
                
            } else {
                echo "<div style='color: #FF0000; font-size: 16px; margin: 20px 0; padding: 15px; border: 1px solid #FF0000;'>";
                echo "❌ Database connection failed. Please check your credentials in db-creds.inc";
                echo "</div>";
            }
            ?>
        </div>
        
        <div class="section">
            <h3 style="color: #FFFF00;">What's Different in This Modern Version?</h3>
            <ul style="color: #CCCCCC;">
                <li>✅ Uses MySQLi instead of deprecated mysql_* functions</li>
                <li>✅ Proper error handling and reporting</li>
                <li>✅ UTF-8 character set support</li>
                <li>✅ Better HTML structure and styling</li>
                <li>✅ Improved security practices</li>
                <li>✅ More readable and maintainable code</li>
            </ul>
        </div>
    </div>
</body>
</html>
