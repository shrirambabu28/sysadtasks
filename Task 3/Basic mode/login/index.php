<html>
	<head>
		<title>LOGIN PAGE</title>
	</head>
	
	<body background="af.jpg">

<?php		

	include("config.php");
   	session_start();
   
  	if($_SERVER["REQUEST_METHOD"] == "POST") {
        // username and password recieved from the registration form.
      
      	$user = ($_POST['username']); 
	$pass = ($_POST['password']);
	$hsdpass = sha1($lpass);
      
      	$sql = "SELECT * FROM userTable WHERE userName = '$user' and password = '$hsdpass'";
      	$result = $conn->query($sql);
      
      	$count = $result->num_rows;
      
	if($count == 1) {
	$row = $result->fetch_assoc();
  
        $_SESSION['user_fullname'] = $row['full_name'];
	$_SESSION['user_email'] = $row['email'];
         
        header("location: welcome.php");
      }else {
         $error = "Your Login Name or Password is invalid";
      }
   }
?>
		

	<h1><center><font color="yellow">Login</font></center></h1>		
	<form align="center" autocomplete="off" method = "POST" action ="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
	<table align ="center">
            <tr>
	    <td>Username:</td>
	    <td>
	    <input type="text" placeholder="Username" name="username"></td></tr>
            <tr>
            <td>Password:</td>
            <td>
            <input type="password" placeholder="Password" name="password"></td></tr>
            <tr>				
	    <tr><td><input type="submit" value ="Submit"></td></tr>		
	</table>		
	</form>
	<br/>
	<?php echo $error; ?>
	</body>
</html>
