<?php
$time = $_POST["time"];
$output = exec(escapeshellcmd("./light.py add $time 2>&1"));
echo "$output";
?>
