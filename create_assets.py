"""
キャラクター画像の作成（アップロード画像からアセットを生成）
"""
import os
from PIL import Image, ImageDraw, ImageFont

ASSET_DIR = "assets"
os.makedirs(ASSET_DIR, exist_ok=True)


def create_placeholder_character(name: str, color: tuple, size=(400, 500)) -> Image.Image:
    """キャラクタープレースホルダー画像を作成"""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    w, h = size
    # 体（楕円）
    draw.ellipse([w//4, h//3, 3*w//4, 4*h//5], fill=color + (255,))
    # 頭（円）
    draw.ellipse([w//5, h//10, 4*w//5, h//2], fill=color + (255,))
    # 目
    eye_y = h // 3
    draw.ellipse([w//3 - 15, eye_y - 15, w//3 + 15, eye_y + 15], fill=(50, 30, 20, 255))
    draw.ellipse([2*w//3 - 15, eye_y - 15, 2*w//3 + 15, eye_y + 15], fill=(50, 30, 20, 255))
    # 笑顔
    draw.arc([w//3, eye_y + 10, 2*w//3, eye_y + 50], 0, 180, fill=(200, 50, 50, 255), width=5)

    return img


def save_character_images():
    # ももちゃん（ピンク系）
    momo = create_placeholder_character("momo", (255, 182, 193))
    momo.save(os.path.join(ASSET_DIR, "momo.png"))
    print("✓ momo.png saved")

    # ポポ（茶色系）
    popo = create_placeholder_character("popo", (180, 120, 60))
    popo.save(os.path.join(ASSET_DIR, "popo.png"))
    print("✓ popo.png saved")


if __name__ == "__main__":
    save_character_images()
    print("Assets created successfully!")
