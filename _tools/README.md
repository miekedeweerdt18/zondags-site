# zondags.be: hoe de contentpagina's gemaakt worden

De site is statische HTML. `main` is de bron, `gh-pages` is wat live staat (altijd dezelfde commit pushen naar beide). Na elke push naar `main` meldt `.github/workflows/indexnow.yml` de gewijzigde pagina's aan bij Bing en IndexNow.

Bouwen vanuit de root van de repo:

    PYTHONPATH=_tools python3 _tools/pseo.py

## Twee soorten pagina's

1. Oudere sjabloonpagina's (`beroepen/`, `diensten/`, `gids/`, `jobs/`, `regio/huishoudhulp-*`) uit `pseo_data.py`, plus de pijlerpagina's uit `geo_pillars.py`. Deze lijken sterk op elkaar (70 tot 90 procent dezelfde tekst). Breid ze niet verder uit met dezelfde sjablonen.
2. Unieke pagina's (sinds 4 oktober 2026): elke pagina heeft een eigen tekst in `_tools/content/<pad>.json`. Het plan met alle gegevens per pagina staat in `_tools/content/plan.json` (gemaakt door `_tools/content_plan.py`). Groepen:
   - `poetshulp/<gemeente>`: poetshulp voor bedrijven per gemeente (70) en per regio (10)
   - `regio/kookhulp-<stad>`, `regio/boodschappendienst-<stad>`, `regio/hulp-in-huis-<stad>` (12 steden)
   - `sectoren/`: per type bedrijf, per ruimte en per gelegenheid (40)
   - `vragen/`: vragen van bedrijven, de H1 is de vraag (44)
   - `regio/<dienst>-<gemeente>` uitgebreid naar alle 57 gemeenten (5 oktober 2026)
   - `werken/studentenjob-<gemeente>`, `werken/flexi-job-<gemeente>`, `werken/vaste-job-overdag-<gemeente>`: kandidatenpagina's (22 gemeenten), met sollicitatieformulier en JobPosting-schema
   Hubs: `poetshulp/`, `sectoren/`, `vragen/`, `werken/` (gemaakt door `pseo.py`).

## Nieuwe pagina's toevoegen (wekelijkse uitbreiding)

1. Voeg de nieuwe pagina's toe aan `_tools/content_plan.py` (nieuwe gemeenten met correcte postcode, deelgemeenten en buurgemeenten; of nieuwe sectoren of vragen) en draai `python3 _tools/content_plan.py`.
2. Schrijf per pagina een JSON-bestand volgens `_tools/content/BRIEF.md` (feiten, huisstijl, formaat). Gebruik het voorbeeld `_tools/content/poetshulp/kortrijk.json`.
3. Controleer: `python3 _tools/check_content.py` moet voor elke pagina OK geven (minstens 620 eigen woorden, maximaal 30 procent overlap met eender welke andere pagina, je-vorm, geen verboden woorden of tekens, geen prijzen, links bestaan).
4. Bouw met `pseo.py`, controleer dat er geen kapotte links zijn, commit en push naar `main` en `gh-pages`.

Volgende logische uitbreidingen: dezelfde drie diensten (kookhulp, boodschappendienst, hulp in huis) voor de overige gemeenten uit het plan; kandidatenpagina's per gemeente (studentenjob met flexibele uren, flexi-job of bijverdienen, vaste job overdag) als unieke pagina's; extra gemeenten in Oost-Vlaanderen; extra vragen van bedrijven.

## Leads

Alle formulieren posten naar FormSubmit (mail naar mieke@hummingbirds.be) en sturen dezelfde aanvraag ook naar de Make-webhook (WhatsApp-melding en leadsheet, route `zondags-chat` in het Make-scenario "Leads"). `assets/site.js` bewaart de herkomst van de bezoeker (utm-tags of verwijzende site) en voegt die als veld "Bron" aan elke aanvraag toe.
