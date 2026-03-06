"""
子ども向け教育ショート動画ジェネレーター
キャラクター: ももちゃん & ポポ（プードル）
"""
import os
import sys
import textwrap
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip

sys.path.insert(0, str(Path(__file__).parent))
from scripts.video_content import VIDEO_SCRIPTS, CHARACTERS

# ---- 設定 ----
OUTPUT_DIR = "output"
ASSET_DIR = "assets"
VIDEO_W, VIDEO_H = 1080, 1920   # 縦型ショート動画（9:16）
FPS = 24
FONT_SIZE_LARGE = 72
FONT_SIZE_SMALL = 54

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---- フォント ----
def get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_candidates = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in font_candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# ---- シーン画像生成 ----
def make_scene_image(
    scene: dict,
    char_images: dict[str, Image.Image],
) -> np.ndarray:
    """1シーン分のPIL画像をnumpy配列で返す"""
    bg_color = scene["bg_color"]
    img = Image.new("RGB", (VIDEO_W, VIDEO_H), bg_color)
    draw = ImageDraw.Draw(img)

    # ----- 背景デコレーション（シンプルな星・丸） -----
    for i in range(15):
        rng = np.random.default_rng(seed=i * 7 + sum(bg_color))
        x = int(rng.integers(50, VIDEO_W - 50))
        y = int(rng.integers(50, VIDEO_H // 2))
        r = int(rng.integers(10, 40))
        alpha_color = tuple(min(c + 40, 255) for c in bg_color)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=alpha_color)

    # ----- キャラクター配置 -----
    speaker = scene["speaker"]
    char_img = char_images.get(speaker)
    if char_img:
        char_w, char_h = 500, 620
        char_resized = char_img.resize((char_w, char_h), Image.LANCZOS)

        # ももちゃんは左、ポポは右
        if speaker == "momo":
            cx = VIDEO_W // 2 - char_w // 2 - 60
        else:
            cx = VIDEO_W // 2 - char_w // 2 + 60

        cy = VIDEO_H // 2 - char_h // 2 + 80

        if char_resized.mode == "RGBA":
            img.paste(char_resized, (cx, cy), mask=char_resized.split()[3])
        else:
            img.paste(char_resized, (cx, cy))

    # ----- セリフ吹き出し -----
    draw_speech_bubble(draw, scene, speaker)

    return np.array(img)


def draw_speech_bubble(
    draw: ImageDraw.Draw,
    scene: dict,
    speaker: str,
):
    text: str = scene["text"]
    font_large = get_font(FONT_SIZE_LARGE)
    font_small = get_font(FONT_SIZE_SMALL)

    # 吹き出し位置（下部）
    bubble_x1, bubble_y1 = 80, VIDEO_H - 520
    bubble_x2, bubble_y2 = VIDEO_W - 80, VIDEO_H - 60

    # 吹き出し背景
    draw.rounded_rectangle(
        [bubble_x1, bubble_y1, bubble_x2, bubble_y2],
        radius=40,
        fill=(255, 255, 255, 230),
        outline=(255, 160, 180) if speaker == "momo" else (180, 130, 80),
        width=6,
    )

    # キャラクター名
    char_name = CHARACTERS[speaker]["name"]
    name_color = (220, 80, 120) if speaker == "momo" else (160, 100, 40)
    draw.text((bubble_x1 + 30, bubble_y1 + 20), char_name, fill=name_color, font=get_font(48))

    # テキスト（折り返し）
    lines = text.split("\n")
    text_y = bubble_y1 + 90
    for line in lines:
        draw.text(
            (bubble_x1 + 30, text_y),
            line,
            fill=(40, 40, 40),
            font=font_large if len(line) <= 10 else font_small,
        )
        text_y += FONT_SIZE_LARGE + 12

    # タイトルバー（上部）
    title = scene.get("title", "")
    if title:
        draw.text((VIDEO_W // 2, 60), title, fill=(60, 60, 60), font=get_font(52), anchor="mm")


def draw_title_card(title: str, bg_color=(255, 240, 245)) -> np.ndarray:
    """タイトルカード画像を生成"""
    img = Image.new("RGB", (VIDEO_W, VIDEO_H), bg_color)
    draw = ImageDraw.Draw(img)

    font_title = get_font(90)
    font_sub = get_font(54)

    # タイトル中央
    lines = title.split("？")[0]
    draw.text((VIDEO_W // 2, VIDEO_H // 2 - 80), lines + "？", fill=(60, 60, 140),
              font=font_title, anchor="mm")
    draw.text((VIDEO_W // 2, VIDEO_H // 2 + 80), "いっしょに かんがえよう！",
              fill=(180, 80, 120), font=font_sub, anchor="mm")

    # ロゴ
    draw.text((VIDEO_W // 2, VIDEO_H - 120), "ももちゃんと ポポの なんでなに？",
              fill=(140, 100, 180), font=get_font(42), anchor="mm")

    return np.array(img)


# ---- 動画生成 ----
def generate_video(script: dict, char_images: dict) -> str:
    clips = []

    # タイトルカード（2秒）
    title_arr = draw_title_card(script["title"])
    clips.append(ImageClip(title_arr, duration=2))

    # 各シーン
    for scene in script["scenes"]:
        scene_arr = make_scene_image(scene, char_images)
        clips.append(ImageClip(scene_arr, duration=scene["duration"]))

    # エンドカード（2秒）
    end_arr = draw_title_card("また みてね！", bg_color=(220, 255, 230))
    clips.append(ImageClip(end_arr, duration=2))

    final = concatenate_videoclips(clips)

    out_path = os.path.join(OUTPUT_DIR, f"{script['id']}.mp4")
    final.write_videofile(out_path, fps=FPS, codec="libx264", audio=False, logger=None)
    print(f"✓ Generated: {out_path}")
    return out_path


def load_char_images() -> dict[str, Image.Image]:
    """アセット画像を読み込む（なければプレースホルダーを使用）"""
    images = {}
    for char_id, char_info in CHARACTERS.items():
        path = char_info["image"]
        if os.path.exists(path):
            images[char_id] = Image.open(path).convert("RGBA")
            print(f"✓ Loaded character: {path}")
        else:
            print(f"  Character image not found ({path}), using placeholder")
            images[char_id] = None
    return images


def main():
    print("=" * 50)
    print("  ももちゃんとポポの なんでなに？ 動画ジェネレーター")
    print("=" * 50)

    char_images = load_char_images()

    generated = []
    for script in VIDEO_SCRIPTS:
        print(f"\n▶ 作成中: 「{script['title']}」")
        path = generate_video(script, char_images)
        generated.append(path)

    print("\n" + "=" * 50)
    print("  完成した動画:")
    for p in generated:
        print(f"  - {p}")
    print("=" * 50)


if __name__ == "__main__":
    main()
