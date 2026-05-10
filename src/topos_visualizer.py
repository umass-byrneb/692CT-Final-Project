"""Interactive Categorical Visualizer for CLIFF World Models and Agentic Discovery."""

import json
from pathlib import Path

from .topos_world_model import _load_json, _as_list, _as_dict

def _build_interactive_html(nodes: list, edges: list, query: str) -> str:
    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{query} - CLIFF Epistemic Discovery</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{ font-family: ui-sans-serif, system-ui, sans-serif; background-color: #0a0e14; color: #c9d1d9; margin: 0; padding: 20px; }}
        h1 {{ margin-top: 0; font-size: 24px; color: #58a6ff; }}
        h2 {{ font-size: 18px; color: #c9d1d9; margin-top: 30px; margin-bottom: 10px; border-bottom: 1px solid #30363d; padding-bottom: 5px; }}
        .subtitle {{ font-size: 14px; color: #8b949e; margin-bottom: 20px; }}
        
        .network-container {{ width: 100%; border: 1px solid #30363d; border-radius: 8px; background: #161b22; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 20px; }}
        #mynetwork-topos {{ height: 400px; }}
        #mynetwork-discovery {{ height: 600px; }}
        #mynetwork-bridge {{ height: 500px; }} /* NEW 3RD VIEW */
        
        .legend {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px; font-size: 13px; background: #0d1117; padding: 10px; border-radius: 8px; border: 1px solid #30363d; }}
        .legend-item {{ display: flex; align-items: center; gap: 8px; }}
        .line-green {{ width: 20px; height: 3px; background: #3fb950; }}
        .line-red {{ width: 20px; height: 3px; border-top: 3px dashed #ff7b72; }}
        .line-gold {{ width: 20px; height: 3px; border-top: 3px dashed #d29922; }}
        .line-gray {{ width: 20px; height: 3px; background: #484f58; }}
        .node-domain {{ width: 14px; height: 14px; background: #1f6feb; border: 1px solid #58a6ff; }}
        
        .node-concept {{ width: 14px; height: 14px; background: #21262d; border-radius: 50%; border: 1px solid #8b949e; }}
        .node-bridge {{ width: 16px; height: 16px; background: #bf4b8a; border-radius: 50%; border: 1px solid #d25da6; }} /* MAGENTA FUNCTOR */
        
        div.vis-tooltip {{ background-color: #0d1117 !important; border: 1px solid #58a6ff !important; border-radius: 8px !important; color: #c9d1d9 !important; padding: 15px !important; font-family: 'Courier New', monospace !important; font-size: 13px !important; max-width: 400px; white-space: pre-wrap !important; }}
    </style>
</head>
<body>
    <h1>CLIFF: Native Epistemic Discovery & Topos World Model</h1>
    <div class="subtitle">Query: {query}</div>
    
    <div class="legend">
        <div class="legend-item"><div class="node-domain"></div> Semantic Domain</div>
        <div class="legend-item"><div class="node-concept"></div> Concept Node (Local)</div>
        <div class="legend-item"><div class="node-bridge"></div> Bridge Concept (Cross-Domain)</div>
        <div class="legend-item"><div class="line-green"></div> Compatible Restriction</div>
        <div class="legend-item"><div class="line-red"></div> Topological Void</div>
        <div class="legend-item"><div class="line-gray"></div> Semantic Tether</div>
        <div class="legend-item"><div class="line-gold"></div> Agent Discovery</div>
    </div>

    <h2>1. Global Topos Map (Click a Blue Domain to Restrict)</h2>
    <div id="mynetwork-topos" class="network-container"></div>
    
    <h2>2. Local Discovery Map (Click a Gray Concept to view Domino Cascades)</h2>
    <div id="mynetwork-discovery" class="network-container"></div>
    
    <h2>3. Cross-Domain Bridging (Mathematical Functors linking disciplines)</h2>
    <div id="mynetwork-bridge" class="network-container"></div>

    <script>
        const rawNodes = {nodes_json};
        const rawEdges = {edges_json};
        
        const options = {{
            nodes: {{ font: {{ size: 14, color: '#c9d1d9' }}, borderWidth: 2 }},
            edges: {{ font: {{ size: 11, align: 'middle', color: '#8b949e', strokeWidth: 0 }}, smooth: {{ type: 'continuous' }} }},
            physics: {{ 
                barnesHut: {{ gravitationalConstant: -5000, centralGravity: 0.2, springLength: 200 }}, 
                stabilization: {{ iterations: 150 }} 
            }},
            interaction: {{ hover: true, tooltipDelay: 200 }}
        }};

        // --- 1. TOPOS NETWORK ---
        const toposData = {{
            nodes: new vis.DataSet(rawNodes.filter(n => n.group === 'topos')),
            edges: new vis.DataSet(rawEdges.filter(e => e.group === 'topos_edge'))
        }};
        const toposNetwork = new vis.Network(document.getElementById('mynetwork-topos'), toposData, options);

        // --- 2. LOCAL DISCOVERY NETWORK (With Cascades) ---
        const discoveryNodes = new vis.DataSet(rawNodes.map(n => ({{ ...n, hidden: n.group === 'concept' }})));
        const discoveryEdges = new vis.DataSet(rawEdges.filter(e => e.group !== 'topos_edge').map(e => ({{ ...e, hidden: true }})));
        const discoveryNetwork = new vis.Network(document.getElementById('mynetwork-discovery'), {{ nodes: discoveryNodes, edges: discoveryEdges }}, options);

        const defaultConceptColor = {{ background: "#21262d", border: "#8b949e" }};
        const dimmedConceptColor = {{ background: "rgba(33,38,45,0.3)", border: "rgba(139,148,158,0.3)" }};
        const defaultTetherColor = {{ color: "#484f58" }};
        const dimmedTetherColor = {{ color: "rgba(72,79,88,0.2)" }};
        const defaultCFColor = {{ color: "#d29922" }};
        const dimmedCFColor = {{ color: "rgba(210,153,34,0.15)" }};

        function resetCascade() {{
            const nodeUpdates = [];
            const edgeUpdates = [];
            rawNodes.forEach(n => {{ if (n.group === 'concept') nodeUpdates.push({{ id: n.id, color: defaultConceptColor }}); }});
            rawEdges.forEach(e => {{
                if (e.group === 'tether') edgeUpdates.push({{ id: e.id, color: defaultTetherColor }});
                if (e.group === 'counterfactual') edgeUpdates.push({{ id: e.id, color: defaultCFColor }});
            }});
            discoveryNodes.update(nodeUpdates);
            discoveryEdges.update(edgeUpdates);
        }}

        function highlightCascade(startNodeId) {{
            const highlightedNodes = new Set([startNodeId]);
            const highlightedEdges = new Set();
            const queue = [startNodeId];
            while(queue.length > 0) {{
                const current = queue.shift();
                const outEdges = rawEdges.filter(e => e.from === current && e.group === 'counterfactual');
                outEdges.forEach(e => {{
                    if(!highlightedEdges.has(e.id)) {{
                        highlightedEdges.add(e.id);
                        if(!highlightedNodes.has(e.to)) {{
                            highlightedNodes.add(e.to);
                            queue.push(e.to);
                        }}
                    }}
                }});
            }}

            const nodeUpdates = [];
            const edgeUpdates = [];
            rawNodes.forEach(n => {{
                if (n.group === 'concept') nodeUpdates.push({{ id: n.id, color: highlightedNodes.has(n.id) ? defaultConceptColor : dimmedConceptColor }});
            }});
            rawEdges.forEach(e => {{
                if (e.group === 'tether') edgeUpdates.push({{ id: e.id, color: highlightedNodes.has(e.to) ? defaultTetherColor : dimmedTetherColor }});
                else if (e.group === 'counterfactual') edgeUpdates.push({{ id: e.id, color: highlightedEdges.has(e.id) ? defaultCFColor : dimmedCFColor }});
            }});
            discoveryNodes.update(nodeUpdates);
            discoveryEdges.update(edgeUpdates);
        }}

        function updateDiscoveryView(selectedDomainId) {{
            resetCascade();
            const nodeUpdates = [];
            const edgeUpdates = [];

            if (!selectedDomainId) {{
                rawNodes.forEach(n => nodeUpdates.push({{ id: n.id, hidden: n.group === 'concept' }}));
                rawEdges.forEach(e => {{ if (e.group !== 'topos_edge') edgeUpdates.push({{ id: e.id, hidden: true }}); }});
            }} else {{
                const validTethers = rawEdges.filter(e => e.group === 'tether' && e.from === selectedDomainId);
                const validConceptIds = new Set(validTethers.map(e => e.to));

                rawNodes.forEach(n => {{
                    if (n.group === 'topos') nodeUpdates.push({{ id: n.id, hidden: n.id !== selectedDomainId }});
                    else nodeUpdates.push({{ id: n.id, hidden: !validConceptIds.has(n.id) }});
                }});

                rawEdges.forEach(e => {{
                    if (e.group === 'tether') edgeUpdates.push({{ id: e.id, hidden: e.from !== selectedDomainId }});
                    else if (e.group === 'counterfactual') {{
                        const isVisible = validConceptIds.has(e.from) && validConceptIds.has(e.to);
                        edgeUpdates.push({{ id: e.id, hidden: !isVisible }});
                    }}
                }});
            }}
            discoveryNodes.update(nodeUpdates);
            discoveryEdges.update(edgeUpdates);
            discoveryNetwork.stabilize();
        }}

        toposNetwork.on("selectNode", function(params) {{ updateDiscoveryView(params.nodes[0]); }});
        toposNetwork.on("deselectNode", function(params) {{ updateDiscoveryView(null); }});
        discoveryNetwork.on("selectNode", function(params) {{
            if (params.nodes.length > 0) {{
                const selectedId = params.nodes[0];
                const nodeData = rawNodes.find(n => n.id === selectedId);
                if (nodeData && nodeData.group === 'concept') highlightCascade(selectedId);
            }}
        }});
        discoveryNetwork.on("deselectNode", function(params) {{ resetCascade(); }});

        // --- 3. CROSS-DOMAIN BRIDGING NETWORK (FUNCTORS) ---
        // Find concepts connected to more than one distinct Topos Domain
        const allTethers = rawEdges.filter(e => e.group === 'tether');
        const tetherCounts = {{}};
        allTethers.forEach(e => {{
            if (!tetherCounts[e.to]) tetherCounts[e.to] = new Set();
            tetherCounts[e.to].add(e.from); // Record the domain (anchor)
        }});
        
        // A Bridge Concept must map to at least 2 different domains
        const bridgeIds = new Set(Object.keys(tetherCounts).filter(id => tetherCounts[id].size > 1));

        const bridgeNodes = new vis.DataSet();
        const bridgeEdges = new vis.DataSet();

        rawNodes.forEach(n => {{
            if (n.group === 'topos') {{
                bridgeNodes.add({{...n}}); // Always show domains
            }} else if (bridgeIds.has(n.id)) {{
                // Highlight the Functor nodes in Magenta
                bridgeNodes.add({{
                    ...n, 
                    color: {{background: '#bf4b8a', border: '#d25da6'}}, 
                    title: 'BRIDGE CONCEPT\\nShared between: ' + Array.from(tetherCounts[n.id]).join(', ')
                }});
            }}
        }});

        allTethers.forEach(e => {{
            if (bridgeIds.has(e.to)) {{
                // Highlight the bridging tethers
                bridgeEdges.add({{...e, color: {{color: '#bf4b8a', opacity: 0.8}}, width: 2}});
            }}
        }});

        const bridgeNetwork = new vis.Network(
            document.getElementById('mynetwork-bridge'), 
            {{ nodes: bridgeNodes, edges: bridgeEdges }}, 
            options
        );

    </script>
</body>
</html>
"""

def materialize_integrated_visualizer(
    *,
    query: str,
    route_name: str,
    route_outdir: Path,
    psr_path: Path | None = None,
    counterfactuals_path: Path | None = None
) -> Path:
    
    vis_nodes = []
    vis_edges = []
    processed_nodes = set()
    processed_tethers = set()
    edge_counter = 0

    # 1. ADD TOPOS SHEAF DATA
    psr_payload = _load_json(psr_path) if psr_path else {}
    restrictions = _as_list(psr_payload.get("restriction_diagnostics"))
    
    for row in restrictions:
        clean_row = _as_dict(row)
        source = str(clean_row.get("source_context", ""))
        target = str(clean_row.get("target_context", ""))
        if not source or not target: continue
            
        for ctx in [source, target]:
            if ctx not in processed_nodes:
                vis_nodes.append({
                    "id": ctx, "label": ctx.replace("domain::", ""), "shape": "box",
                    "color": {"background": "#1f6feb", "border": "#58a6ff"},
                    "font": {"size": 18, "color": "#ffffff"},
                    "group": "topos" 
                })
                processed_nodes.add(ctx)
                
        compatible = bool(clean_row.get("compatible"))
        vis_edges.append({
            "id": f"edge_{edge_counter}",
            "from": source, "to": target, 
            "label": "Glued" if compatible else "Void",
            "color": {"color": "#3fb950" if compatible else "#ff7b72"},
            "width": 3 if compatible else 2,
            "dashes": False if compatible else [5,5],
            "arrows": "to",
            "group": "topos_edge" 
        })
        edge_counter += 1

    # 2. ADD AGENTIC DISCOVERY DATA & CALCULATE SIZING
    if counterfactuals_path and counterfactuals_path.exists():
        cf_payload = _load_json(counterfactuals_path)
        counterfactuals = _as_list(cf_payload.get("counterfactuals"))
        
        concept_freq = {}
        for cf in counterfactuals:
            row = _as_dict(cf)
            subj = str(row.get("subj", ""))
            obj = str(row.get("obj", ""))
            if subj: concept_freq[subj] = concept_freq.get(subj, 0) + 1
            if obj: concept_freq[obj] = concept_freq.get(obj, 0) + 1
        
        for index, cf in enumerate(counterfactuals):
            row = _as_dict(cf)
            subj = str(row.get("subj", f"cause_{index}"))
            obj = str(row.get("obj", f"outcome_{index}"))
            raw_domain = str(row.get('domain', ''))
            
            target_domain = f"domain::{raw_domain.strip().replace(' ', '_').lower()}"
            
            if target_domain in processed_nodes:
                anchor = target_domain 
            elif "corpus" in processed_nodes:
                anchor = "corpus"      
            else:
                anchor = None          
            
            hover_text = f"INTERVENTION: {row.get('intervention')}\n\nEXPECTED SHIFT: {row.get('expected_shift')}"
            
            for node in [subj, obj]:
                # Add node if it doesn't exist
                if node not in processed_nodes:
                    short_label = node[:18] + "..." if len(node) > 18 else node
                    freq = concept_freq.get(node, 1)
                    calculated_size = 10 + (freq * 4) 
                    
                    node_tooltip = f"CONCEPT: {node}\nTOTAL CONNECTIONS: {freq}"
                    
                    vis_nodes.append({
                        "id": node, "label": short_label, "shape": "dot", 
                        "size": calculated_size, 
                        "title": node_tooltip,   
                        "color": {"background": "#21262d", "border": "#8b949e"}, 
                        "group": "concept" 
                    })
                    processed_nodes.add(node)
                    
                # Add tether separately so we catch Cross-Domain overlaps!
                if anchor:
                    tether_id = f"{anchor}_tether_to_{node}"
                    if tether_id not in processed_tethers:
                        vis_edges.append({
                            "id": tether_id,
                            "from": anchor, "to": node,
                            "color": {"color": "#484f58"}, "width": 1, "arrows": "to",
                            "group": "tether" 
                        })
                        processed_tethers.add(tether_id)

            vis_edges.append({
                "id": f"edge_{edge_counter}",
                "from": subj, "to": obj, 
                "label": "Counterfactual",
                "title": hover_text,
                "color": {"color": "#d29922"},
                "width": 3, "dashes": [8,4], "arrows": "to",
                "group": "counterfactual" 
            })
            edge_counter += 1

    outdir = route_outdir / "topos_world_model"
    outdir.mkdir(parents=True, exist_ok=True)
    interactive_path = outdir / "cliff_discovery_topos.html"
    interactive_path.write_text(_build_interactive_html(vis_nodes, vis_edges, query), encoding="utf-8")
    
    return interactive_path