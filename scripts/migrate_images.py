"""
scripts/migrate_images.py
既存 assets/*.png を public/images/{char}/ に口パク命名規則でコピー・生成する
- assets/momo.png → public/images/momo/mouth_open.png（口開き基本）
- 口を閉じた差分・各表情差分は既存画像を加工して生成
- create-yukkuri-channel の {emotion}_open / {emotion}_close 命名規則に準拠
"""
import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT      = Path(__file__).parent.parent
ASSETS    = ROOT / "assets"
PUB_IMG   = ROOT / "public" / "images"
EMOTIONS  = ["mouth", "happy", "surprise", "thinking", "question"]
CHARS     = ["momo", "popo", "toto"]


def make_mouth_close(img: Image.Image) -> Image.Image:
    """口を閉じたバリエーション: 口元の下半分を上書きして閉じた印象に"""
    result = img.copy()
    w, h = result.size
    draw = ImageDraw.Draw(result)
    # 口の領域（下1/3あたり）を肌色/毛色で塗りつぶして「閉じた」表現
    mouth_y = int(h * 0.62)
    mouth_h = int(h * 0.08)
    # 周囲ピクセルから塗りつぶし色をサンプル
    sample_x = w // 2
    sample_y = mouth_y - 5
    if result.mode == "RGBA":
        fill_color = result.getpixel((sample_x, sample_y))
    else:
        px = result.getpixel((sample_x, sample_y))
        fill_color = px + (255,) if len(px) < 4 else px
    draw.ellipse(
        [w // 2 - 25, mouth_y, w // 2 + 25, mouth_y + mouth_h],
        fill=fill_color,
    )
    return result


def make_emotion_variant(base: Image.Image, emotion: str) -> Image.Image:
    """表情差分を base 画像から簡易生成"""
    result = base.copy()
    if emotion == "happy":
        # 明度を少し上げる
        enhancer = ImageEnhance.Brightness(result.convert("RGBA"))
        result = enhancer.enhance(1.08)
    elif emotion == "surprise":
        # 少し拡大（驚きで目が開く演出）
        w, h = result.size
        zoomed = result.resize((int(w * 1.05), int(h * 1.05)), Image.LANCZOS)
        canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        offset = ((w - zoomed.width) // 2, (h - zoomed.height) // 2)
        canvas.paste(zoomed, offset, mask=zoomed.split()[3] if zoomed.mode == "RGBA" else None)
        result = canvas
    elif emotion == "thinking":
        # 少し暗め（考え込む）
        enhancer = ImageEnhance.Brightness(result.convert("RGBA"))
        result = enhancer.enhance(0.92)
    elif emotion == "question":
        # 明度そのまま・基本と同じ（？表情は通常顔で表現）
        pass
    return result.convert("RGBA")


def process_character(char_id: str):
    src_candidates = [
        ASSETS / f"{char_id}.png",
        ASSETS / f"{char_id}_smile.png",
        ASSETS / f"{char_id}_laugh.png",
    ]
    src = next((p for p in src_candidates if p.exists()), None)
    if src is None:
        print(f"  ⚠ {char_id}: 元画像が見つかりません → スキップ")
        return

    out_dir = PUB_IMG / char_id
    out_dir.mkdir(parents=True, exist_ok=True)

    base = Image.open(src).convert("RGBA")
    print(f"\n▶ {char_id}: {src.name} → {out_dir}")

    for emotion in EMOTIONS:
        # 表情バリエント生成
        emotion_img = make_emotion_variant(base, emotion) if emotion != "mouth" else base.copy().convert("RGBA")
        close_img   = make_mouth_close(emotion_img)

        open_path  = out_dir / f"{emotion}_open.png"
        close_path = out_dir / f"{emotion}_close.png"

        emotion_img.save(open_path)
        close_img.save(close_path)
        print(f"  ✓ {open_path.name}  /  {close_path.name}")


def main():
    PUB_IMG.mkdir(parents=True, exist_ok=True)
    for char_id in CHARS:
        process_character(char_id)
    print("\n✅ 画像移行完了")


if __name__ == "__main__":
    main()
