<?php
$output = exec(escapeshellcmd("./light.py add 2>&1"));
echo "$output";
if ($output == "Registrert.") {
	exec("python3 light.py notify > /dev/null 2>&1 &"); # mail in background
}
?>
