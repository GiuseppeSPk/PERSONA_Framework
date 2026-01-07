import json
import os
import subprocess
import sys
import time
import re
import argparse
from llm_interface import get_provider

# PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_PATH = os.path.join(BASE_DIR, "data", "corpus.json")
AGENTS_DIR = os.path.join(BASE_DIR, "agents")
EXPERIMENT_DIR = os.path.join(BASE_DIR, "experiment")

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def clean_code_block(text):
    """
    Extracts code from markdown code blocks if present.
    """
    match = re.search(r'```python(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def run_pipeline(provider_type, model_name, limit=None):
    print(f"🚀 Starting PERSONA Socratic Loop (Provider: {provider_type}, Model: {model_name})")
    
    # 0. Initialize Provider
    try:
        llm = get_provider(provider_type, model_name)
    except Exception as e:
        print(f"❌ Failed to initialize provider: {e}")
        return

    # 1. Load Data
    with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    print(f"📚 Loaded {len(corpus)} scenarios.")
    
    if limit:
        corpus = corpus[:limit]
        print(f"⚠️ Limiting execution to first {limit} scenarios.")

    # 2. Load Agents
    ethicist_prompt = load_file(os.path.join(AGENTS_DIR, "ethicist.md"))
    reductionist_prompt = load_file(os.path.join(AGENTS_DIR, "reductionist.md"))
    
    # 3. Execution Loop
    for i, item in enumerate(corpus):
        scenario_id = item['id']
        context = item['context']
        
        print(f"\n[{i+1}/{len(corpus)}] Processing {scenario_id}...")
        
        # Setup Experiment Dir
        # Create a subfolder for the specific model run to support multi-model results
        scen_dir = os.path.join(EXPERIMENT_DIR, scenario_id, f"{provider_type}_{model_name.replace(':', '_')}")
        ensure_dir(scen_dir)
        
        # --- PHASE 1: ETHICIST (Rhetoric) ---
        print("   🗣️  Invoking Ethicist...", end='', flush=True)
        rhetoric = llm.generate(
            prompt=f"SCENARIO:\n{context}\n\nPlease provide your analysis.",
            system_prompt=ethicist_prompt
        )
        with open(os.path.join(scen_dir, "01_rhetoric_mask.txt"), "w", encoding='utf-8') as f:
            f.write(rhetoric)
        print(" Done.")
        
        # --- PHASE 2: REDUCTIONIST (Code) ---
        print("   💻 Invoking Reductionist...", end='', flush=True)
        raw_code_resp = llm.generate(
            prompt=f"SCENARIO:\n{context}\n\nWrite the Python code.",
            system_prompt=reductionist_prompt
        )
        code = clean_code_block(raw_code_resp)
        code_path = os.path.join(scen_dir, "02_procedural_logic.py")
        with open(code_path, "w", encoding='utf-8') as f:
            f.write(code)
        print(" Done.")
        
        # --- PHASE 3: EXECUTION (Truth) ---
        print("   ⚙️  Running Code...", end='', flush=True)
        try:
            # Run the generated code
            result = subprocess.run(
                [sys.executable, code_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout
            if result.stderr:
                output += "\n[STDERR]\n" + result.stderr
                
            log_path = os.path.join(scen_dir, "03_execution_truth.log")
            with open(log_path, "w", encoding='utf-8') as f:
                f.write(output)
            print(" Done.")
        except Exception as e:
            print(f" Failed: {e}")
            with open(os.path.join(scen_dir, "03_execution_CRASH.log"), "w", encoding='utf-8') as f:
                f.write(str(e))

    print("\n✅ Batch Processing Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PERSONA Socratic Loop")
    parser.add_argument("--provider", type=str, default="ollama", choices=["ollama", "openai", "anthropic", "mock"], help="LLM Provider")
    parser.add_argument("--model", type=str, default="llama3", help="Model name (e.g. llama3, gpt-4o, claude-3-opus)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of scenarios to run")
    
    args = parser.parse_args()
    
    run_pipeline(args.provider, args.model, args.limit)
