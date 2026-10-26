# Instruktioner för Claude i detta repo

Detta är hushållets receptdatabas och enda sanningskälla för receptkort. Läs `docs/metod.md` först — den definierar format, frontmatter, struktur och loggregler. Läs `docs/utrustning.md` innan du föreslår teknik eller ingredienser. Ladda skillen `receptkort` (`.claude/skills/receptkort/SKILL.md`) innan du skriver eller skriver om ett kort — den innehåller mallen och checklistan.

## Vid varje ändring av ett kort
1. Läs hela kortet innan du ändrar.
2. Ändra **huvudtexten** så att receptet speglar bästa kända version. Lägg aldrig "gör X istället" i loggen utan att också ändra huvudtexten.
3. Lägg en logg-post (`??? abstract "Lagning N — datum · betyg X"`) längst ner.
4. Uppdatera frontmatter: `status`, `senast_lagad`, `betyg`, `charlie_ok`.
5. Kör `python3 scripts/kontrollera_kort.py`, `python3 scripts/bygg_katalog.py` och `mkdocs build --strict` — alla tre ska gå igenom utan fel eller varningar. Kontrollskriptet fäller kort som avviker från layouten i `docs/metod.md`.
6. Committa med meddelande på formen `ankbröst: Lagning 2, såsen reducerad längre`.

## Nytt kort
- Filnamn: `docs/recept/<slug>.md`, bara a–z, 0–9 och bindestreck, utan "receptkort".
- Utgå från `.claude/skills/receptkort/mall.md`. `status: ny`, `senast_lagad: null`, `betyg: null`. H1 = `titel`.
- Svenska, svenska enheter.
- **Ingredienser alltid som tabell `| Mängd | Ingrediens |`, en vara per rad** — tabellen är inköpslistan. Ingen separat inköpslista. Grupper med fet text, inte `###`.
- Steg numreras löpande 1…N genom hela "Gör så här", även med `###`-faser.
- Rena kort: inga testplaner, A/B-upplägg eller alternativa metoder i receptet. Förslag på vad som kan prövas hör hemma i chatten, inte i kortet.

## Rör inte
- `docs/index.md`, `docs/recept/index.md` — genererade.
- Andras kort i samma commit som ditt, om det inte uttryckligen begärs.
