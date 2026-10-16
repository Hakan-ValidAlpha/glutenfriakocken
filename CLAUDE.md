# Instruktioner för Claude i detta repo

Detta är hushållets receptdatabas. Läs `docs/metod.md` först — den definierar format, frontmatter och loggregler.

## Vid varje ändring av ett kort
1. Läs hela kortet innan du ändrar.
2. Ändra **huvudtexten** så att receptet speglar bästa kända version. Lägg aldrig "gör X istället" i loggen utan att också ändra huvudtexten.
3. Lägg en logg-post (`??? abstract "Lagning N — datum · betyg X"`) längst ner.
4. Uppdatera frontmatter: `status`, `senast_lagad`, `betyg`, `charlie_ok`, `nasta_ab`.
5. Kör `python3 scripts/bygg_katalog.py` och `mkdocs build --strict` — båda ska gå igenom.
6. Committa med meddelande på formen `ankbröst: Lagning 2, såskonsistens → reducera längre`.

## Nytt kort
- Filnamn: `docs/recept/<slug>.md`, bara a–z, 0–9 och bindestreck, utan "receptkort".
- Kopiera frontmatter-mallen från `docs/metod.md`. `status: ny`, `senast_lagad: null`.
- Svenska, svenska enheter. Ingrediensetabell med mängd i vänsterkolumn.

## Rör inte
- `docs/index.md`, `docs/recept/index.md` — genererade.
- Andras kort i samma commit som ditt, om det inte uttryckligen begärs.
