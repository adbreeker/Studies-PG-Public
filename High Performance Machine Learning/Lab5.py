# Lab 5: KV Cache Management and Offloading with vLLM and LMCache
import sys
import os
import time
import torch
from transformers import AutoConfig

os.environ.setdefault("VLLM_USE_FLASHINFER_SAMPLER", "0")

MODEL_NAME = "Qwen/Qwen3-4B-Thinking-2507"
VOCAB_SIZE = 32000
DECODE_STEPS = 3
MAX_MODEL_LEN = 16000

def get_dummy_prompt(length):
    return "The quick brown fox jumps over the lazy dog. " * (length // 10 + 1)

# Task 0: Theoretical KV Cache Estimate and Baseline Run
def task_0():
    print("\nTask 0: Theoretical KV Cache Estimate and Baseline Run")

    # Theoretical Calculation
    config = AutoConfig.from_pretrained(MODEL_NAME, trust_remote_code=True)
    L = config.num_hidden_layers
    H_kv = config.num_key_value_heads
    D = config.head_dim
    b = 2 # 2 bytes for FP16/BF16
    
    kv_per_token = 2 * L * H_kv * D * b
    print(f"[Task 0] KV cache size per token: {kv_per_token} bytes ({kv_per_token / 1024:.2f} KiB)")
    
    total_gpu_mem_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"[Task 0] Total GPU Memory: {total_gpu_mem_gb:.2f} GB")
    # Assuming ~10GB for model weights and overhead
    estimated_remaining_bytes = (total_gpu_mem_gb - 10) * (1024**3)
    print(f"[Task 0] Estimated remaining memory for KV cache: {estimated_remaining_bytes / (1024**3):.2f} GB")
    estimated_tokens = estimated_remaining_bytes / kv_per_token
    print(f"[Task 0] Rough estimate of tokens that fit in remaining memory: ~{int(estimated_tokens):,}")

    # Baseline Run
    print("\n[Task 0] Initializing vLLM Baseline...")
    from vllm import LLM, SamplingParams
    
    llm = LLM(
        model=MODEL_NAME,
        dtype=torch.float16,
        trust_remote_code=True,
        gpu_memory_utilization=0.8,
        max_model_len=MAX_MODEL_LEN,
    )
    sampling_params = SamplingParams(max_tokens=DECODE_STEPS, min_tokens=DECODE_STEPS, temperature=0)
    prompt = get_dummy_prompt(1000)

    torch.cuda.reset_peak_memory_stats()
    start_time = time.time()
    
    outputs = llm.generate([prompt], sampling_params)
    
    inference_time = time.time() - start_time
    free_mem, total_mem = torch.cuda.mem_get_info()
    peak_mem_alloc = torch.cuda.max_memory_allocated() / (1024**3)
    peak_mem_res = torch.cuda.max_memory_reserved() / (1024**3)
    used_mem_gb = (total_mem - free_mem) / (1024**3)

    print(f"\n[Task 0] Prefill: 1000 tokens, Decode: 3 tokens")
    print(f"[Task 0] Inference Time: {inference_time:.4f} seconds")
    print(f"[Task 0] Peak GPU Memory Allocated: {peak_mem_alloc:.4f} GB")
    print(f"[Task 0] Peak GPU Memory Reserved: {peak_mem_res:.4f} GB")
    print(f"[Task 0] Used GPU Memory: {used_mem_gb:.4f} GB")

# Task 1: Empirical KV Cache Limit Without LMCache
def task_1():
    print("\nTask 1: Empirical KV Cache Limit Without LMCache")
    from vllm import LLM
    
    test_lengths = [1000, 8000, 12000, 16000, 20000, 240000, 28000, 32000, 64000, 128000, 256000]
    best_length = 0
    for index, length in enumerate(test_lengths):
        print(f"\n[Task 1] Testing with {length} tokens...")
        try:
            llm = LLM(
                model=MODEL_NAME,
                dtype=torch.float16,
                trust_remote_code=True,
                gpu_memory_utilization=0.8,
                max_model_len=length,
            )
        except RuntimeError as e:
            print(f"[Task 1] RuntimeError at {length} tokens: {e}")
            best_length = index - 1
            break
             
    print(f"\n[Task 1] The empirical limit is between {test_lengths[best_length]} and {test_lengths[best_length + 1]} tokens.")

# Task 2: KV Cache Offloading and Reuse with LMCache
def task_2():
    print("\nTask 2: KV Cache Offloading and Reuse with LMCache")
    # Enable LMCache locally via environment variables before importing vLLM
    os.environ["LMCACHE_USE_LOCAL"] = "1"
    os.environ["LMCACHE_LOCAL_CPU"] = "1" # Instructs LMCache to use CPU offloading
    
    from vllm import LLM, SamplingParams
    
    llm = LLM(
        model=MODEL_NAME,
        dtype=torch.float16,
        trust_remote_code=True,
        gpu_memory_utilization=0.8,
        max_model_len=MAX_MODEL_LEN,
    )
    sampling_params = SamplingParams(max_tokens=10, min_tokens=10, temperature=0)
    
    # A massive shared prefix
    shared_prefix = get_dummy_prompt(4000)

    # Running prompts with same prefix to test cache reuse and offloading
    prompt_1 = shared_prefix + "\nQuestion: What is the capital of France?"
    prompt_2 = shared_prefix + "\nQuestion: What is the capital of Poland?"
    prompt_3 = shared_prefix + "\nQuestion: What is the capital of Germany?"
    prompt_4 = shared_prefix + "\nQuestion: What is the capital of Italy?"
    prompt_5 = shared_prefix + "\nQuestion: What is the capital of Spain?"

    prompts = [prompt_1, prompt_2, prompt_3, prompt_4, prompt_5]
    times = []

    for i, prompt in enumerate(prompts):
        print(f"\n[Task 2] Run {i+1} with prompt: Shared Prefix + '{prompt.splitlines()[-1]}'")
        start_time = time.time()
        llm.generate([prompt], sampling_params)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        print(f"[Task 2] Run {i+1} Time: {elapsed_time:.4f} seconds")

    print("\n[Task 2] Summary:")
    for i, t in enumerate(times):
        print(f"Run {i+1}: {t:.4f} seconds")


if __name__ == "__main__":
    try:
        task_num = int(sys.argv[1])
    except ValueError:
        print("Error during task number parsing")
        sys.exit(1)

    # Route to the correct function
    if task_num == 0:
        task_0()
    elif task_num == 1:
        task_1()
    elif task_num == 2:
        task_2()
    else:
        print("Invalid task number")
        sys.exit(1)