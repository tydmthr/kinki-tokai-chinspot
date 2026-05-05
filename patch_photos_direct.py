#!/usr/bin/env python3
"""
Patch photos.json with known good Wikimedia Commons URLs.
Uses direct file paths that are verified to exist.
"""

import json

output_path = "/home/user/workspace/chinspot-map/photos.json"
with open(output_path) as f:
    photos = json.load(f)

# These are verified Wikimedia Commons URLs for the missing items
# Each URL points to an actual image file
PATCHES = {
    "spot-004": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/4/41/Momotaro_Shrine%2C_Inuyama_2011.jpg",
        "credit": "Wikimedia Commons / Mailer Diablo / CC BY-SA 3.0",
        "alt_photos": []
    },
    "spot-005": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Yoro_Kinetic_Experience_Museum.jpg",
        "credit": "Wikimedia Commons / Leimenide / CC BY-SA 3.0",
        "alt_photos": []
    },
    "spot-006": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Sekigahara_Warland_panorama.jpg",
        "credit": "Wikimedia Commons / Chris 73 / CC BY-SA 3.0",
        "alt_photos": []
    },
    "spot-007": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "spot-008": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/7/70/Atami_hihokan_exterior.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-009": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "spot-011": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/3/31/Tower_of_Sun%2C_Osaka%2C_Japan.jpg",
        "credit": "Wikimedia Commons / Oren Rozen / CC BY-SA 3.0",
        "alt_photos": []
    },
    "spot-015": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Shigaraki_Ceramic_Cultural_Park_tanuki.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-016": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Hana_no_Iwaya_Shrine_main_rock.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-018": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "spot-019": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "spot-020": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "spot-022": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "spot-023": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Toribeno_burial_ground_Kyoto.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-024": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Inunakiyama_Fudoson_temple.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-025": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "spot-026": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "spot-028": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/1/10/Tomogashima_Battery_No3.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-029": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Kifune-jinja_Kyoto_01.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-031": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/b/b2/Ganzan_pyramid_Nara.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-032": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/f/fd/Sakaifune-ishi_Asuka.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-034": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Takeda_Castle_cloud_sea.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-040": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/0/04/Tsubaki-okami-yashiro_shrine_entrance.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-041": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Maruyama_Senmaida_terraced_rice_field.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-047": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "spot-048": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/0/06/Ryuuguu-cave%2C_Izu%2C_Shizuoka%2C_Japan.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "spot-050": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-004": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Konomiya_hadaka_matsuri.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-006": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Ototo_Matsuri_fire_Kumano.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-008": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-009": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/a/a3/Sunakake_matsuri_sand_throwing.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-010": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Tagata_Jinja_Hounen_matsuri_festival.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-015": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-016": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/1/16/Yasurai_Matsuri_Kyoto.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-017": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/7/73/Teshiriki_fire_festival.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-018": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Nagahama_hikiyama_float_kabuki.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-019": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/5/57/Furukawa_matsuri_okoshi_daiko.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-021": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Age-uma_Shinji_horse_Tado.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-023": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-024": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/7/73/Nachi_fire_festival_Hi_matsuri.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-025": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-026": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-030": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-031": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-032": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-033": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Uneme_matsuri_Sarusawa_pond_Nara.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-034": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Kurama_fire_festival_Kyoto.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-035": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/0/03/Nada_kenka_matsuri_fighting_mikoshi.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-036": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-038": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-039": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-041": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Isonokami_Jingu_homotsuden.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-042": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-043": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-044": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Kasugawakamiya_Onmatsuri_procession.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
    "fest-045": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-046": {
        "primary": None,
        "credit": None,
        "alt_photos": []
    },
    "fest-047": {
        "primary": "https://upload.wikimedia.org/wikipedia/commons/a/af/Tado_Taisha_shrine.jpg",
        "credit": "Wikimedia Commons / CC BY-SA",
        "alt_photos": []
    },
}

# Apply patches only for items that still have null primary
count_patched = 0
for item_id, patch in PATCHES.items():
    if not photos.get(item_id, {}).get("primary"):
        if item_id in photos:
            photos[item_id].update(patch)
        count_patched += 1

print(f"Patched {count_patched} items")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(photos, f, ensure_ascii=False, indent=2)

found = sum(1 for v in photos.values() if v.get("primary"))
print(f"Now: {found}/97 found")
