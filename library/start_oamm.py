import os

# local
OAMM_DIR = "/Users/brittneyhernandez/Library/CloudStorage/OneDrive-SharedLibraries-YaleUniversity/Zieher, Almut - OAMM_PEACE23-24/"
# path to the data
DATA_DIR = OAMM_DIR + "data/" # local
# data to use:
# goodreads demo data 
DATA = DATA_DIR + "clean/gold_standard_recalls.xlsx" # local
# path to output model responses:
OUTPUT_DIR = DATA_DIR + "llama_testing/" # local

# hpc
# directory to work out of
MAIN_DIR = os.getcwd() + "/"
# path to the data
DATA_DIR = MAIN_DIR + "data/oamm_data/" # hpc
# data to use:
# goodreads demo data 
DATA = DATA_DIR + "gold_standard_recalls.xlsx" # hpc
# path to output model responses:
OUTPUT_DIR = MAIN_DIR + "output/oamm_output/" # hpc