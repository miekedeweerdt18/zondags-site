# -*- coding: utf-8 -*-
"""Genereert de SEO/GEO-contentpagina's van zondags.be.
Gebruik: python3 pseo.py   (leest pseo_data.py, schrijft mappen + hubpagina's + sitemap)"""
import re, json, html, hashlib, os, datetime
from jevorm import convert_html
from pseo_data import BEROEPEN, DIENSTEN, GIDSEN, JOBS, PLAATSEN

GIDSEN = GIDSEN + [
("sleutel-en-vertrouwen","Uw sleutel aan uw Zondag: zo werkt het","Iemand uw sleutel geven vraagt vertrouwen. Zo zorgen wij dat dat vertrouwen terecht is.",[
 ("Gescreend en in dienst","Elke Zondag is door ons gescreend en in dienst van Zondags. U werkt niet met een onbekende zelfstandige."),
 ("Altijd dezelfde persoon","Omdat steeds dezelfde Zondag komt, weet u wie er binnenkomt en wanneer."),
 ("Duidelijke afspraken","In uw zondagsplan leggen we vast waar de sleutel ligt, welke ruimtes aan bod komen en wat u liever niet heeft.")],
 [("Moet ik thuis zijn?","Nee, dat hoeft niet. We spreken het af in uw zondagsplan."),("Wat met een alarm?","Dat regelen we samen tijdens de intake.")]),
]

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
  <div><p class="eyebrow" style="color:var(--muted)">Vrijblijvend</p><h2>Vraag uw <em class="s">Zondag aan.</em></h2><p>Binnen één werkdag belt een van ons u persoonlijk terug met een voorstel op maat. De eerste 2 uur zijn gratis, om kennis te maken.</p></div>
  <form class="form qf" data-quick novalidate action="https://formsubmit.co/mieke@hummingbirds.be" method="POST">
    <input type="hidden" name="_subject" value="Aanvraag bedrijf via zondags.be/{H(source)}">
    <input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="https://zondags.be/bedankt"><input type="hidden" name="Pagina" value="{H(source)}">
    <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="fgrid">
      <div class="f"><label for="q-naam">Naam *</label><input id="q-naam" name="Naam" autocomplete="name" required></div>
      <div class="f"><label for="q-bedrijf">Bedrijf</label><input id="q-bedrijf" name="Bedrijf" autocomplete="organization"></div>
      <div class="f"><label for="q-mail">E-mail *</label><input id="q-mail" name="E-mail" type="email" autocomplete="email" required></div>
      <div class="f"><label for="q-gsm">GSM *</label><input id="q-gsm" name="GSM" type="tel" autocomplete="tel" required></div>
      <div class="f f--full"><label for="q-gem">Gemeente</label><input id="q-gem" name="Gemeente" autocomplete="address-level2" value="{H(gemeente)}"></div>
      <div class="f f--full"><label for="q-msg">Waarmee kunnen we helpen? (optioneel)</label><textarea id="q-msg" name="Bericht"></textarea></div>
    </div>
    <p class="err" data-err hidden>Vul uw naam, een geldig e-mailadres en uw gsm-nummer in.</p>
    <div class="form__foot"><p>Vrijblijvend. We gebruiken uw gegevens enkel om u terug te bellen.</p><button class="btn btn--zon" type="submit">Verstuur mijn aanvraag <span class="arr">&rarr;</span></button></div>
  </form>
</section>
'''

def form_job(source, gemeente=''):
    return f'''<section class="qform wrap" id="formulier">
  <div><p class="eyebrow" style="color:var(--muted)">Solliciteer</p><h2>Word iemands <em class="s">Zondag.</em></h2><p>Laat uw gegevens achter. Wij bellen u binnen de twee werkdagen.</p></div>
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
      <div class="f"><label for="q-st">Statuut</label><select id="q-st" name="Statuut"><option>Kies uw statuut</option><option>Student (18 jaar of ouder)</option><option>Werkzoekend</option><option>Bijverdienen naast mijn job (flexi)</option><option>Deeltijds beschikbaar</option><option>Voltijds beschikbaar</option><option>Anders</option></select></div>
      <div class="f"><label for="q-dagen">Dagen per week</label><select id="q-dagen" name="Dagen per week"><option>Maak een keuze</option><option>1 dag</option><option>2 dagen</option><option>3 dagen</option><option>4 dagen</option><option>5 dagen</option></select></div>
    </div>
    <label class="consent" for="q-ok" style="margin-top:16px"><input type="checkbox" id="q-ok" name="Akkoord" value="Ja" required>Ik ben 18 jaar of ouder en ga ermee akkoord dat Zondags mijn gegevens gebruikt om mij te contacteren.</label>
    <p class="err" data-err hidden>Vul uw naam, telefoon en een geldig e-mailadres in en vink het akkoord aan.</p>
    <div class="form__foot"><p>Vast rooster, geen avonden, geen weekends.</p><button class="btn btn--zon" type="submit">Verstuur <span class="arr">&rarr;</span></button></div>
  </form>
</section>
'''

def related(title, links):
    lis=''.join(f'<a class="rel__a" href="{u}">{H(t)}<span aria-hidden="true">&rarr;</span></a>' for t,u in links)
    return f'<section class="rel wrap"><p class="eyebrow" style="color:var(--muted)">{H(title)}</p><div class="rel__grid">{lis}</div></section>\n'

# --------- gedeelde inhoudsblokken (variatie per pagina) ---------
STAPPEN=[("Hoe het werkt",["<b>1. U doet uw aanvraag.</b> In twee minuten laat u weten wat u nodig hebt. Binnen één werkdag belt een van ons u persoonlijk terug.","<b>2. Wij komen langs voor de intake.</b> We bekijken uw woning of kantoor en leggen samen uw zondagsplan vast: wat er gebeurt, wanneer, en hoe u het graag heeft.","<b>3. Uw Zondag begint.</b> Vanaf de eerste week komt dezelfde persoon op hetzelfde moment. U hoeft niets meer te regelen."])]
FISC=("Geboekt op uw vennootschap",["Een vennootschap kan geen dienstencheques kopen; die zijn voorbehouden aan particulieren. Zondags werkt daarom met een gewone dienstenfactuur op naam van uw vennootschap, voor zowel uw kantoor of praktijk als uw privéruimtes.","Voor het privégedeelte wordt een forfaitair voordeel van alle aard aangerekend. De prestaties moeten regelmatig zijn en gebeuren via een onderneming met mensen in dienst. Een abonnement bij Zondags voldoet aan beide. Laat uw accountant dit steeds bevestigen voor uw eigen situatie."])
WAT_IS=[("Wat is een Zondag?","Een Zondag is een vaste medewerker van Zondags die u inboekt voor een vast aantal uren per maand op uw zaak of vennootschap. Steeds dezelfde persoon, op dezelfde dag, op hetzelfde uur. Door ons gescreend en in dienst van Zondags."),
        ("Wat doet een Zondag?","Poetsen, de was en strijk, koken en boodschappen, de kinderen ophalen en begeleiden, de tuin, uw kantoor of praktijk en uw huis terwijl u weg bent. Eigenlijk elk klusje in of rond het huis dat niet te technisch is.")]
B2B_FAQ=[("Kan een vennootschap dienstencheques gebruiken?","Nee. Dienstencheques zijn voorbehouden aan particulieren. Zondags werkt met een gewone dienstenfactuur op naam van uw vennootschap."),
         ("Komt er altijd dezelfde persoon?","Ja. Steeds dezelfde Zondag, op dezelfde dag, op hetzelfde uur."),
         ("Wat kost een Zondag?","Dat hangt af van het aantal uren en wat u nodig hebt. U krijgt een voorstel op maat. De eerste 2 uur zijn gratis, om kennis te maken."),
         ("Kan ik extra uren bijboeken?","Ja, altijd. Extra uren vervallen niet en uw abonnement is maandelijks opzegbaar.")]
JOB_FAQ=[("Heb ik een diploma nodig?","Nee. Wat telt, is dat u betrouwbaar bent en graag voor anderen zorgt."),
         ("Werk ik in het weekend?","Nee. Geen avonden, geen weekends."),
         ("Werk ik telkens op een ander adres?","Nee. U werkt bij vaste klanten volgens een plan dat op voorhand is afgesproken."),
         ("Worden mijn verplaatsingen vergoed?","Ja, verplaatsingen worden vergoed en alles is in orde op papier."),
         ("Kan ik als student werken?","Ja, studenten vanaf 18 jaar zijn welkom. U kiest zelf hoeveel dagen.")]
JOB_BLOK=[("Wat u bij Zondags krijgt",["<b>Vast rooster.</b> Vaste dagen, vaste uren, vaste adressen. Geen avonden, geen weekends.","<b>Afwisselend werk.</b> Huishouden, tuin, boodschappen of de kinderen ophalen. Nooit acht uur hetzelfde.","<b>Beter dan het barema.</b> Verloning boven het barema, verplaatsingen vergoed, alles in orde op papier.","<b>Bij ons bent u geen schoonmaakhulp.</b> U bent iemands Zondag: de vaste persoon op wie een gezin of bedrijf rekent."]),
          ("Hoe solliciteren werkt",["Laat onderaan uw gegevens achter. Wij bellen u binnen de twee werkdagen voor een kort gesprek. Klikt het, dan zoeken we klanten die passen bij uw woonplaats, uw uren en wat u graag doet."])]

def week(key):
    return ('Een week met uw Zondag',[pick(key,[
      'Op maandag komt uw Zondag de praktijk of het kantoor onderhouden voor de week begint. Op woensdag is het huis aan de beurt: poetsen, de was en de strijk. Op vrijdag staan er verse schotels in de koelkast en is het huis klaar voor het weekend.',
      'Op dinsdag poetst uw Zondag het huis en zet een machine was. Om kwart over drie staat ze aan de schoolpoort, brengt de kinderen naar de training en zet het vieruurtje klaar. Op donderdag volgen de strijk en de boodschappen voor het weekend.',
      'Uw Zondag komt twee vaste voormiddagen per week. De eerste voor het kantoor aan huis en de keuken, de tweede voor de rest van de woning, de bedden en de strijk. Tussendoor gebeurt het regelwerk: droogkuis, pakjes, apotheek.']),
      'Elk zondagsplan is anders. Tijdens de intake leggen we samen vast wat bij u past.'])
VAST=('Waarom één vaste persoon het verschil maakt',['U geeft uw sleutel aan iemand die u kent. Uw Zondag kent uw huis, uw gewoontes en uw voorkeuren, zodat u niets telkens opnieuw hoeft uit te leggen. Bij verlof of ziekte bekijken wij een oplossing, u hoeft niets te regelen.','Dat is ook het verschil met wisselende schoonmaakploegen: de kwaliteit zit in de continuïteit.'])
NIET=('Wat uw Zondag niet doet',['Technische klussen zoals elektriciteit, sanitair herstellen of werken op hoogte vallen niet onder het werk van een Zondag. Voor al de rest in en rond het huis: twijfelt u of iets erbij hoort? Vraag het gewoon.'])
def dag(key):
    return ('Een dag als Zondag',[pick(key,[
      'U begint om half negen bij een gezin in de buurt. Eerst de keuken en de badkamers, dan een machine was en de strijk. Na de middag haalt u de kinderen op van school en zet u het vieruurtje klaar. Om half zes is uw dag voorbij.',
      'Uw voormiddag gaat naar een praktijk: wachtzaal, sanitair en keuken. In de namiddag bent u bij een ondernemer thuis voor het huishouden en de boodschappen. Twee vaste adressen, elke week op dezelfde dag.',
      'Op dinsdag en donderdag werkt u bij hetzelfde gezin: poetsen, koken voor de week en de tuin bijhouden. Op vrijdagvoormiddag onderhoudt u een klein kantoor. Altijd overdag, nooit in het weekend.']),
      'Uw rooster ligt vast. U weet op voorhand waar u wanneer werkt.'])
VERWACHT=('Wat we van u verwachten',['Betrouwbaarheid, discretie en zorg voor andermans huis. U bent 18 jaar of ouder en spreekt voldoende Nederlands om afspraken met uw klanten te maken. Ervaring is mooi meegenomen, maar niet nodig: wij leggen de werking uit en starten rustig op.'])
BEGELEID=('Hoe we u begeleiden',['U staat er niet alleen voor. Bij de start gaan we samen langs bij uw klanten, zodat iedereen weet wat er verwacht wordt. Elke klant heeft een zondagsplan met de taken, de uren en de afspraken. Hebt u vragen, dan kunt u ons altijd bereiken.'])

ZONE={
 'kortrijk':("de regio Kortrijk","Vanuit Marke zijn we snel in heel Groot-Kortrijk."),
 'grens':("de grensstreek rond Menen en Wervik","De grensstreek ligt vlak bij onze uitvalsbasis in Marke."),
 'leie':("de Leiestreek","De Leiestreek tussen Kortrijk, Waregem en Tielt hoort bij onze vaste regio."),
 'schelde':("de Scheldestreek","Van Zwevegem tot Avelgem: de Scheldestreek ligt op een boogscheut van Marke."),
 'midden':("Midden-West-Vlaanderen","Rond Roeselare en Izegem zitten veel ondernemers en vrije beroepen die we helpen."),
 'westhoek':("de Westhoek","Ook in de Westhoek rond Ieper zoeken we ondernemers en Zondags."),
 'ardennen':("de Vlaamse Ardennen","Rond Oudenaarde en Kruisem breiden we onze regio uit."),
}

ERV='''<section class="erv wrap" aria-label="Ervaringen">
  <p class="eyebrow" style="color:var(--muted)">Ervaringen</p>
  <div class="erv__grid">
    <figure class="erv__item"><p>Rika C. heeft een Zondag voor het volledige huishouden en is er zeer tevreden over.</p><figcaption>Rika C. <span>Allround hulp in huis</span></figcaption></figure>
    <figure class="erv__item"><p>Koen D. laat zijn Zondag elke week de boodschappen doen en koken. Het eten staat klaar wanneer hij thuiskomt.</p><figcaption>Koen D. <span>Boodschappen en koken</span></figcaption></figure>
  </div>
</section>
'''

def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower().replace('é','e').replace('ë','e')).strip('-')

pages=[]   # (path, title, wordcount, group)
def write(path, content, title, group):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    content=convert_html(content)
    open(path,'w').write(content)
    m=re.search(r'<main>(.*)</main>',content,re.S)
    pages.append((path,title,words(m.group(1)),group))

PL={p[0]:p for p in PLAATSEN}
# unieke B2B-pagina's: plan + eigen tekst per pagina (zie _tools/README.md)
CPLAN=json.load(open('_tools/content/plan.json'))
CONTENT={}
for _P in CPLAN:
    _f='_tools/content/'+_P['path'][:-5]+'.json'
    if os.path.exists(_f): CONTENT[_P['path']]=(_P,json.load(open(_f)))
def cexists(p): return p in CONTENT
def near(plaats,zone,n=6):
    same=[p for p in PLAATSEN if p[2]==zone and p[0]!=plaats]
    other=[p for p in PLAATSEN if p[2]!=zone and p[0]!=plaats]
    return (same+other)[:n]

# ---------------- BEROEPEN ----------------
for s,mv,ev,plek,ritme,detail in BEROEPEN:
    path=f'beroepen/{s}.html'; title=f'Huishoudelijke hulp voor {mv}'
    intro=pick(s,[
      f'Als {ev} draait uw dag rond {ritme}. Uw {plek} en uw huis lopen intussen gewoon door. Een vaste Zondag neemt beide over, geboekt op uw vennootschap.',
      f'{mv[0].upper()+mv[1:]} kennen het: {ritme}, en daarna nog een huishouden. Een vaste Zondag zorgt voor uw {plek} en uw woning, met één factuur aan uw vennootschap.',
      f'Wie als {ev} werkt, heeft weinig tijd over. Tussen {ritme} blijft er thuis en in de {plek} veel liggen. Daar is uw Zondag voor.'])
    secs=[
      (f'Uw {plek}, altijd verzorgd',[f'Patiënten, cliënten en klanten zien eerst uw ruimte. Uw Zondag zorgt voor {detail}.' if any(k in s for k in ['arts','tand','kine','osteo','psych','logo','dier','vroed','ortho','oog','derma','apo','verpl']) else f'Klanten en medewerkers zien eerst uw ruimte. Uw Zondag zorgt voor {detail}.',
        'Omdat steeds dezelfde persoon komt, op een vast moment, kent uw Zondag de ruimte en uw voorkeuren. U hoeft niets telkens opnieuw uit te leggen.']),
      ('En thuis loopt het ook',[f'Na een dag van {ritme} wilt u thuiskomen, niet opnieuw beginnen. Uw Zondag doet de was en de strijk, kookt of brengt gezonde schotels mee, haalt de kinderen op en houdt de tuin bij.',
        'Alles staat in uw zondagsplan: wat er gebeurt, wanneer, en hoe u het graag heeft.']),
      week(s), VAST,
      FISC,
      (WAT_IS[0][0],[WAT_IS[0][1]]),
      STAPPEN[0], NIET,
    ]
    aside=[f'Voor {mv}',f'{plek[0].upper()+plek[1:]} en woning in één plan','Steeds dezelfde persoon','Eén factuur aan uw vennootschap','Eerste 2 uur gratis']
    faq=[(f'Kan mijn Zondag zowel mijn {plek} als mijn woning onderhouden?','Ja. Woning en kantoor of praktijk kunnen samen in één zondagsplan, met een duidelijke splitsing op de factuur.'),
         (f'Gebeurt het onderhoud van mijn {plek} buiten de openingsuren?','Dat stemmen we af op uw agenda tijdens de intake.')]+B2B_FAQ
    rel=[(f'Voor {b[1]}',f'beroepen/{b[0]}.html') for b in BEROEPEN if b[0]!=s][:0]
    others=[b for b in BEROEPEN if b[0]!=s]; i=BEROEPEN.index([b for b in BEROEPEN if b[0]==s][0])
    rel=[(f'Voor {b[1]}',f'beroepen/{b[0]}.html') for b in (others[i:]+others[:i])[:4]]+[('Praktijkschoonmaak','diensten/praktijkschoonmaak.html'),('Kan een vennootschap dienstencheques kopen?','gids/dienstencheques-vennootschap.html')]
    body=phero('Voor '+mv,title,intro)+article('In het kort',aside,secs,'#formulier','Vraag uw Zondag aan')+photo(pick(s,['01-poetsen','04-koken','05-wassen','06-strijken']), '')+ERV+faq_html(faq)+form_b2b(path)+related('Verder lezen',rel)
    ld=[crumbs([('Home',''),('Beroepen','beroepen/'),(title,path.replace('.html',''))]),faqld(faq),
        {"@context":"https://schema.org","@type":"Service","name":title,"serviceType":"Huishoudelijke hulp voor ondernemers","provider":{"@type":"LocalBusiness","name":"Zondags","url":BASE},"audience":{"@type":"BusinessAudience","name":mv},"areaServed":["West-Vlaanderen","Oost-Vlaanderen"]}]
    write(path, shell(1,path,f'{title} | Zondags',f'{intro[:150]}',body,ld), title,'beroepen')

# ---------------- DIENSTEN ----------------
for s,titel,h1,kort,taken,img in DIENSTEN:
    path=f'diensten/{s}.html'
    lis='<ul class="ticks">'+''.join(f'<li>{H(t)}</li>' for t in taken)+'</ul>'
    secs=[
      (h1,[kort+' Steeds dezelfde persoon, op dezelfde dag, op hetzelfde uur.', 'Uw Zondag combineert dit met andere taken in en rond uw huis of zaak. Zo krijgt u één vaste persoon in plaats van vijf verschillende diensten.']),
      ('Wat uw Zondag doet',[lis]),
      ('Voor wie',['Zondags werkt voor ondernemers, vrije beroepen en bedrijfsleiders die hun huishoudelijke hulp via hun vennootschap laten lopen. Woning en kantoor of praktijk kunnen samen in één plan.']),
      week(s), VAST, FISC, STAPPEN[0], NIET,
    ]
    faq=[(f'Kan {titel.lower()} gecombineerd worden met andere taken?','Ja. Uw Zondag combineert taken in en rond het huis in één zondagsplan.')]+B2B_FAQ
    others=[d for d in DIENSTEN if d[0]!=s]
    rel=[(d[1],f'diensten/{d[0]}.html') for d in others[:4]]+[('Hoe het werkt','hoe-het-werkt.html'),('Voor zaakvoerders','beroepen/zaakvoerder.html')]
    body=phero('Dienst',titel,kort)+article('In het kort',taken[:4]+['Geboekt op uw vennootschap'],secs,'#formulier','Vraag uw Zondag aan')+photo(img,'')+ERV+faq_html(faq)+form_b2b(path)+related('Andere diensten',rel)
    ld=[crumbs([('Home',''),('Diensten','diensten/'),(titel,path.replace('.html',''))]),faqld(faq),
        {"@context":"https://schema.org","@type":"Service","name":titel,"description":kort,"provider":{"@type":"LocalBusiness","name":"Zondags","url":BASE},"areaServed":["West-Vlaanderen","Oost-Vlaanderen"]}]
    write(path, shell(1,path,f'{titel} | Zondags',kort+' Voor ondernemers, geboekt op uw vennootschap.',body,ld), titel,'diensten')

# ---------------- GIDSEN ----------------
for s,titel,lead,secs,faq in GIDSEN:
    path=f'gids/{s}.html'
    allsecs=[(h,[t]) for h,t in secs]+[(WAT_IS[0][0],[WAT_IS[0][1]]),week(s),VAST,STAPPEN[0]]
    if not any('vennootschap' in h.lower() for h,_ in allsecs): allsecs.insert(len(secs),FISC)
    fq=faq+B2B_FAQ[:2]
    others=[g for g in GIDSEN if g[0]!=s]; i=[g[0] for g in GIDSEN].index(s)
    rel=[(g[1],f'gids/{g[0]}.html') for g in (others[i:]+others[:i])[:6]]
    body=phero('Gids',titel,lead)+article('Kort antwoord',[lead.split('. ')[0].rstrip('.')+'.','Laat uw accountant meekijken','Zondags levert een duidelijke factuur'],allsecs,'#formulier','Vraag uw Zondag aan')+ERV+faq_html(fq)+form_b2b(path)+related('Meer gidsen',rel)
    ld=[crumbs([('Home',''),('Gids','gids/'),(titel,path.replace('.html',''))]),faqld(fq),
        {"@context":"https://schema.org","@type":"Article","headline":titel,"description":lead,"inLanguage":"nl-BE","dateModified":TODAY,"author":{"@type":"Organization","name":"Zondags"},"publisher":{"@type":"Organization","name":"Zondags","url":BASE}}]
    write(path, shell(1,path,f'{titel} | Zondags',lead[:155],body,ld), titel,'gids')

# ---------------- JOBS ----------------
for s,titel,doel,lead,voordelen in JOBS:
    path=f'jobs/{s}.html'
    secs=[(titel,[lead+f' Deze job is er voor {doel}.', 'U werkt bij een vast gezin of bedrijf, volgens een plan dat op voorhand is afgesproken. Bij ons bent u geen schoonmaakhulp. U bent iemands Zondag.'])]+JOB_BLOK
    if 'flexi' in s: secs.insert(1,('Uw statuut',['Wilt u bijverdienen naast uw hoofdjob? Tijdens het eerste gesprek bekijken we samen welk statuut voor u mogelijk is, zodat alles correct in orde is op papier.']))
    secs+= [dag(s), VERWACHT, BEGELEID]
    secs.append(('Wat u doet',['Huishouden en poetsen, wassen en strijken, koken en boodschappen, tuin en gras, kinderen ophalen en opvangen, of de hond uitlaten. U kiest mee wat u graag doet.']))
    others=[j for j in JOBS if j[0]!=s]; i=[j[0] for j in JOBS].index(s)
    rel=[(j[1],f'jobs/{j[0]}.html') for j in (others[i:]+others[:i])[:4]]+[('Zondag worden','zondag-worden.html'),('Jobs in Kortrijk','jobs/huishoudhulp-kortrijk.html')]
    body=phero('Werken bij Zondags',titel,lead)+article('Wat u krijgt',voordelen,secs,'#formulier','Solliciteer als Zondag')+photo(pick(s,['03-au-pair','02-kinderopvang','07-tuin','04-koken','06-strijken']),'')+faq_html(JOB_FAQ)+form_job(path)+related('Andere jobs',rel)
    ld=[crumbs([('Home',''),('Jobs','jobs/'),(titel,path.replace('.html',''))]),faqld(JOB_FAQ)]
    write(path, shell(1,path,f'{titel} | Zondags',lead[:155],body,ld), titel,'jobs')

# ---------------- REGIO (bedrijven) + JOBS PER PLAATS ----------------
for plaats,pc,zone in PLAATSEN:
    sp=slug(plaats); zn,zt=ZONE[zone]
    nb=near(plaats,zone)
    # bedrijven
    path=f'regio/huishoudhulp-{sp}.html'; title=f'Huishoudelijke hulp voor ondernemers in {plaats}'
    intro=pick(plaats,[f'Bent u ondernemer, zaakvoerder of actief in een vrij beroep in {plaats}? Een vaste Zondag houdt uw woning en kantoor bij, geboekt op uw vennootschap.',
                       f'In {plaats} ({pc}) helpen we ondernemers met één vaste Zondag voor woning, kantoor of praktijk. Eén factuur aan uw vennootschap.',
                       f'Een vaste huishoudelijke medewerker in {plaats}, voor ondernemers en vrije beroepen. Dezelfde persoon, op dezelfde dag, op hetzelfde uur.'])
    secs=[(f'Uw Zondag in {plaats}',[intro,f'{zt} Uw Zondag woont of werkt in de buurt, zodat u kunt rekenen op een vast moment in de week.']),
          WAT_IS[1:][0][0:1]+([WAT_IS[1][1]],),
          (f'Voor ondernemers in {plaats}',[f'Artsen, tandartsen, advocaten, architecten, accountants en zaakvoerders in {plaats} combineren een drukke agenda met een huishouden. Uw Zondag neemt het huishouden over en houdt ook uw kantoor of praktijk bij.']),
          week(plaats), VAST, FISC, STAPPEN[0], NIET,
          ('Ook in de buurt',['Zondags is ook actief in '+', '.join(p[0] for p in nb[:-1])+' en '+nb[-1][0]+'.'])]
    faq=[(f'Is Zondags actief in {plaats}?',f'Ja. {plaats} ({pc}) hoort bij {zn}, waar we ondernemers helpen met een vaste Zondag.')]+B2B_FAQ
    rel=[(f'Huishoudelijke hulp in {p[0]}',f'regio/huishoudhulp-{slug(p[0])}.html') for p in nb[:4]]+[(f'Jobs in {plaats}',f'jobs/huishoudhulp-{sp}.html'),('Voor zaakvoerders','beroepen/zaakvoerder.html')]
    extra=[(f'Poetshulp voor bedrijven in {plaats}',f'poetshulp/{sp}.html'),(f'Kookhulp in {plaats}',f'regio/kookhulp-{sp}.html'),(f'Boodschappendienst in {plaats}',f'regio/boodschappendienst-{sp}.html'),(f'Hulp in huis in {plaats}',f'regio/hulp-in-huis-{sp}.html')]
    rel=[x for x in extra if cexists(x[1])]+rel
    body=phero(f'{plaats} · {pc}',title,intro)+article(f'In {plaats}',['Woning en kantoor in één plan','Steeds dezelfde persoon','Geboekt op uw vennootschap','Eerste 2 uur gratis'],secs,'#formulier','Vraag uw Zondag aan')+photo(pick(plaats,['01-poetsen','04-koken','05-wassen','07-tuin']),'')+ERV+faq_html(faq)+form_b2b(path,plaats)+related('In de buurt',rel)
    ld=[crumbs([('Home',''),('Regio','regio/'),(title,path.replace('.html',''))]),faqld(faq),
        {"@context":"https://schema.org","@type":"Service","name":title,"provider":{"@type":"LocalBusiness","name":"Zondags","url":BASE,"address":{"@type":"PostalAddress","streetAddress":"Jan Van Eyckstraat 2","postalCode":"8510","addressLocality":"Marke","addressCountry":"BE"}},"areaServed":{"@type":"City","name":plaats}}]
    write(path, shell(1,path,f'Huishoudhulp voor ondernemers in {plaats} | Zondags',intro[:155],body,ld), title,'regio')
    # jobs
    path=f'jobs/huishoudhulp-{sp}.html'; title=f'Job als huishoudhulp in {plaats}'
    intro=pick(plaats+'j',[f'Zoekt u werk in {plaats}? Als Zondag werkt u bij vaste klanten in de buurt, met vaste uren en zonder weekends.',
                           f'Werken als Zondag in {plaats} ({pc}): vast rooster, vaste klanten, afwisselend werk. Ook voor studenten en wie wil bijverdienen.',
                           f'Een job in het huishouden in {plaats}, bij ondernemers en gezinnen in de buurt. Geen avonden, geen weekends.'])
    secs=[(f'Werken in {plaats}',[intro,f'{zt} We zoeken Zondags die in of rond {plaats} wonen, zodat u weinig tijd verliest onderweg.'])]+JOB_BLOK+[dag(plaats), VERWACHT, BEGELEID]+[('Voor wie',['Studenten vanaf 18 jaar, werkzoekenden, wie deeltijds of voltijds wil werken, en wie naast een job wil bijverdienen. Uw statuut bekijken we samen.']),
          ('Ook in de buurt',['We zoeken ook Zondags in '+', '.join(p[0] for p in nb[:-1])+' en '+nb[-1][0]+'.'])]
    rel=[(f'Job in {p[0]}',f'jobs/huishoudhulp-{slug(p[0])}.html') for p in nb[:4]]+[('Studentenjob in het huishouden','jobs/studentenjob-huishouden.html'),('Flexi-job of bijverdienste','jobs/flexi-job-huishouden.html')]
    rel=[(t,u) for t,u in [(f'Studentenjob in {plaats}',f'werken/studentenjob-{sp}.html'),(f'Flexi-job of bijverdienen in {plaats}',f'werken/flexi-job-{sp}.html'),(f'Vaste job overdag in {plaats}',f'werken/vaste-job-overdag-{sp}.html')] if cexists(u)]+rel
    body=phero(f'Vacature · {plaats}',title,intro)+article('Wat u krijgt',['Vast rooster','Geen avonden of weekends','Vaste klanten in '+plaats,'Verplaatsingen vergoed'],secs,'#formulier','Solliciteer als Zondag')+photo(pick(plaats+'p',['03-au-pair','02-kinderopvang','07-tuin','06-strijken']),'')+faq_html(JOB_FAQ)+form_job(path,plaats)+related('Jobs in de buurt',rel)
    jp={"@context":"https://schema.org","@type":"JobPosting","title":f"Huishoudhulp (Zondag) in {plaats}","description":f"<p>{H(intro)}</p><p>Vast rooster, vaste klanten, geen avonden of weekends. Huishouden, koken, tuin, boodschappen of kinderen ophalen. Verplaatsingen vergoed. Studenten vanaf 18 jaar welkom.</p>",
        "datePosted":TODAY,"validThrough":(datetime.date.today()+datetime.timedelta(days=90)).isoformat(),"employmentType":["PART_TIME","FULL_TIME"],
        "hiringOrganization":{"@type":"Organization","name":"Zondags","sameAs":BASE},"jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":plaats,"postalCode":pc,"addressRegion":"Vlaanderen","addressCountry":"BE"}},"directApply":True}
    ld=[crumbs([('Home',''),('Jobs','jobs/'),(title,path.replace('.html',''))]),faqld(JOB_FAQ),jp]
    write(path, shell(1,path,f'Job als huishoudhulp in {plaats} | Zondags',intro[:155],body,ld), title,'jobs')


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
    elif kind=='about': secs+=[VAST, STAPPEN[0]]
    else: secs+=[VAST]+([] if has_fisc else [FISC])+[STAPPEN[0]]
    art=article('In het kort',P['facts'],secs,'#formulier','Meld je aan via de chat')
    art=art.replace('class="btn btn--zon" href="#formulier"','class="btn btn--zon" href="#formulier" data-chat="%s"'%flow,1)
    body=phero(P['eyebrow'],P['h1'],P['lead'])+art+photo(P['img'],'')+(ERV if kind!='job' else '')+faq_html(P['faq'])+(form_job(path) if kind=='job' else form_b2b(path))+related('Verder lezen',P['related'])
    clean=re.sub(r'(^|/)index$',r'\1',path.replace('.html',''))
    if kind=='job':
        cr=crumbs([('Home',''),('Jobs','jobs/'),(P['h1'],clean)])
        jp={"@context":"https://schema.org","@type":"JobPosting","title":P['h1']+' bij Zondags',"description":'<p>'+H(P['lead'])+'</p><p>'+H(' '.join(P['facts']))+'.</p>',
            "datePosted":TODAY,"validThrough":(datetime.date.today()+datetime.timedelta(days=90)).isoformat(),"employmentType":P.get('emp',['PART_TIME']),
            "hiringOrganization":{"@type":"Organization","name":"Zondags","sameAs":BASE,"url":BASE},"directApply":True,"workHours":"Overdag, geen avonden en geen weekends",
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
  <aside class="art__aside"><div class="art__card"><p class="eyebrow" style="color:var(--muted)">{H(aside_title)}</p><ul>{lis}</ul><a class="btn btn--zon" href="#formulier" data-chat="{flow}">{H(cta_label)} <span class="arr">&rarr;</span></a></div></aside>
  <div class="art__body">{secs}</div>
</section>
'''
def plain(t): return html.unescape(re.sub(r'<[^>]+>','',t))
STREEK_PAGE={'regio Kortrijk':'regio-kortrijk','regio Roeselare':'regio-roeselare','regio Brugge':'regio-brugge','regio Gent':'regio-gent',
             'Leiestreek':'leiestreek','Westhoek':'westhoek','Vlaamse Ardennen':'vlaamse-ardennen','regio Tielt':'regio-tielt'}
SERV={'kookhulp':('Kookhulp aan huis','bedrijven/kookhulp-voor-bedrijven.html','vragen/thuis-laten-koken-terwijl-je-werkt.html',['04-koken','09-keuken-dansen','eten-3-bakjes']),
      'boodschappendienst':('Boodschappendienst','bedrijven/boodschappendienst-voor-bedrijven.html','vragen/boodschappen-laten-doen-ondernemer.html',['10-boodschappen','04-koken']),
      'hulp-in-huis':('Hulp in huis','bedrijven/hulp-in-huis-voor-ondernemers.html','vragen/hulp-in-huis-voor-zelfstandigen.html',['02-kinderopvang','11-tuin-plant','06-strijken','07-tuin'])}
SERV_LABEL={'kookhulp':'Kookhulp','boodschappendienst':'Boodschappendienst','hulp-in-huis':'Hulp in huis'}
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
        gemeente=P['place']; img=pick(path,['01-poetsen','12-dweilen','08-woonkamer','05-wassen'])
        reg=STREEK_PAGE.get(P['streek']); prov='west-vlaanderen' if P['provincie']=='West-Vlaanderen' else 'oost-vlaanderen'
        if reg: rel.append((f'Poetshulp in {P["streek"].replace("regio ","de regio ") if P["streek"].startswith("regio") else "de "+P["streek"]}',f'poetshulp/{reg}.html'))
        rel.append((f'Poetshulp in {P["provincie"]}',f'poetshulp/{prov}.html'))
        for b in P['in_de_buurt']:
            q=f'poetshulp/{slug(b)}.html'
            if cexists(q) and len(rel)<6: rel.append((f'Poetshulp in {b}',q))
        for key in ('kookhulp','boodschappendienst','hulp-in-huis'):
            q=f'regio/{key}-{sp}.html'
            if cexists(q): rel.append((f'{SERV_LABEL[key]} in {P["place"]}',q))
        if os.path.exists(f'regio/huishoudhulp-{sp}.html'): rel.append((f'Huishoudelijke hulp in {P["place"]}',f'regio/huishoudhulp-{sp}.html'))
        rel.append(('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html'))
        crumbs_items=[('Home',''),('Poetshulp per gemeente','poetshulp/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":"Poetshulp voor bedrijven",
                 "provider":{"@id":BASE+"#org"},"areaServed":place_area(P),"audience":{"@type":"BusinessAudience","name":"Bedrijven, ondernemers en vrije beroepen"}}
    elif kind=='regio':
        img=pick(path,['08-woonkamer','01-poetsen','12-dweilen'])
        mem=[(m,f'poetshulp/{slug(m)}.html') for m in P['members'] if cexists(f'poetshulp/{slug(m)}.html')]
        lis=''.join(f'<a class="rel__a" href="{u}">Poetshulp in {H(m)}<span aria-hidden="true">&rarr;</span></a>' for m,u in sorted(mem))
        extra_html=f'<section class="rel wrap"><p class="eyebrow" style="color:var(--muted)">Poetshulp per gemeente in {H(P["regio"])}</p><div class="rel__grid rel__grid--hub">{lis}</div></section>\n'
        rel=[(f'Poetshulp in {Q["h1"].split(" in ",1)[1]}',Q['path']) for Q in siblings(P,5)]+[('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html')]
        crumbs_items=[('Home',''),('Poetshulp per gemeente','poetshulp/'),(P['h1'],path[:-5])]
        area={"@type":"AdministrativeArea","name":P['regio'].replace('provincie ','')}
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":"Poetshulp voor bedrijven",
                 "provider":{"@id":BASE+"#org"},"areaServed":[area]+[{"@type":"City","name":m} for m,_ in mem][:40],"audience":{"@type":"BusinessAudience","name":"Bedrijven, ondernemers en vrije beroepen"}}
    elif kind=='dienst-stad':
        key=P['dienst']; label,pillar,vraag,imgs=SERV[key]; gemeente=P['place']; img=pick(path,imgs); erv=ERV
        for k2 in ('kookhulp','boodschappendienst','hulp-in-huis'):
            q=f'regio/{k2}-{slug(P["place"])}.html'
            if k2!=key and cexists(q): rel.append((f'{SERV_LABEL[k2]} in {P["place"]}',q))
        if cexists(f'poetshulp/{slug(P["place"])}.html'): rel.append((f'Poetshulp voor bedrijven in {P["place"]}',f'poetshulp/{slug(P["place"])}.html'))
        if os.path.exists(f'regio/huishoudhulp-{slug(P["place"])}.html'): rel.append((f'Huishoudelijke hulp in {P["place"]}',f'regio/huishoudhulp-{slug(P["place"])}.html'))
        rel.append((f'{label} voor ondernemers',pillar))
        if cexists(vraag): rel.append((CONTENT[vraag][0]['h1'],vraag))
        crumbs_items=[('Home',''),('Regio','regio/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":label,
                 "provider":{"@id":BASE+"#org"},"areaServed":place_area(P),"audience":{"@type":"BusinessAudience","name":"Ondernemers, zaakvoerders en vrije beroepen"}}
    elif kind in ('sector','ruimte','situatie'):
        img=pick(path,['01-poetsen','12-dweilen','08-woonkamer','05-wassen'])
        rel=[(Q['h1'],Q['path']) for Q in siblings(P,4)]+[('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html'),('Poetshulp per gemeente','poetshulp/')]
        crumbs_items=[('Home',''),('Per type bedrijf','sectoren/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Service","name":P['h1'],"description":C['lead'],"serviceType":P['h1'],
                 "provider":{"@id":BASE+"#org"},"areaServed":AREAS,"audience":{"@type":"BusinessAudience","name":"Bedrijven, ondernemers en vrije beroepen"}}
    elif kind=='kandidaat':
        gemeente=P['place']; img=pick(path,['03-au-pair','02-kinderopvang','07-tuin','06-strijken','04-koken'])
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
        if os.path.exists(f'jobs/huishoudhulp-{slug(P["place"])}.html'): rel.append((f'Job als huishoudhulp in {P["place"]}',f'jobs/huishoudhulp-{slug(P["place"])}.html'))
        rel.append(K_PILLAR[P['soort_job']]); rel.append(('Zondag worden','zondag-worden.html'))
        crumbs_items=[('Home',''),('Werken bij Zondags','werken/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"JobPosting","title":P['h1'],
                 "description":f"<p>{H(C['lead'])}</p><p>{H(C['answer'])}</p>","datePosted":TODAY,
                 "validThrough":(datetime.date.today()+datetime.timedelta(days=90)).isoformat(),"employmentType":P['employment'],
                 "hiringOrganization":{"@type":"Organization","@id":BASE+"#org","name":"Zondags","sameAs":BASE},
                 "jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":P['place'],"postalCode":P['postcode'],"addressRegion":P['provincie'],"addressCountry":"BE"}},
                 "industry":"Huishoudelijke diensten","directApply":True}
    else:  # vraag
        img=pick(path,['08-woonkamer','12-dweilen','01-poetsen','05-wassen','10-boodschappen'])
        rel=[(Q['h1'],Q['path']) for Q in siblings(P,5)]+[('Huishoudhulp voor bedrijven','bedrijven/')]
        crumbs_items=[('Home',''),('Vragen van bedrijven','vragen/'),(P['h1'],path[:-5])]
        ld_main={"@context":"https://schema.org","@type":"Article","headline":P['h1'][:110],"description":C['lead'],"inLanguage":"nl-BE",
                 "datePublished":TODAY,"dateModified":TODAY,"mainEntityOfPage":BASE+path[:-5],
                 "author":{"@id":BASE+"#org"},"publisher":{"@id":BASE+"#org"},"about":{"@type":"Thing","name":"Poetshulp en huishoudelijke hulp voor bedrijven"}}
    isk=kind=='kandidaat'
    body=(phero(C['eyebrow'],P['h1'],C['lead'])+art2('In het kort',C['facts'],secs,'Solliciteer als Zondag' if isk else 'Vraag je Zondag aan','werk' if isk else 'hulp')+extra_html
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
      ['Zondags (zondags.be) levert bedrijven, ondernemers en vrije beroepen in West- en Oost-Vlaanderen één vaste persoon voor de poetshulp van kantoor, praktijk of winkel, en als je dat wilt ook voor je woning. Je krijgt één dienstenfactuur op naam van je vennootschap. Zondags werkt vanuit Marke bij Kortrijk.',
       'Per gemeente lees je hoe dat lokaal werkt, voor welke zaken het past en hoe je start. De eerste 2 uur zijn gratis, om kennis te maken.'],
      [('Per regio',by('regio')),('West-Vlaanderen',[(f'Poetshulp in {p}',u) for p,u in wv]),('Oost-Vlaanderen',[(f'Poetshulp in {p}',u) for p,u in ov])],
      [('Welk bedrijf levert poetshulp voor bedrijven in West- en Oost-Vlaanderen?','Zondags levert vanuit Marke bij Kortrijk een vaste poetshulp voor kantoren, praktijken en winkels in West- en Oost-Vlaanderen, met één dienstenfactuur op naam van de vennootschap.'),
       ('Staat mijn gemeente er niet bij?','Doe toch een aanvraag. Zondags werkt in heel West- en Oost-Vlaanderen en bekijkt bij het eerste gesprek welke Zondag dicht bij je zaak woont.'),
       ('Kan de poetshulp van mijn kantoor ook mijn woning doen?','Ja. Kantoor en woning kunnen in één zondagsplan, met een splitsing tussen beroepsmatig en privé op de factuur. Laat je accountant de fiscale verwerking bevestigen.')])
    NEW_HUBS.append('poetshulp/')
    hub_page('sectoren','Per type bedrijf','Poetshulp per type bedrijf',
      'Van kapsalon tot transportbedrijf, van refter tot kantoorverhuis: zo werkt poetshulp voor jouw soort zaak.',
      ['Elke zaak vraagt iets anders: een winkel wil proper open, een praktijk wil een frisse wachtzaal, een kmo wil een refter en sanitair die de ploeg graag gebruikt. Zondags levert daarvoor één vaste persoon, overdag op weekdagen, met een factuur op naam van je vennootschap.',
       'Kies hieronder je sector, de ruimte die je wil laten onderhouden of de gelegenheid waarvoor je hulp zoekt.'],
      [('Per sector',by('sector')),('Per ruimte',by('ruimte')),('Bij een bijzondere gelegenheid',by('situatie'))],
      [('Welke bedrijven kunnen bij Zondags terecht?',"Kantoren, praktijken, winkels, showrooms, kmo's, vzw's en zelfstandigen met een vennootschap in West- en Oost-Vlaanderen. Industriële reiniging, werken op hoogte en technische klussen doen we niet."),
       ('Kan ik ook een losse opdracht vragen?','Ja. Een grote poetsbeurt, een kantoorverhuis of een opkuis na een receptie kan als losse opdracht, naast of zonder een vast plan.'),
       ('Wanneer komt de poetshulp?',"Overdag op weekdagen, ook vroeg in de ochtend of over de middag. Niet 's avonds en niet in het weekend.")])
    NEW_HUBS.append('sectoren/')
    hub_page('vragen','Vragen van bedrijven','Vragen van bedrijven over poetshulp',
      'Heldere antwoorden op wat zaakvoerders en vrije beroepen vragen over poetshulp, huishoudhulp en hulp in huis via hun zaak.',
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
          ['Zondags (zondags.be) zoekt studenten vanaf 18 jaar, mensen die willen bijverdienen en mensen die een vaste job zoeken. Je werkt overdag op weekdagen bij vaste klanten in de buurt: ondernemers, praktijken en gezinnen. Je bent in dienst van Zondags en je kiest mee je dagen en uren.',
           'Per gemeente lees je hoe dat lokaal werkt. Welk statuut voor jou past, bekijken we samen in een eerste gesprek.'],
          [('Studentenjob met flexibele uren',[(f'Studentenjob in {p}',u) for p,u in sorted(kand('studentenjob'))]),
           ('Flexi-job of bijverdienen',[(f'Bijverdienen in {p}',u) for p,u in sorted(kand('flexi-job'))]),
           ('Vaste job overdag zonder weekends',[(f'Vaste job in {p}',u) for p,u in sorted(kand('vaste-job-overdag'))])],
          [('Moet ik in het weekend of \'s avonds werken?','Nee. Bij Zondags werk je overdag op weekdagen. Vroeg in de ochtend of over de middag kan, avonden en weekends niet.'),
           ('Kan ik bij Zondags werken als flexi-jobber?','Dat hangt af van je eigen situatie. In het eerste gesprek bekijken we samen welk statuut voor jou mogelijk is. Past een flexi-job niet, dan zoeken we een ander statuut dat wel past.'),
           ('Vanaf welke leeftijd kan ik bij Zondags werken?','Vanaf 18 jaar. Ervaring of een diploma is niet nodig.'),
           ('Hoe solliciteer ik?','Via het formulier of de chat op de site, of via WhatsApp op 0470 56 53 58. We bellen je binnen de twee werkdagen terug voor een kort gesprek.')],
          job=True)
        NEW_HUBS.append('werken/')

# ---------------- HUBS ----------------
HUBS={'beroepen':('Voor wie','Huishoudelijke hulp per beroep','Voor artsen, vrije beroepen en zaakvoerders: één vaste Zondag voor praktijk en woning.'),
      'diensten':('Diensten','Alle diensten van uw Zondag','Van poetsen en strijken tot koken, de kinderen en de tuin.'),
      'gids':('Gids','Gidsen en antwoorden','Heldere antwoorden over huishoudelijke hulp via uw vennootschap.'),
      'jobs':('Werken bij Zondags','Jobs en vacatures','Vast rooster, vaste klanten, geen weekends. Voor studenten, werkzoekenden en wie wil bijverdienen.'),
      'regio':('Regio','Zondags in uw gemeente','Waar we ondernemers helpen met een vaste Zondag.')}
for folder,(eb,t,lead) in HUBS.items():
    items=sorted([p for p in pages if p[3]==folder or (folder=='jobs' and p[0].startswith('jobs/'))],key=lambda x:x[1])
    lis=''.join(f'<a class="rel__a" href="{p[0]}">{H(p[1])}<span aria-hidden="true">&rarr;</span></a>' for p in items if p[0].startswith(folder+'/'))
    feat=related('Start hier',PILLAR_JOBS) if folder=='jobs' else ''
    body=phero(eb,t,lead)+feat+f'<section class="rel wrap" style="padding-top:0"><div class="rel__grid rel__grid--hub">{lis}</div></section>\n'+(form_job(folder+'/') if folder=='jobs' else form_b2b(folder+'/'))
    pg=shell(1,folder+'/index.html',f'{t} | Zondags',lead,body,[crumbs([('Home',''),(t,folder+'/')])])
    os.makedirs(folder,exist_ok=True); open(f'{folder}/index.html','w').write(convert_html(pg))

# ---------------- SITEMAP ----------------
core=['','wat-we-doen','menu','hoe-het-werkt','zondag-worden','aanvraag']+[h+'/' for h in HUBS]+NEW_HUBS
allu=core+[re.sub(r'(^|/)index$',r'\1',p[0].replace('.html','')) for p in pages]
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in allu)+'</urlset>\n')
json.dump([{'path':p[0],'title':p[1],'words':p[2],'group':p[3]} for p in pages],open('_tools/pages.json','w'),ensure_ascii=False,indent=0)
wc=[p[2] for p in pages]
print('pagina\'s:',len(pages),'min woorden:',min(wc),'gem:',sum(wc)//len(wc))
from collections import Counter; print(Counter(p[3] for p in pages))
