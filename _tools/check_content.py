# -*- coding: utf-8 -*-
"""Kwaliteitscontrole voor de unieke contentbestanden in _tools/content/**.json
Gebruik:  python3 _tools/check_content.py [bestand.json ...]   (zonder argumenten: alles)
Controleert schema, lengtes, huisstijl (je-vorm, verboden woorden en tekens), links en overlap met andere pagina's."""
import json, re, sys, os, glob, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CDIR = os.path.join(ROOT, '_tools', 'content')
PLAN = {p['path']: p for p in json.load(open(os.path.join(CDIR, 'plan.json')))}

MIN_WORDS = 620          # unieke woorden per pagina (lead + antwoord + secties + faq)
MAX_OVERLAP = 0.30       # max. aandeel gedeelde 5-woordreeksen met eender welke andere pagina
MAX_LINKS = 4

BANNED = [
 (r'—', 'em-dash'), (r'–', 'en-dash'), (r'!', 'uitroepteken'), (r'ontzorg', 'ontzorgen'), (r'totaaloplossing', 'totaaloplossing'),
 (r'een echte mens', 'een echte mens'), (r'poetsvrouw', 'poetsvrouw'), (r'kuisvrouw', 'kuisvrouw'), (r'huishoudster', 'huishoudster'),
 (r'\buw\b', 'u-vorm (uw)'), (r'\bUw\b', 'u-vorm (Uw)'), (r'(?<![\w-])[uU](?![\w-])', 'u-vorm (u)'), (r'€|\beuro\b|\bEUR\b', 'prijs/euro'),
 (r'\d+\s*(%|procent)', 'percentage'), (r'Claude|Anthropic|ChatGPT|Cowork|\bAI\b|kunstmatige intelligentie|OpenAI', 'AI-vermelding'),
 (r'gegarandeerd|garantie|garanderen', 'garantiebelofte'), (r'gecertificeerd|ISO[ -]?\d|ecolabel|keurmerk', 'certificaatclaim'),
 (r'verzekerd|verzekering dekt', 'verzekeringsclaim'), (r'\bhuishouder\b', 'huishouder'), (r'zwart werk|zwartwerk', None),
 (r'beste poets|nummer één|nr\. ?1\b|de goedkoopste|goedkoopste', 'superlatief/claim'), (r'Zondag\'s|zondag\'s', 'spelling Zondags'),
 (r'\bwij hebben al\b|\bonze klanten in\b|tientallen klanten|honderden klanten', 'klantclaim'),
]
ALLOWED_TAGS = re.compile(r'</?(b|li)>|<ul class="ticks">|</ul>|<a href="[^"]+">|</a>')

def existing_targets():
    t = set()
    for f in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        r = os.path.relpath(f, ROOT)
        if r.startswith(('_tools', '.git')): continue
        t.add(r)
        if r.endswith('index.html'): t.add(r[:-10])
    t |= set(PLAN.keys())
    t |= {os.path.dirname(p) + '/' for p in PLAN}
    return t

def text_of(d):
    parts = [d.get('lead', ''), d.get('answer', '')]
    for s in d.get('sections', []):
        parts.append(s.get('h2', '')); parts += s.get('p', [])
    for f in d.get('faq', []):
        parts += [f.get('q', ''), f.get('a', '')]
    return ' '.join(parts)

def words(t):
    t = H.unescape(re.sub(r'<[^>]+>', ' ', t)).lower()
    return re.findall(r"[a-zà-ÿ0-9']+", t)

def shingles(ws, k=5):
    return {' '.join(ws[i:i + k]) for i in range(len(ws) - k + 1)}

def main_text_of_html(path):
    s = open(path).read()
    m = re.search(r'<main>(.*)</main>', s, re.S)
    if not m: return ''
    t = re.sub(r'<form.*?</form>', ' ', m.group(1), flags=re.S)
    return t

def load_all():
    files = sorted(glob.glob(os.path.join(CDIR, '**', '*.json'), recursive=True))
    out = {}
    for f in files:
        if os.path.basename(f) == 'plan.json': continue
        try: out[f] = json.load(open(f))
        except Exception as e: out[f] = e
    return out

def check(f, d, targets, sh_all, sh_site):
    errs, warns = [], []
    rel = os.path.relpath(f, CDIR)[:-5] + '.html'
    if isinstance(d, Exception):
        return [f'ongeldige JSON: {d}'], []
    if d.get('path') != rel: errs.append(f'path moet "{rel}" zijn')
    plan = PLAN.get(rel)
    if not plan: errs.append('pagina staat niet in plan.json')
    elif d.get('h1') != plan['h1']: errs.append(f'h1 moet exact "{plan["h1"]}" zijn')
    for k in ('title', 'desc', 'eyebrow', 'h1', 'lead', 'answer'):
        if not isinstance(d.get(k), str) or not d.get(k).strip(): errs.append(f'veld {k} ontbreekt')
    if len(d.get('title', '')) > 60: errs.append(f'title te lang ({len(d["title"])} > 60 tekens, zonder " | Zondags")')
    if not 110 <= len(d.get('desc', '')) <= 160: errs.append(f'desc moet 110-160 tekens zijn (nu {len(d.get("desc", ""))})')
    if not 80 <= len(d.get('lead', '')) <= 260: errs.append(f'lead moet 80-260 tekens zijn (nu {len(d.get("lead", ""))})')
    aw = len(words(d.get('answer', '')))
    if not 40 <= aw <= 110: errs.append(f'answer moet 40-110 woorden zijn (nu {aw})')
    if 'Zondags' not in d.get('answer', ''): errs.append('answer moet Zondags bij naam noemen')
    fa = d.get('facts', [])
    if not (isinstance(fa, list) and 4 <= len(fa) <= 6): errs.append('facts: 4 tot 6 korte punten')
    elif any(len(x) > 60 for x in fa): errs.append('facts: elk punt max 60 tekens')
    se = d.get('sections', [])
    if not (isinstance(se, list) and 4 <= len(se) <= 8): errs.append('sections: 4 tot 8 secties')
    for s in se if isinstance(se, list) else []:
        if not s.get('h2') or not isinstance(s.get('p'), list) or not s['p']: errs.append('elke sectie heeft h2 en p[] nodig'); break
    fq = d.get('faq', [])
    if not (isinstance(fq, list) and 4 <= len(fq) <= 7): errs.append('faq: 4 tot 7 vragen')
    for q in fq if isinstance(fq, list) else []:
        if not q.get('q', '').endswith('?'): errs.append(f'faq-vraag eindigt niet op ?: {q.get("q", "")[:50]}')
        if len(words(q.get('a', ''))) < 15: warns.append(f'kort faq-antwoord: {q.get("q", "")[:50]}')
    alltext = ' '.join([d.get('title', ''), d.get('desc', ''), d.get('eyebrow', ''), ' '.join(fa if isinstance(fa, list) else []), text_of(d)])
    for pat, name in BANNED:
        if name is None: continue
        m = re.search(pat, re.sub(r'<[^>]+>', ' ', alltext))
        if m: errs.append(f'verboden: {name} ("{alltext[max(0, m.start() - 30):m.end() + 30]}")' if False else f'verboden: {name} -> "{m.group(0)}"')
    stripped = ALLOWED_TAGS.sub('', alltext)
    if re.search(r'<[^>]+>', stripped): errs.append('niet-toegelaten HTML-tag: ' + re.search(r'<[^>]+>', stripped).group(0))
    links = re.findall(r'<a href="([^"]+)">', alltext)
    if len(links) > MAX_LINKS: errs.append(f'te veel inline links ({len(links)} > {MAX_LINKS})')
    for l in links:
        if l.startswith(('http', '/', '#', '../')) or l not in targets: errs.append(f'link bestaat niet of niet relatief vanaf de root: {l}')
    nums = set(re.findall(r'\b\d[\d.,]*\b', re.sub(r'<[^>]+>', ' ', text_of(d))))
    okn = {'2', '18', '0470', '56', '53', '58', '6', '22', '281.20', '281'} | {p.get('postcode', '') for p in PLAN.values()}
    weird = [n for n in nums if n not in okn]
    if weird: warns.append('getallen (controleer of ze kloppen, verzin geen cijfers): ' + ', '.join(sorted(weird)[:8]))
    w = len(words(text_of(d)))
    if w < MIN_WORDS: errs.append(f'te kort: {w} unieke woorden (minimum {MIN_WORDS})')
    me = sh_all.get(f, set())
    worst, wf = 0, ''
    for g, sg in list(sh_all.items()) + list(sh_site.items()):
        if g == f or not me or not sg: continue
        c = len(me & sg) / min(len(me), len(sg))
        if c > worst: worst, wf = c, g
    if worst > MAX_OVERLAP: errs.append(f'te veel overlap ({worst:.0%}) met {os.path.relpath(wf, ROOT)}: herschrijf met eigen invalshoek en eigen zinnen')
    return errs, warns + [f'woorden {w}, max overlap {worst:.0%}']

if __name__ == '__main__':
    allc = load_all()
    targets = existing_targets()
    sh_all = {f: shingles(words(text_of(d))) for f, d in allc.items() if not isinstance(d, Exception)}
    sh_site = {}
    for f in glob.glob(os.path.join(ROOT, '*', '*.html')) + glob.glob(os.path.join(ROOT, '*.html')):
        r = os.path.relpath(f, ROOT)
        if r.startswith('_tools') or r in PLAN: continue
        sh_site[f] = shingles(words(main_text_of_html(f)))
    sel = [os.path.abspath(a) for a in sys.argv[1:]] or list(allc.keys())
    bad = 0
    for f in sel:
        if f not in allc: print(f'?? {f} niet gevonden'); bad += 1; continue
        e, w = check(f, allc[f], targets, sh_all, sh_site)
        rel = os.path.relpath(f, CDIR)
        if e: bad += 1; print(f'FOUT  {rel}\n   - ' + '\n   - '.join(e) + ('\n   . ' + '\n   . '.join(w) if w else ''))
        else: print(f'OK    {rel}   (' + '; '.join(w) + ')')
    print(f'\n{len(sel) - bad}/{len(sel)} in orde')
    sys.exit(1 if bad else 0)
