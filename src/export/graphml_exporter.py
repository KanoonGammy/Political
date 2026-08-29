import os
import json
import networkx as nx
from src.extract.schema import PoliticalGraph

def build_networkx_graph(graph: PoliticalGraph) -> nx.DiGraph:
    """Converts PoliticalGraph schema to NetworkX DiGraph."""
    G = nx.DiGraph()

    for node in graph.nodes:
        G.add_node(
            node.id,
            label=node.name,
            entity_type=node.type.value,
            party=node.party or "",
            role=node.role or "",
            coalition=node.coalition or "",
            mentions=node.mention_count
        )

    for edge in graph.edges:
        G.add_edge(
            edge.source,
            edge.target,
            id=edge.id,
            relation_type=edge.relation_type.value,
            description=edge.description,
            sentiment=float(edge.sentiment),
            date=edge.date,
            weight=int(edge.weight),
            evidence=edge.evidence
        )

    return G

def export_graph_to_graphml(graph: PoliticalGraph, output_file: str = "data/political_graph.graphml"):
    """Exports graph to GraphML format."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    G = build_networkx_graph(graph)
    nx.write_graphml(G, output_file, encoding="utf-8")
    print(f"[OK] Exported GraphML to {output_file}")

def export_graph_to_gexf(graph: PoliticalGraph, output_file: str = "data/political_graph.gexf"):
    """Exports graph to Gephi GEXF format."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    G = build_networkx_graph(graph)
    nx.write_gexf(G, output_file, encoding="utf-8")
    print(f"[OK] Exported GEXF to {output_file}")

if __name__ == "__main__":
    with open("data/graph_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    graph = PoliticalGraph(**data)
    export_graph_to_graphml(graph)
    export_graph_to_gexf(graph)
