"""Premium uitrol (23/10/2026): gedeelde helpers voor pseo.py en de eenmalige migratie.

- deprice_html(): haalt prijzen en uurtarieven uit de ZICHTBARE tekst (niet uit title, meta of JSON-LD).
- PBAND: welk premium beeld een contentpagina krijgt, per map.
"""
import re

E = r'(?:exclusief|excl\.?) ?btw'
EUR = r'(?:€ ?\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)? ?(?:euro|€|EUR)\b)'
# wat check.py (zinv.PRICE_RE) als prijs ziet
PRICE = re.compile(r'(€\s?\d[\d.,]*|\d[\d.,]*\s?(?:€|euro\b|EUR\b)|\beuro per uur\b|\bper uur excl|\bexcl\.? btw\b)', re.I)

# 1. bijzinnen met een bedrag in een verder bruikbare zin (volgorde telt)
INLINE = [(re.compile(p), r) for p, r in [
    (r'\s*\([^()]*' + EUR + r'[^()]*\)', ''),
    (r'^(?:Tarief|Uurprijs|Prijs): (?=' + EUR + ')', ''),
    (r'^Excl\. btw, op naam', 'Op naam'),
    (r'^Extra uren: ' + EUR + r' per uur', 'Extra uren: per uur'),
    (r'^Extra uren aan ' + EUR + r' per uur$', 'Extra uren per uur erbij'),
    (r'\b(boek je|boekt) extra uren aan hetzelfde (?:uur)?tarief', r'\1 extra uren erbij'),
    (r'(Eén pakket), één (?:prijs|tarief|uurprijs): ' + EUR + r' per uur(?: ' + E + r')?(?:,? |(?=\.))', r'\1, '),
    (r',? aan ' + EUR + r' per uur(?: ' + E + r')?,? per blok van 3 uur', ', per blok van 3 uur'),
    (r'(Eén|één) (?:pakket|tarief)(?: aan|:)? ' + EUR + r' per uur(?: ' + E + r')?(?=[,.])', r'\1 pakket'),
    (r'(Je|je) betaalt ' + EUR + r' per uur(?: ' + E + r')?,? (?:geboekt |telkens )?(per blok|in blokken) van 3 uur', r'\1 boekt \2 van 3 uur'),
    (r'(Het|het|De|de) (?:uur)?(?:tarief|prijs) (?:is|blijft) ' + EUR + r' per uur(?: ' + E + r')?,? (?:geboekt )?(per blok|in blokken) van 3 uur', lambda m: ('J' if m.group(1)[0].isupper() else 'j') + 'e boekt ' + m.group(2) + ' van 3 uur'),
    (r'^' + EUR + r' per uur(?: ' + E + r')?,? (?:geboekt |telkens )?(?:per blok|in blokken) van 3 uur(?: geboekt)?', 'Per blok van 3 uur'),
    (r'\b' + EUR + r' per uur(?: ' + E + r')?,? (?:geboekt |telkens )?per blok van 3 uur', 'per blok van 3 uur'),
    (r',? (?:aan|tegen|voor) (?:een (?:vast )?(?:uur)?tarief van )?' + EUR + r'(?: per uur)?(?: ' + E + r')?(?: per (?:blok|uur))?', ''),
    (r', (?:dus|wat neerkomt op|dat is|samen|goed voor) ' + EUR + r'(?: per (?:uur|blok))?(?: ' + E + r')?(?: per (?:blok|uur))?', ''),
    (r',? met extra uren aan (?:hetzelfde (?:uur)?tarief|dezelfde prijs)', ', extra uren kan je erbij boeken'),
    (r',? (?:en )?extra uren (?:boek je aan (?:hetzelfde (?:uur)?tarief|dezelfde prijs)|kosten hetzelfde(?: per uur)?|zijn evenveel per uur|aan hetzelfde (?:uur)?tarief)', ', extra uren kan je erbij boeken'),
]]
# 2. zinnen over extra uren aan hetzelfde tarief: zonder bedrag zeggen ze niets meer
EXTRA = re.compile(r'^(?:En )?[Ee]xtra uren\b[^.]*(?:tarief|hetzelfde|dezelfde prijs|evenveel)[^.]*\.?$')
EXTRA_NEW = 'Extra uren kan je erbij boeken.'
SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-ZÉÈ0-9€])')

# Knopen die volledig over de prijs gingen: vaste vervanging zodat er geen lege elementen overblijven
FIX = {
    '60 euro per uur excl. btw': 'Per blok van 3 uur',
    '60 euro per uur exclusief btw': 'Eén pakket voor alle taken',
    '60 euro per uur, exclusief btw': 'Eén pakket voor alle taken',
    'Uurprijs: 60 euro exclusief btw': 'Eén pakket voor alle taken',
    'Blok van 3 uur is 180 euro excl. btw': 'Je boekt per blok van 3 uur',
    '60 euro per uur.': 'Eén pakket.',
    'Prijs blijft 60 euro per uur': 'Zelfde pakket, per blok van 3 uur',
    'Het tarief van 60 euro per uur exclusief btw': 'Het uurtarief',
    '180 euro exclusief btw voor 3 uur. Het uurtarief is 60 euro exclusief btw en geldt ook voor extra uren.': 'Je boekt per blok van 3 uur. Extra uren kan je erbij boeken.',
    '180 euro exclusief btw. Het uurtarief is 60 euro exclusief btw, en extra uren boek je aan hetzelfde tarief.': 'Je boekt per blok van 3 uur. Extra uren kan je erbij boeken.',
    'Je boekt extra uren aan hetzelfde tarief van 60 euro per uur exclusief btw, via de boekpagina of na een telefoontje naar 0470 56 53 58.': 'Je boekt extra uren erbij, via de boekpagina of na een telefoontje naar 0470 56 53 58.',
    'Het tarief is hetzelfde voor elke taak: 60 euro per uur exclusief btw, dus 180 euro exclusief btw per blok van 3 uur.': 'Hetzelfde pakket voor elke taak, per blok van 3 uur.',
    'Hetzelfde als elke beurt: 60 euro per uur exclusief btw, dus 180 euro exclusief btw per blok van 3 uur.': 'Hetzelfde als elke beurt: je boekt per blok van 3 uur.',
    'Je betaalt voor het geheel 180 euro exclusief btw, en je weet exact wat je eraan hebt.': 'Je weet vooraf exact wat je eraan hebt.',
    'aan 60 euro per uur exclusief btw, dat is 180 euro exclusief btw.': '.',
    'Een bureau, een refter en een kleedruimte die proper blijven, ook als iedereen op het bedrijf buiten bezig is. Eén vaste persoon, 60 euro per uur exclusief btw, in Wingene en Zwevezele.': 'Een bureau, een refter en een kleedruimte die proper blijven, ook als iedereen op het bedrijf buiten bezig is. Eén vaste persoon, regio Wingene en Zwevezele.',
    'Bij Zondags betaal je 60 euro per uur exclusief btw, enkel voor de geboekte uren. Een eigen medewerker brengt loon en andere lasten mee, ook als er weinig werk is.': 'Bij Zondags betaal je enkel voor de geboekte uren. Een eigen medewerker brengt loon en andere lasten mee, ook als er weinig werk is.',
}

def deprice_text(t):
    """Eén tekstknoop (zonder tags): bedragen weg, zin blijft lopen; zinnen die enkel over de prijs gaan vallen weg."""
    if not PRICE.search(t):
        return t
    lead = t[:len(t) - len(t.lstrip())]; trail = t[len(t.rstrip()):]; core = t.strip()
    if core in FIX:
        r = FIX[core]
        return (r if r[0] in '.,' else lead + r) + trail
    for p, r in INLINE:
        core = p.sub(r, core)
    out, dropped, blok, at = [], False, False, None
    for s in SPLIT.split(core):
        if PRICE.search(s) or re.search(r'\b(?:kost|kosten)\.$|\b(?:prijs|tarief) is\.$', s):
            dropped = True; blok |= 'blok' in s
            if at is None: at = len(out)
            continue
        out.append(s)
    out = [EXTRA_NEW if EXTRA.match(s) else ('Je boekt per blok van 3 uur.' if s == 'Per blok van 3 uur.' else s) for s in out]
    if dropped:
        dedup = []
        for s in out:
            if s not in dedup: dedup.append(s)
        out = dedup
        if blok and not any('blok van 3 uur' in s or 'blokken van 3 uur' in s for s in out):
            out.insert(at, 'Je boekt per blok van 3 uur.')
        if out == [EXTRA_NEW]:
            out = ['Je boekt per blok van 3 uur.', EXTRA_NEW]
    core = ' '.join(out)
    core = re.sub(r'\s+([,.])', r'\1', core).replace(',,', ',').replace('.,', '.').replace(',.', '.')
    core = re.sub(r', ook\.', '.', core).strip()
    return lead + core + trail

def deprice_html(html):
    """Alle zichtbare tekst in <body>, buiten <script>/<style>. Titels, metas en JSON-LD blijven zoals ze zijn."""
    b = html.find('<body')
    if b < 0: return html
    head, body = html[:b], html[b:]
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', body, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'>([^<>]+)<', lambda m: '>' + deprice_text(m.group(1)) + '<', parts[i])
    return head + ''.join(parts)

def leftovers(html):
    b = html.find('<body'); body = re.sub(r'<script\b.*?</script>', '', html[b:], flags=re.S)
    return [m.group(0) for m in PRICE.finditer(re.sub(r'<[^>]+>', ' ', body))]

# Premium beelden per type pagina (03-website/beelden van de branding)
PB = {
  'praktijk':  ('sectie-praktijk-2048x1152', 'Rustige wachtzaal met twee stoelen en een houten onthaalbalie'),
  'admin':     ('sectie-administratie-1600x1067', 'Notitieboek, enveloppen en een kop koffie op een houten bureau'),
  'orde':      ('sectie-thuis-op-orde-1600x1067', 'Handen die witte doeken netjes opvouwen op een houten tafel'),
  'tafel':     ('sectie-boodschappen-maaltijden-1600x1067', 'Gedekte tafel met brood, peren en linnen servetten'),
  'licht':     ('achtergrond-licht-2048x1152', 'Zacht ochtendlicht op een lichte muur'),
}
def pband_key(path, old=''):
    p = path.replace('\\', '/')
    if p.startswith(('werken/', 'jobs/')) or 'zondag-worden' in p: return 'orde'
    if 'administra' in p or p.startswith('vragen/'): return 'admin'
    if 'rechterhand' in p or 'concierge' in p or old == '10-boodschappen': return 'tafel'
    return 'praktijk'
def pband_html(path, old=''):
    f, alt = PB[pband_key(path, old)]
    return f'<section class="pband"><img src="assets/img/{f}.webp" alt="{alt}" loading="lazy" width="1600" height="900"></section>\n'
