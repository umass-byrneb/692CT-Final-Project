"""
CLIFF Causal Bridge Finder
Scans a dataset to identify mathematical Functors (Concepts shared across multiple domains)
"""

import sys
import json
from pathlib import Path

def find_bridges(dataset_folder: str):
    base_dir = Path(dataset_folder)
    
    # 1. Locate the generated counterfactuals JSON
    # It will dynamically find the file whether it's in ocean_warming, penguin_synthesis, etc.
    cf_files = list(base_dir.rglob("*democritus_counterfactuals*.json"))
    
    if not cf_files:
        print(f"[-] ERROR: Could not find a democritus_counterfactuals JSON in {dataset_folder}")
        print("    Make sure you ran cliff_full_pipeline.py on this folder first.")
        return
        
    cf_path = cf_files[0]
    print(f"[*] Analyzing Causal Topology in: {cf_path.name}\n")
    
    with open(cf_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
        
    counterfactuals = payload.get("counterfactuals", [])
    
    # 2. Map Concepts to their Semantic Domains
    concept_to_domains = {}
    
    for cf in counterfactuals:
        subj = cf.get("subj", "").strip()
        obj = cf.get("obj", "").strip()
        raw_domain = cf.get("domain", "").strip()
        
        if not raw_domain:
            continue
            
        # Normalize the domain string exactly like our visualizer does
        domain = f"domain::{raw_domain.replace(' ', '_').lower()}"
        
        for concept in [subj, obj]:
            if concept:
                if concept not in concept_to_domains:
                    concept_to_domains[concept] = set()
                concept_to_domains[concept].add(domain)
                
    # 3. Isolate the "Bridges" (Concepts existing in >= 2 distinct domains)
    bridges = {c: d for c, d in concept_to_domains.items() if len(d) > 1}
    
    if not bridges:
        print("[!] No Bridge Concepts (Functors) found. The domains in this dataset are completely isolated.")
        return
        
    print(f"===========================================================")
    print(f"[+] FOUND {len(bridges)} BRIDGE CONCEPTS (CROSS-DOMAIN FUNCTORS)")
    print(f"===========================================================\n")
    
    # Sort bridges by the number of domains they connect (most connected first)
    sorted_bridges = sorted(bridges.items(), key=lambda item: len(item[1]), reverse=True)
    
    for concept, domains in sorted_bridges:
        print(f"🟣 FUNCTOR: {concept}")
        print(f"   🔗 BRIDGES {len(domains)} DOMAINS:")
        for d in sorted(domains):
            print(f"      - {d}")
        print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_bridges.py <path_to_dataset_folder>")
        print("Example: python find_bridges.py /tmp/penguin_synthesis")
        sys.exit(1)
        
    find_bridges(sys.argv[1])