# need 2 terminal windows on the same node

# window 1 = start the interactive session and start ollama

# login to hpc
ssh -Y bah17005@hpc2.storrs.hpc.uconn.edu

# start an interactive job (aka drop in)
srun -n 1 -t 0:30:00 --mem=64G --pty bash
srun -n 1 -p general-gpu --mem=64G --pty bash
srun --x11 -N 1 -n 126 -p general --constraint="epyc128" --exclude=cn[473-479] --pty bash
srun --x11 -N 1 -n 126 --gres=gpu:1 -p general --constraint="epyc128" --exclude=cn[473-479] --pty bash

# add apptainer and remove incompatible packages
# a compatible version of python is loaded later
module unload python
module unload gcc
module load apptainer

# build the container if it isn't already built
apptainer build --force --docker-login --sandbox ollama/ docker://ollama/ollama:latest # sandbox
#apptainer build --force --docker-login ollama_latest.sif docker://ollama/ollama:latest # apptainer

# start ollama in sandbox
apptainer instance start ollama/ ollama_instance
apptainer shell instance://ollama_instance
ollama serve


# window 2 = download the model
# login to hpc
ssh -Y bah17005@hpc2.storrs.hpc.uconn.edu # replace hpc2 with the login node from window 1 e.g., bah17005@login5.storrs.hpc.uconn.edu
# ssh into the running session
ssh cn538 # replace cn538 with the session id

# add apptainer and remove incompatible packages
module unload python
module unload gc
module load apptainer

# start the model
apptainer shell instance://ollama_instance
ollama list # check which models have been pulled
ollama pull llama3.2 # pull a new model




# window 3
# login to hpc
ssh -Y bah17005@hpc2.storrs.hpc.uconn.edu # replace hpc2 with the login node from window 1 e.g., bah17005@login5.storrs.hpc.uconn.edu
# ssh into the running session
ssh cn538 # replace cn538 with the session id

# add apptainer and remove incompatible packages
module unload python
module unload gc
module load apptainer

# python 3.12.5 uses gcc dependency that conflicts with what's needed for apptainer
module load python/3.12.2

# install packages and run the python script
pip3 install -r requirements.txt

# run the script
python3 pilot_classifications_llama_ollama_hpc.py





# exit out of all sessions
exit # end the interactive job







