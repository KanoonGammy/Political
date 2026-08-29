# 03: LLM Entity & Semantic Relation Extraction Engine

**What to build:**
Entity and relationship extraction pipeline that processes news articles in `raw/articles/`, extracts political actors (politicians, political parties, ministries, judicial bodies, civil groups) and semantic relations (coalition/alliance, conflict/lawsuit, political attack, policy stance, defection, investigation) with directional links, sentiment/valence score, timestamp, and citation quotes. Outputs graph dataset to `data/graph_data.json` and populates `wiki/entities/`.

**Blocked by:** 02: 30-Day Thai Political News Ingestion Pipeline

**Status:** done

- [x] Pydantic/dataclass schema for Entity (Node), Relation (Edge), and Graph
- [x] Political entity dictionary & regex/LLM prompt templates
- [x] Relation extraction with evidence snippet, source URL, date, and sentiment
- [x] Graph aggregation and deduplication exporting to `data/graph_data.json`
- [x] Unit tests for graph schema validation and relation extraction logic
