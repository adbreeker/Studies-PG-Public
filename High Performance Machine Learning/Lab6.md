## Lab6: Distributed Inference with vLLM

Create and use a new .venv with [requirements_labs56.txt](https://github.com/adbreeker/Studies-PG-Public/blob/main/High%20Performance%20Machine%20Learning/requirements_labs56.txt). Then:

### 1. Starting ray cluster on head node

On the head node:
```
ray start --head --port=6379
```

### 2. Joining workers to set ray cluster

On each worker node:
```
ray start --address=<HEAD_NODE_IP>:6379
```

### 3. Downloading chosen model

On each node:
```
mkdir -p ~/models/Qwen3-4B-Thinking-2507
cd ~/models/Qwen3-4B-Thinking-2507
huggingface-cli download Qwen/Qwen3-4B-Thinking-2507
```

### 4. Spreading the model across available GPUs

On the head node:
```
vllm serve Qwen/Qwen3-4B-Thinking-2507 --tensor-parallel-size 2 --distributed-executor-backend ray --max_model_len=8192 --max-num-seqs 32 --gpu-memory-utilization 0.65
```

### 5. Testing a distributed inference

On the head node:
```
curl http://localhost:8000/v1/completions \
-X POST \
-H "Content-Type:␣application/json" \
-d ’{"prompt":␣"Hello,␣how␣can␣I␣assist␣you␣today?",␣"
max_tokens":␣50}’
```