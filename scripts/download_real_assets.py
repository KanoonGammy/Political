import os
import urllib.request
import json
import shutil

ASSET_MAP = {
    # Person Portraits (Real High-Res Photos)
    "paetongtarn_shinawatra": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Paetongtarn_Shinawatra_2024.jpg/500px-Paetongtarn_Shinawatra_2024.jpg"
    },
    "natthaphong_ruengpanyawut": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Natthaphong_Ruengpanyawut_2024.jpg/500px-Natthaphong_Ruengpanyawut_2024.jpg"
    },
    "anutin_charnvirakul": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Anutin_Charnvirakul_in_2023.jpg/500px-Anutin_Charnvirakul_in_2023.jpg"
    },
    "thaksin_shinawatra": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Thaksin_Shinawatra_2003_%28cropped%29.jpg/500px-Thaksin_Shinawatra_2003_%28cropped%29.jpg"
    },
    "pirapan_salerathavibhaga": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Pirapan_Salirathavibhaga_2023.jpg/500px-Pirapan_Salirathavibhaga_2023.jpg"
    },
    "chalermchai_sri_on": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Chalermchai_Sri-on_in_2023.jpg/500px-Chalermchai_Sri-on_in_2023.jpg"
    },
    "prawit_wongsuwan": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Prawit_Wongsuwan_2019.jpg/500px-Prawit_Wongsuwan_2019.jpg"
    },
    "thammanat_prompow": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Thammanat_Prompow_2023.jpg/500px-Thammanat_Prompow_2023.jpg"
    },
    "sirikanya_tansakun": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Sirikanya_Tansakun_2023.jpg/500px-Sirikanya_Tansakun_2023.jpg"
    },
    "rangsiman_rome": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Rangsiman_Rome_2023.jpg/500px-Rangsiman_Rome_2023.jpg"
    },
    "parit_wacharasindhu": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Parit_Wacharasindhu_2023.jpg/500px-Parit_Wacharasindhu_2023.jpg"
    },
    "raknok_srinork": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Rukchanok_Srinork_2023.jpg/500px-Rukchanok_Srinork_2023.jpg"
    },
    "mongkol_surasajja": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mongkol_Surasajja_%28cropped%29.jpg/500px-Mongkol_Surasajja_%28cropped%29.jpg"
    },
    "kriangkrai_srirak": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Kriangkrai_Srirak.jpg/500px-Kriangkrai_Srirak.jpg"
    },
    "nanthana_nanthavaropas": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Nanthana_Nanthavaropas.jpg/500px-Nanthana_Nanthavaropas.jpg"
    },
    "itthiporn_boonpracong": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Itthiporn_Boonpracong.jpg/500px-Itthiporn_Boonpracong.jpg"
    },
    "yingcheep_atchanont": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Yingcheep_Atchanont.jpg/500px-Yingcheep_Atchanont.jpg"
    },
    "tewarit_maneechay": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Emblem_of_the_Senate_of_Thailand.svg/500px-Emblem_of_the_Senate_of_Thailand.svg.png"
    },
    "boonsong_noisophon": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Emblem_of_the_Senate_of_Thailand.svg/500px-Emblem_of_the_Senate_of_Thailand.svg.png"
    },
    "sawaeng_boonmee": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Seal_of_the_Election_Commission_of_Thailand.svg/500px-Seal_of_the_Election_Commission_of_Thailand.svg.png"
    },
    "somchai_sawangkarn": {
        "type": "avatar",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Emblem_of_the_Senate_of_Thailand.svg/500px-Emblem_of_the_Senate_of_Thailand.svg.png"
    },

    # Party Logos & Institution Seals (Official Emblems)
    "pheu_thai_party": {
        "type": "logo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Pheu_Thai_Party_logo.svg/500px-Pheu_Thai_Party_logo.svg.png"
    },
    "peoples_party": {
        "type": "logo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Peoples_Party_%28Thailand%29_logo.svg/500px-Peoples_Party_%28Thailand%29_logo.svg.png"
    },
    "bhumjaithai_party": {
        "type": "logo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Bhumjaithai_Party_logo.svg/500px-Bhumjaithai_Party_logo.svg.png"
    },
    "united_thai_nation_party": {
        "type": "logo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/United_Thai_Nation_Party_logo.svg/500px-United_Thai_Nation_Party_logo.svg.png"
    },
    "democrat_party": {
        "type": "logo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Democrat_Party_%28Thailand%29_logo.svg/500px-Democrat_Party_%28Thailand%29_logo.svg.png"
    },
    "palang_pracharath_party": {
        "type": "logo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Palang_Pracharath_Party_logo.svg/500px-Palang_Pracharath_Party_logo.svg.png"
    },
    "constitutional_court": {
        "type": "logo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Emblem_of_the_Constitutional_Court_of_Thailand.svg/500px-Emblem_of_the_Constitutional_Court_of_Thailand.svg.png"
    },
    "election_commission": {
        "type": "logo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Seal_of_the_Election_Commission_of_Thailand.svg/500px-Seal_of_the_Election_Commission_of_Thailand.svg.png"
    },
    "senate_thailand": {
        "type": "logo",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Emblem_of_the_Senate_of_Thailand.svg/500px-Emblem_of_the_Senate_of_Thailand.svg.png"
    }
}

def download_asset(name, info):
    subfolder = "avatars" if info["type"] == "avatar" else "logos"
    ext = "png" if "png" in info["url"] or "svg" in info["url"] else "jpg"
    target_rel = f"images/{subfolder}/{name}.{ext}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 (PoliticalGraphBot/1.0)"
    }
    
    try:
        req = urllib.request.Request(info["url"], headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
            with open(target_rel, "wb") as f:
                f.write(content)
        print(f"[OK] Downloaded {name} -> {target_rel} ({len(content)} bytes)")
        
        # Mirror to web/ and docs/
        shutil.copy(target_rel, f"web/{target_rel}")
        shutil.copy(target_rel, f"docs/{target_rel}")
        return target_rel
    except Exception as e:
        print(f"[ERR] Failed to download {name} from {info['url']}: {e}")
        return None

def main():
    os.makedirs("images/avatars", exist_ok=True)
    os.makedirs("images/logos", exist_ok=True)
    os.makedirs("web/images/avatars", exist_ok=True)
    os.makedirs("web/images/logos", exist_ok=True)
    os.makedirs("docs/images/avatars", exist_ok=True)
    os.makedirs("docs/images/logos", exist_ok=True)
    
    results = {}
    for name, info in ASSET_MAP.items():
        path = download_asset(name, info)
        if path:
            results[name] = path
            
    print(f"\n[DONE] Successfully downloaded {len(results)}/{len(ASSET_MAP)} real assets.")

if __name__ == "__main__":
    main()
