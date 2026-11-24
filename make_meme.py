#!/usr/bin/env python3
"""Build the rogue-agent meme (1024x1024) from the generated base image.

Deterministic: center-crops the base to a square, resizes to 1024x1024,
and draws the caption in classic meme style (white bold, black outline).
Run: python3 make_meme.py  ->  writes entry.png (JPEG bytes if PNG > 1 MiB).
"""
import io
import os
from PIL import Image, ImageDraw, ImageFont

BASE = "media-generation-meme-base-0-28396f31-6a36-4aed-a1e5-8f467d1ca819.png"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SIZE = 1024
LIMIT = 1_048_576


def cover_square(img, size):
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side)).resize(
        (size, size), Image.LANCZOS)


def wrap_to_width(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def caption_block(draw, lines, top_y, fnt):
    step = int(fnt.size * 1.12)
    for line in lines:
        draw.text((SIZE / 2, top_y), line, font=fnt, fill=(255, 255, 255),
                  anchor="ma", stroke_width=4, stroke_fill=(0, 0, 0))
        top_y += step
    return top_y


def main():
    base = Image.open(BASE).convert("RGB")
    img = cover_square(base, SIZE)
    draw = ImageDraw.Draw(img)

    top_font = ImageFont.truetype(SANS_B, 56)
    bottom_font = ImageFont.truetype(SANS_B, 50)
    top_lines = wrap_to_width(draw, "ME: I'LL JUST FIX ONE BUG",
                              top_font, SIZE - 48)
    caption_block(draw, top_lines, 26, top_font)

    bottom_lines = wrap_to_width(
        draw, "MY AGENT AT 3AM: I REWROTE THE ENTIRE CODEBASE",
        bottom_font, SIZE - 48)
    block_h = len(bottom_lines) * int(bottom_font.size * 1.12)
    caption_block(draw, bottom_lines, SIZE - 28 - block_h, bottom_font)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90, optimize=True)
    if buf.tell() <= LIMIT:
        img.save("entry.png", format="JPEG", quality=90, optimize=True)
        kind = "JPEG-in-entry.png"
    else:
        img.save(buf, format="JPEG", quality=80, optimize=True)
        img.save("entry.png", format="JPEG", quality=80, optimize=True)
        kind = "JPEG-in-entry.png (q80)"
    print(f"wrote entry.png ({kind}) {os.path.getsize('entry.png')} bytes")


if __name__ == "__main__":
    main()
