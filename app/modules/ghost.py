"""
Ghost-Hunter Module
Detects ghost employees and fraud syndicates using graph analysis
"""

import pandas as pd
import networkx as nx
from io import BytesIO


def analyze_payroll(csv_bytes):
    """
    Analyze payroll CSV for ghost employees
    Builds a graph where employees sharing attributes are connected
    Returns clusters where more than 2 employees are connected
    """
    # Load CSV
    df = pd.read_csv(BytesIO(csv_bytes))
    
    # Create graph
    G = nx.Graph()
    
    # Add all employees as nodes
    for _, row in df.iterrows():
        emp_id = row['Employee_ID']
        G.add_node(emp_id, **row.to_dict())
    
    # Connect employees who share Mobile or Bank_Acc
    # Group by Mobile
    mobile_groups = df.groupby('Mobile')['Employee_ID'].apply(list)
    for mobile, emp_ids in mobile_groups.items():
        if len(emp_ids) > 1:
            # Connect all employees with same mobile
            for i in range(len(emp_ids)):
                for j in range(i + 1, len(emp_ids)):
                    G.add_edge(emp_ids[i], emp_ids[j], reason='shared_mobile', value=mobile)
    
    # Group by Bank_Acc
    bank_groups = df.groupby('Bank_Acc')['Employee_ID'].apply(list)
    for bank_acc, emp_ids in bank_groups.items():
        if len(emp_ids) > 1:
            # Connect all employees with same bank account
            for i in range(len(emp_ids)):
                for j in range(i + 1, len(emp_ids)):
                    if G.has_edge(emp_ids[i], emp_ids[j]):
                        # Strengthen existing edge
                        G[emp_ids[i]][emp_ids[j]]['reason'] += ',shared_bank'
                    else:
                        G.add_edge(emp_ids[i], emp_ids[j], reason='shared_bank', value=bank_acc)
    
    # Find connected components (clusters)
    clusters = list(nx.connected_components(G))
    
    # Filter clusters with more than 2 employees
    suspicious_clusters = []
    for cluster in clusters:
        if len(cluster) > 2:
            cluster_list = list(cluster)
            # Get details of employees in cluster
            cluster_employees = df[df['Employee_ID'].isin(cluster_list)].to_dict('records')
            
            suspicious_clusters.append({
                'cluster_size': len(cluster),
                'employee_ids': cluster_list,
                'employees': cluster_employees,
                'status': 'GHOST EMPLOYEE SYNDICATE DETECTED'
            })
    
    return {
        'total_employees': len(df),
        'suspicious_clusters': suspicious_clusters,
        'num_flagged_employees': sum(c['cluster_size'] for c in suspicious_clusters),
        'status': 'WARNING' if suspicious_clusters else 'CLEAR'
    }
