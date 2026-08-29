import os
import glob
import re
import json
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Optional, Set
from src.extract.schema import EntityType, RelationType, EntityNode, RelationEdge, PoliticalGraph

# Master Thai Political Entity Registry with metadata
KNOWN_ENTITIES: Dict[str, Dict] = {
    # Politicians
    "paetongtarn_shinawatra": {
        "name": "แพทองธาร ชินวัตร",
        "type": EntityType.PERSON,
        "party": "พรรคเพื่อไทย",
        "role": "นายกรัฐมนตรี",
        "coalition": "Government",
        "aliases": ["แพทองธาร", "อิ๊งค์", "อุ๊งอิ๊งค์", "นายกรัฐมนตรี", "นายกฯ"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Paetongtarn_Shinawatra_2024.jpg/440px-Paetongtarn_Shinawatra_2024.jpg"
    },
    "natthaphong_ruengpanyawut": {
        "name": "ณัฐพงษ์ เรืองปัญญาวุฒิ",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "ผู้นำฝ่ายค้านในสภาฯ / หัวหน้าพรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["ณัฐพงษ์", "เท้ง", "หัวหน้าพรรคประชาชน", "ผู้นำฝ่ายค้าน"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Natthaphong_Ruengpanyawut_2024.jpg/440px-Natthaphong_Ruengpanyawut_2024.jpg"
    },
    "anutin_charnvirakul": {
        "name": "อนุทิน ชาญวีรกูล",
        "type": EntityType.PERSON,
        "party": "พรรคภูมิใจไทย",
        "role": "รองนายกรัฐมนตรี และ รมว.มหาดไทย",
        "coalition": "Government",
        "aliases": ["อนุทิน", "เสี่ยหนู", "หัวหน้าพรรคภูมิใจไทย", "มท.1"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Anutin_Charnvirakul_in_2023.jpg/440px-Anutin_Charnvirakul_in_2023.jpg"
    },
    "pirapan_salerathavibhaga": {
        "name": "พีระพันธุ์ สาลีรัฐวิภาค",
        "type": EntityType.PERSON,
        "party": "พรรครวมไทยสร้างชาติ",
        "role": "รองนายกรัฐมนตรี และ รมว.พลังงาน",
        "coalition": "Government",
        "aliases": ["พีระพันธุ์", "หัวหน้าพรรครวมไทยสร้างชาติ"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Pirapan_Salirathavibhaga_2023.jpg/440px-Pirapan_Salirathavibhaga_2023.jpg"
    },
    "thaksin_shinawatra": {
        "name": "ทักษิณ ชินวัตร",
        "type": EntityType.PERSON,
        "party": "พรรคเพื่อไทย",
        "role": "อดีตนายกรัฐมนตรี",
        "coalition": "Government",
        "aliases": ["ทักษิณ", "อดีตนายกฯ ทักษิณ", "ทักษิณ ชินวัตร"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Thaksin_Shinawatra_2003_%28cropped%29.jpg/440px-Thaksin_Shinawatra_2003_%28cropped%29.jpg"
    },
    "chalermchai_sri_on": {
        "name": "เฉลิมชัย ศรีอ่อน",
        "type": EntityType.PERSON,
        "party": "พรรคประชาธิปัตย์",
        "role": "รมว.ทรัพยากรธรรมชาติฯ / หัวหน้าพรรคประชาธิปัตย์",
        "coalition": "Government",
        "aliases": ["เฉลิมชัย", "เฉลิมชัย ศรีอ่อน"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Chalermchai_Sri-on_in_2023.jpg/440px-Chalermchai_Sri-on_in_2023.jpg"
    },
    "sirikanya_tansakun": {
        "name": "ศิริกัญญา ตันสกุล",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "รองหัวหน้าพรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["ศิริกัญญา", "ไหม ศิริกัญญา"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Sirikanya_Tansakun_2023.jpg/440px-Sirikanya_Tansakun_2023.jpg"
    },
    "rangsiman_rome": {
        "name": "รังสิมันต์ โรม",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "ประธาน กมธ. ความมั่นคงฯ / สส. พรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["รังสิมันต์ โรม", "รังสิมันต์", "โรม"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Rangsiman_Rome_2023.jpg/440px-Rangsiman_Rome_2023.jpg"
    },
    "prawit_wongsuwan": {
        "name": "พล.อ.ประวิตร วงษ์สุวรรณ",
        "type": EntityType.PERSON,
        "party": "พรรคพลังประชารัฐ",
        "role": "หัวหน้าพรรคพลังประชารัฐ",
        "coalition": "Opposition",
        "aliases": ["ประวิตร", "บิ๊กป้อม", "พล.อ.ประวิตร", "พลเอกประวิตร"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Prawit_Wongsuwan_2019.jpg/440px-Prawit_Wongsuwan_2019.jpg"
    },
    "thammanat_prompow": {
        "name": "ร.อ.ธรรมนัส พรหมเผ่า",
        "type": EntityType.PERSON,
        "party": "พรรคพลังประชารัฐ (กลุ่มธรรมนัส)",
        "role": "อดีต รมว.เกษตรฯ / แกนนำกลุ่มการเมือง",
        "coalition": "Government",
        "aliases": ["ธรรมนัส", "ผู้กองธรรมนัส", "ร.อ.ธรรมนัส"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Thammanat_Prompow_2023.jpg/440px-Thammanat_Prompow_2023.jpg"
    },
    "parit_wacharasindhu": {
        "name": "พริษฐ์ วัชรสินธุ",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "โฆษกพรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["พริษฐ์", "ไอติม พริษฐ์", "พริษฐ์ วัชรสินธุ"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Parit_Wacharasindhu_2023.jpg/440px-Parit_Wacharasindhu_2023.jpg"
    },
    "raknok_srinork": {
        "name": "รักชนก ศรีนอก",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "สส.กทม. พรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["รักชนก", "ไอซ์ รักชนก"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Rukchanok_Srinork_2023.jpg/440px-Rukchanok_Srinork_2023.jpg"
    },
    "prajak_kongkirati": {
        "name": "ประจักษ์ ก้องกีรติ",
        "type": EntityType.PERSON,
        "party": "อิสระ",
        "role": "นักวิชาการด้านรัฐศาสตร์",
        "coalition": "Independent",
        "aliases": ["ประจักษ์", "ศ.ดร.ประจักษ์ ก้องกีรติ"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/User_icon_2.svg/300px-User_icon_2.svg.png"
    },

    # Political Parties
    "pheu_thai_party": {
        "name": "พรรคเพื่อไทย",
        "type": EntityType.PARTY,
        "party": "พรรคเพื่อไทย",
        "role": "แกนนำพรรคร่วมรัฐบาล",
        "coalition": "Government",
        "aliases": ["พรรคเพื่อไทย", "เพื่อไทย", "พท."],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Pheu_Thai_Party_logo.svg/500px-Pheu_Thai_Party_logo.svg.png"
    },
    "peoples_party": {
        "name": "พรรคประชาชน",
        "type": EntityType.PARTY,
        "party": "พรรคประชาชน",
        "role": "พรรคแกนนำฝ่ายค้าน",
        "coalition": "Opposition",
        "aliases": ["พรรคประชาชน", "ประชาชน", "พรรคส้ม", "ค่ายส้ม"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Peoples_Party_%28Thailand%29_logo.svg/500px-Peoples_Party_%28Thailand%29_logo.svg.png"
    },
    "bhumjaithai_party": {
        "name": "พรรคภูมิใจไทย",
        "type": EntityType.PARTY,
        "party": "พรรคภูมิใจไทย",
        "role": "พรรคร่วมรัฐบาล",
        "coalition": "Government",
        "aliases": ["พรรคภูมิใจไทย", "ภูมิใจไทย", "ภท.", "ค่ายน้ำเงิน"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Bhumjaithai_Party_logo.svg/500px-Bhumjaithai_Party_logo.svg.png"
    },
    "united_thai_nation_party": {
        "name": "พรรครวมไทยสร้างชาติ",
        "type": EntityType.PARTY,
        "party": "พรรครวมไทยสร้างชาติ",
        "role": "พรรคร่วมรัฐบาล",
        "coalition": "Government",
        "aliases": ["พรรครวมไทยสร้างชาติ", "รวมไทยสร้างชาติ", "รทสช."],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/United_Thai_Nation_Party_logo.svg/500px-United_Thai_Nation_Party_logo.svg.png"
    },
    "democrat_party": {
        "name": "พรรคประชาธิปัตย์",
        "type": EntityType.PARTY,
        "party": "พรรคประชาธิปัตย์",
        "role": "พรรคร่วมรัฐบาล",
        "coalition": "Government",
        "aliases": ["พรรคประชาธิปัตย์", "ประชาธิปัตย์", "ปชป."],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Democrat_Party_%28Thailand%29_logo.svg/500px-Democrat_Party_%28Thailand%29_logo.svg.png"
    },
    "palang_pracharath_party": {
        "name": "พรรคพลังประชารัฐ",
        "type": EntityType.PARTY,
        "party": "พรรคพลังประชารัฐ",
        "role": "พรรคการเมืองฝ่ายค้าน / แตกขั้ว",
        "coalition": "Opposition",
        "aliases": ["พรรคพลังประชารัฐ", "พลังประชารัฐ", "พปชร."],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Palang_Pracharath_Party_logo.svg/500px-Palang_Pracharath_Party_logo.svg.png"
    },

    # State & Judicial Institutions
    "constitutional_court": {
        "name": "ศาลรัฐธรรมนูญ",
        "type": EntityType.INSTITUTION,
        "party": "ตุลาการ",
        "role": "ศาลสูงสุดด้านรัฐธรรมนูญ",
        "coalition": "Judicial",
        "aliases": ["ศาลรัฐธรรมนูญ", "ศาล รธน."],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Emblem_of_the_Constitutional_Court_of_Thailand.svg/500px-Emblem_of_the_Constitutional_Court_of_Thailand.svg.png"
    },
    "election_commission": {
        "name": "คณะกรรมการการเลือกตั้ง (กกต.)",
        "type": EntityType.INSTITUTION,
        "party": "องค์กรอิสระ",
        "role": "องค์กรควบคุมการเลือกตั้งและตรวจสอบพรรคการเมือง",
        "coalition": "Independent",
        "aliases": ["กกต.", "คณะกรรมการการเลือกตั้ง", "สำนักงาน กกต."],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Seal_of_the_Election_Commission_of_Thailand.svg/500px-Seal_of_the_Election_Commission_of_Thailand.svg.png"
    },
    "nacc": {
        "name": "คณะกรรมการ ป.ป.ช.",
        "type": EntityType.INSTITUTION,
        "party": "องค์กรอิสระ",
        "role": "องค์กรป้องกันและปราบปรามการทุจริตแห่งชาติ",
        "coalition": "Independent",
        "aliases": ["ป.ป.ช.", "คณะกรรมการป้องกันและปราบปรามการทุจริตแห่งชาติ", "สำนักงาน ป.ป.ช."],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Seal_of_the_National_Anti-Corruption_Commission_of_Thailand.svg/500px-Seal_of_the_National_Anti-Corruption_Commission_of_Thailand.svg.png"
    },
    "senate_thailand": {
        "name": "วุฒิสภา (สว.)",
        "type": EntityType.INSTITUTION,
        "party": "สถาบันนิติบัญญัติ",
        "role": "สภาสูง / กลั่นกรองกฎหมายและแต่งตั้งองค์กรอิสระ",
        "coalition": "Independent",
        "aliases": ["วุฒิสภา", "สว.", "สมาชิกวุฒิสภา", "สภาสูง"],
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Emblem_of_the_Senate_of_Thailand.svg/500px-Emblem_of_the_Senate_of_Thailand.svg.png"
    },

    # Key Policies & Events
    "digital_wallet_policy": {
        "name": "นโยบายดิจิทัลวอลเล็ต 10,000 บาท",
        "type": EntityType.POLICY,
        "party": "พรรคเพื่อไทย",
        "role": "นโยบายเรือธงกระตุ้นเศรษฐกิจ",
        "coalition": "Government",
        "aliases": ["ดิจิทัลวอลเล็ต", "แจกเงินหมื่น", "เงิน 10,000 บาท", "ดิจิทัลวอลเล็ต 10,000 บาท"],
        "image_url": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=400&auto=format&fit=crop&q=80"
    },
    "constitution_amendment": {
        "name": "การแก้ไขรัฐธรรมนูญ",
        "type": EntityType.POLICY,
        "party": "รัฐสภา",
        "role": "วาระการปฏิรูปกติกาการเมืองและหมวดจริยธรรม",
        "coalition": "Cross-Party",
        "aliases": ["แก้รัฐธรรมนูญ", "แก้ไขรัฐธรรมนูญ", "แก้ รธน.", "แก้มาตรฐานจริยธรรม"],
        "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400&auto=format&fit=crop&q=80"
    }
}

def find_entities_in_text(text: str) -> List[Tuple[str, Dict]]:
    """Identifies mentioned political entities in a text."""
    found = []
    for entity_id, meta in KNOWN_ENTITIES.items():
        matched = False
        if meta["name"] in text:
            matched = True
        else:
            for alias in meta["aliases"]:
                if alias in text:
                    matched = True
                    break
        if matched:
            found.append((entity_id, meta))
    return found

def classify_relation(source_meta: Dict, target_meta: Dict, sentence: str) -> Tuple[RelationType, str, float]:
    """Infers semantic relation type, description, and sentiment between two entities in context."""
    s_name = source_meta["name"]
    t_name = target_meta["name"]
    
    # 1. Legal / Investigation
    if any(k in sentence for k in ["ยื่นร้อง", "ฟ้อง", "ไต่สวน", "วินิจฉัย", "ยุบพรรค", "คำร้อง", "จริยธรรม", "สอบข้อเท็จจริง"]):
        if source_meta["type"] in (EntityType.INSTITUTION, EntityType.PERSON) or target_meta["type"] in (EntityType.INSTITUTION, EntityType.PARTY):
            return RelationType.LEGAL_ACTION, f"กระบวนการทางกฎหมาย/ตรวจสอบระหว่าง {s_name} และ {t_name}", -0.6

    # 2. Opposition / Conflict / Criticism
    if any(k in sentence for k in ["คัดค้าน", "วิจารณ์", "ซัด", "โจมตี", "ตรวจสอบ", "อภิปราย", "จี้", "ขัดแย้ง", "แฉ", "ไม่ไว้วางใจ"]):
        return RelationType.CRITICISM, f"{s_name} วิพากษ์วิจารณ์/ตรวจสอบท่าทีของ {t_name}", -0.7

    # 3. Alliance / Coalition cooperation
    if any(k in sentence for k in ["ร่วมมือ", "พรรคร่วม", "จับมือ", "สนับสนุน", "โหวตหนุน", "เห็นชอบ", "ราบรื่น", "เหนียวแน่น", "ร่วมรัฐบาล"]):
        return RelationType.ALLIANCE, f"{s_name} และ {t_name} ร่วมมือทางการเมือง/พรรคร่วมรัฐบาล", 0.8

    # 4. Membership / Affiliation
    if source_meta.get("party") == target_meta.get("name") or target_meta.get("party") == source_meta.get("name"):
        return RelationType.MEMBER_OF, f"{s_name} สังกัด/ดำรงตำแหน่งใน {t_name}", 0.5

    # 5. Default Co-occurrence interaction
    if source_meta.get("coalition") == target_meta.get("coalition") and source_meta.get("coalition") in ("Government", "Opposition"):
        return RelationType.ALLIANCE, f"{s_name} และ {t_name} ในขั้วการเมืองเดียวกัน ({source_meta.get('coalition')})", 0.4
    else:
        return RelationType.OPPOSITION, f"{s_name} และ {t_name} มีปฏิสัมพันธ์ในประเด็นการเมือง", -0.2

def extract_entities_and_relations_from_text(
    text: str,
    title: str,
    date_str: str,
    source_url: str
) -> Tuple[List[EntityNode], List[RelationEdge]]:
    """Extracts entity nodes and semantic relation edges from a news article."""
    full_content = f"{title}\n{text}"
    found_entities = find_entities_in_text(full_content)
    
    nodes: List[EntityNode] = []
    for ent_id, meta in found_entities:
        node = EntityNode(
            id=ent_id,
            name=meta["name"],
            type=meta["type"],
            party=meta.get("party"),
            role=meta.get("role"),
            coalition=meta.get("coalition"),
            aliases=meta.get("aliases", []),
            mention_count=1,
            wiki_link=f"[[entities/{ent_id}]]",
            image_url=meta.get("image_url")
        )
        nodes.append(node)

    edges: List[RelationEdge] = []
    sentences = [s.strip() for s in re.split(r"[\n\.\?!]", full_content) if len(s.strip()) > 15]

    for i in range(len(found_entities)):
        for j in range(i + 1, len(found_entities)):
            src_id, src_meta = found_entities[i]
            tgt_id, tgt_meta = found_entities[j]

            # Find matching context sentences
            matched_sentences = [
                s for s in sentences
                if (src_meta["name"] in s or any(a in s for a in src_meta["aliases"]))
                and (tgt_meta["name"] in s or any(a in s for a in tgt_meta["aliases"]))
            ]

            evidence = matched_sentences[0] if matched_sentences else title
            rel_type, desc, sentiment = classify_relation(src_meta, tgt_meta, evidence)

            edge_id = f"{src_id}__{tgt_id}__{hashlib.md5(evidence.encode('utf-8')).hexdigest()[:6]}"
            edge = RelationEdge(
                id=edge_id,
                source=src_id,
                target=tgt_id,
                relation_type=rel_type,
                description=desc,
                sentiment=sentiment,
                date=date_str,
                evidence=evidence[:250],
                source_url=source_url,
                weight=1
            )
            edges.append(edge)

    return nodes, edges

def build_political_graph(raw_dir: str = "raw/articles") -> PoliticalGraph:
    """Processes all raw articles and builds a consolidated PoliticalGraph."""
    files = glob.glob(os.path.join(raw_dir, "*.md"))
    print(f"[*] Extracting knowledge graph from {len(files)} raw news files...")

    node_map: Dict[str, EntityNode] = {}
    edge_map: Dict[str, RelationEdge] = {}

    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse frontmatter
        title_match = re.search(r'title:\s*"(.*?)"', content)
        url_match = re.search(r'url:\s*"(.*?)"', content)
        date_match = re.search(r'published_at:\s*"(.*?)"', content)

        title = title_match.group(1) if title_match else os.path.basename(filepath)
        url = url_match.group(1) if url_match else ""
        date_raw = date_match.group(1) if date_match else datetime.now(timezone.utc).isoformat()
        date_str = date_raw[:10]

        nodes, edges = extract_entities_and_relations_from_text(content, title, date_str, url)

        for n in nodes:
            if n.id in node_map:
                node_map[n.id].mention_count += 1
            else:
                node_map[n.id] = n

        for e in edges:
            pair_key = f"{min(e.source, e.target)}__{max(e.source, e.target)}__{e.relation_type.value}"
            if pair_key in edge_map:
                edge_map[pair_key].weight += 1
                # Update with latest date
                if e.date > edge_map[pair_key].date:
                    edge_map[pair_key].date = e.date
                    edge_map[pair_key].evidence = e.evidence
                    edge_map[pair_key].source_url = e.source_url
            else:
                edge_map[pair_key] = e

    all_nodes = list(node_map.values())
    all_edges = list(edge_map.values())

    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_nodes": len(all_nodes),
        "total_edges": len(all_edges),
        "articles_analyzed": len(files),
        "date_range": "Past 30 Days"
    }

    graph = PoliticalGraph(
        nodes=all_nodes,
        edges=all_edges,
        metadata=metadata
    )

    return graph

def save_graph_data(graph: PoliticalGraph, output_file: str = "data/graph_data.json"):
    """Saves serialized graph data to JSON (both data/ and web/data/ for GitHub Pages/web)."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(graph.model_dump(), f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved Political Graph to {output_file} ({len(graph.nodes)} nodes, {len(graph.edges)} edges)")
    
    # Also write copy to web/data/ for web server and GitHub Pages
    web_output = "web/data/graph_data.json"
    os.makedirs(os.path.dirname(web_output), exist_ok=True)
    with open(web_output, "w", encoding="utf-8") as f:
        json.dump(graph.model_dump(), f, ensure_ascii=False, indent=2)
    print(f"[OK] Synced copy to {web_output}")

if __name__ == "__main__":
    graph = build_political_graph()
    save_graph_data(graph)
