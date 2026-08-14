#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import render_cards as cards  # noqa: E402


class RenderCardsTests(unittest.TestCase):
    def test_contract_and_naming(self) -> None:
        rows = cards.read_rows(cards.CARDS_PATH, cards.CARDS_HEADER)
        self.assertGreaterEqual(len(rows), 4)
        stems = {cards.card_stem(row) for row in rows}
        self.assertEqual(len(stems), len(rows))
        first = rows[0]
        self.assertTrue(cards.card_stem(first).startswith(first["date_classement"]))
        self.assertIn(first["fond"], cards.FONDS if hasattr(cards, "FONDS") else cards.ALLOWED_FONDS)

    def test_incomplete_gps_is_rejected(self) -> None:
        row = cards.read_rows(cards.CARDS_PATH, cards.CARDS_HEADER)[0].copy()
        row["gps_lat"] = "48.8566"
        row["gps_lon"] = "a"
        image = cards.paint_card(row, {"publisher": "Alchimiste IA", "canonical": "https://alchimiste-ia.com"})
        tmp = ROOT / "output" / "cards" / ".gps-test.webp"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        image.save(tmp, "WEBP")
        with self.assertRaises(cards.PipelineError) as caught:
            cards.write_metadata(tmp, row, {"author": "Test", "publisher": "Alchimiste IA"})
        tmp.unlink(missing_ok=True)
        self.assertIn("GPS_INCOMPLETE", str(caught.exception))

    def test_voices_are_henri_and_denise(self) -> None:
        self.assertEqual(cards.VOICES["henri"], "fr-FR-HenriNeural")
        self.assertEqual(cards.VOICES["denise"], "fr-FR-DeniseNeural")
        self.assertNotIn("henriette", cards.VOICES)

    def test_duo_alternates_henri_then_denise(self) -> None:
        row = {
            "titre": "Un",
            "ligne_2": "Deux",
            "ligne_3": "Trois",
        }
        self.assertEqual(
            cards.duo_turns(row),
            [("henri", "Un"), ("denise", "Deux"), ("henri", "Trois")],
        )


if __name__ == "__main__":
    unittest.main()
