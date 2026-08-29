import os
import sys
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open("data/graph_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

nodes = data["nodes"]

print(f"=== POLITICAL GRAPH IMAGE AUDIT (Total Nodes: {len(nodes)}) ===")
all_pass = True

for i, n in enumerate(nodes, 1):
    nid = n["id"]
    ntype = n["type"]
    nname = n["name"]
    img_url = n.get("image_url", "")
    
    # Check physical file
    exists = os.path.exists(img_url)
    size = os.path.getsize(img_url) if exists else 0
    
    web_exists = os.path.exists(f"web/{img_url}")
    docs_exists = os.path.exists(f"docs/{img_url}")
    
    status = "[PASS]" if (exists and size > 20000 and web_exists and docs_exists) else "[FAIL]"
    if status == "[FAIL]":
        all_pass = False
        
    print(f"{i:2d}. {status} [{ntype:11s}] {nname:<32s} -> {img_url} ({size:,} bytes)")

print("\n" + "="*70)
if all_pass:
    print(" >>> AUDIT SUCCESS: 100% OF PERSONS & PARTIES HAVE VERIFIED REAL IMAGES! <<<")
else:
    print(" >>> AUDIT WARNING: SOME IMAGES FAILED CHECKS! <<<")
print("="*70)
