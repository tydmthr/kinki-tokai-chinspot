#!/usr/bin/env python3
"""Rebuild data.js by merging spots.json + festivals.json + photos + access + EN translations."""
import json, os

base = os.path.dirname(__file__)

def load(name):
    p = os.path.join(base, name)
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)

spots = load('spots.json') or []
fests = load('festivals.json') or []
photos = load('photos.json') or {}
access = load('access_info.json') or {}
spots_en = load('spots_en.json') or {}
fests_en = load('festivals_en.json') or {}

# Normalize EN dicts (could be list or dict)
def to_dict_by_id(x):
    if isinstance(x, dict):
        return x
    if isinstance(x, list):
        return {item['id']: item for item in x if 'id' in item}
    return {}

spots_en = to_dict_by_id(spots_en)
fests_en = to_dict_by_id(fests_en)
photos = to_dict_by_id(photos) if isinstance(photos, list) else photos
access = to_dict_by_id(access) if isinstance(access, list) else access

def enrich(item):
    iid = item['id']
    p = photos.get(iid)
    if p:
        if isinstance(p, dict):
            item['photo_url'] = p.get('primary') or p.get('url')
            item['photo_credit'] = p.get('credit')
            item['photo_license'] = p.get('license')
        elif isinstance(p, str):
            item['photo_url'] = p
    a = access.get(iid)
    if a:
        item['access'] = a
    e = (spots_en if iid.startswith('spot-') else fests_en).get(iid)
    if e:
        for k in ['name_en','prefecture_en','city_en','summary_en','highlights_en']:
            if k in e:
                item[k] = e[k]
    return item

spots = [enrich(s) for s in spots]
fests = [enrich(f) for f in fests]

out = "/* Auto-generated. Do not edit directly. */\n"
out += "const SPOTS = " + json.dumps(spots, ensure_ascii=False) + ";\n"
out += "const FESTIVALS = " + json.dumps(fests, ensure_ascii=False) + ";\n"

with open(os.path.join(base, 'data.js'), 'w', encoding='utf-8') as f:
    f.write(out)

print(f'data.js regenerated: {len(spots)} spots, {len(fests)} festivals')
print(f'Spots with deepdive: {sum(1 for s in spots if s.get("deepdive"))}')
print(f'Fests with deepdive: {sum(1 for f in fests if f.get("deepdive"))}')
