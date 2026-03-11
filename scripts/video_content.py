"""
【改善版】なんでそらはあおいの？ 台本
対象: 小学生（7歳以上）
変更点:
  - オープニング・エンディング追加
  - ももちゃんのセリフを子どもらしく修正
  - 1シーンの情報量を削減
  - 感情リアクション（驚き・笑い）を強化
  - ポポの説明をステップごとに分割
"""

CHARACTERS = {
    "momo": {
        "name": "ももちゃん",
        "color": (255, 182, 193),
        "image": "assets/momo.png",
        "role": "question_asker",
    },
    "popo": {
        "name": "ポポ",
        "color": (205, 133, 63),
        "image": "assets/popo.png",
        "role": "answerer",
    },
}

VIDEO_SCRIPTS = [
    {
        "id": "why_sky_blue",
        "title": "なんでそらはあおいの？",
        "duration_sec": 35,
        "scenes": [
            # ① オープニング
            {
                "speaker": "momo",
                "text": "ねえポポ！\nきょうも「なんで？」\nしらべちゃおう！",
                "bg_color": (135, 206, 235),
                "duration": 3,
                "animation": "bounce",
            },
            # ② 質問
            {
                "speaker": "momo",
                "text": "ポポ〜！\nそらって なんで\nあおいの？",
                "bg_color": (135, 206, 235),
                "duration": 4,
                "animation": "bounce",
            },
            # ③ ポポ反応
            {
                "speaker": "popo",
                "text": "おっ！\nいい「なんで？」だワン！\nいっしょに かんがえよう！",
                "bg_color": (255, 255, 200),
                "duration": 4,
                "animation": "wave",
            },
            # ④ 説明①：太陽の光
            {
                "speaker": "popo",
                "text": "たいようの ひかりには\nにじの いろが\nぜんぶ はいってるんだ！",
                "bg_color": (255, 255, 200),
                "duration": 5,
                "animation": "explain",
            },
            # ⑤ ももリアクション
            {
                "speaker": "momo",
                "text": "えっ！しろい ひかりに\nいろが かくれてるの？\nしらなかった〜！",
                "bg_color": (255, 240, 200),
                "duration": 4,
                "animation": "surprised",
            },
            # ⑥ 説明②：空気と青い光
            {
                "speaker": "popo",
                "text": "そらの くうきが\nあおい ひかりだけを\nはじいて ちらすんだ！",
                "bg_color": (135, 206, 235),
                "duration": 5,
                "animation": "explain",
            },
            # ⑦ 説明③：夕焼け
            {
                "speaker": "popo",
                "text": "ゆうやけが オレンジなのは\nひかりが とおくを とおって\nあかい いろだけ のこるから！",
                "bg_color": (255, 160, 60),
                "duration": 6,
                "animation": "wave",
            },
            # ⑧ ももまとめリアクション
            {
                "speaker": "momo",
                "text": "そっかー！\nひかりって\nすごいんだね！",
                "bg_color": (135, 206, 235),
                "duration": 4,
                "animation": "happy",
            },
            # ⑨ エンディング
            {
                "speaker": "popo",
                "text": "またいっしょに\n「なんで？」\nさがそうね！だワン♪",
                "bg_color": (200, 240, 255),
                "duration": 4,
                "animation": "wave",
            },
        ],
    },
]
