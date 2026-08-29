import os
import json
import glob
from typing import List, Dict
from src.extract.schema import EntityNode, RelationEdge, PoliticalGraph

def generate_mermaid_diagram(node: EntityNode, edges: List[RelationEdge], node_map: Dict[str, EntityNode]) -> str:
    """Generates Mermaid flowchart diagram for entity network."""
    lines = ["```mermaid", "flowchart LR"]
    lines.append(f'    curr["{node.name}"]:::target')
    
    connected_edges = [e for e in edges if e.source == node.id or e.target == node.id][:8]
    if not connected_edges:
        lines.append("```")
        return "\n".join(lines)

    for idx, edge in enumerate(connected_edges):
        other_id = edge.target if edge.source == node.id else edge.source
        other_node = node_map.get(other_id)
        other_name = other_node.name if other_node else other_id
        
        node_def = f'n{idx}["{other_name}"]'
        rel_label = edge.relation_type.value
        
        if edge.source == node.id:
            lines.append(f'    curr -- "{rel_label}" --> {node_def}')
        else:
            lines.append(f'    {node_def} -- "{rel_label}" --> curr')

    lines.append("    classDef target fill:#1e40af,stroke:#60a5fa,stroke-width:2px,color:#ffffff;")
    lines.append("```")
    return "\n".join(lines)

def generate_entity_markdown(node: EntityNode, edges: List[RelationEdge], node_map: Dict[str, EntityNode]) -> str:
    """Generates LLM-Wiki entity article."""
    connected_edges = [e for e in edges if e.source == node.id or e.target == node.id]
    mermaid_block = generate_mermaid_diagram(node, edges, node_map)
    
    relations_list = []
    for e in connected_edges:
        other_id = e.target if e.source == node.id else e.source
        other_node = node_map.get(other_id)
        other_name = other_node.name if other_node else other_id
        relations_list.append(f"- **{e.relation_type.value}** ➔ [[entities/{other_id}|{other_name}]]: {e.description} (เมื่อ {e.date})\n  > *\"{e.evidence}\"*")

    relations_str = "\n".join(relations_list) if relations_list else "*ไม่มีประวัติความสัมพันธ์ในรอบ 30 วัน*"

    img_embed = f'<img src="{node.image_url}" alt="{node.name}" width="120" style="border-radius:50%; margin-bottom:12px;" />\n\n' if node.image_url else ""
    party_str = f"{node.party_symbol} {node.party}" if node.party_symbol and node.party else (node.party or 'อิสระ')

    return f"""---
id: "{node.id}"
title: "{node.name}"
type: "{node.type.value}"
party: "{node.party or ''}"
party_symbol: "{node.party_symbol or ''}"
role: "{node.role or ''}"
coalition: "{node.coalition or ''}"
mentions: {node.mention_count}
image_url: "{node.image_url or ''}"
party_logo_url: "{node.party_logo_url or ''}"
---

# {node.name}

{img_embed}> **สังกัด**: {party_str} | **บทบาท**: {node.role or '-'} | **ขั้วการเมือง**: {node.coalition or '-'}

## 📊 ข้อมูลสังเขป & สถิติ
- **การปรากฏในข่าว 30 วันล่าสุด**: {node.mention_count} ครั้ง
- **สถานะทางการเมือง**: {node.coalition or '-'}
- **ชื่อเรียก/ฉายา**: {', '.join(node.aliases) if node.aliases else '-'}

## 🌐 แผนผังความสัมพันธ์ (Semantic Network)
{mermaid_block}

## 🔗 โครงข่ายความสัมพันธ์และเหตุการณ์สำคัญ
{relations_str}

## 📑 เอกสารและข่าวที่เกี่ยวข้อง
- ดูสรุปข่าวรอบ 30 วันใน [[wiki/index#Source Summaries|Index Summaries]]
"""

def compile_wiki(data_file: str = "data/graph_data.json", wiki_dir: str = "wiki"):
    """Compiles entities, concepts, and master index into wiki markdown."""
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = [EntityNode(**n) for n in data["nodes"]]
    edges = [RelationEdge(**e) for e in data["edges"]]
    node_map = {n.id: n for n in nodes}

    # 1. Compile entities/
    ent_dir = os.path.join(wiki_dir, "entities")
    os.makedirs(ent_dir, exist_ok=True)
    for node in nodes:
        content = generate_entity_markdown(node, edges, node_map)
        filepath = os.path.join(ent_dir, f"{node.id}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    print(f"[OK] Compiled {len(nodes)} entity pages in {ent_dir}")

    # 2. Compile concepts/
    concept_dir = os.path.join(wiki_dir, "concepts")
    os.makedirs(concept_dir, exist_ok=True)
    
    concepts_data = {
        "Government_Coalition.md": ("พรรคร่วมรัฐบาล (Government Coalition)", "วิเคราะห์ขั้วรัฐบาลนำโดยพรรคเพื่อไทย ร่วมกับพรรคภูมิใจไทย รวมไทยสร้างชาติ และประชาธิปัตย์"),
        "Opposition_Bloc.md": ("พรรคฝ่ายค้าน (Opposition Bloc)", "พรรคฝ่ายค้านนำโดยพรรคประชาชน ขับเคลื่อนบทบาทตรวจสอบฝ่ายบริหารและการเมืองเชิงนโยบาย"),
        "Judicial_Politics_and_Petitions.md": ("นิติสงครามและการเมืองในศาล (Judicial Politics)", "การยื่นคำร้องต่อ กกต. ศาลรัฐธรรมนูญ และ ป.ป.ช. ในคดียุบพรรคและจริยธรรมนักการเมือง"),
        "Digital_Wallet_Policy.md": ("นโยบายดิจิทัลวอลเล็ต (Digital Wallet)", "นโยบายแจกเงินกระตุ้นเศรษฐกิจและการพิจารณางบประมาณในสภา"),
        "Constitutional_Amendment.md": ("การแก้ไขรัฐธรรมนูญ (Constitutional Amendment)", "ข้อถกเถียงการแก้รัฐธรรมนูญหมวดจริยธรรมและการตั้ง สสร.")
    }

    for c_file, (c_title, c_desc) in concepts_data.items():
        c_path = os.path.join(concept_dir, c_file)
        c_content = f"""---
title: "{c_title}"
type: "CONCEPT"
---

# {c_title}

> {c_desc}

## 📌 สาระสำคัญ & พลวัตในรอบ 30 วัน
ประเด็นและข้อถกเถียงทางการเมืองหลักที่มีผลต่อเสถียรภาพและทิศทางของประเทศ

## 👥 ตัวละครที่เกี่ยวข้อง
- [[entities/paetongtarn_shinawatra|แพทองธาร ชินวัตร]]
- [[entities/natthaphong_ruengpanyawut|ณัฐพงษ์ เรืองปัญญาวุฒิ]]
- [[entities/anutin_charnvirakul|อนุทิน ชาญวีรกูล]]
- [[entities/pheu_thai_party|พรรคเพื่อไทย]]
- [[entities/peoples_party|พรรคประชาชน]]
"""
        with open(c_path, "w", encoding="utf-8") as f:
            f.write(c_content)

    print(f"[OK] Compiled concept pages in {concept_dir}")

    # 3. Compile summaries catalog index
    all_summary_files = sorted(glob.glob("wiki/summaries/*.md"), reverse=True)
    all_summary_links = []
    for sf in all_summary_files:
        slug = os.path.splitext(os.path.basename(sf))[0]
        if slug != "index":
            all_summary_links.append(f"- [[summaries/{slug}]]")

    with open(os.path.join(wiki_dir, "summaries", "index.md"), "w", encoding="utf-8") as f:
        f.write(f"# All Summaries ({len(all_summary_links)})\n\n" + "\n".join(all_summary_links))

    # 4. Compile Master Index wiki/index.md
    entities_links = [f"- [[entities/{n.id}|{n.name}]] — {n.role or n.party} ({n.coalition})" for n in nodes]
    recent_summaries = all_summary_links[:20]

    index_content = f"""# Index — Thai Politics Knowledge Base (30-Day Intelligence Graph)

> Comprehensive semantic knowledge base and relationship network tracking Thai political dynamics, key actors, party coalitions, policy debates, and legal milestones.

## 🔖 Navigation
- [[#Concepts & Coalitions]] · [[#Key Actors & Entities]] · [[#Source Summaries]] · [[#Open Questions]]

## Concepts & Coalitions
### Political Coalitions & Dynamics
- [[concepts/Government_Coalition|พรรคร่วมรัฐบาล (Government Coalition)]] — Ruling coalition led by Pheu Thai Party and allied partners.
- [[concepts/Opposition_Bloc|พรรคฝ่ายค้าน (Opposition Bloc)]] — Parliamentary opposition led by People's Party (พรรคประชาชน) and allies.
- [[concepts/Judicial_Politics_and_Petitions|นิติสงครามและการเมืองในศาล]] — Petitions to Election Commission, Constitutional Court cases, and independent organ rulings.

### Major Policy & Political Debates
- [[concepts/Digital_Wallet_Policy|นโยบายดิจิทัลวอลเล็ต]] — Flagship economic stimulus initiative and associated political tensions.
- [[concepts/Constitutional_Amendment|การแก้ไขรัฐธรรมนูญ]] — Parliamentary debates on drafting a new constitution and charter amendment hurdles.

## Key Actors & Entities ({len(nodes)})
{chr(10).join(entities_links)}

## Source Summaries (Past 30 Days — Total {len(all_summary_links)})
- [[summaries/index|📑 ดูรายการสรุปข่าวทั้งหมด ({len(all_summary_links)} ข่าว)]]
{chr(10).join(recent_summaries)}

## Open Questions
- Q1: How do recent senatorial dynamics affect coalition legislative stability?
- Q2: What are the primary legal battlefronts between the ruling coalition and opposition parties?
"""
    with open(os.path.join(wiki_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)
        
    print(f"[OK] Rebuilt master catalog at {wiki_dir}/index.md")

if __name__ == "__main__":
    compile_wiki()
