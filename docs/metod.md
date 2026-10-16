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

Sektioner i denna ordning. Sektioner som inte är relevanta stryks, men ordningen behålls.

```markdown
# Rättens namn

**N portioner · ca X min · glutenfri**

En eller två meningar om rätten.

## Ingredienser
| Mängd | Ingrediens |
|---:|---|
| 2 st | ankbröst (ca 350 g styck) |

(Gruppera med underrubriker vid behov: Deg / Fyllning / Sås.)

## Gör så här
1. Numrerade steg. Ange temperaturer, tider och sensoriska riktmärken
   ("tills gyllene", "54 °C i kärnan") — inte bara klocktid.

## Charlie-version
Konkreta avvikelser: vad byts ut, när i processen delas satsen, mängder.

## Servering
Tillbehör, temperatur, vila.

## Att tänka på
Kända fallgropar, skalning, inköpskällor för ovanliga ingredienser, länkar.

## Logg
(se nedan)
```

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
3. Claude skriver tillbaka kortet, uppdaterar frontmattern, committar.
4. Sajten byggs om automatiskt inom ett par minuter.

Git-historiken svarar på "vad ändrade vi mellan Lagning 1 och 3?" — `git log -p docs/recept/<kort>.md`.

## Regler

- Svenska. Svenska enheter (g, dl, ml, msk, tsk, krm). Aldrig cups eller oz.
- Alkohol: vuxenportion ok, Charlie får alltid alkoholfri version — skriv ut hur.
- Chili modereras för Charlie — skriv ut hur.
- Mjöl: Lailas blå mjölmix är standard om inget annat anges.
- Utrustning och skafferi: se [Utrustning och skafferi](utrustning.md). Recept föreskriver inte teknik eller varor som inte finns där utan att flagga det.
