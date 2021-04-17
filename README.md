<h1 align="center"> Trojan.C2 🐎</h1>
<h4 align="center">Trojan Command and Control (C2) Framework uses a Github account to control, update, and receive data from your implants while remaining stealthy.</h4>

<p align="center">
  <a href="#How-to">How to</a> •
  <a href="#Modules">Modules</a> •
  <a href="#Config">Config</a> •
  <a href="#Data">Data</a> •
  <a href="#Important">Important!</a>
  <a href="#Credits">Credits</a>
</p>

___

<h5>Why to use Github to build and deploy a trojan using Python?</h5>
First, because your traffic to GitHub will be encrypted over SSL. Several entreprises already use Github for their own work, so your traffic can be completely invisible to their blue teams. 
In addition, you can use Python's native library import to deploy new functionality on your trojans - this means you can automatically update your implants, and any dependant libraries, directly from your repo.

## How-to

1. Create a private repository.
2. Create a personal access token (PAT), instructions [here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line/)
3. Add the token's filename to the .gitignore file.
4. Tweak the functionality of your trojan using the modules and config folders.
5. Compile the trojan to run in the victim's OS.
6. Send it and enjoy!

<p>Optional: Add functionality by modifying the Modules and Config folders.</p>

## Modules 💪 The muscles of your Trojans.💪 

<p align="center">💪 The muscles of your Trojans.💪 </p> <br />

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
<td>Retrieves a list of folders & files in the target's current directory</td>
</tr>
<tr>
<td>Environment</td>
<td>Retrieves a list of the target's environmental variables. </td>
</tr>
<tr>
<td>Key Logger</td>
<td>Prints out PID, process name, window name and keystrokes of target.</td>
</tr>
<tr>  
<td>Screenshooter</td>
<td>Takes a screenshot of target's desktop. </td>
</tr>
<tr>  
<td>Shellcode</td>
<td>Connects to your remote web server and executes your shellcode directly into the target's memory.</td>
</tr>
</tbody>
</table>

* To expand functionality and update your trojan remotely, write the necesary code in this folder.
* Recommended usage: 
  Each module you add should expose a `run(**args)` function that takes a variable number of arguments. 
This enables to load each module in the same fashion, but also allows you to customize the configuration
files to pass different arguments to the modules.

<h6> Tip: To assess your modules, push them to GitHub and enable them in a configuration file fror your local testing version of the Trojan.</h6> 

## Config

<p align="center">🧠 The brains of your Trojans. 🧠 </p> <br />

This is where you tell each trojan which actions to perform and the modules required to do so:
  1. Add a new JSON file following the structure of `test.json`.
  2. Name the file with a unique ID depending on its functionality. 
  3. Modify the `horsy.py` file by removing the filename 'test' and add the name of your file. 

* Each trojan should also have a unique ID. This helps when sorting retrieved data based on the ID and provides modular
control of your trojans. 

## Data

* Data path where the trojan will write its output files directly. 

<br>

## Important


`.gitignore` This file should have the filename of your PAT(personal access token). Give the token read and write permissions. Beware that is you forget to do this step, you will end up **posting your token to your repository**.

<h6> Tip: Create several different tokens for different trojans so you can control what each trojan can access in your repository. That way, if victims catch your trojan, they can’t come along and delete all of your retrieved data.</h6> 


## Credits

This repo was created while reading the amazing book: [Black Hat Python 2](https://www.amazon.com/Black-Hat-Python-2nd-Programming/dp/1718501129/ref=sr_1_3?dchild=1&keywords=black+hat+python+2&qid=1618619206&sr=8-3) by Justin Seitz and Tim Arnold. 

Writers and contributors take NO responsibility and/or liability for how you choose to use any of the source code available here. By using any of the files available in this repository, you understand that you are AGREEING TO USE AT YOUR OWN RISK. Once again, ALL files available here are for EDUCATION and/or RESEARCH purposes ONLY.
