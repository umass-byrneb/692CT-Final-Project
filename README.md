# CLIFF Visualizer Extension: Interactive Categorical Epistemic Discovery

An interactive visualization dashboard and terminal toolkit extending the **CLIFF (Categorical Language Inference for Functor Flow)** AGI architecture.

This repository translates the dense mathematical outputs of CLIFF's Topos Predictive State Representations (PSRs) and Democritus extraction engine into an interpretable, multi-layered UI. It allows researchers to visually audit the rules of Category Theory—specifically Sheaf Gluing, Morphism Cascades, and Functors—operating on synthesized literature.

---

## Features

### View 1: Global Topos Map
Visualizes the rigid "Base Space" of the World Model.

Parses Hankel matrix restriction gaps to render:

- **Sheaf Gluing** (Solid Green edges)
- **Topological Voids** (Dashed Red edges)

### View 2: Local Discovery Map
Enforces global-to-local restriction.

Clicking a Topos domain exclusively reveals the localized causal sections bound to it.

Features:

- Degree Centrality node sizing
- Interactive Breadth-First Search (BFS)
- Multi-step "Domino Cascades"

### View 3: Functorial Bridges
Mathematically isolates variables shared across multiple distinct semantic domains, rendering them as **Magenta Functor Nodes** to reveal the systemic bridges connecting interdisciplinary sciences.

### Terminal Bridge Finder
A lightweight CLI tool to instantly print cross-domain Functors without generating the HTML canvas.

---

## Prerequisites

- Python 3.8+
- Active internet connection  
  *(The HTML output loads the `Vis.js` library via CDN.)*
- JSON outputs from a standard CLIFF Democritus run:
  - `democritus_counterfactuals.json`
  - `democritus_topos_psr_hankel.json`

---

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/CLIFF-Visualizer-Extension.git
cd CLIFF-Visualizer-Extension
```

> **Note:**  
> This extension relies purely on Python built-in libraries:
>
> - `json`
> - `pathlib`
> - `sys`
>
> No `pip install` is required for the core scripts.

---

## Usage

You can run these scripts against the provided `sample_data/penguin_synthesis` folder, or point them to any folder containing your own CLIFF JSON artifacts.

---

## 1. Generate the Interactive Dashboard

To generate the 3-view HTML dashboard, run the main visualizer script and pass the directory containing your CLIFF data:

```bash
python run_visualizer.py ./sample_data/penguin_synthesis
```

This will:

1. Parse the data
2. Create a new folder inside your target directory called `topos_world_model`
3. Generate:

```text
cliff_discovery_topos.html
```

Open this HTML file in any modern web browser.

---

## 2. Run the Terminal Functor Script

If you only want to audit the interdisciplinary bridges in your terminal without generating the UI, run the bridge finder:

```bash
python find_bridges.py ./sample_data/penguin_synthesis
```

### Expected Output

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

---

## Theoretical Grounding

This extension is built upon the mathematical frameworks outlined in the *Categories for AGI (CatAGI)* text by :contentReference[oaicite:0]{index=0}.

It programmatically enforces **Topos Causal Models (TCMs)** by treating causal extraction not as a universal graph, but as contextually bound local sections within a topological geometry.

### Sheaf Gluing
Visualized in **View 1** via the SVD restriction gap parsing.

### Morphisms
Visualized in **View 2** via the BFS causal domino cascades.

### Functors
Visualized in **View 3** via the decoupling of cross-domain semantic tethers.
