import os

MAIN_DIR = os.getcwd() + "/"

DATA_DIR = MAIN_DIR + "data/" # hpc
#DATA_DIR = "/Users/brittneyhernandez/Library/CloudStorage/OneDrive-SharedLibraries-YaleUniversity/Zieher, Almut - OAMM_PEACE23-24/data/"

PROMPT = DATA_DIR + "demo_prompts.csv"
DATA = DATA_DIR + "goodreads.csv"

#DATA = DATA_DIR + "gold_standard_recalls.xlsx" # hpc
#DATA = DATA_DIR + "clean/gold_standard_recalls.xlsx"

OUTPUT_DIR = MAIN_DIR # hpc
#OUTPUT_DIR = DATA_DIR + "llama_testing/"
