# 04: Standalone Interactive Political Graph Network Web Dashboard

**What to build:**
A modern, standalone interactive web dashboard in `web/` using HTML5, CSS (glassmorphism / dark theme), and Vis.js Network. Features interactive force-directed physics, node clustering by political coalition/party, edge color-coding by relation type (green = alliance/support, red = conflict/legal challenge, orange = criticism/debate, blue = institutional action), dynamic 30-day timeline slider, actor search/autocomplete, and an interactive slide-over inspector displaying actor dossiers, connected relationships, citation quotes, and links to LLM-Wiki summaries.

**Blocked by:** 03: LLM Entity & Semantic Relation Extraction Engine

**Status:** done

- [x] Interactive Canvas using Vis.js network visualization with smooth physics and zoom/pan
- [x] Party / Coalition legend & color-coding (Pheu Thai, People's Party / Move Forward, Bhumjaithai, UTN, Democrats, Independent Organs, etc.)
- [x] Relationship type filtering (Alliance, Conflict, Affiliation, Investigation)
- [x] 30-Day date range slider to observe political shifts over time
- [x] Search box with autocomplete for quick actor jumping
- [x] Evidence Drawer showing news excerpts and links for selected nodes/edges
- [x] Fully functional standalone mode (loads `data/graph_data.json` or embedded fallback)
