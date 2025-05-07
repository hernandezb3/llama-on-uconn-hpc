# build and run a Docker container from the a Docker image:
# instead of using Apptainer to build the container

# login to docker
docker login

# pull the latest ollama image
docker pull ollama/ollama:latest # docker

# run the container
# -d = run container in background
# -v = bind mount volume
# -p = publish containers ports to the host
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama:latest

# run download and run llama3.2 3B
docker exec -it ollama ollama run llama3.2

# assumes python is installed
# to mimic hpc, use the same version of python aka 3.12.2

# install packages for classify_with_ollama.py
# requirements.txt should be saved in the working directory
# use cd to change directories 
# or add the exact path to the front of the requirements.txt
# e.g., Documents/llama-on-uconn-hpc/requirements.txt
pip3 install -r requirements.txt

# run the script
python3 classify_with_ollama.py