#!/usr/bin/env python3
"""
Läser frontmatter i docs/recept/*.md och genererar:
  - docs/index.md           : översikt med statusräknare + senast lagat
  - docs/recept/index.md    : sorterbar tabell över alla kort

Körs automatiskt i GitHub Actions före `mkdocs build`,
och kan köras lokalt: python3 scripts/bygg_katalog.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RECEPT = ROOT / "docs" / "recept"

STATUS_ORDNING = ["ny", "testad", "etablerad", "skrotad"]
STATUS_ETIKETT = {
    "ny": "🆕 Ny",
    "testad": "🧪 Testad",
    "etablerad": "✅ Etablerad",
    "skrotad": "🗑️ Skrotad",
}
KATEGORI_ORDNING = ["huvudrätt", "frukost", "bröd", "bakverk", "efterrätt", "glass", "tillbehör", "sås", "övrigt"]


def las_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"FEL i frontmatter: {path.name}: {e}", file=sys.stderr)
        return None
    fm["_fil"] = path.name
    return fm


def samla() -> list[dict]:
    kort = []
    for p in sorted(RECEPT.glob("*.md")):
        if p.name == "index.md":
            continue
        fm = las_frontmatter(p)
        if fm is None:
            print(f"VARNING: {p.name} saknar frontmatter — hoppar över", file=sys.stderr)
            continue
        if "titel" not in fm:
            print(f"VARNING: {p.name} saknar 'titel'", file=sys.stderr)
            fm["titel"] = p.stem
        kort.append(fm)
    return kort


def ja_nej(v) -> str:
    if v is True:
        return "✓"
    if v is False:
        return "✗"
    return "–"


def tabellrad(k: dict) -> str:
    status = STATUS_ETIKETT.get(k.get("status", ""), k.get("status", "–"))
    tid = f"{k['tid_min']} min" if k.get("tid_min") else "–"
    betyg = f"{k['betyg']:.1f}" if isinstance(k.get("betyg"), (int, float)) else "–"
    lagad = str(k.get("senast_lagad") or "–")
    return (
        f"| [{k['titel']}]({k['_fil']}) | {k.get('kategori') or '–'} | {k.get('protein') or '–'} "
        f"| {ja_nej(k.get('glutenfri'))} | {tid} | {status} | {betyg} | {ja_nej(k.get('charlie_ok'))} | {lagad} |"
    )


def bygg_recept_index(kort: list[dict]) -> str:
    rader = [
        "# Alla receptkort",
        "",
        "Klicka på en kolumnrubrik för att sortera. Sök med fältet uppe till höger — det söker i hela korttexten, inte bara titeln.",
        "",
        "| Rätt | Kategori | Protein | GF | Tid | Status | Betyg | Charlie | Senast lagad |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    nyckel = lambda k: (KATEGORI_ORDNING.index(k.get("kategori")) if k.get("kategori") in KATEGORI_ORDNING else 99, k["titel"].lower())
    rader += [tabellrad(k) for k in sorted(kort, key=nyckel)]
    return "\n".join(rader) + "\n"


def bygg_index(kort: list[dict]) -> str:
    antal = {s: sum(1 for k in kort if k.get("status") == s) for s in STATUS_ORDNING}
    olagade = [k for k in kort if k.get("status") == "ny"]
    senaste = sorted([k for k in kort if k.get("senast_lagad")], key=lambda k: str(k["senast_lagad"]), reverse=True)[:8]

    rader = [
        "# Glutenfria köket",
        "",
        "Hushållets receptkort. Varje kort är ett levande dokument: receptet som det ser ut just nu, plus loggen över varje gång det lagats och vad som ändrades.",
        "",
        "## Status",
        "",
        "| | |",
        "|---|---|",
    ]
    for s in STATUS_ORDNING:
        rader.append(f"| {STATUS_ETIKETT[s]} | **{antal[s]}** |")
    rader += ["", f"**{len(kort)} kort totalt.** [Visa alla →](recept/index.md)", ""]

    if olagade:
        rader += ["## Att prova", ""]
        for k in sorted(olagade, key=lambda k: k["titel"].lower()):
            rader.append(f"- [{k['titel']}](recept/{k['_fil']})")
        rader.append("")

    if senaste:
        rader += ["## Senast lagat", ""]
        for k in senaste:
            rader.append(f"- {k['senast_lagad']} — [{k['titel']}](recept/{k['_fil']})")
        rader.append("")

    return "\n".join(rader) + "\n"


def main() -> int:
    kort = samla()
    (RECEPT / "index.md").write_text(bygg_recept_index(kort), encoding="utf-8")
    (ROOT / "docs" / "index.md").write_text(bygg_index(kort), encoding="utf-8")
    print(f"Katalog byggd: {len(kort)} kort")
    return 0


if __name__ == "__main__":
    sys.exit(main())
