import os
import json
import pytest
from src.wiki.compiler import generate_entity_markdown, generate_mermaid_diagram
from src.wiki.linter import lint_wiki
from src.export.graphml_exporter import export_graph_to_graphml, export_graph_to_gexf
from src.extract.schema import EntityNode, RelationEdge, PoliticalGraph, EntityType, RelationType

def test_generate_mermaid_diagram():
    node = EntityNode(id="p1", name="นักการเมือง A", type=EntityType.PERSON, party="พรรคเพื่อไทย")
    edges = [
        RelationEdge(
            id="e1", source="p1", target="p2",
            relation_type=RelationType.ALLIANCE,
            description="พรรคร่วม",
            date="2026-08-20",
            evidence="ร่วมมือ",
            source_url=""
        )
    ]
    node_map = {"p1": node, "p2": EntityNode(id="p2", name="นักการเมือง B", type=EntityType.PERSON, party="พรรคภูมิใจไทย")}
    
    diagram = generate_mermaid_diagram(node, edges, node_map)
    assert "flowchart LR" in diagram
    assert "นักการเมือง A" in diagram
    assert "นักการเมือง B" in diagram
    assert "ALLIANCE" in diagram

def test_export_graphml(tmp_path):
    graph = PoliticalGraph(
        nodes=[
            EntityNode(id="p1", name="Node A", type=EntityType.PERSON, party="Party X"),
            EntityNode(id="p2", name="Node B", type=EntityType.PARTY, party="Party Y")
        ],
        edges=[
            RelationEdge(
                id="e1", source="p1", target="p2",
                relation_type=RelationType.ALLIANCE,
                description="test", date="2026-08-20", evidence="test", source_url=""
            )
        ],
        metadata={"total_nodes": 2}
    )
    
    out_file = str(tmp_path / "test_graph.graphml")
    export_graph_to_graphml(graph, out_file)
    assert os.path.exists(out_file)
    with open(out_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "<graphml" in content
        assert "Node A" in content
