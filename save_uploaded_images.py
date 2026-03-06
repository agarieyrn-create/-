"""
アップロードされた画像をアセットとして保存するスクリプト
使い方: python save_uploaded_images.py <popo_image_path> <momo_image_path>
"""
import sys
import os
from PIL import Image

ASSET_DIR = "assets"
os.makedirs(ASSET_DIR, exist_ok=True)


def save_asset(src_path: str, dest_name: str):
    img = Image.open(src_path).convert("RGBA")
    dest = os.path.join(ASSET_DIR, dest_name)
    img.save(dest)
    print(f"✓ Saved {src_path} -> {dest}")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        save_asset(sys.argv[1], "popo.png")   # プードル
        save_asset(sys.argv[2], "momo.png")   # 女の子
    else:
        print("Usage: python save_uploaded_images.py <popo_image> <momo_image>")
        print("Generating placeholder assets instead...")
        from create_assets import save_character_images
        save_character_images()
