#!/usr/bin/env python3
"""Draw 'The World in One Day - Saturday 21 November 2026'.

A hand-drawn vector newspaper front page (1024x1024) summing up six
verified stories from Saturday 21 November 2026:
  1. Russian missiles land in Poland; Tusk calls it a deliberate
     provocation, NATO calls it a grave violation
  2. Wall Street slides into correction as AI shares plunge
  3. US State Department details $12bn in Venezuelan oil revenue
  4. France holds a fourth weekend of cost-of-living protests
  5. Russian strikes on Kryvyi Rih kill 2 and injure 42
  6. Los Angeles jury convicts the man who started the Palisades Fire
Only PIL is used; the output is deterministic, so repeated runs write
identical bytes.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (26, 26, 26)
RED = (176, 42, 32)
BLUE = (31, 78, 121)
TEAL = (18, 110, 105)
GOLD = (184, 134, 11)
GREY = (90, 86, 78)
LIGHT = (233, 226, 208)
DUSK = (43, 52, 84)
SKY = (214, 231, 240)
SEA = (52, 110, 140)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def _font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def serif_b(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _font("DejaVuSerif.ttf", size)


def sans_b(size):
    return _font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, width, text, fnt, fill=INK, leading=1.22):
    """Draw wrapped text; returns the y just below the block."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def panel(draw, x, y, w, h, fill=(255, 255, 255)):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=INK, width=2)


def kicker(draw, x, y, label, fill=RED):
    f = sans_b(17)
    draw.text((x, y), label.upper(), font=f, fill=fill)
    return y + 24


def star(draw, cx, cy, r_out, r_in, fill, points=4):
    """A compass-style star with `points` long spikes."""
    pts = []
    n = points * 2
    for i in range(n * 2):
        ang = math.pi * i / n - math.pi / 2
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=INK, width=1)


def flame(draw, x, y, s):
    """A simple flame rising from base point (x, y), scaled by s."""
    draw.polygon([(x - 16 * s, y), (x - 10 * s, y - 26 * s),
                  (x - 2 * s, y - 12 * s), (x + 4 * s, y - 34 * s),
                  (x + 10 * s, y - 16 * s), (x + 16 * s, y)],
                 fill=(255, 140, 0), outline=(200, 60, 0), width=2)
    draw.polygon([(x - 7 * s, y), (x - 3 * s, y - 16 * s),
                  (x + 3 * s, y - 8 * s), (x + 7 * s, y)],
                 fill=(255, 210, 60))


def draw_poland(draw, x, y, w, h):
    """Night sky over Poland: missile trail, Polish flag, NATO star."""
    draw.rectangle([x, y, x + w, y + h], fill=DUSK)
    # stars
    for sx, sy in ((x + 30, y + 18), (x + 90, y + 34), (x + 180, y + 14),
                   (x + 260, y + 30), (x + 340, y + 16), (x + 420, y + 38),
                   (x + 130, y + 52), (x + 300, y + 56)):
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 220))
    # moon
    draw.ellipse([x + w - 52, y + 12, x + w - 22, y + 42], fill=(240, 236, 210))
    # missile streaking down, left to right
    mx0, my0 = x + 60, y + 46
    mx1, my1 = x + 210, y + 96
    draw.line([(mx0, my0), (mx1, my1)], fill=(255, 200, 90), width=5)
    draw.line([(mx0, my0), (mx0 - 34, my0 - 14)], fill=(255, 140, 0), width=3)
    draw.polygon([(mx1, my1), (mx1 - 22, my1 - 8), (mx1 - 22, my1 + 8)],
                 fill=(200, 200, 200), outline=INK, width=1)
    # NATO compass star, upper right
    star(draw, x + w - 78, y + 92, 30, 9, (200, 210, 235))
    draw.text((x + w - 118, y + 128), "NATO", font=sans_b(14),
              fill=(200, 210, 235))
    # ground
    gy = y + h - 26
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(24, 40, 28))
    for tx in (x + 40, x + 330, x + 390):
        draw.polygon([(tx, gy - 34), (tx - 14, gy), (tx + 14, gy)],
                     fill=(16, 60, 30))
    # Polish flag on a pole
    fx, fy = x + 30, gy - 84
    draw.line([(fx, fy), (fx, gy)], fill=INK, width=3)
    draw.rectangle([fx, fy, fx + 64, fy + 20], fill=(245, 245, 240),
                   outline=INK, width=1)
    draw.rectangle([fx, fy + 20, fx + 64, fy + 40], fill=(220, 40, 50),
                   outline=INK, width=1)
    draw.text((fx + 72, fy + 8), "POLAND", font=sans_b(18), fill=(255, 255, 255))
    # impact burst on the ground
    bx, by = x + 250, gy - 6
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        draw.line([(bx, by), (bx + 22 * math.cos(a), by + 22 * math.sin(a))],
                  fill=(255, 140, 0), width=4)
    draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(255, 200, 60),
                 outline=(200, 60, 0), width=2)
    draw.text((bx + 28, by - 8), "2 MISSILES + 1 DRONE", font=sans_b(13),
              fill=(255, 220, 120))


def draw_market_fall(draw, x, y, w, h):
    """Falling red chart over a trading-floor grid."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 228, 224))
    for gx in range(x + 12, x + w - 8, 34):
        draw.line([(gx, y + 10), (gx, y + h - 30)], fill=(214, 200, 196),
                  width=1)
    for gy in range(y + 12, y + h - 28, 26):
        draw.line([(x + 10, gy), (x + w - 10, gy)], fill=(214, 200, 196),
                  width=1)
    pts = [(x + 16, y + 22), (x + 70, y + 34), (x + 120, y + 30),
           (x + 170, y + 58), (x + 220, y + 74), (x + w - 18, y + h - 46)]
    draw.line(pts, fill=(178, 34, 34), width=5, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(178, 34, 34))
    draw.polygon([(x + w - 18, y + h - 46), (x + w - 42, y + h - 50),
                  (x + w - 22, y + h - 26)], fill=(178, 34, 34))
    draw.text((x + 14, y + h - 34), "-3.7%  S&P 500", font=sans_b(20),
              fill=(178, 34, 34))
    for i, bh in enumerate((34, 22, 28, 16)):
        bx = x + w - 110 + i * 24
        draw.rectangle([bx, y + h - 16 - bh, bx + 15, y + h - 16],
                       fill=(178, 90, 80))


def draw_oil(draw, x, y, w, h):
    """Oil pumpjack and barrels under a desert sun."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 226, 196))
    draw.ellipse([x + w - 62, y + 10, x + w - 22, y + 50], fill=(255, 200, 80),
                 outline=(200, 140, 0), width=2)
    # ground
    gy = y + h - 22
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(150, 110, 70))
    # pumpjack, right of the text block so its beam clears the labels
    px, py = x + 120, gy
    draw.line([(px, py), (px + 26, py - 62)], fill=INK, width=4)
    draw.line([(px + 52, py), (px + 26, py - 62)], fill=INK, width=4)
    draw.line([(px + 14, py - 66), (px + 88, py - 74)], fill=INK, width=5)
    draw.line([(px + 88, py - 74), (px + 88, py - 34)], fill=INK, width=3)
    draw.line([(px + 88, py - 34), (px + 74, py - 34)], fill=INK, width=3)
    # derrick tower, right
    dx = x + w - 84
    draw.polygon([(dx, gy), (dx + 44, gy), (dx + 34, gy - 78),
                  (dx + 10, gy - 78)], fill=(120, 90, 60), outline=INK,
                 width=2)
    draw.line([(dx + 6, gy - 20), (dx + 38, gy - 20)], fill=INK, width=2)
    draw.line([(dx + 8, gy - 44), (dx + 36, gy - 44)], fill=INK, width=2)
    # barrels, left
    for bx in (x + 30, x + 62):
        draw.rectangle([bx, gy - 30, bx + 26, gy], fill=(40, 60, 90),
                       outline=INK, width=2)
        draw.line([(bx, gy - 20), (bx + 26, gy - 20)], fill=INK, width=1)
        draw.line([(bx, gy - 10), (bx + 26, gy - 10)], fill=INK, width=1)
    draw.text((x + 14, y + 10), "$12 BN", font=sans_b(26), fill=INK)
    draw.text((x + 14, y + 40), "OIL + MINERALS", font=sans_b(13), fill=GREY)


def draw_protest(draw, x, y, w, h):
    """Street march with placards and the Eiffel Tower behind.

    All geometry is relative to the scene height h, so placards and
    marchers stay inside the scene box.
    """
    draw.rectangle([x, y, x + w, y + h], fill=(222, 228, 238))
    # Eiffel Tower silhouette, right
    tx, ty = x + w - 56, y + h - 20
    draw.polygon([(tx - 26, ty), (tx + 26, ty), (tx + 4, y + 16),
                  (tx - 4, y + 16)], fill=(90, 100, 120), outline=INK,
                 width=2)
    draw.line([(tx - 14, ty - 46), (tx + 14, ty - 46)], fill=INK, width=3)
    # street
    gy = y + h - 20
    draw.rectangle([x, gy, x + w, y + h], fill=(120, 116, 110))
    # marchers: heads, shoulders and placards, all inside the scene
    crowd = [(x + 34, (220, 60, 60)), (x + 78, (40, 70, 130)),
             (x + 122, (30, 120, 60)), (x + 166, (200, 140, 30)),
             (x + 196, (120, 60, 140))]
    for cx, shirt in crowd:
        draw.ellipse([cx - 13, gy - 52, cx + 13, gy - 28],
                     fill=(232, 190, 150), outline=INK, width=2)
        draw.polygon([(cx - 20, gy), (cx + 20, gy), (cx + 15, gy - 30),
                      (cx - 15, gy - 30)], fill=shirt, outline=INK, width=1)
    # placards on sticks, kept inside the scene (top at gy-92)
    for cx, label in ((x + 34, "PRICES"), (x + 122, "COST OF"),
                      (x + 196, "LIVING")):
        draw.line([(cx + 16, gy - 92), (cx + 16, gy - 52)], fill=INK, width=3)
        draw.rectangle([cx - 12, gy - 92, cx + 44, gy - 68],
                       fill=(255, 255, 255), outline=INK, width=2)
        draw.text((cx - 8, gy - 88), label, font=sans_b(11), fill=INK)


def draw_strike(draw, x, y, w, h):
    """City skyline at dusk with a blast and smoke over Kryvyi Rih.

    Building heights and the blast are scaled to the scene height h,
    so nothing pokes out of the scene box.
    """
    draw.rectangle([x, y, x + w, y + h], fill=(232, 196, 150))
    k = h / 120.0
    ground = y + h - int(12 * k)
    for bx, bw, bh, col in ((x + 8, 44, 66, (120, 110, 100)),
                            (x + 58, 40, 88, (96, 88, 80)),
                            (x + 104, 46, 58, (130, 118, 106)),
                            (x + 156, 42, 78, (104, 94, 86)),
                            (x + 204, 48, 62, (124, 112, 100))):
        bh = int(bh * k)
        draw.rectangle([bx, ground - bh, bx + bw, ground], fill=col,
                       outline=INK, width=2)
        for wy in range(ground - bh + 8, ground - 8, 14):
            for wx in range(bx + 7, bx + bw - 6, 12):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 220, 120))
    draw.rectangle([x, ground, x + w, y + h], fill=(70, 66, 60))
    bx, by = x + 78, ground - int(30 * k)
    r = int(26 * k)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        draw.line([(bx, by), (bx + r * math.cos(a), by + r * math.sin(a))],
                  fill=(255, 140, 0), width=4)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 200, 60),
                 outline=(200, 60, 0), width=2)
    for sx, sy, sr in ((bx - 30, by - 22, 9), (bx + 26, by - 30, 11),
                       (bx + 6, by - 38, 8)):
        if sy - sr >= y + 2:
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                         fill=(120, 116, 110))


def draw_court_fire(draw, x, y, w, h):
    """Courtroom bench and gavel, with a wildfire flame behind.

    All geometry is relative to the scene height h, so the bench,
    gavel and flames stay inside the scene box.
    """
    draw.rectangle([x, y, x + w, y + h], fill=(226, 222, 205))
    # wildfire glow band across the top third
    band = int(h * 0.34)
    draw.rectangle([x, y, x + w, y + band], fill=(240, 190, 120))
    flame(draw, x + w * 0.28, y + band, 0.7)
    flame(draw, x + w * 0.62, y + band, 0.6)
    flame(draw, x + w * 0.85, y + band, 0.5)
    # judge's bench across the lower half
    top = y + int(h * 0.52)
    bot = y + h - 4
    draw.rectangle([x + 30, top, x + w - 30, bot], fill=(96, 62, 32),
                   outline=INK, width=2)
    draw.rectangle([x + 30, top, x + w - 30, top + 8], fill=(120, 80, 44),
                   outline=INK, width=2)
    # gavel resting on the bench top, left of centre
    gx, gy = x + w // 2 - 40, top
    draw.line([(gx, gy), (gx + 30, gy - 18)], fill=(80, 50, 26), width=5)
    draw.rectangle([gx - 14, gy - 28, gx + 8, gy - 14], fill=(60, 38, 20),
                   outline=INK, width=2)
    # verdict slip on the bench front
    draw.rectangle([x + 40, top + 16, x + 118, top + 44], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.text((x + 48, top + 20), "GUILTY", font=sans_b(16), fill=RED)
    # small scales emblem on the bench, right
    cx, cy = x + w - 66, top + 28
    draw.line([(cx, cy - 14), (cx, cy + 10)], fill=INK, width=3)
    draw.line([(cx - 16, cy - 11), (cx + 16, cy - 11)], fill=INK, width=3)
    draw.arc([cx - 22, cy - 9, cx - 10, cy + 2], 0, 180, fill=INK, width=2)
    draw.arc([cx + 10, cy - 9, cx + 22, cy + 2], 0, 180, fill=INK, width=2)
    draw.ellipse([cx - 3, cy - 17, cx + 3, cy - 11], fill=GOLD, outline=INK)


def story_panel(draw, x, y, w, h, scene, kicker_text, headline, subhead,
                share=0.48, head_size=22, sub_size=16):
    panel(draw, x, y, w, h)
    ih = int(h * share)
    scene(draw, x + 2, y + 2, w - 4, ih)
    ty = y + ih + 8
    kicker(draw, x + 12, ty, kicker_text)
    ty += 24
    ty = text_block(draw, x + 12, ty, w - 24, headline, serif_b(head_size),
                    leading=1.08)
    text_block(draw, x + 12, ty + 4, w - 24, subhead, sans(sub_size),
               fill=(60, 56, 48), leading=1.2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # ---- masthead ----
    my = 30
    title = "THE WORLD IN ONE DAY"
    tf = serif_b(56)
    d.text(((W - d.textlength(title, font=tf)) / 2, my), title, font=tf,
           fill=INK)
    my += 72
    rule(d, 40, my, W - 40, 3, RED)
    my += 12
    date = "SATURDAY 21 NOVEMBER 2026"
    df = sans_b(30)
    d.text(((W - d.textlength(date, font=df)) / 2, my), date, font=df,
           fill=RED)
    my += 42
    sub = "SIX STORIES FROM AROUND THE WORLD  •  DRAWN FROM THE DAY'S REPORTING"
    sf = sans(16)
    d.text(((W - d.textlength(sub, font=sf)) / 2, my), sub, font=sf, fill=GREY)
    my += 28
    rule(d, 40, my, W - 40, 2)

    # ---- lead story: missiles land in Poland ----
    ly = my + 12
    lh = 290
    panel(d, 32, ly, W - 64, lh)
    hx = 52
    hy = ly + 12
    hy = text_block(d, hx, hy, W - 104,
                    "RUSSIAN MISSILES HIT POLAND",
                    serif_b(33), leading=1.05)
    rule(d, hx, hy + 4, W - 52, 1, GREY)
    iy = hy + 14
    ih = ly + lh - iy - 14
    draw_poland(d, 44, iy, 470, ih)
    tx = 534
    text_block(d, tx, iy + 6, W - 52 - tx,
               "Two missiles and a drone come down in south-east Poland "
               "as Russia pounds Ukraine.",
               sans_b(21), leading=1.25)
    text_block(d, tx, iy + 96, W - 52 - tx,
               "Prime Minister Tusk calls it an intentional provocation. "
               "NATO chief Rutte calls it a grave violation of allied "
               "airspace. No one in Poland is hurt.",
               sans(18), fill=(60, 56, 48), leading=1.3)
    d.text((tx, ly + lh - 34), "CONFLICT  •  EUROPE", font=sans_b(15),
           fill=RED)

    # ---- middle row: three stories ----
    ry = ly + lh + 12
    rh = 250
    cw = (W - 64 - 24) // 3
    story_panel(d, 32, ry, cw, rh, draw_market_fall, "Markets • New York",
                "WALL STREET SLIDES INTO CORRECTION",
                "S&P 500 falls as AI shares plunge and Anthropic slides.",
                head_size=20)
    story_panel(d, 44 + cw, ry, cw, rh, draw_oil, "Americas • Energy",
                "US DETAILS $12BN IN VENEZUELAN OIL CASH",
                "State Dept report tracks oil and mineral revenue.",
                head_size=20)
    story_panel(d, 56 + 2 * cw, ry, cw, rh, draw_protest, "Society • France",
                "FOURTH WEEKEND OF COST-OF-LIVING PROTESTS",
                "Crowds march over rising prices.",
                head_size=18)

    # ---- bottom row: two stories ----
    by = ry + rh + 12
    bh = H - by - 52
    bw = (W - 64 - 12) // 2
    story_panel(d, 32, by, bw, bh, draw_strike, "War in Ukraine",
                "KRYVYI RIH: 2 DEAD, 42 HURT IN STRIKES",
                "Children among the injured as Russian attacks hit the city.",
                share=0.42)
    story_panel(d, 44 + bw, by, bw, bh, draw_court_fire, "Justice • Los Angeles",
                "PALISADES FIRE: MAN FOUND GUILTY",
                "Jury convicts the man who started the Los Angeles wildfire.",
                share=0.42)

    # ---- footer ----
    fy = H - 44
    rule(d, 40, fy, W - 40, 1, GREY)
    foot = "SATURDAY 21 NOVEMBER 2026  —  THE WORLD IN ONE DAY"
    ff = sans_b(15)
    d.text(((W - d.textlength(foot, font=ff)) / 2, fy + 8), foot, font=ff,
           fill=INK)

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
