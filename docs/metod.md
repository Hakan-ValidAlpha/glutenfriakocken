# Så funkar det

## Ett kort = ett levande dokument

Varje rätt har exakt **ett** kort i `docs/recept/`. Kortet innehåller receptet *som det ser ut just nu* — inte historiken. Historiken ligger i loggen längst ner och i git.

När en lagning visar att något ska ändras: **ändra huvudtexten** och skriv i loggen *vad* som ändrades och *varför*. Nästa gång du lagar rätten läser du bara huvudtexten.

## Frontmatter

Överst i varje kort:

```yaml
---
titel: Ankbröst med körsbärsgastrique
kategori: huvudrätt       # huvudrätt | bröd | bakverk | efterrätt | glass | tillbehör | sås | övrigt
protein: anka             # kyckling | fläsk | nöt | anka | lax | vegetariskt | null
glutenfri: true
tid_min: 75               # aktiv + passiv tid, vardagsmått
status: testad            # ny | testad | iterering | etablerad | skrotad
senast_lagad: 2026-09-28
betyg: 4.5                # 1–5, hushållets samlade omdöme senaste lagningen
charlie_ok: true          # true | false | null
nasta_ab: Såskonsistens   # en mening: nästa variabel att testa. null om inget planerat
tags: [helg, sås, syra]
---
```

Det är frontmattern som gör översikten, tabellen och taggsidan möjliga. Håll den uppdaterad — det är fem sekunder per lagning.

### Status betyder

| Status | När |
|---|---|
| `ny` | Kort skrivet, aldrig lagat |
| `testad` | Lagat minst en gång, inte färdigutvecklat |
| `iterering` | Aktiv A/B-serie pågår |
| `etablerad` | Vi är nöjda; lagas utan ändringar |
| `skrotad` | Fungerade inte för hushållet (behåll kortet — det är data) |

## Loggformat

En logg-post per lagning, nyaste längst ner, som hopfällbar sektion:

```markdown
??? abstract "Lagning 2 — 2026-10-12 · betyg 4.0"
    **Resultat:** …
    **Problem:** …
    **Ändrat i huvudtexten:** …
    **Nästa variabel:** …
    **Charlie:** …
```

En variabel per lagning. Två variabler samtidigt ger ingen information.

## Arbetsflöde med Claude

1. Be Claude hämta kortet från repot (eller klistra in det).
2. Logga lagningen tillsammans: resultat → ändringar → nästa variabel.
3. Claude skriver tillbaka kortet, uppdaterar frontmattern, committar.
4. Sajten byggs om automatiskt inom ett par minuter.

Git-historiken svarar på "vad ändrade vi mellan Lagning 1 och 3?" — `git log -p docs/recept/<kort>.md`.

## Regler

- Svenska. Svenska enheter (g, dl, msk, tsk, krm). Aldrig cups eller oz.
- Alkohol: adult-portion ok, Charlie får alltid alkoholfri version — skriv ut hur.
- Chili modereras för Charlie — skriv ut hur.
- Mjöl: Lailas blå mjölmix är standard om inget annat anges.
