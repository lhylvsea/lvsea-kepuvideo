#!/usr/bin/env python3
"""Validate the lvsea-kepuvideo package contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT_FILES = (
    "SKILL.md",
    "README.md",
    "USAGE.zh-CN.md",
    "LICENSE",
    "manifest.json",
    "agents/interface.yaml",
    "evals/trigger_cases.json",
    "reports/skill-ir.json",
    "reports/trigger-eval.json",
    "reports/prior-art-research.md",
    "reports/creation-handoff.md",
)
REPORT_FILES = ("reports/context-budget.json", "reports/output-evidence.json")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(read(path))
    return payload if isinstance(payload, dict) else {}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\s*\n(?P<body>.*?)\n---\s*", text, re.S)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("'\"")
    return result


def add(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"check": name, "passed": passed, "detail": detail})


def validate(root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []

    for relative in ROOT_FILES:
        path = root / relative
        passed = path.is_file()
        add(checks, f"file:{relative}", passed, str(path))
        if not passed:
            failures.append(f"missing required file: {relative}")

    for relative in REPORT_FILES:
        path = root / relative
        if not path.is_file():
            warnings.append(f"optional evidence report missing: {relative}")

    skill_text = read(root / "SKILL.md") if (root / "SKILL.md").is_file() else ""
    frontmatter = parse_frontmatter(skill_text)
    add(checks, "frontmatter:name", frontmatter.get("name") == "lvsea-kepuvideo", frontmatter.get("name", ""))
    add(checks, "frontmatter:description", bool(frontmatter.get("description")), "description is required")
    if frontmatter.get("name") != "lvsea-kepuvideo":
        failures.append("SKILL.md frontmatter name must be lvsea-kepuvideo")
    if not frontmatter.get("description"):
        failures.append("SKILL.md frontmatter description is missing")
    if len(skill_text.encode("utf-8")) > 14_000:
        warnings.append("SKILL.md exceeds the production context warning budget of 14,000 bytes")
    if re.search(r"(?:C:\\\\Users\\\\|/Users/|/home/|-----BEGIN .*PRIVATE KEY-----)", skill_text, re.I):
        failures.append("SKILL.md contains a private absolute path or private-key marker")
    nested = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("SKILL.md")
        if path != root / "SKILL.md" and ".git" not in path.parts and "__pycache__" not in path.parts
    )
    add(checks, "single-root-entrypoint", not nested, ", ".join(nested) or "only root SKILL.md")
    if nested:
        failures.append("nested SKILL.md entrypoints found: " + ", ".join(nested))

    manifest: dict[str, Any] = {}
    manifest_path = root / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest = load_json(manifest_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"manifest.json is invalid: {exc}")
    for field in ("name", "version", "owner", "updated_at", "status", "maturity_tier", "review_due", "review_cadence", "release_gates"):
        passed = bool(manifest.get(field))
        add(checks, f"manifest:{field}", passed, str(manifest.get(field, "")))
        if not passed:
            failures.append(f"manifest.json missing field: {field}")
    add(checks, "version-match", manifest.get("name") == frontmatter.get("name"), str(manifest.get("name", "")))
    if manifest.get("name") != frontmatter.get("name"):
        failures.append("manifest.json name does not match SKILL.md")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
        failures.append("manifest.json version is not semantic X.Y.Z")

    interface_text = read(root / "agents/interface.yaml") if (root / "agents/interface.yaml").is_file() else ""
    for field in ("display_name:", "short_description:", "default_prompt:", "examples:", "adapter_targets:", "allow_implicit_invocation:"):
        passed = field in interface_text
        add(checks, f"interface:{field}", passed, field)
        if not passed:
            failures.append(f"agents/interface.yaml missing {field}")

    cases: dict[str, Any] = {}
    cases_path = root / "evals/trigger_cases.json"
    if cases_path.is_file():
        try:
            cases = load_json(cases_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"trigger cases are invalid: {exc}")
    for bucket in ("should_trigger", "should_not_trigger", "near_neighbor", "adversarial"):
        passed = bool(cases.get(bucket))
        add(checks, f"trigger:{bucket}", passed, str(len(cases.get(bucket, []))))
        if not passed:
            failures.append(f"trigger cases missing bucket: {bucket}")

    ir_path = root / "reports/skill-ir.json"
    if ir_path.is_file():
        try:
            ir = load_json(ir_path)
            package = ir.get("package", {})
            passed = package.get("name") == manifest.get("name") and package.get("version") == manifest.get("version")
            add(checks, "ir-version-consistency", passed, json.dumps(package, ensure_ascii=False))
            if not passed:
                failures.append("reports/skill-ir.json package identity does not match manifest.json")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"reports/skill-ir.json is invalid: {exc}")

    trigger_path = root / "reports/trigger-eval.json"
    if trigger_path.is_file():
        try:
            trigger = load_json(trigger_path)
            summary = trigger.get("summary", {})
            passed = trigger.get("ok") is True and summary.get("total", 0) > 0 and summary.get("passed") == summary.get("total")
            add(checks, "trigger-report-pass", passed, json.dumps(summary, ensure_ascii=False))
            if not passed:
                failures.append("reports/trigger-eval.json is not passing all cases")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"reports/trigger-eval.json is invalid: {exc}")

    output_path = root / "reports/output-evidence.json"
    if output_path.is_file():
        try:
            output = load_json(output_path)
            if output.get("evidence_kind") not in {"provider_backed", "human_blind_review"}:
                warnings.append("provider or human video evidence is intentionally marked missing evidence")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"reports/output-evidence.json is invalid: {exc}")

    return {
        "status": "PASS" if not failures else "FAIL",
        "root": str(root),
        "failures": failures,
        "warnings": warnings,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the lvsea-kepuvideo package.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    args = parser.parse_args()
    result = validate(Path(args.skill_dir).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 2)


if __name__ == "__main__":
    main()

