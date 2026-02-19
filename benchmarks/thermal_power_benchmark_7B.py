import time
import json
import subprocess
from datetime import datetime
import psutil
from mlx_lm import load, generate
model_name = "mlx-community/Qwen2.5-7B-Instruct-4bit"
NUM_GENERATIONS = 50

print("Loading model...")
model, tokenizer = load(model_name)

prompt = "Explain unified memory architecture in simple terms."

results = []

print("Starting aligned power sampling test...")

for i in range(NUM_GENERATIONS):

    gen_start = time.time()
    output = generate(model, tokenizer, prompt, max_tokens=100)
    gen_end = time.time()

    tokens_per_sec = 100 / (gen_end - gen_start)

    # Immediately sample power after generation
    power_output = subprocess.check_output(
        ["sudo", "powermetrics", "--samplers", "cpu_power,gpu_power,thermal", "-n", "1"],
        text=True
    )

    combined_power = None
    cpu_power = None
    gpu_power = None
    thermal_pressure = None

    for line in power_output.splitlines():
        if "Combined Power" in line:
            combined_power = float(line.split(":")[1].strip().split()[0])
        elif "CPU Power" in line and "Combined" not in line:
            cpu_power = float(line.split(":")[1].strip().split()[0])
        elif "GPU Power" in line:
            gpu_power = float(line.split(":")[1].strip().split()[0])
        elif "Current pressure level" in line:
            thermal_pressure = line.split(":")[1].strip()

    entry = {
        "iteration": i,
        "timestamp": datetime.now().isoformat(),
        "tokens_per_sec": tokens_per_sec,
        "combined_power_mW": combined_power,
        "cpu_power_mW": cpu_power,
        "gpu_power_mW": gpu_power,
        "thermal_pressure": thermal_pressure,
        "memory_used_GB": psutil.virtual_memory().used / (1024 ** 3)
    }

    results.append(entry)

    print(f"[Iter {i}] "
          f"{tokens_per_sec:.2f} tok/s | "
          f"{combined_power} mW | "
          f"GPU: {gpu_power} mW | "
          f"Thermal: {thermal_pressure}")

with open("aligned_power_results_3B.json", "w") as f:
    json.dump(results, f, indent=2)

print("Aligned test completed. Results saved.")
