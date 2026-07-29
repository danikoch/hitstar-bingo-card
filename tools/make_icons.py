#!/usr/bin/env python3
"""Generate the app icons (no third-party deps — raw PNG via zlib).

Run from the repo root:  python3 tools/make_icons.py
"""
import os
import struct
import zlib

BG = (0x0e, 0x0e, 0x14)
PALETTE = [
    (0xe6, 0x39, 0x46),
    (0xf7, 0x7f, 0x00),
    (0xfc, 0xbf, 0x49),
    (0x2a, 0x9d, 0x8f),
    (0x43, 0x61, 0xee),
]
# which palette colour sits in each of the 25 fields
LAYOUT = [
    0, 2, 4, 1, 3,
    3, 1, 0, 4, 2,
    4, 3, 2, 0, 1,
    1, 4, 3, 2, 0,
    2, 0, 1, 3, 4,
]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")


def rounded(px, py, x, y, w, h, r):
    """Is pixel (px, py) inside the rounded rect at (x, y, w, h)?"""
    if not (x <= px < x + w and y <= py < y + h):
        return False
    cx = min(max(px, x + r), x + w - r)
    cy = min(max(py, y + r), y + h - r)
    return (px - cx) ** 2 + (py - cy) ** 2 <= r * r


def draw(size, pad_ratio):
    pad = size * pad_ratio
    inner = size - 2 * pad
    gap = inner * 0.055
    tile = (inner - 4 * gap) / 5
    radius = tile * 0.22

    boxes = []
    for i, color in enumerate(LAYOUT):
        col, row = i % 5, i // 5
        boxes.append((
            pad + col * (tile + gap),
            pad + row * (tile + gap),
            PALETTE[color],
        ))

    rows = []
    for y in range(size):
        row = bytearray([0])  # PNG filter byte: none
        for x in range(size):
            rgb = BG
            for bx, by, color in boxes:
                if rounded(x + 0.5, y + 0.5, bx, by, tile, tile, radius):
                    rgb = color
                    break
            row += bytes(rgb)
        rows.append(bytes(row))
    return b"".join(rows)


def png(path, size, raw):
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    header = struct.pack(">2I5B", size, size, 8, 2, 0, 0, 0)  # 8-bit truecolour
    blob = (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(blob)
    print(f"{path}  {len(blob) / 1024:.1f} KB")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, size, pad in [
        ("icon-192.png", 192, 0.09),
        ("icon-512.png", 512, 0.09),
        ("icon-180.png", 180, 0.09),          # apple-touch-icon
        ("icon-maskable-512.png", 512, 0.20),  # extra padding for the safe zone
    ]:
        png(os.path.join(OUT, name), size, draw(size, pad))
