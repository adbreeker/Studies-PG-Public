import requests
import time
import json

# API Configuration
API_URL = "http://localhost:8000/v1/completions"
MODEL_NAME = "/models/Qwen3-4B-Thinking-2507"

def run_benchmark(prompt="Hello, how can I assist you today?", max_tokens=50):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": max_tokens
    }

    print(f"Sending request: '{prompt}' (Max tokens: {max_tokens})")
    
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to vLLM server: {e}")
        return

    end_time = time.time()
    latency = end_time - start_time
    
    data = response.json()
    generated_text = data['choices'][0]['text']
    usage = data['usage']
    
    # Calculate metrics
    generated_tokens = usage['completion_tokens']
    throughput = generated_tokens / latency if latency > 0 else 0

    print("\n--- Benchmark Results ---")
    print(f"Response: {generated_text.strip()}")
    print(f"Inference Latency: {latency:.4f} seconds")
    print(f"Tokens Generated: {generated_tokens}")
    print(f"Throughput: {throughput:.2f} tokens/second")
    print("-------------------------\n")
    print("Note: Check 'nvidia-smi' or 'ray status' in a separate terminal during generation to record peak GPU memory usage.")

if __name__ == "__main__":
    # Warmup run (optional, compiling kernels can make the first run slow)
    print("Performing warmup run...")
    run_benchmark(prompt="Warmup", max_tokens=10)
    
    # Actual measurement
    print("Performing actual measurement...")
    run_benchmark(prompt="Explain the theory of relativity in simple terms.", max_tokens=100)