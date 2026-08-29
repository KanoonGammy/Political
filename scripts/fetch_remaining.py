import os
import sys
import urllib.request
import urllib.parse
import json
import shutil

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

USER_AGENT = "PoliticalIntelligenceApp/2.0 (contact@kanoongammy.com)"

REMAINING = {
    "kriangkrai_srirak": ("en", "Kriangkrai Srirak", "avatars"),
    "itthiporn_boonpracong": ("en", "Itthiporn Boonpracong", "avatars"),
    "bhumjaithai_party": ("en", "Bhumjaithai Party", "logos"),
    "democrat_party": ("en", "Democrat Party (Thailand)", "logos"),
    "yingcheep_atchanont": ("th", "ยิ่งชีพ อัชฌานนท์", "avatars"),
    "tewarit_maneechay": ("th", "เทวฤทธิ์ มณีฉาย", "avatars"),
    "boonsong_noisophon": ("th", "บุญส่ง น้อยโสภณ", "avatars"),
    "sawaeng_boonmee": ("th", "แสวง บุญมี", "avatars"),
}

def fetch_wiki_image(lang, title):
    encoded = urllib.parse.quote(title)
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&titles={encoded}&prop=pageimages&format=json&pithumbsize=600"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            pages = data.get("query", {}).get("pages", {})
            for pid, p in pages.items():
                if "thumbnail" in p:
                    return p["thumbnail"]["source"]
    except Exception as e:
        print(f"[ERR] Query {title}: {e}")
    return None

def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read()
            with open(path, "wb") as f:
                f.write(content)
        return len(content)
    except Exception as e:
        print(f"[ERR] Download: {e}")
        return 0

def main():
    for ent_id, (lang, title, subfolder) in REMAINING.items():
        path = f"images/{subfolder}/{ent_id}.jpg"
        print(f"[*] Querying {lang}:{title} for {ent_id}...")
        img_url = fetch_wiki_image(lang, title)
        if img_url:
            size = download(img_url, path)
            print(f"  [OK] Saved {path} ({size:,} bytes)")
            shutil.copy(path, f"web/{path}")
            shutil.copy(path, f"docs/{path}")
        else:
            print(f"  [MISS] No thumbnail found for {title}")

if __name__ == "__main__":
    main()
