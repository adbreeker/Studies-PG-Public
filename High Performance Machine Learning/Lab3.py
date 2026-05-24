#Lab 3: CPU Quantization
import os
import time
import psutil
import threading
import multiprocessing
import torch
import gc
import intel_extension_for_pytorch as ipex
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.profiler import profile, record_function, ProfilerActivity

MODEL_NAME = "Qwen/Qwen3-4B-Thinking-2507"
CONTEXT_LEN = 1000
DECODE_STEPS = 3

# Memory measurement
def monitor_memory(pid, stop_event, results):
    process = psutil.Process(pid)
    peak_rss = 0
    while not stop_event.is_set():
        try:
            current_rss = process.memory_info().rss
            if current_rss > peak_rss:
                peak_rss = current_rss
        except psutil.NoSuchProcess:
            break
        time.sleep(0.01)
    results['peak_rss_mb'] = peak_rss / (1024 * 1024) # Bytes to MB

# Inference and profiling
def run_inference_and_profile(model, input_ids, mode_name):
    pid = os.getpid()
    
    # Warmup 3 times
    for _ in range(3):
        with torch.no_grad():
            model.generate(input_ids, max_new_tokens=1, min_new_tokens=1)

    stop_event = threading.Event()
    mem_results = {}
    monitor_thread = threading.Thread(target=monitor_memory, args=(pid, stop_event, mem_results))
    
    print(f"\n[{mode_name}] Inference and profiling...")
    monitor_thread.start()
    start_time = time.time()

    # Profiling
    with profile(
        activities=[ProfilerActivity.CPU],
        record_shapes=False,
        profile_memory=False,
        with_stack=False
    ) as prof:
        with record_function(f"model_inference_{mode_name}"):
            with torch.no_grad():
                _ = model.generate(input_ids, max_new_tokens=DECODE_STEPS, min_new_tokens=DECODE_STEPS)

    end_time = time.time()
    stop_event.set()
    monitor_thread.join()

    # Results
    inference_time = end_time - start_time
    peak_rss_mb = mem_results.get('peak_rss_mb', 0)

    print(f"[{mode_name}] Inference time: {inference_time:.4f} s")
    print(f"[{mode_name}] Peak memory usage (RSS): {peak_rss_mb:.2f} MB")
    print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=15))

    # Trace export
    trace_path = f"./Traces/Lab3_{mode_name}.json"
    prof.export_chrome_trace(trace_path)
    print(f"[{mode_name}] Trace exported to {trace_path}\n")

#Task 0: FP16 baseline and memory measurement
def task0_fp16_baseline():
    print("\n\nFP16 Baseline:")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    input_ids = torch.randint(0, tokenizer.vocab_size, (1, CONTEXT_LEN), dtype=torch.long)

    #Loading model in FP16
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16)
    model.eval()

    run_inference_and_profile(model, input_ids, "FP16_Baseline")

    del model
    gc.collect()

#Task 1: Full-model quantization with IPEX
def task1_int8_quantization():
    print("\n\nINT8 Quantization with IPEX:")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    input_ids = torch.randint(0, tokenizer.vocab_size, (1, CONTEXT_LEN), dtype=torch.long)

    #Loading model in native FP32 for quantization
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32, low_cpu_mem_usage=True)
    model.eval()

    # Quantization config
    qconfig_mapping = ipex.quantization.default_dynamic_qconfig_mapping
    # Prepare and convert the model to Quantized INT8
    prepared_model = ipex.quantization.prepare(model, qconfig_mapping, inplace=True)
    quantized_model = ipex.quantization.convert(prepared_model, inplace=True)

    # Clean up
    del model
    del prepared_model
    gc.collect()

    run_inference_and_profile(quantized_model, input_ids, "INT8_IPEX")

    del quantized_model
    gc.collect()

if __name__ == "__main__":
    #Task 0: FP16 baseline and memory measurement
    p1 = multiprocessing.Process(target=task0_fp16_baseline)
    p1.start()
    p1.join()

    #Task 1: Full-model quantization with IPEX
    p2 = multiprocessing.Process(target=task1_int8_quantization)
    p2.start()
    p2.join()
    
    #Task 2: Profiling and interpretation
    print("\nAll processes completed. \nCheck traces on https://ui.perfetto.dev/")