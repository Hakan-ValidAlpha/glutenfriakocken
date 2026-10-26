# Så funkar det

## Ett kort = ett levande dokument

Varje rätt har exakt **ett** kort i `docs/recept/`. Kortet innehåller receptet *som det ser ut just nu* — inte historiken. Historiken ligger i loggen längst ner och i git.

När en lagning visar att något ska ändras: **ändra huvudtexten** och skriv i loggen *vad* som ändrades och *varför*. Nästa gång du lagar rätten läser du bara huvudtexten. Kortet ska vara rent: inga testplaner, hypoteser eller alternativa metoder i receptet — bara den version vi tror på just nu.

## Frontmatter

Överst i varje kort:

```yaml
---
titel: Ankbröst med körsbärsgastrique
kategori: huvudrätt       # huvudrätt | bröd | bakverk | efterrätt | glass | tillbehör | sås | frukost | övrigt
protein: anka             # kyckling | fläsk | nöt | anka | fisk | vegetariskt | null
glutenfri: true
tid_min: 75               # aktiv + passiv tid samma dag; nattjäsning och kylning räknas inte med – ange dem i kortets huvud
status: testad            # ny | testad | etablerad | skrotad
senast_lagad: 2026-09-28  # null om aldrig lagat
betyg: 4.5                # 1–5, hushållets helhetsomdöme senaste lagningen. null om aldrig lagat
charlie_ok: true          # true | false | null
tags: [helg, sås, syra]   # 3–6 st, små bokstäver
---
```

Det är frontmattern som gör översikten, tabellen och taggsidan möjliga. Håll den uppdaterad — det är fem sekunder per lagning.

### Status betyder

| Status | När |
|---|---|
| `ny` | Kort skrivet, aldrig lagat |
| `testad` | Lagat minst en gång, inte färdigutvecklat |
| `etablerad` | Vi är nöjda; lagas utan ändringar |
| `skrotad` | Fungerade inte för hushållet (behåll kortet — det är data) |

### Betyg

Ett helhetsbetyg 1–5, satt inom en halvtimme efter maten:

| | |
|---|---|
| **1** | görs inte om |
| **3** | vardagsduglig |
| **5** | repertoarklass — inget skulle ändras |

`charlie_ok` sätts separat: `true` om Charlie åt med aptit eller bad om mer, `false` om hon inte åt, `null` om hon inte smakade. Fråga Charlie innan vuxenbetygen diskuteras högt.

**Betyg ≥ 4 två gånger i rad → `etablerad`.** Två lagningar som inte fungerar för hushållet → `skrotad`.

## Kortets struktur

Alla kort har exakt samma layout. Förebilden är [Glutenfri lasagne](recept/lasagne-glutenfri.md). Sektionerna kommer i denna ordning; `Tidsplan` och `Servering` får strykas när de inte behövs, de övriga är obligatoriska. `scripts/kontrollera_kort.py` kontrollerar strukturen maskinellt.

```markdown
# Rättens namn            ← identiskt med `titel` i frontmattern

**4 portioner · ca 90 min (varav 60 i ugn) · glutenfri**

En eller två meningar om rätten: vad det är, var den kommer ifrån, vad som är poängen.

## Ingredienser

**Köttfärssås**

| Mängd | Ingrediens |
|---:|---|
| 500 g | nötfärs (ett paket) |
| 1 st | gul lök, finhackad |
| | salt och svartpeppar |

**Ostsås**

| Mängd | Ingrediens |
|---:|---|
| 9 dl | mjölk |

## Tidsplan            ← valfri: bara för rätter med flera parallella moment eller lång väntan

| Tid | Moment |
|---|---|
| T−5 h | Ta fram köttet · ugn på |

## Gör så här

1. Numrerade steg som löper 1…N genom hela sektionen, även om den delas
   med ### Delrubriker (Dag 1 / Dag 2, T−75 min …). Numreringen börjar aldrig om.
2. Ange temperaturer, tider och sensoriska riktmärken ("tills gyllene",
   "54 °C i kärnan") — inte bara klocktid.

## Charlie-version

- Punktlista. Första punkten är antingen "Ingen avvikelse – …" eller den första avvikelsen:
  vad byts ut, när i processen delas satsen, mängder.

## Servering

- Punktlista: tillbehör, temperatur, vila, rester.

## Att tänka på

- **Fetstilt ledord** per punkt. Återkommande ledord när de är relevanta:
  **Glutenkoll**, **Utrustning**, **Skalning**, **Rester**, **Källa** (länkar).

## Logg

*Ingen lagning loggad ännu.*       ← eller loggposter, se nedan
```

### Ingredienstabellen är inköpslistan

Det här är den regel som oftast brutits, och den som gör mest nytta i butiken.

- **Alltid tabell**, aldrig punktlista. Rubrikraden är `| Mängd | Ingrediens |` och skiljeraden `|---:|---|` (mängden högerställs).
- **En vara per rad.** Aldrig `lingonsylt + flingsalt`, `smör eller olja`, `gurka, rödlök, senap`. Dela upp i rader. Ett alternativ till samma vara skrivs i parentes efter varan: `fläskfärs (eller blandfärs)`.
- **Mängd i vänsterkolumnen**, med enhet. Vikt i parentes när det hjälper: `4 msk (ca 40 g)`. Tom cell när mängden är "efter smak".
- **Förberedelse efter kommatecken** i högerkolumnen: `gul lök, finhackad`. Anmärkningar i parentes: `nötfärs (ett paket)`.
- **Samma vara på flera ställen i receptet:** en rad med totalmängden och fördelningen i parentes: `125 g | riven lagrad ost (100 g i smeten, 25 g ovanpå)`.
- **Gruppera med fet text** (`**Ostsås**`) följd av en egen tabell — inte med `###`, som skulle hamna i innehållsförteckningen. En rätt utan naturliga delar har en enda tabell utan gruppnamn.
- **Tillbehör som ingår i rätten** (sallad, vinägrett, pickles) har en egen grupp. Sådant som bara nämns som förslag under Servering behöver inte stå i tabellen.
- **Till Charlie:** ingredienser som bara används i hennes version får gruppen `**Till Charlie**`.
- **Skafferivaror står med** (salt, olja, smör) — det är lättare att stryka det man har hemma än att upptäcka i butiken att något saknades. Därför finns ingen separat inköpslista på kortet; tabellen är listan.

### Övriga formregler

- Metaraden under titeln: `**portioner · tid · glutenfri**` med `·` som avskiljare. Tiden är den som gäller samma dag; nattjäsning och kylning skrivs ut i ord (`+ 12–16 h i kyl`).
- Kontroller som gäller celiaki (märkning, korskontaminering) står under **Att tänka på** som punkt **Glutenkoll** — inte under Charlie-version, som bara beskriver avvikelser i hennes portion.
- Rubriknivåer: `##` för de sju sektionerna, `###` endast för faser under Gör så här. Inget annat.
- Loggen när inget är loggat: `*Ingen lagning loggad ännu.*` (bakning: `*Inget bak loggat ännu.*`), eventuellt följt av en mening om vad som ska noteras vid första gången.

## Loggformat

En logg-post per lagning, nyaste längst ner, som hopfällbar sektion:

```markdown
??? abstract "Lagning 2 — 2026-10-12 · betyg 4.0"
    **Resultat:** Hur det blev — smak, konsistens, tid.
    **Ändrat i huvudtexten:** Vad som ändrades i receptet och varför. "Inget" om inget.
    **Charlie:** Hur hon reagerade.
```

För bakning används "Bak N" i stället för "Lagning N". Loggen är en dagbok över vad som hände och vad vi lärde oss — inte en testplan. Idéer om vad som kan prövas nästa gång får stå som en kort mening under **Resultat**, men huvudtexten beskriver alltid bara den metod vi kör.

## Arbetsflöde med Claude

1. Be Claude hämta kortet från repot (eller klistra in det).
2. Logga lagningen tillsammans: resultat → ändringar → Charlie.
3. Claude skriver tillbaka kortet, uppdaterar frontmattern, kör `python3 scripts/kontrollera_kort.py` och committar.
4. Sajten byggs om automatiskt inom ett par minuter.

Nya kort skrivs från mallen i `.claude/skills/receptkort/mall.md` — Claude laddar den skillen innan den skriver eller skriver om ett kort.

Git-historiken svarar på "vad ändrade vi mellan Lagning 1 och 3?" — `git log -p docs/recept/<kort>.md`.

## Regler

- Svenska. Svenska enheter (g, dl, ml, msk, tsk, krm). Aldrig cups eller oz.
- Alkohol: vuxenportion ok, Charlie får alltid alkoholfri version — skriv ut hur.
- Chili modereras för Charlie — skriv ut hur.
- Mjöl: Lailas blå mjölmix är standard om inget annat anges.
- Utrustning och skafferi: se [Utrustning och skafferi](utrustning.md). Recept föreskriver inte teknik eller varor som inte finns där utan att flagga det.
