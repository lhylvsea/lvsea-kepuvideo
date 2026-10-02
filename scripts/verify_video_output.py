#!/usr/bin/env python3
"""Verify MP4 streams and timing with ffprobe."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


def run_ffprobe(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        str(path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "ffprobe failed")
    payload = json.loads(completed.stdout)
    return payload if isinstance(payload, dict) else {}


def as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fps(stream: dict[str, Any]) -> float | None:
    raw = str(stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "")
    if "/" in raw:
        numerator, denominator = raw.split("/", 1)
        try:
            return float(numerator) / float(denominator)
        except (ValueError, ZeroDivisionError):
            return None
    return as_float(raw)


def stream_duration(stream: dict[str, Any], fallback: float | None) -> float | None:
    return as_float(stream.get("duration")) or fallback


def verify(args: argparse.Namespace) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    if shutil.which("ffprobe") is None:
        return {"status": "FAIL", "failures": ["ffprobe is not on PATH"], "warnings": [], "input": str(args.input)}
    if not args.input.is_file():
        return {"status": "FAIL", "failures": [f"input does not exist: {args.input}"], "warnings": [], "input": str(args.input)}
    try:
        metadata = run_ffprobe(args.input)
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "failures": [str(exc)], "warnings": [], "input": str(args.input)}

    streams = metadata.get("streams", [])
    video = next((row for row in streams if row.get("codec_type") == "video"), None)
    audio = next((row for row in streams if row.get("codec_type") == "audio"), None)
    format_data = metadata.get("format", {})
    duration = as_float(format_data.get("duration"))
    if video is None:
        failures.append("no video stream")
    if audio is None:
        failures.append("no audio stream")
    if video is not None:
        if args.expected_width and video.get("width") != args.expected_width:
            failures.append(f"width {video.get('width')} != {args.expected_width}")
        if args.expected_height and video.get("height") != args.expected_height:
            failures.append(f"height {video.get('height')} != {args.expected_height}")
        if args.expected_fps:
            actual_fps = fps(video)
            if actual_fps is None or abs(actual_fps - args.expected_fps) > 0.05:
                failures.append(f"fps {actual_fps} != {args.expected_fps}")
        if args.require_h264 and video.get("codec_name") not in {"h264", "libx264"}:
            failures.append(f"video codec is {video.get('codec_name')}, expected H.264")
    if audio is not None and args.require_aac and audio.get("codec_name") not in {"aac", "mp4a"}:
        failures.append(f"audio codec is {audio.get('codec_name')}, expected AAC")
    if args.expected_duration is not None and (duration is None or abs(duration - args.expected_duration) > args.max_delta):
        failures.append(f"duration {duration} differs from expected {args.expected_duration} by more than {args.max_delta}s")

    if args.audio is not None and args.audio.is_file():
        try:
            audio_meta = run_ffprobe(args.audio)
            audio_duration = as_float(audio_meta.get("format", {}).get("duration"))
            if duration is not None and audio_duration is not None and abs(duration - audio_duration) > args.max_delta:
                failures.append(f"video/audio duration mismatch: video={duration}, audio={audio_duration}")
        except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"audio ffprobe failed: {exc}")
    elif args.audio is not None:
        failures.append(f"audio file does not exist: {args.audio}")

    warnings.append("visual review, black-frame review, subtitle overflow and final-frame review remain manual checks")
    return {
        "status": "PASS" if not failures else "FAIL",
        "input": str(args.input),
        "duration": duration,
        "video_stream": video,
        "audio_stream": audio,
        "failures": failures,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a rendered MP4 with ffprobe.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--expected-width", type=int)
    parser.add_argument("--expected-height", type=int)
    parser.add_argument("--expected-fps", type=float, default=30.0)
    parser.add_argument("--expected-duration", type=float)
    parser.add_argument("--max-delta", type=float, default=0.15)
    parser.add_argument("--no-h264-check", dest="require_h264", action="store_false")
    parser.add_argument("--no-aac-check", dest="require_aac", action="store_false")
    parser.set_defaults(require_h264=True, require_aac=True)
    args = parser.parse_args()
    result = verify(args)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    raise SystemExit(0 if result["status"] == "PASS" else 2)


if __name__ == "__main__":
    main()

