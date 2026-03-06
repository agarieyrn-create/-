"""
アップロード画像を参考にした高品質キャラクター画像生成
"""
import os
import math
from PIL import Image, ImageDraw, ImageFilter

ASSET_DIR = "assets"
os.makedirs(ASSET_DIR, exist_ok=True)


def draw_popo(size=(600, 700)) -> Image.Image:
    """ポポ（チョコレート色プードル）を描く"""
    W, H = size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    body_color = (160, 90, 40)
    dark_color = (120, 60, 20)
    pink = (255, 182, 193)
    white = (255, 255, 255)

    # --- 胴体 ---
    draw.ellipse([W//4, H//2 - 40, 3*W//4, H - 80], fill=body_color)

    # --- 尻尾（右上） ---
    draw.ellipse([3*W//4 - 20, H//3, 3*W//4 + 60, H//3 + 80], fill=body_color)

    # --- 後ろ足 ---
    for x in [W//3 - 20, 2*W//3 - 40]:
        draw.ellipse([x, H - 130, x + 80, H - 20], fill=dark_color)
        draw.ellipse([x - 10, H - 50, x + 90, H + 10], fill=body_color)

    # --- 前足（左：上げている） ---
    draw.ellipse([W//6, H//2 + 20, W//6 + 80, H//2 + 140], fill=body_color)
    draw.ellipse([W//6 - 10, H//2 + 120, W//6 + 90, H//2 + 190], fill=dark_color)

    # --- 前足（右：地につけている） ---
    draw.ellipse([2*W//3, H//2 + 80, 2*W//3 + 80, H//2 + 180], fill=body_color)
    draw.ellipse([2*W//3 - 5, H//2 + 160, 2*W//3 + 85, H//2 + 220], fill=dark_color)

    # --- 頭 ---
    head_cx, head_cy, head_r = W // 2, H // 3, 150
    draw.ellipse(
        [head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
        fill=body_color,
    )

    # ふわふわ感（小さい円を重ねる）
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        ex = int(head_cx + (head_r - 15) * math.cos(rad))
        ey = int(head_cy + (head_r - 15) * math.sin(rad))
        draw.ellipse([ex - 28, ey - 28, ex + 28, ey + 28], fill=body_color)

    # --- 耳 ---
    for sign in [-1, 1]:
        ear_cx = head_cx + sign * 130
        ear_cy = head_cy + 20
        draw.ellipse([ear_cx - 40, ear_cy - 60, ear_cx + 40, ear_cy + 60], fill=dark_color)
        for a in range(0, 360, 40):
            r2 = math.radians(a)
            ex = int(ear_cx + 30 * math.cos(r2))
            ey = int(ear_cy + 50 * math.sin(r2))
            draw.ellipse([ex - 20, ey - 20, ex + 20, ey + 20], fill=dark_color)

    # --- 目 ---
    for sign in [-1, 1]:
        ex = head_cx + sign * 55
        ey = head_cy - 10
        draw.ellipse([ex - 18, ey - 22, ex + 18, ey + 22], fill=(30, 20, 10))
        draw.ellipse([ex - 7, ey - 10, ex + 7, ey + 10], fill=white)
        # まつげ
        for i in range(-2, 3):
            draw.line(
                [(ex + sign * 16, ey - 18 + i * 4),
                 (ex + sign * 28, ey - 30 + i * 6)],
                fill=(30, 20, 10), width=2,
            )

    # --- 鼻 ---
    nose_y = head_cy + 25
    draw.ellipse([head_cx - 20, nose_y - 12, head_cx + 20, nose_y + 12], fill=(40, 25, 15))

    # --- 口 ---
    draw.arc([head_cx - 30, nose_y + 5, head_cx + 30, nose_y + 40], 0, 180,
             fill=(200, 80, 80), width=4)
    # 舌
    draw.ellipse([head_cx - 12, nose_y + 25, head_cx + 12, nose_y + 45], fill=(240, 100, 120))

    # --- バンダナ（ピンク・さくらんぼ柄） ---
    bx1, by1 = head_cx - 80, head_cy + head_r - 20
    bx2, by2 = head_cx + 80, head_cy + head_r + 50
    draw.polygon(
        [(bx1, by1), (bx2, by1), (bx2 + 30, by2), (head_cx, by2 + 30), (bx1 - 30, by2)],
        fill=(255, 182, 193),
        outline=(220, 140, 160),
    )
    # バンダナの白い花柄
    for cx2, cy2 in [(head_cx - 40, by1 + 15), (head_cx + 30, by1 + 20), (head_cx - 5, by1 + 30)]:
        draw.ellipse([cx2 - 8, cy2 - 8, cx2 + 8, cy2 + 8], fill=white)

    # バンダナのさくらんぼ模様
    for cx2, cy2 in [(head_cx - 55, by1 + 25), (head_cx + 50, by1 + 18)]:
        draw.ellipse([cx2 - 6, cy2 - 6, cx2 + 6, cy2 + 6], fill=(220, 50, 50))
        draw.ellipse([cx2 + 6, cy2 - 10, cx2 + 14, cy2 - 2], fill=(220, 50, 50))
        draw.line([(cx2, cy2 - 6), (cx2 + 6, cy2 - 14), (cx2 + 10, cy2 - 10)],
                  fill=(60, 160, 60), width=2)

    # --- 頭のさくらんぼ飾り ---
    hd_x, hd_y = head_cx - 80, head_cy - head_r - 10
    draw.ellipse([hd_x - 10, hd_y - 10, hd_x + 10, hd_y + 10], fill=(220, 50, 50))
    draw.ellipse([hd_x + 8, hd_y - 14, hd_x + 24, hd_y], fill=(220, 50, 50))
    draw.line([(hd_x, hd_y - 10), (hd_x + 10, hd_y - 22), (hd_x + 16, hd_y - 14)],
              fill=(60, 160, 60), width=3)

    # --- 胸元のメダル ---
    medal_x, medal_y = head_cx + 20, head_cy + head_r + 60
    draw.ellipse([medal_x - 15, medal_y - 15, medal_x + 15, medal_y + 15],
                 fill=(220, 180, 80), outline=(180, 140, 40))
    draw.text = None  # skip font rendering in this helper

    return img


def draw_momo(size=(600, 800)) -> Image.Image:
    """ももちゃん（アニメ風女の子）を描く"""
    W, H = size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    skin = (255, 220, 185)
    hair_color = (100, 65, 30)
    highlight = (180, 130, 80)
    pink = (255, 182, 193)
    dark_pink = (230, 130, 150)
    white = (255, 255, 255)
    denim = (100, 130, 190)

    # --- 脚 ---
    for lx in [W//2 - 70, W//2 + 10]:
        draw.rectangle([lx, 3*H//4, lx + 55, H - 40], fill=skin)
    # くつ
    draw.ellipse([W//2 - 90, H - 80, W//2 - 10, H - 20], fill=dark_pink)
    draw.ellipse([W//2 + 5, H - 70, W//2 + 85, H - 10], fill=dark_pink)

    # --- スカート ---
    draw.polygon(
        [(W//4 - 20, H//2 + 60), (3*W//4 + 20, H//2 + 60),
         (3*W//4 + 60, 3*H//4 + 20), (W//4 - 60, 3*H//4 + 20)],
        fill=denim, outline=(80, 105, 160),
    )
    # フリル
    for i in range(6):
        fx = W//4 - 50 + i * (W // 5 + 15)
        fy = 3*H//4 + 10
        draw.arc([fx, fy, fx + 60, fy + 30], 0, 180, fill=white, width=5)

    # スカート下のシャツのフリル（白）
    for i in range(5):
        fx = W//4 - 20 + i * (W // 5)
        fy = H//2 + 50
        draw.arc([fx, fy, fx + 50, fy + 24], 0, 180, fill=white, width=5)

    # --- 体（ピンクパーカー） ---
    draw.rounded_rectangle([W//4, H//3, 3*W//4, H//2 + 80], radius=20, fill=pink)

    # パーカーのもも（桃）アイコン
    pc_x, pc_y = W // 2 - 30, H//2 - 20
    draw.ellipse([pc_x, pc_y - 25, pc_x + 40, pc_y + 15], fill=(255, 180, 120))
    draw.ellipse([pc_x + 15, pc_y - 35, pc_x + 55, pc_y + 5], fill=(255, 180, 120))
    draw.ellipse([pc_x + 10, pc_y - 45, pc_x + 40, pc_y - 5], fill=(80, 160, 60))

    # --- 腕 ---
    # 左腕（上げている）
    draw.rounded_rectangle([W//4 - 60, H//3 - 10, W//4 + 10, H//3 + 100], radius=25, fill=pink)
    draw.ellipse([W//4 - 70, H//3 - 50, W//4 + 20, H//3 + 30], fill=pink)
    draw.ellipse([W//4 - 65, H//3 - 80, W//4 + 10, H//3 - 20], fill=skin)  # 手
    # グー（こぶし）
    draw.rounded_rectangle([W//4 - 62, H//3 - 90, W//4 + 8, H//3 - 30],
                            radius=15, fill=skin, outline=(220, 180, 150), width=2)

    # 右腕（上げている）
    draw.rounded_rectangle([3*W//4 - 10, H//3 - 10, 3*W//4 + 60, H//3 + 100], radius=25, fill=pink)
    draw.ellipse([3*W//4 - 20, H//3 - 50, 3*W//4 + 70, H//3 + 30], fill=pink)
    draw.ellipse([3*W//4 - 10, H//3 - 80, 3*W//4 + 65, H//3 - 20], fill=skin)
    draw.rounded_rectangle([3*W//4 - 8, H//3 - 90, 3*W//4 + 62, H//3 - 30],
                            radius=15, fill=skin, outline=(220, 180, 150), width=2)

    # --- ランドセル（ピンク） ---
    draw.rounded_rectangle([3*W//4 - 10, H//4 + 10, 3*W//4 + 100, H//2 + 40],
                            radius=15, fill=(230, 130, 150), outline=(200, 100, 130), width=3)

    # --- 頭 ---
    head_cx, head_cy, head_r = W // 2, H // 5, 130
    draw.ellipse(
        [head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
        fill=skin,
    )

    # --- 髪（後ろ・ウェーブ） ---
    # 後ろ髪
    draw.ellipse([head_cx - head_r - 40, head_cy - 60, head_cx + head_r + 40, head_cy + head_r + 60],
                 fill=hair_color)

    # 前髪
    draw.ellipse([head_cx - head_r, head_cy - head_r - 20, head_cx + head_r, head_cy + 20],
                 fill=hair_color)
    draw.ellipse([head_cx - head_r + 10, head_cy - head_r + 20, head_cx + 30, head_cy + 10],
                 fill=skin)  # 前髪の切り込み

    # ウェーブした後ろ髪の束
    for sign, offset in [(-1, -30), (1, 30)]:
        for i in range(3):
            wh_x = head_cx + sign * (head_r + 20 + i * 5)
            wh_y = head_cy + 60 + i * 50
            r2 = 30 - i * 3
            draw.ellipse([wh_x - r2, wh_y - r2, wh_x + r2, wh_y + r2 * 2], fill=hair_color)

    # ハイライト
    draw.arc([head_cx - 60, head_cy - head_r + 10, head_cx + 20, head_cy - 30],
             200, 340, fill=highlight, width=6)

    # --- 目（笑顔で閉じ気味） ---
    for sign in [-1, 1]:
        ex = head_cx + sign * 48
        ey = head_cy + 5
        # 目の弧（笑い目）
        draw.arc([ex - 22, ey - 16, ex + 22, ey + 16], 10, 170, fill=(50, 30, 20), width=6)
        # まつげ
        for i in range(-2, 3):
            draw.line(
                [(ex + sign * 18, ey - 10 + i * 4),
                 (ex + sign * 28, ey - 22 + i * 5)],
                fill=(50, 30, 20), width=2,
            )

    # --- 口（笑顔） ---
    draw.arc([head_cx - 30, head_cy + 25, head_cx + 30, head_cy + 65], 15, 165,
             fill=(220, 80, 100), width=5)
    # 歯
    draw.arc([head_cx - 22, head_cy + 28, head_cx + 22, head_cy + 60], 20, 160,
             fill=white, width=8)

    # ほっぺ
    for sign in [-1, 1]:
        cx2 = head_cx + sign * 75
        cy2 = head_cy + 30
        cheek_img = Image.new("RGBA", (60, 35), (0, 0, 0, 0))
        cheek_draw = ImageDraw.Draw(cheek_img)
        cheek_draw.ellipse([0, 0, 59, 34], fill=(255, 140, 160, 120))
        img.paste(cheek_img, (cx2 - 30, cy2 - 17), mask=cheek_img.split()[3])

    # --- いちごの髪飾り ---
    for sign, hx_off in [(-1, -60), (1, 40)]:
        hd_x = head_cx + hx_off
        hd_y = head_cy - head_r + 10
        # いちご
        draw.polygon(
            [(hd_x, hd_y - 18), (hd_x - 12, hd_y), (hd_x, hd_y + 18), (hd_x + 12, hd_y)],
            fill=(220, 50, 60),
        )
        draw.ellipse([hd_x - 6, hd_y - 26, hd_x + 6, hd_y - 10], fill=(80, 160, 60))

    return img


def main():
    # ポポ画像
    popo = draw_popo()
    popo.save(os.path.join(ASSET_DIR, "popo.png"))
    print(f"✓ Saved popo.png ({popo.size})")

    # ももちゃん画像
    momo = draw_momo()
    momo.save(os.path.join(ASSET_DIR, "momo.png"))
    print(f"✓ Saved momo.png ({momo.size})")


if __name__ == "__main__":
    main()
