#!/usr/bin/env python3
"""
Migrerar befintliga receptkort (markdown utan frontmatter) in i docs/recept/.

Användning:
    python3 scripts/migrera.py /sökväg/till/gamla/kort/*.md

För varje fil:
  - om den redan har frontmatter: kopieras oförändrad
  - annars: gissar titel (första H1), kategori och glutenfri-flagga från
    filnamn/innehåll, skriver en frontmatter-stub med status: ny och TODO-markeringar
    för det som inte går att härleda (tid, betyg, senast_lagad)
  - stryker sektionen "## Nästa A/B-test" (korten ska vara rena från testplaner)

Stubben är avsiktligt konservativ — fyll i resten för hand eller låt Claude göra det
kort för kort. Skriptet skriver aldrig över en fil som redan finns i docs/recept/.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECEPT = ROOT / "docs" / "recept"

KATEGORI_HINT = {
    "frukost": ["äggmuffins", "frukost"],
    "bröd": ["bröd", "baguette", "focaccia", "naan", "filmjölksbröd"],
    "bakverk": ["paj", "kaka", "chokladkaka", "oats", "pizza"],
    "glass": ["glass", "gelato"],
    "efterrätt": ["cheesecake", "dessert"],
    "sås": ["béarnaise", "bearnaise", "gastrique", "sås"],
    "tillbehör": ["chutney", "marinad", "sylt", "raita", "lassi", "pickl"],
}
PROTEIN_HINT = {
    "kyckling": ["kyckling"],
    "fläsk": ["fläsk", "karré", "revben", "frikadeller", "skinka"],
    "nöt": ["biff", "oxfilé", "entrecote"],
    "anka": ["ankbröst", "anka"],
    "lax": ["lax"],
}


def gissa(text: str, filnamn: str, tabell: dict[str, list[str]]) -> str | None:
    hay = (filnamn + " " + text[:2000]).lower()
    for nyckel, ord in tabell.items():
        if any(o in hay for o in ord):
            return nyckel
    return None


def slug(filnamn: str) -> str:
    s = filnamn.lower().replace("-receptkort", "")
    return re.sub(r"[^a-z0-9åäö\-]", "-", s).strip("-") + ".md" if not s.endswith(".md") else s.replace("-receptkort", "")


def stryk_ab(text: str) -> tuple[str, bool]:
    """Tar bort en '## Nästa A/B-test'-sektion (t.o.m. nästa rubrik på samma eller högre nivå)."""
    m = re.search(r"^##\s+Nästa A/B-test.*?(?=^#{1,2}\s|\Z)", text, re.M | re.S)
    if not m:
        return text, False
    return text[: m.start()] + text[m.end():], True


def migrera(src: Path) -> None:
    text = src.read_text(encoding="utf-8")
    text, struket = stryk_ab(text)
    if struket:
        print(f"  strök sektionen 'Nästa A/B-test' i {src.name}")
    dst = RECEPT / slug(src.name)
    if dst.exists():
        print(f"hoppar över (finns redan): {dst.name}")
        return
    if text.lstrip().startswith("---"):
        dst.write_text(text, encoding="utf-8")
        print(f"kopierad (hade frontmatter): {dst.name}")
        return

    h1 = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    titel = h1.group(1).strip() if h1 else src.stem.replace("-", " ").replace("receptkort", "").strip().capitalize()
    kategori = gissa(text, src.name, KATEGORI_HINT) or "huvudrätt"
    protein = gissa(text, src.name, PROTEIN_HINT)
    glutenfri = "glutenfri" in (src.name + text[:3000]).lower()

    # Grov statusgissning: finns en loggrad "Lagning 1" / "Bak 1" med datum → testad
    testad = re.search(r"(Lagning|Bak)\s+\d", text) is not None

    fm = ["---", f"titel: {titel}", f"kategori: {kategori}"]
    fm.append(f"protein: {protein}" if protein else "protein: null")
    fm += [
        f"glutenfri: {'true' if glutenfri else 'false'}",
        "tid_min: null        # TODO",
        f"status: {'testad' if testad else 'ny'}",
        "senast_lagad: null   # TODO  (ÅÅÅÅ-MM-DD)",
        "betyg: null          # TODO  (1–5)",
        "charlie_ok: null     # TODO",
        "tags: []",
        "---",
        "",
    ]
    dst.write_text("\n".join(fm) + text, encoding="utf-8")
    print(f"migrerad: {src.name} → {dst.name}  [{kategori}/{protein or '-'}/{'gf' if glutenfri else 'gluten'}]")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    RECEPT.mkdir(parents=True, exist_ok=True)
    for arg in argv[1:]:
        p = Path(arg)
        if p.is_dir():
            for f in sorted(p.glob("*.md")):
                migrera(f)
        elif p.suffix == ".md":
            migrera(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
