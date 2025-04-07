# llama with ollama
# pytorch not yet supported for Python 3.13 - .venv for 3.12.2
import os
import math
import re
import datetime # couldn't install use datetime
from datetime import datetime
import psutil
import pandas as pd
import ollama
from ollama import chat
from ollama import ChatResponse
from langchain_ollama import OllamaLLM
from library import dictionary, fit # take out oamm. to run whole file
from library import start_oamm as start

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
# prompts for oamm data
ALL_OUTCOMES = ["sa", "ob", "pr", "re", "cu", "di", "w", "co"]
OUTCOMES = ["sa", "di"]
PROMPT_SHEET = "Zero Shot 3"

prompts = {}
for outcome in ALL_OUTCOMES:
    prompt_filename = start.DATA_DIR + "prompts_" + outcome + ".xlsx" # 1
    prompt_xlsx = pd.read_excel(prompt_filename, sheet_name = PROMPT_SHEET) # 2
    prompt = prompt_xlsx["content"][0]
    # prompt = classify.create_prompt(prompts, PROMPT_SHEET) # 3
    prompts[outcome] = prompt

# dataframe
# get a sample of oamm data
SAMPLE_SIZE = 5
df = pd.read_excel(start.DATA)
empty_text = []
for row in list(range(0, len(df["recall_texts"]))):
    if (type(df["recall_texts"][row])) == float:
        empty_text.append(row)
df = df.drop(empty_text, axis = 0) # drop cases with no survey response
df = df.sample(SAMPLE_SIZE, random_state = 1) # get a random sample


# loop through running the model for each outcome and corresponding prompt
rmse = []
for outcome in OUTCOMES:
    llama_output = [] # initialize list
    for case in df["recall_texts"]:
        prompt_case = prompts[outcome] + " " + case
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

checkpoint2 = datetime.now() # end runtime counter

# get runtime and cpu, ram usage:
total_runtime = checkpoint2 - checkpoint0 
pull_model_runtime = "n/a"
request_runtime = checkpoint2 - checkpoint1
cpu_usage = psutil.cpu_percent(total_runtime.total_seconds())
ram_used = psutil.virtual_memory()[3]/1000000000 # in GB

output = {"model": [model_id], "outcomes": [OUTCOMES], "cases per outcome": [SAMPLE_SIZE], "rmse": [rmse], "total runtime (min)": [total_runtime/60], "model_pull": [pull_model_runtime/60], "request": [request_runtime/60], "cpu ()": [cpu_usage], "ram (gb)": [ram_used]}
output = pd.DataFrame(output)

# write .xlsx
path = start.DATA_DIR + "/llama_testing/"
filename = dictionary.model_names[model_id] + "_out" + str(len(OUTCOMES)) + "_n" + str(SAMPLE_SIZE) + ".csv"

print(df)
print(output)

# write .xlsx
path = start.OUTPUT_DIR
filename = dictionary.model_names[model_id] + "_out" + str(len(OUTCOMES)) + "_n" + str(SAMPLE_SIZE) + ".csv"

df.to_csv(path + "df_"+ filename, index = False)
output.to_csv(path + filename, index = False)