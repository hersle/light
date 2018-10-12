<?php
$email = $_POST["email"];
$output = exec(escapeshellcmd("./light.py subscribe $email 2>&1"));
echo "$output";
?>
