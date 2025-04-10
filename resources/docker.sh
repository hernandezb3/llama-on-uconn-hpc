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
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# run download and run llama3.2 3B
docker exec -it ollama ollama run llama3.2