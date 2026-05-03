#Lab 1: Model profiling
import torch
from torch.profiler import profile, record_function, ProfilerActivity
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-4B-Thinking-2507"
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map=device, trust_remote_code=True)

#Task 1: Model Parameter Analysis
#___________________________________________________________________________________________________

#1.1 Estimate the total number of parameters in the model manually
V = model.config.vocab_size # Vocabulary size
DM = model.config.hidden_size # Model dimension - d_model
L = model.config.num_hidden_layers # Number of layers - n_layers
DFF = model.config.intermediate_size # Intermediate FFN Size - dff
QH = model.config.num_attention_heads # Attention Heads / Query Heads - n_heads
KVH = model.config.num_key_value_heads # Key/Value Heads
HD = model.config.head_dim # Head Dimension - d_head

#Basic estimation formula - 12 x n_layers x d_model^2
P_basic = 12 * L * DM**2
print(f"\nEstimated Total Parameters (Basic): {P_basic:,}")

embedding_layer = V * DM # 151936 x 2560 = 388,956,160
attention_per_layer = DM * ((QH*HD) + 2*(HD*KVH) + (QH*HD)) # 10,485,760 + 2,621,440 + 2,621,440 + 10,485,760 = 26,214,400
ffn_per_layer = 3*(DM * DFF) # 3 x 24,903,680 = 74,711,040
norm_per_layer = 2*DM # 2 x 2560 = 5,120

#P = Embeddings + Hidden Layers + Final Norm
P = embedding_layer + L * (attention_per_layer + ffn_per_layer + norm_per_layer) + DM
print(f"Estimated Total Parameters (Manual): {P:,}")

#1.2 Check the total number of parameters in PyTorch. 
total_params = sum(p.numel() for p in model.parameters())
print(f"Total Parameters (PyTorch): {total_params:,}")

#1.3 Print all parameter sizes and their corresponding names using PyTorch.
print(f"\n{'Parameter Name':<60} | {'Shape':<25} | {'Count'}")
print("-" * 105)

for name, param in model.named_parameters():
    shape_str = str(list(param.size()))
    param_count = param.numel()
    print(f"{name:<60} | {shape_str:<25} | {param_count:,}")



#Task 2: Profiling with PyTorch and Perfetto
#___________________________________________________________________________________________________

#Create two profiles for a single inference step (batch size=1,context len=1000, num new tokens=20)
input_ids = torch.randint(0, model.config.vocab_size, (1, 1000)).to(device)

#Warm-up
print("\nRunning warm-up...")
for _ in range(3):
    _ = model.generate(input_ids, max_new_tokens=20)

#2.1 Use the torch.profiler table to identify the longest running operations (CPU) and kernels (GPU).
print("Profiling...")
with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    record_shapes=True,
    profile_memory=False,
    with_stack=True
) as prof:
    with record_function("model_inference"):
        # Generate exactly 20 new tokens
        model.generate(input_ids, max_new_tokens=20)

print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=15)) #CPU
print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=15)) #GPU

#2.2 Export for Perfetto (https://ui.perfetto.dev/)
prof.export_chrome_trace("qwen_trace.json")