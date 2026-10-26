#!/usr/bin/env python3
"""
Kontrollerar att alla kort i docs/recept/ följer layouten i docs/metod.md.

Körs lokalt (python3 scripts/kontrollera_kort.py [fil ...]) och i CI.
Avslutar med kod 1 om något kort bryter mot reglerna.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RECEPT = ROOT / "docs" / "recept"

KATEGORIER = {"huvudrätt", "bröd", "bakverk", "efterrätt", "glass", "tillbehör", "sås", "frukost", "övrigt"}
PROTEINER = {"kyckling", "fläsk", "nöt", "anka", "fisk", "vegetariskt", None}
STATUS = {"ny", "testad", "etablerad", "skrotad"}
FM_KRAV = ["titel", "kategori", "protein", "glutenfri", "tid_min", "status", "senast_lagad", "betyg", "charlie_ok", "tags"]

SEKTIONER = ["Ingredienser", "Tidsplan", "Gör så här", "Charlie-version", "Servering", "Att tänka på", "Logg"]
OBLIGATORISKA = {"Ingredienser", "Gör så här", "Charlie-version", "Att tänka på", "Logg"}

TABELLHUVUD = "| Mängd | Ingrediens |"
TABELLSKILJE = "|---:|---|"


def fel(path: Path, msg: str, rad: int | None = None) -> str:
    var = f"{path.name}:{rad}" if rad else path.name
    return f"  {var}: {msg}"


def dela(text: str) -> tuple[dict | None, list[str], int]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None, text.splitlines(), 0
    fm = yaml.safe_load(m.group(1)) or {}
    offset = m.group(0).count("\n")
    return fm, text[m.end():].splitlines(), offset


def kontrollera(path: Path) -> list[str]:
    f: list[str] = []
    fm, rader, offset = dela(path.read_text(encoding="utf-8"))
    if fm is None:
        return [fel(path, "saknar frontmatter")]

    # --- frontmatter ---
    for k in FM_KRAV:
        if k not in fm:
            f.append(fel(path, f"frontmatter saknar `{k}`"))
    if fm.get("kategori") not in KATEGORIER:
        f.append(fel(path, f"okänd kategori: {fm.get('kategori')!r}"))
    if fm.get("protein") not in PROTEINER:
        f.append(fel(path, f"okänt protein: {fm.get('protein')!r}"))
    if fm.get("status") not in STATUS:
        f.append(fel(path, f"okänd status: {fm.get('status')!r}"))
    tags = fm.get("tags") or []
    if not isinstance(tags, list) or not 3 <= len(tags) <= 6:
        f.append(fel(path, f"tags ska vara 3–6 st, är {len(tags) if isinstance(tags, list) else '?'}"))
    elif any(t != t.lower() for t in tags):
        f.append(fel(path, "tags ska vara små bokstäver"))

    # --- rubriker ---
    h1 = [(i, r) for i, r in enumerate(rader) if r.startswith("# ")]
    if len(h1) != 1:
        f.append(fel(path, f"exakt en H1 krävs, hittade {len(h1)}"))
    else:
        i, r = h1[0]
        if r[2:].strip() != str(fm.get("titel", "")).strip():
            f.append(fel(path, f"H1 {r[2:].strip()!r} skiljer sig från titel {fm.get('titel')!r}", i + offset + 1))
        # metarad: första icke-tomma raden efter H1
        efter = [x for x in rader[i + 1:i + 4] if x.strip()]
        if not efter or not re.match(r"^\*\*.+·.+·.+\*\*$", efter[0].strip()):
            f.append(fel(path, "raden efter H1 ska vara metaraden `**portioner · tid · glutenfri**`", i + offset + 2))

    h2 = [(i, r[3:].strip()) for i, r in enumerate(rader) if r.startswith("## ")]
    namn = [n for _, n in h2]
    for i, n in h2:
        if n not in SEKTIONER:
            f.append(fel(path, f"okänd sektion `## {n}`", i + offset + 1))
    for n in OBLIGATORISKA:
        if n not in namn:
            f.append(fel(path, f"saknar sektionen `## {n}`"))
    ordning = [SEKTIONER.index(n) for n in namn if n in SEKTIONER]
    if ordning != sorted(ordning):
        f.append(fel(path, f"sektionerna kommer i fel ordning: {' → '.join(namn)}"))
    if len(namn) != len(set(namn)):
        f.append(fel(path, "en sektion förekommer två gånger"))

    # --- sektionernas innehåll ---
    gränser = [i for i, _ in h2] + [len(rader)]
    for (i, n), slut in zip(h2, gränser[1:]):
        block = rader[i + 1:slut]
        start = i + 1

        if n == "Ingredienser":
            for j, r in enumerate(block):
                s = r.strip()
                nr = start + j + offset + 1
                if re.match(r"^[-*] ", s):
                    f.append(fel(path, "punktlista under Ingredienser — ska vara tabell", nr))
                if s.startswith("#"):
                    f.append(fel(path, "rubrik under Ingredienser — gruppera med **fet text**", nr))
                if s.startswith("|") and j + 1 < len(block) and block[j + 1].strip().startswith("|---"):
                    if s != TABELLHUVUD:
                        f.append(fel(path, f"tabellhuvud ska vara `{TABELLHUVUD}`, är `{s}`", nr))
                    if block[j + 1].strip() != TABELLSKILJE:
                        f.append(fel(path, f"skiljerad ska vara `{TABELLSKILJE}`", nr + 1))
                elif s.startswith("|") and not s.startswith("|---") and s != TABELLHUVUD:
                    celler = [c.strip() for c in s.strip("|").split("|")]
                    if len(celler) != 2:
                        f.append(fel(path, f"ingrediensrad ska ha 2 celler, har {len(celler)}", nr))
                        continue
                    ingr = celler[1]
                    if not ingr:
                        f.append(fel(path, "tom ingredienscell", nr))
                    utan_parentes = re.sub(r"\([^)]*\)", "", ingr)
                    if re.search(r"\s\+\s|\s/\s|\seller\s", utan_parentes):
                        f.append(fel(path, f"flera varor på en rad: `{ingr}` — en vara per rad", nr))

        elif n == "Gör så här":
            nummer = [int(m.group(1)) for r in block if (m := re.match(r"^\s{0,1}(\d+)\. ", r))]
            if not nummer:
                f.append(fel(path, "Gör så här saknar numrerade steg", start + offset + 1))
            elif nummer != list(range(1, len(nummer) + 1)):
                f.append(fel(path, f"stegen ska numreras löpande 1…N, är {nummer}", start + offset + 1))
            for j, r in enumerate(block):
                if r.startswith("#") and not r.startswith("### "):
                    f.append(fel(path, "bara ### tillåts som delrubrik under Gör så här", start + j + offset + 1))

        elif n in ("Charlie-version", "Servering", "Att tänka på"):
            for j, r in enumerate(block):
                if r.startswith("#"):
                    f.append(fel(path, f"ingen rubrik tillåts under {n} — använd fet text i punkter", start + j + offset + 1))
            if n == "Charlie-version":
                inneh = [r for r in block if r.strip()]
                if inneh and not inneh[0].lstrip().startswith("- "):
                    f.append(fel(path, "Charlie-version ska vara en punktlista", start + offset + 1))

        elif n == "Logg":
            text = "\n".join(block)
            if not ("??? abstract" in text or "??? note" in text or re.search(r"\*Ing(en lagning|et bak) logga[dt] ännu", text)):
                f.append(fel(path, "Logg ska innehålla loggposter eller `*Ingen lagning loggad ännu.*`", start + offset + 1))

    return f


def main(argv: list[str]) -> int:
    filer = [Path(a) for a in argv] if argv else sorted(p for p in RECEPT.glob("*.md") if p.name != "index.md")
    alla: list[str] = []
    for p in filer:
        alla += kontrollera(p)
    if alla:
        print(f"{len(alla)} fel i receptkorten:")
        print("\n".join(alla))
        return 1
    print(f"OK: {len(filer)} kort följer layouten.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
