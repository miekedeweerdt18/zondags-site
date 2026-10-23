# -*- coding: utf-8 -*-
"""Premium uitrol (23/10/2026): pass voor alles wat pseo.py NIET genereert (handgeschreven pagina's, llms.txt, chat.js).
Idempotent. Draai daarna pseo.py, dat via write() dezelfde finalize_html() toepast op alle gegenereerde pagina's.
    PYTHONPATH=_tools python3 _tools/premium_finalize.py && PYTHONPATH=_tools python3 _tools/pseo.py
NIET aangeraakt: redirect-stubs, Google-verificatiebestand. (boeken.html is sinds 23/10 een aanvraagformulier zonder prijs; assets/boeken.js wordt niet meer geladen maar blijft staan.)"""
import re, glob, sys
from premium import deprice_text
from premium_regio import finalize_html, regio_text, label, RX

SKIP = {'google051c53e5f6987c1b.html'}  # boeken.html: sinds 23/10 aanvraagformulier zonder prijs, mag mee door de premium-pass
MENU_OLD, MENU_NEW = '>Prijs</a>', '>Ons pakket</a>'   # menu-label naar bedrijven/prijs-poetshulp-voor-bedrijven (URL blijft)

def menu(page):
    return re.sub(r'(<a href="(?:\.\./)*bedrijven/prijs-poetshulp-voor-bedrijven(?:\.html)?"[^>]*)>Prijs</a>', r'\1' + MENU_NEW, page)

def html_files():
    for f in sorted(glob.glob('**/*.html', recursive=True)):
        if f.startswith(('_tools/', 'node_modules/', '.git/')) or f in SKIP: continue
        yield f

# llms.txt en chat.js: weinig regels, dus vaste teksten (geen bedragen, 'regio X')
LLMS_FIX = {
    'Eén pakket: 60 euro per uur excl. btw, geboekt per blok van 3 uur (180 euro excl. btw), extra uren per uur aan dezelfde prijs.':
    'Eén pakket voor alle taken, geboekt per blok van 3 uur, extra uren per uur erbij.',
    '(https://zondags.be/bedrijven/prijs-poetshulp-voor-bedrijven): 60 euro per uur excl. btw, per blok van 3 uur':
    '(https://zondags.be/bedrijven/prijs-poetshulp-voor-bedrijven): één pakket, per blok van 3 uur',
}
CHAT_FIX = {
    "a: 'Eén pakket: 60 euro per uur excl. btw. Je boekt per blok van 3 uur (180 euro excl. btw) en extra uren boek je per uur bij, ook aan 60 euro excl. btw. Je boekt en betaalt online op de boekpagina.'":
    "a: 'Eén pakket voor alle taken. Je boekt per blok van 3 uur en extra uren boek je per uur bij. Je boekt en betaalt online op de boekpagina.'",
    "Onder meer in Kortrijk, Waregem, Harelbeke, Roeselare, Izegem, Menen, Wevelgem, Ieper, Tielt en Oudenaarde.":
    "Onder meer regio Kortrijk, Waregem, Harelbeke, Roeselare, Izegem, Menen, Wevelgem, Ieper, Tielt en Oudenaarde.",
}

def llms(t):
    for a, b in LLMS_FIX.items(): t = t.replace(a, b)
    out = []
    for line in t.split('\n'):
        line = re.sub(r'\[([^\]]+)\]', lambda m: '[' + label(m.group(1)) + ']', line)   # linkteksten = label
        out.append(regio_text(deprice_text(line)))
    return '\n'.join(out)

def chat(t):
    for a, b in CHAT_FIX.items(): t = t.replace(a, b)
    return t

def main():
    n = 0
    for f in html_files():
        s = open(f).read()
        if 'http-equiv="refresh"' in s: continue
        new = finalize_html(menu(s), f)
        if new != s:
            open(f, 'w').write(new); n += 1
    for f, fn in (('llms.txt', llms), ('assets/chat.js', chat)):
        s = open(f).read(); new = fn(s)
        if new != s: open(f, 'w').write(new); n += 1
        left = [m.group(0) for m in RX.finditer(new)]
        if left: print(f, 'nog in-X:', left[:5], file=sys.stderr)
    print('aangepast:', n)

if __name__ == '__main__':
    main()
