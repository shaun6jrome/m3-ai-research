import time
import json
import subprocess
import psutil
from datetime import datetime
from mlx_lm import load, generate

MODEL_NAME = "mlx-community/Qwen2.5-7B-Instruct-4bit"

print("Loading model...")
model, tokenizer = load(MODEL_NAME)

print("Starting 30-minute sustained test...")
start_time = time.time()

results = []

DURATION_MINUTES = 30

iteration = 0

while (time.time() - start_time) < DURATION_MINUTES * 60:
    iteration += 1
    
    t0 = time.time()
    output = generate(
        model,
        tokenizer,
        prompt="Explain how silicon-level power management works.",
        max_tokens=100,
        verbose=False
    )
    t1 = time.time()

    tokens_per_sec = 100 / (t1 - t0)

    # Get power + thermal data
    proc = subprocess.run(
        ["sudo", "powermetrics", "--samplers", "cpu_power,gpu_power,thermal", "-n", "1"],
        capture_output=True,
        text=True
    )

    combined_power = None
    cpu_power = None
    gpu_power = None
    thermal_pressure = None

    for line in proc.stdout.split("\n"):
        if "Combined Power" in line:
            combined_power = float(line.split(":")[1].strip().split()[0])
        elif "CPU Power" in line and "Combined" not in line:
            cpu_power = float(line.split(":")[1].strip().split()[0])
        elif "GPU Power" in line:
            gpu_power = float(line.split(":")[1].strip().split()[0])
        elif "Current pressure level" in line:
            thermal_pressure = line.split(":")[1].strip()

    entry = {
        "iteration": iteration,
        "elapsed_minutes": (time.time() - start_time) / 60,
        "tokens_per_sec": tokens_per_sec,
        "combined_power_mW": combined_power,
        "cpu_power_mW": cpu_power,
        "gpu_power_mW": gpu_power,
        "thermal_pressure": thermal_pressure,
        "memory_used_GB": psutil.virtual_memory().used / (1024 ** 3)
    }

    results.append(entry)

    print(f"[Iter {iteration}] "
          f"{tokens_per_sec:.2f} tok/s | "
          f"{combined_power} mW | "
          f"Thermal: {thermal_pressure}")

with open("sustained_7B_30min.json", "w") as f:
    json.dump(results, f, indent=2)

print("Sustained test completed. Results saved.")
