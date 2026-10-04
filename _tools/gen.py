import re, os
SRC=open('../z/index.html').read()
main=SRC[SRC.index('<main id="top">')+len('<main id="top">'):SRC.index('</main>')]

def seg(a,b):
    i=main.index(a); j=main.index(b,i+len(a)) if b else len(main)
    return main[i:j]
hero=seg('<section class="hero">','<!-- MARQUEE -->')
marquee=seg('<div class="marquee"','<!-- OPENING')
openS=seg('<section class="open"','<!-- WAT IS EEN ZONDAG -->')
defstate=seg('<section class="def wrap"','<!-- DIENSTEN -->')
k=defstate.index('<section class="state')
defS, stateS = defstate[:k], defstate[k:]
svc=seg('<section class="svc"','<!-- MENU -->')
menu=seg('<section class="menu wrap"','<!-- HOE HET WERKT -->')
how=seg('<section class="how wrap"','<!-- GEBOEKT OP UW ZAAK -->')
fisc=seg('<section class="fisc wrap"','<!-- AANVRAAG -->')
aanv=seg('<section class="price wrap"','<!-- ZONDAG WORDEN -->')
job=seg('<section class="job"','<section class="apply wrap"')
apply_=seg('<section class="apply wrap"',None)

LINKS={'#aanvraag':'aanvraag.html','#diensten':'wat-we-doen.html','#menu':'menu.html','#werkwijze':'hoe-het-werkt.html',
       '#worden':'zondag-worden.html','#zondag':'index.html#zondag','#contact':'aanvraag.html#contact','#top':'index.html','#zaak':'hoe-het-werkt.html#zaak'}
def fix(h):
    h=h.replace('src="img/','src="assets/img/')
    for a,b in LINKS.items(): h=h.replace('href="%s"'%a,'href="%s"'%b)
    h=h.replace(' data-cursor="Sleep"','')
    return h

def strip_head(h, pattern, repl=''):
    return re.sub(pattern,repl,h,count=1,flags=re.S)

# ---------- shared ----------
NAV=[('index.html','Home'),('wat-we-doen.html','Wat we doen'),('menu.html','Ons menu'),('hoe-het-werkt.html','Hoe het werkt'),('zondag-worden.html','Zondag worden'),('aanvraag.html','Contact')]
FAV="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2317221E'/%3E%3Ccircle cx='32' cy='32' r='15' fill='%23E9BE55'/%3E%3C/svg%3E"
def head(file,title,desc):
    url='https://zondags.be/'+('' if file=='index.html' else file.replace('.html',''))
    return f'''<!doctype html>
<html lang="nl-BE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_BE">
<meta property="og:site_name" content="Zondags">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://zondags.be/assets/img/01-poetsen.webp">
<meta name="theme-color" content="#17221E">
<link rel="icon" href="{FAV}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Instrument+Serif:ital@0;1&family=Geist:wght@300..600&display=swap">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<div class="curtain" aria-hidden="true"><span class="wm">z<i></i>ndags</span></div>
'''
AC=' aria-current="page"'
def nav(file):
    li=''.join(f'<li><a href="{h}"{AC if h==file else ""}>{t}</a></li>' for h,t in NAV if h!='index.html')
    mli=''.join(f'<li><a href="{h}"{AC if h==file else ""}>{t}</a></li>' for h,t in NAV)
    return f'''<header class="nav" id="nav">
  <a class="logo" href="index.html" aria-label="Zondags, naar de homepage"><span class="wm">z<i></i>ndags</span></a>
  <ul class="nav__links">{li}</ul>
  <div class="nav__right">
    <a class="btn btn--fill" href="aanvraag.html">Vraag uw Zondag aan <span class="arr">&rarr;</span></a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mmenu"><span></span><span></span></button>
  </div>
</header>
<nav class="mmenu" id="mmenu" aria-label="Menu"><ul>{mli}</ul><p>0470 56 53 58, elke dag van 6 tot 22 uur<br>hello@zondags.be</p></nav>
'''
FOOT='''<footer class="foot" id="footer">
  <div class="foot__sun" aria-hidden="true"></div>
  <div class="foot__top">
    <p class="foot__cta">Uw zondag, <em class="s">elke dag.</em></p>
    <div><h4>Menu</h4><ul><li><a href="wat-we-doen.html">Wat we doen</a></li><li><a href="menu.html">Ons menu</a></li><li><a href="hoe-het-werkt.html">Hoe het werkt</a></li><li><a href="zondag-worden.html">Zondag worden</a></li><li><a href="aanvraag.html">Aanvraag</a></li><li><a href="hoe-het-werkt.html#faq">Veelgestelde vragen</a></li></ul></div>
    <div><h4>Ontdek</h4><ul><li><a href="beroepen/">Per beroep</a></li><li><a href="diensten/">Alle diensten</a></li><li><a href="gids/">Gidsen</a></li><li><a href="regio/">Regio</a></li><li><a href="jobs/">Jobs en vacatures</a></li></ul></div>
    <div><h4>Contact</h4><ul><li><a href="https://wa.me/32470565358">0470 56 53 58</a></li><li>Elke dag van 6 tot 22 uur</li><li><a href="mailto:hello@zondags.be">hello@zondags.be</a></li></ul></div>
    <div><h4>Adres</h4><ul><li>Jan Van Eyckstraat 2</li><li>8510 Marke</li></ul></div>
  </div>
  <div class="foot__logo" aria-hidden="true"><span class="wm">z<i></i>ndags</span></div>
  <div class="foot__legal"><span>&copy; 2026 Zondags, een initiatief van Hummingbirds BV. Alle rechten voorbehouden. <span class="foot__id">BE 0684.696.967</span></span></div>
</footer>
<a class="wa" href="https://wa.me/32470565358" aria-label="Stuur een bericht via WhatsApp"><svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2z"/></svg></a>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.14/dist/lenis.min.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
'''
BAND='''<section class="band">
  <h2>Klaar voor uw eigen <em class="s">Zondag?</em></h2>
  <div><p>Laat in twee minuten weten wat u nodig hebt. Binnen één werkdag belt een van ons u persoonlijk terug.</p><a class="btn btn--fill" href="aanvraag.html">Vraag uw Zondag aan <span class="arr">&rarr;</span></a></div>
</section>
'''
def phero(eyebrow,lines,lead,dark=False):
    ls=''.join(f'<span class="line">{l}</span>' for l in lines)
    return f'''<section class="phero{' phero--dark' if dark else ''}">
  <div><p class="eyebrow">{eyebrow}</p><h1 data-split>{ls}</h1></div>
  <p>{lead}</p>
</section>
'''
def page(file,title,desc,body,extra_head=''):
    h=head(file,title,desc).replace('</head>',extra_head+'</head>')
    if file=='wat-we-doen.html': h=h.replace('<body>','<body class="dark-top">')
    open(file,'w').write(h+nav(file)+'<main>\n'+fix(body)+'</main>\n'+FOOT)

# ---------- forms ----------
HID='''<input type="hidden" name="_subject" value="{subj}">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="https://zondags.be/bedankt">
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        '''
aanv=aanv.replace('<form class="form" id="leadForm" novalidate aria-labelledby="leadTitle">',
  '<form class="form" id="leadForm" novalidate aria-labelledby="leadTitle" action="https://formsubmit.co/mieke@hummingbirds.be" method="POST">\n        '+HID.format(subj='Nieuwe aanvraag via zondags.be'))
aanv=aanv.replace(' name="taken"',' data-group="Taken"')
apply_=apply_.replace('<form class="form" id="jobForm" novalidate>',
  '<form class="form" id="jobForm" novalidate action="https://formsubmit.co/mieke@hummingbirds.be" method="POST" enctype="multipart/form-data">\n        '+HID.format(subj='Nieuwe sollicitatie via zondags.be'))
apply_=re.sub(r'<input type="checkbox" id="(g\d)"><label for="\1">([^<]+)</label>',r'<input type="checkbox" id="\1" data-group="Doet graag" value="\2"><label for="\1">\2</label>',apply_)
apply_=apply_.replace('<input type="checkbox" id="j-ok">','<input type="checkbox" id="j-ok" name="Akkoord" value="Ja" required>')
apply_=apply_.replace('Zondags mijn gegevens gebruikt om mij te contacteren over deze sollicitatie.</label>','Zondags mijn gegevens gebruikt om mij te contacteren over deze sollicitatie.</label>\n          <p class="err f--full" id="e-ok" hidden>Vink dit aan om uw sollicitatie te versturen.</p>')
for a,b in [('id="j-st" name="statuut"','id="j-st" name="Statuut"')]: apply_=apply_.replace(a,b)

# ---------- pages ----------
FAQ='<section class="faq wrap" id="faq">\n  <div class="faq__head"><p class="eyebrow" style="color:var(--muted)">Veelgestelde vragen</p><h2 style="margin-top:18px">Goed om <em class="s">te weten.</em></h2></div>\n  <div class="faq__list"><details class="qa"><summary>Wat is een Zondag?<span aria-hidden="true">+</span></summary><p>Een Zondag is een vaste medewerker van Zondags die u inboekt voor een vast aantal uren per maand op uw zaak of vennootschap. Steeds dezelfde persoon, op dezelfde dag, op hetzelfde uur.</p></details><details class="qa"><summary>Wat kan mijn Zondag allemaal doen?<span aria-hidden="true">+</span></summary><p>Poetsen, wassen en strijken, koken en boodschappen, de kinderen ophalen en begeleiden, de tuin, uw kantoor of praktijk, en uw huis bijhouden terwijl u weg bent. Eigenlijk elk klusje in of rond het huis dat niet te technisch is.</p></details><details class="qa"><summary>Kan een vennootschap dienstencheques gebruiken?<span aria-hidden="true">+</span></summary><p>Nee. Dienstencheques zijn wettelijk voorbehouden aan particulieren. Zondags werkt daarom met een gewone dienstenfactuur op naam van uw vennootschap, voor zowel uw kantoor als uw privéruimtes.</p></details><details class="qa"><summary>Hoe wordt het privégedeelte fiscaal verwerkt?<span aria-hidden="true">+</span></summary><p>Voor het privégedeelte wordt een forfaitair voordeel van alle aard aangerekend. De prestaties moeten regelmatig zijn en gebeuren via een onderneming met mensen in dienst. Een abonnement bij Zondags voldoet aan beide. Laat uw accountant dit steeds bevestigen voor uw eigen situatie.</p></details><details class="qa"><summary>Is mijn Zondag in dienst?<span aria-hidden="true">+</span></summary><p>Ja. Elke Zondag is door ons gescreend en in dienst van Zondags. U werkt dus niet met een zelfstandige.</p></details><details class="qa"><summary>Wat kost een Zondag?<span aria-hidden="true">+</span></summary><p>Dat hangt af van het aantal uren en wat u nodig hebt. Na uw aanvraag belt een van ons u binnen één werkdag persoonlijk terug met een voorstel op maat. De eerste 2 uur zijn gratis, om kennis te maken.</p></details><details class="qa"><summary>Kan ik extra uren bijboeken of opzeggen?<span aria-hidden="true">+</span></summary><p>Extra uren bijboeken kan altijd en ze vervallen niet. Uw abonnement is maandelijks opzegbaar.</p></details></div>\n</section>\n'
FAQLD='<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "Wat is een Zondag?", "acceptedAnswer": {"@type": "Answer", "text": "Een Zondag is een vaste medewerker van Zondags die u inboekt voor een vast aantal uren per maand op uw zaak of vennootschap. Steeds dezelfde persoon, op dezelfde dag, op hetzelfde uur."}}, {"@type": "Question", "name": "Wat kan mijn Zondag allemaal doen?", "acceptedAnswer": {"@type": "Answer", "text": "Poetsen, wassen en strijken, koken en boodschappen, de kinderen ophalen en begeleiden, de tuin, uw kantoor of praktijk, en uw huis bijhouden terwijl u weg bent. Eigenlijk elk klusje in of rond het huis dat niet te technisch is."}}, {"@type": "Question", "name": "Kan een vennootschap dienstencheques gebruiken?", "acceptedAnswer": {"@type": "Answer", "text": "Nee. Dienstencheques zijn wettelijk voorbehouden aan particulieren. Zondags werkt daarom met een gewone dienstenfactuur op naam van uw vennootschap, voor zowel uw kantoor als uw privéruimtes."}}, {"@type": "Question", "name": "Hoe wordt het privégedeelte fiscaal verwerkt?", "acceptedAnswer": {"@type": "Answer", "text": "Voor het privégedeelte wordt een forfaitair voordeel van alle aard aangerekend. De prestaties moeten regelmatig zijn en gebeuren via een onderneming met mensen in dienst. Een abonnement bij Zondags voldoet aan beide. Laat uw accountant dit steeds bevestigen voor uw eigen situatie."}}, {"@type": "Question", "name": "Is mijn Zondag in dienst?", "acceptedAnswer": {"@type": "Answer", "text": "Ja. Elke Zondag is door ons gescreend en in dienst van Zondags. U werkt dus niet met een zelfstandige."}}, {"@type": "Question", "name": "Wat kost een Zondag?", "acceptedAnswer": {"@type": "Answer", "text": "Dat hangt af van het aantal uren en wat u nodig hebt. Na uw aanvraag belt een van ons u binnen één werkdag persoonlijk terug met een voorstel op maat. De eerste 2 uur zijn gratis, om kennis te maken."}}, {"@type": "Question", "name": "Kan ik extra uren bijboeken of opzeggen?", "acceptedAnswer": {"@type": "Answer", "text": "Extra uren bijboeken kan altijd en ze vervallen niet. Uw abonnement is maandelijks opzegbaar."}}]}</script>\n'
hero_h=hero.replace('<h1>','<h1 data-split>')
links='''<section class="links wrap">
  <div class="links__head"><h2>Ontdek <em class="s">Zondags.</em></h2></div>
  <a class="lrow" href="wat-we-doen.html"><span class="lrow__img"><img src="assets/img/04-koken.webp" alt="" loading="lazy"></span><b>Wat we doen<small>Poetsen, koken, de kinderen, de tuin en uw zaak.</small></b><span class="go" aria-hidden="true">&rarr;</span></a>
  <a class="lrow" href="menu.html"><span class="lrow__img"><img src="assets/img/eten-1-bowl.webp" alt="" loading="lazy"></span><b>Ons menu<small>Gezonde schotels, klaar in uw koelkast.</small></b><span class="go" aria-hidden="true">&rarr;</span></a>
  <a class="lrow" href="hoe-het-werkt.html"><span class="lrow__img"><img src="assets/img/05-wassen.webp" alt="" loading="lazy"></span><b>Hoe het werkt<small>Drie stappen, geboekt op uw zaak.</small></b><span class="go" aria-hidden="true">&rarr;</span></a>
  <a class="lrow" href="zondag-worden.html"><span class="lrow__img"><img src="assets/img/03-au-pair.webp" alt="" loading="lazy"></span><b>Zondag worden<small>Vast contract, vaste uren, vaste klanten.</small></b><span class="go" aria-hidden="true">&rarr;</span></a>
</section>
'''
ld='''<script type="application/ld+json">{"@context":"https://schema.org","@type":"LocalBusiness","name":"Zondags","description":"Vaste huishoudelijke medewerker voor ondernemers, geboekt op uw vennootschap.","url":"https://zondags.be","telephone":"+32470565358","email":"hello@zondags.be","address":{"@type":"PostalAddress","streetAddress":"Jan Van Eyckstraat 2","postalCode":"8510","addressLocality":"Marke","addressCountry":"BE"},"areaServed":["West-Vlaanderen","Oost-Vlaanderen"],"openingHours":"Mo-Su 06:00-22:00"}</script>
'''
page('index.html','Zondags | Elke dag een beetje zondag',
 'Een vaste Zondag die u inboekt op uw zaak: poetsen, koken, strijken, de kinderen, boodschappen en de tuin. Voor ondernemers, geboekt op uw vennootschap.',
 hero_h+marquee+openS+stateS+defS+links+BAND, ld)

svc_body=strip_head(svc,r'<div class="svc__head">.*?</div>\s*<div class="svc__pin">','<div class="svc__pin">')
svc_body=svc_body.replace('<section class="svc" id="diensten">','<section class="svc" id="diensten" style="padding-top:20px">',1)
svc_body=re.sub(r'^<section class="svc" id="diensten" style="padding-top:20px">','<section class="svc" id="diensten" style="padding-top:20px">\n    ',svc_body)
ph_svc='''<section class="phero phero--dark">
  <div><p class="eyebrow">Wat we doen</p><h1 data-split><span class="line">Poetsen doen</span><span class="line">we sowieso.</span><span class="line"><em class="s">Maar er is veel meer.</em></span></h1></div>
  <div><p>Een Zondag werkt in huis en uit huis: koken, de kinderen ophalen en begeleiden, strijken, boodschappen, de tuin en uw zaak. Eén vaste persoon voor alles wat u anders zelf zou doen.</p>
  <div class="svc__count" aria-hidden="true"><span id="svcN">01</span><i id="svcBar"></i><span>08</span></div></div>
</section>
'''
page('wat-we-doen.html','Wat we doen | Zondags',
 'Poetsen, was en strijk, koken en boodschappen, de kinderen, tuin, uw kantoor en alles terwijl u weg bent. Eén vaste Zondag voor alles.',
 ph_svc+svc_body+defS.replace('class="def wrap" id="zondag"','class="def wrap" id="zondag" style="padding-bottom:clamp(80px,10vw,140px)"')+BAND)

menu_body=strip_head(menu,r'<p class="eyebrow"[^>]*>Ons menu</p>\s*<h2[^>]*>.*?</h2>\s*','')
menu_body=menu_body.replace('<p class="menu__intro">','<p class="menu__intro" style="margin-top:0">',1)
menu_body=re.sub(r'\s*<div class="float-img".*?</div>','',menu_body,flags=re.S)
page('menu.html','Ons menu | Zondags',
 'Gezonde schotels, vers gemaakt en caloriearm. Uw Zondag brengt ze mee en zet ze in uw koelkast.',
 phero('Ons menu',['Eten staat klaar.','<em class="s">Ook dat.</em>'],'Vers gemaakt, caloriearm en klaar om op te warmen. U vinkt ze aan bij uw aanvraag.')+menu_body+BAND)

how_body=strip_head(how,r'<div class="how__head">.*?</div>\s*</div>\s*','')
how_body=how_body.replace('<section class="how wrap" id="werkwijze">','<section class="how wrap" id="werkwijze" style="padding-top:20px">')
page('hoe-het-werkt.html','Hoe het werkt | Zondags',
 'In drie stappen een vaste Zondag: aanvraag, intake en dan begint het. Geboekt op uw vennootschap met één dienstenfactuur.',
 phero('Hoe het werkt',['Drie stappen.','<em class="s">Dan niets meer.</em>'],'U doet uw aanvraag, wij komen langs voor de intake, en vanaf de eerste week komt dezelfde persoon op hetzelfde moment.')+how_body+fisc+FAQ+BAND, FAQLD)

job_body=strip_head(job,r'<p class="eyebrow">Zondag worden</p>\s*<h2[^>]*>.*?</h2>\s*','')
job_body=job_body.replace('<p class="job__lead">','<p class="job__lead" style="margin-top:0">')
job_body=job_body.replace('href="#solliciteer"','href="#solliciteer"')
page('zondag-worden.html','Zondag worden | Werken bij Zondags',
 'Vast contract, vaste uren, vaste klanten. Geen avonden, geen weekends. Ook voor studenten vanaf 18 jaar. Solliciteer als Zondag.',
 phero('Zondag worden',['Bij ons bent u','geen schoonmaakhulp.','<em class="s">U bent iemands Zondag.</em>'],'Vast contract, vaste uren, vaste klanten. U werkt met een plan dat op voorhand is afgesproken, bij mensen die weten wat u komt doen.')+job_body+apply_)

aanv_body=strip_head(aanv,r'<p class="eyebrow"[^>]*>Aanvraag</p>\s*<h2[^>]*>.*?</h2>\s*','')
aanv_body=aanv_body.replace('<section class="price wrap" id="aanvraag">','<section class="price wrap" id="aanvraag" style="padding-top:20px">')
aanv_body=aanv_body.replace('<p class="price__lead">','<p class="price__lead" style="margin-top:0">')
contact='''<section class="contact wrap" id="contact">
  <div><h3>Bel of WhatsApp</h3><p>0470 56 53 58<br><span style="font-size:16px;color:var(--muted)">Elke dag van 6 tot 22 uur</span></p></div>
  <div><h3>Mail</h3><p>hello@zondags.be</p></div>
  <div><h3>Adres</h3><p>Jan Van Eyckstraat 2<br>8510 Marke</p></div>
</section>
'''
page('aanvraag.html','Vraag uw Zondag aan | Zondags',
 'Vraag vrijblijvend uw Zondag aan. Binnen één werkdag belt een van ons u persoonlijk terug met een voorstel op maat van uw zaak.',
 phero('Aanvraag',['Vraag uw','Zondag aan.'],'Twee minuten werk. Wij doen de rest.')+aanv_body+contact)

page('bedankt.html','Bedankt | Zondags','Bedankt voor uw bericht.',
 '''<section class="thanks-page"><div><p class="eyebrow" style="color:var(--muted)">Goed ontvangen</p><h1>Dank <em class="s">u.</em></h1><p>We hebben uw bericht goed ontvangen en nemen snel contact met u op. Meestal al dezelfde werkdag.</p><a class="btn btn--fill" href="index.html">Terug naar de homepage <span class="arr">&rarr;</span></a></div></section>
''','<meta name="robots" content="noindex">\n')
page('404.html','Pagina niet gevonden | Zondags','Deze pagina bestaat niet.',
 '''<section class="thanks-page"><div><p class="eyebrow" style="color:var(--muted)">404</p><h1>Even <em class="s">zondag.</em></h1><p>Deze pagina bestaat niet, of niet meer.</p><a class="btn btn--fill" href="index.html">Naar de homepage <span class="arr">&rarr;</span></a></div></section>
''','<meta name="robots" content="noindex">\n')

open('robots.txt','w').write('User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: https://zondags.be/sitemap.xml\n')
urls=['','wat-we-doen','menu','hoe-het-werkt','zondag-worden','aanvraag']
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://zondags.be/{u}</loc></url>\n' for u in urls)+'</urlset>\n')
open('CNAME','w').write('zondags.be\n')
print('done')
