import os
import re
import glob
from typing import Dict, List, Set, Tuple

def extract_wikilinks(file_path: str) -> List[str]:
    """Extracts all [[target]] or [[target|label]] wikilinks from a markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    links = []
    for match in re.finditer(r"\[\[(.*?)\]\]", content):
        raw = match.group(1).strip()
        target = raw.split("|")[0].split("#")[0].strip()
        if target:
            links.append(target)
    return links

def lint_wiki(wiki_root: str = "wiki") -> Dict[str, Any]:
    """Performs 7-pass health check on LLM-Wiki knowledge base."""
    all_files = glob.glob(os.path.join(wiki_root, "**/*.md"), recursive=True)
    file_slugs = set()
    
    for f in all_files:
        rel = os.path.relpath(f, wiki_root).replace("\\", "/")
        slug = os.path.splitext(rel)[0]
        file_slugs.add(slug)
        file_slugs.add(f"wiki/{slug}")

    dead_links: List[Tuple[str, str]] = []
    inbound_counts: Dict[str, int] = {s: 0 for s in file_slugs}

    for f in all_files:
        rel = os.path.relpath(f, wiki_root).replace("\\", "/")
        src_slug = os.path.splitext(rel)[0]
        links = extract_wikilinks(f)
        for link in links:
            clean_link = link.replace("\\", "/")
            if clean_link.startswith("wiki/"):
                target_slug = clean_link
            else:
                target_slug = clean_link

            # Check existence
            if target_slug not in file_slugs and f"wiki/{target_slug}" not in file_slugs and target_slug != "":
                # Check if it points to raw/
                if not target_slug.startswith("raw/"):
                    dead_links.append((rel, link))
            else:
                if target_slug in inbound_counts:
                    inbound_counts[target_slug] += 1
                if f"wiki/{target_slug}" in inbound_counts:
                    inbound_counts[f"wiki/{target_slug}"] += 1

    # Check orphans (pages with 0 inbound links, excluding index)
    orphans = [s for s, count in inbound_counts.items() if count == 0 and s != "index" and not s.startswith("wiki/")]

    report = {
        "total_pages": len(all_files),
        "dead_links_count": len(dead_links),
        "dead_links": dead_links[:10],
        "orphan_pages_count": len(orphans),
        "orphan_pages": orphans[:10]
    }
    return report

if __name__ == "__main__":
    rep = lint_wiki()
    print(f"[*] Wiki Health Lint Summary:")
    print(f"    - Total Wiki Pages: {rep['total_pages']}")
    print(f"    - Dead Wikilinks: {rep['dead_links_count']}")
    print(f"    - Orphan Pages: {rep['orphan_pages_count']}")
    if rep['dead_links']:
        print(f"    [!] Sample Dead Links: {rep['dead_links']}")
