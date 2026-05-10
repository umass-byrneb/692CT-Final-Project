# CLIFF CatAGI: Full Epistemic Pipeline & Visualizer Extension

An end-to-end framework and interactive visualization dashboard for the **CLIFF (Categorical Language Inference for Functor Flow)** AGI architecture.

This repository contains both the full computational pipeline (which extracts causal triples from raw text and evaluates them using Category Theory) and a custom visualization extension. Together, they allow researchers to process literature and visually audit the rules of Category Theory—specifically Sheaf Gluing, Morphism Cascades, and Functors.

## Features

* **Full CLIFF Pipeline:** Ingests raw PDFs or text, utilizes the Democritus agent to extract causal counterfactuals, and runs Predictive State Representation (Topos PSR) mathematics (Hankel matrices, SVD) to rigorously evaluate causal claims.

* **View 1: Global Topos Map:** Visualizes the rigid "Base Space" of the World Model. Parses Hankel matrix restriction gaps to render Sheaf Gluing (Solid Green edges) and Topological Voids (Dashed Red edges).

* **View 2: Local Discovery Map:** Enforces global-to-local restriction. Clicking a Topos domain exclusively reveals the localized causal sections bound to it. Features Degree Centrality node sizing and an interactive Breadth-First Search (BFS) to simulate multi-step "Domino Cascades."

* **View 3: Functorial Bridges:** Mathematically isolates variables shared across multiple distinct semantic domains, rendering them as Magenta Functor Nodes to reveal the systemic bridges connecting interdisciplinary sciences.

* **Terminal Bridge Finder:** A lightweight CLI tool to instantly print cross-domain Functors without generating the HTML canvas.

## Prerequisites

* Python 3.8+
* An active LLM API Key (required for the `Democritus` extraction agent to process raw PDFs).
* Active internet connection (The HTML output loads the `Vis.js` library via CDN).

## Directory Structure

Ensure your repository matches this structure:

```text
CLIFF-CatAGI-Full/
├── README.md
├── requirements.txt
├── cliff_full_pipeline.py              <-- Core mathematical and extraction engine
├── run_visualizer.py                   <-- Dashboard generator
├── find_bridges.py                     <-- Terminal functor auditor
├── src/
│   ├── __init__.py
│   └── topos_visualizer.py             <-- Interactive mapping logic
└── sample_data/
    ├── raw_pdfs/                       <-- Place your unanalyzed literature here
    └── penguin_synthesis/              <-- Pipeline output destination
        ├── democritus_counterfactuals.json
        └── democritus_topos_psr_hankel.json
```

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/CLIFF-CatAGI-Full.git
cd CLIFF-CatAGI-Full
```

Install the required dependencies (which includes the libraries needed for LLM extraction and matrix math):

```bash
pip install -r requirements.txt
```

Set your environment variable for the extraction agent.

### Windows (PowerShell)

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

### Mac/Linux

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### 1. Run the Full CLIFF Pipeline (Data Ingestion & Math)

To begin, process your raw literature. This script reads the documents in your input folder, runs the Democritus extraction, calculates the Topos restriction gaps, and generates the necessary JSON artifacts.

```bash
python cliff_full_pipeline.py ./sample_data/raw_pdfs --output ./sample_data/penguin_synthesis
```

> **Note:** Depending on the size of your literature corpus, this step may take several minutes to compute the Hankel matrices and SVDs.

### 2. Generate the Interactive Dashboard

Once the pipeline has generated the JSON artifacts, run the visualizer script to translate the mathematics into the interactive HTML interface:

```bash
python run_visualizer.py ./sample_data/penguin_synthesis
```

This will parse the data and create a new folder inside your target directory called `topos_world_model`, containing `cliff_discovery_topos.html`.

Open this HTML file in any modern web browser to interact with the CatAGI World Model.

### 3. Run the Terminal Functor Script

If you wish to audit the interdisciplinary bridges directly in your terminal without rendering the UI, run the bridge finder:

```bash
python find_bridges.py ./sample_data/penguin_synthesis
```

#### Expected Output

```text
[*] Analyzing Causal Topology in: democritus_counterfactuals.json

===========================================================
[+] FOUND 4 BRIDGE CONCEPTS (CROSS-DOMAIN FUNCTORS)
===========================================================

🟣 FUNCTOR: climate change
   🔗 BRIDGES 3 DOMAINS:
      - domain::emperor_penguin_habitat
      - domain::ocean_warming
      - domain::krill_abundance
------------------------------------------------------------
```

## Theoretical Grounding

This repository operationalizes the mathematical frameworks outlined in the *Categories for AGI (CatAGI)* text by Dr. Sridhar Mahadevan. It programmatically enforces Topos Causal Models (TCMs) by treating causal extraction not as a universal graph, but as contextually bound local sections within a topological geometry.

### Sheaf Gluing

Visualized in View 1 via the SVD restriction gap parsing.

### Morphisms

Visualized in View 2 via the BFS causal domino cascades.

### Functors

Visualized in View 3 via the decoupling of cross-domain semantic tethers.
