"""Premium: bedragen uit de zichtbare tekst van alle pagina's (niet boeken.html, niet de redirect-stubs).
Titels, metas, JSON-LD, llms.txt en chat.js blijven ongemoeid (aparte opvolging).
Gebruik: python3 _tools/premium_deprice.py  (vanuit de site-root)"""
import glob, re, sys, collections
sys.path.insert(0, '_tools'); import premium as P
SKIP = {'boeken.html'}
per = collections.Counter(); files = 0; nodes = 0
for f in sorted(glob.glob('**/*.html', recursive=True)):
    if f in SKIP or f.startswith('_tools'): continue
    s = open(f).read()
    if 'http-equiv="refresh"' in s[:3000]: continue
    n = P.deprice_html(s)
    if n != s:
        b = s.find('<body')
        nodes += sum(1 for m in re.finditer(r'>([^<>]+)<', s[b:]) if P.PRICE.search(m.group(1)) and '<script' not in m.group(1))
        open(f, 'w').write(n); files += 1; per[f.split('/')[0] if '/' in f else '(root)'] += 1
print('bestanden aangepast:', files)
for k, v in per.most_common(): print(f'  {k}: {v}')
