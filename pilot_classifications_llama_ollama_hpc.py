# llama with ollama
# pytorch not supported for Python 3.13 - .venv for 3.12
# python3 command
import os
import math
import re
#from dotenv import load_dotenv
import datetime # couldn't install use datetime
from datetime import datetime
import psutil
import pandas as pd
import ollama
from ollama import chat
from ollama import ChatResponse
from langchain_ollama import OllamaLLM
from library import start, secrets, fit # take out oamm. to run whole file
checkpoint0 = datetime.now() # start runtime counter

# llama models: ollama
#model_id = "llama3.3" # ollama: llama3.3
model_id = "llama3.2" # ollama: llama3.2
#model_id = "llama3.2:1b" # ollama: llama3.2:1b

model_names = {"meta-llama/Llama-3.3-70B-Instruct": "llama3.3",
               "meta-llama/Llama-3.2-1B-Instruct": "llama3.2_1b", 
               "meta-llama/Llama-3.2-3B-Instruct": "llama3.2",
               "meta-llama/Llama-3.1-8B": "llama3.1",
               "llama3.3": "llama3.3",
               "llama3.2": "llama3.2",
               "llama3.2_1b": "llama3.2_1b",
               "llama3.1": "llama3.1"}

#load_dotenv(override = True)
ollama_server_url = "http://localhost:11434"
#ollama_server_url = os.environ["http://localhost:11434"]
llm = OllamaLLM(model = model_id, base_url = ollama_server_url)

#ollama.pull(model_id) # initialize the model
checkpoint1 = datetime.now() # start runtime counter

# set input parameters
# 1. determine which outcomes to run the model for
ALL_OUTCOMES = ["sa", "ob", "pr", "re", "cu", "di", "w", "co"]
OUTCOMES = ["sa"]
#PROMPT_FILE = start.DATA_DIR + "prompts_sa.xlsx"
PROMPT_SHEET = "Zero Shot 3"

prompt_dict = {}
for outcome in ALL_OUTCOMES:
    prompt_filename = start.DATA_DIR + "prompts_" + outcome + ".xlsx" # 1
    prompts = pd.read_excel(prompt_filename, sheet_name = PROMPT_SHEET) # 2
    prompt = prompts["content"][0]
    # prompt = classify.create_prompt(prompts, PROMPT_SHEET) # 3
    prompt_dict[outcome] = prompt

# 2. determine how many survey responses to include
SAMPLE_SIZE = 30
#df = pd.read_excel("clean/gold_standard_recalls.xlsx") # for the hpc interactive job
df = pd.read_excel(start.GOLD_STANDARD)
empty_text = []
for row in list(range(0, len(df["recall_texts"]))):
    if (type(df["recall_texts"][row])) == float:
        empty_text.append(row)
df = df.drop(empty_text, axis = 0) # drop cases with no survey response
df = df.sample(SAMPLE_SIZE, random_state = 1) # get a random sample

checkpoint2 = datetime.now()

input = "how are you"
llm.invoke(input)

# loop through running the model for each prompt
rmse = []
for outcome in OUTCOMES:
    llama_output = [] # initialize list
    for case in df["recall_texts"]:
        prompt_case = prompt_dict[outcome] + " " + case
        input = [{"role": "user", "content": prompt_case}]
        response = llm.invoke(input)
        if response.isdigit() == False:
            numbers = []
            for character in response:
                if character.isdigit() == True:
                    number = int(character)
                    number = numbers.append(number)
            response = numbers[0]
        llama_output.append(response)
        print(response)
    df["llama_" + outcome] = llama_output
    rmse.append(fit.get_rmse(df[outcome], df["llama_" + outcome]))

checkpoint3 = datetime.now() # end runtime counter

# get runtime and cpu, ram usage:
total_runtime = checkpoint3 - checkpoint0 
pull_model_runtime = checkpoint2 - checkpoint1
request_runtime = checkpoint3 - checkpoint2
cpu_usage = psutil.cpu_percent(total_runtime.total_seconds())
ram_used = psutil.virtual_memory()[3]/1000000000 # in GB

output = {"model": [model_id], "outcomes": [OUTCOMES], "cases per outcome": [SAMPLE_SIZE], "rmse": [rmse], "total runtime (min)": [total_runtime/60], "model_pull": [pull_model_runtime/60], "request": [request_runtime/60], "cpu ()": [cpu_usage], "ram (gb)": [ram_used]}
output = pd.DataFrame(output)

# write .xlsx
path = start.DATA_DIR + "/llama_testing/"
filename = model_names[model_id] + "_out" + str(len(OUTCOMES)) + "_n" + str(SAMPLE_SIZE) + ".csv"

print(output)
print(output)

# write .xlsx
path = start.OUTPUT_DIR
filename = model_names[model_id] + "_out" + str(len(OUTCOMES)) + "_n" + str(SAMPLE_SIZE) + ".csv"

#df.to_csv(path + "df_"+ filename, index = False)
#output.to_csv(path + filename, index = False)