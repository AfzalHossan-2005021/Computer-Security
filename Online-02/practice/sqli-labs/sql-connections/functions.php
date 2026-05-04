<?php
//including the Mysql connect parameters.
include("../sql-connections/db-creds.inc");

#################################
#  Especially for challenges    # 
#################################

// Function to create MySQLi connection
function createConnection($host, $dbuser, $dbpass, $dbname = null) {
    $conn = new mysqli($host, $dbuser, $dbpass, $dbname);
    
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    
    return $conn;
}

//Creating dynamic string for creating dynamic names
function num_gen($string_length, $characters)
{
	$string = '';
 	for ($i = 0; $i < $string_length; $i++) 
	{
      		$string .= $characters[rand(0, strlen($characters) - 1)];
 	}
	return $string;
}

$characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';   //charset for dynamic generation of strings
// Generating a dynamic alfanumeric Table name with each purge.
$table = num_gen(10, $characters) ;

// Generating Secret key column.
$secret_key = "secret_".num_gen(4, $characters);

//retrieve dynamic table name from database.
function table_name()
{
	include '../sql-connections/db-creds.inc';
	$conn = createConnection($host, $dbuser, $dbpass);
	
	$sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='$dbname1'";
	$result = $conn->query($sql);
	
	if (!$result) {
		die("error in function table_name(): " . $conn->error);
	}
	
	$row = $result->fetch_array();
	if (!$row) {
		die("error in function table_name() output: " . $conn->error);
	}
	
	$conn->close();
	return $row[0];
}

//retrieve Column name from database.
function column_name($idee)
{
	include '../sql-connections/db-creds.inc';
	$conn = createConnection($host, $dbuser, $dbpass);
	
	$table = table_name();
	$sql = "SELECT column_name FROM information_schema.columns WHERE table_name='$table' LIMIT $idee,1";
	$result = $conn->query($sql);
	
	if (!$result) {
		die("error in function column_name(): " . $conn->error);
	}
	
	$row = $result->fetch_array();
	if (!$row) {
		die("error in function column_name() result: " . $conn->error);
	}
	
	$conn->close();
	return $row[0];
}

//retrieve data from table.
function data($tab, $col)
{
	include '../sql-connections/db-creds.inc';
	$conn = createConnection($host, $dbuser, $dbpass);
	
	$sql = "SELECT $col FROM $tab WHERE id=1";
	$result = $conn->query($sql);
	
	if (!$result) {
		die("error in function data(): " . $conn->error);
	}
	
	$row = $result->fetch_array();
	if (!$row) {
		die("error in function data() result: " . $conn->error);
	}
	
	$conn->close();
	return $row[0];
}

//Updating the counter for Attempts at solving problem.
function next_tryy()
{
	$table = table_name();
	//including the Mysql connect parameters.
	include '../sql-connections/db-creds.inc';
	$conn = createConnection($host, $dbuser, $dbpass);
	
	$sql = "UPDATE $table SET tryy=tryy+1 WHERE id=1";
	if (!$conn->query($sql)) {
		die("error in function next_tryy(): " . $conn->error);
	}
	
	$conn->close();
}

function view_attempts()
{
	include '../sql-connections/db-creds.inc';
	$conn = createConnection($host, $dbuser, $dbpass);
	
	$table = table_name();
	$sql = "SELECT tryy FROM $table WHERE id=1";
	$result = $conn->query($sql);
	
	if (!$result) {
		die("error in function view_attempts(): " . $conn->error);
	}
	
	$row = $result->fetch_array();
	if (!$row) {
		die("error in function view_attempts() result: " . $conn->error);
	}
	
	$conn->close();
	return $row[0];	
}

?>
