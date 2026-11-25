#!/usr/bin/env python3
"""Draw the front page of Wednesday 25 November 2026 as one 1024x1024 image.

Deterministic: no network, no clock, no randomness. Pillow only.
Writes entry.png next to this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

PAPER = (247, 243, 234)
NAVY = (16, 35, 63)
NAVY_DARK = (10, 24, 44)
GOLD = (201, 162, 39)
RED = (179, 38, 30)
INK = (26, 26, 26)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)
STEEL = (31, 78, 121)
PURPLE = (108, 52, 131)
TEAL = (14, 124, 107)
TICKER = (159, 176, 195)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 22)
F_KICKER = font("DejaVuSans-Bold.ttf", 15)
F_TAG = font("DejaVuSans-Bold.ttf", 14)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 33)
F_LEAD_BODY = font("DejaVuSans.ttf", 18)
F_PANEL_HEAD = font("DejaVuSans-Bold.ttf", 20)
F_PANEL_BODY = font("DejaVuSans.ttf", 15)
F_PANEL_TAG = font("DejaVuSans-Bold.ttf", 12)
F_DIGEST_HEAD = font("DejaVuSans-Bold.ttf", 17)
F_DIGEST = font("DejaVuSans.ttf", 18)
F_DIGEST_B = font("DejaVuSans-Bold.ttf", 18)
F_TICKER = font("DejaVuSans.ttf", 15)
F_FOOT = font("DejaVuSans.ttf", 12)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w pixels."""
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


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def shield(draw, cx, cy, s, fill):
    """Shield outline with a lightning crack and a gold keyhole."""
    pts = [
        (cx - s, cy - s * 0.85),
        (cx + s, cy - s * 0.85),
        (cx + s, cy + s * 0.15),
        (cx, cy + s),
        (cx - s, cy + s * 0.15),
    ]
    draw.polygon(pts, fill=fill)
    crack = [
        (cx + 2, cy - s * 0.62),
        (cx - 12, cy - s * 0.12),
        (cx + 4, cy + s * 0.05),
        (cx - 6, cy + s * 0.55),
    ]
    draw.line(crack, fill=(255, 255, 255), width=4, joint="curve")
    draw.ellipse(
        (cx + 14 - 6, cy - s * 0.62 - 6, cx + 14 + 6, cy - s * 0.62 + 6),
        fill=GOLD,
    )
    draw.rectangle((cx + 11, cy - s * 0.62 + 2, cx + 17, cy - s * 0.62 + 14), fill=GOLD)


def tower(draw, cx, cy, s):
    """Tapering skyscraper with dark windows and a small drone above it."""
    top = cy - s * 0.92
    base = cy + s * 0.95
    draw.polygon(
        [(cx - s * 0.5, base), (cx - s * 0.26, top), (cx + s * 0.26, top), (cx + s * 0.5, base)],
        fill=(255, 255, 255),
    )
    for row in range(5):
        wy = top + 9 + row * 11
        half = s * 0.5 - (base - wy) * 0.12
        draw.line((cx - half, wy, cx + half, wy), fill=NAVY, width=2)
    # drone: body + two rotors, clear of the tower
    dx, dy = cx + s * 0.78, cy - s * 0.62
    draw.ellipse((dx - 6, dy - 3, dx + 6, dy + 3), fill=(255, 255, 255))
    draw.line((dx - 12, dy - 6, dx + 12, dy - 6), fill=(255, 255, 255), width=2)
    draw.line((dx - 8, dy + 3, dx - 14, dy + 10), fill=(255, 255, 255), width=2)


def ship(draw, cx, cy, s):
    """Cargo ship with containers, a mast and waves, plus a drone overhead."""
    draw.polygon(
        [
            (cx - s, cy + s * 0.25),
            (cx + s, cy + s * 0.25),
            (cx + s * 0.72, cy + s * 0.72),
            (cx - s * 0.72, cy + s * 0.72),
        ],
        fill=(255, 255, 255),
    )
    for i, off in enumerate((-s * 0.55, 0, s * 0.55)):
        c = (255, 255, 255) if i != 1 else GOLD
        draw.rectangle(
            (cx + off - 11, cy - s * 0.42, cx + off + 11, cy + s * 0.1), fill=c
        )
    draw.line((cx + s * 0.55, cy - s * 0.42, cx + s * 0.55, cy - s * 0.85),
              fill=(255, 255, 255), width=3)
    # waves
    for wy in (cy + s * 0.9, cy + s + 6):
        draw.arc(
            (cx - s, wy - 5, cx - s * 0.3, wy + 5), 180, 360, fill=(255, 255, 255), width=2
        )
        draw.arc(
            (cx + s * 0.3, wy - 5, cx + s, wy + 5), 180, 360, fill=(255, 255, 255), width=2
        )
    # drone overhead
    dx, dy = cx + s * 0.55, cy - s
    draw.ellipse((dx - 6, dy - 3, dx + 6, dy + 3), fill=GOLD)
    draw.line((dx - 11, dy - 6, dx + 11, dy - 6), fill=GOLD, width=2)


def chip(draw, cx, cy, s):
    """Microchip: square body, inner die and pins on four sides."""
    draw.rectangle(
        (cx - s * 0.62, cy - s * 0.62, cx + s * 0.62, cy + s * 0.62),
        outline=(255, 255, 255), width=4,
    )
    draw.rectangle(
        (cx - s * 0.3, cy - s * 0.3, cx + s * 0.3, cy + s * 0.3),
        fill=(255, 255, 255),
    )
    for i in range(3):
        off = -s * 0.34 + i * s * 0.34
        draw.line((cx + off, cy - s * 0.62, cx + off, cy - s * 0.9),
                  fill=(255, 255, 255), width=3)
        draw.line((cx + off, cy + s * 0.62, cx + off, cy + s * 0.9),
                  fill=(255, 255, 255), width=3)
        draw.line((cx - s * 0.62, cy + off, cx - s * 0.9, cy + off),
                  fill=(255, 255, 255), width=3)
        draw.line((cx + s * 0.62, cy + off, cx + s * 0.9, cy + off),
                  fill=(255, 255, 255), width=3)


def cross(draw, cx, cy, s):
    """Bold medical cross in a ring."""
    draw.ellipse(
        (cx - s, cy - s, cx + s, cy + s), outline=(255, 255, 255), width=4
    )
    draw.rectangle(
        (cx - s * 0.18, cy - s * 0.62, cx + s * 0.18, cy + s * 0.62),
        fill=(255, 255, 255),
    )
    draw.rectangle(
        (cx - s * 0.62, cy - s * 0.18, cx + s * 0.62, cy + s * 0.18),
        fill=(255, 255, 255),
    )


def panel(draw, x, y, w, h, accent, icon, tag, headline, body):
    draw.rectangle((x, y, x + w, y + h), fill=CARD, outline=BORDER, width=1)
    draw.rectangle((x, y, x + w, y + 5), fill=accent)
    cx, cy, r = x + 54, y + 58, 34
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=accent)
    icon(draw, cx, cy, 22)
    tx = x + 106
    draw.text((tx, y + 16), tag, font=F_PANEL_TAG, fill=accent)
    head = wrap(draw, headline, F_PANEL_HEAD, w - 106 - 14)
    assert len(head) <= 2, f"headline too long: {headline}"
    by = draw_lines(draw, head, tx, y + 36, F_PANEL_HEAD, INK, 24)
    body_lines = wrap(draw, body, F_PANEL_BODY, w - 106 - 14)
    assert len(body_lines) <= 3, f"body too long: {body}"
    end = draw_lines(draw, body_lines, tx, by + 4, F_PANEL_BODY, (68, 68, 68), 19)
    assert end <= y + h - 8, f"panel overflows: {headline}"


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle((0, 0, W, 96), fill=NAVY)
    d.rectangle((0, 96, W, 100), fill=GOLD)
    d.text((28, 22), "THE WORLD TODAY", font=F_TITLE, fill=(255, 255, 255))
    d.text((996, 18), "WEDNESDAY", font=F_DATE, fill=GOLD, anchor="ra")
    d.text((996, 48), "25 NOVEMBER 2026", font=F_DATE, fill=(255, 255, 255), anchor="ra")

    # ---- kicker strip ----
    kicker = "ONE DAY  ·  TEN STORIES  ·  AS REPORTED ON WEDNESDAY 25 NOVEMBER 2026"
    d.text((W // 2, 112), kicker, font=F_KICKER, fill=RED, anchor="ma")

    # ---- lead story: CIA / ODNI hack ----
    lx, ly, lw, lh = 24, 138, 976, 198
    d.rectangle((lx, ly, lx + lw, ly + lh), fill=CARD, outline=BORDER, width=1)
    d.rectangle((lx, ly, lx + 10, ly + lh), fill=RED)
    shield(d, 132, 237, 52, NAVY)
    tx = 240
    d.text((tx, 152), "WASHINGTON — CYBERATTACK", font=F_TAG, fill=RED)
    head = wrap(d, "CIA AND SPY CHIEF'S OFFICE HACKED", F_LEAD_HEAD, lw - 240 - 20)
    assert len(head) <= 2
    by = draw_lines(d, head, tx, 176, F_LEAD_HEAD, INK, 38)
    body = (
        "Hackers breached an unclassified network the CIA and the Director of "
        "National Intelligence use to analyse open-source material. Officials "
        "say no classified data was hit; the attacker is unknown."
    )
    blines = wrap(d, body, F_LEAD_BODY, lw - 240 - 20)
    assert len(blines) <= 3, f"lead body too long: {blines}"
    end = draw_lines(d, blines, tx, by + 6, F_LEAD_BODY, (68, 68, 68), 23)
    assert end <= ly + lh - 8, "lead overflows"

    # ---- grid of four stories ----
    gx, gy = 24, 348
    pw, ph, gap = 482, 158, 12
    panel(d, gx, gy, pw, ph, RED, tower, "RIYADH",
          "Houthi drone hits Riyadh's tallest tower",
          "Second strike on the PIF Tower in a week wounds 11, Saudi civil defence says.")
    panel(d, gx + pw + gap, gy, pw, ph, STEEL, ship, "GULF OF FINLAND",
          "Zelenskiy: we hit Russian ship Sparta II",
          "Kyiv confirms Saturday's drone strike on the arms-carrying cargo vessel; Norway urges caution.")
    panel(d, gx, gy + ph + gap, pw, ph, PURPLE, chip, "NEW YORK",
          "Huawei guilty in US trade-secrets trial",
          "Jury convicts the Chinese telecom giant on 10 of 12 counts, including bank fraud.")
    panel(d, gx + pw + gap, gy + ph + gap, pw, ph, TEAL, cross, "DR CONGO",
          "WHO pulls Ebola team out of Ituri",
          "Staff evacuated from a hospital in Akwe after sheltering three days amid fierce fighting.")

    # ---- digest: five more stories ----
    dy = 688
    d.text((24, dy), "ALSO ON 25 NOVEMBER", font=F_DIGEST_HEAD, fill=RED)
    d.rectangle((24, dy + 26, 144, dy + 29), fill=GOLD)
    items = [
        ("Türkiye — ", "Army helicopter crashes in Eskişehir, killing five soldiers."),
        ("Paris — ", "Sarkozy corruption case ordered to trial; first hearing set for April 2027."),
        ("Washington — ", "Trump awards Rudy Giuliani the Presidential Medal of Freedom."),
        ("London — ", "England beat Australia by eight wickets to level the T20 series."),
        ("Science — ", "Astronomers find a quasar born within 630 million years of the Big Bang."),
    ]
    y = dy + 36
    for i, (lead, rest) in enumerate(items):
        accent = (RED, STEEL, PURPLE, TEAL, NAVY)[i]
        d.rectangle((28, y + 6, 38, y + 16), fill=accent)
        d.text((48, y), lead, font=F_DIGEST_B, fill=INK)
        lw_ = d.textlength(lead, font=F_DIGEST_B)
        d.text((48 + lw_, y), rest, font=F_DIGEST, fill=(68, 68, 68))
        total = d.textlength(lead + rest, font=F_DIGEST)
        assert 48 + total <= 1000, f"digest line too long: {lead}{rest}"
        y += 36
    assert y <= 916, "digest overflows"

    # ---- ticker + footer band ----
    d.rectangle((0, 924, W, H), fill=NAVY)
    ticker = ("THE WIRE  ·  SpaceX sued over Grok deepfakes  ·  "
              "Trump meets NATO chief Rutte  ·  US consumer confidence jumps")
    d.text((W // 2, 938), ticker, font=F_TICKER, fill=(255, 255, 255), anchor="ma")
    foot = "Sources: The New York Times · Reuters · CNN · Associated Press · AFP"
    d.text((W // 2, 970), foot, font=F_FOOT, fill=TICKER, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
