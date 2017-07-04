<html>
<head>
	<title>REGISTER FORM</title>
	<style>
		.error {color: green;}
	</style>
</head>

<body background="bag.jpg">
	
		<?php		
		<p id="demo"></p>
		<p><b>Note: </b>If port number is default, most browers will display 0 or nothing.</p>
		<script>
		document.getElementById("demo").innerHTML =
		"The port number of the current page is:" +window.location.port;</script>
		
		function test_input($data) {
			$data = trim($data);
			$data = stripslashes($data);
			$data = htmlspecialchars($data);
			return $data;
		}
		
			$usererr = $passerr = $nameerr = $emailerr = "";
			$user = $pass = $name = $email = "";
			$exec = TRUE ;
			if ($_SERVER["REQUEST_METHOD"] == "POST"){
			if (empty($_POST["user"])) {
				$usererr = "Username is required";
				$exec = FALSE;
  			} 
			else {
				$user = test_input($_POST["user"]);
				if (strlen($user) < 5){
			   		$usererr = "Username should be between 5 to 10 characters only!";
					$exec = FALSE;				
				}
				elseif(strlen($user) > 10){
					$usererr = "Username should be between 5 to 10 characters only!";
					$exec = FALSE;
				}			
			}
  
			if (empty($_POST["pass"])) {
				$passerr = "Password is required!";
				$exec = FALSE;
			} 
			else {
				$pass = test_input($_POST["pass"]);
			
					if(!preg_match('/^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{5,}$/', $pass)){
						$passerr="Password should be at least 5 characters long with one letter, digit and special character!";
						$exec = FALSE;
					}
				$pass = sha1($pass);
			}
    
			if (empty($_POST["name"])) {
				$nameerr = "Full name is required!";
				$exec = FALSE;
			} 
			else {
				$name = test_input($_POST["name"]);
			}
			if (empty($_POST["email"])) {
				$emailerr = "Valid Email is required!";
				$exec = FALSE;
			} 
			else {
				$email = test_input($_POST["email"]);
				if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
					$emailerr = "Invalid email format";
					$exec = FALSE;
				}
			}
			if($exec)
			{
				define('DB_SERVER', 'localhost');
   				define('DB_USERNAME', 'root');
   				define('DB_PASSWORD', 'password');
   				define('DB_DATABASE', 'Delta_Task_3');
   				$conn = new mysqli(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE, 9000);
           			
				if(  $conn->connect_error ) {
               				die('Could not connect: ' . $conn->connect_error);
            			}
				
   
				$val = $conn->query($sql);
				if($val == FALSE){
					 $sql = 'CREATE TABLE userTable( '.
      						'id INT NOT NULL AUTO_INCREMENT, '.
      						'userName VARCHAR(10) NOT NULL, '.
      						'password  VARCHAR(50) NOT NULL, '.
      						'full_name VARCHAR(100) NOT NULL, '.
						'email VARCHAR(50) NOT NULL, '.
						'primary key ( id ));';
  	
   					$retval = $conn->query($sql);
   
   					if( $retval ) {
      						echo "Created table!";
					}
				}
				
				$sql = "INSERT INTO userTable ". "(userName,password, full_name, 
               				email) ". "VALUES('$user','$pass','$name', '$email')";
				$retval = $conn->query($sql);
            
            if(! $retval ) {
               die('Could not enter data: ' . $conn->error);
            }
            
    
				$conn->close();
			}}
			
		
	?>
		<h1 align="center"><font color="red"><strong>WELCOME TO THE DELTA REGISTRATION PAGE</strong></font></h1>
		<p><span class="error">* required field.</span></p>
		<form autocomplete="off" method = "POST" action = "<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
		<table align="center">
		<tr><td>Username:</td> <td><input type="text" name="user" <?php echo $username;?>/>
		<span class="error">* <?php echo $usererr;?></span><br/></td></tr>
		<tr><td>Password:</td> <td><input type="password" name="pass"<?php echo $pwd;?> />
		<span class="error">* <?php echo $passerr;?></span><br/></td></tr>
		<tr><td>Full Name:</td> <td><input type="text" name="name"<?php echo $fullname;?> />
		<span class="error">* <?php echo $nameerr;?></span><br/></td></tr>
		<tr><td>E-mail address:</td> <td><input type="text" name="email" <?php echo $email;?>/>
		<span class="error">* <?php echo $emailerr;?></span><br/></td></tr>
		<tr><td><input type="submit" value="Submit"></td></tr>		
		</table></form>
	

</body>

</html>
