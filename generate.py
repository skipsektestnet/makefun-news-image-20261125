"""Draw the 25 November 2026 world-news front page: eight illustrated scenes.

One image, 1024x1024, drawn entirely with Pillow: no network, no random
numbers, no timestamps, so every run writes identical bytes.

Layout (the "day in eight" front-page pattern): a dateline strip and a
masthead on top, then eight story panels in two rows of four. Every panel
has its own flat illustration, a number badge, a region/topic/city tag, a
short headline, a one-line summary and a source credit. The eight stories
were picked from what the wires reported on Wednesday 25 November 2026.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
MUTED = (90, 90, 90)
RULE = (26, 35, 63)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    """Vertical gradient across box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)


def skyline(draw, box, color, heights):
    """Dark building silhouettes along the bottom of box."""
    x0, y0, x1, y1 = box
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx = x0 + i * bw
        draw.rectangle([bx + 1, y1 - h, bx + bw - 1, y1], fill=color)


def person(draw, x, y, s, color):
    """Tiny standing figure: head dot + body line."""
    draw.ellipse([x - s * 0.22, y - s * 1.5, x + s * 0.22, y - s * 1.06], fill=color)
    draw.line([(x, y - s * 1.05), (x, y)], fill=color, width=max(2, int(s * 0.14)))
    draw.line([(x, y), (x - s * 0.3, y + s * 0.55)], fill=color, width=max(2, int(s * 0.12)))
    draw.line([(x, y), (x + s * 0.3, y + s * 0.55)], fill=color, width=max(2, int(s * 0.12)))


# ---------------------------------------------------------------- scenes
# Each scene draws a flat illustration inside box (x0, y0, x1, y1).

def scene_hack(draw, b):
    x0, y0, x1, y1 = b
    vgrad(draw, b, (24, 38, 66), (10, 16, 32))
    # server racks
    for i, sx in enumerate(range(x0 + 12, x1 - 30, 34)):
        draw.rectangle([sx, y0 + 26, sx + 26, y1 - 18], fill=(30, 48, 80))
        for r in range(4):
            draw.rectangle([sx + 5, y0 + 34 + r * 14, sx + 21, y0 + 40 + r * 14],
                           fill=(90, 200, 120) if (i + r) % 3 else (230, 170, 60))
    # cracked shield in the middle
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 8
    draw.polygon([(cx - 34, cy - 30), (cx + 34, cy - 30), (cx + 34, cy + 6),
                  (cx, cy + 38), (cx - 34, cy + 6)], fill=(214, 178, 74))
    draw.line([(cx + 8, cy - 28), (cx - 4, cy - 8), (cx + 10, cy + 4),
               (cx - 6, cy + 22)], fill=(22, 35, 63), width=4)
    draw.ellipse([cx - 5, cy - 18, cx + 5, cy - 8], fill=(22, 35, 63))


def scene_tower(draw, b):
    x0, y0, x1, y1 = b
    vgrad(draw, b, (232, 150, 104), (122, 74, 94))
    draw.ellipse([x1 - 52, y0 + 14, x1 - 26, y0 + 40], fill=(244, 214, 150))
    skyline(draw, (x0, y0 + 96, x1, y1), (52, 44, 66), [46, 70, 38, 58, 44])
    # PIF tower: tall tapered slab, centre
    cx = (x0 + x1) // 2
    draw.polygon([(cx - 26, y1), (cx - 16, y0 + 30), (cx + 16, y0 + 30),
                  (cx + 26, y1)], fill=(38, 34, 52))
    for r in range(5):
        wy = y0 + 44 + r * 16
        draw.line([(cx - 14, wy), (cx + 14, wy)], fill=(244, 200, 110), width=2)
    # smoke + small drone
    for i, (sx, sy, sr) in enumerate([(cx - 6, y0 + 22, 9), (cx + 8, y0 + 12, 12),
                                      (cx + 2, y0 + 2, 8)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 110, 118))
    draw.line([(cx + 44, y0 + 40), (cx + 58, y0 + 40)], fill=(30, 28, 40), width=3)
    draw.line([(cx + 51, y0 + 33), (cx + 51, y0 + 47)], fill=(30, 28, 40), width=3)


def scene_ship(draw, b):
    x0, y0, x1, y1 = b
    vgrad(draw, (x0, y0, x1, y0 + 92), (207, 216, 220), (159, 179, 192))
    draw.rectangle([x0, y0 + 92, x1, y1], fill=(61, 107, 142))
    for i in range(3):
        wy = y0 + 112 + i * 18
        draw.arc([x0 + 8 + i * 30, wy, x0 + 70 + i * 30, wy + 14],
                 200, 340, fill=(200, 220, 232), width=3)
    # cargo ship
    sx, sy = x0 + 42, y0 + 108
    draw.polygon([(sx, sy), (sx + 150, sy), (sx + 138, sy + 30), (sx + 12, sy + 30)],
                 fill=(32, 40, 56))
    for i, cc in enumerate([(178, 90, 60), (90, 140, 90), (200, 170, 80)]):
        draw.rectangle([sx + 18 + i * 34, sy - 26, sx + 46 + i * 34, sy - 2], fill=cc)
    draw.rectangle([sx + 118, sy - 44, sx + 138, sy - 2], fill=(220, 220, 210))
    # drone + impact splash
    draw.line([(sx + 128, sy - 58), (sx + 142, sy - 58)], fill=(30, 30, 36), width=3)
    draw.line([(sx + 135, sy - 65), (sx + 135, sy - 51)], fill=(30, 30, 36), width=3)
    for a in range(6):
        import math
        ang = a * 1.047
        ex, ey = sx + 150 + int(14 * math.cos(ang)), sy + 8 + int(10 * math.sin(ang))
        draw.line([(sx + 150, sy + 8), (ex, ey)], fill=(235, 240, 244), width=2)


def scene_trial(draw, b):
    x0, y0, x1, y1 = b
    vgrad(draw, b, (216, 207, 192), (190, 178, 158))
    # courthouse: pediment + columns
    cx = (x0 + x1) // 2
    draw.polygon([(cx - 78, y0 + 52), (cx + 78, y0 + 52), (cx, y0 + 16)], fill=(164, 150, 124))
    draw.rectangle([x0 + 18, y0 + 52, x1 - 18, y0 + 60], fill=(140, 126, 100))
    for i in range(4):
        px = x0 + 30 + i * 48
        draw.rectangle([px, y0 + 60, px + 16, y1 - 30], fill=(196, 184, 160))
    draw.rectangle([x0 + 14, y1 - 30, x1 - 14, y1 - 18], fill=(140, 126, 100))
    # chip on the steps
    draw.rectangle([cx - 26, y1 - 62, cx + 26, y1 - 14], fill=(52, 44, 66))
    draw.rectangle([cx - 14, y1 - 50, cx + 14, y1 - 26], fill=(120, 170, 90))
    for i in range(3):
        draw.line([(cx - 32, y1 - 52 + i * 12), (cx - 26, y1 - 52 + i * 12)],
                  fill=(52, 44, 66), width=3)
        draw.line([(cx + 26, y1 - 52 + i * 12), (cx + 32, y1 - 52 + i * 12)],
                  fill=(52, 44, 66), width=3)


def scene_hospital(draw, b):
    x0, y0, x1, y1 = b
    vgrad(draw, (x0, y0, x1, y0 + 90), (232, 220, 192), (210, 196, 160))
    draw.polygon([(x0, y1), (x0, y1 - 52), (x0 + 90, y1 - 78), (x1, y1 - 52), (x1, y1)],
                 fill=(122, 154, 90))
    draw.polygon([(x0, y1), (x0, y1 - 34), (x0 + 120, y1 - 58), (x1, y1 - 30), (x1, y1)],
                 fill=(93, 127, 71))
    # hospital block + cross
    hx, hy = x0 + 52, y0 + 78
    draw.rectangle([hx, hy, hx + 110, y1 - 26], fill=(240, 238, 230))
    draw.rectangle([hx + 44, hy - 22, hx + 66, hy], fill=(240, 238, 230))
    draw.rectangle([hx + 50, hy - 14, hx + 60, hy + 8], fill=(46, 130, 90))
    draw.rectangle([hx + 42, hy - 6, hx + 68, hy + 2], fill=(46, 130, 90))
    for i in range(3):
        draw.rectangle([hx + 10 + i * 32, hy + 18, hx + 26 + i * 32, hy + 34],
                       fill=(90, 120, 140))
    person(draw, x1 - 44, y1 - 26, 20, (40, 40, 48))
    person(draw, x1 - 66, y1 - 26, 18, (40, 40, 48))


def scene_crash(draw, b):
    x0, y0, x1, y1 = b
    vgrad(draw, b, (217, 201, 168), (176, 158, 120))
    draw.polygon([(x0, y1), (x0, y1 - 46), (x0 + 110, y1 - 84), (x1, y1 - 40), (x1, y1)],
                 fill=(120, 104, 70))
    draw.polygon([(x0, y1), (x0, y1 - 26), (x0 + 140, y1 - 52), (x1, y1 - 22), (x1, y1)],
                 fill=(96, 84, 56))
    # smoke column
    for i, (sx, sy, sr) in enumerate([(150, 96, 10), (158, 74, 13), (146, 52, 15),
                                      (156, 30, 12)]):
        draw.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                     fill=(110, 104, 100))
    # tilted helicopter
    hx, hy = x0 + 118, y0 + 118
    draw.ellipse([hx - 26, hy - 10, hx + 26, hy + 10], fill=(52, 52, 60))
    draw.polygon([(hx + 22, hy - 4), (hx + 52, hy - 12), (hx + 52, hy - 4),
                  (hx + 22, hy + 2)], fill=(52, 52, 60))
    draw.line([(hx - 34, hy - 16), (hx + 34, hy - 16)], fill=(52, 52, 60), width=4)
    draw.line([(hx - 6, hy + 10), (hx - 14, hy + 26)], fill=(52, 52, 60), width=3)


def scene_paris(draw, b):
    x0, y0, x1, y1 = b
    vgrad(draw, b, (207, 212, 216), (176, 182, 188))
    cx = (x0 + x1) // 2
    draw.polygon([(cx - 74, y0 + 58), (cx + 74, y0 + 58), (cx, y0 + 22)], fill=(150, 138, 116))
    draw.rectangle([x0 + 22, y0 + 58, x1 - 22, y0 + 66], fill=(128, 116, 96))
    for i in range(4):
        px = x0 + 34 + i * 46
        draw.rectangle([px, y0 + 66, px + 15, y1 - 34], fill=(188, 176, 152))
    for i in range(3):
        draw.rectangle([x0 + 14, y1 - 34 + i * 8, x1 - 14, y1 - 28 + i * 8],
                       fill=(150, 138, 116))
    # small tricolore on a pole
    fx = x0 + 30
    draw.line([(fx, y0 + 18), (fx, y0 + 58)], fill=(60, 60, 66), width=3)
    draw.rectangle([fx, y0 + 18, fx + 12, y0 + 32], fill=(36, 68, 150))
    draw.rectangle([fx + 12, y0 + 18, fx + 24, y0 + 32], fill=(240, 240, 236))
    draw.rectangle([fx + 24, y0 + 18, fx + 36, y0 + 32], fill=(190, 60, 60))


def scene_chip(draw, b):
    x0, y0, x1, y1 = b
    vgrad(draw, b, (26, 32, 40), (12, 16, 22))
    # circuit traces
    for i, (tx, ty) in enumerate([(30, 40), (180, 30), (40, 150), (190, 140)]):
        draw.line([(x0 + tx, y0 + ty), (x0 + tx + 26, y0 + ty + 18)],
                  fill=(60, 90, 70), width=2)
        draw.ellipse([x0 + tx + 22, y0 + ty + 14, x0 + tx + 30, y0 + ty + 22],
                     fill=(118, 185, 0))
    # big chip, centre
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 6
    draw.rectangle([cx - 52, cy - 40, cx + 52, cy + 40], fill=(30, 38, 30))
    draw.rectangle([cx - 38, cy - 26, cx + 38, cy + 26], fill=(118, 185, 0))
    draw.rectangle([cx - 20, cy - 12, cx + 20, cy + 12], fill=(30, 38, 30))
    for i in range(5):
        px = cx - 44 + i * 22
        draw.line([(px, cy - 52), (px, cy - 40)], fill=(160, 170, 160), width=3)
        draw.line([(px, cy + 40), (px, cy + 52)], fill=(160, 170, 160), width=3)
    # rising arrow
    draw.line([(cx + 62, cy + 26), (cx + 62, cy - 18), (cx + 62, cy - 18)],
              fill=(118, 185, 0), width=5)
    draw.polygon([(cx + 52, cy - 14), (cx + 72, cy - 14), (cx + 62, cy - 30)],
                 fill=(118, 185, 0))


SCENES = [scene_hack, scene_tower, scene_ship, scene_trial,
          scene_hospital, scene_crash, scene_paris, scene_chip]

STORIES = [
    ("UNITED STATES · WASHINGTON", (168, 52, 52),
     "Hackers breach the CIA's open network",
     "Hackers hit the CIA's unclassified system for public material. No secrets touched.",
     "NYT · REUTERS"),
    ("MIDDLE EAST · RIYADH", (168, 52, 52),
     "Drone hits Riyadh's tallest tower again",
     "A Houthi drone struck the PIF Tower, the second hit in a week. Eleven were wounded.",
     "REUTERS · AL JAZEERA"),
    ("EUROPE · GULF OF FINLAND", (40, 80, 130),
     "Ukraine says it hit a Russian cargo ship",
     "Kyiv confirms the drone strike on the Sparta II. Norway urges caution.",
     "REUTERS · BLOOMBERG"),
    ("TECHNOLOGY · NEW YORK", (110, 60, 130),
     "Huawei guilty in US secrets trial",
     "A jury convicts Huawei on 10 of 12 counts, including bank fraud. It is cleared of racketeering.",
     "DOJ · AFP"),
    ("AFRICA · DR CONGO", (30, 110, 80),
     "WHO pulls its Ebola team out of Ituri",
     "Staff leave a hospital in Akwe after three days sheltering from fighting in the Ebola zone.",
     "WHO · REUTERS"),
    ("EUROPE · ESKISEHIR", (40, 80, 130),
     "Army helicopter crashes, five killed",
     "A Turkish military helicopter comes down during a training flight. Five soldiers die.",
     "DAILY SABAH"),
    ("EUROPE · PARIS", (40, 80, 130),
     "Sarkozy's Libya case goes to trial",
     "The former president must stand trial over alleged Libyan funding. First hearing: April 2027.",
     "REUTERS"),
    ("TECHNOLOGY · CALIFORNIA", (90, 140, 40),
     "Nvidia brings back Jensen Huang",
     "The chipmaker reinstates Huang as chief executive days after his sudden exit.",
     "AP · FT"),
]


def draw_panel(draw, idx, x, y, w, h):
    tag, accent, headline, summary, source = STORIES[idx]
    # illustration
    ix0, iy0, ix1, iy1 = x, y, x + w, y + 182
    SCENES[idx](draw, (ix0, iy0, ix1, iy1))
    draw.rectangle([ix0, iy0, ix1, iy1], outline=(60, 60, 60), width=1)
    # number badge
    bx, by = x + 18, y + 18
    draw.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=NAVY)
    nf = SANS_BOLD(15)
    tw = draw.textlength(str(idx + 1), font=nf)
    draw.text((bx - tw / 2, by - 8), str(idx + 1), font=nf, fill=(255, 255, 255))
    # tag with accent square
    ty = y + 196
    draw.rectangle([x, ty + 1, x + 9, ty + 10], fill=accent)
    tf = SANS_BOLD(12)
    draw.text((x + 14, ty), tag, font=tf, fill=accent)
    # headline
    hf = SERIF_BOLD(25)
    lines = wrap(draw, headline, hf, w)[:3]
    hy = ty + 22
    for ln in lines:
        draw.text((x, hy), ln, font=hf, fill=INK)
        hy += 30
    # summary
    sf = SANS(14)
    slines = wrap(draw, summary, sf, w)[:3]
    sy = hy + 6
    for ln in slines:
        draw.text((x, sy), ln, font=sf, fill=(74, 74, 74))
        sy += 18
    # source credit, pinned to panel bottom
    cf = SANS(11)
    draw.text((x, y + h - 16), source, font=cf, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # outer border
    draw.rectangle([10, 10, W - 11, H - 11], outline=RULE, width=3)
    # dateline strip
    df = SANS_BOLD(17)
    draw.text((28, 26), "WEDNESDAY, 25 NOVEMBER 2026", font=df, fill=NAVY)
    rf = SANS(15)
    right = "8 STORIES · EVERY ONE SOURCED"
    draw.text((W - 28 - draw.textlength(right, font=rf), 28), right, font=rf, fill=MUTED)
    draw.line([(28, 56), (W - 28, 56)], fill=RULE, width=2)
    # masthead
    mf = SERIF_BOLD(56)
    draw.text((28, 66), "THE WORLD IN EIGHT", font=mf, fill=NAVY)
    draw.line([(28, 136), (W - 28, 136)], fill=RULE, width=2)
    draw.line([(28, 141), (W - 28, 141)], fill=RULE, width=1)
    # grid: 2 rows x 4 cols
    gx, gy = 28, 156
    gw = (W - 2 * 28 - 3 * 12) // 4
    gh = 384
    for i in range(8):
        px = gx + (i % 4) * (gw + 12)
        py = gy + (i // 4) * (gh + 12)
        draw_panel(draw, i, px, py, gw, gh)
    # footer
    fy = gy + 2 * gh + 12 + 18
    ff = SANS(13)
    foot = "SOURCES: THE NEW YORK TIMES · REUTERS · ASSOCIATED PRESS · AFP · BBC · WHO"
    draw.text(((W - draw.textlength(foot, font=ff)) / 2, fy), foot, font=ff, fill=MUTED)
    img.save("entry.png")


if __name__ == "__main__":
    main()
