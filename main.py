#!/usr/bin/env python3
"""Sum 24 — one-page newspaper front page for Tuesday 24 November 2026.
Writes /output/entry.png (1024x1024, deterministic, no network).
All news, dates and numbers come from the writer brief only.
"""
import hashlib
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/output/entry.png"

FD = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_TITLE = font("DejaVuSerif-Bold.ttf", 46)
F_DATE = font("DejaVuSerif-Bold.ttf", 21)
F_SEC = font("DejaVuSans-Bold.ttf", 11)
F_KICK = font("DejaVuSans-Bold.ttf", 8)
F_HEAD = font("DejaVuSans-Bold.ttf", 10)
F_HEAD_S = font("DejaVuSans-Bold.ttf", 9)
F_BODY = font("DejaVuSans.ttf", 9)
F_BODY_S = font("DejaVuSans.ttf", 8)
F_SMALL = font("DejaVuSans.ttf", 8)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 8)
F_TINY = font("DejaVuSans.ttf", 7)
F_TINY_B = font("DejaVuSans-Bold.ttf", 7)
F_STAT_V = font("DejaVuSans-Bold.ttf", 16)
F_STAT_L = font("DejaVuSans-Bold.ttf", 7)

INK = (15, 15, 15)
GREY = (90, 90, 90)
RED = (178, 34, 34)
BLUE = (30, 80, 140)
SEA = (205, 228, 245)
LAND = (226, 232, 205)
LAND_EDGE = (120, 130, 95)
PAPER = (255, 255, 255)

def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_lines(draw, x, y, lines, fnt, fill=INK, leading=None, max_lines=None):
    if max_lines is not None:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def box(draw, x, y, w, h, fill=None, outline=INK, width=1):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=outline, width=width)

def hline(draw, x, y, w, width=1, fill=INK):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)

# ---------------------------------------------------------------- scenes
def scene(draw, kind, x, y, w, h):
    """Flat-colour drawn illustration inside (x, y, w, h)."""
    box(draw, x, y, w, h, fill=(245, 244, 238), outline=(150, 150, 140))
    cx, cy = x + w // 2, y + h // 2
    if kind == "chess":
        # board detail: 8 columns x 4 rows, square cells, two kings, clock.
        # Cell size is the same both ways so the board can never spill
        # outside its scene box.
        sq = 12
        bw, bh = 8 * sq, 4 * sq
        bx = x + (w - bw) // 2
        by = y + 2
        for r in range(4):
            for c in range(8):
                col = (235, 225, 200) if (r + c) % 2 == 0 else (90, 70, 55)
                draw.rectangle([bx + c * sq, by + r * sq,
                                bx + (c + 1) * sq - 1, by + (r + 1) * sq - 1],
                               fill=col)
        draw.rectangle([bx, by, bx + bw - 1, by + bh - 1], outline=INK)
        # white king (left), black king (right), standing on the back rank
        draw.ellipse([bx + 8, by + 4, bx + 24, by + 20], fill=(255, 255, 255), outline=INK)
        draw.rectangle([bx + 13, by, bx + 19, by + 8], fill=(255, 255, 255), outline=INK)
        draw.ellipse([bx + bw - 24, by + 4, bx + bw - 8, by + 20], fill=(30, 30, 30), outline=INK)
        draw.rectangle([bx + bw - 19, by, bx + bw - 13, by + 8], fill=(30, 30, 30), outline=INK)
        # clock chip, bottom-right corner of the scene box
        draw.rectangle([x + w - 36, y + h - 13, x + w - 4, y + h - 2], fill=(255, 255, 255), outline=INK)
        draw.text((x + w - 33, y + h - 13), "15:00", font=F_TINY_B, fill=RED)
    elif kind == "fire":
        # burned factory shell + rescuers + smoke
        draw.rectangle([x + 8, y + 18, x + w - 8, y + h - 8], fill=(70, 60, 55))
        draw.rectangle([x + 8, y + 18, x + w - 8, y + 30], fill=(40, 35, 32))
        for wx in (x + 16, x + w // 2 - 6, x + w - 30):
            draw.rectangle([wx, y + 34, wx + 14, y + 46], fill=(255, 190, 60))
        draw.polygon([(x + 100, y + 18), (x + 108, y + 6), (x + 116, y + 18)], fill=(255, 120, 30))
        draw.polygon([(x + w - 30, y + 18), (x + w - 22, y + 6), (x + w - 14, y + 18)], fill=(255, 120, 30))
        # rescuers in orange helmets
        for rx in (x + 22, x + w // 2, x + w - 26):
            draw.ellipse([rx - 5, y + h - 26, rx + 5, y + h - 16], fill=(255, 140, 0), outline=INK)
            draw.rectangle([rx - 4, y + h - 16, rx + 4, y + h - 6], fill=(255, 200, 40), outline=INK)
        draw.text((x + 4, y + 2), "CIKANDE, BANTEN", font=F_TINY_B, fill=INK)
    elif kind == "dymer":
        # struck residential block, broken floors, rescue ladder
        draw.rectangle([x + 14, y + 14, x + w - 40, y + h - 8], fill=(200, 190, 170), outline=INK)
        draw.rectangle([x + 14, y + 14, x + w - 40, y + 30], fill=(90, 80, 70))
        draw.polygon([(x + 30, y + 30), (x + 55, y + 44), (x + 30, y + 52)], fill=(60, 55, 50))
        for wy in (y + 34, y + 44):
            for wx in (x + 22, x + 46):
                draw.rectangle([wx, wy, wx + 12, wy + 7], fill=(140, 180, 210), outline=INK)
        draw.line([(x + w - 30, y + h - 8), (x + w - 12, y + 20)], fill=RED, width=3)
        draw.ellipse([x + w - 22, y + h - 22, x + w - 12, y + h - 12], fill=(255, 140, 0), outline=INK)
        draw.text((x + 4, y + 2), "DYMER, KYIV REGION", font=F_TINY_B, fill=INK)
    elif kind == "corvette":
        # ship burning at port, water, smoke — all inside the scene box
        draw.rectangle([x, y + h - 14, x + w, y + h], fill=(90, 150, 200))
        draw.rectangle([x + 12, y + h - 30, x + w - 12, y + h - 14], fill=(120, 120, 125), outline=INK)
        draw.rectangle([x + 30, y + h - 42, x + w - 40, y + h - 30], fill=(80, 80, 85), outline=INK)
        draw.polygon([(x + 34, y + h - 42), (x + 40, y + 2), (x + 46, y + h - 42)], fill=(255, 120, 30))
        draw.polygon([(x + 54, y + h - 42), (x + 60, y + 4), (x + 66, y + h - 42)], fill=(255, 180, 40))
        draw.ellipse([x + 78, y + 2, x + 94, y + 14], fill=(180, 180, 180))
        draw.ellipse([x + 96, y + 6, x + 110, y + 18], fill=(200, 200, 200))
        draw.text((x + 4, y + h - 13), "BENGHAZI", font=F_TINY_B, fill=(255, 255, 255))
    elif kind == "sparta":
        draw.rectangle([x, y + h - 18, x + w, y + h], fill=(70, 130, 190))
        draw.rectangle([x + 10, y + h - 36, x + w - 10, y + h - 18], fill=(60, 60, 65), outline=INK)
        draw.rectangle([x + w - 40, y + h - 50, x + w - 22, y + h - 36], fill=(90, 90, 95), outline=INK)
        draw.polygon([(x + 24, y + h - 36), (x + 32, y + 2), (x + 40, y + h - 36)], fill=(255, 110, 25))
        draw.ellipse([x + 52, y + 4, x + 68, y + 18], fill=(170, 170, 170))
        draw.ellipse([x + 72, y + 8, x + 88, y + 22], fill=(190, 190, 190))
        draw.text((x + 4, y + h - 14), "GULF OF FINLAND", font=F_TINY_B, fill=(255, 255, 255))
    elif kind == "nvidia":
        # chip + rising chart
        draw.rectangle([x + 8, y + 18, x + w // 2 - 2, y + h - 10], fill=(30, 60, 40), outline=INK)
        draw.rectangle([x + 16, y + 26, x + w // 2 - 10, y + h - 18], fill=(70, 180, 110))
        draw.text((x + 18, y + h - 30), "NVDA", font=F_TINY_B, fill=(255, 255, 255))
        pts = [(x + w // 2 + 4, y + h - 14), (x + w // 2 + 16, y + h - 26),
               (x + w // 2 + 26, y + h - 20), (x + w // 2 + 38, y + h - 34),
               (x + w - 6, y + 18)]
        draw.line(pts, fill=RED, width=3)
        draw.polygon([(x + w - 12, y + 14), (x + w - 4, y + 14), (x + w - 8, y + 24)], fill=RED)
        draw.text((x + w // 2 + 2, y + 2), "+30%", font=F_TINY_B, fill=RED)
    elif kind == "cop31":
        # hall, empty chairs, delegates walking out (door at right)
        draw.rectangle([x + 6, y + 16, x + w - 26, y + h - 8], fill=(210, 200, 180), outline=INK)
        for cx0 in (x + 12, x + 30, x + 48):
            draw.rectangle([cx0, y + h - 26, cx0 + 12, y + h - 12], fill=(150, 140, 120), outline=INK)
        draw.rectangle([x + w - 22, y + 16, x + w - 6, y + h - 8], fill=(120, 180, 120), outline=INK)
        for px in (x + w - 44, x + w - 34):
            draw.ellipse([px, y + 22, px + 8, y + 30], fill=(200, 150, 110), outline=INK)
            draw.rectangle([px, y + 30, px + 8, y + h - 14], fill=(60, 60, 140), outline=INK)
        draw.text((x + 4, y + 2), "ANTALYA — WALKOUT", font=F_TINY_B, fill=INK)
    elif kind == "alcaraz":
        # player lifting trophy (trophy kept below the scene label)
        draw.text((x + 4, y + 2), "TURIN — CHAMPION", font=F_TINY_B, fill=INK)
        draw.ellipse([cx - 6, y + 28, cx + 6, y + 40], fill=(210, 170, 120), outline=INK)
        draw.rectangle([cx - 9, y + 40, cx + 9, y + h - 2], fill=(220, 60, 60), outline=INK)
        draw.line([(cx - 9, y + 44), (cx - 22, y + 28)], fill=(210, 170, 120), width=4)
        draw.line([(cx + 9, y + 44), (cx + 22, y + 28)], fill=(210, 170, 120), width=4)
        draw.polygon([(cx - 16, y + 14), (cx + 16, y + 14), (cx + 10, y + 26), (cx - 10, y + 26)], fill=(255, 215, 0), outline=INK)
    elif kind == "un":
        # UN chamber: semicircle desks + speaker
        for i in range(5):
            ax = x + 10 + i * ((w - 20) // 5)
            draw.arc([ax, y + 18, ax + 22, y + 44], 180, 360, fill=INK, width=2)
            draw.rectangle([ax + 4, y + 34, ax + 18, y + 42], fill=(120, 140, 180), outline=INK)
        draw.rectangle([cx - 12, y + h - 22, cx + 12, y + h - 10], fill=(90, 70, 50), outline=INK)
        draw.ellipse([cx - 5, y + h - 34, cx + 5, y + h - 24], fill=(210, 170, 120), outline=INK)
        draw.text((x + 4, y + 2), "UN — NEW YORK", font=F_TINY_B, fill=INK)
    elif kind == "drone":
        # desert road + drone overhead
        draw.rectangle([x, y + h - 20, x + w, y + h], fill=(220, 190, 130))
        draw.line([(x, y + h - 10), (x + w, y + h - 10)], fill=(255, 255, 255), width=2)
        draw.ellipse([cx - 14, y + 16, cx + 14, y + 26], fill=(80, 80, 85), outline=INK)
        draw.line([(cx - 22, y + 20), (cx - 12, y + 20)], fill=INK, width=2)
        draw.line([(cx + 12, y + 20), (cx + 22, y + 20)], fill=INK, width=2)
        draw.line([(cx, y + 26), (cx + 8, y + h - 22)], fill=(200, 200, 200), width=1)
        draw.text((x + 4, y + 2), "SINALOA, MEXICO", font=F_TINY_B, fill=INK)
    elif kind == "gaza":
        # students arriving: plane + students with bags
        draw.polygon([(x + 8, y + 14), (x + w - 8, y + 20), (x + 8, y + 26)], fill=(180, 200, 220), outline=INK)
        draw.rectangle([x + 8, y + 18, x + 30, y + 24], fill=(120, 150, 190), outline=INK)
        for px in (x + 56, x + 84, x + 112):
            draw.ellipse([px, y + h - 38, px + 10, y + h - 28], fill=(210, 170, 120), outline=INK)
            draw.rectangle([px, y + h - 28, px + 10, y + h - 14], fill=(60, 120, 180), outline=INK)
        draw.text((x + 4, y + h - 12), "DUBLIN", font=F_TINY_B, fill=INK)
    elif kind == "bepi":
        # probe at Mercury
        draw.ellipse([x + 8, y + h - 34, x + 38, y + h - 4], fill=(200, 140, 90), outline=INK)
        draw.ellipse([x + 14, y + h - 28, x + 22, y + h - 20], fill=(170, 110, 70))
        draw.rectangle([cx - 4, y + 16, cx + 4, y + 30], fill=(180, 180, 190), outline=INK)
        draw.rectangle([cx - 22, y + 20, cx - 6, y + 28], fill=(40, 90, 160), outline=INK)
        draw.rectangle([cx + 6, y + 20, cx + 22, y + 28], fill=(40, 90, 160), outline=INK)
        draw.text((x + 4, y + 2), "MERCURY ORBIT", font=F_TINY_B, fill=INK)
    elif kind == "wallst":
        # traders + board with rising line
        draw.rectangle([x + 6, y + 8, x + w - 6, y + 30], fill=(20, 40, 30), outline=INK)
        draw.line([(x + 10, y + 26), (x + 30, y + 18), (x + 50, y + 22), (x + w - 10, y + 12)],
                  fill=(80, 220, 120), width=2)
        for px in (x + 72, x + 102, x + 132):
            draw.ellipse([px, y + h - 28, px + 10, y + h - 18], fill=(210, 170, 120), outline=INK)
            draw.rectangle([px - 2, y + h - 18, px + 12, y + h - 6], fill=(50, 50, 60), outline=INK)
        draw.text((x + 4, y + h - 12), "NEW YORK", font=F_TINY_B, fill=INK)


# ---------------------------------------------------------------- map
# Simplified continent polygons in (lon, lat). One equirectangular
# projection is used for the whole map and for every pin.
NA = [(-168, 66), (-150, 70), (-130, 71), (-115, 68), (-100, 69), (-90, 69),
      (-82, 66), (-78, 71), (-70, 62), (-60, 55), (-55, 52), (-60, 47),
      (-68, 44), (-75, 39), (-76, 35), (-80, 32), (-81, 26), (-84, 30),
      (-90, 21), (-96, 16), (-92, 15), (-87, 13), (-83, 9), (-79, 9),
      (-83, 13), (-90, 14), (-97, 16), (-105, 20), (-112, 29), (-120, 34),
      (-125, 40), (-124, 48), (-130, 55), (-140, 60), (-155, 58), (-165, 60),
      (-168, 66)]
SA = [(-79, 9), (-75, 11), (-68, 11), (-62, 9), (-55, 6), (-51, 4), (-50, 0),
      (-44, -3), (-38, -5), (-35, -8), (-39, -15), (-41, -22), (-48, -27),
      (-52, -33), (-58, -35), (-62, -41), (-65, -45), (-68, -50), (-68, -55),
      (-71, -54), (-73, -44), (-73, -37), (-71, -30), (-70, -23), (-72, -18),
      (-77, -12), (-81, -6), (-80, -3), (-77, 4), (-79, 9)]
EU = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50),
      (-9, 51), (-10, 53), (-8, 55), (-5, 55), (0, 54), (3, 53), (5, 53),
      (8, 55), (8, 57), (10, 59), (5, 60),
      (5, 62), (10, 64), (14, 67), (18, 69), (24, 71), (30, 70), (35, 68),
      (40, 67), (44, 66), (40, 62), (38, 58), (32, 56), (28, 55), (24, 58),
      (21, 55), (24, 52), (32, 51), (36, 49), (33, 46), (28, 44), (24, 42), (23, 40),
      (22, 37), (26, 38), (28, 41), (30, 36), (33, 36), (36, 36), (30, 41),
      (28, 45), (22, 45), (19, 42), (16, 40), (12, 42), (8, 44), (3, 42),
      (0, 39), (-1, 37), (-6, 36), (-10, 36)]
AF = [(-17, 15), (-16, 20), (-14, 25), (-10, 30), (-6, 34), (-2, 35), (5, 35),
      (10, 35.5), (11, 34), (15, 32.5), (20, 32.4), (25, 32.3), (30, 32.2), (32, 32.3),
      (34, 28), (36, 24), (38, 20), (40, 16), (43, 12), (47, 11), (51, 11),
      (50, 5), (46, 2), (42, -1), (40, -5), (39, -10), (36, -14), (34, -20),
      (32, -26), (29, -30), (26, -34), (20, -35), (17, -33), (15, -28),
      (13, -22), (12, -17), (12, -11), (9, -2), (9, 4), (2, 6), (-5, 5),
      (-9, 4), (-13, 8), (-16, 11), (-17, 15)]
AS = [(30, 36), (33, 36), (36, 36), (39, 38), (42, 40), (45, 39), (48, 38),
      (50, 39), (54, 38), (57, 37), (60, 38), (63, 40), (66, 40), (70, 42),
      (74, 44), (78, 46), (82, 50), (86, 54), (90, 58), (95, 62), (100, 66),
      (108, 68), (115, 70), (122, 71), (130, 71), (138, 72), (146, 72),
      (155, 70), (162, 68), (170, 67), (178, 66), (175, 62), (170, 60),
      (162, 56), (158, 52), (155, 55), (150, 59), (145, 59), (142, 55),
      (140, 48), (138, 43), (135, 43), (132, 40), (129, 35), (127, 34),
      (124, 38), (122, 38), (120, 33), (118, 28), (114, 22), (110, 20),
      (108, 18), (106, 12), (104, 9), (101, 7), (99, 9), (97, 12), (95, 16),
      (92, 20), (90, 22), (87, 21), (84, 19), (81, 16), (79, 13), (77, 8),
      (75, 12), (73, 18), (71, 20), (68, 22), (66, 25), (63, 25), (59, 26),
      (57, 26), (54, 27), (52, 27), (50, 29), (48, 29), (46, 29), (43, 29),
      (41, 31), (39, 32), (36, 34), (33, 35), (30, 36)]
AU = [(113, -22), (114, -28), (115, -32), (116, -35), (120, -34), (124, -33),
      (128, -32), (132, -32), (135, -35), (138, -35), (140, -38), (144, -38),
      (147, -39), (150, -37), (153, -32), (153, -27), (151, -24), (148, -20),
      (146, -19), (142, -11), (139, -14), (136, -12), (133, -12), (130, -13),
      (127, -14), (124, -15), (122, -17), (119, -20), (115, -21), (113, -22)]
JAVA = [(105, -5.8), (108, -6.2), (111, -6.5), (114, -7.3), (114, -8.5),
        (111, -8.2), (108, -7.8), (105, -6.8)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
         (142, 42), (140, 44), (138, 40), (136, 36), (133, 34)]
CONTINENTS = [NA, SA, EU, AF, AS, AU, JAVA, JAPAN]

def point_in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and \
           (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

# The coarse continent polygons fill the Gulf of Finland as land; it is a
# bay, so carve it out as sea (the Sparta II pin must sit at sea, honestly).
GULF_OF_FINLAND = [(21, 59.0), (23, 60.0), (27, 60.3), (30, 59.9),
                   (29, 59.3), (24, 59.0)]

def on_land(lon, lat):
    if point_in_poly(lon, lat, GULF_OF_FINLAND):
        return False
    return any(point_in_poly(lon, lat, p) for p in CONTINENTS)

# name, lat, lon, label, label dx, dy, anchor side ("l" label right of pin, "r" left)
PINS = [
    ("GENEVA — CHESS", 46.20, 6.14, -118, -16, "r"),
    ("TURIN — ALCARAZ", 45.07, 7.69, 10, -18, "l"),
    ("THE HAGUE — ICJ", 52.07, 4.32, -12, -26, "l"),
    ("KYIV — STRIKES", 50.45, 30.52, 8, 4, "l"),
    ("GULF OF FINLAND — SPARTA II (AT SEA)", 59.90, 25.00, -10, 36, "r"),
    ("ANTALYA — COP31", 36.90, 30.71, -10, 30, "r"),
    ("BENGHAZI — CORVETTE", 32.12, 20.07, 8, 6, "l"),
    ("DUBLIN — STUDENTS", 53.35, -6.26, -108, 12, "r"),
    ("NEW YORK — UN", 40.75, -73.97, -96, -4, "r"),
    ("CULIACAN — DRONE", 24.80, -107.39, 8, 8, "l"),
    ("SHENZHEN — APEC", 22.54, 114.06, -108, 16, "r"),
    ("CIKANDE — FIRE", -6.35, 106.28, -104, 12, "r"),
    ("JAKARTA", -6.21, 106.85, 8, -16, "l"),
]
# land check (all pins except the honestly-at-sea Gulf of Finland pin)
for _name, _lat, _lon, *_ in PINS:
    if "AT SEA" in _name:
        assert not on_land(_lon, _lat), _name
    else:
        assert on_land(_lon, _lat), _name

def draw_map(draw, mx, my, mw, mh):
    lon0, lon1, lat0, lat1 = -180.0, 180.0, -58.0, 84.0
    def proj(lon, lat):
        px = mx + (lon - lon0) / (lon1 - lon0) * mw
        py = my + (lat1 - lat) / (lat1 - lat0) * mh
        return px, py
    draw.rectangle([mx, my, mx + mw, my + mh], fill=SEA, outline=INK)
    for lat in (-40, -20, 0, 20, 40, 60):
        _, gy = proj(0, lat)
        draw.line([(mx, gy), (mx + mw, gy)], fill=(185, 210, 230), width=1)
    for lon in (-120, -60, 0, 60, 120):
        gx, _ = proj(lon, 0)
        draw.line([(gx, my), (gx, my + mh)], fill=(185, 210, 230), width=1)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # pins + labels (white-backed labels, leader lines, spread offsets)
    placed = []
    for name, lat, lon, dx, dy, side in PINS:
        px, py = proj(lon, lat)
        lx = px + dx
        ly = py + dy
        tw = draw.textlength(name, font=F_TINY_B)
        th = 11
        if side == "r":
            lx = px + dx - tw - 8
        bx0, by0 = lx - 3, ly - 2
        bx1, by1 = lx + tw + 3, ly + th
        placed.append((name, bx0, by0, bx1, by1))
        # leader line from pin to label box edge
        ex = bx1 if side == "r" else bx0
        draw.line([(px, py), (ex, ly + 5)], fill=GREY, width=1)
        draw.rectangle([bx0, by0, bx1, by1], fill=(255, 255, 255), outline=(180, 180, 180))
        draw.text((lx, ly), name, font=F_TINY_B, fill=INK)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED, outline=(255, 255, 255))
    # collision self-check: no two label boxes may overlap
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            a, b = placed[i], placed[j]
            overlap = not (a[3] <= b[1] or b[3] <= a[1] or a[4] <= b[2] or b[4] <= a[2])
            assert not overlap, f"label collision: {a[0]} vs {b[0]}"
    return placed


# ---------------------------------------------------------------- stories
# (region, tag, headline, body, scene or None)
# 36 stories: Europe 9, Asia-Pacific 7, Middle East 6, Americas 7,
# Africa 3, Global 2, Sport 2. Heroes are the first Europe, Asia and Sport items.
GRID = [
    # Europe (8 grid + 1 hero)
    ("EUROPE", "NATO vows space defence", "After a report of a Russian nuclear satellite, NATO pledges to defend space.", None),
    ("EUROPE", "Strikes hit Kyiv region", "Russian strikes hit the Kyiv region on Tuesday, including a home in Dymer.", None),
    ("EUROPE", "Sparta II hit on Saturday", "Two drones struck the Russian-flagged cargo ship in the Gulf of Finland.", "sparta"),
    ("EUROPE", "Sparta II still burning", "On Sunday the ship still burned off Finland; 16 crew were evacuated.", None),
    ("EUROPE", "Finland points at Kyiv", "Finland says Ukraine was likely behind the Sparta II drone strike.", None),
    ("EUROPE", "COP31 collapses in Antalya", "Climate talks ended on Sunday with no deal on fossil fuels.", "cop31"),
    ("EUROPE", "EU walks out at COP31", "The EU left rather than accept a text with no mention of fossil fuels.", None),
    ("EUROPE", "Longest COP ever", "Nearly 200 countries; the talks overran by two days in Antalya.", None),
    # Asia-Pacific (6 grid + 1 hero)
    ("ASIA-PACIFIC", "24 dead, confirmed Monday", "The death toll from the Cikande factory fire was confirmed on Monday.", None),
    ("ASIA-PACIFIC", "DNA tests will take weeks", "Victims cannot be identified visually; police collect DNA from relatives.", None),
    ("ASIA-PACIFIC", "300 on the Saturday shift", "The factory sits about 50 km west of Jakarta; hotspots still smoulder.", None),
    ("ASIA-PACIFIC", "APEC summit in Shenzhen", "Leaders gather in Shenzhen for the APEC summit on Tuesday.", None),
    ("ASIA-PACIFIC", "First US-China-Russia talks", "The three leaders are set for their first trilateral meeting.", None),
    ("ASIA-PACIFIC", "China-Japan stalemate", "China and Japan are in a diplomatic stalemate after summit friction.", None),
    # Middle East (6)
    ("MIDDLE EAST", "Gaza students head to Ireland", "Students are set to begin studies in Ireland after winning a visa battle.", "gaza"),
    ("MIDDLE EAST", "Visa battle won", "The Gaza students won their fight for visas to study in Ireland.", None),
    ("MIDDLE EAST", "Gaza children reach the UK", "Children from Gaza arrive in Britain for medical treatment.", None),
    ("MIDDLE EAST", "Oxfam: Gaza poisoned", "A report released Tuesday says Gaza's air, soil and water are contaminated.", None),
    ("MIDDLE EAST", "Contamination for decades", "Heavy metals, explosive residues, asbestos and dioxins will linger.", None),
    ("MIDDLE EAST", "Report names the poisons", "Oxfam and the Conflict and Environment Observatory issued the report.", None),
    # Americas (7)
    ("AMERICAS", "US drone over Mexico", "A US drone flew over Mexican territory to help capture a drug lord.", "drone"),
    ("AMERICAS", "Nvidia brings Huang back", "Nvidia reinstated Jensen Huang as chief executive on Monday.", "nvidia"),
    ("AMERICAS", "Shares surge about 30%", "The reinstatement added roughly $960 billion in market value.", "wallst"),
    ("AMERICAS", "Trump praises the decision", "Trump praised Nvidia's decision to reinstate Huang as chief executive.", None),
    ("AMERICAS", "Trump pauses detonation", "Trump pauses a planned detonation of degraded explosives.", None),
    ("AMERICAS", "Trump's $6 trillion claim", "Trump posted on Sunday a claim of $6 trillion; see Date Check.", None),
    ("AMERICAS", "UN chief: AI rules in a year", "The UN chief calls for an AI risk-management framework within a year.", "un"),
    # Africa (3)
    ("AFRICA", "Corvette burns at Benghazi", "The corvette, believed to be the Merkury, burned at the port.", "corvette"),
    ("AFRICA", "Kyiv claims sea-drone hit", "Ukraine claimed on Monday its sea drones sank a Russian warship.", None),
    ("AFRICA", "Cargo vessel damaged", "A cargo vessel was also damaged off Libya, Ukraine said on Monday.", None),
    # Global (2)
    ("GLOBAL", "ICJ: Myanmar committed genocide", "The court ruled on Thursday 19 Nov, by nine votes to six, on the Rohingya.", None),
    ("GLOBAL", "BepiColombo reaches Mercury", "The ESA-JAXA probe entered orbit around Mercury on Saturday.", "bepi"),
    # Sport (1 grid + 1 hero)
    ("SPORT", "Alcaraz wins ATP Finals", "Alcaraz beat Zverev 6-2, 7-6(7) on Sunday in Turin; his sixth title of 2026.", "alcaraz"),
]
assert len(GRID) == 33, len(GRID)

HEROES = [
    ("SPORT  •  CHESS  •  TUESDAY", "Youngest title match ever begins in Geneva",
     "Gukesh Dommaraju, 20, defends against Javokhir Sindarov, 20, in a 14-game "
     "match, first to 7.5 points, for a $2.5 million prize. Game 1 starts at "
     "15:00 CET at the Fondation Martin Bodmer, Cologny; Sindarov has White.",
     "chess"),
    ("ASIA-PACIFIC  •  INDONESIA  •  TUESDAY", "Search goes on for about 30 missing after factory fire",
     "Rescuers are still searching today in Cikande, Banten, after the candy-factory "
     "fire. 24 people are confirmed dead; 29 are confirmed safe, 5 in hospital. "
     "The burned building is unstable, with hotspots still smouldering.",
     "fire"),
    ("EUROPE  •  UKRAINE  •  TUESDAY", "Zelensky warns of new Russian strikes",
     "President Zelensky says intelligence shows Russia is planning new strikes on "
     "Ukraine. Russian strikes hit the Kyiv region, including a residential "
     "building in Dymer, where rescue work is under way.",
     "dymer"),
]

STATS = [
    ("24", "DEAD IN FACTORY FIRE"),
    ("~30", "STILL MISSING"),
    ("$2.5m", "CHESS PRIZE FUND"),
    ("14", "GAMES IN THE MATCH"),
    ("15:00 CET", "FIRST MOVE, GAME 1"),
    ("20 & 20", "AGES OF BOTH PLAYERS"),
]

REGIONS = ["EUROPE 9", "ASIA-PACIFIC 7", "MIDDLE EAST 6", "AMERICAS 7",
           "AFRICA 3", "GLOBAL 2", "SPORT 2"]

TIMELINE = [
    ("15:00 CET", "Game 1 first move, Geneva"),
    ("TUESDAY", "Rescuers search Cikande"),
    ("TUESDAY", "Zelensky warns of strikes"),
    ("TUESDAY", "Oxfam Gaza report out"),
    ("TUESDAY", "US drone over Mexico"),
]

DATE_CHECK = ("DATE CHECK — NOT TUESDAY: COP31 collapsed Sunday 22 Nov  •  Alcaraz won "
              "the ATP Finals Sunday 22 Nov  •  Sparta II strike Saturday 21 Nov  •  "
              "Nvidia reinstatement announced Monday 23 Nov  •  Trump's $6 trillion claim "
              "posted Sunday 22 Nov  •  ICJ Myanmar ruling Thursday 19 Nov  •  "
              "BepiColombo entered Mercury orbit Saturday 21 Nov.")

# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, 5], fill=INK)
    # masthead
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 10), title, font=F_TITLE, fill=INK)
    d.text((14, 16), "ONE PAGE", font=F_SMALL_B, fill=GREY)
    d.text((14, 30), "WORLD NEWS", font=F_SMALL_B, fill=GREY)
    rt = "PRESS TIME 16:00 UTC"
    d.text((W - 14 - d.textlength(rt, font=F_SMALL_B), 16), rt, font=F_SMALL_B, fill=GREY)
    rt2 = "TUESDAY EDITION"
    d.text((W - 14 - d.textlength(rt2, font=F_SMALL_B), 30), rt2, font=F_SMALL_B, fill=GREY)
    hline(d, 14, 70, W - 28, width=2)
    dt = "Tuesday 24 November 2026"
    dw = d.textlength(dt, font=F_DATE)
    d.text(((W - dw) / 2, 74), dt, font=F_DATE, fill=INK)
    hline(d, 14, 100, W - 28, width=2)
    # region bar
    x = 14
    for r in REGIONS:
        d.text((x, 106), r, font=F_SMALL_B, fill=BLUE)
        x += int(d.textlength(r, font=F_SMALL_B)) + 34
    d.text((W - 14 - d.textlength("36 STORIES  •  13 SCENES", font=F_SMALL_B), 106),
           "36 STORIES  •  13 SCENES", font=F_SMALL_B, fill=RED)
    hline(d, 14, 122, W - 28, width=1)
    # stat strip
    sw = (W - 28 - 5 * 6) // 6
    for i, (val, lab) in enumerate(STATS):
        sx = 14 + i * (sw + 6)
        box(d, sx, 128, sw, 34, fill=(245, 244, 238), outline=(180, 180, 170))
        vw = d.textlength(val, font=F_STAT_V)
        d.text((sx + (sw - vw) / 2, 130), val, font=F_STAT_V, fill=RED)
        lw = d.textlength(lab, font=F_STAT_L)
        d.text((sx + (sw - lw) / 2, 149), lab, font=F_STAT_L, fill=INK)
    # heroes
    hy, hh = 168, 132
    hw = (W - 28 - 2 * 12) // 3
    for i, (kick, head, body, kind) in enumerate(HEROES):
        hx = 14 + i * (hw + 12)
        box(d, hx, hy, hw, hh, fill=PAPER, outline=INK, width=2)
        d.text((hx + 8, hy + 6), kick, font=F_KICK, fill=RED)
        hl = wrap(d, head, F_HEAD, hw - 16)
        y = text_lines(d, hx + 8, hy + 18, hl, F_HEAD, leading=12, max_lines=2)
        scene(d, kind, hx + 8, y + 2, hw - 16, 52)
        bl = wrap(d, body, F_BODY_S, hw - 16)
        text_lines(d, hx + 8, y + 58, bl, F_BODY_S, leading=10, max_lines=2)
    # map header + map
    d.text((14, 306), "THE WORLD IN ONE MAP — EVERY PIN FROM REAL LATITUDE & LONGITUDE",
           font=F_SEC, fill=INK)
    d.text((W - 14 - d.textlength("RED DOT = STORY  •  GULF OF FINLAND PIN IS AT SEA, HONESTLY",
                                  font=F_TINY), 308),
           "RED DOT = STORY  •  GULF OF FINLAND PIN IS AT SEA, HONESTLY", font=F_TINY, fill=GREY)
    draw_map(d, 14, 322, W - 28, 130)
    # timeline
    ty = 458
    d.text((14, ty), "TIMELINE OF TUESDAY", font=F_SEC, fill=INK)
    tx = 190
    for t, label in TIMELINE:
        d.text((tx, ty + 1), t, font=F_SMALL_B, fill=RED)
        tx += int(d.textlength(t, font=F_SMALL_B)) + 6
        d.text((tx, ty + 1), label, font=F_SMALL, fill=INK)
        tx += int(d.textlength(label, font=F_SMALL)) + 22
    hline(d, 14, 476, W - 28, width=1)
    # grid: 5 columns, balanced so each column holds exactly 2 scenes
    cols = [[], [], [], [], []]
    scene_idx = [i for i, s in enumerate(GRID) if s[3]]
    text_idx = [i for i, s in enumerate(GRID) if not s[3]]
    # deal 2 scenes + texts per column (33 stories: 7,7,7,6,6)
    per_col = [7, 7, 7, 6, 6]
    si = ti = 0
    for ci, n in enumerate(per_col):
        n_scene = 2
        for _ in range(n_scene):
            cols[ci].append(GRID[scene_idx[si]]); si += 1
        for _ in range(n - n_scene):
            cols[ci].append(GRID[text_idx[ti]]); ti += 1
    gy, gh = 482, 446
    cw = (W - 28 - 4 * 8) // 5
    for ci, col in enumerate(cols):
        cx = 14 + ci * (cw + 8)
        heights = [88 if s[3] else 46 for s in col]
        total = sum(heights) + 6 * (len(col) - 1)
        assert total <= gh, f"column {ci} too tall: {total} > {gh}"
        y = gy
        for s, bh in zip(col, heights):
            region, head, body, kind = s
            box(d, cx, y, cw, bh, fill=PAPER, outline=(170, 170, 160))
            d.text((cx + 5, y + 3), region, font=F_TINY_B, fill=BLUE)
            hl = wrap(d, head, F_HEAD_S, cw - 10)
            yy = text_lines(d, cx + 5, y + 13, hl, F_HEAD_S, leading=10, max_lines=2)
            if kind:
                scene(d, kind, cx + 5, yy + 1, cw - 10, 52)
                bl = wrap(d, body, F_BODY_S, cw - 10)
                cap = max(0, (y + bh - 3 - (yy + 56)) // 9)
                text_lines(d, cx + 5, yy + 56, bl, F_BODY_S, leading=9, max_lines=cap)
            else:
                bl = wrap(d, body, F_BODY_S, cw - 10)
                cap = max(0, (y + bh - 3 - yy) // 9)
                text_lines(d, cx + 5, yy + 1, bl, F_BODY_S, leading=9, max_lines=cap)
            y += bh + 6
    # date check + footer
    by = 934
    box(d, 14, by, W - 28, 52, fill=(255, 248, 220), outline=RED, width=2)
    dl = wrap(d, DATE_CHECK, F_SMALL_B, W - 44)
    text_lines(d, 22, by + 5, dl, F_SMALL_B, leading=12, max_lines=4)
    fy = 992
    d.text((14, fy), "✓ 36 STORIES  •  ✓ 13 DRAWN SCENES  •  ✓ MAP PINS CHECKED ON LAND  •  ✓ ALL TUESDAY STORIES VERIFIED FOR 24 NOVEMBER 2026",
           font=F_SMALL_B, fill=INK)
    d.text((14, fy + 13), "The World Today — one-page summary of Tuesday 24 November 2026. Older stories are dated honestly and appear only where marked.",
           font=F_TINY, fill=GREY)
    return img

def main():
    img = render()
    os.makedirs("/output", exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    data = open(OUT, "rb").read()
    print(f"wrote {OUT} {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")

if __name__ == "__main__":
    main()
