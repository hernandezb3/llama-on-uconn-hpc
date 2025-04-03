# llama with ollama
# pytorch not supported for Python 3.13 - .venv for 3.12
# python3 command
import os
print("os")
import pandas as pd
print("pandas")
from langchain_ollama import OllamaLLM
print("langchain")
from library import dictionary, start 
print("library")

model_id = "llama3.2" # ollama: llama3.2
model_name = dictionary.model_names[model_id]
ollama_server_url = "http://localhost:11434"
llm = OllamaLLM(model = model_name, base_url = ollama_server_url)
print("llm settings")

input = dictionary.demo_prompts["hello"]
print(input)
response = llm.invoke(input)
print(response)

path = start.OUTPUT_DIR
filename = "test.csv"
response = pd.DataFrame([response])
response.to_csv(path + filename, index = False)