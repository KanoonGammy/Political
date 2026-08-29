import pytest
from datetime import datetime, timezone, timedelta
from src.ingest.rss_fetcher import filter_articles_by_date, clean_article_content, deduplicate_articles, RawArticle

def test_filter_articles_by_date():
    now = datetime.now(timezone.utc)
    recent_date = now - timedelta(days=5)
    old_date = now - timedelta(days=45)
    future_date = now + timedelta(days=1)

    articles = [
        RawArticle(title="News 1", url="https://example.com/1", published_at=recent_date, source="ThaiPBS", summary="Text 1", content="Full text 1"),
        RawArticle(title="News 2", url="https://example.com/2", published_at=old_date, source="Matichon", summary="Text 2", content="Full text 2"),
        RawArticle(title="News 3", url="https://example.com/3", published_at=future_date, source="Thairath", summary="Text 3", content="Full text 3"),
    ]

    filtered = filter_articles_by_date(articles, days=30)
    assert len(filtered) == 2
    assert filtered[0].title == "News 1"
    assert filtered[1].title == "News 3"

def test_clean_article_content():
    raw_html = "<p>นายกรัฐมนตรีแถลงข่าว <b>นโยบายแจกเงิน 10,000 บาท</b></p><script>alert(1)</script><style>.cls{}</style>"
    cleaned = clean_article_content(raw_html)
    assert "นายกรัฐมนตรีแถลงข่าว" in cleaned
    assert "alert(1)" not in cleaned
    assert "<p>" not in cleaned

def test_deduplicate_articles():
    now = datetime.now(timezone.utc)
    articles = [
        RawArticle(title="ศาลรัฐธรรมนูญวินิจฉัยคดียุบพรรค", url="https://example.com/1", published_at=now, source="ThaiPBS", summary="1", content="1"),
        RawArticle(title="ศาลรัฐธรรมนูญวินิจฉัยคดียุบพรรค", url="https://example.com/2", published_at=now, source="Matichon", summary="2", content="2"),
        RawArticle(title="พรรคเพื่อไทยประชุมกรรมการบริหาร", url="https://example.com/3", published_at=now, source="Thairath", summary="3", content="3"),
    ]

    deduped = deduplicate_articles(articles)
    assert len(deduped) == 2
    titles = [a.title for a in deduped]
    assert "พรรคเพื่อไทยประชุมกรรมการบริหาร" in titles
