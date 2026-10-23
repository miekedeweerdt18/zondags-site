# -*- coding: utf-8 -*-
"""Premium (23/10/2026): /boeken is een aanvraagformulier, geen boek- of betaalpagina meer.
Zinnen over online boeken en online betalen (kaart, Bancontact, Stripe, 'boekpagina') worden
herschreven naar de echte werkwijze: aanvraag via het formulier, binnen één werkdag contact.
'Je boekt per blok van 3 uur' blijft (eenheid, geen tarief). Draait in finalize_html, na de prijspass.
"""
import re, html as _html

ANCHOR = re.compile(r'<a\b[^>]*href="(?:\.\./)*boeken\.html"[^>]*>')
PAY = re.compile(r'betaal(?:t|d)?(?: je)?(?: \w+)? online|online (?:te )?betal|online betaald|bancontact|stripe|'
                 r'betaal(?:t)?(?: je)? met (?:je )?kaart|met kaart of|betaalpagina|betaling (?:gebeurt |verloopt )?online', re.I)
BOOK = re.compile(r'boekpagina|\bboek(?:t|en)?(?: je)? (?:meteen |direct |gewoon )?online|online (?:te |kan je |kun je )?(?:boek|in te plannen)|'
                  r'\bboeken doe je\b|\bboek(?:t)?(?: je)? (?:via|op) (?:de|zondags)|zondags\.be/boeken|bij het (?:online )?boeken|'
                  r'online geboekt|meteen (?:online )?boeken|\bkan je (?:meteen |ook )?boeken\b|\bboek je (?:meteen|zelf)\b', re.I)

def plain(s): return _html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

# ---- korte labels (facts, tussentitels) ----
LABELS = [
    (r'^Prijs en online boeken$', 'Ons pakket en aanvragen'),
    (r'^Wat je betaalt en hoe je boekt$', 'Ons pakket en aanvragen'),
    (r'^Betalen met kaart of Bancontact$', 'Factuur op naam van je bedrijf'),
    (r'^Online boeken(?: en betalen)?(?:, minstens twee werkdagen vooraf| per blok van 3 uur)?$', 'Online aanvragen'),
    (r'^Online boeken(?: en betalen)?(, .+)$', r'Online aanvragen\1'),
    (r'^(.+), online boeken(?: en betalen)?$', r'\1, online aanvragen'),
    (r'^Boek online$', 'Vraag aan'),
    (r'^Boek meteen online$', 'Vraag meteen aan'),
    (r'^Kan ik als bedrijf online betalen met Bancontact of kaart\?$', 'Hoe betaal ik als bedrijf voor een Zondag?'),
    (r'^Wanneer vraag ik beter een terugbelverzoek dan online te boeken\?$', 'Wanneer vraag ik beter een terugbelverzoek dan het aanvraagformulier te gebruiken?'),
    (r'^Online boeken op zondags\.be/boeken$', 'Online aanvragen op zondags.be/boeken'),
    (r'^Eerst praten of meteen boeken$', 'Eerst praten of meteen aanvragen'),
    (r'^Online: duid bij het boeken het aantal extra uren aan$', 'Online: vermeld de extra uren in je aanvraag'),
    (r'^Het btw-nummer vergeten bij het boeken$', 'Het btw-nummer vergeten in je aanvraag'),
    (r'^Wat je (?:bij het boeken opgeeft|ingeeft bij het boeken)$', 'Wat je in je aanvraag opgeeft'),
    (r'^Online boeken(?: en betalen)? (binnen|in|voor|rond) (.+)$', r'Online aanvragen \1 \2'),
    (r'^Prijs, factuur en online boeken$', 'Ons pakket, factuur en aanvragen'),
    (r'^Je boekt online$', 'Je vraagt aan'),
    (r'^Je betaalt veilig via Stripe$', 'Je krijgt een factuur'),
    (r'^Vijf stappen op de boekpagina$', 'Aanvraag via het formulier'),
    (r'^(?:Online betalen met kaart of Bancontact|Bancontact of kaart|Online via Stripe|Betalen bij het boeken)$', ''),
]
def label(t):
    for p, r in LABELS:
        n = re.sub(p, r, t)
        if n != t: return n
    if PAY.search(t) or BOOK.search(t):
        n = re.sub(r'\b([Oo])nline boeken(?: en betalen)?', lambda m: m.group(1) + 'nline aanvragen', t)
        n = re.sub(r'\bboekpagina\b', 'aanvraagformulier', n)
        if n != t and not (PAY.search(n) or BOOK.search(n)): return n
        if PAY.search(n) and not BOOK.search(n): return ''
    return t

# ---- zinsdelen die de zin laten lopen ----
CLAUSES = [
    (r'\b(boek(?:t)?(?: je)?) online (per blok|in blokken)', r'\1 \2'),
    (r'\bJe betaalt (?:online|met kaart of Bancontact)(?: met kaart of Bancontact)? en (krijgt|ontvangt)', r'Je \1'),
    (r'\bBetaal online en je (krijgt|ontvangt)', r'Je \1'),
    (r', (?:en )?(?:meteen )?online boeken(?: en betalen)?(?: per blok van 3 uur)?(?=[.;]|$)', ', online aan te vragen'),
    (r'(^|[.!?] )Online boeken(?: en betalen)?(?: per blok van 3 uur)?, ', r'\1Online aan te vragen, '),
    (r'\bMeteen starten kan ook online\.', 'Meteen starten kan ook via het aanvraagformulier.'),
    (r'(^|[.!?] )Online te boeken\.', r'\1Online aan te vragen.'),
]

CANON_LINK = 'Vraag je Zondag aan via het {a}aanvraagformulier</a>, dan nemen we binnen één werkdag contact op om de rest af te spreken.'
CANON_TXT = 'Je vraagt je Zondag aan via het aanvraagformulier op zondags.be/boeken, en binnen één werkdag nemen we contact op om de rest af te spreken.'
CANON_CB_LINK = 'Laat je aanvraag achter via het {a}aanvraagformulier</a> of vraag een terugbelgesprek aan, dan spreken we samen de rest af.'
CANON_CB_TXT = 'Laat je aanvraag achter via het aanvraagformulier op zondags.be/boeken of vraag een terugbelgesprek aan, dan spreken we samen de rest af.'
SHORT_LINK = 'Je aanvraag doe je via het {a}aanvraagformulier</a>.'
SHORT_TXT = 'Je aanvraag doe je via het aanvraagformulier op zondags.be/boeken.'
STATE = {'n': 0}
FACT_RX = re.compile(r'\b(diensten)?factuur op naam van (?:je|jouw) (bedrijf|vennootschap|praktijk|zaak|vzw|onderneming|kantoor)', re.I)

def _factuur(t):
    m = FACT_RX.search(t)
    if not m: return ''
    return f'Je krijgt een {(m.group(1) or "").lower()}factuur op naam van je {m.group(2).lower()}.'

def sentence(s, a=None):
    """Eén zin (met eventuele inline tags). Geeft de nieuwe zin terug, '' = zin valt weg."""
    for p, r in CLAUSES: s = re.sub(p, r, s)
    t = plain(s)
    if 'aanvraagformulier' in t: return s   # al herschreven (idempotent)
    if not (PAY.search(t) or BOOK.search(t)): return s
    m = ANCHOR.search(s); a = m.group(0) if m else None
    if t.endswith('?'):
        return 'Hoe verloopt de betaling?' if PAY.search(t) and not BOOK.search(t) else 'Hoe vraag ik een Zondag aan?'
    if BOOK.search(t):
        cb = 'terugbel' in t.lower()
        STATE['n'] += 1
        if STATE['n'] > 1 and not cb:   # niet op elke plek van de pagina dezelfde lange zin
            return SHORT_LINK.format(a=a) if a else SHORT_TXT
        if a: return (CANON_CB_LINK if cb else CANON_LINK).format(a=a)
        return CANON_CB_TXT if cb else CANON_TXT
    return _factuur(t)

SPLIT = re.compile(r'(?<=[.?!])(\s+)(?=[A-ZÉÈ"\u201c<])')
LEAD_Q = re.compile(r'^(?:Liever|Wil je|Wilt u|Zin om|Klaar om)\b.*\?$')

def text(t, inline_html=True):
    """Lopende tekst (een blok of een plain string)."""
    if not (PAY.search(plain(t)) or BOOK.search(plain(t))): return t
    if 'aanvraagformulier' in plain(t) and not PAY.search(plain(t)) and not BOOK.search(re.sub(r'aanvraagformulier op zondags\.be/boeken', '', plain(t))): return t
    parts = SPLIT.split(t)
    sents = parts[0::2]; seps = parts[1::2] + ['']
    out = []
    for i, s in enumerate(sents):
        n = sentence(s)
        if n != s and n and i and out and (LEAD_Q.match(plain(out[-1][0])) and not plain(out[-1][0]).startswith('Hoe ')
                                           or plain(out[-1][0]) in ('Ja.', 'Zeker.', 'Ja, dat kan.')):
            out.pop()  # 'Liever meteen starten?' voor een herschreven boekzin
        if n and any(plain(n) == plain(o) for o, _ in out): n = ''
        if n: out.append((n, seps[i]))
    if not out: return ''
    out[-1] = (out[-1][0], '')
    r = ''.join(s + sep for s, sep in out)
    return r

CANON_Q_BOOK = 'Hoe vraag ik een Zondag aan?'
CANON_A_BOOK = ('Via het aanvraagformulier op zondags.be/boeken: je naam, je bedrijf of praktijk, je gemeente, de taken en wanneer je wil starten. '
                'Binnen één werkdag nemen we contact op om dag, uur en de rest samen af te spreken.')
CANON_Q_PAY = 'Hoe verloopt de betaling?'
CANON_A_PAY = 'Je krijgt een factuur op naam van je bedrijf. De praktische afspraken maken we samen, nadat je je aanvraag via het aanvraagformulier hebt doorgegeven.'

def faq_pair(q, a):
    """Vraag + antwoord (plain). Gaat de vraag over online boeken/betalen, dan beide vervangen."""
    tq = plain(q)
    if PAY.search(tq) or BOOK.search(tq) or re.search(r'\bboek(?:en)?\b.*\?$', tq) and re.search(r'online', tq, re.I):
        if PAY.search(tq) and not BOOK.search(tq): return CANON_Q_PAY, CANON_A_PAY
        return CANON_Q_BOOK, CANON_A_BOOK
    na = text(a)
    if not plain(na) and re.search(r'\bboek', tq, re.I): return CANON_Q_BOOK, CANON_A_BOOK
    return q, na

BLOCK = re.compile(r'(<(p|li|h[2-6]|dd|dt|td|figcaption|blockquote)\b[^>]*>)(.*?)(</\2>)', re.S)
DETAILS = re.compile(r'(<details\b[^>]*>\s*<summary\b[^>]*>)(.*?)(<span aria-hidden="true">\+</span></summary>\s*<p>)(.*?)(</p>\s*</details>)', re.S)

BOTH = re.compile(DETAILS.pattern + '|' + BLOCK.pattern.replace('\\2', '\\7'), re.S)
class _Shift:
    """maakt van een BOTH-match (BLOCK-deel = groepen 6..9) een BLOCK-achtige match"""
    def __init__(self, m): self.m = m
    def group(self, i): return self.m.group(0) if i == 0 else self.m.group(i + 5)

def body(b):
    STATE['n'] = len(re.findall(r'binnen één werkdag contact op om de rest|binnen één werkdag nemen we contact op om de rest|Je aanvraag doe je via', plain(re.sub(r'<script\b.*?</script>', '', b, flags=re.S))))
    seen_q = set()
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', b, flags=re.S)
    for i in range(0, len(parts), 2):
        seg = parts[i]
        def det(m):
            q, a = faq_pair(m.group(2), m.group(4))
            if q in (CANON_Q_BOOK, CANON_Q_PAY):
                if q in seen_q: return ''          # zelfde vraag niet twee keer
                seen_q.add(q)
            return m.group(1) + q + m.group(3) + a + m.group(5)
        def blk(m):
            inner = m.group(3)
            if re.search(r'<(?:p|li|h[2-6])\b', inner): return m.group(1) + BLOCK.sub(blk, inner) + m.group(4)
            pt = plain(inner)
            if pt and len(pt) <= 70 and not pt.endswith(('.', '?', '!')):
                new = label(inner) if '<' not in inner else inner
            else:
                new = text(inner)
            if not plain(new) and m.group(2) == 'li': return ''
            return m.group(1) + new + m.group(4)
        seg = BOTH.sub(lambda m: det(m) if m.group(1) is not None else blk(_Shift(m)), seg)   # in documentvolgorde
        seg = re.sub(r'(<a\b[^>]*class="rel__a"[^>]*>)([^<]+)(<)', lambda m: m.group(1) + label(m.group(2)) + m.group(3), seg)
        seg = re.sub(r'(<a\b[^>]*href="(?:\.\./)*boeken\.html"[^>]*>)([^<]+)(</a>)', lambda m: m.group(1) + label(m.group(2)) + m.group(3), seg)
        parts[i] = seg
    return ''.join(parts)

def plain_text(t):
    """metas, JSON-LD (geen tags)"""
    if len(t) <= 70 and not t.rstrip().endswith(('.', '?', '!')): return label(t)
    keep = STATE['n']; STATE['n'] = 0          # metas en JSON-LD krijgen altijd de volledige zin
    try: return text(t, False)
    finally: STATE['n'] = keep
