# ももちゃんとポポの「なんでなに？」動画ジェネレーター

子どもの「なんで？」を解決する縦型教育ショート動画を自動生成するツールです。

## キャラクター

| キャラクター | 役割 | 説明 |
|---|---|---|
| **ももちゃん** | 質問する子 | ピンクのパーカーを着た元気な女の子 |
| **ポポ** | 答える子 | さくらんぼ柄のバンダナをしたプードル |

## 収録コンテンツ（動画3本）

1. **なんでそらはあおいの？** — レイリー散乱・夕焼けのしくみ
2. **なんでにじはでるの？** — 光の屈折・虹の7色
3. **なんできせつがかわるの？** — 地球の公転・地軸の傾き

## ファイル構成

```
.
├── assets/               # キャラクター画像
│   ├── momo.png          # ももちゃん
│   └── popo.png          # ポポ
├── scripts/
│   └── video_content.py  # 動画台本・コンテンツ定義
├── output/               # 生成動画（MP4）
├── create_character_assets.py   # キャラクター画像生成
├── generate_videos.py    # メイン動画生成スクリプト
└── save_uploaded_images.py      # 外部画像を取り込む場合
```

## 使い方

### セットアップ
```bash
pip install Pillow moviepy numpy
```

### キャラクター画像の準備

アップロード画像を使う場合:
```bash
python save_uploaded_images.py <プードル画像> <女の子画像>
```

自動生成キャラクターを使う場合:
```bash
python create_character_assets.py
```

### 動画生成
```bash
python generate_videos.py
```

生成された動画は `output/` フォルダに MP4 形式で保存されます。

## 動画仕様

- 解像度: **1080×1920px**（縦型・TikTok/Reels/YouTube Shorts対応）
- FPS: 24
- 1動画あたり: **約30秒**
- コーデック: H.264（音声なし）

## 新しい「なんで？」を追加するには

`scripts/video_content.py` の `VIDEO_SCRIPTS` リストに辞書を追加するだけです：

```python
{
    "id": "why_xxx",
    "title": "なんで○○なの？",
    "duration_sec": 30,
    "scenes": [
        {
            "speaker": "momo",   # または "popo"
            "text": "セリフをここに書く",
            "bg_color": (R, G, B),
            "duration": 5,       # 秒数
            "animation": "bounce",
        },
        ...
    ],
}
```
