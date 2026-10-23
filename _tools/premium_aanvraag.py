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
    t = lead_label(t)
    for p, r in ONLINE_LABELS + LABELS:
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

# ---- losse zinnen over online boeken die BOOK niet vangt (23/10, 19u): natuurlijk herschreven ----
F = 'via het aanvraagformulier'
ONLINE = [
    (r'\bBoeken kan online voor een weekdag, minstens twee werkdagen vooraf\.', f'Vraag het aan {F}, dan spreken we samen een weekdag af.'),
    (r'\bJe boekt een extra blok online, minstens twee werkdagen vooraf, aan hetzelfde uurtarief\.', f'Een extra blok vraag je aan {F}, aan hetzelfde uurtarief.'),
    (r'\bBoeken kan online per blok van 3 uur\b', f'Aanvragen kan {F}, per blok van 3 uur'),
    (r'\bBoeken kan online\.', f'Aanvragen kan {F}.'),
    (r'\bJe boekt (per blok van 3 uur), online, en\b', r'Je boekt \1 en'),
    (r'\b(Je boekt (?:per blok van 3 uur|blokken van 3 uur|per blok|binnen regio [^,.]+ één vaste persoon)),? online(?=[,.])', r'\1'),
    (r'\bJe boekt (per blok van 3 uur), online,', r'Je boekt \1,'),
    (r'\bJe boekt blokken van 3 uur, online of na een telefoontje\.', f'Je boekt blokken van 3 uur, {F} of na een telefoontje.'),
    (r'\bBoek (een eerste blok(?: van 3 uur)?|eerst|één blok|een blok van 3 uur)( online|)(?: een blok van 3 uur)?(?: online)?(?:, minstens twee werkdagen vooraf)?(?: voor een weekdag, minstens twee werkdagen vooraf)?(?=[,. ])',
        lambda m: {'een eerste blok': 'Vraag een eerste blok aan ' + F, 'een eerste blok van 3 uur': 'Vraag een eerste blok van 3 uur aan ' + F,
                   'eerst': 'Vraag eerst een blok van 3 uur aan ' + F, 'één blok': 'Vraag één blok aan ' + F + ', dan spreken we samen een weekdag af',
                   'een blok van 3 uur': 'Vraag een blok van 3 uur aan ' + F}[m.group(1)]),
    (r'\bEen losse boeking kan je ook meteen online regelen\.', f'Een losse beurt vraag je ook meteen aan {F}.'),
    (r'\bJe boekt één blok van 3 uur online aan het normale tarief en beslist', f'Je vraagt één blok van 3 uur aan {F}, aan het normale tarief, en beslist'),
    (r'\bJe boekt (één blok van 3 uur|een eerste blok|extra blokken|het) online\b', lambda m: f'Je vraagt {m.group(1)} aan {F}'),
    (r'\bje boekt (extra blokken|het) online\b', lambda m: f'je vraagt {m.group(1)} aan {F}'),
    (r'\ben je boekt de eerste beurt online\.', 'en spreken samen de eerste beurt af.'),
    (r'\bboek je gewoon een blok online\.', f'vraag je gewoon een blok aan {F}.'),
    (r'\bJe kan online een eerste blok boeken of\b', f'Je kan een eerste blok aanvragen {F} of'),
    (r'\bNiet voor een losse boeking, die kan je online doen\.', f'Niet voor een losse beurt, die vraag je aan {F}.'),
    (r'\bEen losse beurt boek je rechtstreeks online\.', f'Een losse beurt vraag je rechtstreeks aan {F}.'),
    (r'\bVoor een losse boeking krijg je een bevestiging na je online bestelling\.', 'Voor een losse beurt nemen we na je aanvraag binnen één werkdag contact op.'),
    (r'\bLosse extra blokken kan je online bijboeken\.', f'Losse extra blokken vraag je aan {F}.'),
    (r'\bEen extra blok boeken voor een drukke periode kan online,', f'Een extra blok voor een drukke periode vraag je aan {F},'),
    (r'\bboek je dat online voor een weekdag in blokken van 3 uur, extra uren kan je erbij boeken\.', f'vraag je dat aan {F}, voor een weekdag in blokken van 3 uur, en extra uren kan je erbij vragen.'),
    # dubbel/scheef na de eerste pass
    (r'via het aanvraagformulier (?:op|via) de (<a\b[^>]*>)aanvraagformulier</a>', r'via het \1aanvraagformulier</a>'),
    (r'via het aanvraagformulier (?:op|via) de boekpagina', 'via het aanvraagformulier'),
    (r'via het aanvraagformulier (?:op|via) (<a\b[^>]*>)de aanvraagformulier</a>', r'via het \1aanvraagformulier</a>'),
    (r'(aanvraagformulier</a>)(?=[A-Z])', r'\1. '),
    (r'\b(op|via) de (<a\b[^>]*>)?aanvraagformulier\b', r'\1 het \2aanvraagformulier'),
    (r'\bOnline aanvragen via het aanvraagformulier\b', 'Aanvragen via het formulier'),
    # oude online betaling / online kiezen
    (r': datum, aantal blokken, taken en de gegevens van je bedrijf, daarna betaal je online\.', ': je gegevens, de taken en wanneer je wil starten. Binnen één werkdag nemen we contact op.'),
    (r'\bBetalen doe je online, de factuur komt\b', 'De factuur komt'),
    (r'\bBetalen (?:doe je|gaat) online\.', 'Je krijgt een factuur op naam van je bedrijf.'),
    (r'\bJe rekent online af en (?:krijgt|ontvangt) een dienstenfactuur\b', 'Je krijgt een dienstenfactuur'),
    (r'\bJe geeft de gegevens van je bedrijf in en rekent online af\.', f'Je geeft de gegevens van je bedrijf in {F}.'),
    (r'\bOmdat je online betaalt, is de factuur bij ontvangst al vereffend\. Dat is handig voor je boekhouder: de betaling zit meteen in je bankuittreksel of in het overzicht van je kaart, en de factuur hoeft niet in een betaalrun terecht te komen\.', 'Hoe en wanneer je de factuur betaalt, spreken we samen af na je aanvraag.'),
    (r'\bJe betaalt dat blok online\. ?', ''),
    (r'\bJe kiest datum en moment online of belt\b', f'Je vraagt het aan {F} of belt'),
    (r'\bJe kiest online de datum en het aantal blokken van 3 uur,', f'Je vraagt de blokken van 3 uur aan {F},'),
    (r'\bJe kiest dat zelf online\.', 'Dat spreek je gewoon met ons af.'),
    (r'\bOnline kan voor een weekdag, minstens twee werkdagen vooraf\.', f'Vraag het aan {F}, dan nemen we binnen één werkdag contact op en spreken we samen een weekdag af.'),
    (r'\bEen eerste beurt boek je bij Zondags \(zondags\.be\) online voor een weekdag, minstens twee werkdagen vooraf\.', f'Een eerste beurt vraag je bij Zondags (zondags.be) aan {F}. Binnen één werkdag nemen we contact op en spreken we samen een weekdag af.'),
]
ONLINE_LABELS = [(r'^Boeken (?:en betalen|en bijsturen|kan) online$', 'Aanvragen via het formulier'), (r'^Online aanvragen via (?:de|het) aanvraagformulier$', 'Aanvragen via het formulier')]

def qfix(q):
    """FAQ-vragen 'Hoe boek ik...?' / 'Hoe snel kan ik ... boeken?' -> aanvragen"""
    if 'boekhoud' in q: return q
    m = re.match(r'^Hoe boek ik(.*)\?$', q)
    if m:
        rest = m.group(1)
        if rest.startswith(' de eerste keer'): return 'Hoe vraag ik de eerste keer een Zondag aan' + rest[len(' de eerste keer'):] + '?'
        k = re.search(r' (?:binnen|voor|uit|als)\b|,', rest)
        obj, tail = (rest[:k.start()], rest[k.start():]) if k else (rest, '')
        return f'Hoe vraag ik{obj or " een Zondag"} aan{tail}?'
    m = re.match(r'^Hoe snel kan ik (.*?)boeken(.*)\?$', q)
    if m: return f'Hoe snel kan ik {m.group(1) or "een Zondag "}aanvragen{m.group(2)}?'
    q = re.sub(r'\b(voor|voordat) ik boek\?$', r'\1 ik aanvraag?', q)
    q = re.sub(r'\bvoor we boeken\?$', 'voor we aanvragen?', q)
    return q

# ---- geen vaste aanlooptijd meer (Mieke, 23/10: 'minstens twee werkdagen vooraf' weg) ----
_W = r'(?:minstens|zeker) twee werkdagen (?:vooraf|op voorhand)'
_DAG = 'Je Zondag komt op een weekdag die we samen afspreken.'
_START = 'De startdag spreken we samen af.'
LEAD_LABELS = [
    (r'^Losse beurt: ' + _W + r'$', 'Losse beurt: dag in overleg'),
    (r'^Boeken ' + _W + r'$', 'Startdag samen afspreken'),
    (r'^Op een weekdag, ' + _W + r'$', 'Op een weekdag, in overleg'),
    (r'^(?:Online boeken(?: en betalen)?|Boeken), ' + _W + r'$', 'Startdag samen afspreken'),
]
LEAD = [
    # antwoorden die enkel uit de regel bestaan
    (r'(?:(?<=^)|(?<=[>"] )|(?<=[.?!] ))(?:Minstens twee werkdagen vooraf, voor een weekdag|Minstens twee werkdagen voor een weekdag|Voor een weekdag, ' + _W + r'|Minstens twee werkdagen na je boeking, op een weekdag)\.', 'Op een weekdag die we samen afspreken.'),
    (r'^Minstens twee werkdagen (?:vooraf|op voorhand)\.', 'Dat spreken we samen af na je aanvraag.'),
    (r'(?:(?<=[>"] )|(?<=[.?!] ))Minstens twee werkdagen (?:vooraf|op voorhand)\.', '\x00'),
    (r'\bBoek liever iets eerder, zodat\b', 'Vraag liever op tijd aan, zodat'),
    # zinnen die enkel de regel geven
    (r'\bEr is geen haast: boeken kan (?:voor|op) een weekdag, ' + _W + r'\.', 'Er is geen haast: je Zondag komt op een weekdag die we samen afspreken.'),
    (r'\b(?:Boeken kan (?:voor|op) (?:een weekdag|weekdagen), ' + _W + r'|Boeken kan ' + _W + r', (?:voor een weekdag|op weekdagen)|Je boekt (?:voor )?een weekdag, ' + _W + r'|Dat kan voor een weekdag, ' + _W + r'|Een boeking moet ' + _W + r' vastliggen, voor een weekdag)\.', _DAG),
    (r'\bJa, op weekdagen, ' + _W + r'\.', 'Ja, op weekdagen, op een dag die we samen afspreken.'),
    (r'\bJe boekt ' + _W + r', of je vraagt een vast terugkerend plan aan\.', 'Je vraagt een losse beurt of een vast terugkerend plan aan, en de dag spreken we samen af.'),
    (r'\b(?:Een enkel blok|Een eenmalige beurt) boek je ' + _W + r'\.', lambda m: 'Ook ' + m.group(0)[0].lower() + m.group(0)[1:].split(' boek je')[0] + ' kan, op een dag die we samen afspreken.'),
    (r'\bVoor een eenmalige beurt boek je ' + _W + r'\.', 'Ook een eenmalige beurt kan, op een dag die we samen afspreken.'),
    (r'\bEen eerste blok boek je ' + _W + r'\.', 'Voor een eerste blok spreken we de dag samen af.'),
    (r'\bEen blok boek je ' + _W + r' voor een weekdag\.', 'Een blok plannen we samen in, op een weekdag.'),
    (r'\bBoek zeker twee werkdagen (?:vooraf|op voorhand)\.', 'Spreek die dag op tijd met ons af.'),
    (r'\bSpreek (dat|het) vooraf af, (?:minstens twee werkdagen voor je boekt|boeken kan ' + _W + r')\.', r'Spreek \1 vooraf met ons af.'),
    (r'\bDe dagen kies je zelf, zolang het een weekdag is en je ' + _W + r' boekt\.', 'De dagen kies je zelf, zolang het een weekdag is.'),
    (r'\bJe boekt per blok van 3 uur, en je boekt ' + _W + r'\.', 'Je boekt per blok van 3 uur, en de dag spreken we samen af.'),
    (r'\b(?:Het boeken kan|Boeken kan|Dat kan|Boek|Houd er rekening mee dat je) ' + _W + r'(?: boekt)?\.|\bMinstens twee werkdagen vooraf boeken (?:is nodig|volstaat)\.|\bDe afspraak moet ' + _W + r' vastliggen\.', '\x00'),
    # bijzin weglaten, de rest van de zin blijft
    (r' met minstens twee werkdagen voorsprong', ''),
    (r',? ' + _W + r'(?=[,.])', ''),
]
_SAMEN = re.compile(r'af te spreken|spreken we samen|samen af|in overleg', re.I)
def lead(t):
    if not re.search(r'twee werkdagen', t): return t
    for p, r in LEAD: t = re.sub(p, r, t)
    return t
def lead_fix(t):
    """marker \\x00 = weggevallen regelzin: weg als de tekst de afspraak al noemt, anders de startdagzin"""
    if '\x00' in t:
        rest = plain(t.replace('\x00', ''))
        if rest and _SAMEN.search(rest): t = re.sub(r'\s*\x00', '', t).lstrip()
        else: t = t.replace('\x00', _START)
    if 'die we samen afspreken' in t:   # niet twee keer 'afspreken' na elkaar
        t = re.sub(r'(af te spreken\.|samen de rest af\.)(\s*)Je Zondag komt op een weekdag die we samen afspreken\.', r'\1\2Je Zondag komt op een weekdag.', t)
    return t
def lead_label(t):
    for p, r in LEAD_LABELS:
        n = re.sub(p, r, t)
        if n != t: return n
    return lead_fix(lead(t))

def online(t):
    for p, r in ONLINE: t = re.sub(p, r, t)
    return t

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
    return lead_fix(_text(lead(online(t)), inline_html))

def _text(t, inline_html=True):
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
    q = qfix(q)
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
    if len(t) <= 140 and t.rstrip().endswith('?'): t = qfix(t)
    keep = STATE['n']; STATE['n'] = 0          # metas en JSON-LD krijgen altijd de volledige zin
    try: return text(t, False)
    finally: STATE['n'] = keep
