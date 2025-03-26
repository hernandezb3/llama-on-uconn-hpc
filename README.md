# Llama on UConn High Performance Computing (HPC)
This repository (repo) is for running a Llama model from a Python script in UConn's HPC environment. Two approaches are included in the repo:

1. Ollama downloaded with Apptainer
2. Hugging Face

## Pre-Requisites
This README documents Approach #1 (above) and assumes the following:
- Personal Device:
    - Mac Operating System (OS)
    - [VS Code](https://code.visualstudio.com) Interactive Development Environment (IDE)
- UConn Account:
    - UConn NetID and Password
    - [Cisco Duo](https://kb.uconn.edu/space/IKB/10789815076/Setting+up+a+Mobile+Phone+for+2FA) Two-Factor Authentication (2FA)
- HPC:
    - [UConn Storrs HPC Account](https://login.uconn.edu/cas/login?service=https%3A%2F%2Fhpc.uconn.edu%2Fwp-login.php%3Fprivacy%3D2%26redirect_to%3Dhttps%253A%252F%252Fhpc.uconn.edu%252Fstorrs%252Faccount-application%252F)
    - [FileZilla]() 
    - [Cisco AnyConnect]((https://kb.uconn.edu/space/IKB/10907091023/Set+Up+Cisco+AnyConnect+VPN)) Virtual Private Network (VPN)
    - [XQuartz](https://www.xquartz.org) Secure SHell (SSH) Client and X-Server
    - [Docker Account](https://www.docker.com)

## Connecting to UConn HPC
This section summarizes UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide.

### Connect to VPN
The Cisco AnyConnect VPN allows active staff, faculty, and students acess to the UConn network. Computers connected to UConn-Secure WiFi or an on-campus ethernet port do not need to use a VPN. To access the UConn network off campus, install Cisco AnyConnect and follow the set-up instructions [here](https://kb.uconn.edu/space/IKB/10907091023/Set+Up+Cisco+AnyConnect+VPN) (also linked in the pre-requisites section).

Open the Cisco Secure Client application. You will be prompted to log in with your NetID and Password. 

### Enable Graphics Forwarding
Displaying program graphics, like a plot or graph output, requires an X11 Window System to enable graphics forwarding. Graphics forwarding is how graphics are sent from a remote host (i.e., the HPC cluster) to the local client (i.e., your computer). [XQuartz](https://www.xquartz.org) is the X11 Window System for MacOS. The X11 Window System requirements will vary by OS and by computer. Some Windows users may need to install [VcXsrv] (https://sourceforge.net/projects/vcxsrv/) while Linux users don't need to install an X11 Window System. For more information, see Step 3 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. 

### Login to HPC
Login to HPC uses a Secure Shell (SSH) protocol, a method for secure remote login between your computer and HPC. MacOS and Linux OS users can login to HPC using the default Terminal application. For Windows OS, [MobaXterm](https://mobaxterm.mobatek.net) is recommended by Storrs HPC Admins and this application jointly acts as an X11 Window System and SSH protocol. For more information, see Step 3 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. 

To login to Storrs HPC from a MacOS computer, run the following in Terminal:
```
# login to hpc
# replace netid with your personal NetID
ssh -Y netid@hpc2.storrs.hpc.uconn.edu
```

Follow the prompts to enter your password and complete any 2FA authorization. When successfully logged in you'll be assigned to a login node on HPC. 
```
# check the node e.g., login
hostname
```


### Start an interactive job
Meta recommends XX for running Llama 3.3
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