# llama with ollama
# pytorch not supported for Python 3.13 - .venv for 3.12
# python3 command
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
from library import start, secrets, classify, fit # take out oamm. to run whole file

checkpoint0 = datetime.now() # start runtime counter

# llama models:
# hugging face:
#model_id = "meta-llama/Llama-3.3-70B-Instruct" # hugging face
#model_id = "meta-llama/Llama-3.2-3B-Instruct" # hugging face
#model_id = "meta-llama/Llama-3.2-1B-Instruct" # hugging face
#model_id = "meta-llama/Llama-3.1-8B" # hugging face

#model_id = "llama3.3" # ollama: llama3.3
model_id = "llama3.3" # ollama: llama3.2
#model_id = "llama3.2:1b" # ollama: llama3.2:1b

ollama.pull(model_id) # initialize the model
checkpoint1 = datetime.now() # start runtime counter

#TOKENS = 30 # n characters in output

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
df = pd.read_excel(start.DATA_DIR + "clean/gold_standard_recalls.xlsx")
empty_text = []
for row in list(range(0, len(df["recall_texts"]))):
    if (type(df["recall_texts"][row])) == float:
        empty_text.append(row)
df = df.drop(empty_text, axis = 0) # drop cases with no survey response
df = df.sample(SAMPLE_SIZE, random_state = 1) # get a random sample

checkpoint2 = datetime.now()

# loop through running the model for each prompt
rmse = []
for outcome in OUTCOMES:
    llama_output = [] # initialize list
    for case in df["recall_texts"]:
        prompt_case = prompt_dict[outcome] + " " + case
        input = [{"role": "user", "content": prompt_case}]
        output: ChatResponse = chat(model = model_id, messages = input)
        response = output["message"]["content"]
        if response.isdigit() == False:
            numbers = []
            for character in response:
                if character.isdigit() == True:
                    number = int(character)
                    number = numbers.append(number)
            response = numbers[0]
        llama_output.append(response)
    df["llama_" + outcome] = llama_output
    rmse.append(fit.get_rmse(df[outcome], df["llama_" + outcome]))

checkpoint3 = datetime.now() 

# get runtime and cpu, ram usage:
checkpoint4 = datetime.now() # end runtime counter
total_runtime = checkpoint4 - checkpoint0 # add other markers... total runtime, model request runtime
pull_model_runtime = checkpoint2 - checkpoint1
request_runtime = checkpoint3 - checkpoint2
cpu_usage = psutil.cpu_percent(total_runtime.total_seconds())
ram_used = psutil.virtual_memory()[3]/1000000000 # in GB

output = {"model": [model_id], "outcomes": [OUTCOMES], "cases per outcome": [SAMPLE_SIZE], "rmse": [rmse], "total runtime (min)": [total_runtime/60], "model_pull": [pull_model_runtime/60], "request": [request_runtime/60], "cpu ()": [cpu_usage], "ram (gb)": [ram_used]}
output_csv = pd.DataFrame(output)

# write .xlsx
path = start.DATA_DIR + "/llama_testing/"
filename = model_id + "_out" + str(len(OUTCOMES)) + "_n" + str(SAMPLE_SIZE) + ".csv"

print(output_csv)
print(output)
# for saving locally
# sheet 1 = llama output for gold standard cases
#df.to_csv(path + "df_"+ filename, index = False)
#output_csv.to_csv(path + filename, index = False)

# for hpc run
#df.to_csv("df_"+ filename, index = False)
#output_csv.to_csv(filename, index = False)
# sheet 2 = rmse + metadata