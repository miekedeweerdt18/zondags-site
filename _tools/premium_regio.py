# -*- coding: utf-8 -*-
"""Premium uitrol (23/10/2026): 'in <gemeente>' wordt 'regio <gemeente>' en prijzen verdwijnen ook uit
title, metas, JSON-LD (incl. FAQ-schema), llms.txt en chat.js.

Eén schakelaar: ALLOW_IN. Enkel die gemeenten mogen nog 'in <gemeente>' zeggen (het echte kantoor).
Kortrijk toevoegen = ALLOW_IN = {'Marke', 'Kortrijk'} en opnieuw bouwen:
    PYTHONPATH=_tools python3 _tools/premium_finalize.py && PYTHONPATH=_tools python3 _tools/pseo.py

Twee schrijfwijzen:
- label (title, og:title, H1, korte linkteksten, JSON-LD name/headline/title): 'Poetshulp in Kortrijk' -> 'Poetshulp regio Kortrijk'
- zin (body, metas, FAQ, alt): 'actief in Kortrijk en omgeving' -> 'actief binnen regio Kortrijk',
  'kantoren in Kortrijk' -> 'kantoren uit regio Kortrijk', 'In Gent kan je' -> 'Binnen regio Gent kan je'
- taalpas (23/10): 'een kantoor in X' -> 'een kantoor uit regio X' (UIT_SUFFIX), 'we zoeken Zondags uit regio X',
  tweede vermelding in dezelfde zin na en/of/ook/tot/komma -> 'regio X' (geen dubbel 'binnen regio'),
  link in een lopende zin na een vacature-woord -> 'binnen regio X', los lijstitem/tussentitel -> 'Regio X'.
- labels: werkwoord/tijd ervoor (Starten, Boeken, voorbeeldweek) -> "binnen regio X"; "Klanten" -> "uit regio X"; kort fragment met werkwoord = zin.
Nooit 'in X', 'in regio X' of 'in de regio X'.
"""
import re, json, os, html as _html
from premium import deprice_html, deprice_text, PRICE
import premium_aanvraag as AANVRAAG  # /boeken = aanvraagformulier: geen online boeken/betalen meer in de tekst

ALLOW_IN = {'Marke'}          # <- de enige schakelaar

_HERE = os.path.dirname(os.path.abspath(__file__))
def _load_towns():
    plan = json.load(open(os.path.join(_HERE, 'content', 'plan.json')))
    names = set()
    for P in plan:
        for k in ('place', 'in_de_buurt', 'members', 'deelgemeenten'):
            v = P.get(k)
            if isinstance(v, str): names.add(v)
            elif isinstance(v, list): names |= {x for x in v if isinstance(x, str)}
    names -= {'Werken'}            # deelgemeente van Kortrijk, maar ook een gewoon woord
    return names
TOWNS = _load_towns()

# organisaties/personen: 'kantoren in X' -> 'kantoren uit regio X'
UIT = {'bedrijven', 'kantoren', 'praktijken', 'winkels', 'bedrijfsleiders', 'zaakvoerders', 'ondernemers', "kmo's",
       'zaken', 'familiebedrijven', 'landbouwbedrijven', 'vennootschappen', 'studenten', 'mensen', 'huisartsen',
       'klanten', 'beroepen', 'artsen', 'zelfstandigen', 'showrooms', 'collega\'s', 'gezinnen', 'organisaties',
       'vzw\'s', 'tandartsen', 'kinesisten', 'apothekers', 'notarissen', 'advocaten', 'architecten', 'accountants'}

# enkelvoudige zaken: 'een kantoor in X' -> 'een kantoor uit regio X' (ook samenstellingen: tandartspraktijk, bouwbedrijf, ...)
UIT_SUFFIX = ('kantoor', 'praktijk', 'bedrijf', 'zaak', 'firma', 'bureau', 'unit', 'winkel', 'shop', 'showroom',
              'toonzaal', 'magazijn', 'atelier', 'vennootschap', 'kmo', 'consultant', 'zaakvoerder', 'bedrijfsleider',
              'buur', 'buren', 'student')
# vacature-woorden: in een lopende zin wordt een link 'studentenjob in X' -> 'studentenjob binnen regio X'
JOB = {'job', 'flexi-job', 'studentenjob', 'overdag', 'weekends', 'bijverdienen', 'contract', 'uren', 'studentencontract'}
# opsomming na een eerdere vervanging in dezelfde zin: 'binnen regio A en binnen regio B' -> 'binnen regio A en regio B'
CHAIN = {'en', 'of', 'ook', 'tot', 'richting', 'maar', 'zoals'}
_PLACE_VERB = re.compile(r'\b(?:[Ll]igt|[Ll]iggen|[Zz]it|[Zz]itten|gevestigd|[Ww]erk|[Ww]erkt|[Ww]erken|huurt|hebt|heeft)\b')

def _rx():
    towns = sorted((t for t in TOWNS if t not in ALLOW_IN), key=len, reverse=True)
    alt = '|'.join(re.escape(t) for t in towns)
    # optionele aanloop: 'in en rond', 'in (de) regio'; staart: 'en (de) omgeving/buurt', 'en rondom', 'en omstreken'
    return re.compile(r'(?P<pre>(?P<prev>[\w\'’-]+,?) )?(?P<in>\b[Ii]n)(?: en rond)? (?:de )?(?:regio )?(?P<town>' + alt +
                      r')(?![\w-])(?P<omg> en (?:de )?(?:omgeving|buurt)(?! van)| en rondom| en omstreken)?')
RX = _rx()
_SENT = re.compile(r'(?:^|[.!?:]\s+|\n\s*)$')
_SENT_END = re.compile(r'[.!?]\s')

# labels die met een werkwoord/tijdsaanduiding beginnen lezen beter met 'binnen' ('Starten binnen regio X'),
# 'Klanten' leest beter met 'uit' ('Klanten uit regio X'); een kort fragment met een werkwoord is een zin.
LABEL_BINNEN = {'starten', 'boeken', 'voorbeeldweek', 'week', 'dag', 'werken', 'beginnen'}
LABEL_UIT = {'klanten'}
_FRAG_VERB = re.compile(r'\b(zijn|is|ligt|liggen|zit|zitten|werkt|werken|zoekt|zoeken)\b', re.I)

def _is_uit(prev, before, sentence):
    w = prev.lower().rstrip(',')
    if not w: return False
    if w == 'zondags' and prev == 'Zondags' and re.search(r'\bzoek', sentence): return True     # 'we zoeken Zondags uit regio X'
    if not (w in UIT or w.endswith(UIT_SUFFIX)): return False
    words = before.split()[-4:-1]          # woorden voor het zelfstandig naamwoord
    if 'in' in [x.lower() for x in words[-2:]]: return False      # 'in een kantoor in X' -> 'binnen regio X'
    if _PLACE_VERB.search(' '.join(before.split()[-4:])): return False   # 'Ligt je zaak in X' -> 'binnen regio X'
    return True

def regio_text(t, label=False, inline=False):
    """Eén stuk platte tekst (mag entities bevatten).
    label=True: korte labels (title, H1, losse link/lijstitem): 'regio X'.
    inline=True (enkel samen met label): link midden in een zin; na een vacature-woord wordt het 'binnen regio X'."""
    if not t or ' ' not in t and 'n' not in t: return t
    done = []                              # posities van eerdere vervangingen in deze tekst
    def rep(m):
        prev = m.group('prev') or ''
        pre = m.group('pre') or ''
        start = m.start('in')
        cap = m.group('in')[0] == 'I'
        sent_start = bool(_SENT.search(t[:start])) if not pre else False
        town = m.group('town')
        sb = max([0] + [x.end() for x in _SENT_END.finditer(t[:start])])
        se = _SENT_END.search(t, m.end()); sentence = t[sb:se.start() if se else len(t)]
        earlier = any(sb <= d < start for d in done)
        done.append(start)
        lab = label and not (inline and prev.lower() in JOB) and not (label and _FRAG_VERB.search(t[:start]) and prev.lower() not in LABEL_BINNEN)
        if lab and prev.lower().rstrip(':') in LABEL_BINNEN:
            return pre + 'binnen regio ' + town
        if lab and prev.lower().rstrip(':') in LABEL_UIT:
            return pre + 'uit regio ' + town
        if lab:
            word = 'Regio' if (cap and not pre) else 'regio'
            return pre + word + ' ' + town
        lastw = (t[:start].split() or [''])[-1]
        if earlier and (lastw.lower().rstrip(',') in CHAIN or lastw.endswith(',')):
            return pre + 'regio ' + town
        if _is_uit(prev, t[:m.start('in')], sentence):
            return pre + 'uit regio ' + town
        word = 'Binnen' if (cap and not pre) or (sent_start and cap) else 'binnen'
        return pre + word + ' regio ' + town
    return RX.sub(rep, t)

def label(t): return regio_text(t, True)
def zin(t): return regio_text(t, False)

def clean_text(t, as_label=False):
    """prijs weg + regio, in die volgorde"""
    return regio_text(AANVRAAG.plain_text(deprice_text(t)), as_label)

# ---------------- HTML ----------------
LABEL_KEYS = {'name', 'headline', 'title', 'serviceType', 'alternativeHeadline'}
DROP_KEYS = {'priceRange', 'offers', 'priceSpecification', 'price', 'priceCurrency'}

def _ld_walk(x, parent_type=None, key=None):
    if isinstance(x, dict):
        t = x.get('@type')
        return {k: _ld_walk(v, t if t else parent_type, k) for k, v in x.items() if k not in DROP_KEYS}
    if isinstance(x, list):
        return [_ld_walk(v, parent_type, key) for v in x]
    if isinstance(x, str):
        if key in ('@id', '@type', '@context', 'url', 'item', 'image', 'sameAs', 'mainEntityOfPage', 'email', 'telephone'): return x
        lab = key in LABEL_KEYS and parent_type not in ('Question',)
        return clean_text(x, lab)
    return x

def _plain(s):
    return _html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def visible_faq(page):
    out = []
    for m in re.finditer(r'<details\b[^>]*>\s*<summary\b[^>]*>(.*?)</summary>(.*?)</details>', page, re.S):
        q = re.sub(r'<span aria-hidden="true">\+</span>', '', m.group(1))
        out.append((_plain(q), _plain(m.group(2))))
    return out

def _fix_ld(page):
    vis = None
    def rep(m):
        nonlocal vis
        raw = m.group(2)
        try: data = json.loads(raw)
        except Exception: return m.group(0)
        new = _ld_walk(data)
        # FAQ-schema = zichtbare tekst, letterlijk
        def faqs(d):
            if isinstance(d, dict):
                if d.get('@type') == 'FAQPage': yield d
                for v in d.values(): yield from faqs(v)
            elif isinstance(d, list):
                for v in d: yield from faqs(v)
        for f in faqs(new):
            if vis is None: vis = visible_faq(page)
            me = f.get('mainEntity', [])
            if vis and len(vis) == len(me):
                for qa, (q, a) in zip(me, vis):
                    qa['name'] = q; qa['acceptedAnswer']['text'] = a
            elif vis and me:   # zichtbare dubbele vraag weggelaten (aanvraagpass): schema volgt de zichtbare lijst
                f['mainEntity'] = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in vis]
        if new == data: return m.group(0)
        compact = '","' in raw or '":{' in raw
        out = json.dumps(new, ensure_ascii=False, separators=(',', ':') if compact else None)
        return m.group(1) + out.replace('</', '<\\/') + m.group(3)
    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', rep, page, flags=re.S)

_ATTR_META = re.compile(r'(<meta (?:name|property)="(description|og:description|twitter:description|og:title|twitter:title)" content=")([^"]*)(")')
_ATTR_BODY = re.compile(r'(\s(?:alt|aria-label|title)=")([^"]*)(")')

TITLE_MAX = 60
def title_text(t):
    """title/og:title: label-vorm. 'regio ' is 3 tekens langer dan 'in ': wordt de title daardoor langer dan
    max(60, oude lengte), dan eerst de postcode weg, dan ' | Zondags'."""
    new = label(deprice_text(t))
    lim = max(TITLE_MAX, len(_html.unescape(t)))
    if len(_html.unescape(new)) > lim: new = re.sub(r' \(\d{4}\)', '', new)
    if len(_html.unescape(new)) > lim and new.endswith(' | Zondags'): new = new[:-len(' | Zondags')]
    return new

def _head(head):
    head = re.sub(r'(<title>)(.*?)(</title>)', lambda m: m.group(1) + title_text(m.group(2)) + m.group(3), head, flags=re.S)
    def meta(m):
        if m.group(2).endswith('title'): return m.group(1) + title_text(m.group(3)) + m.group(4)
        return m.group(1) + clean_text(m.group(3)) + m.group(4)
    return _ATTR_META.sub(meta, head)

_BLOCK_OPEN = re.compile(r'<(li|h[2-6]|dt|dd|p|figcaption|strong|b|span|div)\b[^>]*>$', re.I)
_BLOCK_CLOSE = re.compile(r'</(li|h[2-6]|dt|dd|p|figcaption|strong|b|span|div)>$', re.I)

def _body(body):
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', body, flags=re.S)
    for i in range(0, len(parts), 2):
        toks = re.split(r'(<[^>]+>)', parts[i])
        h1 = a = 0
        for j, tk in enumerate(toks):
            if j % 2:   # tag
                low = tk.lower()
                if low.startswith('<h1'): h1 += 1
                elif low.startswith('</h1'): h1 = max(0, h1 - 1)
                elif low.startswith('<a ') or low == '<a>': a += 1
                elif low.startswith('</a'): a = max(0, a - 1)
                toks[j] = _ATTR_BODY.sub(lambda m: m.group(1) + clean_text(m.group(2)) + m.group(3), tk)
            elif tk.strip():
                s = tk.strip()
                short = len(s) <= 70 and not s.endswith(('.', '?', '!', ':', ','))
                prev_tag = toks[j - 1] if j else ''
                next_tag = toks[j + 1] if j + 1 < len(toks) else ''
                # korte losse tekst in een eigen blok (li, h2, dt, ...) = label: 'Regio X'
                frag = short and bool(_BLOCK_OPEN.match(prev_tag)) and bool(_BLOCK_CLOSE.match(next_tag))
                lab = h1 > 0 or (a > 0 and short) or frag
                inline = False
                if a > 0 and prev_tag.lower().startswith('<a'):
                    before = ''.join(t for t in toks[max(0, j - 3):j - 1] if not t.startswith('<')).rstrip()
                    inline = bool(before) and not before.endswith(('.', '?', '!', ':', '>'))
                toks[j] = regio_text(tk, lab, inline)
        parts[i] = ''.join(toks)
    return ''.join(parts)

def finalize_html(page, path=''):
    """Volledige premium-pass voor één pagina: zichtbare prijzen (Charm), head, JSON-LD, regio."""
    if 'http-equiv="refresh"' in page: return page
    page = deprice_html(page)
    b = page.find('<body')
    if b < 0: return page
    page = _head(page[:b]) + _body(AANVRAAG.body(page[b:]))
    page = _fix_ld(page)
    # na het weghalen van '60 euro per uur.' begint de volgende zin soms met kleine letter: '. per blok' -> '. Per blok'
    return re.sub(r'([.!?]["\u201d]?\s)per blok\b', r'\1Per blok', page)

def leftovers_in(page):
    t = _html.unescape(re.sub(r'<[^>]+>', ' ', page))
    return [m.group(0) for m in RX.finditer(t)]
