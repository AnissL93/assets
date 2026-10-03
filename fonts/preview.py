#!/usr/bin/env python3
"""Render fonts/previews/FOLDER.png for every font folder (shown in README.md and on the website).

usage: uv run --with pillow --with fonttools fonts/preview.py
"""
import glob
import os

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.realpath(__file__))
W, PAD, BG, FG, DIM = 1200, 36, "#1b1820", "#efe6d8", "#8f8496"
LATIN = ["The quick brown fox jumps over the lazy dog", "0123456789 {}[]()<>=> != && || ;:'\"`~"]
CJK = ["天地玄黃 宇宙洪荒 日月盈昃 辰宿列張", "你好，世界！個人電腦設定"]
CJK_SC = ["天地玄黄 宇宙洪荒 日月盈昃 辰宿列张", "你好，世界！个人电脑设定"]   # simplified-only fonts
# pixel fonts: native size multiples, drawn without antialiasing
SIZE = {"oldschool-pc": 32, "press-start-2p": 24, "cubic-11": 36}
# icon fonts: the glyphs the desktop actually uses first (dwm tags, status bar)
ICONS = {
    "symbols-nerd-font": [0xF0CA0, 0xF0CA2, 0xF0CA4, 0xF0CA6, 0xF0CA8, 0xF0CAA, 0xF0CAC, 0xF0CAE, 0xF0CB0,
                          0xF0239, 0xF0AC, 0xE795, 0xE632, 0xF0A1E, 0xF082E, 0xF1C1, 0xF03D, 0xF2D0],
    "typicons": [0xE098, 0xE09C, 0xE059, 0xE146, 0xE024, 0xE009, 0xE0CD, 0xE02A],
}


def font_file(folder):
    files = sorted(glob.glob(os.path.join(HERE, folder, "*.ttf")))
    return next((f for f in files if "Regular" in f), files[0])


def render(folder):
    path = font_file(folder)
    tt = TTFont(path, lazy=True)
    cmap, family = tt.getBestCmap(), tt["name"].getBestFamilyName()
    has = lambda s: all(ord(c) in cmap for c in s if not c.isspace())
    size = SIZE.get(folder, 34)
    big, body = ImageFont.truetype(path, size * 2), ImageFont.truetype(path, size)
    meta = ImageFont.truetype(os.path.join(HERE, "oldschool-pc", "PxPlus_IBM_VGA_8x16.ttf"), 16)

    rows = []   # (font, text)
    if folder in ICONS:
        cps = ICONS[folder] + sorted(c for c in cmap if c >= 0xE000 and c not in ICONS[folder])
        per = (W - 2 * PAD) // (size * 3)          # one glyph per cell: icon fonts have no space glyph
        cps = [c for c in cps if c in cmap][:per * 4]
        rows += [(big, [chr(c) for c in cps[i:i + per]]) for i in range(0, len(cps), per)]
    else:
        rows.append((big, family if has(family) else "Aa 字"))
        rows += [(body, s) for s in LATIN if has(s)]
        rows += [(body, s) for s in (CJK if has(CJK[0]) else CJK_SC) if has(s)]

    heights = [int(f.size * 1.45) for f, _ in rows]
    img = Image.new("RGB", (W, PAD * 2 + sum(heights) + 28), BG)
    d = ImageDraw.Draw(img)
    d.fontmode = "1" if folder in SIZE else "L"
    y = PAD
    for (f, text), h in zip(rows, heights):
        if isinstance(text, list):
            for i, ch in enumerate(text):
                d.text((PAD + i * size * 3, y), ch, font=f, fill=FG)
        else:
            d.text((PAD, y), text, font=f, fill=FG)
        y += h
    d.fontmode = "1"
    d.text((PAD, img.height - PAD - 4), f"{family} · {os.path.basename(path)} · {len(cmap)} glyphs", font=meta, fill=DIM)
    out = os.path.join(HERE, "previews", folder + ".png")
    img.save(out, optimize=True)
    return out


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "previews"), exist_ok=True)
    for folder in sorted(d for d in os.listdir(HERE) if glob.glob(os.path.join(HERE, d, "*.ttf"))):
        print(render(folder))
