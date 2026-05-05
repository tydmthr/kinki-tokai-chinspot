#!/usr/bin/env python3
"""
Fetch representative photo URLs from Wikimedia Commons for spots and festivals.
Uses the Wikimedia Commons API (MediaSearch / imageinfo).
"""

import json
import time
import urllib.parse
import urllib.request
import hashlib
import os

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
WIKIPEDIA_API = "https://ja.wikipedia.org/w/api.php"

def wikimedia_search(query, limit=5):
    """Search Wikimedia Commons for images matching query."""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": f"filetype:bitmap {query}",
        "srnamespace": "6",  # File namespace
        "srlimit": str(limit),
        "format": "json",
        "origin": "*"
    }
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ChinSpotBot/1.0 (photo-collection)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("query", {}).get("search", [])
    except Exception as e:
        print(f"  [ERROR] wikimedia_search({query}): {e}")
        return []

def get_file_info(filename):
    """Get direct URL and metadata for a Commons file."""
    params = {
        "action": "query",
        "titles": filename,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": "800",
        "format": "json",
        "origin": "*"
    }
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ChinSpotBot/1.0 (photo-collection)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get("query", {}).get("pages", {})
            for page_id, page in pages.items():
                ii = page.get("imageinfo", [])
                if ii:
                    info = ii[0]
                    ext = page.get("imageinfo", [{}])[0].get("extmetadata", {})
                    artist = ext.get("Artist", {}).get("value", "")
                    license_short = ext.get("LicenseShortName", {}).get("value", "")
                    license_url = ext.get("LicenseUrl", {}).get("value", "")
                    # Clean artist HTML
                    import re
                    artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
                    return {
                        "url": info.get("url", ""),
                        "thumb": info.get("thumburl", info.get("url", "")),
                        "artist": artist_clean,
                        "license": license_short,
                        "license_url": license_url,
                        "filename": filename
                    }
    except Exception as e:
        print(f"  [ERROR] get_file_info({filename}): {e}")
    return None

def search_wikipedia_image(article_name):
    """Get the main image from a Japanese Wikipedia article."""
    params = {
        "action": "query",
        "titles": article_name,
        "prop": "pageimages",
        "pithumbsize": "800",
        "format": "json",
        "origin": "*"
    }
    url = WIKIPEDIA_API + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ChinSpotBot/1.0 (photo-collection)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get("query", {}).get("pages", {})
            for page_id, page in pages.items():
                if "thumbnail" in page:
                    thumb_url = page["thumbnail"]["source"]
                    # Convert thumb URL to full image URL
                    # Thumb URL pattern: .../thumb/a/ab/filename.jpg/800px-filename.jpg
                    # Full URL: .../a/ab/filename.jpg
                    import re
                    m = re.search(r'/thumb/(.+?)(?:/\d+px-[^/]+)?$', thumb_url)
                    if m:
                        path = m.group(1)
                        full_url = f"https://upload.wikimedia.org/wikipedia/commons/{path}"
                        # Also try ja wikipedia path
                        if not full_url.startswith("https://upload.wikimedia.org/wikipedia/commons/"):
                            full_url = thumb_url  # fallback to thumb
                        return {
                            "url": full_url,
                            "thumb": thumb_url,
                            "artist": "Wikipedia contributor",
                            "license": "CC BY-SA",
                            "from_wikipedia": article_name
                        }
    except Exception as e:
        print(f"  [ERROR] search_wikipedia_image({article_name}): {e}")
    return None

def wikimedia_mediasearch(query, limit=5):
    """Use MediaSearch API for better image search."""
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": query,
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": "800",
        "format": "json",
        "origin": "*"
    }
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ChinSpotBot/1.0 (photo-collection)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get("query", {}).get("pages", {})
            results = []
            import re
            for page_id, page in pages.items():
                ii = page.get("imageinfo", [])
                if ii:
                    info = ii[0]
                    ext = info.get("extmetadata", {})
                    artist = ext.get("Artist", {}).get("value", "")
                    artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
                    license_short = ext.get("LicenseShortName", {}).get("value", "")
                    img_url = info.get("url", "")
                    # Only include actual images
                    if any(img_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        results.append({
                            "url": img_url,
                            "thumb": info.get("thumburl", img_url),
                            "artist": artist_clean,
                            "license": license_short,
                            "filename": page.get("title", "")
                        })
            return results
    except Exception as e:
        print(f"  [ERROR] wikimedia_mediasearch({query}): {e}")
        return []

def fetch_photo(item_id, name, alt_queries=None):
    """
    Fetch a representative photo for a spot/festival.
    Returns dict with primary URL, credit, and alt_photos.
    """
    print(f"\n[{item_id}] Searching: {name}")
    
    queries = [name]
    if alt_queries:
        queries.extend(alt_queries)
    
    all_results = []
    for q in queries[:2]:  # limit to 2 queries per item
        results = wikimedia_mediasearch(q, limit=5)
        if results:
            all_results.extend(results)
            break
        time.sleep(0.3)
    
    # Filter for valid image URLs
    valid = [r for r in all_results if r.get("url") and 
             any(r["url"].lower().endswith(e) for e in ['.jpg', '.jpeg', '.png', '.webp'])]
    
    if valid:
        primary = valid[0]
        alt_photos = [r["url"] for r in valid[1:3] if r["url"] != primary["url"]]
        
        # Build credit string
        artist = primary.get("artist", "")
        license_str = primary.get("license", "CC BY-SA")
        if artist:
            credit = f"Wikimedia Commons / {artist} / {license_str}"
        else:
            credit = f"Wikimedia Commons / {license_str}"
        
        print(f"  -> Found: {primary['url'][:80]}...")
        return {
            "name": name,
            "primary": primary["url"],
            "credit": credit,
            "alt_photos": alt_photos
        }
    
    # Fallback: try Wikipedia article image
    wiki_result = search_wikipedia_image(name)
    if wiki_result:
        print(f"  -> Wikipedia fallback: {wiki_result['url'][:80]}...")
        return {
            "name": name,
            "primary": wiki_result["url"],
            "credit": f"Wikipedia / {wiki_result.get('artist', 'contributor')} / CC BY-SA",
            "alt_photos": []
        }
    
    print(f"  -> Not found")
    return {
        "name": name,
        "primary": None,
        "credit": None,
        "alt_photos": []
    }

# Load data
with open("/home/user/workspace/chinspot-map/spots.json") as f:
    spots = json.load(f)

with open("/home/user/workspace/chinspot-map/festivals.json") as f:
    festivals = json.load(f)

# Output
photos = {}
output_path = "/home/user/workspace/chinspot-map/photos.json"

# Load existing progress if any
if os.path.exists(output_path):
    with open(output_path) as f:
        try:
            photos = json.load(f)
            print(f"Resuming from existing file with {len(photos)} entries")
        except:
            photos = {}

def save_progress():
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(photos, f, ensure_ascii=False, indent=2)

# Process spots
print("\n=== SPOTS (50) ===")
for spot in spots:
    sid = spot["id"]
    if sid in photos:
        print(f"[{sid}] Already done: {spot['name']}")
        continue
    
    name = spot["name"]
    # Build alt queries from other names/locations
    alts = []
    if spot.get("prefecture"):
        alts.append(f"{name} {spot['prefecture']}")
    
    result = fetch_photo(sid, name, alts)
    photos[sid] = result
    time.sleep(0.5)
    
    # Save every 5 items
    if len([k for k in photos if k.startswith("spot")]) % 5 == 0:
        save_progress()
        print(f"  [Saved progress: {len(photos)} entries]")

save_progress()
print(f"\n=== Spots done. Total entries: {len(photos)} ===")

# Process festivals
print("\n=== FESTIVALS (47) ===")
for fest in festivals:
    fid = fest["id"]
    if fid in photos:
        print(f"[{fid}] Already done: {fest['name']}")
        continue
    
    name = fest["name"]
    # For festivals, also try the shrine/temple name
    alts = []
    if fest.get("shrine"):
        alts.append(fest["shrine"])
    if fest.get("prefecture"):
        alts.append(f"{name} {fest['prefecture']}")
    
    result = fetch_photo(fid, name, alts)
    photos[fid] = result
    time.sleep(0.5)
    
    if len([k for k in photos if k.startswith("fest")]) % 5 == 0:
        save_progress()
        print(f"  [Saved progress: {len(photos)} entries]")

save_progress()

# Statistics
total = len(photos)
found = sum(1 for v in photos.values() if v.get("primary"))
print(f"\n=== COMPLETE ===")
print(f"Total: {total} | Found: {found} | Missing: {total-found}")
