# 05: Wiki Graph Synchronizer, Health Linter & Export Tools

**What to build:**
A synchronization and health monitoring toolkit for the LLM-Wiki. Compiles graph data into individual Markdown pages in `wiki/entities/<slug>.md` and `wiki/concepts/<slug>.md` embedded with Mermaid diagrams for local Obsidian viewing. Implements a 7-pass wiki health linter (`src/wiki/linter.py`) that checks dead wikilinks, orphan nodes, and index consistency. Generates Gephi (GEXF) and GraphML exports for advanced external network analysis.

**Blocked by:** 04: Standalone Interactive Political Graph Network Web Dashboard

**Status:** done

- [x] Wiki Compiler generating formatted `wiki/entities/` and `wiki/concepts/` with Mermaid charts
- [x] Auto-regeneration of `wiki/index.md` categorized hierarchy
- [x] 7-pass Wiki Health Linter script (`src/wiki/linter.py`)
- [x] Export utility to GEXF and GraphML formats (`src/export/graphml_exporter.py`)
- [x] Verification tests ensuring clean linting and valid export formats
