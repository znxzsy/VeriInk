"""Artifact-integrity checks for the public VeriInk gallery."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json


def verify_manifest(record: dict, root: str | Path) -> list[str]:
    errors: list[str] = []
    image_path = Path(root) / record.get("file", "")
    if not image_path.is_file():
        return [f"missing image: {image_path}"]
    digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
    if digest != record.get("sha256"):
        errors.append(f"hash mismatch: {image_path.name}")
    if len(record.get("slots", [])) != 5:
        errors.append(f"unexpected slot count: {image_path.name}")
    if not record.get("verified"):
        errors.append(f"renderer checks failed: {image_path.name}")
    for slot in record.get("slots", []):
        if slot.get("grade") not in (0, 1):
            errors.append(f"invalid grade: {image_path.name} item {slot.get('index')}")
        if not slot.get("checks", {}).get("render_intent_matches_label"):
            errors.append(f"label check failed: {image_path.name} item {slot.get('index')}")
        if not slot.get("checks", {}).get("inside_canvas"):
            errors.append(f"safe-margin check failed: {image_path.name} item {slot.get('index')}")
    return errors


def verify_gallery(manifest_path: str | Path) -> list[str]:
    manifest_file = Path(manifest_path)
    payload = json.loads(manifest_file.read_text(encoding="utf-8"))
    errors: list[str] = []
    for record in payload.get("pages", []):
        errors.extend(verify_manifest(record, manifest_file.parent))
    if payload.get("page_count") != len(payload.get("pages", [])):
        errors.append("manifest page_count mismatch")
    return errors
