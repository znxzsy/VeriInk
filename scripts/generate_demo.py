#!/usr/bin/env python3
"""Regenerate the public synthetic gallery, hero image, and review wall."""

from __future__ import annotations

from pathlib import Path
import json
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from veriink.generator import SlotSpec, render_page  # noqa: E402
from veriink.validator import verify_gallery  # noqa: E402


CASES = [
    [("47 + 26 = ____", "73"), ("82 - 39 = ____", "43"), ("6 x 8 = ____", "48"), ("72 / 9 = ____", "8"), ("56 ____ 65", "<")],
    [("95 - 38 = ____", "58", 0), ("34 + 58 = ____", "92"), ("7 x 9 = ____", "63"), ("64 / 8 = ____", "8"), ("19 ____ 17", ">")],
    [("3.6 + 2.4 = ____", "6.0"), ("8.5 - 3.7 = ____", "4.8"), ("0.4 x 5 = ____", "2"), ("9.6 / 3 = ____", "3.2"), ("2.75 ____ 2.57", ">")],
    [("18 + ____ = 46", "28"), ("____ - 27 = 35", "62"), ("9 x ____ = 72", "8"), ("____ / 6 = 7", "42"), ("53 - ____ = 19", "34")],
    [("86 - 49 = ____", "37"), ("27 + 65 = ____", "82", 0), ("8 x 7 = ____", "56"), ("81 / 9 = ____", "9"), ("44 ____ 4 x 11", "=")],
    [("120 + 85 = ____", "205"), ("400 - 176 = ____", "224"), ("25 x 4 = ____", "100"), ("144 / 12 = ____", "12"), ("305 ____ 350", "<")],
    [("2 m = ____ cm", "200"), ("5 kg = ____ g", "5000"), ("90 min = ____ h", "1.5"), ("3 L = ____ mL", "3000"), ("1 day = ____ h", "24")],
    [("14 + 29 = ____", "43"), ("73 - 26 = ____", "47"), ("12 x 3 = ____", "36"), ("56 / 7 = ____", "7", 0), ("68 ____ 86", "<")],
    [("5.75 + 1.25 = ____", "7"), ("10 - 3.45 = ____", "6.55"), ("1.2 x 6 = ____", "7.2"), ("8.4 / 4 = ____", "2.1"), ("0.9 ____ 0.90", "=")],
    [("33 + ____ = 70", "37"), ("____ - 18 = 24", "42"), ("7 x ____ = 49", "7"), ("____ / 8 = 6", "48"), ("100 - ____ = 62", "38")],
    [("69 + 17 = ____", "86"), ("92 - 54 = ____", "38"), ("11 x 6 = ____", "67", 0), ("96 / 12 = ____", "8"), ("75 ____ 57", ">")],
    [("250 + 375 = ____", "625"), ("900 - 468 = ____", "432"), ("32 x 5 = ____", "160"), ("225 / 15 = ____", "15"), ("480 ____ 48 x 10", "=")],
]

STYLES = ["warm", "cool", "kraft", "gray"]
WRITERS = ["handlee", "patrick"]


def font(size: int, bold: bool = False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def build_review_wall(records: list[dict], gallery: Path) -> None:
    width, height = 1920, 1560
    board = Image.new("RGB", (width, height), (238, 240, 243))
    draw = ImageDraw.Draw(board)
    draw.text((55, 38), "SYNTHETIC REVIEW WALL", font=font(44, True), fill=(24, 33, 45))
    draw.text((55, 93), "12 deterministic scenes / labels + seeds + SHA256 / public showcase", font=font(24), fill=(76, 87, 102))
    draw.rounded_rectangle((1510, 36, 1864, 101), radius=22, fill=(216, 243, 232), outline=(112, 188, 157), width=2)
    draw.text((1560, 58), "ALL CHECKS PASSED", font=font(21, True), fill=(21, 112, 79))

    cols, card_w, card_h = 4, 440, 430
    for index, record in enumerate(records):
        row, col = divmod(index, cols)
        x = 45 + col * 468
        y = 145 + row * 455
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=14, fill=(255, 255, 255), outline=(207, 212, 220), width=2)
        page = Image.open(gallery / record["file"]).convert("RGB")
        page.thumbnail((230, 326), Image.Resampling.LANCZOS)
        px = x + (card_w - page.width) // 2
        board.paste(page, (px, y + 20))
        draw.text((x + 20, y + 354), f"CASE {index + 1:02d}  /  seed {record['seed']}", font=font(18, True), fill=(40, 51, 67))
        digest = record["sha256"][:12]
        draw.text((x + 20, y + 385), f"VERIFIED  sha256:{digest}", font=font(17), fill=(36, 130, 91))
    board.save(gallery / "synthetic_review_wall.png", optimize=True)


def build_hero(records: list[dict], gallery: Path) -> None:
    width, height = 1800, 820
    hero = Image.new("RGB", (width, height), (16, 24, 38))
    draw = ImageDraw.Draw(hero)
    for y in range(height):
        mix = y / height
        color = (16 + int(13 * mix), 24 + int(18 * mix), 38 + int(26 * mix))
        draw.line((0, y, width, y), fill=color)
    draw.text((80, 82), "VERIINK", font=font(76, True), fill=(245, 248, 252))
    draw.multiline_text(
        (80, 174),
        "Verifiable Handwriting\nSimulation Agent",
        font=font(37, True),
        fill=(132, 222, 188),
        spacing=5,
    )
    draw.multiline_text(
        (80, 294),
        "Synthetic scenes you can reproduce, inspect,\nand feed back into the next training pass.",
        font=font(30),
        fill=(205, 215, 229),
        spacing=16,
    )
    badges = ["SYNTHETIC", "REPRODUCIBLE", "VERIFIED"]
    bx = 80
    for badge in badges:
        bw = 210 if badge != "REPRODUCIBLE" else 255
        draw.rounded_rectangle((bx, 448, bx + bw, 505), radius=18, fill=(32, 52, 70), outline=(86, 141, 131), width=2)
        draw.text((bx + 23, 465), badge, font=font(20, True), fill=(155, 232, 202))
        bx += bw + 18
    draw.text((80, 570), "Generate  ->  Validate  ->  Review  ->  Refine", font=font(28, True), fill=(243, 190, 110))
    draw.text((80, 638), "Public demo edition / no real student data", font=font(22), fill=(139, 154, 174))

    for index, record in enumerate(records[:4]):
        page = Image.open(gallery / record["file"]).convert("RGB")
        page.thumbnail((210, 510), Image.Resampling.LANCZOS)
        x = 820 + index * 230
        y = 132 + (index % 2) * 32
        shadow = Image.new("RGBA", (page.width + 28, page.height + 28), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle((10, 10, page.width + 18, page.height + 18), radius=15, fill=(0, 0, 0, 95))
        hero.paste(shadow, (x - 10, y - 10), shadow)
        hero.paste(page, (x, y))
    hero.save(ROOT / "assets/hero.png", optimize=True)


def main() -> None:
    gallery = ROOT / "examples/gallery"
    gallery.mkdir(parents=True, exist_ok=True)
    records = []
    for index, pairs in enumerate(CASES, start=1):
        slots = [SlotSpec(*item) for item in pairs]
        record = render_page(
            slots,
            gallery / f"scene_{index:02d}.png",
            seed=4100 + index * 37,
            style=STYLES[(index - 1) % len(STYLES)],
            writer=WRITERS[(index - 1) % len(WRITERS)],
        )
        records.append(record)
    payload = {
        "schema": "veriink.public-gallery.v1",
        "notice": "All images and labels in this gallery are synthetic.",
        "page_count": len(records),
        "pages": records,
    }
    manifest = gallery / "manifest.json"
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    errors = verify_gallery(manifest)
    if errors:
        raise SystemExit("\n".join(errors))
    build_review_wall(records, gallery)
    build_hero(records, gallery)
    print(f"Generated and verified {len(records)} synthetic scenes.")


if __name__ == "__main__":
    main()
