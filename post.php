<?php
$output = exec(escapeshellcmd("./light.py add 2>&1"));
echo "$output";
?>
