<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>SETUP DB - SQL Injection Labs</title>
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
    .output {
        background-color: #111111;
        padding: 20px;
        border: 1px solid #333333;
        margin: 20px 0;
        border-radius: 5px;
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
        <h1 style="color: #00FF00; font-size: 32px;">Welcome&nbsp;&nbsp;&nbsp;<span style="color: #FF0000;">Dhakkan</span></h1>
        <h2 style="color: #FFFF00; font-size: 24px;">SETTING UP THE DATABASE SCHEMA AND POPULATING DATA IN TABLES</h2>
    </div>

    <div class="output">
        <font size="3" color="#FFFF00">

<?php
//including the Mysql connect parameters.
include("../sql-connections/db-creds.inc");

// Updated to use MySQLi instead of deprecated mysql_* functions
$con = new mysqli($host, $dbuser, $dbpass);
if ($con->connect_error) {
    die('[*]...................Could not connect to DB, check the creds in db-creds.inc: ' . $con->connect_error);
}

// Function to execute query and display result
function executeQuery($connection, $sql, $successMessage, $errorMessage) {
    if ($connection->query($sql)) {
        echo "[*]...................$successMessage";
        echo "<br><br>\n";
    } else {
        echo "[*]...................$errorMessage: " . $connection->error;
        echo "<br><br>\n";
    }
}

//purging Old Database	
$sql = "DROP DATABASE IF EXISTS security";
executeQuery($con, $sql, "Old database 'SECURITY' purged if exists", "Error purging database");

//Creating new database security
$sql = "CREATE DATABASE `security` CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`";
executeQuery($con, $sql, "Creating New database 'SECURITY' successfully", "Error creating database");

//creating table users
$sql = "CREATE TABLE security.users (id int(3) NOT NULL AUTO_INCREMENT, username varchar(20) NOT NULL, password varchar(20) NOT NULL, PRIMARY KEY (id))";
executeQuery($con, $sql, "Creating New Table 'USERS' successfully", "Error creating Table");

//creating table emails
$sql = "CREATE TABLE security.emails (
    id int(3) NOT NULL AUTO_INCREMENT,
    email_id varchar(30) NOT NULL,
    PRIMARY KEY (id)
)";
executeQuery($con, $sql, "Creating New Table 'EMAILS' successfully", "Error creating Table");

//creating table uagents
$sql = "CREATE TABLE security.uagents (
    id int(3) NOT NULL AUTO_INCREMENT,
    uagent varchar(256) NOT NULL,
    ip_address varchar(35) NOT NULL,
    username varchar(20) NOT NULL,
    PRIMARY KEY (id)
)";
executeQuery($con, $sql, "Creating New Table 'UAGENTS' successfully", "Error creating Table");

//creating table referers
$sql = "CREATE TABLE security.referers (
    id int(3) NOT NULL AUTO_INCREMENT,
    referer varchar(256) NOT NULL,
    ip_address varchar(35) NOT NULL,
    PRIMARY KEY (id)
)";
executeQuery($con, $sql, "Creating New Table 'REFERERS' successfully", "Error creating Table");

//inserting data
$sql = "INSERT INTO security.users (id, username, password) VALUES 
    ('1', 'Dumb', 'Dumb'), 
    ('2', 'Angelina', 'I-kill-you'), 
    ('3', 'Dummy', 'p@ssword'), 
    ('4', 'secure', 'crappy'), 
    ('5', 'stupid', 'stupidity'), 
    ('6', 'superman', 'genious'), 
    ('7', 'batman', 'mob!le'), 
    ('8', 'admin', 'admin'), 
    ('9', 'admin1', 'admin1'), 
    ('10', 'admin2', 'admin2'), 
    ('11', 'admin3', 'admin3'), 
    ('12', 'dhakkan', 'dumbo'), 
    ('14', 'admin4', 'admin4')";
executeQuery($con, $sql, "Inserted data correctly into table 'USERS'", "Error inserting data");

//inserting data
$sql = "INSERT INTO `security`.`emails` (id, email_id) VALUES 
    ('1', 'Dumb@dhakkan.com'), 
    ('2', 'Angel@iloveu.com'), 
    ('3', 'Dummy@dhakkan.local'), 
    ('4', 'secure@dhakkan.local'), 
    ('5', 'stupid@dhakkan.local'), 
    ('6', 'superman@dhakkan.local'), 
    ('7', 'batman@dhakkan.local'), 
    ('8', 'admin@dhakkan.com')";
executeQuery($con, $sql, "Inserted data correctly into table 'EMAILS'", "Error inserting data");

// Close the connection
$con->close();

echo "<br><div style='color: #00FF00; font-size: 18px; text-align: center; padding: 20px; border: 2px solid #00FF00; margin: 20px 0;'>";
echo "✓ SECURITY DATABASE SETUP COMPLETED SUCCESSFULLY!";
echo "</div>";

//including the Challenges DB creation file.
include("../sql-connections/setup-db-challenge.php");
?>

        </font>
    </div>
</div>
</body>
</html>
