# Lab 0: Lab introduction
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# 5. Run everything on gpu.
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"\nUsing device: {device}")


# 2. Run inference on Qwen/Qwen3-4B-Thinking-2507 model.
model_name = "Qwen/Qwen3-4B-Thinking-2507" 

# 2. Do not use transformers.pipelines - load the tokenizer and run the generate function by yourself.
print(f"\nLoading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 3. Convert the model to fp32 if it’s in other format by default.
print(f"\nLoading model in fp32...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.float16, 
    device_map=device
)

# 4. Write prompt that has exactly 20 tokens.
raw_text = "In this laboratory exercise, we are going to explore the fundamental principles of running large language models locally using PyTorch."
messages = [
    {"role": "user", "content": raw_text}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)
encoded_inputs = tokenizer([text], return_tensors="pt")

input_ids = encoded_inputs.input_ids[:, :20].to(device)

token_count = input_ids.shape[1]
print(f"\nPrompt token count: {token_count}")

actual_prompt = tokenizer.decode(input_ids[0])
print(f"Actual prompt used: '{actual_prompt}'")

# 4. Learn about parameters of generate function and set them so that you are doing the same amount of computation each time.
fixed_generation_length = 20
generate_params = {
    "input_ids": input_ids,
    "temperature" : 0,
    "max_new_tokens": fixed_generation_length, 
    "min_new_tokens": fixed_generation_length, 
    "do_sample": False, 
}

# 2. Run the generate function by yourself.
print("\nRunning generation...")
with torch.no_grad():
    output_ids = model.generate(**generate_params)

generated_ids = output_ids[0]
generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

print("\n--- Generated Output ---")
print(generated_text)