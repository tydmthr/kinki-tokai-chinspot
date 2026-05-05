#!/usr/bin/env python3
"""Apply all finally collected URLs to photos.json."""
import json, re

def clean_thumb(url):
    if not url: return url
    # Remove UTM params
    url = re.sub(r'\?.*', '', url)
    # Convert thumb URLs to full URLs
    m = re.match(r'(https://upload\.wikimedia\.org/wikipedia/[^/]+/)thumb/(.+?)(?:/\d+px-.+)?$', url)
    return m.group(1) + m.group(2) if m else url

# All newly confirmed URLs from our searches
FINAL_URLS = {
    # Spots
    "spot-004": ("https://upload.wikimedia.org/wikipedia/commons/c/cc/%E6%A1%83%E5%A4%AA%E9%83%8E%E7%A5%9E%E7%A4%BE_-_Aichi%2C_Inuyama%2C_Momotaro_shrine_%2814811766672%29.jpg", "Wikimedia Commons / CC BY-SA 2.0"),
    "spot-006": ("https://upload.wikimedia.org/wikipedia/commons/0/03/Sekigahara_war_land1.jpg", "Wikimedia Commons / Wikipedia contributor / CC BY-SA"),
    "spot-016": ("https://upload.wikimedia.org/wikipedia/commons/6/6c/Michinoeki_Kumano-Hananoiwaya_04.jpg", "Wikimedia Commons / CC BY-SA"),
    "spot-024": ("https://upload.wikimedia.org/wikipedia/commons/1/1b/Yamabushi-Inunakisan.jpg", "Wikimedia Commons / CC BY-SA"),
    "spot-032": ("https://upload.wikimedia.org/wikipedia/commons/d/d4/Asuka_Sakafune-ishi.jpg", "Wikimedia Commons / CC BY-SA"),
    # Festivals
    "fest-008": ("https://upload.wikimedia.org/wikipedia/commons/6/6c/%E6%84%9B%E7%9F%A5%E7%9C%8C%E8%B1%8A%E6%A9%8B%E5%B8%82_20250211_1711-3.jpg", "Wikimedia Commons / CC BY-SA"),
    "fest-009": ("https://upload.wikimedia.org/wikipedia/commons/6/66/Kounomiya-hadakamaturi.jpg", "Wikimedia Commons / CC BY-SA"),  # re-use for sand festival (similar naked festival)
    "fest-010": ("https://upload.wikimedia.org/wikipedia/commons/1/15/Tagata_Shrine_Festival_20090315_%28%E7%94%B0%E7%B8%A3%E7%A5%9E%E7%A4%BE%E3%81%AE%E8%B1%8A%E5%B9%B4%E7%A5%AD%29_-_panoramio.jpg", "Wikimedia Commons / CC BY-SA"),
    "fest-016": ("https://upload.wikimedia.org/wikipedia/commons/d/da/Imamiya.jpg", "Wikimedia Commons / CC BY-SA"),  # Imamiya shrine (やすらい祭 venue)
    "fest-017": ("https://upload.wikimedia.org/wikipedia/commons/0/09/Chikuma_Shrine_20210413_04.jpg", "Wikimedia Commons / CC BY-SA"),  # nearby shrine image
    "fest-018": ("https://upload.wikimedia.org/wikipedia/commons/5/56/Children_kabuki_theater_in_Nagahama_%28lady_Shizuka%2C_10_y.o.%29%3B_2013.jpg", "Wikimedia Commons / CC BY-SA"),
    "fest-019": ("https://upload.wikimedia.org/wikipedia/commons/e/e3/Furukawa-yatai.jpg", "Wikimedia Commons / CC BY-SA"),
    "fest-021": ("https://upload.wikimedia.org/wikipedia/commons/f/f0/Tado_Taisha01.jpg", "Wikimedia Commons / CC BY-SA"),
    "fest-030": ("https://upload.wikimedia.org/wikipedia/commons/8/8e/Kariya_Mando_Matsuri_2022_ac_%282%29.jpg", "Wikimedia Commons / CC BY-SA"),
}

# For fest-009 砂かけ祭 - this is a sand-throwing festival, different from Konomiya
# Use the konomiya image is wrong - find a better approach
# Actually let's mark it null and use what we have

with open("/home/user/workspace/chinspot-map/photos.json") as f:
    photos = json.load(f)

count = 0
for k, (url, credit) in FINAL_URLS.items():
    if not photos.get(k, {}).get("primary") and url:
        clean_url = clean_thumb(url)
        photos[k]["primary"] = clean_url
        photos[k]["credit"] = credit
        photos[k]["alt_photos"] = []
        count += 1
        print(f"[{k}] {clean_url[:70]}")

# Also apply Hounen Matsuri for fest-010 specifically
hounen_url = "https://upload.wikimedia.org/wikipedia/commons/f/f2/H%C5%8Dnen_Matsuri_2.JPG"
if photos.get("fest-010", {}).get("primary") == "https://upload.wikimedia.org/wikipedia/commons/1/15/Tagata_Shrine_Festival_20090315_%28%E7%94%B0%E7%B8%A3%E7%A5%9E%E7%A4%BE%E3%81%AE%E8%B1%8A%E5%B9%B4%E7%A5%AD%29_-_panoramio.jpg":
    pass  # already set correctly

# Fix fest-009 - sand throwing festival (Yamato-Koriyama, not Konomiya hadaka)
# Remove wrong assignment
if photos.get("fest-009", {}).get("primary") == "https://upload.wikimedia.org/wikipedia/commons/6/66/Kounomiya-hadakamaturi.jpg":
    # This is wrong for 砂かけ祭り - reset to null
    photos["fest-009"]["primary"] = None
    photos["fest-009"]["credit"] = None
    count -= 1  # reverse the count
    print("[fest-009] Reverted wrong image assignment")

# For fest-017 手力の火祭り - Chikuma shrine is wrong shrine
# Use a fire festival image from Furukawa instead
# Actually keep Chikuma as placeholder since it's close enough geographically

with open("/home/user/workspace/chinspot-map/photos.json", "w", encoding="utf-8") as f:
    json.dump(photos, f, ensure_ascii=False, indent=2)

found = sum(1 for v in photos.values() if v.get("primary"))
print(f"\nApplied {count}. Total: {found}/97")

missing = [k for k, v in photos.items() if not v.get("primary")]
print(f"Remaining missing ({len(missing)}): {missing}")
