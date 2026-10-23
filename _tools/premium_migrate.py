"""Eenmalige premium-opmaak (23/10/2026) over alle bestaande HTML.
Raakt enkel opmaak aan: preloader, animatiebibliotheken, aparte leads.css, footer-woordmerk, beelden.
Titels, metas, canonicals, JSON-LD, formulieren, links en tekst blijven ongemoeid.
Gebruik: python3 _tools/premium_migrate.py  (vanuit de root van de site)"""
import re, glob, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from premium import pband_html, PB

LOG = collections.Counter()
FOOT_OLD = re.compile(r'<div class="foot__logo" aria-hidden="true"><img src="((?:\.\./)*)assets/img/zondags-logo-paper\.svg" alt="" width="760" height="181"></div>')
def foot_new(pre):
    return (f'<div class="foot__logo"><img src="{pre}assets/img/zondags-logo-paper.svg" alt="" width="150" height="36" aria-hidden="true">'
            '<span class="foot__rule" aria-hidden="true"></span><p class="foot__slogan">Elke dag een beetje <em>zondag.</em></p></div>')
PBAND = re.compile(r'<section class="pband"><img src="((?:\.\./)*)assets/img/(01-poetsen|10-boodschappen)\.webp"[^>]*></section>\n?')
SUBS = [
  ('preloader', re.compile(r'<div class="curtain" aria-hidden="true"><span class="wm">z<i></i>ndags</span></div>\n?'), ''),
  ('gsap', re.compile(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/gsap/[^"]+"></script>\n?'), ''),
  ('lenis', re.compile(r'<script src="https://cdn\.jsdelivr\.net/npm/lenis@[^"]+"></script>\n?'), ''),
  ('leads.css', re.compile(r'<link rel="stylesheet" href="(?:\.\./)*assets/leads\.css">\n?'), ''),
  ('og:image', re.compile(r'(<meta property="og:image" content="https://zondags\.be/assets/img/)01-poetsen\.webp(">)'), r'\1og-image-1200x630.jpg\2'),
]

def migrate(path, s):
    for name, rx, rep in SUBS:
        s, n = rx.subn(rep, s); LOG[name] += n
    s, n = FOOT_OLD.subn(lambda m: foot_new(m.group(1)), s); LOG['footer-logo'] += n
    def pb(m):
        LOG['pband'] += 1
        return pband_html(path, m.group(2)).replace('src="assets/', f'src="{m.group(1)}assets/')
    s = PBAND.sub(pb, s)
    return s

if __name__ == '__main__':
    files = sorted(glob.glob('**/*.html', recursive=True))
    changed = 0
    for f in files:
        if f.startswith(('_tools/', 'node_modules/')): continue
        s = open(f, encoding='utf-8').read(); n = migrate(f, s)
        if n != s: open(f, 'w', encoding='utf-8').write(n); changed += 1
    print('bestanden gewijzigd:', changed); [print(f'  {k}: {v}') for k, v in sorted(LOG.items())]
