"""Ghost-Hunter / Graph-Fraud module

Detects possible ghost employees and syndicates in payroll data.

Design:
- Each employee is a node.
- We create edges between employees that share a mobile number, address,
  or bank account number.
- We then run a connected components algorithm to find clusters of
  tightly connected employees.
- Any cluster with more than a configurable size (e.g. > 5 employees)
  is flagged as "High Risk".

Implementation notes:
- We provide an in-memory NetworkX implementation that works out of the
  box for the hackathon.
- Optionally, if a Neo4j connection URL is configured, we show how
  the same relationships could be persisted to a graph database.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Dict, Any, List, Optional

import pandas as pd
import networkx as nx

try:
    from neo4j import GraphDatabase  # type: ignore
except Exception:  # pragma: no cover - optional
    GraphDatabase = None  # type: ignore


EXPECTED_COLUMNS = ["employee_id", "name", "mobile", "address", "bank_account"]


@dataclass
class EmployeeNode:
    employee_id: str
    name: str
    mobile: str
    address: str
    bank_account: str


def _load_payroll_dataframe(csv_bytes: bytes) -> pd.DataFrame:
    """Load payroll CSV from bytes into a pandas DataFrame.

    The CSV is expected to have at least the columns in EXPECTED_COLUMNS.
    """

    df = pd.read_csv(BytesIO(csv_bytes))
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in payroll CSV: {missing}")
    return df[EXPECTED_COLUMNS].astype(str)


def _build_networkx_graph(df: pd.DataFrame) -> nx.Graph:
    """Build a NetworkX graph from payroll DataFrame.

    For each shared attribute (mobile, address, bank_account), we connect
    employees that share the same value. The more attributes shared, the
    denser the cluster, which is suspicious.
    """

    G = nx.Graph()

    # Add all employee nodes first
    for _, row in df.iterrows():
        emp_id = row["employee_id"]
        G.add_node(emp_id, **row.to_dict())

    # Helper: connect employees sharing a given attribute
    def connect_by(column: str):
        groups = df.groupby(column)["employee_id"].apply(list)
        for value, emp_ids in groups.items():
            if not value or len(emp_ids) < 2:
                continue
            # Fully connect all employees sharing this value
            for i in range(len(emp_ids)):
                for j in range(i + 1, len(emp_ids)):
                    u, v = emp_ids[i], emp_ids[j]
                    if G.has_edge(u, v):
                        # Increment weight if they share multiple attributes
                        G[u][v]["weight"] += 1
                    else:
                        G.add_edge(u, v, weight=1, reason=column)

    for col in ["mobile", "address", "bank_account"]:
        connect_by(col)

    return G


def _find_risky_clusters(G: nx.Graph, min_size: int = 5) -> List[Dict[str, Any]]:
    """Find connected components with more than `min_size` employees."""

    risky_clusters: List[Dict[str, Any]] = []
    for component in nx.connected_components(G):
        if len(component) > min_size:
            subgraph = G.subgraph(component)
            risky_clusters.append(
                {
                    "size": len(component),
                    "employee_ids": list(component),
                    "avg_degree": sum(dict(subgraph.degree()).values()) / float(len(component)),
                    "description": "Employees sharing contact or banking details – possible ghost or syndicate.",
                }
            )
    return risky_clusters


def _optional_push_to_neo4j(df: pd.DataFrame, uri: Optional[str], user: str = "neo4j", password: str = "password") -> None:
    """Optional demonstration of how we'd push the graph into Neo4j.

    For the hackathon demo we do not require a running Neo4j instance,
    but this function shows the Cypher pattern for judges.
    """

    if not uri or GraphDatabase is None:
        return

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        session.run("MATCH (e:Employee) DETACH DELETE e")
        for _, row in df.iterrows():
            session.run(
                """
                MERGE (e:Employee {employee_id: $employee_id})
                SET e.name = $name,
                    e.mobile = $mobile,
                    e.address = $address,
                    e.bank_account = $bank_account
                """,
                **row.to_dict(),
            )

        # Relationships for employees sharing bank accounts (most suspicious)
        groups = df.groupby("bank_account")["employee_id"].apply(list)
        for bank_account, emp_ids in groups.items():
            if len(emp_ids) < 2:
                continue
            for i in range(len(emp_ids)):
                for j in range(i + 1, len(emp_ids)):
                    session.run(
                        """
                        MATCH (e1:Employee {employee_id: $e1}), (e2:Employee {employee_id: $e2})
                        MERGE (e1)-[:SHARES_BANK_ACCOUNT {bank_account: $bank_account}]->(e2)
                        """,
                        e1=emp_ids[i],
                        e2=emp_ids[j],
                        bank_account=bank_account,
                    )

    driver.close()


def scan_payroll_csv(csv_bytes: bytes, min_cluster_size: int = 5, neo4j_uri: Optional[str] = None) -> Dict[str, Any]:
    """Entry point used by the FastAPI endpoint `/scan-payroll`.

    Args:
        csv_bytes: Raw CSV bytes uploaded by the user.
        min_cluster_size: Minimum size of connected component to flag.
        neo4j_uri: Optional bolt URI for Neo4j (e.g. `bolt://localhost:7687`).

    Returns:
        JSON-serializable dict with basic graph stats and risky clusters.
    """

    df = _load_payroll_dataframe(csv_bytes)

    # Optional: push to Neo4j for visualization / further analytics
    _optional_push_to_neo4j(df, uri=neo4j_uri)

    # In-memory NetworkX analysis (fast for hackathon data sizes)
    G = _build_networkx_graph(df)
    risky_clusters = _find_risky_clusters(G, min_size=min_cluster_size)

    return {
        "num_employees": int(G.number_of_nodes()),
        "num_edges": int(G.number_of_edges()),
        "num_risky_clusters": len(risky_clusters),
        "risky_clusters": risky_clusters,
    }

