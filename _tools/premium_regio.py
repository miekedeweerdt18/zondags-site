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
Nooit 'in X', 'in regio X' of 'in de regio X'.
"""
import re, json, os, html as _html
from premium import deprice_html, deprice_text, PRICE

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

def _rx():
    towns = sorted((t for t in TOWNS if t not in ALLOW_IN), key=len, reverse=True)
    alt = '|'.join(re.escape(t) for t in towns)
    # optionele aanloop: 'in en rond', 'in (de) regio'; staart: 'en omgeving' / 'en de omgeving'
    return re.compile(r'(?P<pre>(?P<prev>[\w\'’-]+) )?(?P<in>\b[Ii]n)(?: en rond)? (?:de )?(?:regio )?(?P<town>' + alt +
                      r')(?![\w-])(?P<omg> en (?:de )?omgeving(?! van))?')
RX = _rx()
_SENT = re.compile(r'(?:^|[.!?:]\s+|\n\s*)$')

def regio_text(t, label=False):
    """Eén stuk platte tekst (mag entities bevatten)."""
    if not t or ' ' not in t and 'n' not in t: return t
    def rep(m):
        prev = m.group('prev') or ''
        pre = m.group('pre') or ''
        start = m.start('in')
        cap = m.group('in')[0] == 'I'
        sent_start = bool(_SENT.search(t[:start])) if not pre else False
        town = m.group('town')
        if label:
            word = 'Regio' if (cap and not pre) else 'regio'
            return pre + word + ' ' + town
        if prev.lower() in UIT:
            return pre + 'uit regio ' + town
        word = 'Binnen' if (cap and not pre) or (sent_start and cap) else 'binnen'
        return pre + word + ' regio ' + town
    return RX.sub(rep, t)

def label(t): return regio_text(t, True)
def zin(t): return regio_text(t, False)

def clean_text(t, as_label=False):
    """prijs weg + regio, in die volgorde"""
    return regio_text(deprice_text(t), as_label)

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
                lab = h1 > 0 or (a > 0 and len(s) <= 70 and not s.endswith(('.', '?', '!')))
                toks[j] = regio_text(tk, lab)
        parts[i] = ''.join(toks)
    return ''.join(parts)

def finalize_html(page, path=''):
    """Volledige premium-pass voor één pagina: zichtbare prijzen (Charm), head, JSON-LD, regio."""
    if 'http-equiv="refresh"' in page: return page
    page = deprice_html(page)
    b = page.find('<body')
    if b < 0: return page
    page = _head(page[:b]) + _body(page[b:])
    return _fix_ld(page)

def leftovers_in(page):
    t = _html.unescape(re.sub(r'<[^>]+>', ' ', page))
    return [m.group(0) for m in RX.finditer(t)]
