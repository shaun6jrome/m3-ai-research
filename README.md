## Architectural Evaluation of On-Device LLM Inference  
### Apple Silicon M3 (16GB Unified Memory)

---

## Abstract

This project evaluates the architectural performance characteristics of on-device Large Language Model (LLM) inference on Apple Silicon M3 (16GB unified memory).  

We benchmark 1B, 3B, and 7B parameter models using Apple’s MLX framework to analyze:

- Throughput scaling (tokens/sec)
- Power consumption behavior
- Energy cost per token
- Unified memory utilization
- Sustained thermal stability under load

The goal is to study hardware–software co-design implications of consumer-grade silicon running transformer-scale inference workloads locally.

---

## Hardware Configuration

- Device: MacBook Air M3 (Fanless)
- CPU: 8-core (4 Performance + 4 Efficiency)
- GPU: 8-core integrated
- Memory: 16GB Unified Memory
- OS: macOS 15.2
- Framework: MLX (Apple Silicon optimized)

---

## Experimental Methodology

- 4-bit quantized models (MLX community)
- Local inference (no cloud acceleration)
- Power measured via `powermetrics`
- CPU + GPU combined power tracked
- Thermal pressure monitored
- Sustained 30-minute load test for 7B model
- Multiple iterations averaged for statistical stability

---

## Models Evaluated

| Model | Parameters | Quantization |
|-------|------------|--------------|
| Llama 3.2 1B | 1 Billion | 4-bit |
| Qwen 2.5 3B | 3 Billion | 4-bit |
| Qwen 2.5 7B | 7 Billion | 4-bit |

---

## Key Metrics

- Average tokens/sec
- Average combined power (mW)
- Energy per token (mW/token)
- Peak memory usage (GB)
- Thermal pressure behavior
- Sustained performance stability# Apple Silicon M3 AI Research

Benchmarking on-device LLM inference performance on MacBook Air M3 (16GB).

## Hardware

- Device: MacBook Air M3 (2024)
- Memory: 16GB Unified Memory
- CPU: 8-core (4 performance + 4 efficiency)
- GPU: 8-core
- macOS: 15.2

## Baseline Benchmark (1B Model)

Model: mlx-community/Llama-3.2-1B-Instruct-4bit

Performance:
- Speed: 37.95 tokens/sec
- Total time: 2.69 seconds
- Peak memory: 0.717 GB
- Tokens generated: 102

## Methodology

- Framework: Apple MLX
- Quantization: 4-bit
- Local inference (no cloud)
- Single prompt test


---

## Results Summary

### Average Performance Comparison

| Model | Avg Tokens/sec | Avg Power (mW) | Energy per Token (mW/token) | Avg Memory (GB) |
|-------|----------------|----------------|-----------------------------|-----------------|
| 3B | ~20 tok/s | ~68 mW | ~3.4 | ~8.8 |
| 7B | ~9 tok/s | ~120–200 mW (variable) | Higher than 3B | ~9.8 |

> Note: Power variability observed due to dynamic frequency scaling and workload bursts.

### Observations

- 3B model achieves significantly higher throughput than 7B.
- 7B shows sublinear scaling relative to parameter increase.
- GPU contribution increases under heavier load.
- Unified memory usage scales modestly between 3B and 7B.
- Thermal pressure remained **Nominal** even during sustained testing.


---

## Systems-Level Analysis

### 1. Scaling Behavior

The transition from 3B to 7B does not produce linear throughput degradation proportional to parameter increase.  
Instead, performance decreases by roughly ~2x while parameter count increases by >2x.

This suggests:

- Memory bandwidth and cache locality play significant roles.
- Unified memory architecture reduces memory copy overhead.
- Apple’s hardware–software co-design benefits inference workloads.

---

### 2. Power Efficiency

Energy per token increases with model size.

However:

- Power spikes stabilize quickly.
- Dynamic frequency scaling adapts to workload.
- GPU utilization increases for 7B, indicating heterogeneous workload balancing.

This demonstrates effective silicon-level power management.

---

### 3. Thermal Envelope

Despite sustained 7B inference:

- Thermal pressure remained Nominal.
- No visible throttling occurred.
- Throughput remained stable over time.

This validates Apple Silicon’s thermal design efficiency, even in fanless systems.

---

### 4. Unified Memory Implications

The modest increase in memory usage from 3B to 7B highlights:

- Efficient quantization impact
- Reduced duplication between CPU and GPU memory pools
- Architectural advantages over discrete GPU memory systems

Unified memory appears well-suited for medium-scale transformer inference.

---

## Conclusion

This study demonstrates that Apple Silicon M3 (16GB unified memory) can sustain medium-scale LLM inference (up to 7B parameters) locally without thermal throttling, even in a fanless MacBook Air configuration.

Key findings:

- Throughput scales sublinearly with model size.
- Energy cost per token increases with parameter count.
- Power management dynamically stabilizes under sustained load.
- Thermal pressure remains nominal during extended inference.
- Unified memory enables efficient CPU–GPU workload interaction.

These results highlight the strength of Apple’s hardware–software co-design philosophy for on-device AI workloads.

---

## Future Work

Future experiments may include:

- 13B parameter feasibility testing
- Memory bandwidth saturation analysis
- CPU vs GPU workload partitioning breakdown
- Token latency distribution profiling
- Comparative evaluation against x86 + discrete GPU systems
- ANE (Neural Engine) acceleration study

---

## Repository Structure
```
m3-ai-research/
├── benchmarks/              # Benchmark scripts
├── results/
│   └── charts/              # Generated comparison plots
├── data/                    # Raw & processed data
├── thermal_power_results_3B.json
├── thermal_power_results_7B.json
├── sustained_7B_30min.json
└── README.md                # Research documentation```

---

## Author

Shaun Jerome
Independent Systems & AI Research
