<?php
$output = exec(escapeshellcmd("./light.py add"));
echo "$output";
if ($output == "Slukking registrert.") {
	exec("python3 light.py notify > /dev/null 2>&1 &"); # mail in background
}
?>
