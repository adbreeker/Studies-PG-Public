# Advanced AI Technics

This repository contains hands-on labs for modern AI workflows, centered on transformer-based NLP and one graph-learning lab using PyTorch Geometric.

The material moves from text generation and model compression, through PEFT fine-tuning, to downstream tasks such as sentiment analysis, NER, and a simple RAG pipeline.

## 🎯 Course Scope

- Transformer text generation and prompting
- 4-bit quantization for large language models
- PEFT/LoRA fine-tuning workflows
- Graph node classification (Cora, GCN/GAT/MLP)
- Sentiment analysis and token classification
- Retrieval-Augmented Generation with embeddings + generation model

## 📁 Repository Structure

```text
lab1/  Lab1.ipynb
lab2/  Lab2.ipynb
lab3/  Lab3.ipynb
lab4/  data_processing.py, models.py, full_batch_training.py, sampling_training.py
lab5/  Lab5.ipynb, Lab5_Experiments.ipynb, lab5.py
lab6/  lab6.ipynb, lab6.py
lab7/  lab7.ipynb, lab7.py
```

## 📋 Prerequisites

### Software

- Python 3.8+
- Jupyter Notebook
- CUDA-capable GPU (recommended for larger models)

### Core Python Libraries

- torch
- transformers
- datasets
- peft
- trl
- bitsandbytes
- sentence-transformers
- evaluate
- seqeval
- spacy
- torch-geometric

## 🧪 Labs Overview

### Lab 1: Text Generation with GPT-2

Objective:
- Intro to causal language models and generation behavior.

What is implemented:
- Loading `openai-community/gpt2-large`
- Tokenization and text generation
- Basic generation experimentation with Hugging Face APIs

Key model:
- GPT-2 Large

### Lab 2: Quantization and Prompt Formatting

Objective:
- Run larger models with reduced memory footprint.

What is implemented:
- Loading `mistralai/Mistral-7B-v0.1`
- 4-bit quantization via `BitsAndBytesConfig(load_in_4bit=True)`
- Chat template formatting (`apply_chat_template`)
- PEFT adapter loading for inference

Key model:
- Mistral-7B

### Lab 3: PEFT Fine-Tuning with LoRA

Objective:
- Explore parameter-efficient fine-tuning on a causal LM.

What is implemented:
- LoRA config setup (`LoraConfig`)
- PEFT wrapping (`PeftModel` / `get_peft_model`)
- SFT workflow (`SFTTrainer`)
- Quantized base model loading

Key model:
- Llama-3.2-1B (gated model; access may be required)

### Lab 4: Graph Model Training Strategies (PyG)

Objective:
- Compare full-batch and sampled training on graph data.

What is implemented:
- Cora dataset loading via `Planetoid`
- Model classes for MLP/GCN/GAT in `models.py`
- Full-batch training script
- Sampling-based training script with `NeighborLoader`

Current status note:
- Parts of Lab 4 are scaffold-style templates (marked with placeholders), so this lab is currently less complete than Labs 1-3 and 5-7.

### Lab 5: Sentiment Analysis

Objective:
- Fine-tune transformer classifiers on movie reviews.

What is implemented:
- IMDB dataset (`stanfordnlp/imdb`)
- BERT fine-tuning in `lab5.py`
- Additional experiments notebook using DistilBERT
- Evaluation + inference examples

Key models:
- `bert-base-uncased`
- `distilbert-base-uncased` (experiments)

### Lab 6: Named Entity Recognition (NER)

Objective:
- Train and evaluate token classification with label alignment.

What is implemented:
- WNUT-17 dataset (`wnut_17`)
- Subword-to-label alignment handling (`-100` masking)
- `AutoModelForTokenClassification`
- Metrics with `seqeval`
- Optional visualization with spaCy displacy

### Lab 7: Retrieval-Augmented Generation (RAG)

Objective:
- Build a minimal end-to-end retrieval + generation pipeline.

What is implemented:
- Source corpus: `tcltcl/small-simple-wikipedia`
- Text chunking with overlap
- Embedding model: `all-MiniLM-L6-v2`
- Similarity-based retrieval of best chunk
- Response generation with `HuggingFaceH4/zephyr-7b-beta`

## 🔧 Practical Notes

- Labs 1-3 are primarily notebook-driven.
- Labs 5-7 have both notebook and script variants.
- Some models are large/gated, so login/authentication and sufficient VRAM may be needed.
- No dedicated `requirements.txt` is currently included in this folder; install dependencies manually based on the list above.

## 📈 Learning Progression

1. Transformer basics and generation
2. Efficient inference through quantization
3. PEFT/LoRA fine-tuning patterns
4. Graph learning training modes (full batch vs sampling)
5. Supervised NLP tasks (classification + NER)
6. Retrieval-augmented QA pipeline construction

## 📝 Summary

This repository documents practical AI coursework with emphasis on implementation and experimentation using Hugging Face and PyTorch ecosystems, plus graph-learning extensions in PyG.