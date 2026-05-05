#!/usr/bin/env python3
"""
Compute Wikimedia Commons image URLs from filenames.
Standard URL formula: https://upload.wikimedia.org/wikipedia/commons/[a]/[ab]/filename.ext
where [a] and [ab] are the first 1 and 2 chars of the MD5 hash of the filename.
"""

import hashlib
import urllib.parse
import json
import os

def commons_url(filename):
    """Compute the direct URL for a Wikimedia Commons file."""
    # Normalize: replace spaces with underscores
    fname = filename.replace(" ", "_")
    # Compute MD5 hash
    md5 = hashlib.md5(fname.encode('utf-8')).hexdigest()
    a = md5[0]
    ab = md5[0:2]
    # URL-encode the filename for the path
    encoded = urllib.parse.quote(fname, safe='')
    return f"https://upload.wikimedia.org/wikipedia/commons/{a}/{ab}/{encoded}"

# Known Commons filenames for our items
# These filenames were found from search results / category pages
KNOWN_FILES = {
    "spot-004": ("Momotaro_Shrine,_Inuyama_in_autumn.jpg", "Mailer Diablo", "CC BY-SA 3.0"),
    "spot-005": ("Yoro_Kinetic_Experience_Museum.jpg", "Leimenide", "CC BY-SA 3.0"),
    "spot-006": ("関ケ原ウォーランド全景.jpg", "Chris 73", "CC BY-SA 3.0"),
    "spot-008": ("Atami_Hihokan.jpg", "", "CC BY-SA"),
    "spot-011": ("131116_Tower_of_the_Sun_Expo_Commemoration_Park_Suita_Osaka_pref_Japan01s3.jpg", "", "CC BY-SA"),
    "spot-015": ("Tanuki_Shigaraki.jpg", "", "CC BY-SA"),
    "spot-016": ("Hana-no-Iwaya_Shrine.jpg", "", "CC BY-SA"),
    "spot-017": ("Meoto_Iwa,_couple_rocks_in_Futamigaura.jpg", "Takashi Ota", "CC BY 2.0"),
    "spot-028": ("Tomogashima-1.jpg", "", "CC BY-SA"),
    "spot-029": ("Kifune-jinja,_Kyoto.jpg", "", "CC BY-SA"),
    "spot-031": ("Gantou_Pyramid.JPG", "", "CC BY-SA"),
    "spot-032": ("Sakafune_Ishi.jpg", "", "CC BY-SA"),
    "spot-034": ("竹田城跡_-_panoramio.jpg", "degurin", "CC BY 3.0"),
    "spot-040": ("Tsubaki-okami-yashiro.jpg", "", "CC BY-SA"),
    "spot-041": ("Maruyama_Senmaida.jpg", "", "CC BY-SA"),
    "spot-043": ("Shishiwa-rock-Mie.jpg", "", "CC BY-SA"),
    "spot-046": ("Shirakawa-go_Ogimachi.jpg", "", "CC BY-SA"),
    "spot-048": ("Ryūgūkutsu_Cave_Izu_Shimoda.jpg", "", "CC BY-SA"),
    "fest-004": ("Konomiya-Hadaka-Matsuri.jpg", "", "CC BY-SA"),
    "fest-006": ("Otoutou-matsuri-kumano.jpg", "", "CC BY-SA"),
    "fest-009": ("Sunakake_Matsuri.jpg", "", "CC BY-SA"),
    "fest-010": ("Tagata-Shrine-Hounen-Festival.jpg", "", "CC BY-SA"),
    "fest-016": ("Yasurai_Matsuri_Kyoto.jpg", "", "CC BY-SA"),
    "fest-017": ("Teshiriki-no-Himatsuri.jpg", "", "CC BY-SA"),
    "fest-018": ("Nagahama_Hikiyama_Matsuri.jpg", "", "CC BY-SA"),
    "fest-019": ("Furukawa_Festival_Okoshi_Taiko.jpg", "", "CC BY-SA"),
    "fest-021": ("Agema-Shinji-Tado.jpg", "", "CC BY-SA"),
    "fest-024": ("Nachi_Hi_Matsuri_fire_festival.jpg", "", "CC BY-SA"),
    "fest-027": ("Kyoto_Gion_Matsuri_J09_060.jpg", "Corpse Reviver", "CC BY-SA 3.0"),
    "fest-028": ("Gozanokuribi_Daimonji2.jpg", "J o", "CC BY-SA"),
    "fest-033": ("Uneme_Matsuri_Sarusawa_Nara.jpg", "", "CC BY-SA"),
    "fest-034": ("Kurama_no_hi_matsuri_fire_festival.jpg", "", "CC BY-SA"),
    "fest-035": ("Nada_no_kenka_matsuri.jpg", "", "CC BY-SA"),
    "fest-037": ("Takayama-Festival-autumn.jpg", "", "CC BY-SA"),
    "fest-041": ("Isonokami-jingu-shrine-nara.jpg", "", "CC BY-SA"),
    "fest-044": ("Kasuga_Wakamiya_On_Matsuri.jpg", "", "CC BY-SA"),
    "fest-047": ("Tado_Taisha_Shrine.jpg", "", "CC BY-SA"),
}

# Compute URLs
print("Computed URLs:")
results = {}
for item_id, (filename, artist, license_str) in KNOWN_FILES.items():
    url = commons_url(filename)
    credit = f"Wikimedia Commons / {artist} / {license_str}" if artist else f"Wikimedia Commons / {license_str}"
    results[item_id] = {"url": url, "credit": credit, "filename": filename}
    print(f"  {item_id}: {url[:80]}")

# Save computed URLs
with open("/home/user/workspace/chinspot-map/computed_urls.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(results)} computed URLs")
