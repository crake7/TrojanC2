# TrojanC2
Trojan framework to control, update, and receive data from your implants.


<h4>Modules</h4>

This is where you add additional functionality to your trojans.
Each module you add should expose a run(**args) function that takes a varialbe number of arguments. 
This enables to load each module in the same fashion, but also allows you to customize the configuration
files to pass different arguments to the modules. 

