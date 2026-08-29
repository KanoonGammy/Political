# 02: 30-Day Thai Political News Ingestion Pipeline

**What to build:**
Automated news crawler, RSS aggregator, and parser that collects Thai political news over the past 30 days from multi-source RSS feeds (ThaiPBS, Matichon, Thairath, The Standard, Prachatai, BBC Thai, Google News) and search queries. Cleans HTML, extracts metadata (date, outlet, author, URL, title), deduplicates articles, and saves them into `raw/articles/<slug>.md` along with initial summaries in `wiki/summaries/<slug>.md` and logging in `log/`.

**Blocked by:** 01: Scaffold LLM-Wiki Knowledge Base & Project Core Structure

**Status:** done

- [x] RSS fetcher supporting multiple Thai news outlets with 30-day date cutoff
- [x] News parser that cleans HTML content into structured markdown
- [x] Deduplication based on title similarity and URL hashing
- [x] Storage in `raw/articles/<slug>.md` with frontmatter metadata
- [x] Automated generation of initial concise summaries in `wiki/summaries/<slug>.md`
- [x] Unit tests for RSS parsing and date filtering
