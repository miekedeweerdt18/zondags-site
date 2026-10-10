# -*- coding: utf-8 -*-
"""Genereert de pagina's van zondags.be (enkel B2B): pijlerpagina's + unieke pagina's uit _tools/content/**.json,
hubpagina's, redirect-stubs voor verwijderde pagina's en de sitemap.
Gebruik (vanuit de repo-root): PYTHONPATH=_tools python3 _tools/pseo.py"""
import re, json, html, hashlib, os, datetime
from jevorm import convert_html

TODAY=datetime.date.today().isoformat()
BASE='https://zondags.be/'
SHELL=open('aanvraag.html').read()
HEAD=SHELL[:SHELL.index('<main>')]
TAIL=SHELL[SHELL.index('</main>')+len('</main>'):]

def H(s): return html.escape(s, quote=True)
def pick(key, options):
    h=int(hashlib.md5(key.encode()).hexdigest(),16)
    return options[h%len(options)]
def words(t): return len(re.sub('<[^>]+>',' ',t).split())

def shell(depth, path, title, desc, body, ld_list, noindex=False):
    pre='../'*depth
    h=HEAD
    h=re.sub(r'<title>.*?</title>',f'<title>{H(title)}</title>',h)
    h=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{H(desc)}">',h)
    h=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{H(title)}">',h)
    h=re.sub(r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{H(desc)}">',h)
    url=BASE+re.sub(r'(^|/)index$',r'\1',path.replace('.html',''))
    h=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{url}">',h)
    h=re.sub(r'<meta property="og:url" content="[^"]*">',f'<meta property="og:url" content="{url}">',h)
    h=h.replace(' aria-current="page"','')
    extra=''.join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>\n' for x in ld_list)
    if noindex: extra+='<meta name="robots" content="noindex">\n'
    h=h.replace('</head>',extra+'</head>')
    t=TAIL
    page=h+'<main>\n'+body+'</main>\n'+t
    if depth:
        page=re.sub(r'(href|src)="(?!https?:|mailto:|#|data:|\.\./)([^"]+)"',lambda m:f'{m.group(1)}="{pre}{m.group(2)}"',page)
    return page

def crumbs(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(items)]}
def faqld(faq):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}

def faq_html(faq):
    return '<section class="faq wrap"><div class="faq__head"><p class="eyebrow" style="color:var(--muted)">Veelgestelde vragen</p><h2 style="margin-top:18px">Goed om <em class="s">te weten.</em></h2></div><div class="faq__list">'+''.join(f'<details class="qa"><summary>{H(q)}<span aria-hidden="true">+</span></summary><p>{H(a)}</p></details>' for q,a in faq)+'</div></section>\n'

def phero(eyebrow,title,lead,dark=False):
    w=title.split(); k=max(1,len(w)//2)
    l1,l2=' '.join(w[:k]),' '.join(w[k:])
    return f'''<section class="phero{' phero--dark' if dark else ''}">
  <div><p class="eyebrow">{H(eyebrow)}</p><h1 data-split><span class="line">{H(l1)}</span><span class="line"><em class="s">{H(l2)}</em></span></h1></div>
  <p>{H(lead)}</p>
</section>
'''

def article(aside_title, aside_items, sections, cta_href, cta_label):
    secs=''.join(f'<h2>{H(h)}</h2>'+''.join(f'<p>{p}</p>' for p in (ps if isinstance(ps,list) else [ps])) for h,ps in sections)
    lis=''.join(f'<li>{H(i)}</li>' for i in aside_items)
    return f'''<section class="art wrap">
  <aside class="art__aside"><div class="art__card"><p class="eyebrow" style="color:var(--muted)">{H(aside_title)}</p><ul>{lis}</ul><a class="btn btn--zon" href="{cta_href}">{H(cta_label)} <span class="arr">&rarr;</span></a></div></aside>
  <div class="art__body">{secs}</div>
</section>
'''

def photo(img, alt):
    return f'<section class="pband" aria-hidden="true"><img src="assets/img/{img}.webp" alt="" loading="lazy"></section>\n'

def form_b2b(source, gemeente=''):
    return f'''<section class="qform wrap" id="formulier">
  <div><p class="eyebrow" style="color:var(--muted)">Liever eerst praten?</p><h2>Vraag je <em class="s">Zondag aan.</em></h2><p>Wil je meteen starten? <a href="boeken.html">Boek online</a> per blok van 3 uur aan 60 euro per uur exclusief btw. Liever eerst even overleggen? Laat je gegevens achter en we bellen je binnen één werkdag terug.</p></div>
  <form class="form qf" data-quick novalidate action="https://formsubmit.co/mieke@hummingbirds.be" method="POST">
    <input type="hidden" name="_subject" value="Aanvraag bedrijf via zondags.be/{H(source)}">
    <input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="https://zondags.be/bedankt"><input type="hidden" name="Pagina" value="{H(source)}">
    <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="fgrid">
      <div class="f"><label for="q-naam">Naam *</label><input id="q-naam" name="Naam" autocomplete="name" required></div>
      <div class="f"><label for="q-bedrijf">Bedrijf *</label><input id="q-bedrijf" name="Bedrijf" autocomplete="organization" required></div>
      <div class="f"><label for="q-mail">E-mail *</label><input id="q-mail" name="E-mail" type="email" autocomplete="email" required></div>
      <div class="f"><label for="q-gsm">GSM *</label><input id="q-gsm" name="GSM" type="tel" autocomplete="tel" required></div>
      <div class="f f--full"><label for="q-gem">Gemeente</label><input id="q-gem" name="Gemeente" autocomplete="address-level2" value="{H(gemeente)}"></div>
      <div class="f f--full"><label for="q-msg">Waarmee kunnen we helpen? (optioneel)</label><textarea id="q-msg" name="Bericht"></textarea></div>
    </div>
    <p class="err" data-err hidden>Vul je naam, bedrijf, een geldig e-mailadres en je gsm-nummer in.</p>
    <div class="form__foot"><p>Vrijblijvend. We gebruiken je gegevens enkel om je terug te bellen.</p><button class="btn btn--zon" type="submit">Verstuur mijn aanvraag <span class="arr">&rarr;</span></button></div>
  </form>
</section>
'''

def form_job(source, gemeente=''):
    return f'''<section class="qform wrap" id="formulier">
  <div><p class="eyebrow" style="color:var(--muted)">Solliciteer</p><h2>Werk bij <em class="s">Zondags.</em></h2><p>Laat je gegevens achter. Wij bellen je binnen de twee werkdagen.</p></div>
  <form class="form qf" data-quick novalidate action="https://formsubmit.co/mieke@hummingbirds.be" method="POST">
    <input type="hidden" name="_subject" value="Kandidaat via zondags.be/{H(source)}">
    <input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="https://zondags.be/bedankt"><input type="hidden" name="Pagina" value="{H(source)}">
    <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="fgrid">
      <div class="f"><label for="q-naam">Naam *</label><input id="q-naam" name="Naam" autocomplete="name" required></div>
      <div class="f"><label for="q-gsm">Telefoon *</label><input id="q-gsm" name="Telefoon" type="tel" autocomplete="tel" required></div>
      <div class="f"><label for="q-mail">E-mail *</label><input id="q-mail" name="E-mail" type="email" autocomplete="email" required></div>
      <div class="f"><label for="q-gem">Woonplaats</label><input id="q-gem" name="Woonplaats" autocomplete="address-level2" value="{H(gemeente)}"></div>
      <div class="f"><label for="q-st">Statuut</label><select id="q-st" name="Statuut"><option>Kies je statuut</option><option>Student (18 jaar of ouder)</option><option>Werkzoekend</option><option>Bijverdienen naast mijn job</option><option>Deeltijds beschikbaar</option><option>Voltijds beschikbaar</option><option>Anders</option></select></div>
      <div class="f"><label for="q-dagen">Dagen per week</label><select id="q-dagen" name="Dagen per week"><option>Maak een keuze</option><option>1 dag</option><option>2 dagen</option><option>3 dagen</option><option>4 dagen</option><option>5 dagen</option></select></div>
    </div>
    <label class="consent" for="q-ok" style="margin-top:16px"><input type="checkbox" id="q-ok" name="Akkoord" value="Ja" required>Ik ben 18 jaar of ouder en ga ermee akkoord dat Zondags mijn gegevens gebruikt om mij te contacteren.</label>
    <p class="err" data-err hidden>Vul je naam, telefoon en een geldig e-mailadres in en vink het akkoord aan.</p>
    <div class="form__foot"><p>Overdag op weekdagen, vaste klanten, vaste uren.</p><button class="btn btn--zon" type="submit">Verstuur <span class="arr">&rarr;</span></button></div>
  </form>
</section>
'''

def related(title, links):
    lis=''.join(f'<a class="rel__a" href="{u}">{H(t)}<span aria-hidden="true">&rarr;</span></a>' for t,u in links)
    return f'<section class="rel wrap"><p class="eyebrow" style="color:var(--muted)">{H(title)}</p><div class="rel__grid">{lis}</div></section>\n'


# --------- gedeelde inhoudsblokken (enkel B2B) ---------
FISC=("Op de factuur van je bedrijf",["Zondags werkt enkel voor bedrijven en factureert met een gewone dienstenfactuur op naam van je bedrijf. De prijs is 60 euro per uur exclusief btw, geboekt per blok van 3 uur.","Over de fiscale verwerking beslist je accountant. Hij bevestigt wat voor jouw bedrijf geldt."])
def dag(key):
    return ('Een dag als Zondag',[pick(key,[
      'Je begint om half negen bij een kantoor in de buurt: bureaus, vergaderzaal, keuken en sanitair. Na de middag ga je naar een praktijk of winkel voor de vaste beurt. Twee vaste adressen, elke week op dezelfde dag.',
      'Op dinsdag en donderdag werk je bij hetzelfde bedrijf: poetsen, de post sorteren en de keuken aanvullen. Op vrijdagvoormiddag onderhoud je een kleine winkel. Altijd overdag, nooit in het weekend.',
      'Je voormiddag gaat naar een kantoor: werkplekken, vergaderzaal en refter. In de namiddag doe je de administratie en de boodschappen voor een drukke bedrijfsleider. Je rooster ligt vast.']),
      'Je rooster ligt vast. Je weet op voorhand waar je wanneer werkt.'])
VERWACHT=('Wat we van je verwachten',['Betrouwbaarheid, discretie en zorg voor andermans zaak. Je bent 18 jaar of ouder en spreekt voldoende Nederlands om afspraken met klanten te maken. Ervaring is mooi meegenomen, maar niet nodig: wij leggen de werking uit en starten rustig op.'])
BEGELEID=('Hoe we je begeleiden',['Je staat er niet alleen voor. Bij de start gaan we samen langs bij de klant, zodat iedereen weet wat er verwacht wordt. Elke klant heeft een zondagsplan met de taken, de uren en de afspraken. Heb je vragen, dan kun je ons altijd bereiken.'])
NEUTRAL_IMG=['01-poetsen','10-boodschappen']

def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower().replace('é','e').replace('ë','e')).strip('-')

pages=[]   # (path, title, wordcount, group)
def write(path, content, title, group):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    content=convert_html(content)
    open(path,'w').write(content)
    m=re.search(r'<main>(.*)</main>',content,re.S)
    pages.append((path,title,words(m.group(1)),group))

# unieke B2B-pagina's: plan + eigen tekst per pagina (zie _tools/README.md)
CPLAN=json.load(open('_tools/content/plan.json'))
CONTENT={}
for _P in CPLAN:
    _f='_tools/content/'+_P['path'][:-5]+'.json'
    if os.path.exists(_f): CONTENT[_P['path']]=(_P,json.load(open(_f)))
def cexists(p): return p in CONTENT

# ---------------- PIJLERPAGINA'S (GEO: antwoorden voor ChatGPT, Perplexity, Gemini) ----------------
from geo_pillars import PILLARS
ORG_REF={"@id":BASE+"#org"}
AREAS=[{"@type":"AdministrativeArea","name":"West-Vlaanderen"},{"@type":"AdministrativeArea","name":"Oost-Vlaanderen"}]
for P in PILLARS:
    path=P['path']; kind=P['kind']; depth=path.count('/')
    flow='werk' if kind=='job' else 'hulp'
    secs=list(P['sections'])
    has_fisc=any('fisca' in h.lower() or 'vennootschap' in h.lower() for h,_ in secs)
    if kind=='job': secs+=[dag(path), VERWACHT, BEGELEID]
    elif kind=='b2b' and not has_fisc: secs+=[FISC]
    art=article('In het kort',P['facts'],secs,'boeken.html' if kind!='job' else '#formulier','Boek je Zondag online' if kind!='job' else 'Meld je aan via de chat')
    if kind=='job': art=art.replace('class="btn btn--zon" href="#formulier"','class="btn btn--zon" href="#formulier" data-chat="%s"'%flow,1)
    body=phero(P['eyebrow'],P['h1'],P['lead'])+art+photo(P['img'],'')+faq_html(P['faq'])+(form_job(path) if kind=='job' else form_b2b(path))+related('Verder lezen',P['related'])
    clean=re.sub(r'(^|/)index$',r'\1',path.replace('.html',''))
    if kind=='job':
        cr=crumbs([('Home',''),('Werken bij Zondags','werken/'),(P['h1'],clean)])
        jp={"@context":"https://schema.org","@type":"JobPosting","title":P['h1']+' bij Zondags',"description":'<p>'+H(P['lead'])+'</p><p>'+H(' '.join(P['facts']))+'.</p>',
            "datePosted":TODAY,"validThrough":(datetime.date.today()+datetime.timedelta(days=90)).isoformat(),"employmentType":P.get('emp',['PART_TIME']),
            "hiringOrganization":{"@type":"Organization","name":"Zondags","sameAs":BASE,"url":BASE},"directApply":True,"workHours":"Overdag op weekdagen",
            "jobLocation":[{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":"Kortrijk","postalCode":"8500","addressRegion":"West-Vlaanderen","addressCountry":"BE"}},
                           {"@type":"Place","address":{"@type":"PostalAddress","addressLocality":"Oudenaarde","postalCode":"9700","addressRegion":"Oost-Vlaanderen","addressCountry":"BE"}}]}
        ld=[cr,faqld(P['faq']),jp]; grp='jobs'
    elif kind=='about':
        ld=[crumbs([('Home',''),('Over Zondags',clean)]),faqld(P['faq']),{"@context":"https://schema.org","@type":"AboutPage","name":P['h1'],"url":BASE+clean,"about":ORG_REF,"inLanguage":"nl-BE"}]; grp='over'
    else:
        items=[('Home',''),('Voor bedrijven','bedrijven/')]+([] if clean=='bedrijven/' else [(P['h1'],clean)])
        ld=[crumbs(items),faqld(P['faq']),{"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":P['lead'],"serviceType":P['eyebrow'],
            "provider":{"@type":"LocalBusiness","@id":BASE+"#org","name":"Zondags","url":BASE},"areaServed":AREAS,"audience":{"@type":"BusinessAudience","name":"Bedrijven, ondernemers en vrije beroepen"}}]; grp='bedrijven'
    write(path, shell(depth,path,P['title'],P['desc'],body,ld), P['h1'], grp)
PILLAR_JOBS=[(P['h1'],P['path']) for P in PILLARS if P['kind']=='job']

# ---------------- UNIEKE B2B-PAGINA'S (eigen tekst per pagina uit _tools/content/**.json) ----------------
def art2(aside_title, aside_items, sections, cta_label, flow='hulp'):
    def para(x): return x if x.lstrip().startswith('<ul') else f'<p>{x}</p>'
    secs=''.join(f'<h2>{H(h)}</h2>'+''.join(para(p) for p in ps) for h,ps in sections)
    lis=''.join(f'<li>{H(i)}</li>' for i in aside_items)
    return f'''<section class="art wrap">
  <aside class="art__aside"><div class="art__card"><p class="eyebrow" style="color:var(--muted)">{H(aside_title)}</p><ul>{lis}</ul><a class="btn btn--zon" href="{'boeken.html' if flow=='hulp' else '#formulier'}"{'' if flow=='hulp' else ' data-chat="'+flow+'"'}>{H(cta_label)} <span class="arr">&rarr;</span></a></div></aside>
  <div class="art__body">{secs}</div>
</section>
'''
def plain(t): return html.unescape(re.sub(r'<[^>]+>','',t))
STREEK_PAGE={'regio Kortrijk':'regio-kortrijk','regio Roeselare':'regio-roeselare','regio Brugge':'regio-brugge','regio Gent':'regio-gent',
             'Leiestreek':'leiestreek','Westhoek':'westhoek','Vlaamse Ardennen':'vlaamse-ardennen','regio Tielt':'regio-tielt'}
SERV={
 'schoonmaak-kantoor':('Schoonmaakhulp voor kantoren','bedrijven/poetshulp-voor-bedrijven.html','vragen/hoe-vaak-kantoor-poetsen.html'),
 'schoonmaak-praktijk':('Schoonmaakhulp voor praktijken','bedrijven/poetshulp-voor-bedrijven.html','vragen/hygiene-afspraken-praktijk.html'),
 'schoonmaak-winkel':('Schoonmaakhulp voor winkels','bedrijven/poetshulp-voor-bedrijven.html','vragen/schoonmaakplan-winkel-maken.html'),
}
SERV_LABEL={'schoonmaak-kantoor':'Schoonmaakhulp voor kantoren','schoonmaak-praktijk':'Schoonmaakhulp voor praktijken','schoonmaak-winkel':'Schoonmaakhulp voor winkels'}
GROUP_ORDER={g:[P for P in CPLAN if P['group']==g] for g in ('poetshulp','regio','sectoren','vragen')}
def siblings(P, n):
    lst=[Q for Q in CPLAN if Q['kind']==P['kind'] and Q['path']!=P['path'] and cexists(Q['path'])]
    if not lst: return []
    i=[Q['path'] for Q in CPLAN if Q['kind']==P['kind']].index(P['path'])
    return (lst[i:]+lst[:i])[:n]
def place_area(P):
    return {"@type":"City","name":P['place'],"containedInPlace":{"@type":"AdministrativeArea","name":P.get('provincie','West-Vlaanderen')}}

NEW_PAGES=[]
for idx,(path,(P,C)) in enumerate(CONTENT.items()):
    kind=P['kind']; sp=path.split('/')[-1][:-5]
    secs=[('Het korte antwoord',[C['answer']])]+[(s['h2'],s['p']) for s in C['sections']]
    faq=[(q['q'],q['a']) for q in C['faq']]
    rel=[]; extra_html=''; ld_main=None; gemeente=''; erv=''; img='01-poetsen'
    if kind=='stad':
        gemeente=P['place']; img=pick(path,NEUTRAL_IMG)
        reg=STREEK_PAGE.get(P['streek']); prov='west-vlaanderen' if P['provincie']=='West-Vlaanderen' else 'oost-vlaanderen'
        if reg: rel.append((f'Poetshulp in {P["streek"].replace("regio ","de regio ") if P["streek"].startswith("regio") else "de "+P["streek"]}',f'poetshulp/{reg}.html'))
        rel.append((f'Poetshulp in {P["provincie"]}',f'poetshulp/{prov}.html'))
        for b in P['in_de_buurt']:
            q=f'poetshulp/{slug(b)}.html'
            if cexists(q) and len(rel)<4: rel.append((f'Poetshulp in {b}',q))
        for key in ('schoonmaak-kantoor','schoonmaak-praktijk','schoonmaak-winkel'):
            q=f'regio/{key}-{sp}.html'
            if cexists(q): rel.append((f'{SERV_LABEL.get(key,SERV[key][0])} in {P["place"]}',q))
        rel.append(('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html'))
        crumbs_items=[('Home',''),('Poetshulp per gemeente','poetshulp/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":"Poetshulp voor bedrijven",
                 "provider":{"@id":BASE+"#org"},"areaServed":place_area(P),"audience":{"@type":"BusinessAudience","name":"Bedrijven, ondernemers en vrije beroepen"}}
    elif kind=='regio':
        img=pick(path,NEUTRAL_IMG)
        mem=[(m,f'poetshulp/{slug(m)}.html') for m in P['members'] if cexists(f'poetshulp/{slug(m)}.html')]
        lis=''.join(f'<a class="rel__a" href="{u}">Poetshulp in {H(m)}<span aria-hidden="true">&rarr;</span></a>' for m,u in sorted(mem))
        extra_html=f'<section class="rel wrap"><p class="eyebrow" style="color:var(--muted)">Poetshulp per gemeente in {H(P["regio"])}</p><div class="rel__grid rel__grid--hub">{lis}</div></section>\n'
        rel=[(f'Poetshulp in {Q["h1"].split(" in ",1)[1]}',Q['path']) for Q in siblings(P,5)]+[('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html')]
        crumbs_items=[('Home',''),('Poetshulp per gemeente','poetshulp/'),(P['h1'],path[:-5])]
        area={"@type":"AdministrativeArea","name":P['regio'].replace('provincie ','')}
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":"Poetshulp voor bedrijven",
                 "provider":{"@id":BASE+"#org"},"areaServed":[area]+[{"@type":"City","name":m} for m,_ in mem][:40],"audience":{"@type":"BusinessAudience","name":"Bedrijven, ondernemers en vrije beroepen"}}
    elif kind=='dienst-stad':
        key=P['dienst']; label,pillar,vraag=SERV[key]; gemeente=P['place']; img=pick(path,NEUTRAL_IMG)
        if cexists(f'poetshulp/{slug(P["place"])}.html'): rel.append((f'Poetshulp voor bedrijven in {P["place"]}',f'poetshulp/{slug(P["place"])}.html'))
        _sib=[]
        for k2 in SERV:
            q=f'regio/{k2}-{slug(P["place"])}.html'
            if k2!=key and cexists(q): _sib.append((f'{SERV_LABEL.get(k2,SERV[k2][0])} in {P["place"]}',q))
        rel+=_sib[:4]
        rel.append((f'{label} voor ondernemers',pillar))
        if cexists(vraag): rel.append((CONTENT[vraag][0]['h1'],vraag))
        crumbs_items=[('Home',''),('Poetshulp per gemeente','poetshulp/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":label,
                 "provider":{"@id":BASE+"#org"},"areaServed":place_area(P),"audience":{"@type":"BusinessAudience","name":"Ondernemers, zaakvoerders en vrije beroepen"}}
    elif kind=='ruimte-stad':
        img=pick(path,NEUTRAL_IMG); gemeente=P['place']
        _pil=f'sectoren/{P["ruimte"]}.html'
        if cexists(_pil): rel.append((CONTENT[_pil][0]['h1'],_pil))
        rel+=[(Q['h1'],Q['path']) for Q in CPLAN if Q['kind']=='ruimte-stad' and Q['place']==P['place'] and Q['path']!=path and cexists(Q['path'])][:3]
        rel+=[(Q['h1'],Q['path']) for Q in CPLAN if Q['kind']=='ruimte-stad' and Q['ruimte']==P['ruimte'] and Q['place'] in P['in_de_buurt'] and cexists(Q['path'])][:2]
        if cexists(f'poetshulp/{slug(P["place"])}.html'): rel.append((f'Poetshulp voor bedrijven in {P["place"]}',f'poetshulp/{slug(P["place"])}.html'))
        crumbs_items=[('Home',''),('Per type bedrijf','sectoren/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":P['h1'],
                 "provider":{"@id":BASE+"#org"},"areaServed":place_area(P),"audience":{"@type":"BusinessAudience","name":"Bedrijven, ondernemers en vrije beroepen"}}
    elif kind=='sector-dienst':
        img=pick(path,NEUTRAL_IMG)
        _par=f'sectoren/{P["sector"]}.html'
        if cexists(_par): rel.append((CONTENT[_par][0]['h1'],_par))
        rel+=[(Q['h1'],Q['path']) for Q in CPLAN if Q['kind']=='sector-dienst' and Q['sector']==P['sector'] and Q['path']!=path and cexists(Q['path'])]
        rel+=[('Poetshulp voor bedrijven in Kortrijk','poetshulp/kortrijk.html'),('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html')]
        crumbs_items=[('Home',''),('Per type bedrijf','sectoren/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":P['h1'],
                 "provider":{"@id":BASE+"#org"},"areaServed":AREAS,"audience":{"@type":"BusinessAudience","name":"Bedrijven, ondernemers en vrije beroepen"}}
    elif kind in ('sector','ruimte','situatie','gids'):
        img=pick(path,NEUTRAL_IMG)
        rel=[(Q['h1'],Q['path']) for Q in siblings(P,4)]+[('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html'),('Poetshulp per gemeente','poetshulp/')]
        crumbs_items=[('Home',''),('Per type bedrijf','sectoren/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":P['h1'],
                 "provider":{"@id":BASE+"#org"},"areaServed":AREAS,"audience":{"@type":"BusinessAudience","name":"Bedrijven, ondernemers en vrije beroepen"}}
    elif kind=='kandidaat':
        gemeente=P['place']; img=pick(path,NEUTRAL_IMG)
        K_LABEL={'studentenjob':'Studentenjob','flexi-job':'Flexi-job of bijverdienen','vaste-job-overdag':'Vaste job overdag'}
        K_PILLAR={'studentenjob':('Studentenjob met flexibele uren','jobs/studentenjob-flexibele-uren.html'),
                  'flexi-job':('Flexi-job met flexibele uren','jobs/flexi-job-flexibele-uren.html'),
                  'vaste-job-overdag':('Vaste job met flexibele uren','jobs/vaste-job-flexibele-uren.html')}
        for k2 in ('studentenjob','flexi-job','vaste-job-overdag'):
            q=f'werken/{k2}-{slug(P["place"])}.html'
            if k2!=P['soort_job'] and cexists(q): rel.append((f'{K_LABEL[k2]} in {P["place"]}',q))
        for b in P['in_de_buurt']:
            q=f'werken/{P["soort_job"]}-{slug(b)}.html'
            if cexists(q) and len(rel)<5: rel.append((f'{K_LABEL[P["soort_job"]]} in {b}',q))
        rel.append(K_PILLAR[P['soort_job']]); rel.append(('Zondag worden','zondag-worden.html'))
        crumbs_items=[('Home',''),('Werken bij Zondags','werken/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"JobPosting","title":P['h1'],
                 "description":f"<p>{H(C['lead'])}</p><p>{H(C['answer'])}</p>","datePosted":TODAY,
                 "validThrough":(datetime.date.today()+datetime.timedelta(days=90)).isoformat(),"employmentType":P['employment'],
                 "hiringOrganization":{"@type":"Organization","@id":BASE+"#org","name":"Zondags","sameAs":BASE},
                 "jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":P['place'],"postalCode":P['postcode'],"addressRegion":P['provincie'],"addressCountry":"BE"}},
                 "industry":"Zakelijke dienstverlening","directApply":True}
    else:  # vraag
        img=pick(path,NEUTRAL_IMG)
        rel=[(Q['h1'],Q['path']) for Q in siblings(P,5)]+[('Voor bedrijven','bedrijven/'),('Online boeken','boeken.html')]
        crumbs_items=[('Home',''),('Vragen van bedrijven','vragen/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Article","headline":P['h1'][:110],"description":C['lead'],"inLanguage":"nl-BE",
                 "datePublished":TODAY,"dateModified":TODAY,"mainEntityOfPage":BASE+path[:-5],
                 "author":{"@id":BASE+"#org"},"publisher":{"@id":BASE+"#org"},"about":{"@type":"Thing","name":"Poetshulp en hulp voor bedrijven"}}
    isk=kind=='kandidaat'
    body=(phero(C['eyebrow'],P['h1'],C['lead'])+art2('In het kort',C['facts'],secs,'Solliciteer als Zondag' if isk else 'Boek je Zondag online','werk' if isk else 'hulp')+extra_html
          +photo(img,'')+erv+faq_html([(q,plain(a)) for q,a in faq]).replace('Goed om <em class="s">te weten.</em>','Vragen en <em class="s">antwoorden.</em>')
          +(form_job(path,gemeente) if isk else form_b2b(path,gemeente))+related('Verder lezen',rel[:8]))
    ld=[crumbs(crumbs_items),faqld([(q,plain(a)) for q,a in faq]),ld_main]
    write(path, shell(1,path,f"{C['title']} | Zondags",C['desc'],body,ld), P['h1'], P['group'])
    NEW_PAGES.append((path,P,C))

# hubs voor de nieuwe groepen
def hub_list(items):
    return '<div class="rel__grid rel__grid--hub">'+''.join(f'<a class="rel__a" href="{u}">{H(t)}<span aria-hidden="true">&rarr;</span></a>' for t,u in items)+'</div>'
def hub_page(folder, eyebrow, h1, lead, intro, blocks, faq, job=False):
    secs=''.join(f'<section class="rel wrap" style="padding-top:0"><p class="eyebrow" style="color:var(--muted)">{H(t)}</p>{hub_list(items)}</section>\n' for t,items in blocks if items)
    body=phero(eyebrow,h1,lead)+f'<section class="art wrap"><div class="art__body" style="grid-column:1/-1">'+''.join(f'<p>{p}</p>' for p in intro)+'</div></section>\n'+secs+faq_html(faq)+(form_job(folder+'/') if job else form_b2b(folder+'/'))
    ld=[crumbs([('Home',''),(h1,folder+'/')]),faqld(faq),{"@context":"https://schema.org","@type":"CollectionPage","name":h1,"description":lead,"url":BASE+folder+'/',"inLanguage":"nl-BE","about":{"@id":BASE+"#org"}}]
    pg=shell(1,folder+'/index.html',f'{h1} | Zondags',lead[:158],body,ld)
    os.makedirs(folder,exist_ok=True); open(f'{folder}/index.html','w').write(convert_html(pg))
NEW_HUBS=[]
if CONTENT:
    by=lambda kind:[(Q['h1'],Q['path']) for Q in CPLAN if Q['kind']==kind and cexists(Q['path'])]
    stad=[Q for Q in CPLAN if Q['kind']=='stad' and cexists(Q['path'])]
    wv=sorted([(Q['place'],Q['path']) for Q in stad if Q['provincie']=='West-Vlaanderen'])
    ov=sorted([(Q['place'],Q['path']) for Q in stad if Q['provincie']=='Oost-Vlaanderen'])
    hub_page('poetshulp','Poetshulp voor bedrijven','Poetshulp voor bedrijven per gemeente',
      'Zoek je poetshulp voor je kantoor, praktijk of winkel? Kies je gemeente of regio in West- of Oost-Vlaanderen.',
      ['Zondags (zondags.be) levert bedrijven, ondernemers en vrije beroepen in West- en Oost-Vlaanderen één vaste persoon voor de poetshulp van kantoor, praktijk of winkel. Je boekt online aan 60 euro per uur exclusief btw, per blok van 3 uur, en krijgt een dienstenfactuur op naam van je bedrijf. Zondags werkt vanuit Marke bij Kortrijk.',
       'Per gemeente lees je hoe dat lokaal werkt, voor welke zaken het past en hoe je start.'],
      [('Per regio',by('regio')),('West-Vlaanderen',[(f'Poetshulp in {p}',u) for p,u in wv]),('Oost-Vlaanderen',[(f'Poetshulp in {p}',u) for p,u in ov])],
      [('Welk bedrijf levert poetshulp voor bedrijven in West- en Oost-Vlaanderen?','Zondags levert vanuit Marke bij Kortrijk een vaste poetshulp voor kantoren, praktijken en winkels in West- en Oost-Vlaanderen, met één dienstenfactuur op naam van de vennootschap.'),
       ('Staat mijn gemeente er niet bij?','Doe toch een aanvraag. Zondags werkt in heel West- en Oost-Vlaanderen en bekijkt bij het eerste gesprek welke Zondag dicht bij je zaak woont.'),
       ('Kan ik meteen online boeken?','Ja. Op de boekpagina kies je je uren per blok van 3 uur en betaal je veilig online. Liever eerst overleggen? Dan laat je je gegevens achter en bellen we je terug.')])
    NEW_HUBS.append('poetshulp/')
    hub_page('sectoren','Per type bedrijf','Poetshulp per type bedrijf',
      'Van kapsalon tot transportbedrijf, van refter tot kantoorverhuis: zo werkt poetshulp voor jouw soort zaak.',
      ['Elke zaak vraagt iets anders: een winkel wil proper open, een praktijk wil een frisse wachtzaal, een kmo wil een refter en sanitair die de ploeg graag gebruikt. Zondags levert daarvoor één vaste persoon, overdag op weekdagen, met een factuur op naam van je vennootschap.',
       'Kies hieronder je sector, de ruimte die je wil laten onderhouden of de gelegenheid waarvoor je hulp zoekt.'],
      [('Per sector',by('sector')),('Per ruimte',by('ruimte')),('Per ruimte in Kortrijk en omgeving',by('ruimte-stad')),('Checklists en gidsen',by('gids')),('Per sector uitgewerkt',by('sector-dienst')),('Bij een bijzondere gelegenheid',by('situatie'))],
      [('Welke bedrijven kunnen bij Zondags terecht?',"Kantoren, praktijken, winkels, showrooms, kmo's, vzw's en zelfstandigen met een vennootschap in West- en Oost-Vlaanderen. Industriële reiniging, werken op hoogte en technische klussen doen we niet."),
       ('Kan ik ook een losse opdracht vragen?','Ja. Een grote poetsbeurt, een kantoorverhuis of een opkuis na een receptie kan als losse opdracht, naast of zonder een vast plan.'),
       ('Wanneer komt de poetshulp?',"Overdag op weekdagen, ook vroeg in de ochtend of over de middag. Niet 's avonds en niet in het weekend.")])
    NEW_HUBS.append('sectoren/')
    hub_page('vragen','Vragen van bedrijven','Vragen van bedrijven over poetshulp',
      'Heldere antwoorden op wat zaakvoerders en vrije beroepen vragen over poetshulp, administratie en hulp voor hun zaak.',
      ["Hoe vaak laat je een kantoor poetsen, wat bepaalt de prijs, kan het via je vennootschap en wat als je poetshulp ziek is? Op deze pagina's vind je per vraag een kort antwoord en daarna de nuance.",
       'Gaat het over fiscaliteit, dan leggen we de algemene lijnen uit. Je accountant bevestigt altijd wat voor jouw situatie geldt.'],
      [('Alle vragen',by('vraag'))],
      [('Geeft Zondags fiscaal advies?','Nee. Zondags legt de algemene werking uit en levert een duidelijke dienstenfactuur. Je accountant bevestigt de fiscale verwerking voor je eigen situatie.'),
       ('Hoe stel ik een vraag die hier niet staat?','Via de chat op de site, telefonisch of via WhatsApp op 0470 56 53 58, elke dag van 6 tot 22 uur, of via hello@zondags.be.')])
    NEW_HUBS.append('vragen/')
    kand=lambda k:[(f"{Q['place']}",Q['path']) for Q in CPLAN if Q['kind']=='kandidaat' and Q['soort_job']==k and cexists(Q['path'])]
    if kand('studentenjob') or kand('flexi-job') or kand('vaste-job-overdag'):
        hub_page('werken','Werken bij Zondags','Werken bij Zondags per gemeente',
          'Studentenjob, flexi-job of bijverdienen, of een vaste job overdag zonder weekends: kies je gemeente in West- of Oost-Vlaanderen.',
          ['Zondags (zondags.be) zoekt studenten vanaf 18 jaar, mensen die willen bijverdienen en mensen die een vaste job zoeken. Je werkt overdag op weekdagen bij vaste klanten in de buurt: bedrijven, praktijken en winkels. Je bent in dienst van Zondags en je kiest mee je dagen en uren.',
           'Per gemeente lees je hoe dat lokaal werkt. Welk statuut voor jou past, bekijken we samen in een eerste gesprek.'],
          [('Start hier',[(t,u) for t,u in PILLAR_JOBS]),('Studentenjob met flexibele uren',[(f'Studentenjob in {p}',u) for p,u in sorted(kand('studentenjob'))]),
           ('Flexi-job of bijverdienen',[(f'Bijverdienen in {p}',u) for p,u in sorted(kand('flexi-job'))]),
           ('Vaste job overdag zonder weekends',[(f'Vaste job in {p}',u) for p,u in sorted(kand('vaste-job-overdag'))])],
          [('Moet ik in het weekend of \'s avonds werken?','Nee. Bij Zondags werk je overdag op weekdagen. Vroeg in de ochtend of over de middag kan, avonden en weekends niet.'),
           ('Kan ik bij Zondags werken als flexi-jobber?','Dat hangt af van je eigen situatie. In het eerste gesprek bekijken we samen welk statuut voor jou mogelijk is. Past een flexi-job niet, dan zoeken we een ander statuut dat wel past.'),
           ('Vanaf welke leeftijd kan ik bij Zondags werken?','Vanaf 18 jaar. Ervaring of een diploma is niet nodig.'),
           ('Hoe solliciteer ik?','Via het formulier of de chat op de site, of via WhatsApp op 0470 56 53 58. We bellen je binnen de twee werkdagen terug voor een kort gesprek.')],
          job=True)
        NEW_HUBS.append('werken/')

# ---------------- REDIRECT-STUBS voor verwijderde pagina's ----------------
REDIR=json.load(open('_tools/redirects.json'))
def stub(old, target):
    url=BASE+re.sub(r'(^|/)index$',r'\1',target.replace('.html','')) if target else BASE
    os.makedirs(os.path.dirname(old) or '.', exist_ok=True)
    open(old,'w').write(f'''<!doctype html>
<html lang="nl-BE"><head><meta charset="utf-8"><title>Zondags</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}"><script>location.replace("{url}")</script></head>
<body><p>Deze pagina is verhuisd naar <a href="{url}">{url}</a>.</p></body></html>
''')
for old,target in REDIR.items(): stub(old,target)

# ---------------- SITEMAP ----------------
core=['','wat-we-doen','hoe-het-werkt','boeken','zondag-worden','aanvraag']+NEW_HUBS
allu=core+[re.sub(r'(^|/)index$',r'\1',p[0].replace('.html','')) for p in pages]
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in allu)+'</urlset>\n')
json.dump([{'path':p[0],'title':p[1],'words':p[2],'group':p[3]} for p in pages],open('_tools/pages.json','w'),ensure_ascii=False,indent=0)
wc=[p[2] for p in pages]
print("pagina's:",len(pages),'min woorden:',min(wc),'gem:',sum(wc)//len(wc),'stubs:',len(REDIR))
from collections import Counter; print(Counter(p[3] for p in pages))

