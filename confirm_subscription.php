<html>

<body>

<?php
$email = $_GET["email"];
$code = $_GET["code"];
$output = exec(escapeshellcmd("./mail.py confirm $email $code 2>&1"));
echo "$output";
?>

</body>

</html>
