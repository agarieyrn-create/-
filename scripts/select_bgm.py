"""
scripts/select_bgm.py
script.ts の bgm_type をもとに BGM ファイルをアサインし
public/bgm/background.mp3 にコピーする

使い方:
  python3 scripts/select_bgm.py --type upbeat
"""
import argparse
import json
import shutil
from pathlib import Path

ROOT         = Path(__file__).parent.parent
BGM_MAP_PATH = ROOT / "config" / "bgm_map.json"
BGM_DIR      = ROOT / "public" / "bgm"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", default="upbeat")
    args = parser.parse_args()

    with open(BGM_MAP_PATH) as f:
        bgm_map = json.load(f)

    entry = bgm_map["bgm"].get(args.type) or bgm_map["bgm"][bgm_map["default"]["bgm_type"]]
    if not entry["file"]:
        print(f"BGM type '{args.type}' はBGMなし設定です。")
        return

    src = BGM_DIR / entry["file"]
    dst = BGM_DIR / "background.mp3"

    if not src.exists():
        print(f"⚠ BGMファイルが見つかりません: {src}")
        print(f"  → public/bgm/ に {entry['file']} を配置してください")
        return

    shutil.copy2(src, dst)
    print(f"✓ BGM set: {entry['file']} (volume: {entry['volume']}) → background.mp3")


if __name__ == "__main__":
    main()
