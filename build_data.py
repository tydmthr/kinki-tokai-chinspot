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
        # Copy all keys ending in _en (covers name_en, summary_en, origin_en,
        # viewing_notes_en, cultural_position_en, local_view_en, related_works_en,
        # trivia_en, photo_tips_en, references_en, etc. — anything translated)
        for k, v in e.items():
            if k.endswith('_en'):
                item[k] = v
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

# ============ Update index.html / en/index.html count display ============
import re

spot_count = len(spots)
fest_count = len(fests)
prefs = {d.get('prefecture') for d in spots + fests if d.get('prefecture')}
pref_count = len(prefs)

def update_html(path, patterns):
    """Apply (regex, replacement) pairs to file. Report changes."""
    full = os.path.join(base, path)
    if not os.path.exists(full):
        print(f'  skip (not found): {path}')
        return 0
    with open(full, encoding='utf-8') as f:
        text = f.read()
    original = text
    total = 0
    for pat, repl in patterns:
        text, n = re.subn(pat, repl, text)
        total += n
    if text != original:
        with open(full, 'w', encoding='utf-8') as f:
            f.write(text)
    print(f'  {path}: {total} replacements')
    return total

# JA index.html patterns: 珍スポットXXX＆奇祭YYY 形式、XXX件と奇祭YYY件 形式、XXX strange spots and YYY 形式
ja_patterns = [
    # 珍スポットN＆奇祭M（title / og:title）
    (r'珍スポット\d+＆奇祭\d+', f'珍スポット{spot_count}＆奇祭{fest_count}'),
    # 珍スポットN件と奇祭M件
    (r'珍スポット\d+件と奇祭\d+件', f'珍スポット{spot_count}件と奇祭{fest_count}件'),
    # N strange spots and M wild festivals
    (r'\d+ strange spots and \d+ wild festivals', f'{spot_count} strange spots and {fest_count} wild festivals'),
    # hero stat: <span ... id="statSpots">N</span>
    (r'(id="statSpots"[^>]*>)\d+(</span>)', rf'\g<1>{spot_count}\g<2>'),
    (r'(id="statFests"[^>]*>)\d+(</span>)', rf'\g<1>{fest_count}\g<2>'),
    (r'(id="statPrefs"[^>]*>)\d+(</span>)', rf'\g<1>{pref_count}\g<2>'),
    # list-tab JA
    (r'(data-listtab="spots">)珍スポット\s*\d+(</button>)', rf'\g<1>珍スポット {spot_count}\g<2>'),
    (r'(data-listtab="festivals">)奇祭\s*\d+(</button>)', rf'\g<1>奇祭 {fest_count}\g<2>'),
]

# EN index.html patterns
en_patterns = [
    (r'\d+ Strange Spots & \d+ Wild Festivals', f'{spot_count} Strange Spots & {fest_count} Wild Festivals'),
    (r'\d+ strange spots and \d+ wild festivals', f'{spot_count} strange spots and {fest_count} wild festivals'),
    (r'(id="statSpots"[^>]*>)\d+(</span>)', rf'\g<1>{spot_count}\g<2>'),
    (r'(id="statFests"[^>]*>)\d+(</span>)', rf'\g<1>{fest_count}\g<2>'),
    (r'(id="statPrefs"[^>]*>)\d+(</span>)', rf'\g<1>{pref_count}\g<2>'),
    # list-tab EN: "Spots — N" / "Festivals — N"
    (r'(data-listtab="spots">)Spots\s*—\s*\d+(</button>)', rf'\g<1>Spots — {spot_count}\g<2>'),
    (r'(data-listtab="festivals">)Festivals\s*—\s*\d+(</button>)', rf'\g<1>Festivals — {fest_count}\g<2>'),
]

print(f'Updating HTML count display (spots={spot_count}, fests={fest_count}, prefs={pref_count})')
update_html('index.html', ja_patterns)
update_html('en/index.html', en_patterns)
