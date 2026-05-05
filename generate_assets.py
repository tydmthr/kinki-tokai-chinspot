#!/usr/bin/env python3
"""
bizarrejapan.com OGP画像・favicon生成スクリプト
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ===== カラーパレット =====
BLACK_URUSHI = (10, 8, 8)        # #0a0808 黒漆
SHU = (200, 51, 43)              # #c8332b 朱
KOGANE = (212, 164, 55)          # #d4a437 古金
SUMI_WHITE = (245, 241, 234)     # #f5f1ea 墨白
DARK_RED = (140, 20, 15)         # 暗い朱（装飾用）
LIGHT_KOGANE = (240, 200, 100)   # 明るい金（ハイライト）

# ===== フォントパス =====
SERIF_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SERIF_REG  = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
SANS_BOLD  = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
DEJAVU     = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

OUTPUT_DIR = "/home/user/workspace/chinspot-map"


def load_font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def draw_seigaiha(draw, width, height, color, alpha=40, scale=1.0):
    """青海波（うろこ波）パターンを描画"""
    r = int(30 * scale)
    cols = width // r + 2
    rows = height // r + 2
    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            x = col * r * 2
            if row % 2 == 1:
                x += r
            y = row * r
            # 半円（上向き）
            draw.arc(
                [x - r, y - r, x + r, y + r],
                start=180, end=360,
                fill=(*color, alpha), width=1
            )
            draw.arc(
                [x - int(r * 0.7), y - int(r * 0.35), x + int(r * 0.7), y + int(r * 0.65)],
                start=180, end=360,
                fill=(*color, alpha // 2), width=1
            )


def draw_hemp_leaf(draw, cx, cy, size, color, alpha=30):
    """麻の葉文様の六角星を描画（簡略版）"""
    for i in range(6):
        angle = math.radians(i * 60)
        x1 = cx + math.cos(angle) * size
        y1 = cy + math.sin(angle) * size
        draw.line([cx, cy, x1, y1], fill=(*color, alpha), width=1)
    for i in range(6):
        a1 = math.radians(i * 60)
        a2 = math.radians((i + 2) * 60)
        x1 = cx + math.cos(a1) * size
        y1 = cy + math.sin(a1) * size
        x2 = cx + math.cos(a2) * size
        y2 = cy + math.sin(a2) * size
        draw.line([x1, y1, x2, y2], fill=(*color, alpha), width=1)


def draw_torii_silhouette(img, x, y, size, color):
    """鳥居シルエットを描画（RGBA画像に合成）"""
    draw = ImageDraw.Draw(img)
    s = size
    # 笠木（上の横棒・反り付き）
    draw.rectangle([x - s, y, x + s, y + int(s * 0.12)], fill=color)
    # 島木（笠木の下の横棒）
    draw.rectangle([x - int(s * 0.85), y + int(s * 0.16), x + int(s * 0.85), y + int(s * 0.26)], fill=color)
    # 柱（2本）
    pillar_w = int(s * 0.1)
    pillar_h = int(s * 1.0)
    draw.rectangle([x - int(s * 0.72), y + int(s * 0.26), x - int(s * 0.62), y + int(s * 1.26)], fill=color)
    draw.rectangle([x + int(s * 0.62), y + int(s * 0.26), x + int(s * 0.72), y + int(s * 1.26)], fill=color)
    # 貫（中央横木）
    draw.rectangle([x - int(s * 0.78), y + int(s * 0.55), x + int(s * 0.78), y + int(s * 0.65)], fill=color)
    # 笠木の反り（三角形で上端をカーブ風に）
    draw.polygon([
        (x - s, y),
        (x + s, y),
        (x, y - int(s * 0.15))
    ], fill=color)


def create_gradient_bg(width, height):
    """黒漆から深い赤へのグラデーション背景"""
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / height
        r = int(BLACK_URUSHI[0] + (30 - BLACK_URUSHI[0]) * ratio * 0.4)
        g = int(BLACK_URUSHI[1] + (5 - BLACK_URUSHI[1]) * ratio * 0.3)
        b = int(BLACK_URUSHI[2] + (5 - BLACK_URUSHI[2]) * ratio * 0.3)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    return img


def add_vignette(img):
    """周囲を暗くするビネット効果"""
    w, h = img.size
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vignette)
    steps = 60
    for i in range(steps):
        alpha = int(180 * (i / steps) ** 2)
        margin = i * 4
        draw.rectangle([margin, margin, w - margin, h - margin],
                        outline=(0, 0, 0, alpha), width=4)
    img = Image.alpha_composite(img, vignette)
    return img


def create_og_image():
    """OGP画像 1200x630px を生成"""
    W, H = 1200, 630
    img = create_gradient_bg(W, H)
    draw = ImageDraw.Draw(img, "RGBA")

    # ===== 青海波パターン（薄く透かし）=====
    seigaiha_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seigaiha_layer, "RGBA")
    r = 28
    for row in range(-1, H // r + 3):
        for col in range(-1, W // (r * 2) + 3):
            x = col * r * 2
            if row % 2 == 1:
                x += r
            y = row * r
            # 大きな半円
            sd.arc([x - r, y - r, x + r, y + r], 180, 360, fill=(200, 51, 43, 25), width=1)
            # 内側の半円
            ri = int(r * 0.65)
            sd.arc([x - ri, y - int(ri * 0.3), x + ri, y + int(ri * 0.8)], 180, 360, fill=(200, 51, 43, 15), width=1)
    img = Image.alpha_composite(img, seigaiha_layer)
    draw = ImageDraw.Draw(img, "RGBA")

    # ===== 左端の縦線装飾 =====
    for i, x_pos in enumerate([18, 22, 26]):
        alpha = [120, 80, 50][i]
        draw.line([(x_pos, 0), (x_pos, H)], fill=(*KOGANE, alpha), width=1)

    # ===== 右端の縦線装飾 =====
    for i, x_pos in enumerate([W - 18, W - 22, W - 26]):
        alpha = [120, 80, 50][i]
        draw.line([(x_pos, 0), (x_pos, H)], fill=(*KOGANE, alpha), width=1)

    # ===== 上下の横線装飾 =====
    draw.line([(30, 20), (W - 30, 20)], fill=(*KOGANE, 150), width=1)
    draw.line([(30, 24), (W - 30, 24)], fill=(*KOGANE, 80), width=1)
    draw.line([(30, H - 20), (W - 30, H - 20)], fill=(*KOGANE, 150), width=1)
    draw.line([(30, H - 24), (W - 30, H - 24)], fill=(*KOGANE, 80), width=1)

    # ===== 鳥居シルエット（右側、大きく薄く）=====
    torii_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_torii_silhouette(torii_layer, W - 160, 80, 130, (*SHU, 45))
    img = Image.alpha_composite(img, torii_layer)
    draw = ImageDraw.Draw(img, "RGBA")

    # ===== 「鬼」字（右上に大きく薄く装飾）=====
    font_oni_deco = load_font(SERIF_BOLD, 280)
    oni_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    oni_draw = ImageDraw.Draw(oni_layer)
    try:
        bbox = font_oni_deco.getbbox("鬼")
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except Exception:
        tw, th = 200, 200
    oni_draw.text((W - tw - 30, H - th - 10), "鬼", font=font_oni_deco, fill=(*SHU, 30))
    img = Image.alpha_composite(img, oni_layer)
    draw = ImageDraw.Draw(img, "RGBA")

    # ===== 朱の横帯（タイトル背景）=====
    draw.rectangle([40, 155, W - 40, 165], fill=(*SHU, 200))

    # ===== メインタイトル「異界巡礼」=====
    font_title = load_font(SERIF_BOLD, 128)
    title = "異界巡礼"
    try:
        bbox = font_title.getbbox(title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except Exception:
        tw, th = 512, 120
    tx = (W - tw) // 2
    ty = 170

    # 影
    draw.text((tx + 4, ty + 4), title, font=font_title, fill=(0, 0, 0, 160))
    # 本文（墨白）
    draw.text((tx, ty), title, font=font_title, fill=SUMI_WHITE)

    # ===== 副題「近畿・東海 珍スポット50＆奇祭47」=====
    font_sub = load_font(SERIF_BOLD, 44)
    subtitle = "近畿・東海  珍スポット50 ＆ 奇祭47"
    try:
        bbox = font_sub.getbbox(subtitle)
        sw = bbox[2] - bbox[0]
    except Exception:
        sw = 700
    sx = (W - sw) // 2
    sy = ty + th + 20

    # 副題の背景（薄い黒）
    draw.rectangle([sx - 20, sy - 8, sx + sw + 20, sy + 52], fill=(0, 0, 0, 100))
    draw.text((sx, sy), subtitle, font=font_sub, fill=(*KOGANE, 230))

    # ===== 区切り線 =====
    line_y = sy + 72
    draw.line([(W // 2 - 200, line_y), (W // 2 + 200, line_y)], fill=(*KOGANE, 150), width=1)
    draw.ellipse([W // 2 - 5, line_y - 4, W // 2 + 5, line_y + 4], fill=(*SHU, 200))

    # ===== 英語サブタイトル "Bizarre Japan" =====
    font_en_title = load_font(DEJAVU, 52)
    en_title = "Bizarre Japan"
    try:
        bbox = font_en_title.getbbox(en_title)
        etw = bbox[2] - bbox[0]
    except Exception:
        etw = 400
    etx = (W - etw) // 2
    ety = line_y + 15

    draw.text((etx + 2, ety + 2), en_title, font=font_en_title, fill=(0, 0, 0, 140))
    draw.text((etx, ety), en_title, font=font_en_title, fill=SUMI_WHITE)

    # ===== 英語副題 =====
    font_en_sub = load_font(DEJAVU, 22)
    en_sub = "Strange Spots & Wild Festivals of Kinki & Tokai"
    try:
        bbox = font_en_sub.getbbox(en_sub)
        esw = bbox[2] - bbox[0]
    except Exception:
        esw = 500
    esx = (W - esw) // 2
    esy = ety + 62
    draw.text((esx, esy), en_sub, font=font_en_sub, fill=(*SUMI_WHITE, 180))

    # ===== URL "bizarrejapan.com" =====
    font_url = load_font(DEJAVU, 28)
    url_text = "bizarrejapan.com"
    try:
        bbox = font_url.getbbox(url_text)
        uw = bbox[2] - bbox[0]
    except Exception:
        uw = 280
    ux = (W - uw) // 2
    uy = H - 55

    draw.text((ux + 2, uy + 2), url_text, font=font_url, fill=(0, 0, 0, 130))
    draw.text((ux, uy), url_text, font=font_url, fill=KOGANE)

    # ===== ドット装飾（URL両端）=====
    dot_margin = 40
    draw.ellipse([ux - dot_margin - 6, uy + 8, ux - dot_margin + 6, uy + 20], fill=(*SHU, 200))
    draw.ellipse([ux + uw + dot_margin - 6, uy + 8, ux + uw + dot_margin + 6, uy + 20], fill=(*SHU, 200))

    # ===== ビネット =====
    img = add_vignette(img)

    # ===== 保存 =====
    final = img.convert("RGB")
    out_path = os.path.join(OUTPUT_DIR, "og-image.png")
    final.save(out_path, "PNG", optimize=True)
    print(f"Saved: {out_path} ({final.size})")
    return out_path


def create_favicon(size, filename):
    """favicon生成（朱地に金の「鬼」字）"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    # 円形マスク
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    margin = max(1, size // 16)
    mask_draw.ellipse([margin, margin, size - margin, size - margin], fill=255)

    # 背景（朱）
    bg = Image.new("RGBA", (size, size), (*SHU, 255))
    img = Image.composite(bg, img, mask)
    draw = ImageDraw.Draw(img, "RGBA")

    # 内側の円（黒）
    inner_margin = size // 8
    draw.ellipse(
        [inner_margin, inner_margin, size - inner_margin, size - inner_margin],
        outline=(*BLACK_URUSHI, 200), width=max(1, size // 24)
    )

    # 外側のリング（金）
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        outline=(*KOGANE, 220), width=max(1, size // 20)
    )

    # 「鬼」字
    font_size = int(size * 0.62)
    font_oni = load_font(SERIF_BOLD, font_size)
    char = "鬼"
    try:
        bbox = font_oni.getbbox(char)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = (size - tw) // 2 - bbox[0]
        ty = (size - th) // 2 - bbox[1]
    except Exception:
        tx = size // 4
        ty = size // 4

    # 影
    shadow_offset = max(1, size // 32)
    draw.text((tx + shadow_offset, ty + shadow_offset), char, font=font_oni, fill=(0, 0, 0, 120))
    # 本文（古金）
    draw.text((tx, ty), char, font=font_oni, fill=(*KOGANE, 255))

    # RGBAのまま保存（PNG）
    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path, "PNG", optimize=True)
    print(f"Saved: {out_path} ({img.size})")
    return out_path


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== OGP画像生成中... ===")
    create_og_image()

    print("\n=== favicon-32.png 生成中... ===")
    create_favicon(32, "favicon-32.png")

    print("\n=== favicon-180.png 生成中... ===")
    create_favicon(180, "favicon-180.png")

    print("\n=== favicon.png (32x32) 生成中... ===")
    create_favicon(32, "favicon.png")

    print("\n=== 完了！ファイル一覧 ===")
    for fname in ["og-image.png", "favicon.png", "favicon-32.png", "favicon-180.png"]:
        fpath = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            with Image.open(fpath) as im:
                dims = im.size
            print(f"  {fname}: {dims[0]}x{dims[1]}px, {size:,} bytes")


if __name__ == "__main__":
    main()
