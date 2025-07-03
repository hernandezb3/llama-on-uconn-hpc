import pandas as pd
import numpy as np
from huggingface_hub import login
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import TrainingArguments

from library import start, secrets, dictionary

login(secrets.LLAMA_31_API_KEY)

MODEL = "meta-llama/Llama-3.3-70B-Instruct"

# data to finetune with
data = pd.read_csv(start.DATA)

# model to fineune
tokenizer = AutoTokenizer.from_pretrained(MODEL)

def tokenize(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

data = data.map(tokenize, batched = True)

# create a subset of data to test with
small_train = data["train"].shuffle(seed=42).select(range(1000))
small_eval = data["test"].shuffle(seed=42).select(range(1000))

model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels = 5)

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    # convert the logits to their predicted class
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments(
    output_dir="yelp_review_classifier",
    eval_strategy="epoch",
    push_to_hub=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=data["train"],
    eval_dataset=data["test"],
    compute_metrics=compute_metrics,
)
trainer.train()
trainer.evaluate()
trainer.push_to_hub()