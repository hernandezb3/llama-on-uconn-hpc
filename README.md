# Llama on UConn High Performance Computing (HPC)
This repository (repo) is for running a Llama model from a Python script in UConn's HPC environment. Two approaches are included in the repo:

1. Ollama downloaded with Apptainer
2. Hugging Face

## Pre-Requisites
This README documents Approach #1 (above) and assumes the following:
- Device:
    - Mac Operating System (OS)
    - [VS Code](https://code.visualstudio.com) Interactive Development Environment (IDE)
- UConn Account:
    - UConn NetID and Password
    - [Cisco Duo](https://kb.uconn.edu/space/IKB/10789815076/Setting+up+a+Mobile+Phone+for+2FA) Two-Factor Authentication (2FA)
- HPC:
    - [UConn HPC Account](https://login.uconn.edu/cas/login?service=https%3A%2F%2Fhpc.uconn.edu%2Fwp-login.php%3Fprivacy%3D2%26redirect_to%3Dhttps%253A%252F%252Fhpc.uconn.edu%252Fstorrs%252Faccount-application%252F)
    - [Cisco AnyConnect]((https://kb.uconn.edu/space/IKB/10907091023/Set+Up+Cisco+AnyConnect+VPN)) Virtual Private Network (VPN)
    - [XQuartz](https://www.xquartz.org) Secure SHell (SSH) Client and X-Server
    - [Docker Account](https://www.docker.com)

## Connecting to UConn HPC
To connect to UConn HPC 

### Log in to HPC
From terminal run:
```
# ssh into hpc
ssh -Y netid@hpc2.storrs.hpc.uconn.edu

# check the node e.g., login
hostname
```
[add photo of the output?]

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

readme updated: March 26, 2025