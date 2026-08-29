import os
import sys
import urllib.request
import urllib.parse
import json
import shutil
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ENTITIES_TO_FETCH = {
    # Persons
    "paetongtarn_shinawatra": {"wiki": "แพทองธาร ชินวัตร", "type": "avatar"},
    "natthaphong_ruengpanyawut": {"wiki": "ณัฐพงษ์ เรืองปัญญาวุฒิ", "type": "avatar"},
    "anutin_charnvirakul": {"wiki": "อนุทิน ชาญวีรกูล", "type": "avatar"},
    "thaksin_shinawatra": {"wiki": "ทักษิณ ชินวัตร", "type": "avatar"},
    "pirapan_salerathavibhaga": {"wiki": "พีระพันธุ์ สาลีรัฐวิภาค", "type": "avatar"},
    "chalermchai_sri_on": {"wiki": "เฉลิมชัย ศรีอ่อน", "type": "avatar"},
    "prawit_wongsuwan": {"wiki": "ประวิตร วงษ์สุวรรณ", "type": "avatar"},
    "thammanat_prompow": {"wiki": "ธรรมนัส พรหมเผ่า", "type": "avatar"},
    "sirikanya_tansakun": {"wiki": "ศิริกัญญา ตันสกุล", "type": "avatar"},
    "rangsiman_rome": {"wiki": "รังสิมันต์ โรม", "type": "avatar"},
    "parit_wacharasindhu": {"wiki": "พริษฐ์ วัชรสินธุ", "type": "avatar"},
    "raknok_srinork": {"wiki": "รักชนก ศรีนอก", "type": "avatar"},
    "mongkol_surasajja": {"wiki": "มงคล สุระสัจจะ", "type": "avatar"},
    "kriangkrai_srirak": {"wiki": "เกรียงไกร ศรีรักษ์", "type": "avatar"},
    "nanthana_nanthavaropas": {"wiki": "นันทนา นันทวโรภาส", "type": "avatar"},
    "tewarit_maneechay": {"wiki": "เทวฤทธิ์ มณีฉาย", "type": "avatar"},
    "boonsong_noisophon": {"wiki": "บุญส่ง น้อยโสภณ", "type": "avatar"},
    "itthiporn_boonpracong": {"wiki": "อิทธิพร บุญประคอง", "type": "avatar"},
    "sawaeng_boonmee": {"wiki": "แสวง บุญมี", "type": "avatar"},
    "somchai_sawangkarn": {"wiki": "สมชาย แสวงการ", "type": "avatar"},
    "yingcheep_atchanont": {"wiki": "ยิ่งชีพ อัชฌานนท์", "type": "avatar"},

    # Parties & Institutions
    "pheu_thai_party": {"wiki": "พรรคเพื่อไทย", "type": "logo"},
    "peoples_party": {"wiki": "พรรคประชาชน (พ.ศ. 2567)", "type": "logo", "alt_wiki": "พรรคประชาชน"},
    "bhumjaithai_party": {"wiki": "พรรคภูมิใจไทย", "type": "logo"},
    "united_thai_nation_party": {"wiki": "พรรครวมไทยสร้างชาติ", "type": "logo"},
    "democrat_party": {"wiki": "พรรคประชาธิปัตย์", "type": "logo"},
    "palang_pracharath_party": {"wiki": "พรรคพลังประชารัฐ", "type": "logo"},
    "constitutional_court": {"wiki": "ศาลรัฐธรรมนูญ (ประเทศไทย)", "type": "logo"},
    "election_commission": {"wiki": "คณะกรรมการการเลือกตั้ง (ประเทศไทย)", "type": "logo"},
    "senate_thailand": {"wiki": "วุฒิสภาไทย", "type": "logo"}
}

USER_AGENT = "PoliticalIntelligenceApp/2.0 (https://github.com/KanoonGammy/Political; admin@kanoongammy.com)"

def get_wiki_image_url(title):
    encoded_title = urllib.parse.quote(title)
    api_url = f"https://th.wikipedia.org/w/api.php?action=query&titles={encoded_title}&prop=pageimages&format=json&pithumbsize=600"
    
    req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get("query", {}).get("pages", {})
            for pid, page in pages.items():
                if "thumbnail" in page:
                    return page["thumbnail"]["source"]
    except Exception as e:
        print(f"[ERR] Querying Wikipedia API for '{title}': {e}")
    return None

def download_file(url, target_path):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            with open(target_path, "wb") as f:
                f.write(content)
        return len(content)
    except Exception as e:
        print(f"[ERR] Downloading from {url}: {e}")
        return 0

def main():
    os.makedirs("images/avatars", exist_ok=True)
    os.makedirs("images/logos", exist_ok=True)
    os.makedirs("web/images/avatars", exist_ok=True)
    os.makedirs("web/images/logos", exist_ok=True)
    os.makedirs("docs/images/avatars", exist_ok=True)
    os.makedirs("docs/images/logos", exist_ok=True)

    results = {}
    for ent_id, meta in ENTITIES_TO_FETCH.items():
        subfolder = "avatars" if meta["type"] == "avatar" else "logos"
        target_path = f"images/{subfolder}/{ent_id}.jpg"
        
        print(f"[*] Fetching real photo/logo for: {meta['wiki']} ({ent_id})...")
        img_url = get_wiki_image_url(meta["wiki"])
        if not img_url and "alt_wiki" in meta:
            img_url = get_wiki_image_url(meta["alt_wiki"])
            
        if img_url:
            bytes_downloaded = download_file(img_url, target_path)
            if bytes_downloaded > 2000:
                print(f"  [OK] Saved -> {target_path} ({bytes_downloaded:,} bytes)")
                shutil.copy(target_path, f"web/{target_path}")
                shutil.copy(target_path, f"docs/{target_path}")
                results[ent_id] = target_path
            else:
                print(f"  [WARN] Downloaded size too small: {bytes_downloaded} bytes")
        else:
            print(f"  [WARN] No Wikipedia thumbnail found for '{meta['wiki']}'")
        time.sleep(0.3)

    print(f"\n===========================================================")
    print(f" [*] Successfully fetched and stored: {len(results)}/{len(ENTITIES_TO_FETCH)} real photos/logos locally!")
    print(f"===========================================================")

if __name__ == "__main__":
    main()
