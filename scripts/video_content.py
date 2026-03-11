"""
子ども向けショート動画コンテンツ定義
キャラクター: ももちゃん（女の子）・ポポ（プードル犬）・トト（男の子）
テーマ: 子どもの「なんで？」を解決する教育コンテンツ
"""

CHARACTERS = {
    "momo": {
        "name": "ももちゃん",
        "color": (255, 182, 193),       # ピンク
        "image": "assets/momo.png",
        "role": "question_asker",
        "catchphrase": "〜なの！？",     # 語尾
    },
    "popo": {
        "name": "ポポ",
        "color": (205, 133, 63),         # 茶色
        "image": "assets/popo.png",
        "role": "answerer",
        "catchphrase": "〜だワン！",     # 語尾
    },
    "toto": {
        "name": "トト",
        "color": (135, 185, 220),        # 水色（パーカーの色）
        "image": "assets/toto.png",
        "role": "question_asker",
        "catchphrase": "〜なの？",       # 語尾
        "description": "水色パーカー・りんごマーク・カーゴショーツ・元気な男の子",
    },
}

# ================================================================
# 動画台本
# 登場キャラは動画ごとに自由に組み合わせOK
# speaker: "momo" / "popo" / "toto"
# expression: "smile" / "surprise" / "dislike" / "curious" / "think"
# ================================================================

VIDEO_SCRIPTS = [
    # ----------------------------------------
    # 動画①：ももちゃん＋ポポ
    # ----------------------------------------
    {
        "id": "why_sky_blue",
        "title": "なんでそらはあおいの？",
        "characters": ["momo", "popo"],   # この動画の登場キャラ
        "duration_sec": 35,
        "scenes": [
            {
                "speaker": "momo",
                "expression": "smile",
                "text": "ねえポポ！\nきょうも「なんで？」\nしらべちゃおう！",
                "bg_color": (135, 206, 235),
                "duration": 3,
                "animation": "bounce",
            },
            {
                "speaker": "momo",
                "expression": "curious",
                "text": "ポポ〜！\nそらって なんで\nあおいの？",
                "bg_color": (135, 206, 235),
                "duration": 4,
                "animation": "bounce",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "おっ！\nいい「なんで？」だワン！\nいっしょに かんがえよう！",
                "bg_color": (255, 255, 200),
                "duration": 4,
                "animation": "wave",
            },
            {
                "speaker": "popo",
                "expression": "think",
                "text": "たいようの ひかりには\nにじの いろが\nぜんぶ はいってるんだ！",
                "bg_color": (255, 255, 200),
                "duration": 5,
                "animation": "explain",
            },
            {
                "speaker": "momo",
                "expression": "surprise",
                "text": "えっ！しろい ひかりに\nいろが かくれてるの？\nしらなかった〜！",
                "bg_color": (255, 240, 200),
                "duration": 4,
                "animation": "surprised",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "そらの くうきが\nあおい ひかりだけを\nはじいて ちらすんだ！",
                "bg_color": (135, 206, 235),
                "duration": 5,
                "animation": "explain",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "ゆうやけが オレンジなのは\nひかりが とおくを とおって\nあかい いろだけ のこるから！",
                "bg_color": (255, 160, 60),
                "duration": 6,
                "animation": "wave",
            },
            {
                "speaker": "momo",
                "expression": "smile",
                "text": "そっかー！\nひかりって\nすごいんだね！",
                "bg_color": (135, 206, 235),
                "duration": 4,
                "animation": "happy",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "またいっしょに\n「なんで？」\nさがそうね！だワン♪",
                "bg_color": (200, 240, 255),
                "duration": 4,
                "animation": "wave",
            },
        ],
    },

    # ----------------------------------------
    # 動画②：トト＋ポポ
    # ----------------------------------------
    {
        "id": "why_rainbow",
        "title": "なんでにじはでるの？",
        "characters": ["toto", "popo"],   # トトが登場！
        "duration_sec": 35,
        "scenes": [
            {
                "speaker": "toto",
                "expression": "smile",
                "text": "ポポ！ポポ！\nきょうも「なんで？」\nしらべるなの！",
                "bg_color": (200, 230, 255),
                "duration": 3,
                "animation": "bounce",
            },
            {
                "speaker": "toto",
                "expression": "curious",
                "text": "にじって\nなんで できるなの？",
                "bg_color": (200, 230, 255),
                "duration": 4,
                "animation": "bounce",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "トト！\nいい「なんで？」だワン！\nおしえてあげる！",
                "bg_color": (200, 255, 200),
                "duration": 4,
                "animation": "wave",
            },
            {
                "speaker": "popo",
                "expression": "think",
                "text": "あめあがりに\nたいようが でると\nにじが みえるよね！",
                "bg_color": (200, 255, 200),
                "duration": 4,
                "animation": "explain",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "くうきの なかの\nちいさな みずの つぶが\nひかりを まげて\nいろに わけるんだ！",
                "bg_color": (255, 255, 200),
                "duration": 6,
                "animation": "explain",
            },
            {
                "speaker": "toto",
                "expression": "surprise",
                "text": "みずの つぶが\nひかりを わけるなの？\nすごーい！",
                "bg_color": (220, 200, 255),
                "duration": 4,
                "animation": "surprised",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "あか・オレンジ・き・\nみどり・あお・あい・むらさき\n7つの いろが にじだワン！",
                "bg_color": (220, 200, 255),
                "duration": 5,
                "animation": "explain",
            },
            {
                "speaker": "toto",
                "expression": "smile",
                "text": "7いろ！\nかぞえて みるなの！",
                "bg_color": (255, 220, 220),
                "duration": 4,
                "animation": "happy",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "またいっしょに\n「なんで？」\nさがそうね！だワン♪",
                "bg_color": (200, 240, 255),
                "duration": 4,
                "animation": "wave",
            },
        ],
    },

    # ----------------------------------------
    # 動画③：ももちゃん＋トト＋ポポ（3人全員！）
    # ----------------------------------------
    {
        "id": "why_seasons",
        "title": "なんできせつがかわるの？",
        "characters": ["momo", "toto", "popo"],  # 3人全員登場！
        "duration_sec": 40,
        "scenes": [
            {
                "speaker": "momo",
                "expression": "smile",
                "text": "トト！きょうも\n「なんで？」しらべよう！",
                "bg_color": (255, 220, 100),
                "duration": 3,
                "animation": "bounce",
            },
            {
                "speaker": "toto",
                "expression": "curious",
                "text": "うん！ねえ ももちゃん\nなんで なつは あついなの？\nふゆは さむいなの？",
                "bg_color": (255, 220, 100),
                "duration": 5,
                "animation": "bounce",
            },
            {
                "speaker": "momo",
                "expression": "curious",
                "text": "あ！わたしも\nずっと きになってた！\nポポ おしえて！",
                "bg_color": (255, 230, 150),
                "duration": 4,
                "animation": "bounce",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "ふたりとも\nいい「なんで？」だワン！\nきいてきいて！",
                "bg_color": (200, 230, 255),
                "duration": 4,
                "animation": "wave",
            },
            {
                "speaker": "popo",
                "expression": "think",
                "text": "ちきゅうは たいようの\nまわりを ぐるぐる\nまわっているんだ",
                "bg_color": (200, 230, 255),
                "duration": 5,
                "animation": "explain",
            },
            {
                "speaker": "toto",
                "expression": "surprise",
                "text": "ぐるぐる まわってるなの！？\nしらなかった〜！",
                "bg_color": (255, 220, 100),
                "duration": 3,
                "animation": "surprised",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "ちきゅうは すこし\nかたむいて いるから\nたいように ちかい じきが あるんだよ！",
                "bg_color": (255, 200, 100),
                "duration": 6,
                "animation": "explain",
            },
            {
                "speaker": "momo",
                "expression": "think",
                "text": "ちかいと あたたかくて\nとおいと さむく なるなの？",
                "bg_color": (200, 230, 255),
                "duration": 4,
                "animation": "curious",
            },
            {
                "speaker": "popo",
                "expression": "smile",
                "text": "そのとおり！\nはるや あきは ちょうどいい\nきょりだから すごしやすいんだワン",
                "bg_color": (200, 255, 200),
                "duration": 5,
                "animation": "wave",
            },
            {
                "speaker": "toto",
                "expression": "smile",
                "text": "ちきゅうって\nすごいなの〜！",
                "bg_color": (255, 230, 150),
                "duration": 3,
                "animation": "happy",
            },
            {
                "speaker": "momo",
                "expression": "smile",
                "text": "またみんなで\n「なんで？」さがそうね！",
                "bg_color": (200, 240, 255),
                "duration": 3,
                "animation": "wave",
            },
        ],
    },
]
