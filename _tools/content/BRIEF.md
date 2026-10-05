# Brief: unieke B2B-contentpagina's voor zondags.be

You write page content (in Dutch, Belgian usage) for zondags.be. Each page is ONE JSON file. A generator turns it into HTML. Your text must be genuinely unique per page, accurate, useful for a business owner, and easy for search engines and AI assistants (ChatGPT, Copilot, Perplexity, Gemini) to quote.

Gold example (read it first): `_tools/content/poetshulp/kortrijk.json`
Page plan with all data per page: `_tools/content/plan.json` (look up your page by `id`).
Quality check (run it, fix every FOUT): `python3 _tools/check_content.py <your files>`

## About Zondags (the ONLY facts you may use)
- Zondags (zondags.be) is a service company from Marke, a deelgemeente of Kortrijk (address Jan Van Eyckstraat 2, 8510 Marke). It works in West- en Oost-Vlaanderen.
- It supplies businesses, ondernemers (zaakvoerders, bedrijfsleiders), vrije beroepen, kantoren, praktijken and winkels with ONE fixed person for cleaning and household support. That person is called "je Zondag" (plural: "onze Zondags"). The agreed plan is the "zondagsplan".
- Steeds dezelfde persoon, op een vaste dag en een vast uur. Gescreend door Zondags en in dienst van Zondags (not a self-employed cleaner).
- Tasks: poetsen van kantoor, praktijk, winkel en woning; was en strijk; koken bij de klant thuis of gezonde schotels voor de week; boodschappen; regelwerk (apotheek, droogkuis, pakjes); kinderen ophalen van school en opvang na school; tuin, gras en terras (licht onderhoud); hond uitlaten; huis bijhouden tijdens de vakantie; ramen langs binnen.
- NOT done: technical jobs (elektriciteit, sanitair herstellen), werken op hoogte, gevelreiniging, ramen langs buiten op hoogte, industriële reiniging, productiehallen, bouwopkuis na werken, reiniging van voertuigen, sterilisatie of medisch materiaal.
- Hours: overdag, op weekdagen. Vroeg in de ochtend of over de middag kan. Nooit 's avonds, nooit in het weekend.
- Invoicing: a normal dienstenfactuur op naam van de vennootschap. Kantoor/praktijk and woning can be in one plan; the invoice splits beroepsmatig and privé.
- Tax wording (keep it careful, always end with the accountant check): een vennootschap kan geen dienstencheques kopen (enkel particulieren). Het onderhoud van beroepsruimtes is een beroepskost. Voor het privégedeelte (de woning van de bedrijfsleider) geldt een forfaitair voordeel van alle aard, op voorwaarde dat de prestaties regelmatig zijn en gebeuren via een onderneming met mensen in dienst. Btw op het beroepsmatige deel is in principe recupereerbaar voor een btw-plichtige zaak met aftrekrecht; op het privégedeelte in principe niet; een btw-vrijgestelde praktijk kan de btw doorgaans niet recupereren. NEVER give amounts, rates or percentages. Always add: laat je accountant dit bevestigen voor je eigen situatie.
- Price: op maat, na een kort gesprek. De eerste 2 uur zijn gratis, om kennis te maken. Maandelijks opzegbaar. Uren bijboeken of het plan aanpassen kan. Losse opdrachten (bijvoorbeeld een grote poetsbeurt of een verhuis) zijn ook mogelijk. NO prices, NO hourly rates, NO euro amounts anywhere.
- Process (for businesses): aanvraag via het formulier of de chat op de site -> binnen één werkdag belt iemand terug -> intake ter plaatse -> samen het zondagsplan opmaken -> je Zondag start. Bij ziekte of verlof van je Zondag zoeken wij een oplossing (no guaranteed replacement). Klikt het niet, dan zoeken we samen een andere Zondag.
- People: Zondags werkt met studenten vanaf 18 jaar, flexi-jobbers en mensen met een vast contract; allemaal gescreend en in dienst.
- Contact: telefoon en WhatsApp 0470 56 53 58, elke dag van 6 tot 22 uur; hello@zondags.be; chat op de site.

## Hard rules (the checker enforces most of them)
1. Je-vorm only (je, jij, jouw, jezelf). Never u/uw.
2. No em dash and no en dash as punctuation, no exclamation marks.
3. Never use: ontzorgen, totaaloplossing, "een echte mens", poetsvrouw, kuisvrouw, huishoudster, huishouder, garantie/gegarandeerd, verzekerd, gecertificeerd, keurmerk, "de beste", "de goedkoopste", prices, euro, percentages, AI/ChatGPT/Claude.
4. Invent nothing: no statistics, no numbers of customers, no testimonials or customer names, no named businesses, no business parks, hospitals, schools or landmarks, no driving times or distances, no claims that Zondags already has customers or staff in a place. For places use ONLY the data in plan.json (postcode, deelgemeenten, in_de_buurt, streek, provincie). For deelgemeenten (soort = deelgemeente) say they belong to the main municipality (`deel_van`).
5. Scenarios are allowed and useful, but always hypothetical: "Stel: je hebt ..." or "Neem een ...". Use the `scenario` and `angle` from plan.json as your main angle, so every page has its own focus.
6. Unique writing. Do not reuse sentences between pages, not even with a different place name. Vary structure, headings, order, examples and FAQ questions. The checker rejects more than 30 percent overlap with any other page. Write each page fresh.
7. Belgian Dutch: kantoor, praktijk, zaakvoerder, vennootschap, refter, strijk, gsm, poetsen, kuisen is ok in moderation, boodschappen, frigo is ok.
8. Inline links: at most 4 per page, format `<a href="path">anchor</a>` with paths relative to the site root WITHOUT leading slash, for example `bedrijven/poetshulp-voor-bedrijven.html`, `gids/huishoudhulp-via-vennootschap.html`, `regio/huishoudhulp-kortrijk.html`, `poetshulp/waregem.html`, `sectoren/kapsalons.html`, `vragen/hoe-vaak-kantoor-poetsen.html`. Only link to pages that exist in the repo or in plan.json. Allowed tags: `<b>`, `<a href="...">`, and one list per paragraph slot as `<ul class="ticks"><li>...</li></ul>`.

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
 "facts": ["...", "..."],                          // 4-6 short points, max 60 chars each
 "sections": [{"h2": "...", "p": ["...", "..."]}],// 4-7 sections, specific and practical
 "faq": [{"q": "...?", "a": "..."}]               // 5-6 questions as people would ask them to ChatGPT or Google, each answer 25-70 words
}
```
Length: lead + answer + sections + faq together 650 to 900 words (minimum 620).

## What each kind of page must do
- `stad` (poetshulp/<plaats>): "Poetshulp voor bedrijven in <plaats>". Local intent. Answer which company offers business cleaning there, for whom, what is included, how it is invoiced, how to start. Use the `angle` and `scenario` from plan.json as the central thread. Mention postcode, deelgemeenten or the main municipality, and nearby places from plan.json. One FAQ must literally contain "poetshulp" + the place name, phrased like "Welk bedrijf ... in <plaats>?".
- `regio` (poetshulp/<regio>): region page. Explain business cleaning in that region, which types of businesses, how one fixed person works across kantoor and woning, and name several member places from `members`. The generator adds the full list of links itself; you do not need to list all places.
- `dienst-stad` (regio/<dienst>-<plaats>): kookhulp, boodschappendienst or hulp in huis for ondernemers in one city. Focus on that service (`scope`), concrete weekly routines, combination with poetsen, invoicing to the vennootschap. Local references only from plan.json.
- `sector` (sectoren/...): cleaning support for one type of business (`scope`). What needs doing in that type of space, how often, at which moment (before opening, daluren), what stays with the business itself, combining with the zaakvoerder's woning, invoicing and VAT nuance where relevant, how to start.
- `ruimte` (sectoren/...): one type of space at work (`scope`): what to clean, how often, small habits for the team in between, how Zondags fits in.
- `situatie` (sectoren/...): a one-off or seasonal situation (`scope`): planning, checklist, timing on weekdays, as losse opdracht or within a fixed plan.
- `kandidaat` (werken/<soort>-<plaats>): a page for JOB SEEKERS, not for businesses. Kinds via `soort_job`: `studentenjob` (studentenjob met flexibele uren), `flexi-job` (flexi-job of bijverdienen), `vaste-job-overdag` (vaste job overdag zonder weekends). Use `scope` and the hypothetical `persona` from plan.json as the central thread ("Stel: je bent ..."). Explain what the work is, how hours and days are chosen, what a week can look like, who the clients are (ondernemers, praktijken, kantoren en gezinnen in de buurt, never named), how applying works, and local references only from plan.json (postcode, deelgemeenten, in_de_buurt). One FAQ must literally contain the job type + the place name, e.g. "Waar vind ik een studentenjob met flexibele uren in <plaats>?". Use the CANDIDATE FACTS below. The CTA on the page is the application form (the generator adds it).

## Candidate facts (for `kandidaat` pages only, next to the facts above)
- Je werkt als Zondag: de vaste persoon bij vaste klanten (ondernemers, vrije beroepen, kantoren, praktijken en hun gezinnen). Bij Zondags ben je geen anonieme schoonmaakhulp, je bent iemands Zondag.
- In dienst van Zondags, alles correct in orde op papier. Verloning boven het barema en verplaatsingen vergoed (NEVER give amounts, hourly wages, numbers of hours or percentages).
- Overdag op weekdagen. Vroeg in de ochtend of over de middag kan. Nooit 's avonds, nooit in het weekend. Je kiest mee je dagen en uren; eens afgesproken ligt je rooster vast, bij dezelfde klanten.
- Taken: huishouden en poetsen, was en strijk, koken, boodschappen, kinderen ophalen en opvangen na school, tuin en terras (licht), hond uitlaten, kantoor of praktijk onderhouden. Je kiest mee wat je graag doet. Geen technische klussen, geen werken op hoogte.
- Vanaf 18 jaar. Geen diploma of ervaring nodig; betrouwbaarheid, discretie en zorg voor andermans huis tellen. Voldoende Nederlands om afspraken te maken.
- Studenten: studentencontract, je volgt zelf je urensaldo op via Student@work, werken naast de lessen of vooral in de vakanties kan. Do not state legal hour limits.
- Flexi-job: NEVER promise that a flexi-job is possible. Say: of een flexi-job voor jou kan, hangt af van je eigen situatie (bijvoorbeeld je hoofdjob of je pensioen); dat bekijken we samen in het eerste gesprek; past het niet, dan zoeken we samen een ander statuut dat wel past. No legal conditions, dates or fractions.
- Vaste job: vast contract, deeltijds of voltijds; ook enkel binnen de schooluren kan. Voor herintreders, zij-instromers, ouders.
- Solliciteren: via het formulier of de chat op de site, of WhatsApp 0470 56 53 58. We bellen binnen de twee werkdagen voor een kort gesprek. Klikt het, dan zoeken we klanten dicht bij je woonplaats die passen bij je uren en wat je graag doet. Bij de start gaan we samen langs bij je klanten; elke klant heeft een zondagsplan met de taken, de uren en de afspraken.
- Never claim Zondags already has clients or vacancies at a specific address or number of openings; say "we zoeken Zondags in en rond <plaats>".
- Allowed links for kandidaat pages: `zondag-worden.html`, `jobs/studentenjob-flexibele-uren.html`, `jobs/flexi-job-flexibele-uren.html`, `jobs/vaste-job-flexibele-uren.html`, `jobs/werken-met-flexibele-uren.html`, `jobs/huishoudhulp-<plaats>.html` (only if the file exists), other `werken/...` pages in plan.json.
- `vraag` (vragen/...): the H1 is a question. The `answer` gives the direct answer in the first sentence. Sections explain nuance, steps, checklists and pitfalls, practical and honest, and then how Zondags handles it. Never invent legal rules; stay with the tax wording above and refer to the accountant.

## Tone
Calm, warm, business-like, concrete. Short sentences. Speak to the business owner as "je". No hype, no slogans, no exclamation marks. Every section should help the reader decide or act.

## Workflow
1. For each page id assigned to you: read its entry in plan.json, write the JSON file.
2. Run `python3 _tools/check_content.py` on your files. Fix every FOUT (rewrite, do not just delete text). Warnings about numbers: remove any number you cannot justify from this brief or plan.json.
3. Do not edit any other file. Do not run git. Do not touch files of other pages.
4. When all your files pass, reply with: the number of files written, and any page where you were unsure about a fact.
