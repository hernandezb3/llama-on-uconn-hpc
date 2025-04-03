# TERMINAL WINDOW 1 
# objective = start the interactive session and start ollama

# Step B: login to hpc
# replace netid with your personal NetID
ssh -Y netid@hpc2.storrs.hpc.uconn.edu
hostname

# Step D: check files loaded
ls

# Step E: start an interactive job (aka drop in)
srun -n 1 -t 0:30:00 --mem=16G --pty bash
hostname

# Step F: load modules
# remove incompatible packages
module unload python
module unload gcc
# add apptainer and python
module load apptainer
module load python/3.12.2 # technically can skip loading python here, but this keeps continuity with Step L

# Step G: build the container
apptainer build --force --docker-login --sandbox ollama/ docker://ollama/ollama:latest # sandbox

# Step H: start the container in sandbox
apptainer instance start ollama/ ollama_instance

# Step I: run ollama
apptainer shell instance://ollama_instance
ollama serve



# TERMINAL WINDOW 2 
# objective = download the model and run the script

# Step J: login to hpc
# this is output of hostname in Step B
ssh -Y netid@hpc2.storrs.hpc.uconn.edu # replace hpc2 with the login node from window 1 e.g., bah17005@login5.storrs.hpc.uconn.edu

# Step K: ssh into the running session

# this is output of hostname in Step E
ssh node # replace node with the session id

# Step L: load modules
# remove incompatible packages
module unload python
module unload gcc
# add apptainer and python
module load apptainer
module load python/3.12.2

# Step M: download the model
# apptainer = application
# shell = enter the container
# instance://ollama_instance = name of the instance to shell into
apptainer shell instance://ollama_instance
# see which model's have been downloaded to the container
ollama list
# pull the Llama 3.2 model (by default this pulls the 3B param model)
ollama pull llama3.2 # pull a new model

# leave the Ollama container shell
exit

# Step N: install python packages
pip3 install -r requirements.txt

# Step O: run the script
python3 classify_with_ollama.py



# ALL WINDOWS
# exit out of all sessions
exit # end the interactive job