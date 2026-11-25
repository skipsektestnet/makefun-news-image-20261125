#!/usr/bin/env python3
"""Generate the make.fun news-image-20261125 v3 entry: 'The World Today'.

Design (own work, pattern synthesis of the top-5 entries' shared traits):
- masthead + a top band of 3 big data headlines (Ref B pattern)
- 2x4 grid of 8 illustrated panels (Ref A pattern), each with a number badge,
  a data callout inside the illustration, a status badge (Ref C/E pattern),
  a location tag, a bold headline, a one-line summary and a source credit.
- 11 stories total, every one dated and sourced. All headlines, summaries and
  illustrations are written/drawn fresh here; no text or image is copied from
  any other entry. All facts verified against named sources on 25 Nov 2026.

Deterministic: Pillow + stdlib only, no network, no timestamps, no randomness.
Running twice produces byte-identical output.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
WHITE = (255, 255, 255)
INK = (20, 33, 61)
RED = (180, 35, 24)
GREEN = (30, 125, 50)
BLUE = (21, 101, 192)
AMBER = (166, 98, 0)
MUTED = (96, 96, 92)
RULE = (180, 175, 160)
PANEL_LINE = (205, 200, 185)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w, max_lines):
    """Greedy word wrap; raises if the text cannot fit in max_lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if not cur:
                raise ValueError(f"single word too wide: {word!r}")
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        raise ValueError(f"text needs {len(lines)} lines (max {max_lines}): {text!r}")
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=fnt, fill=fill)
    return y + len(lines) * lh


def pill(draw, box, fill):
    draw.rounded_rectangle(box, radius=9, fill=fill)


def badge(draw, x, y, text, fill):
    """Small status pill; returns its width."""
    fnt = SANS_B(11)
    w = int(draw.textlength(text, font=fnt)) + 16
    pill(draw, [x, y, x + w, y + 18], fill)
    draw.text((x + 8, y + 3), text, font=fnt, fill=WHITE)
    return w


# ---------------------------------------------------------------- stories
# Each panel: number, tag, tag colour, headline, summary, sources, badge,
# badge colour, data callout shown inside the illustration, scene key.
PANELS = [
    dict(n=1, tag="UNITED STATES · WASHINGTON", tc=RED,
         head="Hackers breach the CIA's open network",
         summ="Hackers hit the CIA's unclassified system for public material. No secrets touched.",
         src="NYT · REUTERS", badge="REPORTED", bc=AMBER,
         call="22:27 UTC", scene="cia"),
    dict(n=2, tag="MIDDLE EAST · RIYADH", tc=RED,
         head="Drone hits Riyadh's tallest tower again",
         summ="A Houthi drone struck the PIF Tower, the second hit in a week. Eleven were wounded.",
         src="REUTERS · AL JAZEERA", badge="CONFIRMED", bc=GREEN,
         call="11 WOUNDED", scene="riyadh"),
    dict(n=3, tag="EUROPE · GULF OF FINLAND", tc=BLUE,
         head="Ukraine says it hit a Russian cargo ship",
         summ="Kyiv confirms the drone strike on the Sparta II. Norway urges caution.",
         src="REUTERS · BLOOMBERG", badge="CONFIRMED", bc=GREEN,
         call="SHIP HIT", scene="sparta"),
    dict(n=4, tag="TECHNOLOGY · NEW YORK", tc=(107, 60, 140),
         head="Huawei guilty in US secrets trial",
         summ="A jury convicts Huawei on 10 of 12 counts, including bank fraud. It is cleared of racketeering.",
         src="DOJ · AFP", badge="CONFIRMED", bc=GREEN,
         call="10/12 GUILTY", scene="huawei"),
    dict(n=5, tag="AFRICA · DR CONGO", tc=(0, 122, 90),
         head="WHO pulls its Ebola team out of Ituri",
         summ="Staff leave a hospital in Akwe after three days sheltering from fighting in the Ebola zone.",
         src="WHO · REUTERS", badge="OFFICIAL", bc=BLUE,
         call="3 DAYS SHELTERED", scene="who"),
    dict(n=6, tag="EUROPE · ESKISEHIR", tc=BLUE,
         head="Army helicopter crashes, five killed",
         summ="A Turkish military helicopter comes down during a training flight. Five soldiers die.",
         src="DAILY SABAH", badge="CONFIRMED", bc=GREEN,
         call="5 KILLED", scene="heli"),
    dict(n=7, tag="EUROPE · PARIS", tc=BLUE,
         head="Sarkozy's Libya case goes to trial",
         summ="The former president must stand trial over alleged Libyan funding. First hearing: April 2027.",
         src="REUTERS", badge="OFFICIAL", bc=BLUE,
         call="1 APR 2027", scene="sarkozy"),
    dict(n=8, tag="TECHNOLOGY · CALIFORNIA", tc=(0, 122, 90),
         head="Nvidia brings back Jensen Huang",
         summ="The chipmaker reinstates Huang as chief executive days after his sudden exit.",
         src="AP · FT", badge="CONFIRMED", bc=GREEN,
         call="11 DAYS OUT", scene="nvidia"),
]

# Top band: three more stories (Ref B pattern). chip = big data figure.
TOP = [
    dict(chip="A$740M", cc=RED,
         head="Solomons pick Australia as top security partner",
         summ="Canberra pledges A$740m over a decade; Honiara rules out any foreign base.",
         src="REUTERS · ABC · GUARDIAN", badge="CONFIRMED", bc=GREEN),
    dict(chip="00:18 UTC", cc=INK,
         head="Shenzhou-24 lifts off with first foreign astronaut",
         summ="Pakistan's Zeeshan Ali joins the crew aboard Tiangong for 90+ tests.",
         src="XINHUA · AL JAZEERA", badge="OFFICIAL", bc=BLUE),
    dict(chip="16 PARTNERS", cc=RED,
         head="US readies new tariffs on 16 trading partners",
         summ="Levies target up to 20% on China and 15% or less on the EU and Japan.",
         src="REUTERS · AP", badge="REPORTED", bc=AMBER),
]

FOOTER = ("SOURCES: THE NEW YORK TIMES · REUTERS · ASSOCIATED PRESS · AFP · BBC · "
          "GUARDIAN · ABC · XINHUA · AL JAZEERA · DAILY SABAH · WHO · FT")


# ---------------------------------------------------------------- scenes
def scene_cia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 30, 58))
    for i in range(5):
        rx = x + 12 + i * (w - 24) // 5
        d.rectangle([rx, y + 10, rx + 26, y + h - 12], fill=(30, 48, 84))
        for j in range(4):
            col = (46, 204, 113) if (i + j) % 3 else (255, 176, 32)
            d.rectangle([rx + 5, y + 18 + j * 22, rx + 21, y + 28 + j * 22], fill=col)
    cx, cy = x + w // 2, y + h // 2 + 6
    d.polygon([(cx, cy - 34), (cx + 30, cy - 20), (cx + 30, cy + 8),
               (cx, cy + 34), (cx - 30, cy + 8), (cx - 30, cy - 20)],
              fill=(255, 176, 32), outline=(20, 33, 61))
    d.line([(cx - 4, cy - 18), (cx + 6, cy - 4), (cx - 6, cy + 4), (cx + 4, cy + 20)],
           fill=(20, 33, 61), width=4)


def scene_riyadh(d, x, y, w, h):
    for i, col in enumerate([(232, 126, 62), (214, 104, 58), (196, 88, 60), (58, 48, 72)]):
        d.rectangle([x, y + i * h // 4, x + w, y + (i + 1) * h // 4], fill=col)
    d.ellipse([x + w - 52, y + 12, x + w - 22, y + 42], fill=(255, 214, 130))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(44, 38, 58))
    for bx, bw, bh in [(8, 34, 52), (48, 26, 70), (170, 30, 58), (206, 22, 44)]:
        d.rectangle([x + bx, y + h - 34 - bh, x + bx + bw, y + h - 34], fill=(30, 26, 44))
    tx = x + w // 2 - 14
    d.polygon([(tx, y + h - 34), (tx + 10, y + 18), (tx + 28, y + 18),
               (tx + 28, y + h - 34)], fill=(24, 20, 36))
    for wy in range(y + 30, y + h - 40, 12):
        d.line([(tx + 13, wy), (tx + 25, wy)], fill=(255, 214, 130), width=3)
    for cx, cy, r in [(tx + 22, y + 8, 9), (tx + 34, y + 2, 7), (tx + 12, y + 14, 6)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 116, 120))
    d.line([(x + w - 78, y + 26), (x + w - 58, y + 26)], fill=(20, 33, 61), width=3)
    d.line([(x + w - 68, y + 20), (x + w - 68, y + 32)], fill=(20, 33, 61), width=3)


def scene_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 200, 220))
    d.rectangle([x, y + h * 2 // 3, x + w, y + h], fill=(38, 90, 140))
    for wy in (y + h * 2 // 3 + 8, y + h - 22):
        for k in range(4):
            d.arc([x + k * 62 - 10, wy - 8, x + k * 62 + 34, wy + 8],
                  start=180, end=360, fill=(255, 255, 255), width=3)
    d.polygon([(x + 28, y + h - 46), (x + w - 30, y + h - 46),
               (x + w - 52, y + h - 16), (x + 50, y + h - 16)], fill=(24, 28, 40))
    for cx, col in [(78, (214, 69, 65)), (118, (46, 160, 90)), (156, (255, 176, 32))]:
        d.rectangle([x + cx, y + h - 78, x + cx + 30, y + h - 48], fill=col)
    d.rectangle([x + w - 44, y + h - 86, x + w - 22, y + h - 48], fill=(240, 240, 235))
    for sx, sy in [(x + w - 34, y + 22), (x + w - 22, y + 34), (x + w - 46, y + 36)]:
        d.line([(sx - 8, sy), (sx + 8, sy)], fill=(255, 255, 255), width=2)
        d.line([(sx, sy - 8), (sx, sy + 8)], fill=(255, 255, 255), width=2)


def scene_huawei(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
    d.polygon([(x + 20, y + 52), (x + w // 2, y + 16), (x + w - 20, y + 52)], fill=(196, 176, 138))
    for i in range(4):
        cx = x + 34 + i * (w - 68) // 3
        d.rectangle([cx - 8, y + 54, cx + 8, y + h - 34], fill=(214, 196, 158))
    d.rectangle([x + 16, y + h - 34, x + w - 16, y + h - 24], fill=(196, 176, 138))
    d.rectangle([x + w // 2 - 34, y + h - 78, x + w // 2 + 34, y + h - 22],
                fill=(24, 28, 40))
    d.rectangle([x + w // 2 - 18, y + h - 64, x + w // 2 + 18, y + h - 36],
                fill=(46, 204, 113))
    d.rectangle([x + w // 2 - 8, y + h - 54, x + w // 2 + 8, y + h - 46], fill=(24, 28, 40))
    for px in (x + w // 2 - 40, x + w // 2 + 34):
        for py in (y + h - 70, y + h - 52, y + h - 34):
            d.line([(px, py), (px + 6, py)], fill=(46, 204, 113), width=2)


def scene_who(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 208))
    d.polygon([(x, y + h), (x + w // 2, y + h - 52), (x + w, y + h)], fill=(120, 170, 110))
    d.rectangle([x + 34, y + 52, x + w - 40, y + h - 26], fill=(255, 255, 255))
    d.rectangle([x + 34, y + 52, x + w - 40, y + 66], fill=(0, 122, 90))
    for wx in (x + 52, x + 92, x + 132):
        d.rectangle([wx, y + 82, wx + 22, y + 104], fill=(90, 140, 170))
    d.rectangle([x + w // 2 - 6, y + 30, x + w // 2 + 6, y + 52], fill=(0, 160, 90))
    d.rectangle([x + w // 2 - 16, y + 38, x + w // 2 + 16, y + 50], fill=(0, 160, 90))
    for fx in (x + w - 52, x + w - 34):
        d.ellipse([fx - 5, y + h - 52, fx + 5, y + h - 42], fill=(40, 40, 40))
        d.line([(fx, y + h - 42), (fx, y + h - 18)], fill=(40, 40, 40), width=3)
        d.line([(fx, y + h - 18), (fx - 6, y + h - 6)], fill=(40, 40, 40), width=3)
        d.line([(fx, y + h - 18), (fx + 6, y + h - 6)], fill=(40, 40, 40), width=3)


def scene_heli(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 188))
    d.polygon([(x, y + h), (x + w // 3, y + h - 62), (x + 2 * w // 3, y + h - 34),
               (x + w, y + h - 58), (x + w, y + h), (x, y + h)], fill=(150, 118, 80))
    d.polygon([(x, y + h), (x + w // 4, y + h - 40), (x + w // 2, y + h - 18),
               (x + 3 * w // 4, y + h - 30), (x + w, y + h)], fill=(120, 94, 62))
    cx, cy = x + w // 2 - 6, y + 74
    d.ellipse([cx - 34, cy - 12, cx + 26, cy + 12], fill=(40, 44, 52))
    d.rectangle([cx + 24, cy - 4, cx + 66, cy + 2], fill=(40, 44, 52))
    d.rectangle([cx + 58, cy - 16, cx + 66, cy + 12], fill=(40, 44, 52))
    d.line([(cx - 44, cy - 20), (cx + 34, cy - 20)], fill=(40, 44, 52), width=4)
    d.line([(cx - 12, cy - 20), (cx - 12, cy - 12)], fill=(40, 44, 52), width=3)
    for sx, sy, r in [(cx - 30, y + 22, 10), (cx - 12, y + 10, 8), (cx + 4, y + 28, 7)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(110, 106, 104))


def scene_sarkozy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 220, 232))
    d.polygon([(x + 24, y + 46), (x + w // 2, y + 14), (x + w - 24, y + 46)], fill=(176, 164, 132))
    for i in range(4):
        cx = x + 38 + i * (w - 76) // 3
        d.rectangle([cx - 9, y + 48, cx + 9, y + h - 28], fill=(232, 222, 200))
    d.rectangle([x + 20, y + h - 28, x + w - 20, y + h - 18], fill=(176, 164, 132))
    d.line([(x + 22, y + 12), (x + 22, y + 52)], fill=(60, 60, 60), width=3)
    for i, col in enumerate([(0, 85, 164), (255, 255, 255), (239, 65, 53)]):
        d.rectangle([x + 25, y + 12 + i * 9, x + 45, y + 21 + i * 9], fill=col)


def scene_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 24, 40))
    cx, cy = x + w // 2 - 12, y + h // 2 + 4
    d.rectangle([cx - 40, cy - 34, cx + 40, cy + 34], fill=(20, 52, 32))
    d.rectangle([cx - 26, cy - 20, cx + 26, cy + 20], fill=(118, 200, 80))
    d.rectangle([cx - 12, cy - 8, cx + 12, cy + 8], fill=(14, 24, 40))
    for px in range(cx - 34, cx + 35, 12):
        d.line([(px, cy - 44), (px, cy - 36)], fill=(118, 200, 80), width=3)
        d.line([(px, cy + 36), (px, cy + 44)], fill=(118, 200, 80), width=3)
    ax = x + w - 44
    d.line([(ax, y + h - 40), (ax, y + 34)], fill=(118, 200, 80), width=6)
    d.polygon([(ax - 12, y + 46), (ax + 12, y + 46), (ax, y + 26)], fill=(118, 200, 80))
    for ex, ey in [(x + 24, y + 30), (x + 30, y + h - 30), (x + w - 30, y + h - 44)]:
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(118, 200, 80))
        d.line([(ex, ey), (ex + 12, ey + 8)], fill=(118, 200, 80), width=2)


SCENES = dict(cia=scene_cia, riyadh=scene_riyadh, sparta=scene_sparta,
             huawei=scene_huawei, who=scene_who, heli=scene_heli,
             sarkozy=scene_sarkozy, nvidia=scene_nvidia)


# ---------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)

    # masthead
    d.text((24, 16), "WEDNESDAY, 25 NOVEMBER 2026", font=SANS_B(15), fill=INK)
    right = "11 STORIES · EVERY ONE SOURCED"
    d.text((W - 24 - d.textlength(right, font=SANS_B(13)), 18), right,
           font=SANS_B(13), fill=MUTED)
    d.text((24, 36), "THE WORLD TODAY", font=SERIF_B(56), fill=INK)
    d.line([(24, 100), (W - 24, 100)], fill=INK, width=2)
    d.line([(24, 104), (W - 24, 104)], fill=INK, width=1)

    # top band: three big data headlines
    d.text((24, 110), "TOP OF THE DAY", font=SANS_B(12), fill=RED)
    col_w = (W - 48 - 2 * 14) // 3
    for i, t in enumerate(TOP):
        cx = 24 + i * (col_w + 14)
        cy = 128
        chip_w = int(d.textlength(t["chip"], font=SANS_B(15))) + 18
        pill(d, [cx, cy, cx + chip_w, cy + 22], t["cc"])
        d.text((cx + 9, cy + 3), t["chip"], font=SANS_B(15), fill=WHITE)
        badge(d, cx + col_w - 76, cy + 2, t["badge"], t["bc"])
        head_lines = wrap(d, t["head"], SERIF_B(18), col_w, 2)
        y = draw_lines(d, head_lines, cx, cy + 27, SERIF_B(18), INK, 22)
        sum_lines = wrap(d, t["summ"], SANS(12), col_w, 2)
        y = draw_lines(d, sum_lines, cx, y + 3, SANS(12), (60, 60, 58), 15)
        d.text((cx, y + 4), t["src"], font=SANS(10), fill=MUTED)
        if i < 2:
            d.line([(cx + col_w + 7, 128), (cx + col_w + 7, 244)], fill=RULE, width=1)
    d.line([(24, 250), (W - 24, 250)], fill=INK, width=2)

    # grid: 2 rows x 4 panels
    gx, gy = 24, 258
    pw = (W - 48 - 3 * 12) // 4
    ph = 362
    for i, p in enumerate(PANELS):
        px = gx + (i % 4) * (pw + 12)
        py = gy + (i // 4) * (ph + 12)
        d.rectangle([px, py, px + pw, py + ph], outline=PANEL_LINE, width=1)
        ih = 152
        SCENES[p["scene"]](d, px + 1, py + 1, pw - 1, ih)
        # number badge
        d.ellipse([px + 8, py + 8, px + 32, py + 32], fill=INK)
        num = str(p["n"])
        d.text((px + 20 - d.textlength(num, font=SANS_B(14)) / 2, py + 12),
               num, font=SANS_B(14), fill=WHITE)
        # status badge, top right of the illustration
        bw = int(d.textlength(p["badge"], font=SANS_B(11))) + 16
        pill(d, [px + pw - 8 - bw, py + 10, px + pw - 8, py + 28], p["bc"])
        d.text((px + pw - 8 - bw + 8, py + 13), p["badge"], font=SANS_B(11), fill=WHITE)
        # data callout chip, bottom-left inside the illustration
        cw = int(d.textlength(p["call"], font=SANS_B(12))) + 16
        pill(d, [px + 8, py + ih - 28, px + 8 + cw, py + ih - 8], (20, 33, 61))
        d.text((px + 16, py + ih - 24), p["call"], font=SANS_B(12), fill=(255, 214, 130))
        # text block
        tx = px + 8
        ty = py + ih + 10
        d.text((tx, ty), p["tag"], font=SANS_B(12), fill=p["tc"])
        head_lines = wrap(d, p["head"], SERIF_B(18), pw - 16, 3)
        y = draw_lines(d, head_lines, tx, ty + 20, SERIF_B(18), INK, 22)
        sum_lines = wrap(d, p["summ"], SANS(12), pw - 16, 3)
        y = draw_lines(d, sum_lines, tx, y + 4, SANS(12), (60, 60, 58), 15)
        d.text((tx, py + ph - 18), p["src"], font=SANS(10), fill=MUTED)
        d.text((px + pw - 8 - d.textlength("25 NOV", font=SANS_B(10)), py + ph - 18),
               "25 NOV", font=SANS_B(10), fill=MUTED)

    # footer
    d.text(((W - d.textlength(FOOTER, font=SANS(11))) / 2, 998), FOOTER,
           font=SANS(11), fill=MUTED)
    return img


if __name__ == "__main__":
    out = os.environ.get("OUT", "entry.png")
    main().save(out, format="PNG")
    print(f"wrote {out}")
