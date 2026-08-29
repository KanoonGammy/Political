import os
import sys
import urllib.request
import re
import shutil

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

URLS = [
    ('tewarit_maneechay', 'https://thematter.co/social/tewarit-maneechay-senator/228789'),
    ('itthiporn_boonpracong', 'https://www.thaipbs.or.th/news/content/340801'),
    ('itthiporn_boonpracong', 'https://www.thaipbs.or.th/news/content/327772'),
    ('itthiporn_boonpracong', 'https://www.thairath.co.th/news/politic/2708304')
]

for name, u in URLS:
    try:
        req = urllib.request.Request(u, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        m = re.search(r'<meta\s+(?:property|name)=[\"\']og:image[\"\']\s+content=[\"\']([^\"\']+)[\"\']', html, re.I)
        if not m:
            m = re.search(r'<meta\s+content=[\"\']([^\"\']+)[\"\']\s+(?:property|name)=[\"\']og:image[\"\']', html, re.I)
        if m:
            img = m.group(1).strip()
            print(f"Found {name} -> {img[:70]}")
            req_img = urllib.request.Request(img, headers=HEADERS)
            content = urllib.request.urlopen(req_img, timeout=15).read()
            if len(content) > 5000:
                dest = f"images/avatars/{name}.jpg"
                with open(dest, "wb") as f:
                    f.write(content)
                shutil.copy(dest, f"web/{dest}")
                shutil.copy(dest, f"docs/{dest}")
                print(f"[OK] Saved {dest} ({len(content):,} bytes) from {u}")
    except Exception as e:
        print(f"Err {name} from {u}: {e}")
