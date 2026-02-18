# Apple Silicon M3 AI Research

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

## Project Structure
pwd
git add README.md
git commit -m "Add README with 1B benchmark results"
git push
