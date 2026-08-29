# LLM-Wiki Schema & Guidelines — Thai Politics Intelligence Graph

## Scope
Knowledge base and semantic network graph tracking **Thai Politics** (events, politicians, parties, state agencies, coalitions, legal rulings, and policy debates).

## Core Principles
1. **Divide and Conquer**: Concept and entity pages stay between 400–1,200 words. Split complex topics into subfolders if they exceed this limit.
2. **Mermaid for Diagrams**: All political alliances, actor networks, hierarchy, and conflict flows must use Mermaid charts.
3. **KaTeX for Metrics**: Quantitative metrics (sentiment scores, poll ratings, seat distributions) use KaTeX syntax `$x$`.
4. **Immutable Raw Data**: `raw/` contains unmodified source news articles. Never edit original raw text.
5. **Traceable Audit**: Human corrections and fact-checks are filed in `audit/` and archived in `audit/resolved/`.

## Ontology & Graph Schema

### Entity Types (Nodes)
- `Person`: Politicians, party leaders, ministers, activists, judges, key figures.
- `Party`: Political parties (e.g., Pheu Thai, People's Party / Move Forward, Bhumjaithai, United Thai Nation, Democrat).
- `Institution`: Government bodies, Constitutional Court, Election Commission (ECT), NACC, Senate, Parliament.
- `Event`: Critical political events (e.g., Prime Minister selection, court rulings, no-confidence motions, coalition reshuffles).
- `Policy`: Key legislation or initiatives (e.g., Digital Wallet, constitutional amendment, entertainment complex).

### Relationship Types (Edges)
- `ALLIANCE` / `COALITION`: Government partners, electoral alliances, cross-party voting pacts.
- `OPPOSITION` / `CONFLICT`: Political opposition, debate confrontation, parliamentary battle.
- `CRITICISM` / `ALLEGATION`: Public statements, press attacks, verbal critiques.
- `LEGAL_ACTION` / `INVESTIGATION`: Petitions to ECT, court indictments, Constitutional Court rulings, NACC probes.
- `MEMBER_OF` / `AFFILIATION`: Politician party membership, committee appointments, leadership roles.
- `POLICY_STANCE`: Endorsing, sponsoring, or opposing a policy/bill.

## Directory Structure
```
.
├── CLAUDE.md                ← Knowledge base schema & conventions
├── log/                     ← Daily operational logs (YYYYMMDD.md)
├── audit/                   ← Human feedback & fact-check inbox
│   └── resolved/            ← Processed feedback
├── raw/                     ← Source news articles (markdown)
│   └── articles/
├── wiki/                    ← Compiled knowledge base
│   ├── index.md             ← Master category catalog
│   ├── concepts/            ← Broad topics, policies, coalitions
│   ├── entities/            ← Politicians, parties, institutions
│   └── summaries/           ← Per-article executive summaries
├── data/                    ← graph_data.json and export datasets
├── src/                     ← Python ingestion, extraction, compilation scripts
├── web/                     ← Standalone Interactive Graph Dashboard
└── tests/                   ← Automated unit and integration tests
```

## Operation Commands
- **Ingest News**: `python src/ingest/news_collector.py`
- **Extract Graph**: `python src/extract/extractor.py`
- **Compile Wiki**: `python src/wiki/compiler.py`
- **Lint Wiki & Graph**: `python src/wiki/linter.py`
- **Export GraphML/GEXF**: `python src/export/graphml_exporter.py`
- **Run Web Server**: `python -m http.server 8000 --directory web`
