# TrojanC2
Trojan framework to control, update, and receive data from your implants.


<h4>Modules</h4>

This is where you add additional functionality to your trojans.
Each module you add should expose a "run(**args)" function that takes a varialbe number of arguments. 
This enables to load each module in the same fashion, but also allows you to customize the configuration
files to pass different arguments to the modules. 

Tip: 
To assess your modules, push them to GitHub and enable them in a configuration file fror your local testing
version of the Trojan. 

<h4>Config</h4>

This folder holds unique config files for each trojan: this is where you tell each trojan which actions to perform and the modules required to do so.\n
Each trojan should have a unique ID. This help when sorting retrieved data based on the ID and provides modular
control of your trojans. 

<h4>.gitignore</h4>

This file should have the filename of your PAT(personal access token). Give the token read and write permissions.
To create a token and add it to a file, check: https://help.github.com/en/github/authenticating-to-github/
creating-a-personal-access-token-for-the-command-line/ 
