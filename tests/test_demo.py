from pathlib import Path

from veriink.generator import SlotSpec, render_page
from veriink.validator import verify_manifest


def test_renderer_is_deterministic(tmp_path: Path) -> None:
    slots = [
        SlotSpec("47 + 26 = ____", "73"),
        SlotSpec("82 - 39 = ____", "43"),
        SlotSpec("6 x 8 = ____", "48"),
        SlotSpec("72 / 9 = ____", "8"),
        SlotSpec("56 ____ 65", "<"),
    ]
    first = render_page(slots, tmp_path / "first.png", seed=2026)
    second = render_page(slots, tmp_path / "second.png", seed=2026)
    assert first["sha256"] == second["sha256"]
    assert verify_manifest(first, tmp_path) == []


def test_requires_five_items(tmp_path: Path) -> None:
    try:
        render_page([SlotSpec("1 + 1 = ____", "2")], tmp_path / "bad.png", seed=1)
    except ValueError as exc:
        assert "exactly five" in str(exc)
    else:
        raise AssertionError("render_page should reject incomplete pages")

