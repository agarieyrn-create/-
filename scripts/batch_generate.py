"""
scripts/batch_generate.py
複数トピックを一括で動画生成するバッチ処理
Google Sheets からトピックリストを取得し、順番に処理する（量産モード）

使い方:
  python3 scripts/batch_generate.py --topics "なんで空は青い？,なんで虹ができる？"
  python3 scripts/batch_generate.py --from-file topics.txt
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def run(cmd: list[str], check: bool = True):
    print(f"\n  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if check and result.returncode != 0:
        print(f"  ✗ Failed (exit={result.returncode})")
        return False
    return True


def process_topic(topic: str, index: int):
    print(f"\n{'='*50}")
    print(f"  [{index}] {topic}")
    print(f"{'='*50}")

    # 1. サムネイル生成
    run([
        sys.executable, "scripts/generate_thumbnail.py",
        "--title", topic,
        "--output", f"assets/thumbnails/thumbnail_{index:02d}.png",
    ], check=False)

    # 2. Bロール取得
    run([sys.executable, "scripts/fetch_b_roll.py"], check=False)

    # 3. 音声生成
    run(["npm", "run", "voices"], check=False)

    # 4. 動画ビルド
    run(["npm", "run", "build"])

    # 5. 完成動画をリネーム
    src = ROOT / "out" / "video.mp4"
    dst = ROOT / "assets" / "exports" / f"video_{index:02d}_{topic[:20].replace(' ', '_')}.mp4"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        import shutil
        shutil.copy2(src, dst)
        print(f"\n  ✓ Saved: {dst.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics",    default=None, help="カンマ区切りのトピックリスト")
    parser.add_argument("--from-file", default=None, help="1行1トピックのテキストファイル")
    args = parser.parse_args()

    topics: list[str] = []
    if args.topics:
        topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    elif args.from_file:
        with open(args.from_file) as f:
            topics = [line.strip() for line in f if line.strip()]
    else:
        print("Usage: --topics か --from-file を指定してください")
        return

    print(f"▶ {len(topics)} トピックを処理します")
    for i, topic in enumerate(topics, start=1):
        process_topic(topic, i)

    print(f"\n✅ バッチ処理完了: {len(topics)} 本生成")


if __name__ == "__main__":
    main()
