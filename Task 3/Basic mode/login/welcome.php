<?php
	session_start(); 
?>
<html>
   
   <head>
      <title>Welcome </title>
   </head>
   
   <body>
      <h4>Welcome <?php echo $_SESSION['user_fullname']; ?></h4> 
	<h4>Your email address is <?php echo $_SESSION['user_email']; ?></h4><br/>       
	<h5><a href = "logout.php">Sign Out</a></h5>
   </body>
   
</html>
