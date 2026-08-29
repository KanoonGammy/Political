import os
import sys
import urllib.request
import urllib.parse
import re
import shutil

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

TARGETS = {
    "sawaeng_boonmee": [
        "https://thestandard.co/sawaeng-boonmee-profile/",
        "https://thestandard.co/sawaeng-boonmee-profile-ec-secretary-general/",
        "https://news.ch7.com/detail/555891",
        "https://www.thaipbs.or.th/news/content/313386"
    ],
    "itthiporn_boonpracong": [
        "https://thestandard.co/itthiporn-boonpracong/",
        "https://thestandard.co/itthiporn-boonpracong-profile/",
        "https://www.thaipbs.or.th/news/content/273766"
    ],
    "boonsong_noisophon": [
        "https://www.thaipbs.or.th/news/content/342371",
        "https://thestandard.co/boonsong-noisophon-profile/",
        "https://www.thairath.co.th/news/politic/2803130"
    ],
    "tewarit_maneechay": [
        "https://thestandard.co/the-movement-of-tewarit-maneechay/",
        "https://prachatai.com/journal/2024/07/110058",
        "https://thematter.co/social/tewarit-maneechay-senator/228789"
    ],
    "yingcheep_atchanont": [
        "https://thestandard.co/yingcheep-atchanont-ilaw/",
        "https://thematter.co/brief/183204/183204",
        "https://prachatai.com/journal/2023/07/104924"
    ]
}

def extract_og_image(article_url):
    try:
        req = urllib.request.Request(article_url, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        m = re.search(r'<meta\s+(?:property|name)=[\"\']og:image[\"\']\s+content=[\"\']([^\"\']+)[\"\']', html, re.I)
        if not m:
            m = re.search(r'<meta\s+content=[\"\']([^\"\']+)[\"\']\s+(?:property|name)=[\"\']og:image[\"\']', html, re.I)
        if m:
            return m.group(1).strip()
    except Exception as e:
        # print(f"  [err] {article_url}: {e}")
        pass
    return None

def download_and_save(img_url, target_path):
    try:
        req = urllib.request.Request(img_url, headers=HEADERS)
        content = urllib.request.urlopen(req, timeout=15).read()
        if len(content) > 3000:
            with open(target_path, "wb") as f:
                f.write(content)
            return len(content)
    except Exception as e:
        print(f"  [download err] {img_url}: {e}")
    return 0

def main():
    for name, urls in TARGETS.items():
        target = f"images/avatars/{name}.jpg"
        print(f"[*] Searching real face photo for: {name}...")
        found = False
        for u in urls:
            og_img = extract_og_image(u)
            if og_img:
                print(f"  -> Found image candidate: {og_img[:80]}...")
                size = download_and_save(og_img, target)
                if size > 0:
                    print(f"  [SUCCESS] Saved {target} ({size:,} bytes) from {u}")
                    shutil.copy(target, f"web/{target}")
                    shutil.copy(target, f"docs/{target}")
                    found = True
                    break
        if not found:
            print(f"  [FAILED] Could not find photo for {name}")

if __name__ == "__main__":
    main()
