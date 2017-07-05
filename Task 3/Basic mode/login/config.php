<?php
	define('DB_SERVER', 'localhost');
	define('DB_USERNAME', 'root');
	define('DB_PASSWORD', 'password');
	define('DB_DATABASE', 'Delta_Task_3');
	$conn = new mysqli(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE,9000);
	if(  $conn->connect_error ) {
		die('Could not connect: ' . $conn->connect_error);
	}
?>
