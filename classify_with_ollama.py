# llama with ollama
# pytorch not yet supported for Python 3.13 - .venv for 3.12.2
import os
import math
import re
import datetime # couldn't install use datetime
from datetime import datetime
import psutil
import pandas as pd
from langchain_ollama import OllamaLLM
from library import start, dictionary, fit # take out oamm. to run whole file

checkpoint0 = datetime.now() # start runtime counter

# ollama model ids
#model_id = "llama3.3" # llama3.3 70B
model_id = "llama3.2" # llama3.2
#model_id = "llama3.2:1b" # llama3.2:1b
model_name = dictionary.model_names[model_id]

# initialize the model
ollama_server_url = "http://localhost:11434"
llm = OllamaLLM(model = model_name, base_url = ollama_server_url)

checkpoint1 = datetime.now() # runtime counter

# prompts 
prompts = dictionary.demo_prompts["goodreads"]

# data frame
df = pd.read_csv(start.DATA)

# loop through running the model for each prompt
rmse = []
llama_output = [] # initialize list
for case in df["review_text"]:
    prompt_case = prompts["goodreads"] + " " + case
    input = [{"role": "user", "content": prompt_case}]
    response = llm.invoke(input)
    llama_output.append(response)
    print(response)
df["llama_rating"] = llama_output
rmse.append(fit.get_rmse(df["rating"], df["llama_rating"]))

checkpoint2 = datetime.now() # end runtime counter
print(df)

# get runtime and cpu, ram usage:
total_runtime = checkpoint2 - checkpoint0 
pull_model_runtime = "na"
request_runtime = checkpoint2 - checkpoint1
cpu_usage = psutil.cpu_percent(total_runtime.total_seconds())
ram_used = psutil.virtual_memory()[3]/1000000000 # in GB
# compile into dataframe
output = {"model": [model_id], "n cases": [df.index], "rmse": [rmse], "total runtime (min)": [total_runtime/60], "model_pull": [pull_model_runtime/60], "request": [request_runtime/60], "cpu ()": [cpu_usage], "ram (gb)": [ram_used]}
output = pd.DataFrame(output)
print(output)

# write df and output to an .xlsx file
# create an output file in the parent directory
path = start.OUTPUT_DIR
filename = df.index + dictionary.model_names[model_id] + ".csv"

df.to_csv(path + "df_demo_" + filename, index = False)
output.to_csv(path + "output_demo_" + filename, index = False)