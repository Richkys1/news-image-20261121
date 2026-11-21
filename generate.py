#!/usr/bin/env python3
"""Draw the front page of Saturday 21 November 2026 as one 1024x1024 PNG.

Deterministic: fixed layout, fixed palette, no network, no timestamps,
no randomness. Running this file twice produces byte-identical output.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (176, 0, 32)
NAVY = (18, 41, 77)
GREY = (110, 105, 92)
LIGHT = (232, 226, 210)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = "DejaVuSerif-Bold.ttf"
F_SANS = "DejaVuSans.ttf"
F_BOLD = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", max_w=None):
    """Draw lines of text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        if align == "center":
            lx = x + (max_w - draw.textlength(line, font=fnt)) // 2 if max_w else x
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, w, h=2, fill=INK):
    draw.rectangle([x, y, x + w, y + h], fill=fill)


def draw_masthead(draw):
    """Top banner: paper name, date, edition line."""
    rule(draw, 0, 0, W, 8)
    title = "THE WORLD TODAY"
    f_title = font(F_SERIF, 74)
    tw = draw.textlength(title, font=f_title)
    draw.text(((W - tw) / 2, 18), title, font=f_title, fill=INK)
    rule(draw, 24, 102, W - 48, 3)
    f_date = font(F_BOLD, 26)
    date = "SATURDAY  21  NOVEMBER  2026"
    dw = draw.textlength(date, font=f_date)
    draw.text(((W - dw) / 2, 112), date, font=f_date, fill=RED)
    f_small = font(F_SANS, 15)
    draw.text((24, 116), "No. 325", font=f_small, fill=GREY)
    right = "THE DAY IN ONE IMAGE"
    rw = draw.textlength(right, font=f_small)
    draw.text((W - 24 - rw, 116), right, font=f_small, fill=GREY)
    rule(draw, 24, 146, W - 48, 2)


def draw_lead_text(draw):
    """Lead story: kicker, wrapped headline, short deck."""
    x = 24
    y = 160
    f_kick = font(F_BOLD, 19)
    draw.text((x, y), "POLAND  •  NATO  •  WAR IN UKRAINE", font=f_kick, fill=RED)
    y += 28
    f_head = font(F_BOLD, 46)
    head = "NATO CHIEF IN WARSAW AS POLAND PRESSES ALLIES"
    for line in wrap(draw, head, f_head, 560):
        draw.text((x, y), line, font=f_head, fill=INK)
        y += 50
    y += 6
    f_deck = font(F_SANS, 20)
    deck = ("Rutte arrives today to seek more Eastern Sentry forces "
            "after Russian missiles fell on Polish soil on Friday.")
    lines = wrap(draw, deck, f_deck, 560)
    y = text_block(draw, x, y, lines, f_deck, leading=26)
    return y


def draw_lead_graphic(draw):
    """Dark navy panel on the right of the lead: a drawn missile and
    a four-point NATO-style compass star, all geometry, no assets."""
    x0, y0, x1, y1 = 616, 162, 1000, 396
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 18
    # four-point compass star inside a thin ring
    draw.ellipse([cx - 84, cy - 84, cx + 84, cy + 84], outline=(247, 243, 232), width=3)
    for (dx, dy, ln, wd) in [(0, -1, 62, 26), (0, 1, 62, 26),
                             (-1, 0, 62, 26), (1, 0, 62, 26)]:
        tip = (cx + dx * ln, cy + dy * ln)
        left = (cx - dy * wd, cy - dx * wd)
        right = (cx + dy * wd, cy + dx * wd)
        draw.polygon([tip, left, right], fill=(247, 243, 232))
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=RED)
    f_cap = font(F_BOLD, 16)
    cap = "THREE OBJECTS FELL ON POLISH SOIL"
    cw = draw.textlength(cap, font=f_cap)
    draw.text(((x0 + x1 - cw) / 2, y1 - 30), cap, font=f_cap,
              fill=(247, 243, 232))
    f_sub = font(F_SANS, 14)
    sub = "TUSK: AN \u201cINTENTIONAL PROVOCATION\u201d"
    sw = draw.textlength(sub, font=f_sub)
    draw.text(((x0 + x1 - sw) / 2, y1 - 52), sub, font=f_sub,
              fill=(200, 205, 220))


GRID = [
    ("EUROPE  •  YOUTH",
     "GEN Z WEEKEND OF ACTION",
     "Protests roll into Saturday across 25 nations over living "
     "costs, military spending and the climate."),
    ("CLIMATE  •  COP31",
     "COP31 DEAL STALLS",
     "Nations struggle to agree a climate plan as fossil fuels "
     "are cut from the draft deal."),
    ("DENMARK  •  RUSSIA",
     "DIPLOMAT EXPELLED OVER 'PLOT'",
     "Copenhagen accuses Moscow of plotting to kill a "
     "US-Ukrainian rapper; Russia denies it."),
    ("MARKETS  •  TECH",
     "TECH STOCKS SLIDE",
     "Markets dragged down as Anthropic shares slide in a "
     "broad sell-off of technology stocks."),
    ("HEALTH  •  CONGO",
     "EBOLA HITS CONGO'S CHILDREN",
     "An uncommon Ebola crisis in the east of DR Congo "
     "shuts about 100 schools."),
    ("HAITI  •  BLAST",
     "TWO SOLDIERS KILLED IN HAITI",
     "Two Salvadoran soldiers die handling explosives "
     "while serving with the Haiti mission."),
]


def draw_grid(draw, y_top):
    """Two columns by three rows of story boxes."""
    x0, x1 = 24, 1000
    col_w = (x1 - x0 - 16) // 2
    row_h = 148
    f_kick = font(F_BOLD, 15)
    f_head = font(F_BOLD, 21)
    f_deck = font(F_SANS, 16)
    for i, (kick, head, deck) in enumerate(GRID):
        col = i % 2
        row = i // 2
        bx = x0 + col * (col_w + 16)
        by = y_top + row * (row_h + 10)
        draw.rectangle([bx, by, bx + col_w, by + row_h], outline=INK, width=2)
        draw.rectangle([bx, by, bx + col_w, by + 6], fill=RED)
        draw.text((bx + 12, by + 14), kick, font=f_kick, fill=RED)
        y = by + 38
        for line in wrap(draw, head, f_head, col_w - 24):
            draw.text((bx + 12, y), line, font=f_head, fill=INK)
            y += 25
        for line in wrap(draw, deck, f_deck, col_w - 24):
            draw.text((bx + 12, y), line, font=f_deck, fill=INK)
            y += 20
    return y_top + 3 * row_h + 2 * 10


ALSO_TODAY = [
    ("HOUTHI MISSILES DOWNED",
     "Saudi-led coalition intercepts missiles aimed south."),
    ("TRUMP ON NVIDIA",
     "President calls for Jensen Huang to be reinstated."),
    ("FRENCH POLICE SENTENCED",
     "Officers jailed over the beating of Michel Zecler."),
    ("UFO FOOTAGE RELEASED",
     "US declassifies more Middle East UFO footage."),
]


def draw_also_today(draw, y_top):
    """Footer strip: four short items in columns under a red header."""
    rule(draw, 24, y_top, W - 48, 3, fill=RED)
    f_head = font(F_BOLD, 18)
    draw.text((24, y_top + 10), "ALSO TODAY", font=f_head, fill=RED)
    col_w = (W - 48) // 4
    f_item = font(F_BOLD, 14)
    f_deck = font(F_SANS, 13)
    for i, (head, deck) in enumerate(ALSO_TODAY):
        bx = 24 + i * col_w
        y = y_top + 40
        for line in wrap(draw, head, f_item, col_w - 18):
            draw.text((bx, y), line, font=f_item, fill=INK)
            y += 18
        for line in wrap(draw, deck, f_deck, col_w - 18):
            draw.text((bx, y), line, font=f_deck, fill=INK)
            y += 17
    return y_top + 40 + 4 * 18 + 2 * 17


def draw_footer(draw):
    f_foot = font(F_SANS, 14)
    line = ("THE WORLD TODAY  •  SATURDAY 21 NOVEMBER 2026  •  "
            "WARSAW  •  KYIV  •  BRUSSELS  •  PARIS  •  KINSHASA")
    lw = draw.textlength(line, font=f_foot)
    draw.text(((W - lw) / 2, H - 26), line, font=f_foot, fill=GREY)


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W - 1, H - 1], outline=INK, width=6)
    draw_masthead(draw)
    draw_lead_text(draw)
    draw_lead_graphic(draw)
    rule(draw, 24, 410, W - 48, 3)
    grid_bottom = draw_grid(draw, 424)
    also_bottom = draw_also_today(draw, grid_bottom + 12)
    draw_footer(draw)
    img.save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(target)
    print("wrote", target)
