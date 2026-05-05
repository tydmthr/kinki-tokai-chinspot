import json
import re

def clean_url(url):
    """Remove UTM params from Wikimedia URLs"""
    return re.sub(r'\?.*', '', url)

# Load current photos.json
with open('/home/user/workspace/chinspot-map/photos.json', 'r', encoding='utf-8') as f:
    photos = json.load(f)

# Updates to apply based on our research session
updates = {
    # 竜宮窟 - Shimoda Ryugu sea cave (better photo)
    'spot-048': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/8/8b/Shimoda_Ryugu-Seeh%C3%B6hle_am_Abend_02.jpg',
        'credit': 'Wikimedia Commons / Wikipedia contributor / CC BY-SA',
    },
    # 首塚大明神 - actual festival photo at Kubizuka Daimyojin shrine
    'spot-022': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/b/b2/Kubizuka_Daimyoujin_Annual_festival_April_15%2C_2019_IMG_20190415_095838.jpg',
        'credit': 'Wikimedia Commons / Wikipedia contributor / CC BY-SA',
    },
    # 鳥辺野 - Toribeno Myoken-do panoramio photo
    'spot-023': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/a/a4/%E9%B3%A5%E8%BE%BA%E9%87%8E%E5%A6%99%E8%A6%8B%E5%A0%82_-_panoramio.jpg',
        'credit': 'Wikimedia Commons / panoramio contributor / CC BY-SA',
    },
    # 旧長野トンネル - Nagano Tunnel (Tsu side / old abandoned tunnel)
    'spot-019': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/d/d2/%E6%97%A7%E9%95%B7%E9%87%8E%E3%83%88%E3%83%B3%E3%83%8D%E3%83%AB%E6%B4%A5.jpg',
        'credit': 'Wikimedia Commons / Wikipedia contributor / CC BY-SA',
    },
    # 白高大神廃神社 - actual photo of the Shirataka Daimyojin signs at the site
    'spot-026': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/2/2c/%E3%80%8C%E7%99%BD%E9%AB%98%E5%A4%A7%E6%98%8E%E7%A5%9E%E3%80%8D%E3%81%A8%E3%80%8C%E5%A4%A9%E6%B4%A5%E5%BD%A6%E5%A4%A7%E7%A5%9E%E3%80%8D_%E4%BA%94%E6%A2%9D%E5%B8%82%E5%8C%97%E5%B1%B1%E7%94%BA_2013.4.18_-_panoramio.jpg',
        'credit': 'Wikimedia Commons / panoramio contributor / CC BY-SA',
    },
    # 湯の山温泉 - panoramio photo of Yunoyama Onsen resort area
    'spot-020': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/8/80/Yunoyama_onsen_%2C_%E6%B9%AF%E3%81%AE%E5%B1%B1%E6%B8%A9%E6%B3%89_-_panoramio.jpg',
        'credit': 'Wikimedia Commons / panoramio contributor / CC BY-SA',
    },
    # 鍋冠祭 - Edo period painting by Kusumi Morikage showing the Nabekaburi festival
    'fest-023': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/e/e3/%E4%B9%85%E9%9A%85%E5%AE%88%E6%99%AF%E3%80%8A%E9%8D%8B%E5%86%A0%E7%A5%AD%E5%9B%B3%E6%8A%BC%E7%B5%B5%E8%B2%BC%E5%B1%8F%E9%A2%A8%E3%80%8B17%E4%B8%96%E7%B4%80%E3%80%81%E6%B1%9F%E6%88%B8%E6%99%82%E4%BB%A3.jpg',
        'credit': 'Wikimedia Commons / 久隅守景（江戸時代の絵師）/ パブリックドメイン',
    },
    # 潮かけ祭り（大島祭）- 八雲神社（和具）= the Yakumo shrine where the festival starts
    'fest-026': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Wagu_Yakumo_Shrine.jpg',
        'credit': 'Wikimedia Commons / Wikipedia contributor / CC BY-SA',
    },
    # 奥山大権現 虫送り - 方広寺（浜松市）main hall where the festival is held
    'fest-039': {
        'primary': 'https://upload.wikimedia.org/wikipedia/commons/0/06/Hokoji-hondo.jpg',
        'credit': 'Wikimedia Commons / Wikipedia contributor / CC BY-SA',
    },
}

# Apply updates
for key, vals in updates.items():
    if key in photos:
        photos[key]['primary'] = vals['primary']
        photos[key]['credit'] = vals['credit']
        print(f"Updated {key}: {photos[key]['name']}")
    else:
        print(f"Key not found: {key}")

# Count results
null_count = sum(1 for v in photos.values() if v.get('primary') is None)
found_count = sum(1 for v in photos.values() if v.get('primary') is not None)
print(f"\nTotal: {len(photos)} items")
print(f"Found: {found_count}")
print(f"Null: {null_count}")

# Show remaining nulls
print("\nRemaining null items:")
for k, v in photos.items():
    if v.get('primary') is None:
        print(f"  {k}: {v['name']}")

# Save
with open('/home/user/workspace/chinspot-map/photos.json', 'w', encoding='utf-8') as f:
    json.dump(photos, f, ensure_ascii=False, indent=2)
print("\nSaved.")
