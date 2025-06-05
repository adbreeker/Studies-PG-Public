import torch
import numpy as np
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM

#1 --------------------------------------------------
#1.1 Load the dataset
dataset = load_dataset("tcltcl/small-simple-wikipedia")
texts = dataset['train']['text']

#1.2 Define chunking parameters
chunk_size = 200
overlap = 50

#1.3 Chunk the dataset
chunks = []
for text in texts:
    words = text.split()
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

#2---------------------------------------------------
#2.1 Import SentenceTransformer
from sentence_transformers import SentenceTransformer

#2.2 Load the embeddings model
retriever_model = SentenceTransformer("all-MiniLM-L6-v2")

#2.3 Create embeddings for chunks
embeddings = retriever_model.encode(chunks)

#3---------------------------------------------------
#3.1 Create a retriever function
def retriever(question):
    #3.2 Calculate question embedding
    question_embedding = retriever_model.encode([question])
    
    #3.3 Calculate similarity between question and all chunks
    similarities = retriever_model.similarity(question_embedding, embeddings)
    
    #3.4 Retrieve the best matching chunk
    best_chunk_idx = np.argmax(similarities)
    return chunks[best_chunk_idx]

#4---------------------------------------------------
#4.1 Load the model
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-beta")
model = AutoModelForCausalLM.from_pretrained(
    "HuggingFaceH4/zephyr-7b-beta",
    torch_dtype=torch.float16,
    device_map="auto"
)

#4.2 Prepare the model prompt function
def create_prompt(question, retrieved_context):
    return f"<|user|>\nUse the following context to answer the question.\n\nContext: {retrieved_context}\n\nQuestion: {question}\n<|assistant|>"

def rag_answer(question):
    # Get context using retriever
    retrieved_context = retriever(question)
    
    # Create prompt
    prompt = create_prompt(question, retrieved_context)
    
    #4.3 Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    #4.4 Generate output
    output = model.generate(**inputs)
    
    #4.5 Decode response
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    
    #4.6 Get last model response
    answer = answer.split("<|assistant|>")[-1].strip()
    
    return answer

# Example usage
if __name__ == "__main__":
    question = "What is artificial intelligence?"
    answer = rag_answer(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")