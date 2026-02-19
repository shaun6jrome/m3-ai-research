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

---

## Architectural Discussion

### Unified Memory Advantage

Apple’s unified memory architecture eliminates discrete CPU–GPU memory duplication.

For transformer inference workloads:

- Model weights are shared across compute units  
- No PCIe transfer overhead  
- Reduced memory bandwidth bottlenecks  
- Improved energy efficiency per token  

This directly contributes to the stable scaling behavior observed between 3B and 7B models.

---

### Fanless Thermal Envelope Stability

The MacBook Air M3 is a fanless system.

Despite sustained 7B inference:

- Thermal pressure remained Nominal  
- No observable throughput degradation  
- Power fluctuations did not cause throttling  

This demonstrates effective dynamic frequency scaling and significant thermal headroom within Apple Silicon’s efficiency-oriented architecture.

---

### Silicon-Level Tradeoffs

Observations:

- Throughput scales sub-linearly with parameter size  
- Energy cost scales super-linearly  
- Memory usage increases modestly relative to model size  

Implication:

Apple Silicon’s architectural design favors moderate transformer scales (≤3B parameters) for optimal performance-per-watt under consumer thermal envelopes.

While 7B models remain thermally stable, they incur significantly higher energy cost per token compared to 3B models.
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
## Key Findings

• 7B models reduce throughput by ~2.3x compared to 3B
• Energy cost per token increases ~3.3x
• Unified memory allows both models to run without swap
• No sustained thermal throttling observed over 30-minute stress test
• Performance-per-watt degrades non-linearly with model scale

---
## Statistical Summary (3B vs 7B)

### 3B Model
- Average Throughput: 20.6 tokens/sec
- Average Combined Power: 72 mW
- Energy per Token: 3.5 mW/token
- Average Memory Used: 8.8 GB
- Sustained Thermal Pressure: Nominal

### 7B Model
- Average Throughput: 9.1 tokens/sec
- Average Combined Power: 105 mW
- Energy per Token: 11.6 mW/token
- Average Memory Used: 9.8 GB
- Sustained Thermal Pressure: Nominal

### Efficiency Comparison

- 7B consumes ~3.3x more energy per token than 3B.
- Throughput drops ~2.2x when scaling from 3B to 7B.
- Memory increases modestly (~1 GB increase) despite parameter scaling.
- Thermal stability remained Nominal in all sustained tests.

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



