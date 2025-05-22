import os
from datasets import load_dataset
from transformers import AutoTokenizer

#1 ---------------------------------------------------------------------------------- 1
#1.1
imdb = load_dataset("stanfordnlp/imdb")
print(imdb)

#1.2
train_full = imdb["train"].shuffle(seed=42).select(range(1000))
train_dataset = train_full.select(range(900))
val_dataset = train_full.select(range(900, 1000))
test_dataset = imdb["test"].shuffle(seed=42).select(range(200))

#1.3
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

#1.4
def tokenize_function(example):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=tokenizer.model_max_length
    )

train_dataset_tok = train_dataset.map(tokenize_function, batched=True)
val_dataset_tok = val_dataset.map(tokenize_function, batched=True)
test_dataset_tok = test_dataset.map(tokenize_function, batched=True)

#1.5
sample = train_dataset[0]
tokens = tokenizer.convert_ids_to_tokens(
    tokenizer(sample["text"], truncation=True, max_length=tokenizer.model_max_length)["input_ids"]
)
print("Original text:", sample["text"])
print("Tokenized:", tokens)

#2 ---------------------------------------------------------------------------------- 2
from transformers import DataCollatorWithPadding, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np

#2.1
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

#2.2
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    preds = np.argmax(predictions, axis=1)
    accuracy = (preds == labels).mean()
    return {"accuracy": accuracy}

#2.3
id2label = {0: "neg", 1: "pos"}
label2id = {"neg": 0, "pos": 1}
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2,
    id2label=id2label,
    label2id=label2id
)

#2.4 & #2.5
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    num_train_epochs=3,
    weight_decay=0.01,
)

#2.6
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset_tok,
    eval_dataset=val_dataset_tok,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

#2.7
trainer.train()

#3 ---------------------------------------------------------------------------------- 3
#3.1 
test_results = trainer.evaluate(test_dataset_tok)
print("Test results:", test_results)

#3.2 
from transformers import pipeline

sentiment_pipe = pipeline(
    "sentiment-analysis",
    model=trainer.model,
    tokenizer=tokenizer,
    device=0
)

texts = [
    "This movie was fantastic! I loved it.",
    "The film was boring and too long.",
    "An average experience, nothing special."
]

for text in texts:
    result = sentiment_pipe(text)
    print(f"Text: {text}\nResult: {result}\n")

#4 ---------------------------------------------------------------------------------- 4
#modify code for experiments