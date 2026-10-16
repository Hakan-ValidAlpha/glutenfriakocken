# Glutenfria köket

Hushållets receptkort som markdown + en statisk sajt på GitHub Pages.

**Sajt:** https://hakan-validalpha.github.io/glutenfriakocken/

## Struktur

```
docs/recept/*.md          ett kort per rätt, frontmatter överst
docs/metod.md             formatregler och arbetsflöde
docs/utrustning.md        utrustning och skafferistandard
scripts/bygg_katalog.py   genererar översikt + tabell från frontmatter (körs i CI)
scripts/migrera.py        lägger frontmatter-stub på gamla kort
.github/workflows/        bygger och publicerar vid push till main
```

`docs/index.md` och `docs/recept/index.md` är genererade och gitignorerade — redigera inte dem.

## Lokalt

```
pip install -r requirements.txt
python3 scripts/bygg_katalog.py
mkdocs serve
```

## Migrera gamla kort

```
python3 scripts/migrera.py ~/Downloads/gamla-kort/
```
Fyller i titel/kategori/protein/glutenfri automatiskt, stryker gamla A/B-sektioner och lämnar TODO på resten.
