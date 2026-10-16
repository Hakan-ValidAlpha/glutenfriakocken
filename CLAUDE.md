# Instruktioner för Claude i detta repo

Detta är hushållets receptdatabas och enda sanningskälla för receptkort. Läs `docs/metod.md` först — den definierar format, frontmatter, struktur och loggregler. Läs `docs/utrustning.md` innan du föreslår teknik eller ingredienser.

## Vid varje ändring av ett kort
1. Läs hela kortet innan du ändrar.
2. Ändra **huvudtexten** så att receptet speglar bästa kända version. Lägg aldrig "gör X istället" i loggen utan att också ändra huvudtexten.
3. Lägg en logg-post (`??? abstract "Lagning N — datum · betyg X"`) längst ner.
4. Uppdatera frontmatter: `status`, `senast_lagad`, `betyg`, `charlie_ok`.
5. Kör `python3 scripts/bygg_katalog.py` och `mkdocs build --strict` — båda ska gå igenom utan varningar.
6. Committa med meddelande på formen `ankbröst: Lagning 2, såsen reducerad längre`.

## Nytt kort
- Filnamn: `docs/recept/<slug>.md`, bara a–z, 0–9 och bindestreck, utan "receptkort".
- Följ frontmatter-mallen och kortstrukturen i `docs/metod.md`. `status: ny`, `senast_lagad: null`, `betyg: null`.
- Svenska, svenska enheter. Ingredienstabell med mängd i vänsterkolumn.
- Rena kort: inga testplaner, A/B-upplägg eller alternativa metoder i receptet. Förslag på vad som kan prövas hör hemma i chatten, inte i kortet.

## Rör inte
- `docs/index.md`, `docs/recept/index.md` — genererade.
- Andras kort i samma commit som ditt, om det inte uttryckligen begärs.
