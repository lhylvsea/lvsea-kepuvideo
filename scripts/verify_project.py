#!/usr/bin/env python3
"""Verify a lvsea-kepuvideo project at a named production stage."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

STAGES = ("brief", "script", "audio", "storyboard", "render", "final")
SRT_TIME = re.compile(r"^(?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2}),(?P<ms>\d{3})$")


def parse_time(value: str) -> float | None:
    match = SRT_TIME.match(value.strip())
    if not match:
        return None
    return (
        int(match.group("h")) * 3600
        + int(match.group("m")) * 60
        + int(match.group("s"))
        + int(match.group("ms")) / 1000
    )


def parse_srt(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    entries: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.is_file():
        return entries, [f"missing SRT: {path}"]
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    index = 0
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        number = lines[index].strip()
        if not number.isdigit() or index + 1 >= len(lines):
            errors.append(f"invalid cue header near line {index + 1}")
            break
        timing = lines[index + 1].split("-->")
        if len(timing) != 2:
            errors.append(f"invalid timing near line {index + 2}")
            break
        start = parse_time(timing[0])
        end = parse_time(timing[1])
        if start is None or end is None or end <= start:
            errors.append(f"invalid cue range near line {index + 2}")
        text_lines: list[str] = []
        index += 2
        while index < len(lines) and lines[index].strip():
            text_lines.append(lines[index].strip())
            index += 1
        entries.append({"number": int(number), "start": start, "end": end, "text": "\n".join(text_lines)})
    for previous, current in zip(entries, entries[1:]):
        if previous["end"] is not None and current["start"] is not None and current["start"] < previous["end"]:
            errors.append(f"SRT overlap between cue {previous['number']} and {current['number']}")
    if entries and entries[0]["start"] != 0:
        errors.append("SRT does not start at 00:00:00,000")
    if not entries:
        errors.append("SRT has no cues")
    return entries, errors


def required_paths(project: Path, stage: str) -> list[Path]:
    base = [project / "brief.md"]
    if stage in {"script", "audio", "storyboard", "render", "final"}:
        base.extend([project / "article.md", project / "evidence.md", project / "script.md"])
    if stage in {"audio", "storyboard", "render", "final"}:
        base.extend([project / "audio", project / "audio" / "voice.mp3", project / "audio" / "voice.srt"])
    if stage in {"storyboard", "render", "final"}:
        base.extend([project / "storyboard.md", project / "hyperframes"])
    if stage in {"render", "final"}:
        base.extend([project / "output"])
    if stage == "final":
        base.extend([project / "output" / "final.mp4", project / "reports" / "final-check.md"])
    return base


def verify(project: Path, stage: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    failures: list[str] = []
    for path in required_paths(project, stage):
        passed = path.exists()
        checks.append({"path": str(path), "exists": passed, "kind": "directory" if path.is_dir() else "file"})
        if not passed:
            failures.append(f"missing required {path}")

    if stage in {"audio", "storyboard", "render", "final"}:
        _, errors = parse_srt(project / "audio" / "voice.srt")
        checks.append({"check": "srt_structure", "passed": not errors, "errors": errors})
        failures.extend(errors)

    return {
        "status": "PASS" if not failures else "FAIL",
        "project": str(project),
        "stage": stage,
        "failures": failures,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a knowledge-video project structure.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--stage", choices=STAGES, default="final")
    args = parser.parse_args()
    result = verify(Path(args.project).resolve(), args.stage)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 2)


if __name__ == "__main__":
    main()

