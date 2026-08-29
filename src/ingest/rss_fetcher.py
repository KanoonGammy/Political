from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
import re
import urllib.parse
import feedparser
from bs4 import BeautifulSoup
import requests
from dateutil import parser as date_parser

@dataclass
class RawArticle:
    title: str
    url: str
    published_at: datetime
    source: str
    summary: str
    content: str
    category: str = "politics"
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)

RSS_FEEDS = {
    "ThaiPBS Politics": "https://www.thaipbs.or.th/rss/news/politics",
    "Matichon Politics": "https://www.matichon.co.th/politics/feed",
    "The Standard": "https://thestandard.co/feed/",
    "Prachatai Politics": "https://prachatai.com/journal/rss.xml",
    "BBC News Thai": "https://feeds.bbci.co.uk/thai/rss.xml",
    "Google News Thai Politics": "https://news.google.com/rss/search?q=%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%87%E0%B9%84%E0%B8%97%E0%B8%A2+when:30d&hl=th&gl=TH&ceid=TH:th",
    "Google News Pheu Thai": "https://news.google.com/rss/search?q=%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B9%80%E0%B8%9E%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B9%8Parse+when:30d&hl=th&gl=TH&ceid=TH:th",
    "Google News Peoples Party": "https://news.google.com/rss/search?q=%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%8A%E0%B8%B2%E0%B8%8A%E0%B8%99+when:30d&hl=th&gl=TH&ceid=TH:th"
}

def clean_article_content(raw_html: str) -> str:
    """Removes script, style, and HTML tags, returning normalized clean text."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    for s in soup(["script", "style", "nav", "header", "footer", "aside"]):
        s.extract()
    text = soup.get_text(separator="\n")
    # Clean excessive whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n\n".join(lines)

def parse_published_date(entry: Dict[str, Any]) -> datetime:
    """Parses various RSS date formats into UTC datetime."""
    now = datetime.now(timezone.utc)
    for field_name in ("published", "pubDate", "updated", "created"):
        if field_name in entry and entry[field_name]:
            try:
                dt = date_parser.parse(entry[field_name])
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                else:
                    dt = dt.astimezone(timezone.utc)
                return dt
            except Exception:
                pass
    if "published_parsed" in entry and entry["published_parsed"]:
        try:
            return datetime(*entry["published_parsed"][:6], tzinfo=timezone.utc)
        except Exception:
            pass
    return now

def filter_articles_by_date(articles: List[RawArticle], days: int = 30) -> List[RawArticle]:
    """Filters articles published within the last N days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return [a for a in articles if a.published_at >= cutoff]

def deduplicate_articles(articles: List[RawArticle]) -> List[RawArticle]:
    """Deduplicates articles based on normalized title and URL."""
    seen_titles = set()
    seen_urls = set()
    unique = []

    for article in articles:
        norm_title = re.sub(r"\s+", " ", article.title.strip().lower())
        norm_url = article.url.split("?")[0].strip()

        if norm_title in seen_titles or norm_url in seen_urls:
            continue

        seen_titles.add(norm_title)
        seen_urls.add(norm_url)
        unique.append(article)

    return unique

def fetch_feed_articles(source_name: str, feed_url: str, timeout: int = 10) -> List[RawArticle]:
    """Fetches and parses articles from a single RSS feed."""
    articles = []
    try:
        resp = requests.get(feed_url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        if resp.status_code != 200:
            return []
        feed = feedparser.parse(resp.content)
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            url = entry.get("link", "").strip()
            if not title or not url:
                continue
            
            pub_date = parse_published_date(entry)
            raw_summary = entry.get("summary", "") or entry.get("description", "")
            summary = clean_article_content(raw_summary)
            
            # Content if available in full RSS
            content = summary
            if "content" in entry and isinstance(entry["content"], list) and len(entry["content"]) > 0:
                content = clean_article_content(entry["content"][0].get("value", ""))

            articles.append(RawArticle(
                title=title,
                url=url,
                published_at=pub_date,
                source=source_name,
                summary=summary,
                content=content or summary
            ))
    except Exception as e:
        print(f"[Warn] Failed fetching {source_name} ({feed_url}): {e}")
    return articles
