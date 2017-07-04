<?php
	session_start(); 
?>
<html>
   
   <head>
      <title>Welcome </title>
   </head>
   
   <body>
      <h1>Welcome <?php echo $_SESSION['user_fullname']; ?></h1> 
	<h2>Your email address is <?php echo $_SESSION['user_email']; ?></h2><br/>       
	<h2><a href = "logout.php">Sign Out</a></h2>
   </body>
   
</html>
