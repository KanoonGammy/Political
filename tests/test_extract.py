import pytest
from src.extract.schema import EntityNode, RelationEdge, PoliticalGraph, EntityType, RelationType
from src.extract.extractor import extract_entities_and_relations_from_text, build_political_graph

def test_entity_node_schema():
    node = EntityNode(
        id="paetongtarn_shinawatra",
        name="แพทองธาร ชินวัตร",
        type=EntityType.PERSON,
        party="พรรคเพื่อไทย",
        role="นายกรัฐมนตรี",
        coalition="Government"
    )
    assert node.id == "paetongtarn_shinawatra"
    assert node.type == EntityType.PERSON
    assert node.party == "พรรคเพื่อไทย"

def test_relation_edge_schema():
    edge = RelationEdge(
        id="rel_1",
        source="paetongtarn_shinawatra",
        target="bhumjaithai_party",
        relation_type=RelationType.ALLIANCE,
        description="พรรคร่วมรัฐบาล",
        sentiment=0.8,
        date="2026-08-15",
        evidence="ยืนยันความร่วมมือแน่นแฟ้นในพรรคร่วมรัฐบาล",
        source_url="https://example.com"
    )
    assert edge.relation_type == RelationType.ALLIANCE
    assert edge.sentiment == 0.8

def test_extract_entities_and_relations():
    sample_text = "นายกรัฐมนตรี แพทองธาร ชินวัตร หัวหน้าพรรคเพื่อไทย ร่วมประชุมกับ อนุทิน ชาญวีรกูล หัวหน้าพรรคภูมิใจไทย เพื่อผลักดันนโยบายดิจิทัลวอลเล็ต ขณะที่ ณัฐพงษ์ เรืองปัญญาวุฒิ หัวหน้าพรรคประชาชน แถลงคัดค้านและยื่นเรื่องให้ กกต. ตรวจสอบ"
    nodes, edges = extract_entities_and_relations_from_text(
        text=sample_text,
        title="การประชุมพรรคร่วมรัฐบาลและการตรวจสอบของฝ่ายค้าน",
        date_str="2026-08-20",
        source_url="https://example.com/test"
    )
    
    node_names = [n.name for n in nodes]
    assert "แพทองธาร ชินวัตร" in node_names
    assert "อนุทิน ชาญวีรกูล" in node_names
    assert "ณัฐพงษ์ เรืองปัญญาวุฒิ" in node_names
    assert len(edges) > 0
