# Lab 4: GPU Quantization with ModelOpt
import os
import time
import warnings

# Disabling logs and warnings
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
warnings.filterwarnings("ignore")

import torch
import gc
import torch.multiprocessing as mp
from transformers import AutoModelForCausalLM, AutoTokenizer
import modelopt.torch.quantization as mtq


MODEL_NAME = "Qwen/Qwen3-4B-Thinking-2507"
CONTEXT_LEN = 1000
DECODE_STEPS = 3

# Inference and memory measures
def run_inference(model, input_ids, mode_name):
    input_ids = input_ids.to("cuda")
    attention_mask = torch.ones_like(input_ids).to("cuda") # Eliminuje log o attention_mask
    
    # Warmup
    for _ in range(3):
        with torch.no_grad():
            model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=1)

    # Cleanup 
    torch.cuda.synchronize()
    gc.collect()
    torch.cuda.empty_cache() 
    torch.cuda.reset_peak_memory_stats()

    print(f"\n[{mode_name}] Inference running...")
    start_time = time.time()

    with torch.no_grad():
        _ = model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=DECODE_STEPS, min_new_tokens=DECODE_STEPS)

    torch.cuda.synchronize()
    end_time = time.time()

    inference_time = end_time - start_time
    peak_mem_mb = torch.cuda.max_memory_allocated() / (1024 * 1024) # Bytes to MB

    print(f"[{mode_name}] Inference time: {inference_time:.4f} s")
    print(f"[{mode_name}] Peak GPU memory usage: {peak_mem_mb:.2f} MB")
    print("_" * 50)

# Dummy calibration loop for ModelOpt quantization
def dummy_calibration_loop(model):
    for _ in range(4):
        dummy_input = torch.randint(0, 32000, (1, 512), device="cuda")
        with torch.no_grad():
            model(dummy_input)

#Task 0: FP16 baseline and GPU memory measurement
def task0_fp16_baseline():
    print("\n\nFP16 Baseline:")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    input_ids = torch.randint(0, tokenizer.vocab_size, (1, CONTEXT_LEN), dtype=torch.long)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        dtype=torch.float16,
        device_map="cuda"
    )
    model.eval()

    run_inference(model, input_ids, "FP16_Baseline")
    
#Task 1: Fixed quantization recipes with ModelOpt 
def task1_fixed_recipes(recipe, name):
    print(f"\n\nFixed Recipe [{name}]:")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    input_ids = torch.randint(0, tokenizer.vocab_size, (1, CONTEXT_LEN), dtype=torch.long)

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.float16, device_map="cuda")
    model.eval()
    
    model = mtq.quantize(model, recipe, forward_loop=dummy_calibration_loop)
    run_inference(model, input_ids, f"Quantized_{name}")

#Task 2: AutoQuantize with mixed recipes
def task2_auto_quantize():
    print("\n\nAutoQuantize (Mixed Recipes):")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    input_ids = torch.randint(0, tokenizer.vocab_size, (1, CONTEXT_LEN), dtype=torch.long)

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.float16, device_map="cuda")
    model.eval()

    dummy_loader = [
        {
            "input_ids": torch.randint(0, 32000, (1, 512), device="cuda"),
            "labels": torch.randint(0, 32000, (1, 512), device="cuda")
        }
        for _ in range(4)
    ]

    def forward_step(model, batch):
        with torch.no_grad():
            return model(**batch)

    def forward_backward_step(model, batch):
        model.zero_grad()
        loss = model(**batch).loss
        loss.backward()
        return loss

    model, _ = mtq.auto_quantize(
        model,
        constraints={"effective_bits": 5.0}, 
        quantization_formats=[mtq.FP8_DEFAULT_CFG, mtq.INT4_AWQ_CFG],
        data_loader=dummy_loader,
        forward_step=forward_step,
        forward_backward_step=forward_backward_step,
        num_calib_steps=4,
        num_score_steps=4
    )

    run_inference(model, input_ids, "AutoQuantize_Mixed")

if __name__ == "__main__":
    mp.set_start_method('spawn', force=True)

    #Task 0: FP16 baseline and GPU memory measurement
    p0 = mp.Process(target=task0_fp16_baseline)
    p0.start() 
    p0.join()

    #Task 1: Fixed quantization recipes with ModelOpt 
    for recipe, name in [(mtq.FP8_DEFAULT_CFG, "FP8_Default"), (mtq.INT8_SMOOTHQUANT_CFG, "INT8_SMOOTHQUANT"), (mtq.INT4_AWQ_CFG, "INT4_AWQ")]:
        p1 = mp.Process(target=task1_fixed_recipes, args=(recipe, name))
        p1.start() 
        p1.join()
    
    #Task 2: AutoQuantize with mixed recipes
    p2 = mp.Process(target=task2_auto_quantize)
    p2.start()
    p2.join()
    
    print("\nAll GPU inference processes completed.")