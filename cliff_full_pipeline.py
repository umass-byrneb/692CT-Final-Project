"""
CLIFF NATIVE PIPELINE
End-to-End Execution: World Model -> Counterfactual Discovery -> Visualization
"""

import sys
from pathlib import Path
from functorflow_v3.democritus_counterfactuals import write_democritus_counterfactual_artifacts
from functorflow_v3.topos_world_model import materialize_topos_world_model

def find_authentic_triples(base_dir: Path) -> Path:
    for path in base_dir.rglob("relational_triples.jsonl"):
        return path
    raise FileNotFoundError(f"Could not find relational_triples.jsonl in {base_dir}")

def run_full_pipeline(dataset_path: str):
    BASE_DIR = Path(dataset_path)
    
    # Locate the authentic Topos math bundle
    PSR_BUNDLE = BASE_DIR / "democritus/democritus_runs/topos_psr/democritus_topos_psr_hankel.json"
    
    # Save the output INSIDE the dataset folder so runs don't overwrite each other
    OUTPUT_DIR = BASE_DIR / "cliff_native_output"
    
    if not PSR_BUNDLE.exists():
        print(f"[-] ERROR: Cannot find the Topos bundle at {PSR_BUNDLE}")
        print("    Make sure you have run the CLIFF Democritus ingestion for this dataset.")
        return

    domain_name = BASE_DIR.name.replace("_", " ").title()

    # 1. Run the Counterfactual Agent natively (No Limit!)
    print(f"[*] STEP 1: Running Epistemic Discovery Agent for {domain_name}...")
    triples_path = find_authentic_triples(BASE_DIR)
    discovery_artifacts = write_democritus_counterfactual_artifacts(
        triples_path=triples_path,
        outdir=OUTPUT_DIR / "discovery",
        domain_name=domain_name,
        limit=9999999, # UNLEASH THE FULL DATASET
        csql_sqlite_path=None, 
        topos_psr_path=PSR_BUNDLE
    )
    counterfactuals_json = discovery_artifacts["json_path"]
    
    # 2. Materialize Standard CLIFF World Model
    print("[*] STEP 2: Materializing standard Topos World Model...")
    standard_html = materialize_topos_world_model(
        query=f"{domain_name} Analysis",
        route_name="democritus",
        route_outdir=OUTPUT_DIR,
        base_artifact_path=None,
        summary_path=None,
        psr_path=PSR_BUNDLE
    )

    # 3. Inject into our Interactive Visualizer
    print("[*] STEP 3: Rendering the Interactive Epistemic Graph...")
    from functorflow_v3.topos_visualizer import materialize_integrated_visualizer
    interactive_html = materialize_integrated_visualizer(
        query=f"{domain_name} Discoveries",
        route_name="democritus",
        route_outdir=OUTPUT_DIR,
        psr_path=PSR_BUNDLE,
        counterfactuals_path=counterfactuals_json
    )
    
    print("\n=============================================")
    print(f"[+] PIPELINE COMPLETE FOR: {domain_name}")
    print(f"    Standard Dashboard: {standard_html}")
    print(f"    Counterfactuals:    {discovery_artifacts['markdown_path']}")
    print(f"    Interactive Topos:  {interactive_html}")
    print("=============================================\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cliff_full_pipeline.py <path_to_dataset_folder>")
        print("Example: python cliff_full_pipeline.py /tmp/ocean_warming_synthesis")
        sys.exit(1)
        
    dataset_folder = sys.argv[1]
    run_full_pipeline(dataset_folder)
