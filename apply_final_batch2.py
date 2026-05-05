import json
import re

def clean_url(url):
    return re.sub(r'\?.*', '', url)

with open('/home/user/workspace/chinspot-map/photos.json', 'r', encoding='utf-8') as f:
    photos = json.load(f)

updates = {
    # 旧女鬼トンネル - 女鬼峠 (Kumano Kodo trail near the old tunnel location)
    'spot-018': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/e/e2/%E7%86%8A%E9%87%8E%E5%8F%A4%E9%81%93%E4%BC%8A%E5%8B%A2%E8%B7%AF%E5%A5%B3%E9%AC%BC%E5%B3%A0_04.jpg',
        'credit': 'Wikimedia Commons / Wikipedia contributor / CC BY-SA',
    },
    # 砂かけ祭り - 廣瀬大社 (Hirose Taisha) is the famous venue for この祭り in Nara
    # The fest-009 says Yasaka Tawaramoto but the famous 砂かけ祭り is at Hirose Taisha
    # Using Hirose Taisha image with appropriate credit note
    'fest-009': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/0/0b/HIROSE_TAISHA_TAIHO.jpg',
        'credit': 'Wikimedia Commons / Wikipedia contributor / CC BY-SA ※廣瀬大社（奈良）の砂かけ祭り関連',
    },
    # 近江中山の芋競べ祭り - use 日野祭 image from 綿向神社 (nearby in Hino-cho) as closest Commons match
    'fest-031': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/d/d7/%E6%97%A5%E9%87%8E%E7%A5%AD%20%E7%B6%BF%E5%90%91%E7%A5%9E%E7%A4%BE%E5%A2%83%E5%86%85%E6%9B%B3%E5%B1%B1%E3%81%AE%E4%B8%A6%E3%81%B31.jpg',
        'credit': 'Wikimedia Commons / Wikipedia contributor / CC BY-SA ※日野町綿向神社の日野祭',
    },
}

# Apply updates
for key, vals in updates.items():
    if key in photos:
        photos[key]['primary'] = vals['primary']
        photos[key]['credit'] = vals['credit']
        print(f"Updated {key}: {photos[key]['name']}")

# Count results
null_count = sum(1 for v in photos.values() if v.get('primary') is None)
found_count = sum(1 for v in photos.values() if v.get('primary') is not None)
print(f"\nTotal: {len(photos)} items")
print(f"Found: {found_count}")
print(f"Null: {null_count}")

print("\nRemaining null items:")
for k, v in photos.items():
    if v.get('primary') is None:
        print(f"  {k}: {v['name']}")

with open('/home/user/workspace/chinspot-map/photos.json', 'w', encoding='utf-8') as f:
    json.dump(photos, f, ensure_ascii=False, indent=2)
print("\nSaved.")
