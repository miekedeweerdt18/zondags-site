# -*- coding: utf-8 -*-
"""B2B-focus (23/10/2026): de site spreekt zaakvoerders, managers en artsen/praktijken rechtstreeks aan.
- Blokken voor pseo.py: voordelen per doelgroep (gain_html), CTA in de paginakop (PHERO_CTA), relabels (b2b_html).
- Pass voor de handgeschreven pagina's (index, wat-we-doen, hoe-het-werkt, aanvraag = shell van pseo.py).
Primaire CTA overal: aanvraag.html. Links naar /boeken volgen de labels van Harper (d4a7136): 'Vraag aan', 'Meteen aanvragen'.
Idempotent. Volgorde:
    PYTHONPATH=_tools python3 _tools/premium_b2b.py && PYTHONPATH=_tools python3 _tools/premium_finalize.py && PYTHONPATH=_tools python3 _tools/pseo.py
NIET aangeraakt: boeken.html, assets/boeken.js, assets/chat.js, formulieren (velden, ids, hidden values), titels, metas, JSON-LD."""
import re, sys

ARR = ' <span class="arr">&rarr;</span>'
CTA_INFO = '<a class="btn btn--fill" href="aanvraag.html">Vraag vrijblijvend info' + ARR + '</a>'

# ---------- relabels die op elke pagina gelden (ook gegenereerde, via pseo.write) ----------
def b2b_html(page):
    page = re.sub(r'<p class="form__alt">Liever meteen starten\? <a href="([^"]*boeken\.html)">Boek online</a> per blok van 3 uur\.</p>',
                  r'<p class="form__alt">Liever alles in één keer doorgeven? <a href="\1">Laat je aanvraag achter</a>.</p>', page)
    page = re.sub(r'(<a href="[^"]*boeken\.html"[^>]*>)Boek online</a>', r'\1Vraag aan</a>', page)
    return page

# ---------- CTA in de paginakop van dienst- en doelgroeppagina's ----------
PHERO_CTA = ('<p class="phero__cta"><a class="btn btn--zon" href="aanvraag.html">Vraag vrijblijvend info' + ARR + '</a>'
             '<a href="#formulier">of laat hier je nummer achter</a></p>')

# ---------- voordelen per doelgroep ----------
ARTS_RX = re.compile(r'artsen|arts\b|schoonmaak-praktijk|wachtzaal|praktijken|apothe|patient|zorgverlener|praktijkpoets|'
                     r'poetsbeurt-praktijk|praktijk-proper|hygiene-afspraken-praktijk|btw-vrijgestelde-praktijk')
def audience(path, P=None):
    if P and P.get('doelgroep') in ('artsen', 'bedrijven'): return P['doelgroep']
    slug = path.split('/')[-1]
    if 'zonder-dienstencheques' in slug: return 'alle'
    return 'artsen' if ARTS_RX.search(slug) else 'bedrijven'

GAIN = {
 'bedrijven': dict(
   eyebrow='Voor zaakvoerders en managers',
   h2='Jij runt je zaak. <em class="s">Wij houden ze op orde.</em>',
   p='Je zaak moet proper en op orde zijn, maar jouw tijd hoort bij je klanten en je team. Daar is je Zondag voor.',
   items=[('Minder tijd kwijt aan poets en papier','Je Zondag poetst, houdt de post en de administratie bij en regelt de kleine dingen. Jij en je team houden tijd over voor jullie klanten.'),
          ('Eén vast gezicht in je zaak','Steeds dezelfde persoon, op een vaste dag en een vast uur. Ze kent je zaak en weet hoe jij het graag hebt.'),
          ('Niemand zelf aanwerven','Je Zondag is gescreend en in dienst van Zondags, geen zelfstandige.'),
          ('Gewoon op de factuur van je bedrijf','Een dienstenfactuur op naam van je bedrijf, zonder dienstencheques.')]),
 'artsen': dict(
   eyebrow='Voor artsen en praktijken',
   h2='Jij zorgt voor je patiënten. <em class="s">Wij voor je praktijk.</em>',
   p='Een frisse wachtzaal en een opgeruimd onthaal, zonder dat het van je consultatietijd afgaat.',
   items=[('Een frisse wachtzaal en een net onthaal','Wachtzaal, onthaal, sanitair en kantoor proper, buiten je consulturen.'),
          ('Hulp bij de niet-medische administratie','Post, klasseren, bestellingen en afspraken die blijven liggen.'),
          ('Duidelijk afgebakend','Je Zondag komt nooit aan medisch materiaal of aan dossiers.'),
          ('Eén vast gezicht voor je praktijk','Steeds dezelfde persoon, gescreend en in dienst van Zondags, met een factuur op naam van je praktijk.')]),
}
GAIN['alle'] = dict(GAIN['bedrijven'], eyebrow='Voor zaakvoerders, managers en artsen',
                    h2='Jij runt je zaak of je praktijk. <em class="s">Wij houden ze op orde.</em>')

def gain_html(aud='bedrijven'):
    g = GAIN[aud]
    lis = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in g['items'])
    return (f'<section class="gain wrap" aria-label="Wat je Zondag je oplevert">\n'
            f'  <div class="gain__head"><p class="eyebrow">{g["eyebrow"]}</p><h2>{g["h2"]}</h2><p>{g["p"]}</p>{CTA_INFO}</div>\n'
            f'  <ul class="gain__list">{lis}</ul>\n</section>\n')

# ---------- homepage ----------
AUD_NEW = '''<section class="aud aud--img wrap" aria-label="Voor wie">
    <a class="aud__c" href="bedrijven/"><span class="aud__img"><img src="assets/img/sectie-administratie-1600x1067.webp" alt="Notitieboek, enveloppen en een kop koffie op een houten bureau" loading="lazy" width="1600" height="1067"></span><span class="aud__txt"><p class="eyebrow">Voor zaakvoerders en managers</p><h3>Voor bedrijven <em class="s">en kantoren</em></h3><p>Een proper kantoor, de post op orde en iemand die de kleine dingen regelt. Zodat jij en je team kunnen doen waarvoor jullie er zijn.</p><span class="go">Wat je Zondag voor je zaak doet &rarr;</span></span></a>
    <a class="aud__c aud__c--art" href="bedrijven/voor-artsen.html"><span class="aud__img"><img src="assets/img/sectie-artsen-1200x1500.webp" alt="Witte doktersjas met stethoscoop aan een kapstok naast een donkere jas" loading="lazy" width="1200" height="1500"></span><span class="aud__txt"><p class="eyebrow">Voor huisartsen en specialisten</p><h3>Voor artsen <em class="s">en praktijken</em></h3><p>Een frisse wachtzaal, een opgeruimd onthaal en hulp bij de niet-medische administratie, buiten je consulturen.</p><span class="go">Wat je Zondag voor je praktijk doet &rarr;</span></span></a>
  </section>
'''
TRUST = '''<section class="trust wrap" id="zondag">
    <div>
      <p class="eyebrow">Wat is een Zondag?</p>
      <h2>Eén vaste persoon, <em class="s">elke week.</em></h2>
      <p class="def__entry">Een medewerker van Zondags die je inboekt per blok van 3 uur op je zaak of vennootschap. Steeds dezelfde persoon, op dezelfde dag, op hetzelfde uur.</p>
    </div>
    <ul class="trust__list" aria-label="Waarom zaakvoerders en artsen voor Zondags kiezen">
      <li><b>Steeds dezelfde Zondag</b><span>Op een vaste dag en een vast uur. Ze kent je zaak en hoe jij het wil.</span></li>
      <li><b>Gescreend en in dienst</b><span>Selectie en opleiding door ons. In dienst van Zondags, geen zelfstandige.</span></li>
      <li><b>Factuur op naam van je bedrijf</b><span>Een gewone dienstenfactuur. Geen dienstencheques.</span></li>
      <li><b>Op het ritme van je zaak</b><span>Overdag op weekdagen, ook vroeg in de ochtend of over de middag.</span></li>
      <li><b>Discreet in een praktijk</b><span>Nooit medisch materiaal of dossiers.</span></li>
      <li><b>Snel geregeld</b><span>Binnen één werkdag teruggebeld. Elke dag bereikbaar van 6 tot 22 uur.</span></li>
    </ul>
  </section>
'''

def _cut(s, start, end):
    """vervang het blok dat begint met start en eindigt met end (inclusief)"""
    i = s.find(start)
    if i < 0: return s, None
    j = s.find(end, i) + len(end)
    return s, (i, j)

def index(s):
    R = [
     ('<a class="btn btn--fill" href="#info">Vraag info', '<a class="btn btn--fill" href="aanvraag.html">Vraag info'),
     ('<p class="eyebrow hero__eyebrow">Voor bedrijven, praktijken en winkels in West- en Oost-Vlaanderen</p>',
      '<p class="eyebrow hero__eyebrow">Voor zaakvoerders, managers en artsen</p>'),
     ('<p class="hero__lead">Een Zondag is één vaste medewerker die je inboekt op je bedrijf. Zij poetst je kantoor, praktijk of winkel, houdt de administratie en de post bij, doet de boodschappen en regelt de kleine dingen.</p>',
      '<p class="hero__lead">Jij hebt je handen vol aan je klanten, je team of je patiënten. Een vaste Zondag houdt je kantoor, praktijk of winkel proper, houdt de post en de administratie bij en regelt de kleine dingen.</p>'),
     ('<ul class="hero__facts"><li>Steeds dezelfde persoon, gescreend en in dienst van Zondags</li><li>Per blok van 3 uur</li><li>Factuur op naam van je bedrijf</li></ul>',
      '<ul class="hero__facts"><li>Steeds dezelfde persoon, gescreend en in dienst van Zondags</li><li>Factuur op naam van je bedrijf of praktijk</li><li>Binnen één werkdag teruggebeld</li></ul>'),
     ('<b>Wat kost het?<small>Eén pakket, per blok van 3 uur.</small></b>', '<b>Ons pakket<small>Eén pakket voor alle taken, per blok van 3 uur.</small></b>'),
     # info-stap (regel 82): Harper's tekst + </span>-herstel uit 36fe506 blijft ongewijzigd
     ('<img src="assets/img/hero-desktop-2048x1152.webp" alt="Lichte ruimte met zacht ochtendlicht" loading="lazy" width="2048" height="1152">',
      '<img src="assets/img/sectie-praktijk-2048x1152.webp" alt="Rustige wachtzaal met twee stoelen en een houten onthaalbalie" loading="lazy" width="2048" height="1152">'),
     ('<p>Eén vaste Zondag, op een vaste dag. Wanneer jij of je team binnenkomt, is het werk al gedaan.</p>',
      '<p>Eén vaste Zondag, op een vaste dag. Wanneer jij, je team of je eerste patiënt binnenkomt, is het werk al gedaan.</p>'),
     ('<p>Laat je naam, je bedrijf en je gsm achter. We bellen je binnen één werkdag terug. Weet je al wat je nodig hebt? Vul dan meteen het aanvraagformulier in.</p><div class="band__ctas"><a class="btn btn--fill" href="#info">Vraag vrijblijvend info <span class="arr">&rarr;</span></a><a class="btn" href="boeken.html">Vraag meteen aan</a></div>',
      '<p>Vertel ons wat je zaak of je praktijk nodig heeft. We bellen je binnen één werkdag terug, vrijblijvend.</p><div class="band__ctas"><a class="btn btn--fill" href="aanvraag.html">Vraag vrijblijvend info <span class="arr">&rarr;</span></a><a class="btn" href="boeken.html">Meteen aanvragen</a></div>'),
    ]
    s = apply(s, R, 'index.html')
    s = s.replace('class="mmenu__cta" href="#info"', 'class="mmenu__cta" href="aanvraag.html"')
    s = replace_block(s, '<section class="aud wrap" aria-label="Voor wie">', '</section>\n', AUD_NEW, 'aud--img')
    s = replace_block(s, '<section class="def wrap" id="zondag">', '</section>\n', TRUST, 'class="trust wrap"')
    s = replace_block(s, '<section class="jobs-strip wrap"', '</section>\n', '', None)
    return s

def wat_we_doen(s):
    R = [
     ('<p class="eyebrow">Wat we doen</p>', '<p class="eyebrow">Voor zaakvoerders, managers en artsen</p>'),
     ('<p>Een Zondag werkt voor je bedrijf: poetsen, administratie, boodschappen en regelwerk. Eén vaste persoon voor alles wat je als bedrijfsleider liever niet zelf doet.</p>',
      '<p>Een Zondag werkt voor je bedrijf of je praktijk: poetsen, administratie, boodschappen en regelwerk. Eén vaste persoon voor alles wat jij en je team liever niet zelf doen, zodat jullie tijd hebben voor klanten en patiënten.</p>'),
     ('<a class="btn btn--zon" href="boeken.html" style="align-self:flex-start">Vraag aan <span class="arr">&rarr;</span></a>',
      '<a class="btn btn--zon" href="aanvraag.html" style="align-self:flex-start">Vraag vrijblijvend info <span class="arr">&rarr;</span></a>'),
    ]
    s = apply(s, R, 'wat-we-doen.html')
    s = band(s, 'wat-we-doen.html')
    if 'class="gain wrap"' not in s:
        s = s.replace('<section class="band">', gain_html('alle') + '\n  <section class="band">', 1)
    return s

BAND_OLD = '<div><p>Vraag je Zondag aan via het aanvraagformulier, dan nemen we binnen één werkdag contact op. Liever eerst praten? Dan bellen we je binnen één werkdag terug.</p><a class="btn btn--fill" href="boeken.html">Vraag aan <span class="arr">&rarr;</span></a></div>'
BAND_NEW = '<div><p>Vertel ons wat je zaak of je praktijk nodig heeft. We bellen je binnen één werkdag terug, vrijblijvend.</p><a class="btn btn--fill" href="aanvraag.html">Vraag vrijblijvend info <span class="arr">&rarr;</span></a></div>'
def band(s, f): return apply(s, [(BAND_OLD, BAND_NEW)], f)

def hoe_het_werkt(s):
    R = [
     ('<p>Je vraagt je Zondag aan via het aanvraagformulier op zondags.be/boeken, en binnen één werkdag nemen we contact op om de rest af te spreken. Voor een vast ritme bespreken we daarna een plan met je.</p>',
      '<p>Je vraagt vrijblijvend info, we bellen je binnen één werkdag terug en je Zondag start op de afgesproken dag. Voor je zaak of je praktijk, met een vast ritme.</p>'),
     ('<h3>Je vraagt aan</h3><p>Via het aanvraagformulier geef je door wat er moet gebeuren, in welke gemeente en wanneer je wil starten.</p>',
      '<h3>Je vraagt info aan</h3><p>Vier velden, vrijblijvend: je naam, je bedrijf of praktijk, je gsm en waarvoor je hulp zoekt.</p>'),
     ('<h3>We nemen contact op</h3><p>Binnen één werkdag spreken we samen taken, dagen en uren af. Je krijgt een factuur op naam van je bedrijf.</p>',
      '<h3>We bellen je terug</h3><p>Binnen één werkdag. We bespreken wat er moet gebeuren, de dag en het uur. Je krijgt een factuur op naam van je bedrijf.</p>'),
     ('<a class="btn" href="boeken.html" style="justify-self:start;background:var(--geel);color:var(--ink);border-color:var(--geel)">Vraag aan <span class="arr">&rarr;</span></a>',
      '<a class="btn" href="aanvraag.html" style="justify-self:start;background:var(--geel);color:var(--ink);border-color:var(--geel)">Vraag vrijblijvend info <span class="arr">&rarr;</span></a>'),
    ]
    return band(apply(s, R, 'hoe-het-werkt.html'), 'hoe-het-werkt.html')

def aanvraag(s):
    R = [
     ('<p class="eyebrow">Vrijblijvend info</p><h1', '<p class="eyebrow">Voor bedrijven, kantoren en praktijken</p><h1'),
    ]
    s = apply(s, R, 'aanvraag.html')
    s = s.replace('<a class="btn btn--fill" href="#infoform">Vraag info', '<a class="btn btn--fill" href="aanvraag.html">Vraag info')
    return s

# ---------- helpers ----------
def apply(s, R, f):
    for a, b in R:
        if a in s: s = s.replace(a, b)
        elif b not in s: print(f"{f}: tekst niet gevonden: {a[:160]}", file=sys.stderr); sys.exit(1)
    return s

def replace_block(s, start, end, new, marker):
    if marker and marker in s: return s
    i = s.find(start)
    if i < 0:
        if marker is None: return s          # al weg
        print('blok niet gevonden:', start, file=sys.stderr); sys.exit(1)
    j = s.find(end, i) + len(end)
    line_start = s.rfind('\n', 0, i) + 1
    if s[line_start:i].strip() == '': i = line_start  # inspringing mee vervangen
    return s[:i] + (('  ' + new) if new and not new.startswith(' ') else new) + s[j:]

PAGES = {'index.html': index, 'wat-we-doen.html': wat_we_doen, 'hoe-het-werkt.html': hoe_het_werkt, 'aanvraag.html': aanvraag}
ROOT_REST = ['zondag-worden.html', 'bedankt.html', 'bedankt-kandidaat.html', '404.html']

def main():
    n = 0
    for f in list(PAGES) + ROOT_REST:
        s = open(f).read()
        new = b2b_html(PAGES[f](s) if f in PAGES else s)
        if new != s: open(f, 'w').write(new); n += 1; print('aangepast:', f)
    print('klaar,', n, 'bestanden')

if __name__ == '__main__':
    main()
