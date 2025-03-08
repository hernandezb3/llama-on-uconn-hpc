# llama with ollama
# pytorch not supported for Python 3.13 - .venv for 3.12
# python3 command
import os
print("os")
import pandas as pd
print("pandas")
from langchain_ollama import OllamaLLM
print("langchain")
from library import start, secrets, fit # take out oamm. to run whole file
print("library")

model_id = "llama3.2" # ollama: llama3.2
print("model_id")
#load_dotenv(override = True)
ollama_server_url = "http://localhost:11434"
#ollama_server_url = os.environ["http://localhost:11434"]
llm = OllamaLLM(model = model_id, base_url = ollama_server_url)
print("llm settings")

input = "how are you?"
print("set input")
response = llm.invoke(input)
print("response")


print(response)

path = start.OUTPUT_DIR
filename = "test.csv"
response = pd.DataFrame([response])
response.to_csv(path + filename, index = False)