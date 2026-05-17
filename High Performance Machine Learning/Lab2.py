#Lab 2: Eager vs Compiled
import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.profiler import profile, record_function, ProfilerActivity
torch.set_float32_matmul_precision('high')

#Setup
MODEL_NAME = "Qwen/Qwen3-4B-Thinking-2507"

print(f"Loading model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, 
    dtype=torch.bfloat16, 
    device_map="cuda", 
    trust_remote_code=True
)
model.eval()

CONTEXT_LEN = 1000
DECODE_LEN = 20
WARMUP_ITERS = 3
MEASURE_ITERS = 10

prefill_input_ids = torch.randint(0, model.config.vocab_size, (1, CONTEXT_LEN), device="cuda")

#Measuring function for latency and kernel count
def measure_latency_and_kernels(model_fn, input_ids, phase_name, is_decode=False):
    """Measures execution time (20 tokens for decode) and counts CUDA kernels (1 pass)."""
    
    #Warmup
    for _ in range(WARMUP_ITERS):
        with torch.no_grad():
            if is_decode:
                decode_input = torch.randint(0, model.config.vocab_size, (1, 1), device="cuda")
                model_fn(decode_input)
            else:
                model_fn(input_ids)
            
    torch.cuda.synchronize()
    
    #Measure latency
    start_time = time.perf_counter()
    for _ in range(MEASURE_ITERS):
        with torch.no_grad():
            if is_decode:
                for _ in range(DECODE_LEN):
                    decode_input = torch.randint(0, model.config.vocab_size, (1, 1), device="cuda")
                    model_fn(decode_input)
            else:
                model_fn(input_ids)
                
    torch.cuda.synchronize()
    avg_time = (time.perf_counter() - start_time) / MEASURE_ITERS
    
    #Profiling
    with profile(activities=[ProfilerActivity.CUDA], record_shapes=False) as prof:
        with torch.no_grad():
            if is_decode:
                decode_input = torch.randint(0, model.config.vocab_size, (1, 1), device="cuda")
                model_fn(decode_input)
            else:
                model_fn(input_ids)
                
    #Count CUDA kernels (1 pass)
    kernel_count = 0
    for event in prof.key_averages():
        if event.device_time_total > 0 or "cuda" in str(event.device_type).lower():
            kernel_count += 1
    
    print(f"[{phase_name}] Avg Latency: {avg_time * 1000:.2f} ms | Kernels (1 pass): {kernel_count}")
    return avg_time, kernel_count

#------------------------------------------------------------------------------------------------------
#Task 1: Eager vs Compiled Execution

#1. Eager Execution
print("\n1.1 - Eager Execution:")
measure_latency_and_kernels(model, prefill_input_ids, "Eager - Prefill", is_decode=False)
measure_latency_and_kernels(model, prefill_input_ids, "Eager - Decode", is_decode=True)

#2. Compiled Execution
compiled_model = torch.compile(model)
print("\nCompiling model (this may take a while)...")
print("\n1.2 - Compiled Execution:")
measure_latency_and_kernels(compiled_model, prefill_input_ids, "Compiled - Prefill", is_decode=False)
measure_latency_and_kernels(compiled_model, prefill_input_ids, "Compiled - Decode", is_decode=True)

#------------------------------------------------------------------------------------------------------
#Task 2: Triton and Kernel Fusion (https://ui.perfetto.dev/)

print("\n2.1 - Generating Perfetto Trace...")
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], 
             with_stack=True, 
             on_trace_ready=torch.profiler.tensorboard_trace_handler('./Traces/')) as prof:
    with torch.no_grad():
        compiled_model(prefill_input_ids)
print("Trace saved to ./Traces/")

#------------------------------------------------------------------------------------------------------
#Task 3: CUDA Graphs and Autotuning

#1. Max-Autotune
print("\n3.1 - Recompiling with max-autotune...")
autotuned_model = torch.compile(model, mode="max-autotune")
measure_latency_and_kernels(autotuned_model, prefill_input_ids, "Max-Autotune - Prefill", is_decode=False)
measure_latency_and_kernels(autotuned_model, prefill_input_ids, "Max-Autotune - Decode", is_decode=True)

#2. CUDA Graphs
print("\n3.2 - Recompiling with CUDA Graphs...")
cudagraph_model = torch.compile(model, backend="inductor", options={"triton.cudagraphs": True})
measure_latency_and_kernels(cudagraph_model, prefill_input_ids, "CUDA Graphs - Prefill", is_decode=False)
measure_latency_and_kernels(cudagraph_model, prefill_input_ids, "CUDA Graphs - Decode", is_decode=True)