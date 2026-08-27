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


def test_crossout_revision_is_deterministic_and_tracked(tmp_path: Path) -> None:
    slots = [
        SlotSpec("835 + 859 = ____", "1694", draft_answer="1594"),
        SlotSpec("953 + 782 = ____", "1735", draft_answer="1635"),
        SlotSpec("668 + 814 = ____", "1482", draft_answer="1472"),
        SlotSpec("807 - 468 = ____", "339", draft_answer="349"),
        SlotSpec("72 x 18 = ____", "1296", draft_answer="1269"),
    ]
    first = render_page(slots, tmp_path / "draft_first.png", seed=4581)
    second = render_page(slots, tmp_path / "draft_second.png", seed=4581)
    assert first["sha256"] == second["sha256"]
    assert verify_manifest(first, tmp_path) == []
    assert all(slot["draft_answer"] for slot in first["slots"])
    assert all(slot["draft_ink_bbox"] for slot in first["slots"])


def test_requires_five_items(tmp_path: Path) -> None:
    try:
        render_page([SlotSpec("1 + 1 = ____", "2")], tmp_path / "bad.png", seed=1)
    except ValueError as exc:
        assert "exactly five" in str(exc)
    else:
        raise AssertionError("render_page should reject incomplete pages")
