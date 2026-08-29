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
    # Key Politicians (Persons) - Real Verified Portrait Photos
    "paetongtarn_shinawatra": {
        "name": "แพทองธาร ชินวัตร",
        "type": EntityType.PERSON,
        "party": "พรรคเพื่อไทย",
        "role": "นายกรัฐมนตรี",
        "coalition": "Government",
        "aliases": ["แพทองธาร", "อิ๊งค์", "อุ๊งอิ๊งค์", "นายกรัฐมนตรี", "นายกฯ"],
        "image_url": "images/avatars/paetongtarn_shinawatra.jpg"
    },
    "natthaphong_ruengpanyawut": {
        "name": "ณัฐพงษ์ เรืองปัญญาวุฒิ",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "ผู้นำฝ่ายค้านในสภาฯ / หัวหน้าพรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["ณัฐพงษ์", "เท้ง", "หัวหน้าพรรคประชาชน", "ผู้นำฝ่ายค้าน"],
        "image_url": "images/avatars/natthaphong_ruengpanyawut.jpg"
    },
    "anutin_charnvirakul": {
        "name": "อนุทิน ชาญวีรกูล",
        "type": EntityType.PERSON,
        "party": "พรรคภูมิใจไทย",
        "role": "รองนายกรัฐมนตรี และ รมว.มหาดไทย",
        "coalition": "Government",
        "aliases": ["อนุทิน", "เสี่ยหนู", "หัวหน้าพรรคภูมิใจไทย", "มท.1"],
        "image_url": "images/avatars/anutin_charnvirakul.jpg"
    },
    "pirapan_salerathavibhaga": {
        "name": "พีระพันธุ์ สาลีรัฐวิภาค",
        "type": EntityType.PERSON,
        "party": "พรรครวมไทยสร้างชาติ",
        "role": "รองนายกรัฐมนตรี และ รมว.พลังงาน",
        "coalition": "Government",
        "aliases": ["พีระพันธุ์", "หัวหน้าพรรครวมไทยสร้างชาติ"],
        "image_url": "images/avatars/pirapan_salerathavibhaga.jpg"
    },
    "thaksin_shinawatra": {
        "name": "ทักษิณ ชินวัตร",
        "type": EntityType.PERSON,
        "party": "พรรคเพื่อไทย",
        "role": "อดีตนายกรัฐมนตรี",
        "coalition": "Government",
        "aliases": ["ทักษิณ", "อดีตนายกฯ ทักษิณ", "ทักษิณ ชินวัตร"],
        "image_url": "images/avatars/thaksin_shinawatra.jpg"
    },
    "chalermchai_sri_on": {
        "name": "เฉลิมชัย ศรีอ่อน",
        "type": EntityType.PERSON,
        "party": "พรรคประชาธิปัตย์",
        "role": "รมว.ทรัพยากรธรรมชาติฯ / หัวหน้าพรรคประชาธิปัตย์",
        "coalition": "Government",
        "aliases": ["เฉลิมชัย", "เฉลิมชัย ศรีอ่อน"],
        "image_url": "images/avatars/chalermchai_sri_on.jpg"
    },
    "sirikanya_tansakun": {
        "name": "ศิริกัญญา ตันสกุล",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "รองหัวหน้าพรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["ศิริกัญญา", "ไหม ศิริกัญญา"],
        "image_url": "images/avatars/sirikanya_tansakun.jpg"
    },
    "rangsiman_rome": {
        "name": "รังสิมันต์ โรม",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "ประธาน กมธ. ความมั่นคงฯ / สส. พรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["รังสิมันต์ โรม", "รังสิมันต์", "โรม"],
        "image_url": "images/avatars/rangsiman_rome.jpg"
    },
    "prawit_wongsuwan": {
        "name": "พล.อ.ประวิตร วงษ์สุวรรณ",
        "type": EntityType.PERSON,
        "party": "พรรคพลังประชารัฐ",
        "role": "หัวหน้าพรรคพลังประชารัฐ",
        "coalition": "Opposition",
        "aliases": ["ประวิตร", "บิ๊กป้อม", "พล.อ.ประวิตร", "พลเอกประวิตร"],
        "image_url": "images/avatars/prawit_wongsuwan.jpg"
    },
    "thammanat_prompow": {
        "name": "ร.อ.ธรรมนัส พรหมเผ่า",
        "type": EntityType.PERSON,
        "party": "พรรคพลังประชารัฐ (กลุ่มธรรมนัส)",
        "role": "อดีต รมว.เกษตรฯ / แกนนำกลุ่มการเมือง",
        "coalition": "Government",
        "aliases": ["ธรรมนัส", "ผู้กองธรรมนัส", "ร.อ.ธรรมนัส"],
        "image_url": "images/avatars/thammanat_prompow.jpg"
    },
    "parit_wacharasindhu": {
        "name": "พริษฐ์ วัชรสินธุ",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "โฆษกพรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["พริษฐ์", "ไอติม พริษฐ์", "พริษฐ์ วัชรสินธุ"],
        "image_url": "images/avatars/parit_wacharasindhu.jpg"
    },
    "raknok_srinork": {
        "name": "รักชนก ศรีนอก",
        "type": EntityType.PERSON,
        "party": "พรรคประชาชน",
        "role": "สส.กทม. พรรคประชาชน",
        "coalition": "Opposition",
        "aliases": ["รักชนก", "ไอซ์ รักชนก"],
        "image_url": "images/avatars/raknok_srinork.jpg"
    },

    # --- Senate Collusion & Investigation Key Figures (คดีฮั้ว สว.) ---
    "mongkol_surasajja": {
        "name": "มงคล สุระสัจจะ",
        "type": EntityType.PERSON,
        "party": "วุฒิสภา (สายสีน้ำเงิน)",
        "role": "ประธานวุฒิสภา / ผู้ถูกกล่าวหาคดีฮั้ว สว. 229 ราย",
        "coalition": "Senate-Blue",
        "aliases": ["มงคล สุระสัจจะ", "มงคล", "ประธานวุฒิสภา", "ประธาน สว."],
        "image_url": "images/avatars/mongkol_surasajja.jpg"
    },
    "kriangkrai_srirak": {
        "name": "พล.อ.เกรียงไกร ศรีรักษ์",
        "type": EntityType.PERSON,
        "party": "วุฒิสภา (สายสีน้ำเงิน)",
        "role": "รองประธานวุฒิสภา คนที่ 1 / แกนนำ สว. สายสีน้ำเงิน",
        "coalition": "Senate-Blue",
        "aliases": ["เกรียงไกร ศรีรักษ์", "พล.อ.เกรียงไกร", "บิ๊กเกรียง", "รองประธานวุฒิสภา คนที่ 1"],
        "image_url": "images/avatars/kriangkrai_srirak.jpg"
    },
    "nanthana_nanthavaropas": {
        "name": "นันทนา นันทวโรภาส",
        "type": EntityType.PERSON,
        "party": "วุฒิสภา (กลุ่มพันธุ์ใหม่)",
        "role": "สมาชิกวุฒิสภา / แกนนำ สว. กลุ่มพันธุ์ใหม่ (ฝ่ายตรวจสอบ)",
        "coalition": "Senate-NewBreed",
        "aliases": ["นันทนา นันทวโรภาส", "นันทนา", "ดร.นันทนา", "สว.นันทนา"],
        "image_url": "images/avatars/nanthana_nanthavaropas.jpg"
    },
    "tewarit_maneechay": {
        "name": "เทวฤทธิ์ มณีฉาย",
        "type": EntityType.PERSON,
        "party": "วุฒิสภา (กลุ่มพันธุ์ใหม่)",
        "role": "สมาชิกวุฒิสภา / โฆษก สว. กลุ่มพันธุ์ใหม่",
        "coalition": "Senate-NewBreed",
        "aliases": ["เทวฤทธิ์ มณีฉาย", "เทวฤทธิ์", "สว.เทวฤทธิ์"],
        "image_url": "images/avatars/tewarit_maneechay.jpg"
    },
    "boonsong_noisophon": {
        "name": "บุญส่ง น้อยโสภณ",
        "type": EntityType.PERSON,
        "party": "วุฒิสภา",
        "role": "รองประธานวุฒิสภา คนที่ 2 / อดีต กกต.",
        "coalition": "Independent",
        "aliases": ["บุญส่ง น้อยโสภณ", "บุญส่ง", "รองประธานวุฒิสภา คนที่ 2"],
        "image_url": "images/avatars/boonsong_noisophon.jpg"
    },
    "itthiporn_boonpracong": {
        "name": "อิทธิพร บุญประคอง",
        "type": EntityType.PERSON,
        "party": "องค์กรอิสระ (กกต.)",
        "role": "ประธานคณะกรรมการการเลือกตั้ง (กกต.)",
        "coalition": "Independent",
        "aliases": ["อิทธิพร บุญประคอง", "อิทธิพร", "ประธาน กกต."],
        "image_url": "images/avatars/itthiporn_boonpracong.jpg"
    },
    "sawaeng_boonmee": {
        "name": "แสวง บุญมี",
        "type": EntityType.PERSON,
        "party": "องค์กรอิสระ (กกต.)",
        "role": "เลขาธิการ กกต. (ผู้รับผิดชอบสำนวนคดีฮั้ว สว.)",
        "coalition": "Independent",
        "aliases": ["แสวง บุญมี", "แสวง", "เลขาธิการ กกต."],
        "image_url": "images/avatars/sawaeng_boonmee.jpg"
    },
    "somchai_sawangkarn": {
        "name": "สมชาย แสวงการ",
        "type": EntityType.PERSON,
        "party": "อดีตวุฒิสภา / ผู้ร้องเรียน",
        "role": "อดีต สว. / ผู้ยื่นหลักฐานเส้นทางการเงินและโพยฮั้ว สว.",
        "coalition": "Independent",
        "aliases": ["สมชาย แสวงการ", "สมชาย"],
        "image_url": "images/avatars/somchai_sawangkarn.jpg"
    },
    "yingcheep_atchanont": {
        "name": "ยิ่งชีพ อัชฌานนท์",
        "type": EntityType.PERSON,
        "party": "ภาคประชาสังคม (iLaw)",
        "role": "ผู้จัดการ iLaw / ผู้เปิดโปงสถิติบล็อกโหวต สว.67",
        "coalition": "Independent",
        "aliases": ["ยิ่งชีพ อัชฌานนท์", "ยิ่งชีพ", "เป๋า ยิ่งชีพ", "iLaw"],
        "image_url": "images/avatars/yingcheep_atchanont.jpg"
    },

    # Political Parties (Official Logos)
    "pheu_thai_party": {
        "name": "พรรคเพื่อไทย",
        "type": EntityType.PARTY,
        "party": "พรรคเพื่อไทย",
        "role": "แกนนำพรรคร่วมรัฐบาล",
        "coalition": "Government",
        "aliases": ["พรรคเพื่อไทย", "เพื่อไทย", "พท."],
        "image_url": "images/logos/pheu_thai_party.jpg"
    },
    "peoples_party": {
        "name": "พรรคประชาชน",
        "type": EntityType.PARTY,
        "party": "พรรคประชาชน",
        "role": "พรรคแกนนำฝ่ายค้าน",
        "coalition": "Opposition",
        "aliases": ["พรรคประชาชน", "ประชาชน", "พรรคส้ม", "ค่ายส้ม"],
        "image_url": "images/logos/peoples_party.jpg"
    },
    "bhumjaithai_party": {
        "name": "พรรคภูมิใจไทย",
        "type": EntityType.PARTY,
        "party": "พรรคภูมิใจไทย",
        "role": "พรรคร่วมรัฐบาล",
        "coalition": "Government",
        "aliases": ["พรรคภูมิใจไทย", "ภูมิใจไทย", "ภท.", "ค่ายน้ำเงิน"],
        "image_url": "images/logos/bhumjaithai_party.jpg"
    },
    "united_thai_nation_party": {
        "name": "พรรครวมไทยสร้างชาติ",
        "type": EntityType.PARTY,
        "party": "พรรครวมไทยสร้างชาติ",
        "role": "พรรคร่วมรัฐบาล",
        "coalition": "Government",
        "aliases": ["พรรครวมไทยสร้างชาติ", "รวมไทยสร้างชาติ", "รทสช."],
        "image_url": "images/logos/united_thai_nation_party.jpg"
    },
    "democrat_party": {
        "name": "พรรคประชาธิปัตย์",
        "type": EntityType.PARTY,
        "party": "พรรคประชาธิปัตย์",
        "role": "พรรคร่วมรัฐบาล",
        "coalition": "Government",
        "aliases": ["พรรคประชาธิปัตย์", "ประชาธิปัตย์", "ปชป."],
        "image_url": "images/logos/democrat_party.jpg"
    },
    "palang_pracharath_party": {
        "name": "พรรคพลังประชารัฐ",
        "type": EntityType.PARTY,
        "party": "พรรคพลังประชารัฐ",
        "role": "พรรคการเมืองฝ่ายค้าน / แตกขั้ว",
        "coalition": "Opposition",
        "aliases": ["พรรคพลังประชารัฐ", "พลังประชารัฐ", "พปชร."],
        "image_url": "images/logos/palang_pracharath_party.jpg"
    },

    # State & Judicial Institutions
    "constitutional_court": {
        "name": "ศาลรัฐธรรมนูญ",
        "type": EntityType.INSTITUTION,
        "party": "ตุลาการ",
        "role": "ศาลสูงสุดด้านรัฐธรรมนูญ",
        "coalition": "Judicial",
        "aliases": ["ศาลรัฐธรรมนูญ", "ศาล รธน."],
        "image_url": "images/logos/constitutional_court.jpg"
    },
    "election_commission": {
        "name": "คณะกรรมการการเลือกตั้ง (กกต.)",
        "type": EntityType.INSTITUTION,
        "party": "องค์กรอิสระ",
        "role": "องค์กรควบคุมการเลือกตั้งและตรวจสอบพรรคการเมือง",
        "coalition": "Independent",
        "aliases": ["กกต.", "คณะกรรมการการเลือกตั้ง", "สำนักงาน กกต."],
        "image_url": "images/logos/election_commission.jpg"
    },
    "nacc": {
        "name": "คณะกรรมการ ป.ป.ช.",
        "type": EntityType.INSTITUTION,
        "party": "องค์กรอิสระ",
        "role": "องค์กรป้องกันและปราบปรามการทุจริตแห่งชาติ",
        "coalition": "Independent",
        "aliases": ["ป.ป.ช.", "คณะกรรมการป้องกันและปราบปรามการทุจริตแห่งชาติ", "สำนักงาน ป.ป.ช."],
        "image_url": "images/logos/nacc.jpg"
    },
    "senate_thailand": {
        "name": "วุฒิสภา (สว.)",
        "type": EntityType.INSTITUTION,
        "party": "สถาบันนิติบัญญัติ",
        "role": "สภาสูง / กลั่นกรองกฎหมายและแต่งตั้งองค์กรอิสระ",
        "coalition": "Independent",
        "aliases": ["วุฒิสภา", "สว.", "สมาชิกวุฒิสภา", "สภาสูง"],
        "image_url": "images/logos/senate_thailand.jpg"
    },

    # Key Policies & Events
    "digital_wallet_policy": {
        "name": "นโยบายดิจิทัลวอลเล็ต 10,000 บาท",
        "type": EntityType.POLICY,
        "party": "พรรคเพื่อไทย",
        "role": "นโยบายเรือธงกระตุ้นเศรษฐกิจ",
        "coalition": "Government",
        "aliases": ["ดิจิทัลวอลเล็ต", "แจกเงินหมื่น", "เงิน 10,000 บาท", "ดิจิทัลวอลเล็ต 10,000 บาท"],
        "image_url": "images/logos/digital_wallet_policy.jpg"
    },
    "constitution_amendment": {
        "name": "การแก้ไขรัฐธรรมนูญ",
        "type": EntityType.POLICY,
        "party": "รัฐสภา",
        "role": "วาระการปฏิรูปกติกาการเมืองและหมวดจริยธรรม",
        "coalition": "Cross-Party",
        "aliases": ["แก้รัฐธรรมนูญ", "แก้ไขรัฐธรรมนูญ", "แก้ รธน.", "แก้มาตรฐานจริยธรรม"],
        "image_url": "images/logos/constitution_amendment.jpg"
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

PARTY_METADATA: Dict[str, Dict] = {
    "พรรคเพื่อไทย": {
        "symbol": "🔴",
        "logo_url": "images/logos/pheu_thai_party.jpg"
    },
    "พรรคประชาชน": {
        "symbol": "🟠",
        "logo_url": "images/logos/peoples_party.jpg"
    },
    "พรรคภูมิใจไทย": {
        "symbol": "🔵",
        "logo_url": "images/logos/bhumjaithai_party.jpg"
    },
    "พรรครวมไทยสร้างชาติ": {
        "symbol": "🔷",
        "logo_url": "images/logos/united_thai_nation_party.jpg"
    },
    "พรรคประชาธิปัตย์": {
        "symbol": "🟦",
        "logo_url": "images/logos/democrat_party.jpg"
    },
    "พรรคพลังประชารัฐ": {
        "symbol": "🟢",
        "logo_url": "images/logos/palang_pracharath_party.jpg"
    },
    "พรรคพลังประชารัฐ (กลุ่มธรรมนัส)": {
        "symbol": "🟢",
        "logo_url": "images/logos/palang_pracharath_party.jpg"
    },
    "ตุลาการ": {
        "symbol": "⚖️",
        "logo_url": "images/logos/constitutional_court.jpg"
    },
    "องค์กรอิสระ": {
        "symbol": "🛡️",
        "logo_url": "images/logos/election_commission.jpg"
    },
    "องค์กรอิสระ (กกต.)": {
        "symbol": "🛡️",
        "logo_url": "images/logos/election_commission.jpg"
    },
    "สถาบันนิติบัญญัติ": {
        "symbol": "🏛️",
        "logo_url": "images/logos/senate_thailand.jpg"
    },
    "วุฒิสภา": {
        "symbol": "🏛️",
        "logo_url": "images/logos/senate_thailand.jpg"
    },
    "วุฒิสภา (สายสีน้ำเงิน)": {
        "symbol": "🏛️🔵",
        "logo_url": "images/logos/senate_thailand.jpg"
    },
    "วุฒิสภา (กลุ่มพันธุ์ใหม่)": {
        "symbol": "🏛️🌱",
        "logo_url": "images/logos/senate_thailand.jpg"
    },
    "อดีตวุฒิสภา / ผู้ร้องเรียน": {
        "symbol": "🔍",
        "logo_url": "images/logos/senate_thailand.jpg"
    },
    "ภาคประชาสังคม (iLaw)": {
        "symbol": "👁️",
        "logo_url": "images/logos/senate_thailand.jpg"
    },
    "รัฐสภา": {
        "symbol": "📜",
        "logo_url": "images/logos/senate_thailand.jpg"
    }
}

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
        party_name = meta.get("party")
        p_meta = PARTY_METADATA.get(party_name, {})
        party_sym = p_meta.get("symbol")
        party_logo = p_meta.get("logo_url") or meta.get("image_url") if meta.get("type") == EntityType.PARTY else p_meta.get("logo_url")

        node = EntityNode(
            id=ent_id,
            name=meta["name"],
            type=meta["type"],
            party=party_name,
            role=meta.get("role"),
            coalition=meta.get("coalition"),
            aliases=meta.get("aliases", []),
            mention_count=1,
            wiki_link=f"[[entities/{ent_id}]]",
            image_url=meta.get("image_url"),
            party_logo_url=party_logo,
            party_symbol=party_sym
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
