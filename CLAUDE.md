# CLAUDE.md — なぜ？なに？動画自動生成システム v2.2

## プロジェクト概要
create-yukkuri-channel ワークフロー統合版。
ももちゃん・ポポ・トトが子どもの「なんで？」を解説する縦型ショート動画を自動生成する。

## キャラクター
| ID   | 名前       | VOICEVOX speaker ID | 語尾           |
|------|-----------|---------------------|---------------|
| momo | ももちゃん | 3                   | 〜だよ！〜かな？ |
| popo | ポポ       | 1                   | 〜ワン！        |
| toto | トト       | 8                   | 〜だね、〜かな  |

## よく使うコマンド
```bash
npm start              # プレビュー (localhost:3000)
npm run voices         # VOICEVOX音声生成
npm run build          # 動画出力 → out/video.mp4
npm run editor         # GUIエディター (localhost:3001/3002)
npm run sync-settings  # YAML設定をconfig.tsに反映
npm run thumbnail      # サムネイル生成
```

## 台本を書くときのルール
1. `src/data/script.ts` の `scriptData` 配列に ScriptLine を追加する
2. `text` は **カタカナ優先**（VOICEVOXが英語を正しく発音できないため）
3. `displayText` に字幕用テキスト（英語表記など）を入れる
4. セリフを書いたら必ず `npm run voices` を実行して音声ファイルを更新する

## セリフ修正（API経由・token節約）
```
PUT http://localhost:3002/api/script/{id}
{ "text": "新しいセリフだよ！", "emotion": "happy" }
```

## よくある発音修正
| 表示          | text（音声用）       |
|---------------|---------------------|
| YouTube       | ユーチューブ         |
| AI            | エーアイ             |
| Google        | グーグル             |
| 100km         | ひゃくキロメートル   |

## durationInFrames 計算式
```
durationInFrames = 音声の秒数 × 30 × 1.2
例: 2.5秒 → 2.5 × 30 × 1.2 = 90フレーム
```
→ `npm run voices` 実行後は自動更新される。手動設定時は上記計算式を使う。

## 表情ファイル命名規則
```
public/images/{character}/
├── mouth_open.png      # 通常・口開き（必須）
├── mouth_close.png     # 通常・口閉じ（必須）
├── happy_open.png
├── happy_close.png
├── surprise_open.png
├── surprise_close.png
├── thinking_open.png
├── thinking_close.png
├── question_open.png
└── question_close.png
```
表情差分がない場合は mouth_open/close に自動フォールバックする。

## トラブルシューティング
| エラー                   | 原因                    | 対処                           |
|--------------------------|-------------------------|-------------------------------|
| ECONNREFUSED port 50021  | VOICEVOX未起動          | VOICEVOXアプリを起動してから実行 |
| 音声と字幕がずれる        | durationInFramesが古い  | `npm run voices` を再実行      |
| キャラ画像が出ない        | useImages:false / パス違い | video-settings.yaml を確認   |
| 英語の発音がおかしい      | textに英語が混入        | textをカタカナに変換            |
