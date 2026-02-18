"""
Simple LLM Benchmark for M3 MacBook Air
Author: Jerome
Hardware: MacBook Air M3, 16GB RAM, 8-core GPU
"""

import time
import json
from datetime import datetime
import psutil
from mlx_lm import load, generate

def simple_benchmark():
    """
    Run a simple benchmark on M3 MacBook Air
    """
    
    print("=" * 60)
    print("M3 MacBook Air AI Benchmark")
    print("Hardware: MacBook Air M3, 16GB RAM, 8-core GPU")
    print("=" * 60)
    
    # Model to test (small and fast)
    model_name = "mlx-community/Llama-3.2-1B-Instruct-4bit"
    
    print(f"\n📦 Loading model: {model_name}")
    print("⏳ This may take 1-2 minutes the first time...")
    print("   (Downloading ~700MB model)")
    
    # Load the model
    model, tokenizer = load(model_name)
    
    print("✅ Model loaded successfully!")
    
    # Test prompt
    prompt = "What is artificial intelligence? Explain in 2 sentences."
    
    print(f"\n💬 Prompt: {prompt}")
    print("\n🤖 Generating response...\n")
    
    # Get starting metrics
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024**3  # Convert to GB
    
    # Time the generation
    start_time = time.time()
    
    response = generate(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_tokens=100,
        verbose=True  # Shows progress
    )
    
    end_time = time.time()
    
    # Calculate metrics
    total_time = end_time - start_time
    tokens = len(tokenizer.encode(response))
    tokens_per_second = tokens / total_time
    mem_after = process.memory_info().rss / 1024**3
    mem_used = mem_after - mem_before
    
    # Display results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Response: {response}")
    print(f"\n📊 Performance Metrics:")
    print(f"   • Total time: {total_time:.2f} seconds")
    print(f"   • Tokens generated: {tokens}")
    print(f"   • Speed: {tokens_per_second:.2f} tokens/second")
    print(f"   • Memory used: {mem_used:.2f} GB")
    
    # Save results
    results = {
        "hardware": "MacBook Air M3 16GB",
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response,
        "metrics": {
            "total_time_seconds": round(total_time, 2),
            "tokens_generated": tokens,
            "tokens_per_second": round(tokens_per_second, 2),
            "memory_used_gb": round(mem_used, 2)
        }
    }
    
    # Save to file
    output_file = f"data/raw/benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    print("\n✅ Benchmark complete!")
    print("=" * 60)

if __name__ == "__main__":
    simple_benchmark()
