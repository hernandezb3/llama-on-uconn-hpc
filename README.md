# Llama on UConn High Performance Computing (HPC)
This repository (repo) is for running Llama models from a Python script in UConn's HPC environment. Two approaches are included in the repo:

1. Ollama downloaded with Apptainer (classify_with_ollama.py)
2. Hugging Face (classify_with_hugging_face.py)

## Summary
This README documents how to use Approach #1 (above) to run a Python script which sends a prompt input and returns a response from a Llama model. 

Llama is a collection of open-source large language models (LLMs) developed by Meta (see more [here](https://www.llama.com)). The two approaches included in the repo are for running the models locally instead of using an API inference endpoint. Running the models locally is free and guarentees the inputs sent to the model won't be used by Meta for retraining current models or developing future models. 

Running these models can be resource intensive depending on the size of the model (i.e., number of parameters - 3B vs 70B) and the approach. Running the same sized model e.g., Llama 3.2 3B is faster using Ollama than Hugging Face.

## Pre-Requisites
This README assumes the following:
- Personal Device:
    - Mac Operating System (OS)
    - [VS Code](https://code.visualstudio.com) Interactive Development Environment (IDE)
- UConn Account:
    - UConn NetID and Password
    - [Cisco Duo](https://kb.uconn.edu/space/IKB/10789815076/Setting+up+a+Mobile+Phone+for+2FA) Two-Factor Authentication (2FA)
- HPC:
    - [UConn Storrs HPC Account](https://login.uconn.edu/cas/login?service=https%3A%2F%2Fhpc.uconn.edu%2Fwp-login.php%3Fprivacy%3D2%26redirect_to%3Dhttps%253A%252F%252Fhpc.uconn.edu%252Fstorrs%252Faccount-application%252F)
    - [Cisco AnyConnect](https://kb.uconn.edu/space/IKB/10907091023/Set+Up+Cisco+AnyConnect+VPN) Virtual Private Network (VPN)
    - [XQuartz](https://www.xquartz.org) Secure SHell (SSH) Client and X11 Window System
    - [FileZilla]() File Transfer Protocol (FTP)
    - [Docker Account](https://www.docker.com)

## Connect to UConn HPC
This section summarizes UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. Each subsection provides direction for how to install the pre-requisites. Each step (e.g., *__Step A__) assumes the pre-requisites are met.

### Connect to a VPN
The Cisco AnyConnect VPN allows active staff, faculty, and students acess to the UConn network. Computers connected to UConn-Secure WiFi or an on-campus ethernet port do not need to use a VPN. To access the UConn network off campus, install Cisco AnyConnect and follow the set-up instructions [here](https://kb.uconn.edu/space/IKB/10907091023/Set+Up+Cisco+AnyConnect+VPN) (also linked in the pre-requisites section).

* __Step A:__ Open the Cisco Secure Client application. You will be prompted to log in with your NetID and Password. 

### Enable Graphics Forwarding
Displaying program graphics, like a plot or graph output, requires an X11 Window System to enable graphics forwarding. Graphics forwarding is how graphics are sent from a remote host (i.e., the HPC cluster) to the local client (i.e., your computer). 

[XQuartz](https://www.xquartz.org) is the X11 Window System for MacOS. The X11 Window System requirements will vary by OS and by computer. Some Windows users may need to install [VcXsrv] (https://sourceforge.net/projects/vcxsrv/) while Linux users don't need to install an X11 Window System. For more information, see Step 3 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. 

### Transfer Files
FileZilla is a File Transfer Protocol (FTP) allowing files to be transferred between your computer and HPC over the internet. The Python script and the files it references need to be transferred to HPC. Note that since the transfer occurs over the internet, you need to be connected to the UConn network (see Connect to a VPN above). 

Following the steps [here](https://kb.uconn.edu/space/SH/26033783688/File+Transfer) download FileZilla

* __Step B:__ Open FileZilla and click the Site Manager icon to connect to HPC
* __Step C:__ Transfer these files to your HPC account: 
    - classify_with_ollama.py
    - test_ollama.py
    - requirements.txt
    - library
        - fit.py
        - secrets.py
        - start.py
    - data
        - test_prompt.csv
        - test_data.csv

### Login to HPC
Login to HPC uses a Secure Shell (SSH) protocol, a method for secure remote login between your computer and HPC. MacOS and Linux OS users can login to HPC using the default Terminal application. 

For Windows OS, [MobaXterm](https://mobaxterm.mobatek.net) is recommended by Storrs HPC Admins and this application jointly acts as an X11 Window System and SSH protocol and has a different process for logging in. For more information, see Step 3 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. 

* __Step D:__ Login to Storrs HPC from a MacOS computer by running the following in Terminal:
```
# login to hpc
# replace netid with your personal NetID
ssh -Y netid@hpc2.storrs.hpc.uconn.edu
```

Follow the prompts to enter your password and complete any 2FA authentication. When successfully logged in you'll be assigned to a login node on HPC. 
```
# check the node 
# hostname should return your assigned login node e.g., login4
hostname
```

### Start an interactive job
Meta recommends XX for running Llama 3.3

* __Step E:__ Request an interactive job by running the following in Terminal:
```
# srun = requests an interactive job
# -n = number of nodes (1)
# -t = time allocation (30 minutes)
# --mem = ram (64 GB)
# --pty = scripting language (bash)
# other : add link to UConn HPC resources
srun -n 1 -t 0:30:00 --mem=64G --pty bash
```
### Install packages
UConn uses Apptainer XX.XX.XX which has a dependency incompatible with dependencies for certain Python versions. 
Python 3.12.2
Some incompatable packages
```
module unload python
module unload gcc
module load apptainer
```
### build the container 
```
# build an apptainer container from the docker repository
apptainer build --force --docker-login --sandbox ollama/ docker://ollama/ollama:latest

```
### Start an Instance and Run Ollama
```
# apptainer = language
# instance start = command
# ollama/ = name of the sandbox to use
# ollama_instance = what to name the instance
apptainer instance start ollama/ ollama_instance
```

Can submit commands to run in the container or can enter into the container and then run commands. The difference is what the working directory is

This shells into the container and 
```
apptainer shell instance://ollama_instance
ollama serve

# to leave the instance
exit
```

# Log into the Node
In a new terminal window
```
# replace login5 with the specific login node
ssh -Y netid@login5.storrs.hpc.uconn.edu
```
### download the model
### run the script

README updated: March 26, 2025