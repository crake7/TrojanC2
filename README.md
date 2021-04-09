<h1 align="center"> Trojan.C2 🐎</h1>
<h4 align="center">Trojan Command and Control (C2) Framework uses a Github account to control, update, and receive data from your implants while remaining stealthy.</h4>

<p align="center">
  <a href="#How-to">How-to</a> •
  <a href="#Modules">Modules</a> •
  <a href="#Config">Config</a> •
  <a href="#Data">Data</a>
</p>

___

<h5>Why to use Github to build and deploy a trojan framework using Python?</h5>
Because you can use Python's native library import mechanism to deploy new functionality on your trojans. This means you can automatically update your implants, and any dependant libraries, directly from your repo.
In addition, your traffic to GitHub will be encrypted over SSL; several entreprises already use Github for their own work, so your traffic can be completely invisible to their blue teams. 

## How-to

1. Create a private repository.
2. Create a personal access token (PAT), instructions [here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line/)
3. Add the token's filename to the .gitignore file.
4. Tweak the functionality of your trojan using the modules and config folders.
5. Compile the trojan to run in the victim's OS.
6. Send it and enjoy!

<p>Optional: Add functionality by modifying the Modules and Config folders.</p>

## Modules

💪 The muscles of your Trojans.💪 <br />

<table>
<thead>
<tr>
<th>Module</th>
<th>Functionality</th>
</tr>
</thead>
<tbody>
<tr>
<td>Dirlister</td>
<td>Retrieves a list of folders/files in the current directory</td>
</tr>
<tr>
<td>Environment</td>
<td>Retrieves a list of the user's environmental variables. </td>
</tr>
<tr>
<td>Key Logger</td>
<td>Prints out PID, process name, window name and keystrokes of user.</td>
</tr>
<tr>  
<td>Screenshooter</td>
<td>Takes a screenshot of user's desktop. </td>
</tr>
</tbody>
</table>
 <br />
<p>To expand functionality and update your trojan remotely, write the necesary code in this folder. </p>
<p>Recommended usage: 
Each module you add should expose a "run(**args)" function that takes a variable number of arguments. 
This enables to load each module in the same fashion, but also allows you to customize the configuration
files to pass different arguments to the modules. </p>

<h6> Tip: To assess your modules, push them to GitHub and enable them in a configuration file fror your local testing version of the Trojan.</h6> 

## Config

🧠 The brains of your Trojans. 🧠  <br />
This is where you tell each trojan which actions to perform and the modules required to do so:<br />

1. Add a new JSON file following the structure of 'test.json'.
2. Name the file with a unique ID depending on its functionality. 
3. Modify the *horsy.py* file by removing the 'test' file and adding the one you have created. 

<br />
Each trojan should also have a unique ID. This help when sorting retrieved data based on the ID and provides modular
control of your trojans. 

## Data

Data path where the trojan will write its output files directly. 

<br>

### .gitignore

This file should have the filename of your PAT(personal access token). Give the token read and write permissions.
Beware that is you forget to do this step, you will end up posting your token to your repository. 

<h6> Tip: Create several different tokens for different trojans so you can control what each trojan can access in your repository. That way, if victims catch your trojan, they can’t come along and delete all of your retrieved data.</h6> 
