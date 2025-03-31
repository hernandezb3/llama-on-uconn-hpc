# how to run the same container in docker:
# with apptainer equivelent
docker login
docker pull ollama/ollama:latest # docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# -d = run container in background
# -v = bind mount volume
# -p = publish containers ports to the host
docker exec -it ollama ollama run llama3.2