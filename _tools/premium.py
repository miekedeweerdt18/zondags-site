"""Premium uitrol (23/10/2026): gedeelde helpers voor pseo.py en de eenmalige migratie.

- deprice(): haalt prijzen en uurtarieven uit tekst (regel: geen prijzen op de site).
- PBAND: welk premium beeld een contentpagina krijgt, per map.
"""
import re

E = r'(?:exclusief|excl\.?|exkl\.?) ?btw'          # "exclusief btw", "excl. btw"
EUR = r'(?:€ ?\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)? ?(?:euro|€))'
# Volgorde telt: specifiek eerst, algemeen daarna.
RULES = [
    # haakjes met een bedrag
    (r' ?\((?:[^()]*?)' + EUR + r'[^()]*\)', ''),
    # "Je betaalt 60 euro per uur exclusief btw, (geboekt) per blok van 3 uur" en varianten
    (r'(Je|je) betaalt ' + EUR + r' per uur(?: ' + E + r')?,? (?:en boek[t]? (?:telkens )?|geboekt |in blokken van|per blok)', lambda m: (m.group(1)+' boekt ' + ('per blok' if m.group(0).endswith('per blok') else 'in blokken van' if m.group(0).endswith('in blokken van') else '')).rstrip()+' '),
    (r'(Je|je) betaalt ' + EUR + r' per uur(?: ' + E + r')?', r'\1 boekt per blok van 3 uur'),
    (r'(Het|het) (?:uur)?tarief is ' + EUR + r'(?: per uur)?(?: ' + E + r')?,? (?:per blok|in blokken|geboekt per blok)', lambda m: ('Je boekt' if m.group(1)=='Het' else 'je boekt') + (' in blokken' if 'blokken' in m.group(0) else ' per blok')),
    (r'(Een|een) (Zondag|uur|vaste Zondag) kost ' + EUR + r'(?: per uur)?(?: ' + E + r')?,? (in blokken|per blok)', lambda m: ('Je boekt' if m.group(1)=='Een' else 'je boekt') + ' ' + ('een Zondag ' if 'Zondag' in m.group(2) else '') + m.group(3)),
    (r'(Eén|één) (?:pakket|tarief)(?: aan|:)? ' + EUR + r' per uur(?: ' + E + r')?,? ', r'\1 pakket, '),
    # lijstpunten en korte feiten
    (r'\b' + EUR + r' per uur,? (?:geboekt )?per blok van 3 uur', 'Per blok van 3 uur'),
    (r'\b' + EUR + r' per uur(?: ' + E + r')?,? (?:geboekt |in )?(?:per )?blok(?:ken)? van 3 uur', 'Per blok van 3 uur'),
    # bijzinnen met een bedrag
    (r',? (?:dus|goed voor|samen|wat neerkomt op|of|is|en dat is|dat is|wat) ' + EUR + r'(?: ' + E + r')?(?: per (?:blok|uur|week|maand))?', ''),
    (r',? (?:aan|voor|tegen|aan dezelfde|aan hetzelfde uurtarief van|aan hetzelfde tarief van) ' + EUR + r'(?: per uur)?(?: ' + E + r')?(?: per (?:blok|uur))?', ''),
    (r',? (?:en |met )?extra uren (?:aan |tegen |kosten )?' + EUR + r'(?: per uur)?(?: ' + E + r')?', ', en extra uren boek je erbij'),
    (r' aan hetzelfde (?:uur)?tarief', ''),
    (r' aan dezelfde prijs', ''),
    (r'(Extra uren) kosten hetzelfde per uur', r'\1 boek je erbij'),
    (r'(extra uren) kosten hetzelfde per uur', r'\1 boek je erbij'),
    (r'(Extra|extra) uren tellen ', r'\1 uren boek je erbij'),
]
RULES = [(re.compile(p), r) for p, r in RULES]
LEFT = re.compile(EUR + r'|\buurtarief\b|\buurprijs\b|per uur ' + E, re.I)

def _sentences_out(t):
    """Laatste vangnet: zinnen die nog een bedrag bevatten, vallen weg (binnen tekst zonder tags of aanhalingstekens)."""
    def drop(m):
        s = m.group(0)
        return '' if LEFT.search(s) else s
    return re.sub(r'(?<=[>".!?:])\s*[^<>"{}\[\]]*?[.!?](?=\s|<|"|$)|(?<=[>".!?:])\s*[^<>"{}\[\].!?]+(?=<|")', drop, t)

def deprice(t):
    for p, r in RULES:
        t = p.sub(r, t)
    t = t.replace(',,', ',').replace(' ,', ',').replace(',.', '.')
    return t

def leftovers(t):
    return LEFT.findall(t)

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
