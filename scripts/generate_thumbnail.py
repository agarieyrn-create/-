"""
scripts/generate_thumbnail.py
canvas-design Skill 活用 — サムネイルPNG（1280×720）自動生成

使い方:
  python3 scripts/generate_thumbnail.py \
    --title "なんでそらはあおいの？" \
    --theme momo-popo-default \
    --output assets/thumbnails/thumbnail.png
"""
import argparse
import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
THEME_CONFIG = ROOT / "config" / "theme_config.json"
ASSETS_DIR   = ROOT / "assets" / "thumbnails"
CHAR_IMAGES  = {
    "momo": ROOT / "public" / "images" / "momo" / "happy_open.png",
    "popo": ROOT / "public" / "images" / "popo" / "happy_open.png",
}
W, H = 1280, 720


def load_theme(theme_id: str) -> dict:
    with open(THEME_CONFIG) as f:
        cfg = json.load(f)
    return cfg["themes"].get(theme_id, cfg["themes"]["momo-popo-default"])


def get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def generate_thumbnail(title: str, theme_id: str, output_path: str):
    theme = load_theme(theme_id)
    colors = theme["colors"]

    # 背景グラデーション
    bg_start = hex_to_rgb(theme["thumbnail"]["bgGradient"][0])
    bg_end   = hex_to_rgb(theme["thumbnail"]["bgGradient"][1])
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(bg_start[0] + (bg_end[0] - bg_start[0]) * y / H)
        g = int(bg_start[1] + (bg_end[1] - bg_start[1]) * y / H)
        b = int(bg_start[2] + (bg_end[2] - bg_start[2]) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # タイトルテキスト
    title_color = hex_to_rgb(theme["thumbnail"]["titleColor"])
    font_large = get_font(90)
    font_small = get_font(52)

    draw.text((W // 2, H // 2 - 60), title, fill=title_color,
              font=font_large, anchor="mm")
    draw.text((W // 2, H // 2 + 80),
              "ももちゃんとポポの「なんでなに？」",
              fill=hex_to_rgb(theme["thumbnail"]["accentColor"]),
              font=font_small, anchor="mm")

    # キャラクター画像を右下に配置
    char_y = H - 280
    for i, (char_id, char_path) in enumerate(CHAR_IMAGES.items()):
        if char_path.exists():
            char_img = Image.open(char_path).convert("RGBA")
            char_img = char_img.resize((240, 300), Image.LANCZOS)
            cx = W - 280 + i * 130
            img.paste(char_img, (cx, char_y), mask=char_img.split()[3])

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img.save(output_path)
    print(f"✓ Thumbnail saved: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title",  default="なんでそらはあおいの？")
    parser.add_argument("--theme",  default="momo-popo-default")
    parser.add_argument("--output", default=str(ASSETS_DIR / "thumbnail.png"))
    args = parser.parse_args()
    generate_thumbnail(args.title, args.theme, args.output)


if __name__ == "__main__":
    main()
