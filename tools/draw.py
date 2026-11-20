#!/usr/bin/env python3
"""Draw the 20 November 2026 front-page poster (1024x1024 PNG).

A newspaper-style one-image summary of the day's world news: a big navy
header names the day, a hero panel covers the Anthropic IPO debut, six
panels cover the other top stories, and a "MORE TODAY" strip adds three
more. Everything is flat vector-style geometry drawn with Pillow; the
script is fully deterministic (no randomness, no time, no network) so
re-running it always writes the same bytes.

Verified facts (20 Nov 2026, checked live before drawing):
- Anthropic (ANT) opened +34% at $111.50, closed +17% at $97.17 on a
  record $81.3bn IPO priced at $83 (Reuters / WSJ / Nasdaq data).
- US Senate rejected the Iran war-powers resolution 51-48 on 19 Nov.
- UK pledged 1,000+ long-range strike drones to Ukraine, GBP 260m,
  announced 19 Nov in Berlin.
- Taiwan Taiex closed down 2,393.60 (-6.22%) at 36,033.29 on 20 Nov;
  intraday drop passed 2,400; worst week since 1990, about -18%.
- Houthi missile damaged the PIF Tower in Riyadh (80 storeys, the
  tallest in the city), windows out on 7-8 floors, no injuries, 19 Nov.
- North Korea fired a ballistic missile from Wonsan toward the East
  Sea, reported Thursday morning after allied drills.
- Van Gogh's "Blossoming Chestnut Trees" (1890) sold for $190.4m at
  Sotheby's, a record for the artist (previous $117.2m).
- US Treasury (OFAC, 19 Nov) sanctioned the Comancheros and the
  'Ndrangheta; US assets frozen.
- Trump gave a posthumous pardon to baseball hit king Pete Rose
  (4,256 hits) on 19 Nov.
- UK and EU provisionally agreed a youth mobility scheme, about
  100,000 places a year.

Run:  python3 tools/draw.py
Out:  entry.png beside this script's parent directory (the repo root).
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 242, 231)
WHITE = (255, 253, 246)
INK = (20, 33, 61)
INK_SOFT = (48, 58, 82)
BRICK = (179, 64, 42)
GOLD = (198, 152, 58)
GOLD_DARK = (168, 124, 38)
MUTED = (96, 90, 78)
BORDER = (214, 204, 188)
NAVY_PANEL = (24, 40, 74)
SKY = (214, 226, 238)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
REG = f"{FONT_DIR}/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    """Draw stacked lines; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag_chip(draw, x, y, text):
    """Small brick-red tag chip; returns the chip width."""
    fnt = font(BOLD, 14)
    tw = draw.textlength(text, font=fnt)
    pad_x, pad_y = 8, 4
    w = int(tw + 2 * pad_x)
    h = 24
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=BRICK)
    draw.text((x + pad_x, y + pad_y), text, font=fnt, fill=WHITE)
    return w


# ---------------------------------------------------------------- artwork
def art_hero(draw, x0, y0, x1, y1):
    """Nasdaq board: gold ANT ticker over rising green bars."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_PANEL)
    # Ticker tape across the top.
    draw.rectangle([x0, y0, x1, y0 + 34], fill=(16, 28, 54))
    tape = font(BOLD, 18)
    draw.text((x0 + 12, y0 + 6), "ANT  $97.17  +17%", font=tape, fill=GOLD)
    # Rising bars, left to right.
    base = y1 - 18
    bars = [(18, 40, (38, 56, 96)), (52, 62, (38, 56, 96)),
            (86, 84, GOLD_DARK), (120, 108, GOLD)]
    for bx, bh, color in bars:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + 26, base], fill=color)
    # Big gold ANT, lower-right, kept inside the art box so it never
    # touches the headline text beside it.
    ant = font(BOLD, 62)
    draw.text((x0 + 168, y0 + 96), "ANT", font=ant, fill=GOLD)
    # Upward arrow above the bars.
    draw.line([x0 + 22, base - 58, x0 + 70, base - 108], fill=(120, 200, 120),
              width=5)
    draw.polygon([(x0 + 70, base - 108), (x0 + 54, base - 102),
                  (x0 + 66, base - 90)], fill=(120, 200, 120))
    draw.line([x0 + 70, base - 108, x0 + 150, base - 118],
              fill=(120, 200, 120), width=5)
    draw.polygon([(x0 + 150, base - 118), (x0 + 132, base - 118),
                  (x0 + 144, base - 102)], fill=(120, 200, 120))


def art_senate(draw, x0, y0, x1, y1):
    """US Capitol dome in navy and gold (Senate vote)."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 234, 246))
    cx = (x0 + x1) // 2
    base = y1 - 20
    # Dome.
    draw.pieslice([cx - 34, y0 + 26, cx + 34, y0 + 94], 180, 360, fill=INK)
    draw.rectangle([cx - 34, y0 + 60, cx + 34, y0 + 78], fill=INK)
    # Lantern on top of the dome.
    draw.rectangle([cx - 5, y0 + 14, cx + 5, y0 + 28], fill=GOLD_DARK)
    draw.ellipse([cx - 4, y0 + 8, cx + 4, y0 + 16], fill=GOLD_DARK)
    # Building body + columns.
    draw.rectangle([cx - 40, y0 + 78, cx + 40, base], fill=WHITE)
    draw.rectangle([cx - 40, y0 + 78, cx + 40, y0 + 86], fill=INK)
    for i in range(5):
        colx = cx - 32 + i * 16
        draw.rectangle([colx, y0 + 92, colx + 7, base - 12], fill=INK)
    draw.rectangle([cx - 44, base - 12, cx + 44, base], fill=INK)
    # Vote tally chips: 51 red, 48 blue, as small squares.
    for i in range(6):
        draw.rectangle([x0 + 8 + i * 7, y0 + 8, x0 + 13 + i * 7, y0 + 13],
                       fill=BRICK)
    for i in range(6):
        draw.rectangle([x1 - 13 - i * 7, y0 + 8, x1 - 8 - i * 7, y0 + 13],
                       fill=INK)


def art_drone(draw, x0, y0, x1, y1):
    """Long-range drone over a map line (UK drones for Ukraine)."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # Dashed flight path, bottom-left to top-right.
    for i in range(8):
        px = x0 + 8 + i * 11
        py = y1 - 26 - i * 11
        draw.line([px, py, px + 6, py - 6], fill=INK_SOFT, width=2)
    # Target ring at the end of the path.
    tx, ty = x0 + 84, y0 + 22
    draw.ellipse([tx - 8, ty - 8, tx + 8, ty + 8], outline=BRICK, width=3)
    draw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=BRICK)
    # Drone body: fuselage + wings + tail.
    dx, dy = x0 + 18, y1 - 78
    draw.polygon([(dx, dy + 8), (dx + 46, dy), (dx + 72, dy + 8),
                  (dx + 46, dy + 14)], fill=INK)
    draw.polygon([(dx + 30, dy - 10), (dx + 48, dy + 4), (dx + 36, dy + 10)],
                 fill=INK)
    draw.polygon([(dx + 58, dy + 2), (dx + 70, dy + 8), (dx + 58, dy + 12)],
                 fill=INK)
    # Propeller blur at the nose.
    draw.ellipse([dx + 68, dy - 2, dx + 80, dy + 18], outline=INK, width=2)
    # Ground line.
    draw.line([x0 + 6, y1 - 12, x1 - 6, y1 - 12], fill=INK_SOFT, width=2)


def art_market(draw, x0, y0, x1, y1):
    """Plunging red chart line (Taiwan stocks)."""
    draw.rectangle([x0, y0, x1, y1], fill=(246, 232, 228))
    # Grid lines.
    for gy in (y0 + 34, y0 + 68, y0 + 102):
        draw.line([x0 + 8, gy, x1 - 8, gy], fill=(228, 200, 192), width=1)
    # Plunging line, left high to right low.
    pts = [(x0 + 10, y0 + 26), (x0 + 30, y0 + 44), (x0 + 50, y0 + 40),
           (x0 + 70, y0 + 72), (x0 + 88, y0 + 96)]
    draw.line(pts, fill=BRICK, width=5, joint="curve")
    # Down arrow at the end.
    ex, ey = pts[-1]
    draw.polygon([(ex, ey + 14), (ex - 9, ey - 2), (ex + 9, ey - 2)],
                 fill=BRICK)
    # Big -6.2% tag.
    pct = font(BOLD, 26)
    draw.text((x0 + 10, y0 + 108), "-6.2%", font=pct, fill=BRICK)


def art_tower(draw, x0, y0, x1, y1):
    """PIF Tower with impact burst (Houthi strike on Riyadh)."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 226, 210))
    cx = (x0 + x1) // 2
    # Tower body, tapering top.
    draw.polygon([(cx - 26, y1 - 10), (cx - 26, y0 + 34),
                  (cx - 16, y0 + 14), (cx + 16, y0 + 14),
                  (cx + 26, y0 + 34), (cx + 26, y1 - 10)], fill=INK)
    # Window grid.
    for wy in range(y0 + 44, y1 - 16, 14):
        for wx in (cx - 20, cx - 6, cx + 8):
            draw.rectangle([wx, wy, wx + 8, wy + 7], fill=(140, 160, 190))
    # Impact burst near the top, gold-orange.
    bx, by = cx + 14, y0 + 52
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        ex = bx + int(16 * math.cos(rad))
        ey = by + int(16 * math.sin(rad))
        draw.line([bx, by, ex, ey], fill=(232, 122, 32), width=3)
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(232, 122, 32))
    # Smoke wisp.
    draw.ellipse([cx - 34, y0 + 30, cx - 18, y0 + 44], fill=(180, 172, 158))
    draw.ellipse([cx - 40, y0 + 18, cx - 26, y0 + 30], fill=(200, 192, 178))


def art_missile(draw, x0, y0, x1, y1):
    """Ballistic missile climbing over the sea (North Korea launch)."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_PANEL)
    stars = [(12, 14), (36, 34), (62, 12), (84, 30), (20, 66), (52, 92),
             (78, 72), (92, 108), (10, 116), (64, 126)]
    for sx, sy in stars:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                     fill=WHITE)
    # Sea at the bottom.
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(38, 80, 120))
    draw.line([x0, y1 - 26, x1, y1 - 26], fill=(120, 180, 220), width=2)
    # Missile body, angled up-right.
    mx, my = x0 + 22, y1 - 62
    draw.polygon([(mx, my), (mx + 26, my - 34), (mx + 34, my - 26),
                  (mx + 10, my + 8)], fill=WHITE)
    draw.polygon([(mx + 26, my - 34), (mx + 32, my - 42),
                  (mx + 38, my - 30)], fill=BRICK)
    # Flame + smoke trail.
    draw.polygon([(mx, my), (mx - 12, my + 14), (mx + 2, my + 18)],
                 fill=(232, 122, 32))
    draw.polygon([(mx, my), (mx - 18, my + 22), (mx - 4, my + 26)],
                 fill=GOLD)


def art_vangogh(draw, x0, y0, x1, y1):
    """Framed painting: chestnut trees over a village road (Van Gogh)."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 226, 196))
    # Frame.
    draw.rectangle([x0 + 8, y0 + 8, x1 - 8, y1 - 8], fill=GOLD_DARK)
    ix0, iy0, ix1, iy1 = x0 + 14, y0 + 14, x1 - 14, y1 - 14
    # Sky.
    draw.rectangle([ix0, iy0, ix1, iy1], fill=(168, 196, 228))
    # Sun.
    draw.ellipse([ix1 - 30, iy0 + 8, ix1 - 12, iy0 + 26], fill=GOLD)
    # Chestnut trees: green canopies with pink blossom dots.
    for tx in (ix0 + 14, ix0 + 38, ix0 + 62):
        draw.rectangle([tx + 6, iy0 + 52, tx + 10, iy1 - 26], fill=(90, 60, 30))
        draw.ellipse([tx - 4, iy0 + 22, tx + 22, iy0 + 54], fill=(60, 120, 60))
        draw.ellipse([tx + 2, iy0 + 28, tx + 8, iy0 + 34], fill=(240, 180, 200))
        draw.ellipse([tx + 12, iy0 + 36, tx + 18, iy0 + 42], fill=(240, 180, 200))
    # Village road.
    draw.polygon([(ix0, iy1), (ix1, iy1), (ix1 - 18, iy1 - 26),
                  (ix0 + 18, iy1 - 26)], fill=(214, 196, 158))
    # Price tag ribbon, bottom-left.
    draw.rectangle([ix0 + 2, iy1 - 24, ix0 + 52, iy1 - 8], fill=BRICK)
    tag = font(BOLD, 11)
    draw.text((ix0 + 5, iy1 - 22), "$190.4m", font=tag, fill=WHITE)


ART = {
    "senate": art_senate,
    "drone": art_drone,
    "market": art_market,
    "tower": art_tower,
    "missile": art_missile,
    "vangogh": art_vangogh,
}

PANELS = [
    ("US POLITICS", "SENATE REJECTS IRAN WAR-POWERS VOTE",
     "51-48 against ending the war; the House-passed measure falls.",
     "senate"),
    ("EUROPE", "UK SENDS 1,000 DRONES TO UKRAINE",
     "GBP 260m package; long-range drones fly 1,000 km.",
     "drone"),
    ("MARKETS", "TAIWAN PLUNGES 2,394 POINTS",
     "Taiex -6.2% to 36,033; worst week since 1990, down 18%.",
     "market"),
    ("MIDDLE EAST", "HOUTHI MISSILE HITS RIYADH TOWER",
     "PIF Tower, the tallest in Riyadh, damaged; no injuries.",
     "tower"),
    ("ASIA", "NORTH KOREA FIRES BALLISTIC MISSILE",
     "Launch from Wonsan toward the East Sea after allied drills.",
     "missile"),
    ("CULTURE", "VAN GOGH SELLS FOR $190.4 MILLION",
     "Blossoming Chestnut Trees sets a record for the artist.",
     "vangogh"),
]

MORE_TODAY = [
    ("US SANCTIONS COMANCHEROS, 'NDRANGHETA",
     "US assets frozen in cartel crackdown."),
    ("TRUMP PARDONS PETE ROSE",
     "Posthumous pardon for the late hit king, 4,256 hits."),
    ("UK-EU YOUTH MOBILITY DEAL",
     "Provisionally agree 100,000 places a year."),
]


def draw_panel(draw, x, y, w, h, tag, headline, caption, art_key):
    """One story panel: art strip left, tag + headline + caption right."""
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=BORDER, width=1)
    art_w = 104
    ART[art_key](draw, x, y, x + art_w, y + h)
    draw.line([x + art_w, y, x + art_w, y + h], fill=BORDER, width=1)
    tx = x + art_w + 16
    text_w = w - art_w - 16 - 14
    tag_chip(draw, tx, y + 12, tag)
    head_fnt = font(BOLD, 24)
    head_lines = wrap_text(draw, headline, head_fnt, text_w)
    y_cur = draw_lines(draw, tx, y + 44, head_lines, head_fnt, INK, 28)
    cap_fnt = font(REG, 18)
    cap_lines = wrap_text(draw, caption, cap_fnt, text_w)
    draw_lines(draw, tx, y_cur + 4, cap_lines, cap_fnt, INK_SOFT, 22)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Header band: the day, named big. ----
    draw.rectangle([0, 0, W, 120], fill=INK)
    sub = font(BOLD, 20)
    sub_text = "THE WORLD IN ONE DAY"
    sw = draw.textlength(sub_text, font=sub)
    draw.text(((W - sw) / 2, 14), sub_text, font=sub, fill=GOLD)
    date_fnt = font(BOLD, 62)
    date_text = "20 NOVEMBER 2026"
    dw = draw.textlength(date_text, font=date_fnt)
    draw.text(((W - dw) / 2, 42), date_text, font=date_fnt, fill=WHITE)
    draw.line([MARGIN, 116, W - MARGIN, 116], fill=GOLD, width=2)

    # ---- Hero: Anthropic closes up 17% on its debut. ----
    hy, hh = 132, 196
    draw.rectangle([MARGIN, hy, W - MARGIN, hy + hh], fill=WHITE,
                   outline=BORDER, width=1)
    art_hero(draw, MARGIN, hy, MARGIN + 320, hy + hh)
    draw.line([MARGIN + 320, hy, MARGIN + 320, hy + hh], fill=BORDER, width=1)
    hx = MARGIN + 320 + 20
    tag_chip(draw, hx, hy + 14, "TECH")
    hero_head = font(BOLD, 34)
    head = "ANTHROPIC CLOSES UP 17%"
    draw.text((hx, hy + 52), head, font=hero_head, fill=INK)
    draw.text((hx, hy + 96), "ON ITS NASDAQ DEBUT", font=hero_head, fill=INK)
    hero_cap = font(REG, 22)
    cap1 = "Opened +34% at $111.50, closed $97.17."
    cap2 = "Record $81.3bn IPO, priced at $83 a share."
    draw.text((hx, hy + 148), cap1, font=hero_cap, fill=INK_SOFT)
    draw.text((hx, hy + 176), cap2, font=hero_cap, fill=INK_SOFT)

    # ---- Grid: six more top stories. ----
    panel_w = (CONTENT_W - 12) // 2
    panel_h = 156
    grid_top = 340
    for i, (tag, headline, caption, art_key) in enumerate(PANELS):
        row, col = divmod(i, 2)
        px = MARGIN + col * (panel_w + 12)
        py = grid_top + row * (panel_h + 12)
        draw_panel(draw, px, py, panel_w, panel_h, tag, headline, caption,
                   art_key)

    # ---- "MORE TODAY" strip: three more stories, one line each. ----
    strip_y = 844
    strip_title = font(BOLD, 18)
    draw.text((MARGIN, strip_y), "MORE TODAY", font=strip_title, fill=BRICK)
    draw.line([MARGIN + 132, strip_y + 10, W - MARGIN, strip_y + 10],
              fill=GOLD, width=2)
    lead_fnt = font(BOLD, 19)
    rest_fnt = font(REG, 19)
    ly = strip_y + 28
    for lead, rest in MORE_TODAY:
        draw.text((MARGIN, ly), lead, font=lead_fnt, fill=INK)
        lw = draw.textlength(lead, font=lead_fnt)
        draw.text((MARGIN + lw + 10, ly), "- " + rest, font=rest_fnt,
                  fill=INK_SOFT)
        ly += 28

    # ---- Footer: the date again, one line. ----
    draw.line([MARGIN, 956, W - MARGIN, 956], fill=BORDER, width=1)
    foot = font(REG, 18)
    foot_text = "20 November 2026  -  World news, one day, one image."
    fw = draw.textlength(foot_text, font=foot)
    draw.text(((W - fw) / 2, 968), foot_text, font=foot, fill=MUTED)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
