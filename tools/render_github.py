#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render Alchimiste GitHub artifacts from CSV contracts. Deterministic, LF only."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "1"
SITE_HEADER = (
    "schema_version",
    "key",
    "value",
)
ENTRIES_HEADER = (
    "schema_version",
    "id",
    "locale",
    "sequence",
    "date_classement",
    "categorie",
    "priorite",
    "emoji",
    "titre",
    "slug",
    "corps",
    "dod",
    "note",
    "state",
)
ALLOWED_STATES = {"source"}
ALLOWED_LOCALES = {"fr"}
EMPTY = "a"
BANNER = "<!-- GENERE depuis contracts/*.csv par tools/render_github.py -- NE PAS EDITER A LA MAIN -->\n"

ROOT = Path(__file__).resolve().parent.parent
SITE_PATH = ROOT / "contracts" / "site.csv"
ENTRIES_PATH = ROOT / "contracts" / "entries.csv"
OUTPUT_DIR = ROOT / "output"
CONTROLES_DIR = OUTPUT_DIR / "controles"


class PipelineError(Exception):
    def __init__(self, code: str, path: Path, line: int, message: str) -> None:
        super().__init__(f"ERROR|{code}|{path.as_posix()}|{line}|{message}")
        self.code = code


def fail(code: str, path: Path, line: int, message: str) -> None:
    raise PipelineError(code, path, line, message)


def read_contract(path: Path, header: tuple[str, ...]) -> list[dict[str, str]]:
    if not path.is_file():
        fail("CSV_MISSING", path, 0, "contract file is missing")
    raw = path.read_bytes()
    if b"\r\n" in raw or b"\r" in raw:
        fail("CSV_CRLF", path, 0, "contract must use LF only")
    text = raw.decode("utf-8")
    lines = [line for line in text.split("\n") if line and not line.startswith("#")]
    reader = csv.DictReader(lines, delimiter=";", quotechar='"')
    if reader.fieldnames != list(header):
        fail("CSV_HEADER", path, 1, f"expected {header}")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(reader, start=2):
        if row.get("schema_version") != SCHEMA_VERSION:
            fail("SCHEMA_VERSION", path, index, "unsupported schema_version")
        row["__line__"] = str(index)
        rows.append(row)
    return rows


def site_map(rows: list[dict[str, str]]) -> dict[str, str]:
    values: dict[str, str] = {}
    for row in rows:
        key = row["key"].strip()
        if not key:
            fail("SITE_KEY", SITE_PATH, int(row["__line__"]), "empty key")
        if key in values:
            fail("SITE_KEY_DUPLICATE", SITE_PATH, int(row["__line__"]), key)
        values[key] = row["value"]
    required = (
        "canonical",
        "site_url",
        "scanner_url",
        "consultant_url",
        "github_user",
        "github_profile",
        "author",
        "publisher",
        "rna",
        "contact",
        "title",
        "tagline",
    )
    for key in required:
        if key not in values or not values[key]:
            fail("SITE_REQUIRED", SITE_PATH, 0, f"missing {key}")
    return values


def field_or_empty(value: str) -> str:
    return "" if value.strip() in {"", EMPTY} else value


def slugify(title: str) -> str:
    text = title.lower()
    replacements = {
        "à": "a",
        "â": "a",
        "ä": "a",
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "î": "i",
        "ï": "i",
        "ô": "o",
        "ö": "o",
        "ù": "u",
        "û": "u",
        "ü": "u",
        "ç": "c",
        "œ": "oe",
        "—": "-",
        "–": "-",
        "'": "-",
        "’": "-",
        "/": "-",
        "«": "",
        "»": "",
    }
    for source, dest in replacements.items():
        text = text.replace(source, dest)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def load_entries(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    prepared: list[dict[str, str]] = []
    for row in rows:
        line = int(row["__line__"])
        if row["locale"] not in ALLOWED_LOCALES:
            fail("LOCALE", ENTRIES_PATH, line, row["locale"])
        if row["state"] not in ALLOWED_STATES:
            fail("STATE", ENTRIES_PATH, line, row["state"])
        if not row["id"] or row["id"] in seen:
            fail("ENTRY_ID", ENTRIES_PATH, line, "missing or duplicate id")
        seen.add(row["id"])
        try:
            sequence = int(row["sequence"])
        except ValueError:
            fail("SEQUENCE", ENTRIES_PATH, line, "sequence must be an integer")
        slug = field_or_empty(row["slug"]) or slugify(row["titre"])
        prepared.append(
            {
                **{name: row[name] for name in ENTRIES_HEADER},
                "sequence_int": str(sequence),
                "slug": slug,
                "emoji": field_or_empty(row["emoji"]),
                "corps": field_or_empty(row["corps"]),
                "dod": field_or_empty(row["dod"]),
                "note": field_or_empty(row["note"]),
            }
        )
    prepared.sort(key=lambda item: (item["date_classement"], int(item["sequence_int"]), item["id"]))
    return prepared


def heading(entry: dict[str, str]) -> str:
    label = entry["titre"]
    if entry["priorite"] and entry["priorite"] != EMPTY:
        label = f"{label} — {entry['priorite']}"
    if entry["emoji"]:
        return f"{entry['emoji']} {label}"
    return label


def render_readme(site: dict[str, str], entries: list[dict[str, str]]) -> str:
    lines = [
        BANNER.rstrip("\n"),
        "---",
        f"canonical: {site['canonical']}",
        f"author: {site['author']}",
        f"publisher: {site['publisher']}",
        f"rna: {site['rna']}",
        "---",
        "",
        f"# {site['title']}",
        "",
        f"> {site['tagline']}",
        f"> {site['site_url']} · {site['github_profile']} · RNA {site['rna']}",
        "",
        "## Scanner",
        "",
        f"- Site : [{site['site_url']}]({site['site_url']})",
        f"- Audit AI-READY : [{site['scanner_url']}]({site['scanner_url']})",
        f"- Consultant : [{site['consultant_url']}]({site['consultant_url']})",
        f"- Compte GitHub : [{site['github_user']}]({site['github_profile']})",
        "",
        "## Sommaire",
        "",
    ]
    for entry in entries:
        label = heading(entry)
        lines.append(f"- [{label}](#{entry['slug']})")
    lines.append("")
    for entry in entries:
        lines.append(f'<a id="{entry["slug"]}"></a>')
        lines.append(f"### {heading(entry)}")
        lines.append("")
        if entry["corps"]:
            lines.append(entry["corps"])
            lines.append("")
        if entry["dod"]:
            lines.append(f"**Definition of Done :** {entry['dod']}")
            lines.append("")
        if entry["note"]:
            lines.append(entry["note"])
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_llms(site: dict[str, str], entries: list[dict[str, str]]) -> str:
    lines = [
        f"# {site['title']}",
        "",
        f"> {site['tagline']}",
        "",
        "Standard: AI-READY",
        "Focus: AI-First",
        "",
        "## Ressources",
        "",
        f"- Site: {site['site_url']}",
        f"- Audit AI-READY: {site['scanner_url']}",
        f"- Consultant: {site['consultant_url']}",
        f"- GitHub: {site['github_profile']}",
        "",
        "## Dix contrôles",
        "",
    ]
    for entry in entries:
        if entry["categorie"] != "controles-indispensables":
            continue
        lines.append(f"### {heading(entry)}")
        if entry["corps"]:
            lines.append(entry["corps"])
        if entry["dod"]:
            lines.append(f"DoD: {entry['dod']}")
        lines.append("")
    lines.extend(
        [
            "## Entité",
            "",
            f"- Organisation: {site['publisher']}",
            f"- Éditeur: {site['author']}",
            f"- Contact: {site['contact']}",
            f"- RNA: {site['rna']}",
            "",
        ]
    )
    return "\n".join(lines)


def render_fiche(site: dict[str, str], entry: dict[str, str]) -> str:
    lines = [
        BANNER.rstrip("\n"),
        "---",
        f"canonical: {site['canonical']}",
        f"id: {entry['id']}",
        f"date_classement: {entry['date_classement']}",
        f"categorie: {entry['categorie']}",
        "---",
        "",
        f"# {heading(entry)}",
        "",
    ]
    if entry["corps"]:
        lines.append(entry["corps"])
        lines.append("")
    if entry["dod"]:
        lines.append(f"**Definition of Done :** {entry['dod']}")
        lines.append("")
    if entry["note"]:
        lines.append(entry["note"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def compare_or_write(path: Path, text: str, check: bool) -> str:
    expected = text.encode("utf-8")
    if path.exists() and path.read_bytes() == expected:
        return "unchanged"
    if check:
        digest = hashlib.sha256(expected).hexdigest()
        fail("GENERATED_DRIFT", path, 0, f"generated file differs; sha256={digest}")
    write_lf(path, text)
    return "updated"


def render_all(check: bool) -> int:
    site = site_map(read_contract(SITE_PATH, SITE_HEADER))
    entries = load_entries(read_contract(ENTRIES_PATH, ENTRIES_HEADER))
    readme = render_readme(site, entries)
    llms = render_llms(site, entries)
    states = [
        f"readme={compare_or_write(OUTPUT_DIR / 'README.md', readme, check)}",
        f"llms={compare_or_write(OUTPUT_DIR / 'llms.txt', llms, check)}",
    ]
    for entry in entries:
        if entry["categorie"] != "controles-indispensables":
            continue
        fiche = render_fiche(site, entry)
        path = CONTROLES_DIR / f"{entry['id']}.md"
        states.append(f"{entry['id']}={compare_or_write(path, fiche, check)}")
    print("OK|RENDER|" + "|".join(states))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return render_all(check=args.check)
    except PipelineError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
