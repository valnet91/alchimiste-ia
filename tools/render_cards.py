#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render CSV-driven WebP cards with honest EXIF/XMP and optional Edge TTS."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCHEMA_VERSION = "1"
EMPTY = "a"
CARDS_HEADER = (
    "schema_version",
    "id",
    "locale",
    "sequence",
    "date_classement",
    "date_modif",
    "categorie",
    "fond",
    "titre",
    "ligne_2",
    "ligne_3",
    "slug",
    "logo",
    "insert_image",
    "insert_after",
    "voix",
    "gps_lat",
    "gps_lon",
    "gps_label",
    "alt",
    "state",
)
ALLOWED_FONDS = {
    "cobalt": ("#12355B", "#F5F0E6", "#D6A545"),
    "cramoisi": ("#8B1E3F", "#F5F0E6", "#D6A545"),
    "noir": ("#0A0A0A", "#F5F0E6", "#D6A545"),
    "blanc": ("#FBFAF6", "#14221F", "#A9761E"),
}
VOICES = {
    "henri": "fr-FR-HenriNeural",
    "denise": "fr-FR-DeniseNeural",
}
DUO = "duo"
SIZE = (1200, 630)

ROOT = Path(__file__).resolve().parent.parent
SITE_PATH = ROOT / "contracts" / "site.csv"
CARDS_PATH = ROOT / "contracts" / "cards.csv"
OUTPUT_DIR = ROOT / "output" / "cards"
EXIFTOOL = shutil.which("exiftool")
FFMPEG = shutil.which("ffmpeg")


class PipelineError(Exception):
    def __init__(self, code: str, path: Path, line: int, message: str) -> None:
        super().__init__(f"ERROR|{code}|{path.as_posix()}|{line}|{message}")


def fail(code: str, path: Path, line: int, message: str) -> None:
    raise PipelineError(code, path, line, message)


def empty(value: str) -> bool:
    return value.strip() in {"", EMPTY}


def read_rows(path: Path, header: tuple[str, ...]) -> list[dict[str, str]]:
    if not path.is_file():
        fail("CSV_MISSING", path, 0, "contract file is missing")
    raw = path.read_bytes()
    if b"\r\n" in raw or b"\r" in raw:
        fail("CSV_CRLF", path, 0, "contract must use LF only")
    lines = [line for line in raw.decode("utf-8").split("\n") if line and not line.startswith("#")]
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


def site_map() -> dict[str, str]:
    values: dict[str, str] = {}
    for row in read_rows(SITE_PATH, ("schema_version", "key", "value")):
        values[row["key"]] = row["value"]
    return values


def slugify(text: str) -> str:
    table = str.maketrans(
        {
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
            "’": "-",
            "'": "-",
            "/": "-",
            "—": "-",
        }
    )
    slug = text.lower().translate(table)
    slug = re.sub(r"[^a-z0-9-]+", "-", slug)
    return slug.strip("-")


def card_stem(row: dict[str, str]) -> str:
    slug = row["slug"] if not empty(row["slug"]) else slugify(row["titre"])
    return f"{row['date_classement']}_{row['categorie']}_{slug}_{row['locale']}"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    path = Path(r"C:\Windows\Fonts") / name
    if not path.exists():
        path = Path(r"C:\Windows\Fonts\arial.ttf")
    return ImageFont.truetype(str(path), size)


def draw_mark(draw: ImageDraw.ImageDraw, accent: str, ink: str) -> None:
    draw.ellipse((56, 48, 128, 120), outline=accent, width=4)
    font = load_font(36, bold=True)
    draw.text((78, 58), "A", font=font, fill=accent)


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_card(row: dict[str, str], site: dict[str, str]) -> Image.Image:
    if row["fond"] not in ALLOWED_FONDS:
        fail("FOND", CARDS_PATH, int(row["__line__"]), row["fond"])
    background, ink, accent = ALLOWED_FONDS[row["fond"]]
    image = Image.new("RGB", SIZE, background)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 18, SIZE[1]), fill=accent)
    draw_mark(draw, accent, ink)

    title_font = load_font(46, bold=True)
    body_font = load_font(28)
    small_font = load_font(18)
    max_width = 1040
    y = 160
    blocks: list[tuple[str, ImageFont.FreeTypeFont]] = [(row["titre"], title_font)]
    if not empty(row["ligne_2"]):
        blocks.append((row["ligne_2"], body_font))
    if not empty(row["ligne_3"]):
        blocks.append((row["ligne_3"], body_font))

    insert_after = None if empty(row["insert_after"]) else int(row["insert_after"])
    for index, (text, font) in enumerate(blocks, start=1):
        for line in wrap(draw, text, font, max_width):
            draw.text((64, y), line, font=font, fill=ink)
            y += font.size + 10
        y += 16
        if insert_after == index and not empty(row["insert_image"]):
            insert_path = (ROOT / row["insert_image"]).resolve()
            if not insert_path.is_file():
                fail("INSERT_MISSING", CARDS_PATH, int(row["__line__"]), row["insert_image"])
            inset = Image.open(insert_path).convert("RGB")
            inset.thumbnail((220, 140))
            image.paste(inset, (64, y))
            y += inset.height + 24

    if not empty(row["logo"]):
        logo_path = (ROOT / row["logo"]).resolve()
        if logo_path.is_file() and logo_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((72, 72))
            image.paste(logo, (1080, 48), logo)

    credit = f"{site.get('publisher', 'Alchimiste IA')} · {site.get('canonical', '')}"
    draw.text((64, 580), credit, font=small_font, fill=accent)
    return image


def exif_dates(value: str) -> str:
    if " " in value:
        date, time = value.split(" ", 1)
    else:
        date, time = value, "12:00:00"
    return f"{date.replace('-', ':')} {time}"


def write_metadata(path: Path, row: dict[str, str], site: dict[str, str]) -> None:
    if not EXIFTOOL:
        fail("EXIFTOOL", path, 0, "exiftool not found on PATH")
    created = exif_dates(row["date_classement"])
    modified = exif_dates(row["date_modif"] if not empty(row["date_modif"]) else row["date_classement"])
    description = row["alt"] if not empty(row["alt"]) else row["titre"]
    args = [
        EXIFTOOL,
        "-overwrite_original",
        "-charset",
        "utf8",
        f"-Artist={site.get('author', '')}",
        f"-Creator={site.get('author', '')}",
        f"-Copyright=© {site.get('publisher', 'Alchimiste IA')}",
        f"-XMP-dc:Title={row['titre']}",
        f"-XMP-dc:Description={description}",
        f"-XMP-dc:Creator={site.get('author', '')}",
        f"-XMP-dc:Rights=© {site.get('publisher', 'Alchimiste IA')}",
        f"-XMP-dc:Subject={row['categorie']}",
        f"-IPTC:Keywords={row['categorie']}",
        f"-ImageDescription={description}",
        f"-XPComment=Generated from contracts/cards.csv id={row['id']}",
        "-Software=Alchimiste_Github/render_cards.py + exiftool",
        f"-DateTimeOriginal={created}",
        f"-CreateDate={created}",
        f"-ModifyDate={modified}",
        f"-XMP-xmp:CreateDate={created}",
        f"-XMP-xmp:ModifyDate={modified}",
    ]
    if not empty(row["gps_lat"]) and not empty(row["gps_lon"]):
        lat = float(row["gps_lat"])
        lon = float(row["gps_lon"])
        args.extend(
            [
                f"-GPSLatitude={abs(lat)}",
                f"-GPSLatitudeRef={'N' if lat >= 0 else 'S'}",
                f"-GPSLongitude={abs(lon)}",
                f"-GPSLongitudeRef={'E' if lon >= 0 else 'W'}",
            ]
        )
        if not empty(row["gps_label"]):
            args.append(f"-XMP-iptcCore:Location={row['gps_label']}")
    elif not empty(row["gps_lat"]) or not empty(row["gps_lon"]):
        fail("GPS_INCOMPLETE", CARDS_PATH, int(row["__line__"]), "gps_lat and gps_lon must both be set")
    args.append(str(path))
    subprocess.run(args, check=True, capture_output=True, text=True)


def _prepare_ssl() -> None:
    import ssl

    try:
        import certifi
    except ImportError:
        return

    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

    def _certifi_context(
        purpose: ssl.Purpose = ssl.Purpose.SERVER_AUTH,
        *,
        cafile: str | None = None,
        capath: str | None = None,
        cadata: str | None = None,
    ) -> ssl.SSLContext:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=cafile or certifi.where(), capath=capath, cadata=cadata)
        return context

    ssl.create_default_context = _certifi_context  # type: ignore[method-assign]


def speak(text: str, voice_key: str, dest: Path) -> None:
    voice = VOICES[voice_key]
    _prepare_ssl()
    import asyncio

    import edge_tts

    async def _run() -> None:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(dest))

    asyncio.run(_run())


def spoken_lines(row: dict[str, str]) -> list[str]:
    parts = [row["titre"]]
    if not empty(row["ligne_2"]):
        parts.append(row["ligne_2"])
    if not empty(row["ligne_3"]):
        parts.append(row["ligne_3"])
    return parts


def spoken_text(row: dict[str, str]) -> str:
    return ". ".join(spoken_lines(row))


def expected_audio_name(stem: str, voix: str) -> str:
    if empty(voix):
        return ""
    suffix = DUO if voix == DUO else voix
    return f"{stem}_{suffix}.mp3"


def voice_label(voix: str) -> str:
    return {"henri": "Henri", "denise": "Denise", DUO: "Henri et Denise"}.get(voix, voix)


def render_demo_html(site: dict[str, str], cards: list[dict[str, str]]) -> str:
    items: list[str] = []
    for card in cards:
        transcript = html.escape(" ".join(spoken_lines(card)))
        titre = html.escape(card["titre"])
        alt = html.escape(card["alt"] if not empty(card["alt"]) else card["titre"])
        speaker = html.escape(voice_label(card["voix"]))
        audio = html.escape(card["audio_name"])
        webp = html.escape(card["webp_name"])
        button = ""
        player = ""
        if audio:
            button = (
                f'<button type="button" data-audio="{html.escape(card["id"])}-audio">'
                f"Écouter {speaker}</button>"
            )
            player = (
                f'<audio id="{html.escape(card["id"])}-audio" preload="none" src="{audio}">'
                f"</audio>"
            )
        items.append(
            f"""<article class="card fond-{html.escape(card["fond"])}">
  <img src="{webp}" width="1200" height="630" alt="{alt}">
  <div class="copy">
    <p class="voice">{speaker}</p>
    <h2>{titre}</h2>
    <p class="transcript">{transcript}</p>
    {button}
    {player}
  </div>
</article>"""
        )
    body = "\n".join(items)
    title = html.escape(site.get("title", "Alchimiste IA"))
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — cartes parlantes</title>
  <style>
    :root {{ color-scheme: dark; --ink: #f5f0e6; --paper: #0a0a0a; --gold: #d6a545; --line: #2a2a2a; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font: 1rem/1.5 Segoe UI, sans-serif; color: var(--ink); background: var(--paper); }}
    header, footer {{ width: min(1100px, calc(100% - 2rem)); margin: 0 auto; padding: 1.5rem 0; }}
    h1 {{ margin: 0 0 .4rem; font-size: 1.6rem; }}
    header p, footer p {{ margin: 0; color: #b8b0a2; }}
    main {{ width: min(1100px, calc(100% - 2rem)); margin: 0 auto 3rem; display: grid; gap: 1.5rem; }}
    .card {{ display: grid; gap: 1rem; padding: 1rem; border: 1px solid var(--line); border-radius: 1rem; background: #141414; }}
    .card img {{ width: 100%; height: auto; border-radius: .6rem; }}
    .voice {{ margin: 0 0 .3rem; color: var(--gold); font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; }}
    h2 {{ margin: 0 0 .5rem; font-size: 1.15rem; }}
    .transcript {{ margin: 0 0 1rem; }}
    button {{ min-height: 2.75rem; padding: .6rem 1rem; border: 0; border-radius: 999px; background: var(--gold); color: #14221f; font-weight: 700; cursor: pointer; }}
    button[aria-pressed="true"] {{ background: #f5f0e6; }}
    a {{ color: var(--gold); }}
    @media (min-width: 800px) {{ .card {{ grid-template-columns: 1.3fr .7fr; align-items: center; }} }}
  </style>
</head>
<body>
  <header>
    <h1>{title} — cartes parlantes</h1>
    <p>Même texte que la carte. Un clic : Henri, Denise, ou le duo.</p>
  </header>
  <main>
{body}
  </main>
  <footer>
    <p><a href="{html.escape(site.get("site_url", "https://alchimiste-ia.com/"))}">{html.escape(site.get("canonical", "https://alchimiste-ia.com"))}</a>
    · page générée depuis contracts/cards.csv</p>
  </footer>
  <script>
    const buttons = document.querySelectorAll("button[data-audio]");
    const stopAll = (except) => {{
      document.querySelectorAll("audio").forEach((audio) => {{
        if (audio !== except) {{ audio.pause(); audio.currentTime = 0; }}
      }});
      buttons.forEach((button) => button.setAttribute("aria-pressed", "false"));
    }};
    buttons.forEach((button) => {{
      const audio = document.getElementById(button.getAttribute("data-audio"));
      if (!audio) return;
      button.addEventListener("click", () => {{
        if (audio.paused) {{ stopAll(audio); audio.play(); button.setAttribute("aria-pressed", "true"); }}
        else {{ audio.pause(); button.setAttribute("aria-pressed", "false"); }}
      }});
      audio.addEventListener("ended", () => button.setAttribute("aria-pressed", "false"));
    }});
  </script>
</body>
</html>
"""


def duo_turns(row: dict[str, str]) -> list[tuple[str, str]]:
    order = ("henri", "denise")
    return [(order[index % 2], line) for index, line in enumerate(spoken_lines(row))]


def concat_mp3(parts: list[Path], dest: Path) -> None:
    if not FFMPEG:
        fail("FFMPEG", dest, 0, "ffmpeg not found on PATH")
    listing = dest.with_suffix(".concat.txt")
    listing.write_text("".join(f"file '{part.name}'\n" for part in parts), encoding="utf-8")
    try:
        subprocess.run(
            [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", listing.name, "-c", "copy", dest.name],
            check=True,
            capture_output=True,
            text=True,
            cwd=dest.parent,
        )
    finally:
        listing.unlink(missing_ok=True)


def render_audio(row: dict[str, str], stem: str) -> str:
    voix = row["voix"]
    if voix == DUO:
        clips: list[Path] = []
        try:
            for index, (speaker, line) in enumerate(duo_turns(row), start=1):
                clip = OUTPUT_DIR / f".{stem}_{speaker}_{index}.mp3"
                speak(line, speaker, clip)
                clips.append(clip)
            audio_path = OUTPUT_DIR / f"{stem}_duo.mp3"
            concat_mp3(clips, audio_path)
        finally:
            for clip in clips:
                clip.unlink(missing_ok=True)
        return audio_path.name
    if voix not in VOICES:
        fail("VOIX", CARDS_PATH, int(row["__line__"]), voix)
    audio_path = OUTPUT_DIR / f"{stem}_{voix}.mp3"
    speak(spoken_text(row), voix, audio_path)
    return audio_path.name


def compare_or_write(path: Path, payload: bytes, check: bool) -> str:
    if path.exists() and path.read_bytes() == payload:
        return "unchanged"
    if check:
        digest = hashlib.sha256(payload).hexdigest()
        fail("GENERATED_DRIFT", path, 0, f"{path.name} differs sha256={digest}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return "updated"


def render_all(check: bool, with_audio: bool) -> int:
    site = site_map()
    rows = read_rows(CARDS_PATH, CARDS_HEADER)
    states: list[str] = []
    demo_cards: list[dict[str, str]] = []
    manifest: list[list[str]] = [["id", "stem", "webp", "audio", "voix"]]
    for row in rows:
        if row["state"] != "source":
            fail("STATE", CARDS_PATH, int(row["__line__"]), row["state"])
        stem = card_stem(row)
        webp_path = OUTPUT_DIR / f"{stem}.webp"
        image = paint_card(row, site)
        raw = image.tobytes()
        # Encode then stamp metadata; --check compares pixels before EXIF.
        buffer_path = OUTPUT_DIR / f".{stem}.tmp.webp"
        buffer_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(buffer_path, "WEBP", quality=90, method=6)
        pixels = Image.open(buffer_path).tobytes()
        if check:
            if not webp_path.is_file():
                buffer_path.unlink(missing_ok=True)
                fail("GENERATED_DRIFT", webp_path, 0, "missing webp")
            current = Image.open(webp_path).convert("RGB").tobytes()
            buffer_path.unlink(missing_ok=True)
            if current != pixels:
                fail("GENERATED_DRIFT", webp_path, 0, "pixels differ")
            states.append(f"{stem}=unchanged")
        else:
            buffer_path.replace(webp_path)
            write_metadata(webp_path, row, site)
            states.append(f"{stem}=updated")
        if not empty(row["voix"]) and row["voix"] != DUO and row["voix"] not in VOICES:
            fail("VOIX", CARDS_PATH, int(row["__line__"]), row["voix"])
        audio_name = expected_audio_name(stem, row["voix"])
        if with_audio and audio_name and not check:
            audio_name = render_audio(row, stem)
        row["webp_name"] = webp_path.name
        row["audio_name"] = audio_name
        demo_cards.append(row)
        manifest.append([row["id"], stem, webp_path.name, audio_name, row["voix"]])
        del raw

    body = ["# genere — ne pas editer"]
    from io import StringIO

    buf = StringIO()
    writer = csv.writer(buf, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writerows(manifest)
    payload = ("\n".join(body) + "\n" + buf.getvalue()).encode("utf-8")
    states.append(f"manifest={compare_or_write(OUTPUT_DIR / 'manifest.csv', payload, check)}")
    demo = render_demo_html(site, demo_cards)
    states.append(f"demo={compare_or_write(OUTPUT_DIR / 'index.html', demo.encode('utf-8'), check)}")
    print("OK|CARDS|" + "|".join(states))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--audio", action="store_true", help="also render Edge TTS mp3")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return render_all(check=args.check, with_audio=args.audio)
    except PipelineError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        print(f"ERROR|SUBPROCESS|0|0|{exc.stderr}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
