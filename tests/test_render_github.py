#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import render_github as pipeline  # noqa: E402


class RenderGithubTests(unittest.TestCase):
    def test_contracts_load(self) -> None:
        site = pipeline.site_map(pipeline.read_contract(pipeline.SITE_PATH, pipeline.SITE_HEADER))
        entries = pipeline.load_entries(
            pipeline.read_contract(pipeline.ENTRIES_PATH, pipeline.ENTRIES_HEADER)
        )
        self.assertEqual(site["github_user"], "valnet91")
        self.assertTrue(site["scanner_url"].startswith("https://aiready.alchimiste-ia.com/"))
        self.assertEqual(len(entries), 11)
        self.assertEqual(entries[0]["id"], "intro-scanner")
        controles = [row for row in entries if row["categorie"] == "controles-indispensables"]
        self.assertEqual(len(controles), 10)

    def test_render_is_deterministic_and_lf(self) -> None:
        site = pipeline.site_map(pipeline.read_contract(pipeline.SITE_PATH, pipeline.SITE_HEADER))
        entries = pipeline.load_entries(
            pipeline.read_contract(pipeline.ENTRIES_PATH, pipeline.ENTRIES_HEADER)
        )
        first = pipeline.render_readme(site, entries)
        second = pipeline.render_readme(site, entries)
        self.assertEqual(first, second)
        self.assertNotIn("\r", first)
        self.assertIn("https://aiready.alchimiste-ia.com/index.html", first)
        self.assertIn("https://github.com/valnet91", first)
        self.assertTrue(first.startswith("<!-- GENERE"))
        self.assertEqual(pipeline.README_PATH, ROOT / "README.md")

    def test_no_backdated_git_author(self) -> None:
        source = (ROOT / "tools" / "render_github.py").read_text(encoding="utf-8")
        self.assertNotIn("GIT_AUTHOR_DATE", source)
        self.assertNotIn("git push", source)


if __name__ == "__main__":
    unittest.main()
