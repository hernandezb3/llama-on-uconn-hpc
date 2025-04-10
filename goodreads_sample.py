import pandas as pd

# read in the kaggle training data
data = pd.read_csv("data/demo_data/goodreads_train.csv")

# generate a random sample of 20 cases
data_20 = data.sample(20)

# save the sample
data_20.to_csv("data/demo_data/goodreads_20.csv")