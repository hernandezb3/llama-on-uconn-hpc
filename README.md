# Running Llama on UConn High Performance Computing (HPC)
This repository (repo) is for running Llama models from a Python script in UConn's HPC environment. Two approaches are included in the repo:

1. Ollama downloaded with Apptainer (classify_with_ollama.py)
2. Hugging Face (classify_with_hugging_face.py)

## Summary
This README documents how to use Approach #1 (above) to run a Python script which inputs a prompt and outputs a response from a Llama model. 

Llama is a collection of open-source large language models (LLMs) developed by Meta (see more [here](https://www.llama.com)). The two approaches included in the repo are for running the models locally instead of using an API inference endpoint. Running the models locally is free and ensures the input data remain private. 

Running these models can be resource intensive depending on the size of the model (i.e., number of parameters - 3B vs 70B) and the approach. Returning output from the same sized model e.g., Llama 3.2 3B is faster using Ollama than Hugging Face.

The ultimate goal of this repo is to use Llama 3.3 70B for Project CRISP which asks the model to classify journal entries across various psychological characteristics e.g., meaning making. The README will demonstrate a classification task with a smaller model, Llama 3.2 3B and demo prompts. The demo (classify_with_ollama.py) prompts the model to classify Goodreads reviews as either a good or bad review. These data are sourced from [Kaggle.com](https://www.kaggle.com/competitions/goodreads-books-reviews-290312/data). 

Before running the demo at full scale, test_ollama.py can be used to ensure core functions of the demo, mainly testing file paths and that the model can take an input and generate an output within the HPC environment. 

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
This section summarizes UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. Each subsection provides direction for how to install the pre-requisites. Each step (e.g., __Step A__) assumes the pre-requisites are met.

### Connect to a VPN
The Cisco AnyConnect VPN allows active staff, faculty, and students access to the UConn network. Computers connected to UConn-Secure WiFi or an on-campus ethernet port do not need to use a VPN. To access the UConn network off campus, install Cisco AnyConnect and follow the set-up instructions [here](https://kb.uconn.edu/space/IKB/10907091023/Set+Up+Cisco+AnyConnect+VPN) (also linked in the pre-requisites section).

* __Step A:__ Open the Cisco Secure Client application. You will be prompted to log in with your NetID and Password. 

### Enable Graphics Forwarding
Displaying program graphics, like rendering a plot, requires an X11 Window System to enable graphics forwarding. Graphics forwarding is how graphics are sent from a remote host (i.e., the HPC cluster) to the local client (i.e., your computer). 

[XQuartz](https://www.xquartz.org) is the X11 Window System for MacOS. The X11 Window System requirements will vary by OS and by computer. Some Windows users may need to install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) while Linux users don't need to install an X11 Window System. For more information, see Step 3 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. 

### Login to HPC
Login to HPC uses a Secure Shell (SSH) protocol, a method for secure remote login between your computer and HPC. MacOS and Linux OS users can login to HPC using the default Terminal application. 

For Windows OS, [MobaXterm](https://mobaxterm.mobatek.net) is recommended by Storrs HPC Admins and this application jointly acts as an X11 Window System and SSH protocol and has a different process for logging in. For more information, see Step 3 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. 

* __Step B:__ Login to Storrs HPC from a MacOS computer by running the following in Terminal:
```
# login to hpc
# replace netid with your personal UConn NetID
ssh -Y netid@hpc2.storrs.hpc.uconn.edu
```

Follow the prompts to enter your password and complete any 2FA authentication. When successfully logged in you'll be assigned to a login node on HPC. 
```
# check the node 
# hostname should return your assigned login node e.g., login4
hostname
```

### Transfer Files
FileZilla is a File Transfer Protocol (FTP) allowing files to be transferred between your computer and HPC over the internet. The Python script and the files it references need to be transferred to HPC. Note that since the transfer occurs over the internet, you need to be connected to the UConn network (see the Connect to a VPN section above). 

To install and connect FileZilla to your HPC account, follow the steps from UConn Storrs HPC's [File Tranfer](https://kb.uconn.edu/space/SH/26033783688/File+Transfer) document, under the Data Storage Guide dropdown.

* __Step C:__ Open FileZilla and click the Site Manager icon to connect to HPC
* __Step D:__ Transfer these files to your HPC account: 
    - classify_with_ollama.py
    - test_ollama.py
    - requirements.txt
    - library
        - fit.py
        - secrets.py
        - start.py
    - data
        - demo_prompts.csv
        - goodreads_20.csv

To check that the files loaded successfully, run the following in Terminal:
```
# check files loaded successfully
ls
```
### Start an Interactive Job
There are two ways to request resources from UConn Storrs HPC, an interactive job (srun) or a scheduled job (sbatch). For more information, see Step 5 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. Sites like [apx.com](https://apxml.com/posts/ultimate-system-requirements-llama-3-models) and [nodeshift.com](https://nodeshift.com/blog/how-to-install-llama-3-3-70b-instruct-locally) can be used to determine what resources to request from HPC when submitting the job request. Note: Llama 3.2 3B requires lighter hardware than Llama 3.3 70B.

See the [SLURM Guide](https://kb.uconn.edu/space/SH/26032963685/SLURM+Guide) for more examples of how to request jobs on HPC.

* __Step E:__ Start an interactive job by running the following in Terminal:
```
# srun = requests an interactive job
# -n = number of nodes (1)
# -t = time allocation (30 minutes)
# --mem = ram (8 GB)
# --pty = scripting language (bash)
srun -n 1 -t 0:30:00 --mem=8G --pty bash

# check what node you are on:
hostname
```
### Load Modules
Some software like Python and Apptainer are available to use on UConn Storrs HPC. Run the following to see what software are available:
```
# list modules
module avail

# check which versions of python are available
module avail python
```

One option for using software not available as a module is with a container. The next section will discuss containers. In this section, we will load the necessary software which includes Python for running the script classify_with_ollama.py script and Apptainer for running the Ollama application. 

UConn Storrs HPC uses Apptainer XX.XX.XX which has a dependency (gcc) incompatible with the default Python version. So we will first unload the conflicting modules and then load Apptainer and a compatible version of Python.

* __Step F:__ Load modules by running the following in Terminal:
```
# remove incompatible packages
module unload python
module unload gcc
# add apptainer and python
module load apptainer
module load python/3.12.2
```
### Build the Ollama Container 
A container is an isolated environment to run an application. Within the container is anything necessary e.g., files, packages, etc. run the application. A container is built from an image, which contains the instructions for how to build the envrionment. The image can be thought of as a blueprint or manifest for building a container. 

Images can be manually built, but Docker, a containerization service, contains a library of prebuilt images. Apptainer, the container system used by UConn Storrs HPC, is compatible with Docker, so with Apptainer we can pull images from the Docker library to build containers. To run Ollama on UConn Storrs HPC, we will the Ollama image from the Docker library to build a container.

* __Step G:__ Build the Ollama container by running the following in Terminal:
```
# build an apptainer container from the docker repository
# apptainer = application
# build = create a container
# --force = overwrites any docker images under the same name
# --docker-login = connects the image to your docker account
# --sandbox = builds the container in a directory instead of as a .SIF file
# ollama/ = the custom name of the directory
# docker://ollama/ollama:latest = path to the docker image to use
apptainer build --force --docker-login --sandbox ollama/ docker://ollama/ollama:latest
```
Login to your Docker account to connect the image to your account. This allows you to use Docker Hub track running containers connected to that image.

### Start an Instance and Run Ollama
Once the container is built, the container needs to be "turned on." Starting the container as an instance (instance start vs apptainer run) runs the container in the background. After the container is started, we shell into it and start the Ollama application. 

Instance start is analagous to turning on the computer and ollama serve to opening the Ollama app.

* __Step H:__ Start the instance by running the following in Terminal:
```
# apptainer = application
# instance start = start running the container
# ollama/ = name of the container (i.e., the custom name of the directory from the last step)
# ollama_instance = a custom name for the instance
apptainer instance start ollama/ ollama_instance
```

* __Step I:__ Shell into the instance and run Ollama by running the following in Terminal:
```
# apptainer = application
# shell = enter the container
# instance://ollama_instance = name of the instance to shell into
apptainer shell instance://ollama_instance

# ollama = application
# serve = start ollama
ollama serve
```
Running Ollama will take up the Terminal window. We'll complete the remainder of the demo in a new Terminal window.

### Login to the Node
In a new terminal window, we will login to the same node Ollama is running on. 

* __Step J:__ Login to UConn Storrs HPC by running the following in Terminal:
```
# replace netid with your personal UConn NetID
# replace hpc2 with the specific login node assigned
# this is output of hostname in Step B
ssh -Y netid@hpc2.storrs.hpc.uconn.edu
```

* __Step K:__ Login to the running session by running the following in Terminal:
```
# replace node with the interactive job node
# this is output of hostname in Step E
ssh node
```

* __Step L:__ Load modules by running the following in Terminal:
```
# remove incompatible packages
module unload python
module unload gcc
# add apptainer and python
module load apptainer
module load python/3.12.2
```

### Download Llama 3.2 3B
The Ollama application is running in the container on the other Terminal window. 

In the current terminal window, we'll enter the container and download the model we want to use i.e., the one referenced in the classify_with_ollama.py Python script.

* __Step M:__ Load modules by running the following in Terminal:
```
# apptainer = application
# shell = enter the container
# instance://ollama_instance = name of the instance to shell into
apptainer shell instance://ollama_instance

# see which model's have been downloaded to the container
ollama list

# pull the Llama 3.2 model (by default this pulls the 3B param model)
ollama pull llama3.2 # pull a new model

# exit out of the container
# i.e., go back to the hpc environment
exit
```

### Install Python Packages
Now that Ollama is running 
```
# Step N: install python packages
pip3 install -r requirements.txt
```

### Run Python Script

```
# Step O: run the script
python3 pilot_classifications_llama_ollama_hpc.py
```
### Log out of instances

```
exit
```


README updated: March 26, 2025