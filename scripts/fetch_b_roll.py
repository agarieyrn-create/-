"""
scripts/fetch_b_roll.py
script.ts の b_roll_keyword をもとに Pixabay / Pexels から動画を取得し
assets/b_roll_cache/ に保存する。取得失敗時は GIF フォールバックに切り替える。

使い方:
  python3 scripts/fetch_b_roll.py
  PIXABAY_API_KEY=xxx python3 scripts/fetch_b_roll.py
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

ROOT       = Path(__file__).parent.parent
CACHE_DIR  = ROOT / "assets" / "b_roll_cache"
SCRIPT_PATH = ROOT / "src" / "data" / "script.ts"
PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY", "")
PEXELS_API_KEY  = os.environ.get("PEXELS_API_KEY", "")


def extract_keywords(script_ts: str) -> list[str]:
    """script.ts から b_roll_keyword フィールドを抽出"""
    return list(set(re.findall(r"b_roll_keyword:\s*'([^']+)'", script_ts)))


def fetch_from_pixabay(keyword: str) -> str | None:
    if not PIXABAY_API_KEY:
        return None
    url = "https://pixabay.com/api/videos/"
    r = requests.get(url, params={
        "key": PIXABAY_API_KEY, "q": keyword,
        "video_type": "film", "per_page": 3,
    }, timeout=10)
    hits = r.json().get("hits", [])
    if hits:
        return hits[0]["videos"]["medium"]["url"]
    return None


def fetch_from_pexels(keyword: str) -> str | None:
    if not PEXELS_API_KEY:
        return None
    r = requests.get(
        "https://api.pexels.com/videos/search",
        headers={"Authorization": PEXELS_API_KEY},
        params={"query": keyword, "per_page": 1},
        timeout=10,
    )
    videos = r.json().get("videos", [])
    if videos:
        files = videos[0].get("video_files", [])
        mp4_files = [f for f in files if f.get("file_type") == "video/mp4"]
        if mp4_files:
            return sorted(mp4_files, key=lambda f: f.get("width", 0))[0]["link"]
    return None


def download_video(url: str, dest: Path):
    r = requests.get(url, stream=True, timeout=30)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"  ✓ Downloaded: {dest.name}")


def main():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    script_src = SCRIPT_PATH.read_text(encoding="utf-8")
    keywords = extract_keywords(script_src)

    if not keywords:
        print("b_roll_keyword が見つかりませんでした。")
        return

    for kw in keywords:
        safe_name = kw.replace(" ", "_") + ".mp4"
        dest = CACHE_DIR / safe_name
        if dest.exists():
            print(f"  ✓ Cache hit: {safe_name}")
            continue
        print(f"▶ Fetching: '{kw}'")
        video_url = fetch_from_pixabay(kw) or fetch_from_pexels(kw)
        if video_url:
            download_video(video_url, dest)
        else:
            print(f"  ⚠ Not found (API key 未設定 or 結果なし) → GIFフォールバック推奨")
            print(f"    → python3 scripts/generate_reaction_gif.py --keyword '{kw}'")


if __name__ == "__main__":
    main()
