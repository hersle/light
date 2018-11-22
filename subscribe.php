<?php
$email = $_POST["email"];
$output = exec(escapeshellcmd("./mail.py subscribe $email 2>&1"));
echo "$output";
?>
