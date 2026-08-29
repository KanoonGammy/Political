import os
import sys
import urllib.request
import re
import shutil

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
urls = [
    'https://www.thaipbs.or.th/news/content/345511',
    'https://www.thaipbs.or.th/news/content/342137',
    'https://www.thaipbs.or.th/news/content/342125',
    'https://www.thaipbs.or.th/news/content/341492'
]

for u in urls:
    try:
        html = urllib.request.urlopen(urllib.request.Request(u, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
        m = re.search(r'<meta\s+(?:property|name)=[\"\']og:image[\"\']\s+content=[\"\']([^\"\']+)[\"\']', html, re.I)
        if m:
            img_url = m.group(1)
            print(f"Found candidate: {img_url}")
            content = urllib.request.urlopen(urllib.request.Request(img_url, headers=headers), timeout=15).read()
            if len(content) > 5000:
                dest = "images/avatars/tewarit_maneechay.jpg"
                with open(dest, "wb") as f:
                    f.write(content)
                shutil.copy(dest, f"web/{dest}")
                shutil.copy(dest, f"docs/{dest}")
                print(f"[OK] Saved {dest} ({len(content):,} bytes) from {u}")
                break
    except Exception as e:
        print(f"Err {u}: {e}")
