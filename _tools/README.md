# zondags.be: hoe de contentpagina's gemaakt worden

De site is statische HTML. `main` is de bron, `gh-pages` is wat live staat (altijd dezelfde commit pushen naar beide). Na elke push naar `main` meldt `.github/workflows/indexnow.yml` de gewijzigde pagina's aan bij Bing en IndexNow.

Bouwen vanuit de root van de repo:

    PYTHONPATH=_tools python3 _tools/pseo.py

## Wat de site is

Zondags is een dienst voor bedrijven (geen particulieren): poetshulp voor kantoor, praktijk of winkel, administratie, boodschappen en regelwerk, en een rechterhand voor drukbezette bedrijfsleiders. Eén pakket: 60 euro per uur excl. btw, geboekt per blok van 3 uur, extra uren per uur (zelfde prijs). Boeken en betalen via `boeken.html` (Stripe Payment Links, zie `assets/boeken.js`). Geen gratis uren, geen kortingen. Daarnaast werk met flexibele uren voor studenten, flexi-jobbers en vaste medewerkers.

## Pagina's

1. Pijlerpagina's uit `geo_pillars.py` (`bedrijven/`, `jobs/*-flexibele-uren`, `over-zondags`).
2. Unieke pagina's: elke pagina heeft een eigen tekst in `_tools/content/<pad>.json`. Het plan met de gegevens per pagina staat in `_tools/content/plan.json` (gemaakt door `_tools/content_plan.py`; draai dat script niet opnieuw zonder het plan te controleren, want het overschrijft plan.json). Groepen:
   - `poetshulp/<gemeente>` (94) en per regio (10)
   - `regio/schoonmaak-{kantoor,praktijk,winkel}-<gemeente>` (134)
   - `sectoren/`: per type bedrijf, per ruimte, per gelegenheid, checklists (154)
   - `vragen/`: vragen van bedrijven, de H1 is de vraag (80)
   - `werken/{studentenjob,flexi-job,vaste-job-overdag}-<gemeente>`: kandidatenpagina's (171) met sollicitatieformulier en JobPosting-schema
   Hubs: `poetshulp/`, `sectoren/`, `vragen/`, `werken/` (gemaakt door `pseo.py`).
3. Redirects: `_tools/redirects.json` (oud pad naar nieuw pad). `pseo.py` schrijft voor elk oud pad een stub met meta refresh, canonical en noindex. Stubs staan niet in de sitemap.

## Nieuwe pagina's toevoegen

1. Voeg ze toe aan `_tools/content_plan.py` en draai `python3 _tools/content_plan.py` (controleer daarna de diff van plan.json).
2. Schrijf per pagina een JSON-bestand volgens `_tools/content/BRIEF.md`. Voorbeeld: `_tools/content/poetshulp/kortrijk.json`.
3. Controleer: `python3 _tools/check_content.py` moet voor elke pagina OK geven.
4. Bouw met `pseo.py`, controleer links, commit en push naar `main` en `gh-pages`.

## Leads

Alle formulieren posten naar FormSubmit (mail naar mieke@hummingbirds.be) en sturen dezelfde aanvraag ook naar de Make-webhook (WhatsApp-melding en leadsheet, route `zondags-chat` in het Make-scenario "Leads"). `assets/site.js` bewaart de herkomst van de bezoeker (utm-tags of verwijzende site) en voegt die als veld "Bron" aan elke aanvraag toe.
