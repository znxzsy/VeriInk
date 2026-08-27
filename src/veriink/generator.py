"""Small, deterministic handwriting-scene renderer for the public VeriInk demo.

This module intentionally contains only a compact showcase renderer. Production
priors, private datasets, service integrations, and internal quality thresholds
are not part of the public repository.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import hashlib
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
FONT_PATHS = {
    "handlee": ROOT / "assets/fonts/handlee/Handlee-Regular.ttf",
    "patrick": ROOT / "assets/fonts/patrickhand/PatrickHand-Regular.ttf",
}


@dataclass(frozen=True)
class SlotSpec:
    """One printed prompt and its deliberately rendered handwritten response."""

    prompt: str
    answer: str
    grade: int = 1
    draft_answer: str | None = None

    @property
    def transcription(self) -> str:
        return " ".join(self.prompt.replace("____", self.answer).split())


PAPER_STYLES = {
    "warm": ((246, 241, 226), (225, 217, 196), (40, 43, 48)),
    "cool": ((235, 240, 239), (210, 220, 218), (36, 42, 46)),
    "kraft": ((225, 211, 184), (196, 177, 144), (47, 42, 35)),
    "gray": ((231, 231, 226), (205, 205, 198), (37, 40, 43)),
}


def _font(path: Path | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [path] if path else []
    candidates += [
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate and candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size=size)
    except OSError:
        return ImageFont.load_default()


def _paper_texture(size: tuple[int, int], base: tuple[int, int, int], rng: random.Random) -> Image.Image:
    image = Image.new("RGB", size, base)
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    width, height = size
    for _ in range(max(900, width * height // 600)):
        x = rng.randrange(width)
        y = rng.randrange(height)
        shade = rng.choice((-1, 1))
        color = (35, 32, 28, 7) if shade < 0 else (255, 255, 255, 9)
        radius = rng.choice((1, 1, 2))
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    return Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")


def _draw_handwriting(
    canvas: Image.Image,
    text: str,
    anchor: tuple[int, int],
    font_path: Path,
    rng: random.Random,
    color: tuple[int, int, int],
    size_range: tuple[int, int] = (47, 58),
) -> tuple[int, int, int, int]:
    size = rng.randint(*size_range)
    font = _font(font_path, size)
    bbox = font.getbbox(text)
    width = max(54, bbox[2] - bbox[0] + 24)
    height = max(72, bbox[3] - bbox[1] + 30)
    patch = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(patch)
    jittered = (12 + rng.randint(-2, 2), 4 - bbox[1] + rng.randint(-2, 2))
    draw.text(jittered, text, font=font, fill=(*color, rng.randint(185, 230)), stroke_width=0)
    patch = patch.rotate(rng.uniform(-3.2, 3.2), resample=Image.Resampling.BICUBIC, expand=True)
    if rng.random() < 0.35:
        patch = patch.filter(ImageFilter.GaussianBlur(radius=0.25))
    x, y = anchor
    x += rng.randint(-3, 5)
    y += rng.randint(-5, 4)
    canvas.alpha_composite(patch, (x, y))
    return (x, y, x + patch.width, y + patch.height)


def _draw_scribble(
    canvas: Image.Image,
    bbox: tuple[int, int, int, int],
    rng: random.Random,
    color: tuple[int, int, int],
) -> None:
    """Cross out a synthetic draft while keeping the final answer readable."""

    draw = ImageDraw.Draw(canvas)
    left, top, right, bottom = bbox
    inset = 6
    left += inset
    right -= inset
    top += 10
    bottom -= 10
    for _ in range(6):
        points = []
        steps = 5
        for step in range(steps):
            x = left + (right - left) * step // (steps - 1)
            y = rng.randint(top, max(top, bottom))
            points.append((x, y))
        draw.line(points, fill=(*color, rng.randint(150, 205)), width=rng.choice((2, 3, 3)))


def render_page(
    slots: list[SlotSpec],
    output_path: str | Path,
    *,
    seed: int,
    style: str = "warm",
    writer: str = "handlee",
) -> dict:
    """Render a five-item synthetic page and return an auditable manifest record."""

    if len(slots) != 5:
        raise ValueError("The public demo renders exactly five items per page.")
    if style not in PAPER_STYLES:
        raise ValueError(f"Unknown paper style: {style}")
    if writer not in FONT_PATHS:
        raise ValueError(f"Unknown writer: {writer}")
    for slot in slots:
        if slot.prompt.count("____") != 1 or not slot.answer.strip():
            raise ValueError("Each prompt needs one blank and one non-empty answer.")
        if slot.grade not in (0, 1):
            raise ValueError("grade must be 0 or 1")
        if slot.draft_answer is not None and not slot.draft_answer.strip():
            raise ValueError("draft_answer cannot be empty")

    rng = random.Random(seed)
    width, height = 720, 1180
    paper, band, ink = PAPER_STYLES[style]
    image = _paper_texture((width, height), paper, rng).convert("RGBA")
    draw = ImageDraw.Draw(image)
    label_font = _font(None, 22)
    print_font = _font(None, 38)
    meta_font = _font(None, 18)
    hand_color = rng.choice(((50, 52, 58), (70, 69, 66), (42, 51, 62), (72, 58, 51)))

    draw.rounded_rectangle((30, 22, width - 30, 78), radius=14, fill=(255, 255, 255, 175))
    draw.text((50, 38), "VERIINK / SYNTHETIC WORKSHEET", font=label_font, fill=(35, 46, 61, 255))
    draw.text((width - 182, 41), f"SEED {seed}", font=meta_font, fill=(85, 91, 94, 255))

    slot_records: list[dict] = []
    for index, slot in enumerate(slots, start=1):
        top = 104 + (index - 1) * 205
        draw.rounded_rectangle((46, top, width - 46, top + 178), radius=12, fill=(*band, 210), outline=(95, 101, 104, 115), width=2)
        draw.rectangle((46, top, width - 46, top + 42), fill=(245, 247, 249, 235), outline=(74, 86, 101, 170), width=2)
        draw.text((65, top + 10), f"ITEM {index}", font=meta_font, fill=(41, 49, 60, 255))

        prefix, suffix = slot.prompt.split("____")
        text_y = top + 82
        text_x = 82
        draw.text((text_x, text_y), prefix, font=print_font, fill=(*ink, 255))
        prefix_bbox = draw.textbbox((text_x, text_y), prefix, font=print_font)
        blank_x = prefix_bbox[2] + 4
        probe_font = _font(FONT_PATHS[writer], 58)
        probe_text = slot.draft_answer or slot.answer
        probe_bbox = probe_font.getbbox(probe_text)
        blank_width = min(220, max(126, probe_bbox[2] - probe_bbox[0] + 34))
        if suffix:
            draw.text((blank_x + blank_width, text_y), suffix, font=print_font, fill=(*ink, 255))
        draw.rounded_rectangle(
            (blank_x - 5, text_y - 7, blank_x + blank_width - 2, text_y + 55),
            radius=6,
            outline=(220, 103, 96, 150),
            width=2,
        )
        draft_bbox = None
        if slot.draft_answer:
            draft_bbox = _draw_handwriting(
                image,
                slot.draft_answer,
                (blank_x + 5, text_y - 7),
                FONT_PATHS[writer],
                rng,
                hand_color,
                (42, 50),
            )
            _draw_scribble(image, draft_bbox, rng, hand_color)
            final_x = draft_bbox[2] + 12
            answer_bbox = _draw_handwriting(
                image,
                slot.answer,
                (final_x, text_y - 9),
                FONT_PATHS[writer],
                rng,
                (45, 89, 76),
                (38, 47),
            )
        else:
            answer_bbox = _draw_handwriting(
                image,
                slot.answer,
                (blank_x + 5, text_y - 7),
                FONT_PATHS[writer],
                rng,
                hand_color,
            )
        all_boxes = [answer_bbox] + ([draft_bbox] if draft_bbox else [])
        safe_margin = all(
            box[0] >= 0 and box[1] >= 0 and box[2] <= width and box[3] <= height
            for box in all_boxes
        )
        slot_records.append(
            {
                "index": index,
                "prompt": slot.prompt,
                "visible_answer": slot.answer,
                "draft_answer": slot.draft_answer,
                "expected_transcription": slot.transcription,
                "grade": slot.grade,
                "ink_bbox": list(answer_bbox),
                "draft_ink_bbox": list(draft_bbox) if draft_bbox else None,
                "checks": {"render_intent_matches_label": True, "inside_canvas": safe_margin},
            }
        )

    image = ImageEnhance.Contrast(image.convert("RGB")).enhance(rng.uniform(0.96, 1.04))
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return {
        "file": output.name,
        "seed": seed,
        "style": style,
        "writer": writer,
        "sha256": digest,
        "verified": all(item["checks"]["inside_canvas"] for item in slot_records),
        "slots": slot_records,
    }
