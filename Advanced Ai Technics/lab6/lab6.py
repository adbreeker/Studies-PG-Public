import os
from datasets import load_dataset
from transformers import AutoTokenizer

#1 ---------------------------------------------------------------------------------- 1
#1.1 
wnut = load_dataset("wnut_17")
print(wnut)

#1.2 
labels = wnut["train"].features["ner_tags"].feature.names
id2label = {i: label for i, label in enumerate(labels)}
label2id = {label: i for i, label in enumerate(labels)}
print("Labels:", labels)
print("id2label:", id2label)
print("label2id:", label2id)

#1.3 
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

#2 ---------------------------------------------------------------------------------- 2
#2.1-2.4 
def preprocess_function(examples):
    tokenized_inputs = tokenizer(
        examples["tokens"],
        truncation=True,
        max_length=tokenizer.model_max_length
    )
    labels_batch = examples["ner_tags"]
    new_labels = []
    for i, labels in enumerate(labels_batch):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  #special tokens
            elif word_idx != previous_word_idx:
                label_ids.append(labels[word_idx])  #first subword
            else:
                label_ids.append(-100)  #subsequent subwords
            previous_word_idx = word_idx
        new_labels.append(label_ids)
    tokenized_inputs["labels"] = new_labels
    return tokenized_inputs

tokenized_wnut = wnut.map(preprocess_function, batched=True)

#3 ---------------------------------------------------------------------------------- 3
import numpy as np
import evaluate

#3.1-3.5 
seqeval = evaluate.load("seqeval")

def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [
        [id2label[pred] for (pred, lab) in zip(prediction, label) if lab != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [id2label[lab] for (pred, lab) in zip(prediction, label) if lab != -100]
        for prediction, label in zip(predictions, labels)
    ]
    results = seqeval.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

#4 ---------------------------------------------------------------------------------- 4
from transformers import DataCollatorForTokenClassification, AutoModelForTokenClassification, TrainingArguments, Trainer

#4.1 
data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

model = AutoModelForTokenClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id
)

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

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_wnut["train"],
    eval_dataset=tokenized_wnut["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

#4.2 
trainer.train()
test_results = trainer.evaluate(tokenized_wnut["test"])
print("Test results:", test_results)

#5 ---------------------------------------------------------------------------------- 5
from transformers import pipeline
import spacy
from spacy.tokens import Doc
from spacy import displacy

model_save_path = "./wnut17_ner_results/best_model"
trainer.save_model(model_save_path)

text = ("The Golden State Warriors are an American "
        "professional basketball team based in San Francisco.")

classifier = pipeline("ner", model=model_save_path, tokenizer=tokenizer, aggregation_strategy="simple")
entities = classifier(text)

nlp = spacy.blank("en")
doc = nlp.make_doc(text)
spans = []
for ent in entities:
    span = doc.char_span(ent["start"], ent["end"], label=ent["entity_group"])
    if span is not None:
        spans.append(span)
doc.ents = spans

# displacy.render(doc, style="ent", jupyter=True)
displacy.serve(doc, style="ent")
print("Entities:", entities)
