# 🌐 Thai Politics Semantic Graph & LLM-Wiki Knowledge Base

ระบบรวบรวมข่าวการเมืองไทยย้อนหลัง 30 วัน สกัดโครงข่ายความสัมพันธ์เชิงความหมาย (Semantic Relations Model) และแสดงผลผ่าน Interactive Force-Directed Web Dashboard พร้อมระบบฐานความรู้ Obsidian-compatible LLM-Wiki

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-8%2F8%20passed-success.svg)

---

## 🌟 ฟีเจอร์หลัก (Key Features)

1. **30-Day News Ingestion Engine (`src/ingest/`):**
   - รวบรวมและกลั่นกรองข่าวการเมืองไทยจาก RSS Feeds สำนักข่าวหลัก (ThaiPBS, Matichon, The Standard, BBC Thai, Google News ฯลฯ)
   - จัดเก็บข่าวต้นฉบับลง `raw/articles/` พร้อมสรุปประเด็นย่อลง `wiki/summaries/`

2. **Semantic Relation Extraction Pipeline (`src/extract/`):**
   - สกัดตัวละครทางการเมือง (นักการเมือง, พรรค, สถาบันตุลาการ, องค์กรอิสระ, นโยบาย)
   - ระบุความสัมพันธ์ชัดเจน (`ALLIANCE`, `OPPOSITION`, `CRITICISM`, `LEGAL_ACTION`, `MEMBER_OF`, `POLICY_STANCE`)
   - คำนวณ Sentiment score, วันที่ และข้อความอ้างอิงจากเนื้อข่าว (Evidence Quote)

3. **Interactive Graph Dashboard (`web/`):**
   - แดชบอร์ด Vis.js Network ธีม Dark Modern Glassmorphism
   - **Party & Coalition Filter:** สลับดูขั้วรัฐบาล, ฝ่ายค้าน, หรือองค์กรอิสระ
   - **Relation Type Filter:** คัดกรองตามประเภทความสัมพันธ์ (พันธมิตร vs ขัดแย้ง vs คดีความ)
   - **30-Day Timeline Scrubber:** เลื่อนดูการเปลี่ยนแปลงทางการเมืองย้อนหลัง
   - **Real-time Search:** ค้นหาชื่อหรือตำแหน่ง พร้อม Zoom Focus อัตโนมัติ
   - **Evidence Drawer:** แถบสไลด์ดูข้อมูลเจาะลึก สถิติ และหลักฐานข่าวอ้างอิง

4. **LLM-Wiki Knowledge Base (`wiki/`):**
   - คอมไพล์บทความวิกิ 256 หน้า พร้อม Mermaid Diagrams ในตัว
   - ผ่านการตรวจสุขภาพ 7-Pass Linter (0 Dead Links, 0 Orphans)
   - รองรับการเปิดใช้งานเป็น Obsidian Vault ทันที

5. **Data Exporters (`src/export/`):**
   - Export โครงข่ายในรูปแบบ GraphML (`data/political_graph.graphml`) และ Gephi GEXF (`data/political_graph.gexf`)

---

## 🚀 การติดตั้งและรันใช้งาน (Quick Start)

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. รัน Dashboard (Port 17325)
```bash
python server.py
```
หรือรันผ่าน Python built-in server:
```bash
python -m http.server 17325 --directory web
```
เข้าชมได้ที่: **`http://localhost:17325`**

---

## 🔄 การอัปเดตข้อมูลข่าวและโครงข่าย (Pipeline Execution)

```bash
# 1. ดึงข่าวการเมือง 30 วันล่าสุด
python -m src.ingest.news_collector

# 2. สกัดโครงข่ายความสัมพันธ์
python -m src.extract.extractor

# 3. คอมไพล์เอกสาร LLM-Wiki
python -m src.wiki.compiler

# 4. ตรวจสอบความถูกต้องของระบบวิกิ (Health Linter)
python -m src.wiki.linter

# 5. Export ไฟล์สำหรับ Gephi / NetworkX
python -m src.export.graphml_exporter
```

---

## 🧪 การทดสอบระบบ (Automated Tests)

```bash
python -m pytest tests/
```

---

## 📂 โครงสร้างโปรเจกต์ (Directory Structure)

```
.
├── CLAUDE.md                # สกีมาและคู่มือมาตรฐาน LLM-Wiki
├── server.py                # เซิร์ฟเวอร์สำหรับรัน Dashboard (Port 17325)
├── requirements.txt         # รายการ Python dependencies
├── raw/                     # ไฟล์ข่าวต้นฉบับ (Immutable Raw Articles)
│   └── articles/
├── wiki/                    # ฐานความรู้ LLM-Wiki
│   ├── index.md             # สารบัญใหญ่ (Master Catalog)
│   ├── entities/            # หน้าบทความตัวละคร/พรรค/องค์กร (พร้อม Mermaid)
│   ├── concepts/            # หน้าบทความประเด็นนโยบาย/ขั้วการเมือง
│   └── summaries/           # บทสรุปข่าวรายชิ้น
├── data/                    # ชุดข้อมูล Graph JSON, GraphML และ GEXF
├── web/                     # ไฟล์เว็บแดชบอร์ด (HTML5/CSS3/Vis.js)
├── src/                     # ซอร์สโค้ดระบบ
│   ├── ingest/              # ระบบดึงและจัดการข่าว RSS
│   ├── extract/             # เอนจินสกัด Entity & Semantic Relations
│   ├── wiki/                # ระบบคอมไพล์และตรวจสอบสุขภาพ Wiki
│   └── export/              # ระบบส่งออก GraphML/GEXF
└── tests/                   # Automated Unit Tests
```

---

## 🌐 การเผยแพร่ขึ้น GitHub และ GitHub Pages

### อัปโหลดขึ้น GitHub Repository:
```bash
git init -b main
git add .
git commit -m "feat: Thai Politics Semantic Graph & LLM-Wiki Knowledge Base"
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
git push -u origin main
```

### เปิดใช้งาน GitHub Pages:
1. ไปที่แท็บ **Settings** > **Pages** ใน GitHub Repository
2. ในส่วน **Build and deployment** เลือก **Deploy from a branch**
3. เลือก Branch `main` และโฟลเดอร์ `/web` (หรือ `/ (root)`) แล้วกด **Save**
