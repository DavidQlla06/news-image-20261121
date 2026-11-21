#!/usr/bin/env python3
"""Draw Saturday 21 November 2026 as a one-page newspaper front page.

Reads stories.json beside this file (a masthead date, one lead story,
four grid stories, two bottom stories and a footer line) and paints
entry.png at 1024x1024 with Pillow. Each story gets a small flat
illustration drawn with basic shapes, so the whole day can be taken
in from the single image. This is a local build step only; the entry
program (main.py) ships the finished PNG unchanged.

Run from this folder:  python3 generate.py
"""

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
SIDE = 1024
EDGE = 42
GAP = 22
COLUMN = (SIDE - 2 * EDGE - GAP) // 2

INK = (22, 22, 22)
SOFT = (78, 76, 70)
FAINT = (150, 146, 138)
PAPER = (252, 250, 244)
CARD = (255, 255, 255)
ACCENT = (166, 30, 30)
WASH = (240, 236, 226)
SKY = (205, 226, 240)
SEA = (110, 158, 196)
LEAF = (74, 140, 74)
AMBER = (214, 150, 32)
NIGHT = (28, 34, 64)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def typeface(points, bold=False, serif=False):
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), points)
    except OSError:
        return ImageFont.load_default()


def split_lines(pen, text, face, limit):
    """Greedy wrap: pack words onto a line while the line still fits."""
    out, line = [], ""
    for word in text.split():
        candidate = word if not line else line + " " + word
        if line and pen.textlength(candidate, font=face) > limit:
            out.append(line)
            line = word
        else:
            line = candidate
    if line:
        out.append(line)
    return out


def paint_lines(pen, x, y, lines, face, colour, step):
    for chunk in lines:
        pen.text((x, y), chunk, font=face, fill=colour)
        y += step
    return y


def centred(pen, y, text, face, colour):
    width = pen.textlength(text, font=face)
    pen.text(((SIDE - width) / 2, y), text, font=face, fill=colour)
    return y + face.size


# ------------------------------------------------------------------ art
def art_missile(pen, box):
    """Lead art: a missile arc coming down on a Polish flag."""
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=SKY)
    pen.rectangle([x0, y1 - 28, x1, y1], fill=(120, 150, 90))
    # Polish flag on a pole, lower left
    pole_x = x0 + 60
    pen.line([pole_x, y0 + 60, pole_x, y1 - 28], fill=INK, width=5)
    pen.rectangle([pole_x, y0 + 60, pole_x + 110, y0 + 92], fill=CARD,
                  outline=INK, width=2)
    pen.rectangle([pole_x, y0 + 92, pole_x + 110, y0 + 124], fill=ACCENT,
                  outline=INK, width=2)
    # missile arc from top-right down toward the ground
    for t in range(9):
        frac = t / 8
        mx = x1 - 60 - frac * 200
        my = y0 + 44 + frac * frac * 150
        r = 4 + frac * 4
        pen.ellipse([mx - r, my - r, mx + r, my + r], fill=(200, 200, 200),
                    outline=FAINT, width=1)
    tip_x, tip_y = x1 - 268, y0 + 206
    pen.polygon([(tip_x, tip_y), (tip_x + 26, tip_y - 14),
                 (tip_x + 34, tip_y - 4)], fill=INK)
    # impact burst
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        pen.line([tip_x + 6, tip_y + 4,
                  tip_x + 6 + 26 * math.cos(rad),
                  tip_y + 4 + 26 * math.sin(rad)], fill=AMBER, width=4)
    pen.ellipse([tip_x - 4, tip_y - 6, tip_x + 16, tip_y + 14],
                fill=ACCENT)


def art_downchart(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=CARD)
    pen.line([x0 + 16, y0 + 12, x0 + 16, y1 - 16], fill=INK, width=3)
    pen.line([x0 + 16, y1 - 16, x1 - 10, y1 - 16], fill=INK, width=3)
    points = [(x0 + 24, y0 + 26), (x0 + 52, y0 + 40), (x0 + 78, y0 + 34),
              (x0 + 102, y1 - 52), (x0 + 122, y1 - 26)]
    pen.line(points, fill=ACCENT, width=5, joint="curve")
    for px, py in points:
        pen.ellipse([px - 5, py - 5, px + 5, py + 5], fill=ACCENT)
    tip_x, tip_y = points[-1]
    pen.polygon([(tip_x, tip_y + 14), (tip_x - 9, tip_y - 4),
                 (tip_x + 9, tip_y - 4)], fill=ACCENT)


def art_scales(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=(240, 236, 226))
    cx = (x0 + x1) // 2
    pen.rectangle([cx - 4, y0 + 30, cx + 4, y1 - 30], fill=INK)
    pen.rectangle([cx - 22, y1 - 30, cx + 22, y1 - 22], fill=INK)
    pen.line([x0 + 16, y0 + 36, x1 - 16, y0 + 36], fill=INK, width=5)
    pen.ellipse([cx - 7, y0 + 26, cx + 7, y0 + 40], fill=AMBER,
                outline=INK, width=2)
    for pan_x, drop in ((x0 + 30, 0), (x1 - 30, 10)):
        pen.line([pan_x, y0 + 36, pan_x - 16, y0 + 78 + drop], fill=INK,
                 width=2)
        pen.line([pan_x, y0 + 36, pan_x + 16, y0 + 78 + drop], fill=INK,
                 width=2)
        pen.arc([pan_x - 20, y0 + 70 + drop, pan_x + 20, y0 + 98 + drop],
                0, 180, fill=INK, width=4)


def art_quake(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=(232, 222, 200))
    ground = y1 - 40
    pen.rectangle([x0, ground, x1, y1], fill=(160, 120, 80))
    # seismograph trace
    pts = []
    for i in range(13):
        px = x0 + 10 + i * 9
        amp = [0, 2, 4, 18, 30, 22, 34, 16, 26, 8, 4, 2, 0][i]
        pts.append((px, ground - 30 - amp))
    pen.line(pts, fill=ACCENT, width=3, joint="curve")
    # crack in the ground
    crack = [(x0 + 20, ground + 6), (x0 + 44, ground + 16),
             (x0 + 62, ground + 10), (x0 + 84, ground + 22),
             (x0 + 106, ground + 14)]
    pen.line(crack, fill=INK, width=3, joint="curve")
    # leaning house
    hx, hy = x0 + 36, ground - 26
    pen.polygon([(hx, hy), (hx + 20, hy - 14), (hx + 40, hy)],
                fill=ACCENT, outline=INK)
    pen.rectangle([hx + 4, hy, hx + 36, ground], fill=CARD, outline=INK,
                  width=2)


def art_summit(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=(234, 238, 246))
    table_y = y0 + 96
    pen.rectangle([x0 + 14, table_y, x1 - 14, table_y + 12], fill=INK)
    pen.rectangle([x0 + 24, table_y + 12, x0 + 32, y1 - 16], fill=INK)
    pen.rectangle([x1 - 32, table_y + 12, x1 - 24, y1 - 16], fill=INK)
    flags = [(x0 + 20, (40, 90, 170)), ((x0 + x1) // 2 - 14, ACCENT),
             (x1 - 48, (200, 40, 40))]
    for flag_x, colour in flags:
        pen.rectangle([flag_x, y0 + 30, flag_x + 28, y0 + 58],
                      fill=colour, outline=INK, width=2)
        pen.line([flag_x, y0 + 30, flag_x, table_y], fill=INK, width=3)


ART = [art_downchart, art_scales, art_quake, art_summit]


# ------------------------------------------------------------------ page
class Page:
    def __init__(self, data):
        self.data = data
        self.canvas = Image.new("RGB", (SIDE, SIDE), PAPER)
        self.pen = ImageDraw.Draw(self.canvas)
        self.y = 24

    def rule(self, weight=2, before=0, after=0):
        self.y += before
        self.pen.line([(EDGE, self.y), (SIDE - EDGE, self.y)],
                      fill=INK, width=weight)
        self.y += weight + after

    def masthead(self):
        eyebrow = typeface(19, bold=True)
        self.y = centred(self.pen, self.y,
                         "ONE DAY · ONE PAGE · WORLD NEWS", eyebrow, SOFT) + 8
        title = typeface(52, bold=True, serif=True)
        self.y = centred(self.pen, self.y, "THE WORLD IN ONE PAGE",
                         title, INK) + 10
        stamp = typeface(23, bold=True)
        self.y = centred(self.pen, self.y, self.data["date"], stamp,
                         ACCENT) + 10
        self.rule(weight=4, after=3)
        self.rule(weight=1, after=12)

    def kicker(self, x, y, text):
        face = typeface(19, bold=True)
        pad = 9
        width = self.pen.textlength(text, font=face)
        self.pen.rounded_rectangle([x, y, x + width + 2 * pad, y + 28],
                                   radius=4, fill=ACCENT)
        self.pen.text((x + pad, y + 4), text, font=face, fill=CARD)
        return y + 36

    def lead(self):
        story = self.data["lead"]
        top, height = self.y, 272
        self.pen.rectangle([EDGE, top, SIDE - EDGE, top + height],
                           fill=CARD, outline=INK, width=2)
        art_missile(self.pen, (EDGE + 2, top + 2, EDGE + 378,
                               top + height - 2))
        self.pen.line([EDGE + 380, top, EDGE + 380, top + height],
                      fill=INK, width=2)
        tx = EDGE + 402
        limit = SIDE - EDGE - tx - 18
        y = self.kicker(tx, top + 16, story["kicker"])
        head = typeface(40, bold=True)
        y = paint_lines(self.pen, tx, y,
                        split_lines(self.pen, story["headline"], head,
                                    limit)[:3], head, INK, 47)
        body = typeface(24)
        paint_lines(self.pen, tx, y + 4,
                    split_lines(self.pen, story["summary"], body,
                                limit)[:4], body, SOFT, 30)
        self.y = top + height + 18

    def cell(self, x, top, story, art):
        height = 182
        self.pen.rectangle([x, top, x + COLUMN, top + height],
                           fill=CARD, outline=INK, width=2)
        art(self.pen, (x + 2, top + 2, x + 126, top + height - 2))
        self.pen.line([x + 128, top, x + 128, top + height],
                      fill=(205, 200, 190), width=1)
        tx = x + 140
        limit = x + COLUMN - tx - 12
        y = self.kicker(tx, top + 10, story["kicker"])
        head = typeface(25, bold=True)
        y = paint_lines(self.pen, tx, y,
                        split_lines(self.pen, story["headline"], head,
                                    limit)[:2], head, INK, 29)
        body = typeface(19)
        paint_lines(self.pen, tx, y + 2,
                    split_lines(self.pen, story["summary"], body,
                                limit)[:3], body, SOFT, 23)
        return top + height

    def grid(self):
        stories = self.data["grid"]
        bottom = self.cell(EDGE, self.y, stories[0], ART[0])
        self.cell(EDGE + COLUMN + GAP, self.y, stories[1], ART[1])
        self.y = bottom + 18
        bottom = self.cell(EDGE, self.y, stories[2], ART[2])
        self.cell(EDGE + COLUMN + GAP, self.y, stories[3], ART[3])
        self.y = bottom + 18

    def bottom_pair(self):
        stories = self.data["bottom"]
        top = self.y
        self.pen.rectangle([EDGE, top, SIDE - EDGE, top + 118],
                           fill=WASH, outline=INK, width=1)
        for index, story in enumerate(stories):
            x = EDGE + 18 + index * (COLUMN + GAP)
            head = typeface(24, bold=True)
            y = paint_lines(
                self.pen, x, top + 12,
                split_lines(self.pen, story["headline"], head,
                            COLUMN - 24)[:2], head, INK, 28)
            body = typeface(19)
            paint_lines(self.pen, x, y + 2,
                        split_lines(self.pen, story["summary"], body,
                                    COLUMN - 24)[:2], body, SOFT, 23)
        self.y = top + 118 + 10

    def footer(self):
        face = typeface(18)
        centred(self.pen, self.y, self.data["footer"], face, FAINT)

    def render(self, path):
        self.masthead()
        self.lead()
        self.grid()
        self.bottom_pair()
        self.footer()
        self.pen.rectangle([5, 5, SIDE - 6, SIDE - 6], outline=INK,
                           width=2)
        self.canvas.save(path, "PNG", optimize=True)


def main():
    with open(os.path.join(ROOT, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    out = os.path.join(ROOT, "entry.png")
    Page(data).render(out)
    print("entry.png written:", os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
