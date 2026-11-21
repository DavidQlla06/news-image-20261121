"""Draw the front page for Saturday 21 November 2026.

Reads stories.json next to this file and renders a 1024x1024 newspaper
front page with PIL. Everything is drawn from primitives and text, so
the output is deterministic: same input, same bytes.
"""

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W = 1024
H = 1024

PAPER = (247, 243, 233)
INK = (26, 24, 22)
MUTED = (96, 90, 80)
RED = (176, 32, 40)
NAVY = (18, 32, 58)
NAVY_LIGHT = (34, 54, 92)
GOLD = (196, 148, 52)
RULE = (26, 24, 22)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text_block(draw, x, y, text, fnt, fill, max_width, leading=None):
    """Draw wrapped text starting at (x, y); return the y just below it."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def dashed_arc(draw, box, start, end, fill, width=3, dash=14, gap=10):
    """Draw an arc as dashes by stamping short arc segments."""
    cx = (box[0] + box[2]) / 2.0
    cy = (box[1] + box[3]) / 2.0
    rx = (box[2] - box[0]) / 2.0
    ry = (box[3] - box[1]) / 2.0
    total = math.radians(end - start)
    steps = max(8, int(total * max(rx, ry) / 4))
    seg = dash + gap
    drawn = 0.0
    prev = None
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(start) + total * t
        px = cx + rx * math.cos(ang)
        py = cy + ry * math.sin(ang)
        if prev is not None:
            seg_len = math.hypot(px - prev[0], py - prev[1])
            if (drawn % seg) < dash:
                draw.line([prev, (px, py)], fill=fill, width=width)
            drawn += seg_len
        prev = (px, py)


# ---------------------------------------------------------------- motifs

def motif_missile(draw, cx, cy, s):
    """A missile on a dashed trajectory toward a target ring."""
    # trajectory
    dashed_arc(draw, (cx - 1.45 * s, cy - 0.4 * s, cx + 1.45 * s, cy + 1.35 * s),
               200, 340, (150, 170, 205), width=max(2, s // 18))
    # target ring, lower right
    tx, ty = cx + 1.18 * s, cy + 0.72 * s
    for r in (0.42 * s, 0.28 * s, 0.14 * s):
        draw.ellipse([tx - r, ty - r, tx + r, ty + r], outline=(230, 120, 90),
                     width=max(2, s // 16))
    # missile body, nose pointing down-right along the arc
    ang = math.radians(38)
    dx, dy = math.cos(ang), math.sin(ang)
    px, py = -dy, dx
    nose = (cx + 0.9 * s * dx, cy + 0.9 * s * dy)
    tail = (cx - 0.9 * s * dx, cy - 0.9 * s * dy)
    half = 0.16 * s
    body = [
        (tail[0] + half * px, tail[1] + half * py),
        (nose[0] - 0.35 * s * dx + half * px, nose[1] - 0.35 * s * dy + half * py),
        nose,
        (nose[0] - 0.35 * s * dx - half * px, nose[1] - 0.35 * s * dy - half * py),
        (tail[0] - half * px, tail[1] - half * py),
    ]
    draw.polygon(body, fill=(238, 240, 244), outline=(120, 130, 150))
    # fins
    for sgn in (1, -1):
        fin = [
            (tail[0] + sgn * half * px, tail[1] + sgn * half * py),
            (tail[0] + sgn * 0.42 * s * px - 0.1 * s * dx,
             tail[1] + sgn * 0.42 * s * py - 0.1 * s * dy),
            (tail[0] - 0.25 * s * dx, tail[1] - 0.25 * s * dy),
        ]
        draw.polygon(fin, fill=RED)
    # flame
    flame = [
        (tail[0] + half * px, tail[1] + half * py),
        (tail[0] - 0.55 * s * dx, tail[1] - 0.55 * s * dy),
        (tail[0] - half * px, tail[1] - half * py),
    ]
    draw.polygon(flame, fill=(245, 166, 35))


def motif_chart(draw, cx, cy, s):
    """Axes with a plunging line and a down arrow."""
    x0, y0 = cx - 0.95 * s, cy - 0.8 * s
    x1, y1 = cx + 0.95 * s, cy + 0.8 * s
    lw = max(2, s // 22)
    draw.line([(x0, y0), (x0, y1), (x1, y1)], fill=MUTED, width=lw)
    pts = [
        (x0 + 0.1 * s, y0 + 0.25 * s),
        (cx - 0.35 * s, y0 + 0.12 * s),
        (cx - 0.05 * s, y0 + 0.45 * s),
        (cx + 0.3 * s, y0 + 0.38 * s),
        (x1 - 0.18 * s, y1 - 0.22 * s),
    ]
    draw.line(pts, fill=RED, width=max(3, s // 12), joint="curve")
    tip = pts[-1]
    draw.polygon([
        tip,
        (tip[0] - 0.30 * s, tip[1] + 0.02 * s),
        (tip[0] - 0.06 * s, tip[1] - 0.26 * s),
    ], fill=RED)
    draw.text((x0 + 0.08 * s, y1 - 0.42 * s), "−5%",
              font=font(SANS_BOLD, int(s * 0.34)), fill=RED)


def motif_scales(draw, cx, cy, s):
    """A balance: pillar, beam, two pans."""
    lw = max(2, s // 18)
    top = cy - 0.85 * s
    base = cy + 0.85 * s
    draw.line([(cx, top), (cx, base)], fill=INK, width=lw)
    draw.line([(cx - 0.45 * s, base), (cx + 0.45 * s, base)], fill=INK, width=lw)
    draw.line([(cx - 0.85 * s, top + 0.12 * s), (cx + 0.85 * s, top + 0.12 * s)],
              fill=INK, width=lw)
    draw.ellipse([cx - 0.09 * s, top - 0.09 * s, cx + 0.09 * s, top + 0.09 * s],
                 fill=GOLD)
    for sgn in (-1, 1):
        px = cx + sgn * 0.85 * s
        py = top + 0.55 * s
        draw.line([(px, top + 0.12 * s), (px - 0.3 * s, py)], fill=INK, width=lw)
        draw.line([(px, top + 0.12 * s), (px + 0.3 * s, py)], fill=INK, width=lw)
        draw.arc([px - 0.34 * s, py - 0.22 * s, px + 0.34 * s, py + 0.30 * s],
                 15, 165, fill=GOLD, width=max(3, s // 12))


def motif_quake(draw, cx, cy, s):
    """A cracked ground line with radiating shock arcs."""
    lw = max(2, s // 16)
    gy = cy + 0.45 * s
    pts = []
    xs = [-1.0, -0.72, -0.5, -0.3, -0.12, 0.05, 0.22, 0.42, 0.62, 0.82, 1.0]
    ys = [0.0, -0.05, 0.10, -0.14, 0.06, -0.20, 0.08, -0.10, 0.04, -0.04, 0.0]
    for fx, fy in zip(xs, ys):
        pts.append((cx + fx * s, gy + fy * s))
    draw.line(pts, fill=INK, width=max(3, s // 10), joint="curve")
    # crack dropping from the centre
    crack = [(cx + 0.05 * s, gy - 0.2 * s), (cx - 0.06 * s, gy + 0.12 * s),
             (cx + 0.08 * s, gy + 0.38 * s), (cx - 0.02 * s, gy + 0.62 * s)]
    draw.line(crack, fill=RED, width=max(3, s // 12), joint="curve")
    # shock arcs above
    for r in (0.55 * s, 0.85 * s, 1.15 * s):
        draw.arc([cx - r, cy - 0.75 * s - r * 0.45, cx + r, cy - 0.75 * s + r * 0.45],
                 200, 340, fill=RED, width=lw)
    draw.text((cx - 0.95 * s, cy - 0.55 * s), "6.8",
              font=font(SANS_BOLD, int(s * 0.36)), fill=RED)


def motif_flags(draw, cx, cy, s):
    """Three flag poles with simple national-colour flags."""
    lw = max(2, s // 20)
    ground = cy + 0.85 * s
    flag_sets = [
        ((60, 80, 160), (240, 240, 240), (200, 50, 50)),   # blue white red
        ((200, 40, 40), (245, 200, 60), (200, 40, 40)),    # red gold red
        ((240, 240, 240), (60, 90, 170), (200, 50, 50)),   # white blue red
    ]
    for i, cols in enumerate(flag_sets):
        fx = cx + (i - 1) * 0.68 * s
        top = cy - 0.8 * s + (0.12 * s if i != 1 else 0)
        draw.line([(fx, top), (fx, ground)], fill=INK, width=lw)
        fw, fh = 0.5 * s, 0.36 * s
        stripe = fh / 3.0
        for j, col in enumerate(cols):
            draw.rectangle([fx, top + j * stripe, fx + fw, top + (j + 1) * stripe],
                           fill=col)
        draw.rectangle([fx, top, fx + fw, top + fh], outline=MUTED, width=1)


def motif_handshake(draw, cx, cy, s):
    """Two clasped hands, drawn as angled rounded shapes."""
    lw = max(2, s // 16)
    # left forearm coming from lower-left, right from lower-right
    draw.polygon([
        (cx - 1.0 * s, cy + 0.55 * s), (cx - 0.25 * s, cy - 0.1 * s),
        (cx + 0.05 * s, cy + 0.18 * s), (cx - 0.55 * s, cy + 0.8 * s),
    ], fill=(66, 96, 150), outline=INK)
    draw.polygon([
        (cx + 1.0 * s, cy + 0.55 * s), (cx + 0.25 * s, cy - 0.1 * s),
        (cx - 0.05 * s, cy + 0.18 * s), (cx + 0.55 * s, cy + 0.8 * s),
    ], fill=(150, 60, 60), outline=INK)
    # clasped hands in the middle
    draw.rounded_rectangle(
        [cx - 0.34 * s, cy - 0.12 * s, cx + 0.34 * s, cy + 0.30 * s],
        radius=int(0.12 * s), fill=(232, 190, 150), outline=INK, width=lw)
    # finger lines
    for i in range(3):
        fx = cx - 0.18 * s + i * 0.18 * s
        draw.line([(fx, cy + 0.02 * s), (fx, cy + 0.22 * s)], fill=INK, width=lw)
    # spark of agreement above
    for ang in (250, 270, 290):
        a = math.radians(ang)
        x1 = cx + 0.35 * s * math.cos(a)
        y1 = cy - 0.35 * s + 0.35 * s * math.sin(a)
        x2 = cx + 0.55 * s * math.cos(a)
        y2 = cy - 0.35 * s + 0.55 * s * math.sin(a)
        draw.line([(x1, y1), (x2, y2)], fill=GOLD, width=lw)


def motif_ballot(draw, cx, cy, s):
    """A ballot box with a ticked paper going in."""
    lw = max(2, s // 16)
    bx0, bx1 = cx - 0.75 * s, cx + 0.75 * s
    by0, by1 = cy + 0.05 * s, cy + 0.8 * s
    draw.rectangle([bx0, by0, bx1, by1], fill=(66, 96, 150), outline=INK, width=lw)
    draw.rectangle([bx0 - 0.08 * s, by0 - 0.14 * s, bx1 + 0.08 * s, by0],
                   fill=NAVY, outline=INK, width=lw)
    # slot
    draw.rectangle([cx - 0.35 * s, by0 - 0.10 * s, cx + 0.35 * s, by0 - 0.04 * s],
                   fill=PAPER)
    # paper
    px0, px1 = cx - 0.28 * s, cx + 0.28 * s
    py0, py1 = cy - 0.85 * s, by0 - 0.06 * s
    draw.rectangle([px0, py0, px1, py1], fill=(255, 255, 255), outline=INK, width=lw)
    # tick
    draw.line([(px0 + 0.10 * s, py0 + 0.30 * s), (px0 + 0.22 * s, py0 + 0.44 * s),
               (px1 - 0.08 * s, py0 + 0.14 * s)],
              fill=RED, width=max(3, s // 10), joint="curve")


MOTIFS = {
    "missile": motif_missile,
    "chart": motif_chart,
    "scales": motif_scales,
    "quake": motif_quake,
    "flags": motif_flags,
    "handshake": motif_handshake,
    "ballot": motif_ballot,
}


# ---------------------------------------------------------------- layout

def panel(draw, box, story, dark=False, motif_scale=58, head_size=30, body_size=19):
    x0, y0, x1, y1 = box
    bg = NAVY if dark else (255, 252, 245)
    draw.rectangle(box, fill=bg, outline=RULE, width=2)
    pad = 16
    ink = (245, 243, 238) if dark else INK
    body_fill = (205, 212, 228) if dark else (52, 48, 44)
    # kicker with a small red square
    ky = y0 + pad
    draw.rectangle([x0 + pad, ky + 2, x0 + pad + 12, ky + 14], fill=RED)
    draw.text((x0 + pad + 20, ky), story["kicker"],
              font=font(SANS_BOLD, 17), fill=RED if not dark else (240, 130, 120))
    # motif at top-right of the panel
    MOTIFS[story["motif"]](draw, x1 - pad - motif_scale, y0 + pad + motif_scale,
                           motif_scale)
    # headline, leaving room for the motif
    head_w = (x1 - x0) - 2 * pad - 2 * motif_scale - 10
    y = draw_text_block(draw, x0 + pad, ky + 30, story["headline"],
                        font(SERIF_BOLD, head_size), ink, head_w)
    # body across the full width, below whichever is lower
    body_y = max(y + 6, y0 + pad + 2 * motif_scale + 14)
    draw_text_block(draw, x0 + pad, body_y, story["body"],
                    font(SANS, body_size), body_fill, (x1 - x0) - 2 * pad)


def render(stories):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 36

    # ---- masthead
    name_f = font(SERIF_BOLD, 64)
    name = stories["paper"]
    tw = d.textlength(name, font=name_f)
    d.text(((W - tw) / 2, 22), name, font=name_f, fill=INK)
    date_f = font(SANS_BOLD, 24)
    date = stories["date"]
    tw = d.textlength(date, font=date_f)
    d.text(((W - tw) / 2, 100), date, font=date_f, fill=RED)
    line_f = font(SANS, 17)
    line = stories["edition_line"]
    tw = d.textlength(line, font=line_f)
    d.text(((W - tw) / 2, 134), line, font=line_f, fill=MUTED)
    d.rectangle([margin, 164, W - margin, 168], fill=RULE)
    d.rectangle([margin, 172, W - margin, 174], fill=RULE)

    # ---- lead story
    lead_box = (margin, 186, W - margin, 438)
    panel(d, lead_box, stories["lead"], dark=True,
          motif_scale=70, head_size=39, body_size=20)

    # ---- 2x2 grid
    grid = stories["grid"]
    gx0, gy0 = margin, 450
    gw = (W - 2 * margin - 12) // 2
    gh = 182
    for i, story in enumerate(grid):
        col, row = i % 2, i // 2
        x0 = gx0 + col * (gw + 12)
        y0 = gy0 + row * (gh + 12)
        panel(d, (x0, y0, x0 + gw, y0 + gh), story,
              motif_scale=42, head_size=24, body_size=15)

    # ---- bottom strip
    by0 = gy0 + 2 * gh + 12 + 12
    bottom = stories["bottom"]
    for i, story in enumerate(bottom):
        x0 = gx0 + i * (gw + 12)
        panel(d, (x0, by0, x0 + gw, by0 + 134), story,
              motif_scale=30, head_size=19, body_size=13)

    # ---- footer
    foot_f = font(SANS, 15)
    foot = "The day in one page  ·  " + date
    tw = d.textlength(foot, font=foot_f)
    d.text(((W - tw) / 2, H - 34), foot, font=foot_f, fill=MUTED)

    return img


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        stories = json.load(fh)
    img = render(stories)
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
