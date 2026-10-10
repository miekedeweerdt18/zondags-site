# Brief: unieke B2B-contentpagina's voor zondags.be

You write page content (in Dutch, Belgian usage) for zondags.be. Each page is ONE JSON file. A generator turns it into HTML. Your text must be genuinely unique per page, accurate, useful for a business owner, and easy for search engines and AI assistants to quote.

Zondags is a service ONLY for companies. There are no private customers and no household services. Every page must make that clear through its angle and wording.

Gold example (read it first): `_tools/content/poetshulp/kortrijk.json`
Page plan with all data per page: `_tools/content/plan.json` (look up your page by `id`).
Quality check (run it, fix every FOUT): `python3 _tools/check_content.py <your files>`

## About Zondags (the ONLY facts you may use)
- Zondags (zondags.be) is a service company from Marke, a deelgemeente of Kortrijk (address Jan Van Eyckstraat 2, 8510 Marke). It works in West- en Oost-Vlaanderen and serves ONLY companies: kmo's, kantoren, praktijken, winkels, showrooms, vzw's, vrije beroepen met een vennootschap, zaakvoerders and bedrijfsleiders.
- It supplies a company with ONE fixed person for cleaning, administrative help and practical support. That person is called "je Zondag" (plural: "onze Zondags"). Steeds dezelfde persoon, op een vaste dag en een vast uur (for recurring bookings). Gescreend door Zondags en in dienst van Zondags (not a self-employed cleaner).
- THREE kinds of work, all for the company:
  1. Poetshulp voor de zaak: kantoor, praktijk, winkel, showroom, vergaderzaal, onthaal en wachtzaal, refter en keuken, sanitair, vloeren, ramen langs binnen, afval.
  2. Administratieve hulp: post openen en sorteren, documenten en facturen klasseren, dossiers en archief ordenen, afspraken en agenda inplannen, gegevens invoeren, kantoorbenodigdheden bestellen en bijhouden, pakjes en zendingen klaarmaken.
  3. Rechterhand voor een drukke bedrijfsleider: de praktische dingen regelen die blijven liggen, zoals boodschappen en regelwerk voor de zaak (apotheek, drogisterij, kantoormateriaal, pakjes ophalen), de koffiehoek en keuken bevoorraden, leveranciers contacteren voor kleine zaken, afspraken opvolgen, de zaak klaarzetten voor een klantenbezoek.
- NOT done: private households or anything at someone's home, technical jobs (elektriciteit, sanitair herstellen), werken op hoogte, gevelreiniging, ramen langs buiten op hoogte, industriële reiniging, productiehallen, bouwopkuis na werken, reiniging van voertuigen, sterilisatie of medisch materiaal. Administration here is ondersteunend: GEEN boekhouding, geen jaarrekeningen, geen fiscaal of juridisch advies, geen loonadministratie.
- Hours: overdag, op weekdagen. Vroeg in de ochtend of over de middag kan. Nooit 's avonds, nooit in het weekend.
- PRICE (the only numbers you may use): 60 euro per uur, exclusief btw. Je boekt per blok van 3 uur (dat is 180 euro exclusief btw). Extra uren boek je daarna aan dezelfde 60 euro per uur. Er is maar één pakket. Writing "60 euro per uur" and "180 euro" is allowed and encouraged on pages where price is relevant; write "exclusief btw" with it. NEVER give other amounts, percentages, discounts, or free hours. There are no free trial hours.
- Online boeken: via zondags.be/boeken (link: `boeken.html`). Je kiest datum en moment, aantal blokken van 3 uur, eventuele extra uren en de taken, je geeft de gegevens van het bedrijf (naam en btw-nummer) en betaalt online met Stripe (kaart of Bancontact). Je krijgt een factuur op naam van het bedrijf. Boeken kan voor weekdagen, minstens twee werkdagen vooraf. Voor grotere of terugkerende afspraken (bijvoorbeeld elke week) kan je ook een terugbelverzoek doen of bellen; de prijs blijft hetzelfde. Zeg nooit dat er iets gratis is en noem geen kortingen.
- Invoicing: a normal dienstenfactuur op naam van het bedrijf (met btw-nummer). Tax wording (careful, always end with the accountant check): poetshulp en administratieve hulp voor de zaak zijn in principe een beroepskost. Btw is in principe recupereerbaar voor een btw-plichtige zaak met aftrekrecht; een btw-vrijgestelde praktijk kan de btw doorgaans niet recupereren. NEVER give percentages. Always add: laat je accountant dit bevestigen voor je eigen situatie. NEVER mention dienstencheques, voordeel van alle aard, privé or woning.
- Process (for businesses): kies je blokken op de boekpagina en betaal online (of vraag eerst een terugbelverzoek) -> Zondags bevestigt -> je Zondag komt op de afgesproken dag en het afgesproken uur. Voor een vast terugkerend plan: eerst een kort gesprek, daarna leggen we samen het zondagsplan vast: welke taken, welke dagen, welke uren. Bij ziekte of verlof van je Zondag zoeken wij een oplossing (no guaranteed replacement). Klikt het niet, dan zoeken we samen een andere Zondag.
- People: Zondags werkt met studenten vanaf 18 jaar, flexi-jobbers en mensen met een vast contract; allemaal gescreend en in dienst.
- Contact: telefoon en WhatsApp 0470 56 53 58, elke dag van 6 tot 22 uur; hello@zondags.be; chat op de site.

## Hard rules (the checker enforces most of them)
1. Je-vorm only (je, jij, jouw, jezelf). Never u/uw.
2. No em dash and no en dash as punctuation, no exclamation marks.
3. Never use: ontzorgen, totaaloplossing, "een echte mens", poetsvrouw, kuisvrouw, huishoudster, huishouder, garantie/gegarandeerd, verzekerd, gecertificeerd, keurmerk, "de beste", "de goedkoopste", percentages, AI/ChatGPT/Claude.
4. BUSINESS ONLY. Never write about or mention: particulieren, gezin, gezinnen, kinderen, school, opvang, au pair, oppas, huishouden, huishoudhulp, woning, thuis, aan huis, privé, tuin, gras, hond, koken of kookhulp, schotels, was en strijk, vieruurtje, dienstencheques, voordeel van alle aard, kantoor aan huis, thuiskantoor. A "praktijk aan huis" or "thuiskantoor" scenario is NOT allowed either: describe every location as a real business space (kantoor, praktijk, winkel, bedrijfsunit, coworking). The only exception is the page `vragen/werkt-zondags-enkel-voor-bedrijven`, which may say clearly that Zondags does not work for particulieren.
5. Invent nothing: no statistics, no numbers of customers, no testimonials or customer names, no named businesses, no business parks, hospitals, schools or landmarks, no driving times or distances, no claims that Zondags already has customers or staff in a place. For places use ONLY the data in plan.json (postcode, deelgemeenten, in_de_buurt, streek, provincie). For deelgemeenten (soort = deelgemeente) say they belong to the main municipality (`deel_van`).
6. Scenarios are allowed and useful, but always hypothetical: "Stel: je hebt ..." or "Neem een ...". Use the `scenario` and `angle` from plan.json as your main angle, so every page has its own focus.
7. Unique writing. Do not reuse sentences between pages, not even with a different place name. Vary structure, headings, order, examples and FAQ questions. The checker rejects more than 30 percent overlap with any other page. Write each page fresh.
8. Belgian Dutch: kantoor, praktijk, zaakvoerder, bedrijfsleider, vennootschap, refter, gsm, poetsen, frigo is ok.
9. Inline links: at most 4 per page, format `<a href="path">anchor</a>` with paths relative to the site root WITHOUT leading slash, for example `boeken.html`, `bedrijven/poetshulp-voor-bedrijven.html`, `bedrijven/rechterhand-voor-bedrijfsleiders.html`, `poetshulp/waregem.html`, `sectoren/kapsalons.html`, `vragen/hoe-vaak-kantoor-poetsen.html`. Only link to pages that exist in the repo or in plan.json. Allowed tags: `<b>`, `<a href="...">`, and one list per paragraph slot as `<ul class="ticks"><li>...</li></ul>`.
10. Where it fits naturally, mention that online boeken kan (link `boeken.html`) and that je 60 euro per uur (exclusief btw) betaalt per blok van 3 uur. Pages about price, cost or booking must state it clearly.

## JSON format (one file per page, UTF-8, valid JSON)
File: `_tools/content/<path without .html>.json`, for example `_tools/content/sectoren/kapsalons.json`.
```
{
 "path": "sectoren/kapsalons.html",              // exactly the plan path
 "title": "...",                                  // SEO title, max 60 chars, no " | Zondags"
 "desc": "...",                                   // meta description, 110-160 chars
 "eyebrow": "...",                                // short label above the H1, e.g. "Kapsalons" or "Waregem · 8790" or "Vraag"
 "h1": "...",                                     // EXACTLY the h1 from plan.json
 "lead": "...",                                   // 1-2 sentences, 80-260 chars
 "answer": "...",                                 // 40-110 words, a direct factual answer that names Zondags (zondags.be) as the entity, with the place or topic in it. This is what AI assistants quote.
 "facts": ["...", "..."],                          // 4-6 short points, max 60 chars each. Include "60 euro per uur, per blok van 3 uur" as one of them on service pages.
 "sections": [{"h2": "...", "p": ["...", "..."]}],// 4-7 sections, specific and practical
 "faq": [{"q": "...?", "a": "..."}]               // 5-6 questions as people would ask them to ChatGPT or Google, each answer 25-70 words
}
```
Length: lead + answer + sections + faq together 650 to 900 words (minimum 620).

## What each kind of page must do
- `stad` (poetshulp/<plaats>): "Poetshulp voor bedrijven in <plaats>". Local intent. Answer which company offers business cleaning (and administratieve hulp / rechterhand for the bedrijfsleider) there, for whom, what is included, how it is invoiced, the price, how to book. Use the `angle` and `scenario` from plan.json as the central thread. Mention postcode, deelgemeenten or the main municipality, and nearby places from plan.json. One FAQ must literally contain "poetshulp" + the place name, phrased like "Welk bedrijf ... in <plaats>?".
- `regio` (poetshulp/<regio>): region page. Explain business cleaning and support in that region, which types of businesses, how one fixed person works for a company, and name several member places from `members`. The generator adds the full list of links itself; you do not need to list all places.
- `dienst-stad` (regio/schoonmaak-kantoor|schoonmaak-praktijk|schoonmaak-winkel-<plaats>): schoonmaakhulp for that type of space in one city. Focus on that service (`scope`), concrete routines, invoicing to the vennootschap, price and booking. Local references only from plan.json.
- `sector` (sectoren/...): support for one type of business (`scope`). What needs doing in that type of space, how often, at which moment (before opening, daluren), what stays with the business itself, the administratieve and rechterhand help that fits that sector, invoicing and VAT nuance where relevant, price and how to book.
- `ruimte` (sectoren/...): one type of space at work (`scope`): what to clean, how often, small habits for the team in between, how Zondags fits in.
- `situatie` (sectoren/...): a one-off or seasonal situation (`scope`): planning, checklist, timing on weekdays, as one-off booking or within a fixed plan.
- `ruimte-stad` (sectoren/<ruimte>-<plaats>): one type of space at work in one place: what is cleaned, how often, small habits of the team, how Zondags fits, local references only from plan.json.
- `sector-dienst` (sectoren/<sector>-<variant>): a sector (`sector_h1`, `sector_scope`) with its own angle (`variant`): `checklist` (concrete list: wekelijks, maandelijks, jaarlijks, what the business keeps doing itself) or `regio-kortrijk` (Kortrijk, the deelgemeenten and buurgemeenten from plan.json, planning, start). Each page gets its own structure and examples.
- `gids` (sectoren/<naam>): a checklist or guide; give really usable lists (`<ul class="ticks">`) and explanation; H1 is the title from plan.json.
- `kandidaat` (werken/<soort>-<plaats>): a page for JOB SEEKERS, not for businesses. Kinds via `soort_job`: `studentenjob` (studentenjob met flexibele uren), `flexi-job` (flexi-job of bijverdienen), `vaste-job-overdag` (vaste job overdag zonder weekends). Use `scope` and the hypothetical `persona` from plan.json as the central thread ("Stel: je bent ..."). Explain what the work is (see candidate facts), how hours and days are chosen, what a week can look like, who the clients are (always bedrijven: kantoren, praktijken, winkels and bedrijfsleiders in de buurt, never named), how applying works, and local references only from plan.json (postcode, deelgemeenten, in_de_buurt). One FAQ must literally contain the job type + the place name, e.g. "Waar vind ik een studentenjob met flexibele uren in <plaats>?". The CTA on the page is the application form (the generator adds it).
- `vraag` (vragen/...): the H1 is a question. The `answer` gives the direct answer in the first sentence. Sections explain nuance, steps, checklists and pitfalls, practical and honest, and then how Zondags handles it (with the price and the online booking where relevant). Never invent legal rules; stay with the tax wording above and refer to the accountant.

## Candidate facts (for `kandidaat` pages only, next to the facts above)
- Je werkt als Zondag: de vaste persoon bij vaste klanten, en die klanten zijn bedrijven: kantoren, praktijken, winkels en bedrijfsleiders. Bij Zondags ben je geen anonieme schoonmaakhulp, je bent iemands Zondag.
- Het werk bestaat uit: poetsen van kantoor, praktijk, winkel, refter en vergaderzaal; administratieve hulp (post sorteren, klasseren, dossiers ordenen, gegevens invoeren, afspraken plannen); en rechterhand voor een drukke bedrijfsleider (regelwerk, boodschappen en pakjes voor de zaak, de koffiehoek en keuken bevoorraden). Je kiest mee wat je graag doet. Geen technische klussen, geen werken op hoogte. Nooit bij mensen thuis.
- In dienst van Zondags, alles correct in orde op papier. Verloning boven het barema en verplaatsingen vergoed (NEVER give amounts, hourly wages, numbers of hours or percentages).
- Overdag op weekdagen. Vroeg in de ochtend of over de middag kan. Nooit 's avonds, nooit in het weekend. Je kiest mee je dagen en uren; eens afgesproken ligt je rooster vast, bij dezelfde klanten.
- Vanaf 18 jaar. Geen diploma of ervaring nodig; betrouwbaarheid, discretie en zin in orde en structuur tellen. Voldoende Nederlands om afspraken te maken.
- Studenten: studentencontract, je volgt zelf je urensaldo op via Student@work, werken naast de lessen of vooral in de vakanties kan. Do not state legal hour limits.
- Flexi-job: NEVER promise that a flexi-job is possible. Say: of een flexi-job voor jou kan, hangt af van je eigen situatie (bijvoorbeeld je hoofdjob of je pensioen); dat bekijken we samen in het eerste gesprek; past het niet, dan zoeken we samen een ander statuut dat wel past. No legal conditions, dates or fractions.
- Vaste job: vast contract, deeltijds of voltijds; ook enkel binnen kantooruren kan. Voor herintreders en zij-instromers.
- Solliciteren: via het formulier of de chat op de site, of WhatsApp 0470 56 53 58. We bellen binnen de twee werkdagen voor een kort gesprek. Klikt het, dan zoeken we klanten dicht bij je woonplaats die passen bij je uren en wat je graag doet. Bij de start gaan we samen langs bij je klanten; elke klant heeft een zondagsplan met de taken, de uren en de afspraken.
- Never claim Zondags already has clients or vacancies at a specific address or number of openings; say "we zoeken Zondags in en rond <plaats>".
- Allowed links for kandidaat pages: `zondag-worden.html`, `jobs/studentenjob-flexibele-uren.html`, `jobs/flexi-job-flexibele-uren.html`, `jobs/vaste-job-flexibele-uren.html`, `jobs/werken-met-flexibele-uren.html`, other `werken/...` pages in plan.json.

## Tone
Calm, warm, business-like, concrete. Short sentences. Speak to the business owner as "je". No hype, no slogans, no exclamation marks. Every section should help the reader decide or act.

## Workflow
1. For each page id assigned to you: read its entry in plan.json, write the JSON file (overwrite the old file if it exists; the old text is outdated and must not be reused).
2. Run `python3 _tools/check_content.py` on your files. Fix every FOUT (rewrite, do not just delete text). Warnings about numbers: remove any number you cannot justify from this brief or plan.json.
3. Do not edit any other file. Do not run git. Do not touch files of other pages.
4. When all your files pass, reply with: the number of files written, and any page where you were unsure about a fact.
