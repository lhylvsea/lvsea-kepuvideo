#!/usr/bin/env python3
"""Small deterministic checks for the lvsea-kepuvideo package itself."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_manifest_identity_and_version(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "lvsea-kepuvideo")
        self.assertRegex(manifest["version"], r"^0\.1\.0$")

    def test_required_entry_and_adapter_exist(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        adapter = (ROOT / "references" / "writing-adapter.md").read_text(encoding="utf-8")
        self.assertIn("name: lvsea-kepuvideo", skill)
        self.assertIn("lvsea-writing", skill)
        self.assertIn("humanizer-zh", adapter)

    def test_governance_files_are_present(self) -> None:
        for relative in (
            "agents/interface.yaml",
            "evals/trigger_cases.json",
            "reports/source-process.md",
            "reports/creation-handoff.md",
            "scripts/validate_skill.py",
            "scripts/verify_project.py",
            "scripts/verify_video_output.py",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
