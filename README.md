# Llama on UConn Storrs HPC
This repository (repo) is for running Llama models from a Python script in UConn's High Performance Computing (HPC) environment. Two approaches are included in the repo:

1. Ollama downloaded with Apptainer (classify_with_ollama.py)
2. Hugging Face (classify_with_hugging_face.py)

## CRISP Project Summary
The ultimate goal of this repo is to use Approach #1 (above) to prompt Llama 3.3 70B with Project CRISP data, asking the model to classify text across various psychological characteristics e.g., meaning making. 

<p align="center">
<img src="readme_images/crisp.png" width="650">
</p>

Included in the repo is a demo, showing how to use Llama models for a similar task within the UConn Storrs HPC environment.

Llama is a collection of open-source large language models (LLMs) developed by Meta (see more [here](https://www.llama.com)). The two approaches included in the repo are for running the models locally instead of using an API inference endpoint. Running the models locally is free and ensures the input data are contained locally. 

Running these models can be resource intensive depending on the size of the model (i.e., number of parameters - 3B vs 70B) and the approach. Returning output from the same sized model e.g., Llama 3.2 3B is faster using Ollama than Hugging Face. While a personal computer might be sufficient for running smaller models, HPC can be useful for running larger models like Llama 3.3 70B. 

## Goodreads Demo Summary
The demo (classify_with_ollama.py) prompts Llama 3.2 3B to classify a random sample of 20 Goodreads book reviews into a 0-5 rating. 

The information input to the model are a combination of a prompt, i.e., the task the model is being asked to perform, and the case, i.e., the scenario the model should consider when performing the task. In the demo, the prompt asks the model to assign a rating on a scale from 0 = bad to 5 = good and the case is a book review. 

<p align="center">
<img src="readme_images/model_interaction.png" width="650">
</p>

The book reviews are sourced from train.csv on [Kaggle.com](https://www.kaggle.com/competitions/goodreads-books-reviews-290312/data). A random sample of 20 reviews was generated using goodreads_sample.py which creates the sample in goodreads_20.csv. There are two variables of interest in goodreads_20.csv: 
- rating: a rating of the book on a 0 to 5 scale
- review_text: the text of the book review

![alt text](readme_images/goodreads_preview.png)

The each row in review_text is a case that is paired with the prompt and input to the model. For each row, Llama will output a rating based on the input, saved to the dataframe as llama_rating. The rating variable is the "true" rating the reviewer posted to Goodreads with their review_text. 

We'll evaluate model performance with the Root Mean Square Error (RMSE) estimating the average difference between the "true" Goodreads rating and Llama's rating. 
```math
\mathop{\mathrm{RMSE}} = \sqrt{ \frac{\sum_{i=1}^{N} (Goodreads_i - Llama_i)^2}{N}  }
```

## Start the Demo
Logging into HPC for the first time requires some initial set up, listed in the Context and Pre-Requisites section. Each subsection of the demo assumes this is the first time connecting to HPC and using containers. Steps A-Q call attention to the steps for running the demo after the inital set up. These steps are also compiled in steps_A-Q.sh in the Resources folder. 
<br/><br/>
Two seperate Terminal windows are used in the demo. The figure below provides a high level overview of Steps A-Q and deliniates the steps performed on each Terminal window. Steps on the left and in green are performed in Terminal Window 1 and steps on the right in blue are perfomed in Terminal Window 2.
<br/><br/>
<p align="center">
<img src="readme_images/steps_A-Q.png" height="650">
</p>

Final thoughts: 
- This demo is not a replacement for the UConn Storrs HPC documentation, but provides an applied task to navigate it with. 
- If you are new to HPC or containers, I'd recommend testing small and building upon these tests. I've included scripts in the Resources folder to support this. For example:
    - __Are you new to HPC?__ test_ollama.py contains an even smaller scale demo testing core functionality of running a Llama model on HPC. It prompts the model with, "Hi, how are you?" and outputs a response.
    - __Are you new to Docker?__ docker.sh contains Terminal commands to build an Ollama Docker container using Docker commands. This allows you to build the container locally before using Apptainer on HPC. 

### Context and Pre-Requisites
The demo is documented under the following assumptions:
- First time using HPC
- Off campus
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


### Connect to Wifi
Users need to be connected to UConn-Secure WiFi to access HPC. Those on campus can connect to UConn-Secure WIFi or an on-campus ethernet port. 

Accessing the UConn network off campus requires a VPN. Install Cisco AnyConnect and follow the set-up instructions [here](https://kb.uconn.edu/space/IKB/10907091023/Set+Up+Cisco+AnyConnect+VPN) (also linked in the pre-requisites section).

* __Step A:__ Open the Cisco Secure Client application and log in with your NetID and Password. 

### Enable Graphics Forwarding
Displaying program graphics, like rendering a plot, requires an X11 Window System to enable graphics forwarding. Graphics forwarding is how graphics are sent from a remote host (i.e., the HPC cluster) to the local client (i.e., your computer). 

[XQuartz](https://www.xquartz.org) the X11 Window System for MacOS. The X11 Window System requirements will vary by OS and by computer. Some Windows users may need to install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) while Linux users don't need to install an X11 Window System. For more information, see Step 3 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. 

### Login to HPC
Login to HPC uses a Secure Shell (SSH) protocol, a method for secure remote login between your computer and HPC. This lets us to communicate with HPC i.e., send inputs and recieve outputs.

<p align="center">
<img src="readme_images/local_to_hpc.png" height="300">
</p>

MacOS and Linux OS users can login to HPC using the default Terminal application without installing anything. Windows OS does not automatically have a Unix Shell program installed and [MobaXterm](https://mobaxterm.mobatek.net) is recommended by Storrs HPC Admins and this application jointly acts as an X11 Window System and SSH protocol. For more information about logging into HPC, see Step 3 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. 

Note: errors have been reported with building and using the Ollama container while logged into UConn Storrs HPC through Remote - SSH extensions in VS Code. More info in Step G and M.

* __Step B:__ Login to Storrs HPC from a MacOS computer by running the following in Terminal:
```
# login to hpc
# replace netid with your personal UConn NetID
ssh -Y netid@hpc2.storrs.hpc.uconn.edu
```

Follow the prompts to enter your password and complete any 2FA authentication. When successfully logged in you'll be assigned to a login node on HPC. 
```
# check the node 
# when logged in, hostname returns your assigned login node e.g., login4
hostname
```

### Load Files
FileZilla is a File Transfer Protocol (FTP) allowing files to be transferred between your computer and HPC over the internet. The Python script and the files it references need to be transferred to HPC. Note that since the transfer occurs over the internet, you need to be connected to the UConn network (see the Connect to a VPN section above). 

To install FileZilla and connect it to your HPC account, following the steps from UConn Storrs HPC's [File Transfer](https://kb.uconn.edu/space/SH/26033783688/File+Transfer) document, under the Data Storage Guide dropdown.

Before uploading any data, please see [this link](https://kb.uconn.edu/space/SH/26033979893/FAQ#What-kind-of-data-can-be-stored-on-the-Storrs-HPC?) to the FAQs about what data can be stored on UConn Storrs HPC.

* __Step C:__ Open FileZilla and click the Site Manager icon to connect to HPC

* __Step D:__ (Option 1) Transfer these folders and files to your HPC account: 
    - classify_with_ollama.py
    - requirements.txt
    - library
        - dictionary.py
        - fit.py
        - start.py
    - data
        - demo_data
            - goodreads_20.csv
    - output
        - demo_output

If you saved these files within a directory, change your working directory to where classify_with_ollama.py is saved:
```
# set your working directory
cd path/to/directory
```

* __Step D:__ (Option 2) Clone the GitHub Repository to your HPC account:
```
# (optional) cd = change directory: set your working directory the folder where you'd like to clone the repo
cd path/to/directory

# clone the repository
git clone https://github.com/hernandezb3/llama-on-uconn-hpc.git

# set your working directory inside the repo
cd llama-on-uconn-hpc
```
If you use Option 2 and are new to GitHub, please see docs.GitHub.com [Getting changes from a remote repository](https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository) guide for how to update the repo as changes are made (e.g., pull, fetch).

To check that the files loaded successfully, run the following in Terminal:
```
# ls = list: check files loaded successfully
ls
```
### Request a Job
There are two ways to request resources from UConn Storrs HPC, an interactive job (srun) or a scheduled job (sbatch). The demo requests an interactive job, so we can drop-in to HPC to send inputs and recieve outputs from HPC in real time. For more information about job types, see Step 5 in UConn Storrs HPC's [Getting Started](https://kb.uconn.edu/space/SH/26694811668/Getting+Started) guide. 

<p align="center">
<img src="readme_images/jobs.png" height="200">
</p>

The job request is where to specify what resources we'd like to use on HPC. You can also request to be assigned to a node in a specific partition. For more information about the UConn Storrs HPC partitions and how to incorporate them into the job request, see [here](https://kb.uconn.edu/space/SH/26032963610/Partitions+%2F+Storrs+HPC+Resources#I.-Partitions-of-the-Storrs-HPC)  
<br/><br/>
<p align="center">
<img src="readme_images/hpc_nodes_1.png" height="150">
</p>
<p align="center">
<img src="readme_images/hpc_nodes_2.png" height="190">
</p>

A program, SLURM, assigns resources on HPC as they become available. See the [SLURM Guide](https://kb.uconn.edu/space/SH/26032963685/SLURM+Guide) for more examples of how to request jobs on HPC.

The output from the classify_with_ollama.py script estimates the runtime, CPU, and RAM of model requests. This is included so various model sizes or features of the model like how complex the task is or number tokens in the output, can be used to test and refine the requirements needed for future job requests.

* __Step E:__ Start an interactive job by running the following in Terminal:
```
# srun = requests an interactive job
# -n = number of nodes (1)
# -t = time allocation (30 minutes)
# --mem = ram (16 GB)
# --pty = scripting language (bash)
srun -n 1 -t 0:30:00 --mem=16G --pty bash
```
```
# returns a node id when assigned resources
hostname
```
### Load Software
Some software (aka modules) like Python and Apptainer are made available to use on UConn Storrs HPC. Run the following to see what software are available:
```
# list modules
module avail
```
```
# check which versions of python are available
module avail python
```

Software not available as a module can be downloaded with a container. The next section will discuss containers. For now, we will load the necessary modules which include Apptainer which we will need to build and run a container. 

UConn Storrs HPC uses Apptainer 1.1.3 which has a dependency (gcc) incompatible with the Python version loaded by default. We will first unload conflicting modules and then load Apptainer and a compatible version of Python.

* __Step F:__ Load modules by running the following in Terminal:
```
# remove incompatible packages
module unload python
module unload gcc
# add apptainer and python
module load apptainer
module load python/3.12.2
```
### Build a Container 
A container is an isolated environment to run an application. Within the container is anything necessary e.g., files, packages, etc. run the application. A container is built from an image, which contains the instructions for how to build the envrionment. The image can be thought of as an instructional manual for building a container. 

Images can be manually built, but Docker, a containerization service, contains a library of prebuilt images. Apptainer, the container module used by UConn Storrs HPC, is compatible with Docker, so with Apptainer we can pull images from the Docker library to build containers. We will reference the Ollama image from the Docker library to build the Ollama container.

</p>
<p align="center">
<img src="readme_images/containers.png" height="200">
</p>

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
Login to your Docker account to connect the image to your account. This allows you to use Docker Hub to track running containers connected to that image. If you don't have a Docker account, press enter when asked for your Docker Username and Password or remove --docker-login from the command.

### Start the Container
Once the container is built, the container needs to be "turned on." Starting the container as an instance (instance start vs apptainer run) runs the container in the background. After the container is started, we shell into it and start the Ollama application. 

I like to think of a container as a "computer" built to run a single application. With that framing, instance start as analagous to turning on the computer and ollama serve to opening the Ollama app.

* __Step H:__ Start the instance by running the following in Terminal:
```
# apptainer = application
# instance start = start running the container
# ollama/ = name of the container (i.e., the custom name of the directory from the last step)
# ollama_instance = a custom name for the instance
apptainer instance start ollama/ ollama_instance
```
### Run Ollama
Shell into the container to run commands within the container.
<p align="center">
<img src="readme_images/hpc_to_container.png" height="300">
</p>

* __Step I:__ Shell into the instance and run Ollama by running the following in Terminal:
```
# apptainer = application
# shell = enter the container
# instance://ollama_instance = name of the instance to shell into
apptainer shell instance://ollama_instance
```
```
# ollama = application
# serve = start ollama
ollama serve
```
Running the Ollama application will take up the entire terminal window. We'll complete the remainder of the demo in another terminal window.

### Login to HPC
In a new terminal window, we will login to the same node Ollama is running on. Start by logging into HPC from the new terminal window.

* __Step J:__ Login to UConn Storrs HPC by running the following in Terminal:
```
# replace netid with your personal UConn NetID
# replace hpc2 with the specific login node assigned
# this is output of hostname in Step B
ssh -Y netid@hpc2.storrs.hpc.uconn.edu
```

### Go to the Job
Once logged into HPC, we can shell into our running interactive job.

* __Step K:__ Login to the job by running the following in Terminal:
```
# replace node with the interactive job node
# this is output of hostname in Step E
ssh node
```

### Load Software
We will be using Apptainer again and Python, so load those modules. 

* __Step L:__ Load modules by running the following in Terminal:
```
# remove incompatible packages
module unload python
module unload gcc
# add apptainer and python
module load apptainer
module load python/3.12.2
```

### Download a Model
Now, enter the container where Ollama is running and download the Llama model is referenced in the classify_with_ollama.py script. Note that Ollama needs to be running (ollama serve) in order to download any models.

To try the demo with another model from the [Ollama library](https://ollama.com/library) it needs to be changed in the script and then downloaded into the container.

* __Step M:__ Download models by running the following in Terminal:
```
# apptainer = application
# shell = enter the container
# instance://ollama_instance = name of the instance to shell into
apptainer shell instance://ollama_instance
```
```
# list the models that are downloaded in the container
ollama list
```
```
# pull the Llama 3.2 model (by default this pulls the 3B parameter model by default)
ollama pull llama3.2
```
```
# exit out of the container
# i.e., go back to the hpc environment
exit
```

The following error has been reported when pulling models from Apptainer containers built while connected to UConn Storrs HPC through Remote - SSH extensions in VS Code:

"Error: pull model manifest: Get "https://registry.ollama.ai/v2/library/1lama3.2/manifests/latest*: dial top: look up registry.ollama.ai on [::1]:53: read up [ 11 3428-7 12 105, read. connection refused"

### Install Python Packages
The Python script, classify_with_ollama.py, uses a host of packages e.g., Pandas and langchain_Ollama, a package for using Ollama. The packages required to run all the scripts in this repo are are listed in requirements.txt. The required packages specific to each script can be found at the top of each script. For Windows commands and additional support installing packages from a requirements file please see this [Pip User Guide](https://pip.pypa.io/en/latest/reference/requirements-file-format/#requirements-file-format). 

* __Step N:__ Install required python packages by running the following in Terminal:
```
# -r = install from the given requirements file
pip3 install -r requirements.txt
```

### Run Python Script
The script uses a demo prompt from the dictionary which asks, "Predict the rating of the following book review on a scale of 0 = bad to 5 = good." The script contains a loop that combines this prompt with each of the 20 reviews in goodreads_20.csv, inputs them into the model, returns an output, and calculates the root mean square error (RMSE). 

* __Step O:__ Install required python packages by running the following in Terminal:
```
python3 classify_with_ollama.py
```

### Save the Output
The script creates two files, df and output: 
- df: contains a dataframe of the data with a added columns for the llama_rating each case
- output: contains the rmse and computing resources used in the model request, e.g., RAM, CPU. This information can be used to compare the resources used for different sized models and different sets of data

```
# = view the contents of a file

```

The files contained in all subfolders of output are ignored in .gitignore so they will not be pushed to GitHub. This structure allows us to standardize a path for where to save output files while protecting actual data from being pushed out publicly. 

* __Step P:__ Save the output files
Output files can be directly downloaded from HPC to your local computer using FileZilla. For additional file storage information see the Storrs HPC [Data Storage Guide](https://kb.uconn.edu/space/SH/26034012236/Data+Storage+Guide).


### Logout of HPC
Finally, exit from all containers and HPC entirely. To stop running Ollama, click into the terminal window and use CTRL + C to cancel and then exit out of both the container and the interactive job. You'll know you're logged out when running hostname on both terminal windows return a login node.

<p align="center">
<img src="readme_images/exit.png" height="300">
</p>

* __Step Q:__ Logout of BOTH terminal windows by running the following in Terminal:

```
exit
```

Check that you are on a login node:
```
hostname
```

Comments, questions, or suggestions to this repo? See the [Discussion](https://github.com/hernandezb3/llama-on-uconn-hpc/discussions) forum

README last updated: April 17, 2025