#!/usr/bin/env python3
"""
Verify which computed URLs actually exist (HTTP HEAD check).
Then update photos.json with verified URLs.
"""

import json
import urllib.request
import urllib.error
import time
import hashlib
import urllib.parse

def check_url(url, timeout=8):
    """Check if a URL returns 200 OK."""
    try:
        req = urllib.request.Request(url, method='HEAD', headers={
            "User-Agent": "ChinSpotBot/1.0"
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        return False
    except Exception as e:
        return False

def commons_url(filename):
    fname = filename.replace(" ", "_")
    md5 = hashlib.md5(fname.encode('utf-8')).hexdigest()
    a = md5[0]
    ab = md5[0:2]
    encoded = urllib.parse.quote(fname, safe='')
    return f"https://upload.wikimedia.org/wikipedia/commons/{a}/{ab}/{encoded}"

# Load computed URLs
with open("/home/user/workspace/chinspot-map/computed_urls.json") as f:
    computed = json.load(f)

# Load existing photos
with open("/home/user/workspace/chinspot-map/photos.json") as f:
    photos = json.load(f)

print("Verifying URLs...")
verified = {}
failed = []

for item_id, info in computed.items():
    if photos.get(item_id, {}).get("primary"):
        print(f"  [{item_id}] Already have photo - skipping")
        continue
    
    url = info["url"]
    print(f"  [{item_id}] Checking: {url[:70]}...", end=" ")
    ok = check_url(url)
    if ok:
        print("OK")
        verified[item_id] = info
    else:
        print("FAIL")
        failed.append((item_id, info["filename"]))
    time.sleep(0.3)

print(f"\nVerified: {len(verified)}, Failed: {len(failed)}")

# For failed ones, try alternative names
# The key insight is that Wikipedia uses a specific hash structure
# Let's try some alternative filenames for the common ones

ALTERNATIVES = {
    "spot-004": [
        "Momotaro_Jinja_Inuyama.jpg",
        "Momotarou_jinja.jpg",
        "Momotaro-jinja-inuyama.jpg"
    ],
    "spot-005": [
        "Yoro_Park_Kinetik.jpg",
        "Yoro_Koen_kinetic.jpg"
    ],
    "spot-006": [
        "Sekigahara_Warland.jpg",
        "Kankeihara_warland.jpg"
    ],
    "spot-008": [
        "Atami_Hihoukan.jpg"
    ],
    "spot-011": [
        "Tower_of_the_Sun.jpg",
        "TowerOfTheSun.jpg",
        "Expo70_Tower_of_Sun.jpg"
    ],
    "spot-015": [
        "Shigaraki_Tanuki.jpg",
        "Tanuki-Shigaraki.jpg",
        "Shigaraki_raccoon.jpg"
    ],
    "spot-016": [
        "Hana_no_Iwaya_Jinja.jpg",
        "HananokutsuJinja.jpg"
    ],
    "spot-017": [
        "Meoto_Iwa.jpg",
        "MeotoIwa.jpg",
        "FutamiIwa.jpg",
        "Futami-okitama-jinja.jpg"
    ],
    "spot-028": [
        "Tomogashima_Dai3-battery.jpg",
        "Tomogashima_fort.jpg"
    ],
    "spot-029": [
        "Kibune_Jinja.jpg",
        "Kifune_jinja_Kyoto.jpg",
        "Kifune_shrine.jpg"
    ],
    "spot-031": [
        "Ganzan-To.jpg",
        "Head-tower-Nara.jpg",
        "Toto_pyramid_nara.jpg"
    ],
    "spot-032": [
        "Sakafune-ishi.jpg",
        "SakafuneIshi.jpg"
    ],
    "spot-034": [
        "Takeda_Castle.JPG",
        "Takeda_castle.jpg",
        "Takeda_Castle_Ruins.jpg"
    ],
    "spot-040": [
        "Tsubaki_Okami_Yashiro.jpg",
        "Tsubaki-shrine.jpg"
    ],
    "spot-041": [
        "Maruyama-senmaida.jpg",
        "Maruyama_senmaida_terrace.jpg"
    ],
    "spot-043": [
        "Shishi_iwa_Kumano.jpg",
        "Lion_Rock_Kumano.jpg"
    ],
    "spot-046": [
        "Shirakawa-go_village.jpg",
        "Shirakawago.jpg",
        "Shirakawa_village.jpg"
    ],
    "spot-048": [
        "Ryugukutsu.jpg",
        "Ryuugu_cave.jpg"
    ],
    "fest-004": [
        "Konomiya_Hadaka_Matsuri.jpg",
        "Hadaka-matsuri-konomiya.jpg"
    ],
    "fest-006": [
        "Ototo_matsuri.jpg",
        "Kamikura_Jinja_fire.jpg"
    ],
    "fest-009": [
        "Sunakake-matsuri.jpg",
        "Suna_kake_matsuri.jpg"
    ],
    "fest-010": [
        "Tagata_Jinja_Hounen_Matsuri.jpg",
        "HounenMatsuri.jpg"
    ],
    "fest-016": [
        "Yasurai_festival_Kyoto.jpg"
    ],
    "fest-017": [
        "Teshiriki_fire_festival.jpg",
        "Teshiriki_himatsuri.jpg"
    ],
    "fest-018": [
        "Nagahama_Hikiyama_festival.jpg",
        "Nagahama-hikiyama.jpg"
    ],
    "fest-019": [
        "Furukawa_matsuri.jpg",
        "Okoshi-daiko.jpg"
    ],
    "fest-021": [
        "Age_uma_Shinji.jpg",
        "Tado_agema.jpg"
    ],
    "fest-024": [
        "Nachi_Himatsuri.jpg",
        "Nachi_fire_festival.jpg"
    ],
    "fest-027": [
        "Gion_Matsuri_Yamahoko.jpg",
        "Kyoto_Gion_Matsuri.jpg"
    ],
    "fest-028": [
        "Gozanokuribi_Daimonji.jpg",
        "Daimonji_Okuribi.jpg",
        "Gozan_okuribi.jpg"
    ],
    "fest-033": [
        "Uneme_matsuri.jpg",
        "Sarusawa_pond_festival.jpg"
    ],
    "fest-034": [
        "Kurama_fire_festival.jpg",
        "Kurama_himatsuri.jpg"
    ],
    "fest-035": [
        "Nada_kenka_matsuri.jpg",
        "Kenka_matsuri_Himeji.jpg"
    ],
    "fest-037": [
        "Hachiman_festival_Takayama.jpg",
        "Takayama_matsuri_autumn.jpg"
    ],
    "fest-041": [
        "Isonokami_jingu.jpg",
        "Isonokami_shrine.jpg"
    ],
    "fest-044": [
        "Kasugawakamiya_onmatsuri.jpg",
        "Wakamiya_onmatsuri.jpg"
    ],
    "fest-047": [
        "Tado_shrine.jpg",
        "Tado-taisha.jpg"
    ]
}

for item_id, filename in failed:
    alts = ALTERNATIVES.get(item_id, [])
    found = False
    for alt_name in alts:
        alt_url = commons_url(alt_name)
        print(f"  [{item_id}] Alt: {alt_url[:70]}...", end=" ")
        ok = check_url(alt_url)
        if ok:
            print("OK")
            verified[item_id] = {
                "url": alt_url, 
                "credit": computed[item_id]["credit"],
                "filename": alt_name
            }
            found = True
            break
        else:
            print("FAIL")
        time.sleep(0.3)
    if not found:
        print(f"  [{item_id}] ALL alternatives failed")

print(f"\nFinal verified: {len(verified)}")

# Update photos.json
count_updated = 0
for item_id, info in verified.items():
    if not photos.get(item_id, {}).get("primary"):
        photos[item_id]["primary"] = info["url"]
        photos[item_id]["credit"] = info["credit"]
        count_updated += 1

with open("/home/user/workspace/chinspot-map/photos.json", "w", encoding="utf-8") as f:
    json.dump(photos, f, ensure_ascii=False, indent=2)

found_total = sum(1 for v in photos.values() if v.get("primary"))
print(f"Updated {count_updated} entries. Total found: {found_total}/97")

# Print remaining missing
missing = [k for k, v in photos.items() if not v.get("primary")]
print(f"Still missing ({len(missing)}): {missing}")
