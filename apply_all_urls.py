#!/usr/bin/env python3
"""Apply all collected URLs to photos.json."""
import json, re

def clean_thumb_url(url):
    """Convert thumb URL to full resolution URL."""
    if not url:
        return url
    # Remove /thumb/ and the size suffix to get full URL
    # Pattern: .../thumb/a/ab/filename.ext/800px-filename.ext -> .../a/ab/filename.ext
    m = re.match(r'(https://upload\.wikimedia\.org/wikipedia/commons/)thumb/(.+?)(?:/\d+px-.+)?$', url)
    if m:
        return m.group(1) + m.group(2)
    m2 = re.match(r'(https://upload\.wikimedia\.org/wikipedia/[a-z]+/)thumb/(.+?)(?:/\d+px-.+)?$', url)
    if m2:
        return m2.group(1) + m2.group(2)
    # Already a direct URL or thumb without size suffix
    return url

# All URLs collected from Wikipedia API (source URLs, may be thumb URLs)
COLLECTED = {
    # From searches above
    "spot-005": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Takidani_Yoro_Park_2008-9-24.jpg/1280px-Takidani_Yoro_Park_2008-9-24.jpg",
    "spot-011": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/131116_Expo_Commemoration_Park_Suita_Osaka_pref_Japan01s3.jpg/1280px-131116_Expo_Commemoration_Park_Suita_Osaka_pref_Japan01s3.jpg",
    "spot-022": None,  # Not found
    "spot-023": None,  # Not found
    "spot-024": None,  # Not found
    "spot-025": "https://upload.wikimedia.org/wikipedia/commons/6/67/Kuniyoshi_Taiba_%28The_End%29.jpg",  # Nue painting - keep as historical art
    "spot-028": "https://upload.wikimedia.org/wikipedia/commons/1/18/%E5%8F%8B%E3%81%8C%E5%B3%B6%E3%83%BB%E7%B4%80%E6%B7%A1%E6%B5%B7%E5%B3%A1PA071003.jpg",
    "spot-029": "https://upload.wikimedia.org/wikipedia/commons/3/3b/Kibune_Shinto_Shrine001.jpg",
    "spot-031": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Zuto_2022.jpg/1280px-Zuto_2022.jpg",
    "spot-032": None,  # Not found
    "spot-039": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Kumano_Kodo_World_heritage_Nachi-no-taki_%E7%86%8A%E9%87%8E%E5%8F%A4%E9%81%93_%E9%82%A3%E6%99%BA%E5%A4%A7%E6%BB%9D10.JPG/1280px-Kumano_Kodo_World_heritage_Nachi-no-taki_%E7%86%8A%E9%87%8E%E5%8F%A4%E9%81%93_%E9%82%A3%E6%99%BA%E5%A4%A7%E6%BB%9D10.JPG",  # Already have from spot-039
    "spot-041": "https://upload.wikimedia.org/wikipedia/commons/e/e6/2011_07_13%E4%B8%B8%E5%B1%B1%E5%8D%83%E6%9E%9A%E7%94%B0%E5%85%A8%E6%99%AF.jpg",
    "spot-042": None,  # Need to set - already found via kigejo
    "spot-044": None,  # Already found
    "spot-045": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Yoro-waterfall.JPG/1280px-Yoro-waterfall.JPG",
    "spot-046": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Shirakawa-go_%282017-07-22%29.jpg/1280px-Shirakawa-go_%282017-07-22%29.jpg",
    "spot-038": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/180429_Hashiguiiwa_Kushimoto_Wakayama_pref_Japan02bs.jpg/1280px-180429_Hashiguiiwa_Kushimoto_Wakayama_pref_Japan02bs.jpg",
    "spot-042": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Oniga-jo01.JPG/1280px-Oniga-jo01.JPG",
    # Festivals
    "fest-002": None,  # Already found
    "fest-004": "https://upload.wikimedia.org/wikipedia/commons/6/66/Kounomiya-hadakamaturi.jpg",
    "fest-005": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Asukaniimasu-jinja04n3900.jpg/1280px-Asukaniimasu-jinja04n3900.jpg",
    "fest-006": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Kamikura-jinja%2C_shaden.jpg/1280px-Kamikura-jinja%2C_shaden.jpg",
    "fest-007": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Owase_Shrine_%28Jinja%29_-_panoramio.jpg/1280px-Owase_Shrine_%28Jinja%29_-_panoramio.jpg",
    "fest-024": "https://upload.wikimedia.org/wikipedia/commons/9/9c/Shrine_Kumano_nachi01.jpg",  # Use shrine image for Nachi fire festival
    "fest-025": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Taimatsuri1.jpg/1280px-Taimatsuri1.jpg",
    "fest-027": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Gion_Matsuri_2017-5.jpg/1280px-Gion_Matsuri_2017-5.jpg",
    "fest-028": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Gozanokuribi_Daimonji3.JPG/1280px-Gozanokuribi_Daimonji3.JPG",
    "fest-029": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/IshidoriMatsuri.JPG/1280px-IshidoriMatsuri.JPG",
    "fest-034": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Fire_festival_of_KURAMA_Kyoto%2C_Japan.jpg",
    "fest-035": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Nada_no_Kenka_matsuri_%2C_himeji01.JPG/1280px-Nada_no_Kenka_matsuri_%2C_himeji01.JPG",
    "fest-037": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Kagura_Tai_Float.jpg/1280px-Kagura_Tai_Float.jpg",
    "fest-040": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Kujirabune01.jpg/1280px-Kujirabune01.jpg",
    "fest-044": "https://upload.wikimedia.org/wikipedia/commons/a/ac/Onmatsuri7.jpeg",
    "fest-047": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Tado-taisha%2C_hongu_and_betsugu.jpg/1280px-Tado-taisha%2C_hongu_and_betsugu.jpg",
}

# Load photos
with open("/home/user/workspace/chinspot-map/photos.json") as f:
    photos = json.load(f)

count = 0
for item_id, url in COLLECTED.items():
    if not photos.get(item_id, {}).get("primary") and url:
        clean_url = clean_thumb_url(url)
        photos[item_id]["primary"] = clean_url
        photos[item_id]["credit"] = "Wikimedia Commons / Wikipedia contributor / CC BY-SA"
        photos[item_id]["alt_photos"] = []
        count += 1
        print(f"[{item_id}] Set: {clean_url[:70]}")

with open("/home/user/workspace/chinspot-map/photos.json", "w", encoding="utf-8") as f:
    json.dump(photos, f, ensure_ascii=False, indent=2)

found = sum(1 for v in photos.values() if v.get("primary"))
print(f"\nApplied {count} URLs. Total: {found}/97")
missing = [k for k, v in photos.items() if not v.get("primary")]
print(f"Still missing ({len(missing)}): {missing}")
