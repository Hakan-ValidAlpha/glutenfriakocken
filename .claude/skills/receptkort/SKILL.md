---
name: receptkort
description: Skriv eller skriv om ett receptkort i docs/recept/ enligt hushållets fasta layout (ingredienstabell en vara per rad, löpande steg, fast sektionsordning). Ladda innan du skapar, ändrar eller loggar ett kort i glutenfriakocken.
---

# Receptkort – så skrivs de

Layouten är definierad i `docs/metod.md` (avsnitt *Kortets struktur*) och kontrolleras av `scripts/kontrollera_kort.py`. Den här skillen är arbetsgången; metod.md är regelboken. Förebild: `docs/recept/lasagne-glutenfri.md`.

## Arbetsgång

1. **Läs** `docs/metod.md`, `docs/utrustning.md` och – vid ändring – hela det befintliga kortet. Sök efter befintligt kort innan du skapar ett nytt (`ls docs/recept/`).
2. **Utgå från mallen** `mall.md` i den här mappen. Kopiera den, byt ut allt i hakparenteser, stryk `## Tidsplan` och `## Servering` om de inte behövs. Inga andra sektioner får läggas till eller tas bort.
3. **Ingredienserna först**, som inköpslista: en tabell per grupp, rubrikrad `| Mängd | Ingrediens |`, skiljerad `|---:|---|`, **en vara per rad**. Skriv aldrig `A + B`, `A eller B`, `A, B och C` i en ingredienscell – dela upp i rader. Alternativ till samma vara i parentes: `fläskfärs (eller blandfärs)`. Förberedelse efter kommatecken: `gul lök, finhackad`. Samma vara på flera ställen: en rad med totalen och fördelningen i parentes. Skafferivaror (salt, olja, smör) står med. Ingen separat inköpslista någonstans på kortet.
4. **Stegen** numreras 1…N genom hela *Gör så här*. Faser markeras med `### Rubrik` eller fetstilta tidsmarkörer (`**T−30 min**`), men numreringen fortsätter. Varje steg har temperatur, tid och ett sensoriskt riktmärke där det går.
5. **Charlie-version** är en punktlista och beskriver bara avvikelser i hennes portion (alkohol, chili, byten). Första punkten är `- Ingen avvikelse – …` när inget skiljer. Glutenkontroller hör inte hit.
6. **Att tänka på** är punkter med fetstilt ledord. Använd de återkommande ledorden när de är relevanta: **Glutenkoll** (märkning, korskontaminering), **Utrustning** (flagga allt som saknas i `docs/utrustning.md`), **Skalning**, **Rester**, **Källa**. Inga testplaner, hypoteser eller alternativa metoder – de hör hemma i chatten.
7. **Logg**: `*Ingen lagning loggad ännu.*` (bak: `*Inget bak loggat ännu.*`) tills första lagningen; därefter `??? abstract "Lagning N — datum · betyg X"`-poster, nyaste längst ner.
8. **Frontmatter**: alla fält, `tags` 3–6 st små bokstäver, H1 identisk med `titel`.
9. **Kör** `python3 scripts/kontrollera_kort.py`, `python3 scripts/bygg_katalog.py` och `mkdocs build --strict`. Alla tre ska gå igenom. Rätta tills de gör det – flytta inte regeln.
10. **Committa** ett kort per commit: `<slug kort>: <vad>`.

## Efter en lagning

Fråga efter helhetsbetyg (1–5) och Charlies reaktion om det saknas. Ändra huvudtexten först, lägg sedan loggposten som beskriver vad som ändrades och varför. Uppdatera `status`, `senast_lagad`, `betyg`, `charlie_ok`. Betyg ≥ 4 två gånger i rad → `etablerad`.

## Vanliga misstag att stoppa

- Punktlista under Ingredienser.
- `###` som gruppnamn i ingredienserna (hamnar i innehållsförteckningen).
- Numreringen börjar om efter en delrubrik.
- Egen sektion (`## Tidsplan`-liknande) före Ingredienser, eller en gluten-sektion i stället för punkten **Glutenkoll**.
- Vinägrett eller sallad som bara beskrivs i Servering fast den ska köpas – lägg ingredienserna i en egen grupp i tabellen.
- Svenska enheter alltid: g, kg, ml, dl, tsk, msk, krm.
