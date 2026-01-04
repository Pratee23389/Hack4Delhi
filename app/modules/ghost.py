"""
Ghost-Hunter Module: Graph Theory-Based Fraud Detection
===============================================================
ALGORITHM: Connected Components + Centrality Analysis
===============================================================

PROBLEM: Detecting ghost employees and fraud syndicates where
multiple fake identities share contact information.

APPROACH: Model payroll as a Bipartite Graph and find Connected
Components. Use Centrality algorithms to identify fraud "Kingpins".

GRAPH THEORY FOUNDATION:
1. Bipartite Graph G = (V₁ ∪ V₂, E) where:
   - V₁ = Employee nodes
   - V₂ = Attribute nodes (Mobile, Bank Account)
   - E = Edges connecting employees to shared attributes

2. Connected Components: Maximal subgraphs where all vertices
   are reachable from each other. Uses Union-Find (Disjoint Set)
   data structure internally.

3. Centrality Measures (for Kingpin detection):
   - Degree Centrality: Number of connections
   - Betweenness Centrality: How often node appears on shortest paths
   - Closeness Centrality: Average distance to all other nodes

TIME COMPLEXITY:
- Graph Construction: O(V + E)
- Connected Components: O(V + E) using DFS/BFS
- Betweenness Centrality: O(V × E) using Brandes' algorithm
- Overall: O(V × E) where V=employees, E=shared attributes

SPACE COMPLEXITY: O(V + E) for adjacency list representation

WHY THIS WORKS:
- Fraudsters must reuse contact info (limited SIM cards/accounts)
- Graph reveals hidden relationships not visible in tabular data
- Centrality identifies the "controller" of fraud ring
- Scales to detect complex, multi-level fraud networks
"""

import pandas as pd
import networkx as nx
from io import BytesIO
import sys
from pathlib import Path

# Add parent directory for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import GraphFraudConfig


def analyze_payroll(csv_bytes):
    """
    Analyze payroll CSV for ghost employees using graph theory
    
    ALGORITHM STEPS:
    1. Build bipartite graph: employees ↔ attributes
    2. Find connected components (fraud clusters)
    3. Calculate centrality scores (identify kingpins)
    4. Compute graph density metrics
    
    Args:
        csv_bytes: Raw bytes of payroll CSV
    
    Returns:
        dict: Analysis results with clusters, kingpins, and graph metrics
        
    COMPLEXITY:
        Time: O(V × E) dominated by centrality calculation
        Space: O(V + E) for graph storage
    """
    # STEP 1: Load Data
    print("Loading payroll data...")
    df = pd.read_csv(BytesIO(csv_bytes))
    print(f"✓ Loaded {len(df)} employee records")
    
    # STEP 2: Build Bipartite Graph
    # Two types of nodes: Employee nodes and Attribute nodes
    print("Building bipartite graph...")
    G = nx.Graph()
    
    # Add employee nodes with attributes
    for _, row in df.iterrows():
        emp_id = row['Employee_ID']
        G.add_node(emp_id, 
                   node_type='employee',
                   **row.to_dict())
    
    # STEP 3: Create edges for shared attributes
    # Using Union-Find logic: employees sharing attributes are in same component
    edge_count = 0
    
    # Connect employees who share Mobile numbers
    print("  Analyzing shared mobile numbers...")
    mobile_groups = df.groupby('Mobile')['Employee_ID'].apply(list)
    for mobile, emp_ids in mobile_groups.items():
        if len(emp_ids) > 1:
            # Create clique: connect all pairs
            for i in range(len(emp_ids)):
                for j in range(i + 1, len(emp_ids)):
                    G.add_edge(emp_ids[i], emp_ids[j], 
                             connection_type='shared_mobile', 
                             shared_value=mobile,
                             weight=2.0)  # Weight for centrality calculation
                    edge_count += 1
    
    # Connect employees who share Bank Accounts
    print("  Analyzing shared bank accounts...")
    bank_groups = df.groupby('Bank_Acc')['Employee_ID'].apply(list)
    for bank_acc, emp_ids in bank_groups.items():
        if len(emp_ids) > 1:
            for i in range(len(emp_ids)):
                for j in range(i + 1, len(emp_ids)):
                    if G.has_edge(emp_ids[i], emp_ids[j]):
                        # Strengthen existing edge (both mobile AND bank shared)
                        G[emp_ids[i]][emp_ids[j]]['connection_type'] += ',shared_bank'
                        G[emp_ids[i]][emp_ids[j]]['weight'] = 5.0  # Higher weight = stronger fraud signal
                    else:
                        G.add_edge(emp_ids[i], emp_ids[j], 
                                 connection_type='shared_bank',
                                 shared_value=bank_acc,
                                 weight=2.0)
                        edge_count += 1
    
    print(f"✓ Graph constructed: {len(G.nodes)} nodes, {edge_count} edges")
    
    # STEP 4: Find Connected Components
    # Uses DFS internally - O(V + E) complexity
    print("Finding connected components (fraud clusters)...")
    components = list(nx.connected_components(G))
    print(f"✓ Found {len(components)} connected components")
    
    # STEP 5: Identify Suspicious Clusters
    # Filter by minimum clique size threshold
    suspicious_clusters = []
    
    for idx, component in enumerate(components):
        if len(component) >= GraphFraudConfig.MIN_CLIQUE_SIZE:
            component_list = list(component)
            cluster_employees = df[df['Employee_ID'].isin(component_list)].to_dict('records')
            
            # Calculate subgraph metrics
            subgraph = G.subgraph(component_list)
            num_nodes = len(component_list)
            num_edges = subgraph.number_of_edges()
            
            # Graph Density = 2E / (V(V-1)) for undirected graph
            # Range: [0, 1] where 1 = complete graph (all nodes connected)
            if num_nodes > 1:
                graph_density = (2 * num_edges) / (num_nodes * (num_nodes - 1))
            else:
                graph_density = 0
            
            # Determine severity based on size and density
            if len(component) >= GraphFraudConfig.SUSPICIOUS_CLIQUE_SIZE:
                severity = 'CRITICAL' if graph_density > GraphFraudConfig.HIGH_DENSITY_THRESHOLD else 'HIGH'
            else:
                severity = 'MEDIUM'
            
            # STEP 6: Calculate Centrality Scores (Identify Kingpin)
            # Betweenness Centrality: measures "brokerage" - who controls information flow
            print(f"  Calculating centrality for cluster {idx+1} ({num_nodes} employees)...")
            
            if GraphFraudConfig.CENTRALITY_ALGORITHM == 'betweenness':
                centrality = nx.betweenness_centrality(subgraph, weight='weight')
            elif GraphFraudConfig.CENTRALITY_ALGORITHM == 'degree':
                centrality = nx.degree_centrality(subgraph)
            elif GraphFraudConfig.CENTRALITY_ALGORITHM == 'closeness':
                centrality = nx.closeness_centrality(subgraph)
            else:
                centrality = nx.betweenness_centrality(subgraph, weight='weight')
            
            # Identify kingpin (highest centrality)
            kingpin_id = max(centrality, key=centrality.get)
            kingpin_score = centrality[kingpin_id]
            kingpin_name = df[df['Employee_ID'] == kingpin_id]['Name'].values[0]
            
            suspicious_clusters.append({
                'cluster_id': idx + 1,
                'size': len(component),
                'severity': severity,
                'graph_density': round(graph_density, 3),
                'num_edges': num_edges,
                'employees': cluster_employees,
                'algorithm': 'Connected Components (DFS-based)',
                'kingpin': {
                    'employee_id': kingpin_id,
                    'name': kingpin_name,
                    'centrality_score': round(kingpin_score, 4),
                    'centrality_type': GraphFraudConfig.CENTRALITY_ALGORITHM,
                    'explanation': 'Highest centrality = likely controller of fraud ring'
                },
                'explanation': f'Detected fraud ring: {num_nodes} employees sharing contact info (density: {graph_density:.1%})'
            })
            print(f"  🚨 Cluster {idx+1}: {num_nodes} employees, Kingpin: {kingpin_name}")
    
    # STEP 7: Calculate Overall Graph Metrics
    total_density = 0
    if len(G.nodes) > 1:
        total_density = (2 * G.number_of_edges()) / (len(G.nodes) * (len(G.nodes) - 1))
    
    # Calculate integrity score
    if suspicious_clusters:
        # Lower score for more/larger clusters
        total_fraud_employees = sum(c['size'] for c in suspicious_clusters)
        fraud_percentage = (total_fraud_employees / len(df)) * 100
        integrity_score = max(0, 100 - (fraud_percentage * 2))  # Scale: 100=clean, 0=fraud
    else:
        integrity_score = 100
    
    return {
        'total_employees': len(df),
        'total_clusters_found': len(components),
        'suspicious_clusters': len(suspicious_clusters),
        'clusters': suspicious_clusters,
        'graph_metrics': {
            'total_nodes': len(G.nodes),
            'total_edges': G.number_of_edges(),
            'overall_density': round(total_density, 4),
            'algorithm_complexity': 'O(V × E)',
            'centrality_algorithm': GraphFraudConfig.CENTRALITY_ALGORITHM
        },
        'status': 'WARNING' if suspicious_clusters else 'CLEAR',
        'integrity_score': round(integrity_score, 2)
    }
