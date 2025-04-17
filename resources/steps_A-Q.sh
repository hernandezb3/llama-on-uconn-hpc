# TERMINAL WINDOW 1 
# objective = start the interactive session and start ollama

# Step A: connect to UConn-Secure wifi through Cisco Secure Client or MobaXterm

# Step B: login to hpc
# replace netid with your personal NetID
ssh -Y netid@hpc2.storrs.hpc.uconn.edu
hostname

# Step D: load files
# option 1 upload files with FileZilla
# option 2 sync github repo
# (optional) cd = change directory: set your working directory the folder where you'd like to clone the repo
cd path/to/directory
# clone the repository
git clone https://github.com/hernandezb3/llama-on-uconn-hpc.git
# set your working directory inside the repo
cd llama-on-uconn-hpc
# check files loaded
ls

# Step E: request a job
# srun = requests an interactive job (aka drop in)
# -n = number of nodes (1)
# -t = time allocation (30 minutes)
# --mem = ram (16 GB)
# --pty = scripting language (bash)
srun -n 1 -t 0:30:00 --mem=16G --pty bash
hostname

# Step F: load software
# remove incompatible packages
module unload python
module unload gcc
# add apptainer and python
module load apptainer
module load python/3.12.2 # technically can skip loading python here, but this keeps continuity with Step L

# Step G: build the container
# build an apptainer container from the docker repository
# apptainer = application
# build = create a container
# --force = overwrites any docker images under the same name
# --docker-login = connects the image to your docker account
# --sandbox = builds the container in a directory instead of as a .SIF file
# ollama/ = the custom name of the directory
# docker://ollama/ollama:latest = path to the docker image to use
apptainer build --force --docker-login --sandbox ollama/ docker://ollama/ollama:latest


# Step H: start the container
# apptainer = application
# instance start = start running the container
# ollama/ = name of the container (i.e., the custom name of the directory from the last step)
# ollama_instance = a custom name for the instance
apptainer instance start ollama/ ollama_instance

# Step I: run ollama
# apptainer = application
# shell = enter the container
# instance://ollama_instance = name of the instance to shell into
apptainer shell instance://ollama_instance
# ollama = application
# serve = start ollama
ollama serve



# TERMINAL WINDOW 2 
# objective = download the model and run the script

# Step J: login to hpc
# this is output of hostname in Step B
ssh -Y netid@hpc2.storrs.hpc.uconn.edu # replace hpc2 with the login node from window 1 e.g., bah17005@login5.storrs.hpc.uconn.edu

# Step K: go to the job
# this is output of hostname in Step E
ssh node # replace node with the session id

# Step L: load software
# remove incompatible packages
module unload python
module unload gcc
# add apptainer and python
module load apptainer
module load python/3.12.2

# Step M: download a model
# apptainer = application
# shell = enter the container
# instance://ollama_instance = name of the instance to shell into
apptainer shell instance://ollama_instance
# list the models that are downloaded in the container
ollama list
# pull the Llama 3.2 model (by default this pulls the 3B param model)
ollama pull llama3.2
# leave the Ollama container shell
exit

# Step N: install python packages
pip3 install -r requirements.txt

# Step O: run python script
python3 classify_with_ollama.py

# Step P: save output
# transfer files from HPC to local with FileZilla

# Step Q: exit hpc
# ctrl + c to cancel ollama serve
# exit out of all sessions until on a login node
exit # end the interactive job