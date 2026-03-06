"""
子ども向けショート動画コンテンツ定義
キャラクター: ももちゃん（女の子）とポポ（プードル犬）
テーマ: 子どもの「なんで？」を解決する教育コンテンツ
"""

CHARACTERS = {
    "momo": {
        "name": "ももちゃん",
        "color": (255, 182, 193),   # ピンク
        "image": "assets/momo.png",
        "role": "question_asker",   # 質問する役
    },
    "popo": {
        "name": "ポポ",
        "color": (205, 133, 63),    # 茶色
        "image": "assets/popo.png",
        "role": "answerer",         # 答える役
    },
}

VIDEO_SCRIPTS = [
    {
        "id": "why_sky_blue",
        "title": "なんでそらはあおいの？",
        "duration_sec": 30,
        "scenes": [
            {
                "speaker": "momo",
                "text": "ねえポポ！\nなんでそらって\nあおいの？",
                "bg_color": (135, 206, 235),  # スカイブルー
                "duration": 4,
                "animation": "bounce",
            },
            {
                "speaker": "popo",
                "text": "いい質問だワン！\nたいようの ひかりには\nいろんな いろが\nまじっているんだよ",
                "bg_color": (255, 255, 200),  # 薄黄色
                "duration": 5,
                "animation": "wave",
            },
            {
                "speaker": "popo",
                "text": "そらの くうきが\nあおい ひかりだけを\nはねかえすから\nあおく みえるんだ！",
                "bg_color": (135, 206, 235),
                "duration": 6,
                "animation": "explain",
            },
            {
                "speaker": "momo",
                "text": "すごーい！\nゆうやけは\nなんでオレンジなの？",
                "bg_color": (255, 165, 0),    # オレンジ
                "duration": 4,
                "animation": "bounce",
            },
            {
                "speaker": "popo",
                "text": "ゆうがたは ひかりが\nとおい みちを とおるから\nあかや オレンジが\nのこるんだワン！",
                "bg_color": (255, 140, 0),
                "duration": 6,
                "animation": "wave",
            },
            {
                "speaker": "momo",
                "text": "そっかー！\nそらって\nふしぎだね！",
                "bg_color": (135, 206, 235),
                "duration": 5,
                "animation": "happy",
            },
        ],
    },
    {
        "id": "why_rainbow",
        "title": "なんでにじはでるの？",
        "duration_sec": 30,
        "scenes": [
            {
                "speaker": "momo",
                "text": "ポポ！ポポ！\nにじって\nなんでできるの？",
                "bg_color": (200, 230, 255),
                "duration": 4,
                "animation": "bounce",
            },
            {
                "speaker": "popo",
                "text": "あめあがりに\nたいようが でると\nにじが みえるよね！",
                "bg_color": (200, 255, 200),
                "duration": 4,
                "animation": "wave",
            },
            {
                "speaker": "popo",
                "text": "くうきの なかの\nちいさな みずの つぶが\nひかりを まげて\nいろに わけるんだ！",
                "bg_color": (255, 255, 200),
                "duration": 6,
                "animation": "explain",
            },
            {
                "speaker": "popo",
                "text": "あか・オレンジ・き・\nみどり・あお・あい・むらさき\n7つの いろが\nにじなんだワン！",
                "bg_color": (220, 200, 255),
                "duration": 6,
                "animation": "explain",
            },
            {
                "speaker": "momo",
                "text": "みずが プリズムに\nなるんだね！\nきれーい！",
                "bg_color": (255, 220, 220),
                "duration": 5,
                "animation": "happy",
            },
            {
                "speaker": "popo",
                "text": "にじは まるいんだよ！\nたかいところから みると\nまるい にじが\nみえるんだワン！",
                "bg_color": (200, 255, 230),
                "duration": 5,
                "animation": "wave",
            },
        ],
    },
    {
        "id": "why_seasons",
        "title": "なんできせつがかわるの？",
        "duration_sec": 30,
        "scenes": [
            {
                "speaker": "momo",
                "text": "ねえ！なんで\nなつは あついの？\nふゆは さむいの？",
                "bg_color": (255, 220, 100),
                "duration": 4,
                "animation": "bounce",
            },
            {
                "speaker": "popo",
                "text": "ちきゅうは たいようの\nまわりを ぐるぐる\nまわっているんだ",
                "bg_color": (200, 230, 255),
                "duration": 5,
                "animation": "explain",
            },
            {
                "speaker": "popo",
                "text": "ちきゅうは すこし\nかたむいて いるから\nたいように ちかい\nじきが あるんだよ！",
                "bg_color": (255, 200, 100),
                "duration": 6,
                "animation": "explain",
            },
            {
                "speaker": "popo",
                "text": "たいように ちかいと\nあたたかくて なつ！\nとおいと さむくて\nふゆに なるんだワン",
                "bg_color": (200, 230, 255),
                "duration": 6,
                "animation": "wave",
            },
            {
                "speaker": "momo",
                "text": "ちきゅうが かたむいてる\nから なんだ！\nしらなかった！",
                "bg_color": (255, 230, 150),
                "duration": 5,
                "animation": "happy",
            },
            {
                "speaker": "popo",
                "text": "はるや あきは\nちょうど いい\nきょりだから\nすごしやすいんだよ！",
                "bg_color": (200, 255, 200),
                "duration": 4,
                "animation": "wave",
            },
        ],
    },
]
