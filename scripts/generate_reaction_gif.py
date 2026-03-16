"""
scripts/generate_reaction_gif.py
slack-gif-creator Skill 活用 — キャラクターリアクションGIF生成
Bロール取得失敗時のフォールバックとして使用

使い方:
  python3 scripts/generate_reaction_gif.py --character popo --emotion happy
  python3 scripts/generate_reaction_gif.py --keyword "blue sky children"
"""
import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw

ROOT     = Path(__file__).parent.parent
GIF_DIR  = ROOT / "assets" / "reaction_gifs"
CHAR_DIR = ROOT / "public" / "images"


def generate_bounce_gif(
    char_img: Image.Image,
    output_path: Path,
    frames: int = 12,
    bounce_height: int = 20,
):
    """キャラクターがバウンスするGIFを生成"""
    gif_frames = []
    W, H = 400, 450
    for i in range(frames):
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        offset_y = int(bounce_height * abs((i % frames) / (frames // 2) - 1))
        resized = char_img.resize((320, 380), Image.LANCZOS)
        frame.paste(resized, (40, offset_y), mask=resized.split()[3])
        gif_frames.append(frame.convert("RGBA"))

    gif_frames[0].save(
        output_path,
        save_all=True,
        append_images=gif_frames[1:],
        loop=0,
        duration=80,  # ms per frame
        optimize=True,
    )
    print(f"✓ GIF saved: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--character", default="popo", choices=["momo", "popo", "toto"])
    parser.add_argument("--emotion",   default="happy")
    parser.add_argument("--keyword",   default=None, help="Bロール検索キーワード（フォールバック時）")
    args = parser.parse_args()

    GIF_DIR.mkdir(parents=True, exist_ok=True)

    # キャラクター画像を読み込む（mouth_open → emotion_open → フォールバック）
    char_path_candidates = [
        CHAR_DIR / args.character / f"{args.emotion}_open.png",
        CHAR_DIR / args.character / "mouth_open.png",
        ROOT / "assets" / f"{args.character}.png",
    ]
    char_img = None
    for p in char_path_candidates:
        if p.exists():
            char_img = Image.open(p).convert("RGBA")
            break

    if char_img is None:
        print(f"⚠ キャラクター画像が見つかりません: {args.character}")
        return

    suffix = args.keyword.replace(" ", "_") if args.keyword else args.emotion
    output_path = GIF_DIR / f"{args.character}_{suffix}.gif"
    generate_bounce_gif(char_img, output_path)


if __name__ == "__main__":
    main()
