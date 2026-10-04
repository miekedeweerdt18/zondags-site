# -*- coding: utf-8 -*-
"""Zet websitecopy om van u-vorm naar je-vorm. Werkt enkel op tekst, niet op tags of code."""
import re

INV = {  # werkwoord vóór 'u' (inversie) -> je-vorm
 'bent':'ben','hebt':'heb','heeft':'heb','wilt':'wil','kunt':'kun','zult':'zul','twijfelt':'twijfel','werkt':'werk',
 'zoekt':'zoek','haalt':'haal','zet':'zet','krijgt':'krijg','onderhoudt':'onderhoud','houdt':'hou','mag':'mag',
 'stelt':'stel','regelt':'regel','pakt':'pak','betaalt':'betaal','doet':'doe','bespreekt':'bespreek','besteedt':'besteed',
 'boekt':'boek','hoeft':'hoef','weet':'weet','laat':'laat','moet':'moet','kan':'kan','komt':'kom','gaat':'ga',
 'vindt':'vind','vult':'vul','vinkt':'vink','geeft':'geef','kiest':'kies','start':'start','wil':'wil','ziet':'zie',
 'leest':'lees','vraagt':'vraag','maakt':'maak','spreekt':'spreek','staat':'sta','blijft':'blijf','wordt':'word','zit':'zit',
}
OBJ_PREV = {'ons','we','wij','bellen','begeleiden','leren','helpen','verwachten','kennen','contacteren','tonen','sturen','geven','vragen','zien','bezorgen'}
PREP_JOU = {'voor','bij','tussen','met','aan','naar','zonder','dan'}

def _cap(src, dst):
    return dst[0].upper()+dst[1:] if src[:1].isupper() else dst

def convert_text(t):
    # uw -> je
    t = re.sub(r'\b(U|u)w\b', lambda m: 'Je' if m.group(1)=='U' else 'je', t)
    t = re.sub(r'\buzelf\b', 'jezelf', t); t = re.sub(r'\bUzelf\b', 'Jezelf', t)
    def rep(m):
        prev, sp, u = m.group(1), m.group(2), m.group(3)
        low = prev.lower()
        if low in PREP_JOU:
            return prev+sp+_cap(u,'jou')
        if low in OBJ_PREV:
            return prev+sp+_cap(u,'je')
        if low in INV:
            return _cap(prev, INV[low])+sp+_cap(u,'je')
        if low == 'dank':
            return prev+sp+'je'
        return prev+sp+_cap(u,'je')
    t = re.sub(r'\b(\w+)(\s+)(u|U)\b(?![\w-])', rep, t)
    # 'U' aan het begin van een zin of tekstblok
    t = re.sub(r'(^\s*|[.?!:>]\s*|\n\s*)U\b(?![\w-])', lambda m: m.group(1)+'Je', t)
    t = re.sub(r'(^|\s)u\b(?![\w-])', lambda m: m.group(1)+'je', t)
    # kleine grammaticale correcties
    t = re.sub(r'\b(j|J)e heeft\b', lambda m: m.group(1)+'e hebt', t)
    t = t.replace('De was hangt. Je niet.','De was hangt. Jij niet.')
    return t

ATTRS = ('content','alt','aria-label','title','placeholder','data-tooltip')
def convert_html(h):
    out=[]; i=0
    for m in re.finditer(r'<[^>]*>', h):
        out.append(convert_text(h[i:m.start()]))
        tag=m.group(0)
        tag=re.sub(r'\b(%s)="([^"]*)"' % '|'.join(ATTRS), lambda a: a.group(1)+'="'+convert_text(a.group(2))+'"', tag)
        out.append(tag); i=m.end()
    out.append(convert_text(h[i:]))
    return ''.join(out)

if __name__=='__main__':
    import sys
    for p in sys.argv[1:]:
        s=open(p).read(); n=convert_html(s) if p.endswith('.html') else convert_text(s)
        if n!=s: open(p,'w').write(n)
