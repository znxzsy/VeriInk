#!/usr/bin/env python3
"""Regenerate the public synthetic gallery, hero image, and review wall."""

from __future__ import annotations

from pathlib import Path
import hashlib
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
    [("835 + 859 = ____", "1694", 1, "1594"), ("953 + 782 = ____", "1735", 1, "1635"), ("668 + 814 = ____", "1482", 1, "1472"), ("807 - 468 = ____", "339", 1, "349"), ("72 x 18 = ____", "1296", 1, "1269")],
    [("4.875 + 19.68 = ____", "24.555", 1, "23.555"), ("63.25 - 18.975 = ____", "44.275", 1, "45.275"), ("3.45 x 0.68 = ____", "2.346", 1, "23.46"), ("7.392 / 2.4 = ____", "3.08", 1, "3.8"), ("12.5 x 0.48 = ____", "6", 1, "60")],
    [("1200 - 786 = ____", "414", 1, "424"), ("374 + 859 = ____", "1233", 1, "1133"), ("36 x 27 = ____", "972", 1, "962"), ("1728 / 24 = ____", "72", 1, "82"), ("6.08 + 3.945 = ____", "10.025", 1, "9.025")],
    [("2.5 h = ____ min", "150", 1, "120"), ("3.75 kg = ____ g", "3750", 1, "3570"), ("1.25 x 48 = ____", "60", 1, "50"), ("960 / 12 = ____", "80", 1, "90"), ("725 ____ 27 x 26", ">", 1, "<")],
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


def cjk_font(size: int, bold: bool = False):
    paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size, index=0)
    return font(size, bold)


def build_review_wall(records: list[dict], gallery: Path) -> None:
    cols, card_w, card_h = 4, 440, 430
    rows = (len(records) + cols - 1) // cols
    width, height = 1920, 150 + rows * 455 + 35
    board = Image.new("RGB", (width, height), (249, 249, 248))
    draw = ImageDraw.Draw(board)
    draw.text((55, 30), "SYNTHETIC DATA AUDIT", font=font(42, True), fill=(20, 29, 40))
    draw.text((55, 82), "合成数据审查", font=cjk_font(25, True), fill=(44, 92, 139))
    draw.text((285, 88), f"{len(records)} scenes / {len(records) * 5} items / labels + seeds + SHA256", font=font(21), fill=(79, 86, 96))
    draw.line((55, 126, width - 55, 126), fill=(49, 100, 150), width=3)
    draw.text((1570, 77), "CHECKS: PASS", font=font(20, True), fill=(28, 111, 73))

    for index, record in enumerate(records):
        row, col = divmod(index, cols)
        x = 45 + col * 468
        y = 145 + row * 455
        draw.rectangle((x, y, x + card_w, y + card_h), fill=(255, 255, 255), outline=(190, 195, 202), width=2)
        page = Image.open(gallery / record["file"]).convert("RGB")
        page.thumbnail((230, 326), Image.Resampling.LANCZOS)
        px = x + (card_w - page.width) // 2
        board.paste(page, (px, y + 20))
        draw.text((x + 20, y + 354), f"Fig. {index + 1:02d}  |  seed {record['seed']}", font=font(18, True), fill=(34, 48, 64))
        digest = record["sha256"][:12]
        draw.text((x + 20, y + 385), f"PASS  |  sha256:{digest}", font=font(17), fill=(32, 107, 75))
    board.save(gallery / "synthetic_review_wall.png", optimize=True)


def build_hero(records: list[dict], gallery: Path) -> None:
    width, height = 1800, 760
    hero = Image.new("RGB", (width, height), (250, 250, 248))
    draw = ImageDraw.Draw(hero)
    draw.line((62, 46, 62, height - 46), fill=(43, 101, 157), width=5)
    draw.text((104, 70), "VERIINK", font=font(78, True), fill=(19, 28, 39))
    draw.text((107, 165), "可验证手写仿真引擎", font=cjk_font(38, True), fill=(43, 101, 157))
    draw.text((107, 220), "VERIFIABLE HANDWRITING SYNTHESIS", font=font(25, True), fill=(72, 81, 92))
    draw.text((107, 306), "把模型做错的题，批量变成下一轮训练与回归数据。", font=cjk_font(27), fill=(40, 46, 54))
    draw.text((107, 355), "Turn model failures into training and regression data.", font=font(21), fill=(58, 66, 76))
    draw.line((107, 450, 690, 450), fill=(182, 187, 194), width=2)
    draw.text((107, 478), "SYNTHESIS  /  VALIDATION  /  REGRESSION", font=font(20, True), fill=(43, 101, 157))
    draw.text((107, 530), "PUBLIC DEMO  ·  SYNTHETIC DATA ONLY", font=font(18), fill=(104, 110, 118))
    draw.text((107, 630), "Method overview and reproducible examples", font=font(18), fill=(104, 110, 118))

    selected = records[-4:]
    for index, record in enumerate(selected):
        page = Image.open(gallery / record["file"]).convert("RGB")
        page.thumbnail((225, 540), Image.Resampling.LANCZOS)
        x = 760 + index * 250
        y = 115 + (index % 2) * 28
        draw.rectangle((x - 8, y - 8, x + page.width + 8, y + page.height + 8), fill=(255, 255, 255), outline=(174, 179, 186), width=2)
        hero.paste(page, (x, y))
        draw.text((x, y + page.height + 22), f"({chr(97 + index)}) HARD CASE {index + 1}", font=font(15, True), fill=(58, 68, 80))
    hero.save(ROOT / "assets/hero.png", optimize=True)


def build_hardcase_panel() -> None:
    source = ROOT / "examples/hardcases"
    manifest_path = source / "manifest.json"
    if not manifest_path.exists():
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = []
    for item in manifest["items"]:
        path = source / item["file"]
        if not path.is_file():
            raise SystemExit(f"missing synthetic hard case: {path.name}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            raise SystemExit(f"SHA256 mismatch for synthetic hard case: {path.name}")
        files.append(path)
    if not files:
        return
    width, height = 1800, 1260
    board = Image.new("RGB", (width, height), (250, 250, 248))
    draw = ImageDraw.Draw(board)
    draw.text((65, 42), "SYNTHETIC HARD CASES", font=font(44, True), fill=(20, 29, 40))
    draw.text((65, 98), "仿真难例：涂改、复杂计算与单位比较", font=cjk_font(25, True), fill=(44, 92, 139))
    draw.text((1285, 80), "SYNTHETIC DATA ONLY / 仅含仿真数据", font=cjk_font(18), fill=(77, 86, 97))
    draw.line((65, 145, width - 65, 145), fill=(49, 100, 150), width=3)

    card_w, card_h = 535, 490
    for index, path in enumerate(files[:6]):
        row, col = divmod(index, 3)
        x = 65 + col * 575
        y = 180 + row * 520
        draw.rectangle((x, y, x + card_w, y + card_h), fill=(255, 255, 255), outline=(188, 194, 202), width=2)
        sample = Image.open(path).convert("RGB")
        sample.thumbnail((485, 395), Image.Resampling.LANCZOS)
        px = x + (card_w - sample.width) // 2
        py = y + 25 + (395 - sample.height) // 2
        board.paste(sample, (px, py))
        draw.text((x + 24, y + 436), f"({chr(97 + index)})  SYNTHETIC HARD CASE {index + 1}", font=font(17, True), fill=(45, 58, 73))
    board.save(ROOT / "assets/synthetic_hardcases_cvpr.png", optimize=True)


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
    build_hardcase_panel()
    print(f"Generated and verified {len(records)} synthetic scenes.")


if __name__ == "__main__":
    main()
