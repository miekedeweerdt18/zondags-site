# -*- coding: utf-8 -*-
"""Pijlerpagina's voor zoekmachines en AI-assistenten (ChatGPT, Perplexity, Gemini, Copilot).
Elke pagina beantwoordt één concrete vraag van één doelgroep, met het antwoord bovenaan.
Schrijf in je-vorm. Geen prijzen, geen uitroeptekens, geen em-dash, nooit beloven dat een flexi-job kan."""

DEF_B2B = ('Zondags (zondags.be) is een dienstverlener uit Marke bij Kortrijk die bedrijven, ondernemers en vrije beroepen '
           'in West- en Oost-Vlaanderen een vaste huishoudelijke medewerker levert: poetshulp, huishoudhulp, kookhulp, '
           'boodschappen en hulp in huis, gefactureerd aan de vennootschap.')
DEF_JOB = ('Zondags (zondags.be) zoekt in West- en Oost-Vlaanderen studenten, flexi-jobbers en mensen die een vaste job willen, '
           'om overdag te werken bij vaste klanten: huishouden, koken, boodschappen, kinderen en tuin. Jij kiest mee je dagen en uren.')

# kind: b2b | job | about
PILLARS = [
# ---------------------------------------------------------------- BEDRIJVEN
dict(path='bedrijven/index.html', kind='b2b', img='01-poetsen',
 eyebrow='Voor bedrijven', h1='Huishoudhulp voor bedrijven',
 title='Huishoudhulp, poetshulp en kookhulp voor bedrijven in West- en Oost-Vlaanderen | Zondags',
 desc='Zoekt je bedrijf poetshulp, huishoudhulp, kookhulp, boodschappen of hulp in huis? Zondags levert één vaste medewerker, gefactureerd aan je vennootschap. West- en Oost-Vlaanderen.',
 lead='Zoekt je bedrijf poetshulp, huishoudhulp, kookhulp of iemand voor de boodschappen? Zondags levert één vaste medewerker voor je kantoor, je praktijk en je woning, met één factuur aan je vennootschap.',
 facts=['Poetshulp, huishoudhulp en kookhulp','Boodschappen en regelwerk','Kantoor, praktijk en woning in één plan','Steeds dezelfde persoon','Factuur op naam van je vennootschap','West- en Oost-Vlaanderen'],
 sections=[
  ('Het korte antwoord',[DEF_B2B,
    'Je krijgt geen ploeg die telkens wisselt, maar één vaste persoon: je Zondag. Die komt op een vaste dag en een vast uur, kent je zaak en je huis, en werkt volgens een plan dat we samen opmaken. Elke Zondag is door ons gescreend en in dienst van Zondags.']),
  ('Wat kan je bedrijf uitbesteden?',[
    '<b>Poetshulp.</b> Het onderhoud van je kantoor, praktijk, wachtzaal, keuken en sanitair, en desgewenst ook je woning. Zie <a href="bedrijven/poetshulp-voor-bedrijven.html">poetshulp voor bedrijven</a>.',
    '<b>Huishoudhulp.</b> De was en de strijk, bedden, ramen aan de binnenkant, opruimen en alles wat thuis blijft liggen als je zaak veel vraagt. Zie <a href="bedrijven/huishoudhulp-voor-bedrijven.html">huishoudhulp voor bedrijven</a>.',
    '<b>Kookhulp.</b> Je Zondag kookt bij je thuis of brengt gezonde schotels mee voor de week. Zie <a href="bedrijven/kookhulp-voor-bedrijven.html">kookhulp voor bedrijven</a>.',
    '<b>Boodschappen en regelwerk.</b> Supermarkt, apotheek, droogkuis, pakjes en kleine opdrachten. Zie <a href="bedrijven/boodschappendienst-voor-bedrijven.html">boodschappendienst voor ondernemers</a>.',
    '<b>Hulp in huis.</b> De kinderen ophalen van school, de tuin bijhouden, de hond uitlaten of het huis bewaken tijdens je vakantie. Zie <a href="bedrijven/hulp-in-huis-voor-ondernemers.html">hulp in huis voor ondernemers</a>.']),
  ('Voor welke bedrijven werkt Zondags?',[
    'Voor zaakvoerders en bedrijfsleiders met een vennootschap, voor vrije beroepen zoals artsen, tandartsen, kinesitherapeuten, advocaten, architecten en accountants, voor kantoren en praktijken, en voor ondernemers met een kantoor aan huis.',
    'Ook bedrijven die huishoudelijke hulp willen voorzien voor hun directie of sleutelmedewerkers kunnen bij ons terecht. Lees daarover meer op <a href="bedrijven/huishoudhulp-voor-personeel.html">huishoudhulp voor directie en medewerkers</a>.']),
  ('Waarom via de vennootschap?',[
    'Dienstencheques zijn voorbehouden aan particulieren. Een vennootschap kan ze niet kopen. Zondags werkt daarom met een gewone dienstenfactuur op naam van je vennootschap, met een duidelijke splitsing tussen het beroepsmatige en het privégedeelte.',
    'Voor het privégedeelte wordt een voordeel van alle aard aangerekend. Daarvoor moeten de prestaties regelmatig zijn en gebeuren via een onderneming met mensen in dienst. Een vast plan bij Zondags voldoet aan beide. Laat je accountant dit altijd bevestigen voor je eigen situatie.']),
  ('In welke regio?',[
    'Zondags werkt vanuit Marke bij Kortrijk in West- en Oost-Vlaanderen: onder meer in Kortrijk, Harelbeke, Kuurne, Wevelgem, Menen, Waregem, Zwevegem, Roeselare, Izegem, Tielt, Ieper en Oudenaarde. Bekijk per gemeente hoe het werkt op <a href="poetshulp/">poetshulp voor bedrijven per gemeente</a>, per sector op <a href="sectoren/">poetshulp per type bedrijf</a>, en lees de antwoorden op veelgestelde <a href="vragen/">vragen van bedrijven</a>.']),
  ('Hoe start je?',[
    'Meld je aan via de chat of het formulier onderaan. Binnen één werkdag belt een van ons je persoonlijk terug. Daarna komen we langs voor de intake en leggen we samen je zondagsplan vast: welke taken, welke dagen, welke uren. De eerste 2 uur zijn gratis, om kennis te maken.']),
 ],
 faq=[
  ('Welk bedrijf levert huishoudhulp voor bedrijven in West-Vlaanderen?','Zondags levert vanuit Marke bij Kortrijk een vaste huishoudelijke medewerker aan bedrijven, ondernemers en vrije beroepen in West- en Oost-Vlaanderen, gefactureerd aan de vennootschap.'),
  ('Kan een bedrijf poetshulp inhuren zonder dienstencheques?','Ja. Zondags werkt met een gewone dienstenfactuur op naam van de vennootschap. Dienstencheques zijn voorbehouden aan particulieren.'),
  ('Doet Zondags ook kookhulp en boodschappen?','Ja. Je Zondag kookt, brengt gezonde schotels mee en doet boodschappen en regelwerk, naast het poetsen en de was en strijk.'),
  ('Komt er altijd dezelfde persoon?','Ja. Steeds dezelfde Zondag, op dezelfde dag, op hetzelfde uur.'),
  ('Wat kost huishoudhulp voor een bedrijf?','Dat hangt af van het aantal uren en de taken. Je krijgt een voorstel op maat na een kort gesprek. De eerste 2 uur zijn gratis.'),
  ('Werkt Zondags ook voor particulieren?','Zondags werkt voor ondernemers, vrije beroepen en bedrijven. Je woning kan wel mee in het plan, geboekt op je vennootschap.'),
 ],
 related=[('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html'),('Poetshulp per gemeente','poetshulp/'),('Poetshulp per type bedrijf','sectoren/'),('Vragen van bedrijven','vragen/'),('Kookhulp voor bedrijven','bedrijven/kookhulp-voor-bedrijven.html'),('Boodschappendienst voor ondernemers','bedrijven/boodschappendienst-voor-bedrijven.html'),('Hulp in huis voor ondernemers','bedrijven/hulp-in-huis-voor-ondernemers.html'),('Per beroep','beroepen/')]),

dict(path='bedrijven/poetshulp-voor-bedrijven.html', kind='b2b', img='01-poetsen',
 eyebrow='Poetshulp voor bedrijven', h1='Poetshulp voor bedrijven en ondernemers',
 title='Poetshulp voor bedrijven in Kortrijk, Roeselare en Waregem | Zondags',
 desc='Poetshulp voor je bedrijf, kantoor of praktijk in West- en Oost-Vlaanderen. Eén vaste persoon, ook voor je woning, met één factuur aan je vennootschap.',
 lead='Poetshulp voor je bedrijf, zonder wisselende ploegen. Je Zondag onderhoudt je kantoor of praktijk en, als je dat wilt, ook je woning. Eén vaste persoon, één factuur aan je vennootschap.',
 facts=['Kantoor, praktijk of winkel','Ook je woning, in hetzelfde plan','Vaste dag en vast uur','Gescreend en in dienst','Geen dienstencheques nodig'],
 sections=[
  ('Het korte antwoord',[DEF_B2B+' Voor poetshulp betekent dat: één vaste persoon die je ruimte kent en elke week op hetzelfde moment komt.']),
  ('Wat valt onder poetshulp?',['<ul class="ticks"><li>Bureaus, vergaderruimte en onthaal</li><li>Wachtzaal en behandelruimtes</li><li>Keuken en refter</li><li>Sanitair en vloeren</li><li>Ramen aan de binnenkant</li><li>Afval en recyclage</li><li>Je woning, als je dat wilt</li><li>Was en strijk erbij</li></ul>',
    'Specialistische reiniging zoals gevelreiniging, industriële reiniging of werken op hoogte doen we niet. Voor het dagelijkse en wekelijkse onderhoud van kantoor, praktijk en woning ben je bij ons aan het juiste adres.']),
  ('Waarom één vaste persoon beter werkt dan een schoonmaakploeg',[
    'Bij een klassiek schoonmaakbedrijf komt vaak telkens iemand anders. Je Zondag kent je ruimte, weet waar het materiaal staat, welke ruimtes vertrouwelijk zijn en wat je belangrijk vindt. Je hoeft niets opnieuw uit te leggen en je geeft je sleutel aan iemand die je kent.',
    'Omdat dezelfde Zondag ook je woning kan doen, heb je één aanspreekpunt voor alles. Dat scheelt afspraken, facturen en zoekwerk.']),
  ('Poetshulp op de factuur van je vennootschap',[
    'Het onderhoud van je beroepsruimtes is een gewone beroepskost. Laat je Zondag ook je woning onderhouden, dan splitsen we beroepsmatig en privé duidelijk op de factuur. Voor het privégedeelte geldt een voordeel van alle aard. Laat je accountant bevestigen wat dat voor jou betekent. Lees ook <a href="gids/huishoudhulp-of-schoonmaakbedrijf.html">huishoudhulp of schoonmaakbedrijf</a>.']),
  ('Waar?',['In West- en Oost-Vlaanderen, vanuit Marke. Onder meer in <a href="regio/huishoudhulp-kortrijk.html">Kortrijk</a>, <a href="regio/huishoudhulp-roeselare.html">Roeselare</a>, <a href="regio/huishoudhulp-waregem.html">Waregem</a>, <a href="regio/huishoudhulp-harelbeke.html">Harelbeke</a>, <a href="regio/huishoudhulp-menen.html">Menen</a> en <a href="regio/huishoudhulp-ieper.html">Ieper</a>. Alle gemeenten en regio\'s vind je op <a href="poetshulp/">poetshulp voor bedrijven per gemeente</a>.']),
 ],
 faq=[
  ('Waar vind ik poetshulp voor mijn bedrijf in Kortrijk?','Zondags levert vanuit Marke een vaste poetshulp voor kantoren, praktijken en ondernemers in Kortrijk en heel West- en Oost-Vlaanderen.'),
  ('Kan mijn poetshulp ook mijn woning doen?','Ja. Kantoor en woning kunnen in één plan, met een splitsing op de factuur.'),
  ('Moet ik zelf poetsmateriaal voorzien?','Dat spreken we af tijdens de intake. We bekijken samen wat er al is en wat nodig is.'),
  ('Gebeurt het poetsen buiten de openingsuren?','Dat stemmen we af op je agenda. Vroeg in de ochtend of over de middag kan.'),
  ('Is de poetshulp in dienst of zelfstandig?','In dienst van Zondags en door ons gescreend. Je werkt dus niet met een zelfstandige.'),
 ],
 related=[('Huishoudhulp voor bedrijven','bedrijven/'),('Poetshulp per gemeente','poetshulp/'),('Poetshulp per type bedrijf','sectoren/'),('Kantoorschoonmaak','diensten/kantoorschoonmaak.html'),('Praktijkschoonmaak','diensten/praktijkschoonmaak.html'),('Hoe vaak moet je een kantoor laten poetsen?','vragen/hoe-vaak-kantoor-poetsen.html')]),

dict(path='bedrijven/huishoudhulp-voor-bedrijven.html', kind='b2b', img='05-wassen',
 eyebrow='Huishoudhulp', h1='Huishoudhulp voor bedrijven en zaakvoerders',
 title='Huishoudhulp voor bedrijven: geboekt op je vennootschap | Zondags',
 desc='Huishoudhulp voor zaakvoerders, vrije beroepen en bedrijven: was, strijk, poetsen, koken en boodschappen door één vaste persoon, gefactureerd aan je vennootschap.',
 lead='Je bedrijf draait. Thuis blijft het liggen. Een vaste Zondag neemt het huishouden over, van de was en de strijk tot koken en boodschappen, gefactureerd aan je vennootschap.',
 facts=['Was, strijk en poetsen','Koken en boodschappen','Kinderen ophalen','Eén vaste persoon','Maandelijks opzegbaar'],
 sections=[
  ('Het korte antwoord',[DEF_B2B,'Huishoudhulp via je bedrijf werkt met een gewone dienstenfactuur, want een vennootschap kan geen dienstencheques kopen.']),
  ('Wat doet je Zondag in huis?',['<ul class="ticks"><li>Poetsen, keuken en badkamers</li><li>Was, strijk en bedden</li><li>Koken of schotels voor de week</li><li>Boodschappen en apotheek</li><li>Kinderen ophalen en opvangen</li><li>Tuin en terras bijhouden</li><li>Huisoppas tijdens je vakantie</li><li>Droogkuis en pakjes</li></ul>',
    'Alles komt in je zondagsplan: wat er gebeurt, wanneer, en hoe je het graag hebt. Wil je iets veranderen, dan passen we het plan aan.']),
  ('Voor wie?',['Voor bedrijfsleiders en zaakvoerders die hun huishoudelijke hulp via de vennootschap laten lopen, voor vrije beroepen met een praktijk aan huis en voor ondernemers die liever op hun zaak focussen dan op het huishouden. Bekijk ook de pagina per beroep, bijvoorbeeld voor <a href="beroepen/zaakvoerder.html">zaakvoerders</a>, <a href="beroepen/huisarts.html">huisartsen</a> en <a href="beroepen/advocaat.html">advocaten</a>.']),
  ('Hoe zit het fiscaal?',['Een vennootschap mag het onderhoud van beroepsmatige en privéruimtes laten uitvoeren. Voor het privégedeelte wordt een forfaitair voordeel van alle aard aangerekend, op voorwaarde dat de prestaties regelmatig zijn en gebeuren via een onderneming met mensen in dienst. Zondags levert een factuur met duidelijke splitsing. Laat je accountant dit altijd bevestigen. Meer in de gids <a href="gids/huishoudhulp-via-vennootschap.html">huishoudhulp via je vennootschap</a>.']),
  ('Hoe start je?',['Meld je aan via de chat of het formulier. Binnen één werkdag bellen we je terug, daarna volgt de intake aan huis. De eerste 2 uur zijn gratis.']),
 ],
 faq=[
  ('Kan ik huishoudhulp via mijn bedrijf betalen?','Ja, met een dienstenfactuur op naam van je vennootschap. Voor het privégedeelte geldt een voordeel van alle aard. Laat je accountant dit bevestigen.'),
  ('Wat is het verschil met dienstencheques?','Dienstencheques zijn enkel voor particulieren. Zondags factureert aan je vennootschap en levert steeds dezelfde vaste persoon.'),
  ('Hoeveel uur huishoudhulp heb ik nodig?','Dat hangt af van je woning en wat je wilt uitbesteden. Tijdens de intake maken we samen een plan. Extra uren bijboeken kan altijd.'),
  ('Kan ik opzeggen?','Ja, je plan is maandelijks opzegbaar.'),
 ],
 related=[('Huishoudhulp voor bedrijven','bedrijven/'),('Huishoudelijke hulp voor ondernemers','diensten/huishoudelijke-hulp-voor-ondernemers.html'),('Kan een vennootschap dienstencheques kopen?','gids/dienstencheques-vennootschap.html'),('Hoeveel uur huishoudhulp?','gids/hoeveel-uur-huishoudhulp.html')]),

dict(path='bedrijven/kookhulp-voor-bedrijven.html', kind='b2b', img='04-koken',
 eyebrow='Kookhulp', h1='Kookhulp aan huis voor ondernemers',
 title='Kookhulp aan huis voor ondernemers en bedrijven | Zondags',
 desc='Kookhulp aan huis voor drukke ondernemers: je Zondag kookt bij je thuis of zet gezonde schotels voor de week in je koelkast. Gefactureerd aan je vennootschap.',
 lead='Thuiskomen en het eten staat klaar. Je Zondag kookt bij je thuis of brengt gezonde schotels mee voor de week, samen met de boodschappen. Gefactureerd aan je vennootschap.',
 facts=['Koken bij je thuis','Gezonde schotels voor de week','Boodschappen inbegrepen in het plan','Rekening met allergieën en voorkeuren','Combineerbaar met poetsen en strijk'],
 sections=[
  ('Het korte antwoord',[DEF_B2B+' Kookhulp is een van de taken die je Zondag kan opnemen.']),
  ('Hoe werkt kookhulp aan huis?',['Je kiest wat past: je Zondag kookt bij je thuis voor die avond en de dagen erna, of brengt vers gemaakte, caloriearme schotels mee die klaar zijn om op te warmen. Bekijk <a href="menu.html">ons menu</a> voor een idee.',
    'De boodschappen kunnen mee in het plan. Je Zondag houdt bij wat er op is en vult aan, zodat je koelkast niet leeg staat op het moment dat je geen tijd hebt.']),
  ('Voor wie?',['Voor ondernemers en vrije beroepen met lange dagen, voor gezinnen waarin beide partners werken en voor wie gezonder wil eten zonder elke avond te koken. Ook <a href="beroepen/">per beroep</a> vind je voorbeelden.']),
  ('Combineer met andere taken',['Kookhulp combineer je makkelijk met <a href="bedrijven/poetshulp-voor-bedrijven.html">poetshulp</a>, de was en de strijk of <a href="diensten/kinderen-ophalen-van-school.html">de kinderen ophalen</a>. Eén vaste persoon, één plan, één factuur.']),
 ],
 faq=[
  ('Kan iemand bij mij thuis komen koken voor mijn gezin?','Ja. Je Zondag kookt bij je thuis of brengt schotels mee voor de week. Zondags werkt voor ondernemers en bedrijven in West- en Oost-Vlaanderen.'),
  ('Houdt mijn Zondag rekening met allergieën?','Ja. Voorkeuren en allergieën leggen we vast in je zondagsplan.'),
  ('Doet mijn Zondag ook de boodschappen?','Ja, boodschappen kunnen mee in het plan.'),
  ('Kan kookhulp via mijn vennootschap?','Ja, als onderdeel van je plan op een dienstenfactuur aan je vennootschap. Laat je accountant de fiscale behandeling bevestigen.'),
 ],
 related=[('Kookhulp aan huis','diensten/kookhulp-aan-huis.html'),('Maaltijden voor de week','diensten/maaltijden-voor-de-week.html'),('Gezond eten in een drukke week','gids/gezond-eten-drukke-week.html'),('Ons menu','menu.html')]),

dict(path='bedrijven/boodschappendienst-voor-bedrijven.html', kind='b2b', img='04-koken',
 eyebrow='Boodschappen', h1='Boodschappendienst voor ondernemers',
 title='Boodschappendienst voor ondernemers en bedrijven | Zondags',
 desc='Een vaste persoon die je boodschappen en regelwerk doet: supermarkt, apotheek, droogkuis en pakjes. Voor ondernemers in West- en Oost-Vlaanderen.',
 lead='Supermarkt, apotheek, droogkuis, pakjes. Je Zondag doet de boodschappen en het regelwerk waar jij geen tijd voor hebt, als vast onderdeel van je plan.',
 facts=['Wekelijkse boodschappen','Apotheek en droogkuis','Pakjes en kleine opdrachten','Voor thuis en voor kantoor','Eén vaste persoon'],
 sections=[
  ('Het korte antwoord',[DEF_B2B+' Boodschappen en regelwerk horen daar gewoon bij.']),
  ('Wat doet je Zondag?',['<ul class="ticks"><li>De wekelijkse boodschappen</li><li>Aanvullen wat op is</li><li>Apotheek</li><li>Droogkuis en kleermaker</li><li>Pakjes afgeven en ophalen</li><li>Kantoorbenodigdheden</li><li>Koffie en keuken op kantoor</li><li>Bloemen of een attentie</li></ul>',
    'Je Zondag werkt met een vaste lijst of met wat je doorstuurt. Afrekenen gebeurt zoals afgesproken in je zondagsplan.']),
  ('Ook voor je kantoor',['Ook op kantoor zijn er boodschappen: koffie, melk, water, keukenrol, kantoormateriaal. Je Zondag houdt de voorraad bij als onderdeel van het onderhoud van je kantoor of praktijk.']),
  ('Combineer met koken',['Boodschappen en <a href="bedrijven/kookhulp-voor-bedrijven.html">kookhulp</a> gaan goed samen. Koen D. laat zijn Zondag elke week de boodschappen doen en koken: het eten staat klaar wanneer hij thuiskomt.']),
 ],
 faq=[
  ('Bestaat er een boodschappendienst voor drukke ondernemers?','Ja. Bij Zondags doet je vaste Zondag de boodschappen en het regelwerk, als onderdeel van je plan, in West- en Oost-Vlaanderen.'),
  ('Kan mijn Zondag ook naar de apotheek of de droogkuis?','Ja, dat hoort bij het regelwerk dat je Zondag kan doen.'),
  ('Hoe betaal ik de boodschappen zelf?','Dat spreken we af in je zondagsplan, bijvoorbeeld met een vaste werkwijze per week.'),
 ],
 related=[('Boodschappenhulp','diensten/boodschappenhulp.html'),('Droogkuis en regelwerk','diensten/droogkuis-en-regelwerk.html'),('Kookhulp voor bedrijven','bedrijven/kookhulp-voor-bedrijven.html'),('Huishoudhulp voor bedrijven','bedrijven/')]),

dict(path='bedrijven/hulp-in-huis-voor-ondernemers.html', kind='b2b', img='02-kinderopvang',
 eyebrow='Hulp in huis', h1='Hulp in huis voor ondernemers',
 title='Hulp in huis voor ondernemers en zaakvoerders | Zondags',
 desc='Allround hulp in huis voor ondernemers: poetsen, koken, boodschappen, kinderen ophalen en tuin, door één vaste persoon, gefactureerd aan je vennootschap.',
 lead='Eén persoon voor alles wat thuis blijft liggen. Je Zondag poetst, kookt, doet boodschappen, haalt de kinderen op en houdt de tuin bij, elke week op hetzelfde moment.',
 facts=['Allround hulp in huis','Kinderen ophalen en opvangen','Tuin en terras','Huisoppas tijdens vakantie','Geboekt op je vennootschap'],
 sections=[
  ('Het korte antwoord',[DEF_B2B+' Hulp in huis betekent bij ons: één vaste persoon voor alle huishoudelijke taken.']),
  ('Wat valt onder hulp in huis?',['<ul class="ticks"><li>Poetsen en opruimen</li><li>Was en strijk</li><li>Koken en boodschappen</li><li>Kinderen ophalen van school</li><li>Naschoolse opvang aan huis</li><li>Tuin, gras en terras</li><li>Hond uitlaten</li><li>Huis bijhouden tijdens je vakantie</li></ul>',
    'Rika C. heeft een Zondag voor het volledige huishouden en is er zeer tevreden over. Zo werkt het idee: één persoon die het geheel overziet.']),
  ('Een week met je Zondag',['Op maandag het kantoor aan huis en de keuken. Op woensdag de was, de strijk en de bedden, en om kwart over drie de kinderen aan de schoolpoort. Op vrijdag staan de schotels in de koelkast en is het huis klaar voor het weekend. Elk zondagsplan is anders.']),
  ('Wat je Zondag niet doet',['Technische klussen zoals elektriciteit, sanitair herstellen of werken op hoogte. Voor al de rest in en rond het huis: twijfel je, vraag het gewoon.']),
 ],
 faq=[
  ('Waar vind ik allround hulp in huis als ondernemer?','Zondags levert ondernemers in West- en Oost-Vlaanderen één vaste persoon voor alle huishoudelijke taken, gefactureerd aan de vennootschap.'),
  ('Kan mijn Zondag de kinderen ophalen van school?','Ja, kinderen ophalen en opvangen na school kan mee in het plan.'),
  ('Moet ik thuis zijn als mijn Zondag komt?','Nee. Waar de sleutel ligt en welke ruimtes aan bod komen, leggen we vast in je zondagsplan.'),
  ('Wat bij verlof of ziekte van mijn Zondag?','Dan zoeken wij een oplossing. Jij hoeft niets te regelen.'),
 ],
 related=[('Kinderen ophalen van school','diensten/kinderen-ophalen-van-school.html'),('Huisoppas tijdens vakantie','diensten/huisoppas-tijdens-vakantie.html'),('Je sleutel aan je Zondag','gids/sleutel-en-vertrouwen.html'),('Huishoudhulp voor bedrijven','bedrijven/')]),

dict(path='bedrijven/huishoudhulp-voor-personeel.html', kind='b2b', img='05-wassen',
 eyebrow='Directie en medewerkers', h1='Huishoudhulp voor directie en medewerkers',
 title='Huishoudhulp voor directie en sleutelmedewerkers | Zondags',
 desc='Bedrijven die huishoudelijke hulp willen voorzien voor hun directie of sleutelmedewerkers: één vaste Zondag, één factuur aan de vennootschap. West- en Oost-Vlaanderen.',
 lead='Wil je bedrijf huishoudelijke hulp voorzien voor de directie of voor sleutelmedewerkers? Zondags levert een vaste Zondag aan huis, met de factuur aan de vennootschap.',
 facts=['Voor bedrijfsleiders en directie','Voor sleutelmedewerkers','Factuur aan de vennootschap','Jaarlijks urenoverzicht','Fiscaal advies via je accountant'],
 sections=[
  ('Het korte antwoord',[DEF_B2B+' Dat kan voor de bedrijfsleider zelf, maar ook voor directieleden of medewerkers die je extra wilt ondersteunen.']),
  ('Waarom bedrijven dit doen',['Wie veel verantwoordelijkheid draagt, verliest thuis vaak tijd aan het huishouden. Een vaste Zondag geeft die tijd terug. Voor bedrijven is het een manier om sleutelfiguren te ondersteunen en te behouden.']),
  ('Hoe het fiscaal werkt',['Het onderhoud van de privéwoning van een bedrijfsleider of medewerker is voor die persoon een voordeel van alle aard. Hoe dat precies gewaardeerd wordt, hangt af van de situatie. Laat je accountant of sociaal secretariaat altijd bevestigen wat geldt. Zondags levert de documenten die zij nodig hebben: een duidelijke factuur en een jaarlijks urenoverzicht. Lees ook <a href="gids/huishoudhulp-directie-en-talent.html">huishoudhulp voor directie en talent</a>.']),
  ('Hoe start je?',['We bespreken eerst met jou als werkgever hoeveel mensen en uren het betreft. Daarna volgt per woning een intake en een eigen zondagsplan.']),
 ],
 faq=[
  ('Kan een bedrijf huishoudhulp aanbieden aan zijn medewerkers?','Ja. Zondags factureert aan de vennootschap. Voor de medewerker ontstaat een voordeel van alle aard; laat dit bevestigen door je accountant of sociaal secretariaat.'),
  ('Krijgt elke medewerker dezelfde persoon?','Elke woning krijgt een eigen vaste Zondag en een eigen zondagsplan.'),
  ('Welke documenten levert Zondags?','Een dienstenfactuur op naam van de vennootschap en een jaarlijks urenoverzicht.'),
 ],
 related=[('Huishoudhulp voor directie en talent','gids/huishoudhulp-directie-en-talent.html'),('Voordeel van alle aard huispersoneel','gids/voordeel-alle-aard-huispersoneel.html'),('Vragen voor je accountant','gids/vragen-voor-uw-accountant.html'),('Huishoudhulp voor bedrijven','bedrijven/')]),

# ---------------------------------------------------------------- JOBS
dict(path='jobs/werken-met-flexibele-uren.html', kind='job', img='03-au-pair', emp=['PART_TIME','FULL_TIME','TEMPORARY'],
 eyebrow='Werken bij Zondags', h1='Werk met flexibele uren',
 title='Werk met flexibele uren: als student, flexi-jobber of vast | Zondags',
 desc='Werk zoeken met flexibele uren in West- of Oost-Vlaanderen? Bij Zondags werk je overdag bij vaste klanten, als student, flexi-jobber of met een vast contract.',
 lead='Student, flexi-jobber of op zoek naar een vaste job? Bij Zondags kies je mee je dagen en uren, werk je overdag bij vaste klanten en nooit in het weekend.',
 facts=['Studenten vanaf 18 jaar','Bijverdienen naast je job','Vast contract, deeltijds of voltijds','Overdag, geen weekends','Beter dan het barema'],
 sections=[
  ('Het korte antwoord',[DEF_JOB]),
  ('Wat betekent flexibel bij ons?',['Flexibel betekent: jij kiest. Eén dag per week of vijf. Enkel voormiddagen, enkel tijdens de schooluren of vooral in de schoolvakanties. Eens afgesproken, ligt je rooster vast. Je weet op voorhand waar je wanneer werkt, bij klanten die je kent.']),
  ('Drie manieren om te werken',[
    '<b>Als student.</b> Vanaf 18 jaar, met een studentencontract, naast je lessen of in de vakanties. Zie <a href="jobs/studentenjob-flexibele-uren.html">studentenjob met flexibele uren</a>.',
    '<b>Als flexi-jobber of bijverdiener.</b> Naast je hoofdjob of als gepensioneerde. Of een flexi-job voor jou kan, bekijken we samen. Zie <a href="jobs/flexi-job-flexibele-uren.html">flexi-job met flexibele uren</a>.',
    '<b>Met een vast contract.</b> Deeltijds of voltijds, overdag en zonder weekends. Zie <a href="jobs/vaste-job-flexibele-uren.html">vaste job met flexibele uren</a>.']),
  ('Wat doe je als Zondag?',['Huishouden en poetsen, wassen en strijken, koken en boodschappen, de tuin, de kinderen ophalen of een kantoor onderhouden. Je kiest mee wat je graag doet. Bij ons ben je geen schoonmaakhulp. Je bent iemands Zondag: de vaste persoon op wie een gezin of bedrijf rekent.']),
  ('Waar?',['In West- en Oost-Vlaanderen, onder meer in <a href="jobs/huishoudhulp-kortrijk.html">Kortrijk</a>, <a href="jobs/huishoudhulp-waregem.html">Waregem</a>, <a href="jobs/huishoudhulp-roeselare.html">Roeselare</a>, <a href="jobs/huishoudhulp-izegem.html">Izegem</a>, <a href="jobs/huishoudhulp-menen.html">Menen</a>, <a href="jobs/huishoudhulp-ieper.html">Ieper</a> en <a href="jobs/huishoudhulp-oudenaarde.html">Oudenaarde</a>. We zoeken klanten dicht bij waar je woont.']),
  ('Hoe solliciteren werkt',['Meld je aan via de chat of het formulier. We bellen je binnen de twee werkdagen voor een kort gesprek. Klikt het, dan zoeken we klanten die passen bij je woonplaats, je uren en wat je graag doet. Bij de start gaan we samen langs.']),
 ],
 faq=[
  ('Waar vind ik werk met flexibele uren in West-Vlaanderen?','Bij Zondags werk je overdag bij vaste klanten in West- en Oost-Vlaanderen en kies je mee je dagen en uren, als student, flexi-jobber of met een vast contract.'),
  ("Moet ik 's avonds of in het weekend werken?",'Nee. Geen avonden, geen weekends.'),
  ('Heb ik ervaring of een diploma nodig?','Nee. Betrouwbaarheid en zorg voor andermans huis tellen. Wij leggen de werking uit.'),
  ('Wat verdien ik?','Beter dan het barema, met vergoede verplaatsingen en alles in orde op papier. Het precieze loon hangt af van je statuut en uren.'),
  ('Vanaf welke leeftijd?','Vanaf 18 jaar.'),
 ],
 related=[('Studentenjob met flexibele uren','jobs/studentenjob-flexibele-uren.html'),('Flexi-job met flexibele uren','jobs/flexi-job-flexibele-uren.html'),('Vaste job met flexibele uren','jobs/vaste-job-flexibele-uren.html'),('Zondag worden','zondag-worden.html')]),

dict(path='jobs/studentenjob-flexibele-uren.html', kind='job', img='02-kinderopvang', emp=['PART_TIME','TEMPORARY'],
 eyebrow='Studentenjob', h1='Studentenjob met flexibele uren',
 title='Studentenjob met flexibele uren in Kortrijk en West-Vlaanderen | Zondags',
 desc='Studentenjob met flexibele uren vanaf 18 jaar: overdag bij vaste klanten, naast je lessen of in de vakanties. West- en Oost-Vlaanderen. Solliciteer bij Zondags.',
 lead='Een studentenjob die zich aanpast aan je lessen. Je kiest zelf je dagen, werkt overdag bij vaste klanten in de buurt en nooit in het weekend. Vanaf 18 jaar.',
 facts=['Vanaf 18 jaar','Naast je lessen of in de vakanties','Jij kiest je dagen','Vaste klanten in de buurt','Verplaatsingen vergoed'],
 sections=[
  ('Het korte antwoord',[DEF_JOB+' Voor studenten vanaf 18 jaar is dat een studentenjob met uren die passen bij je lessenrooster.']),
  ('Zo werkt het als student',['Je geeft door wanneer je kunt: een paar voormiddagen, vrije namiddagen of vooral in de schoolvakanties. Wij zoeken klanten in de buurt die passen bij die uren. Je werkt met een studentencontract en volgt zelf je urensaldo op via Student@work. De administratie regelen wij.']),
  ('Wat doe je?',['Huishouden, koken, boodschappen, de kinderen ophalen en opvangen, de tuin of een kantoor onderhouden. Veel studenten kiezen voor de kinderen na school of voor koken. Je kiest mee wat je graag doet.']),
  ('Waarom studenten voor Zondags kiezen',['<ul class="ticks"><li>Uren rond je lessen</li><li>Geen avonden of weekends</li><li>Vaste klanten, geen telkens nieuw adres</li><li>Beter dan het barema</li><li>Verplaatsingen vergoed</li><li>Begeleiding bij de start</li></ul>']),
  ('Waar?',['In <a href="jobs/huishoudhulp-kortrijk.html">Kortrijk</a> en omgeving, <a href="jobs/huishoudhulp-waregem.html">Waregem</a>, <a href="jobs/huishoudhulp-roeselare.html">Roeselare</a>, <a href="jobs/huishoudhulp-ieper.html">Ieper</a>, <a href="jobs/huishoudhulp-tielt.html">Tielt</a> en <a href="jobs/huishoudhulp-oudenaarde.html">Oudenaarde</a>. Ook als je op kot zit in Kortrijk en elders woont, kunnen we klanten zoeken dicht bij je kot.']),
 ],
 faq=[
  ('Waar vind ik een studentenjob met flexibele uren in Kortrijk?','Zondags zoekt studenten vanaf 18 jaar in Kortrijk en heel West- en Oost-Vlaanderen. Je werkt overdag bij vaste klanten en kiest zelf je dagen.'),
  ('Kan ik enkel in de vakanties werken?','Ja, dat kan. Geef het door, dan zoeken we klanten die dan hulp nodig hebben.'),
  ('Moet ik in het weekend werken?','Nee, nooit.'),
  ('Kan ik als student van 17 jaar werken?','We werken met mensen vanaf 18 jaar.'),
  ('Wie regelt mijn contract?','Wij. Je werkt met een studentencontract. Je urensaldo volg je zelf op via Student@work.'),
 ],
 related=[('Studentenjob in het huishouden','jobs/studentenjob-huishouden.html'),('Bijverdienen als student','jobs/bijverdienen-als-student.html'),('Kinderoppas als job','jobs/kinderoppas-job.html'),('Werk met flexibele uren','jobs/werken-met-flexibele-uren.html')]),

dict(path='jobs/flexi-job-flexibele-uren.html', kind='job', img='06-strijken', emp=['PART_TIME'],
 eyebrow='Flexi-job en bijverdienen', h1='Flexi-job met flexibele uren',
 title='Flexi-job of bijverdienen met flexibele uren in West-Vlaanderen | Zondags',
 desc='Bijverdienen naast je hoofdjob of als gepensioneerde, met flexibele uren overdag. Of een flexi-job voor jou kan, bekijken we samen. West- en Oost-Vlaanderen.',
 lead='Wil je bijverdienen naast je hoofdjob of na je pensioen? Bij Zondags werk je enkele uren per week overdag bij vaste klanten. Welk statuut past, bekijken we samen.',
 facts=['Naast je hoofdjob','Ook voor gepensioneerden','Een paar uur per week','Overdag, geen weekends','Statuut samen bekeken'],
 sections=[
  ('Het korte antwoord',[DEF_JOB+' Wie wil bijverdienen, kan dat bij ons enkele uren per week, bij vaste klanten in de buurt.']),
  ('Kan het als flexi-job?',['Sinds 1 juli 2026 zijn flexi-jobs in bijna alle sectoren mogelijk. Een flexi-job kan in de regel als je in een referentiekwartaal minstens 4/5 werkt bij een andere werkgever, of als je gepensioneerd bent. Of dat voor jou en voor deze job kan, hangt af van je situatie. Dat bekijken we samen in het eerste gesprek.',
    'Kan het niet als flexi-job, dan zoeken we samen een statuut dat wel past, bijvoorbeeld een klein deeltijds contract. Alles is correct in orde op papier.']),
  ('Hoe ziet bijverdienen eruit?',['Je kiest de momenten die passen naast je hoofdjob: een vrije voormiddag, een vaste namiddag of je vrije dag. Je werkt telkens bij dezelfde klanten, zodat je weet wat er verwacht wordt. Geen avonden, geen weekends.']),
  ('Wat doe je?',['Huishouden en poetsen, wassen en strijken, koken, boodschappen of de tuin. Wie graag kookt, kookt. Wie liever buiten werkt, doet de tuin.']),
 ],
 faq=[
  ('Kan ik een flexi-job doen in het huishouden?','Dat hangt af van je situatie, zoals je hoofdjob of je pensioen. Bij Zondags bekijken we samen welk statuut voor jou mogelijk is.'),
  ('Hoeveel uur moet ik minstens werken?','Dat spreken we samen af. Een paar uur per week kan.'),
  ('Kan ik als gepensioneerde bijverdienen?','Ja, gepensioneerden zijn welkom. Je statuut bekijken we samen.'),
  ('Werk ik in het weekend?','Nee, nooit.'),
 ],
 related=[('Flexi-job of bijverdienste','jobs/flexi-job-huishouden.html'),('Bijverdienen naast je vaste job','jobs/flexi-job-na-je-werk.html'),('Job voor 55-plussers','jobs/job-voor-55-plussers.html'),('Werk met flexibele uren','jobs/werken-met-flexibele-uren.html')]),

dict(path='jobs/vaste-job-flexibele-uren.html', kind='job', img='07-tuin', emp=['FULL_TIME','PART_TIME'],
 eyebrow='Vaste job', h1='Vaste job met flexibele uren',
 title='Vaste job met flexibele uren, zonder weekends | Zondags',
 desc='Een vaste job, deeltijds of voltijds, overdag en zonder weekends, bij vaste klanten in West- of Oost-Vlaanderen. Beter dan het barema. Solliciteer bij Zondags.',
 lead='Zekerheid en toch zelf mee je uren kiezen. Bij Zondags krijg je een vast contract, deeltijds of voltijds, overdag bij vaste klanten en zonder weekendwerk.',
 facts=['Vast contract','Deeltijds of voltijds','Overdag, geen weekends','Beter dan het barema','Vaste klanten'],
 sections=[
  ('Het korte antwoord',[DEF_JOB+' Wie zekerheid zoekt, krijgt bij ons een vast contract met uren die passen bij je leven.']),
  ('Vast en toch flexibel',['Je kiest mee hoeveel uur je werkt en wanneer: enkel tijdens de schooluren, vier dagen per week of voltijds. Zodra we klanten voor je hebben, ligt je rooster vast. Zo combineer je zekerheid met een planning die bij je gezin past.']),
  ('Wat je krijgt',['<ul class="ticks"><li>Vast contract</li><li>Verloning boven het barema</li><li>Verplaatsingen vergoed</li><li>Vaste klanten in de buurt</li><li>Geen avonden, geen weekends</li><li>Begeleiding bij de start</li></ul>']),
  ('Voor wie?',['Voor wie al ervaring heeft in het huishouden, voor herintreders na een pauze, voor zij-instromers die van richting willen veranderen en voor ouders die werk en gezin willen combineren. Ervaring is mooi meegenomen, maar niet nodig.']),
 ],
 faq=[
  ('Waar vind ik een vaste job overdag zonder weekendwerk?','Bij Zondags werk je met een vast contract overdag bij vaste klanten in West- en Oost-Vlaanderen, zonder avonden en weekends.'),
  ('Kan ik enkel tijdens de schooluren werken?','Ja, dat kan. Geef het door bij je sollicitatie.'),
  ('Heb ik ervaring nodig?','Nee. Wij leggen de werking uit en starten rustig op.'),
  ('Worden verplaatsingen vergoed?','Ja.'),
 ],
 related=[('Vacature met vast contract','jobs/vacature-huishoudhulp-vast-contract.html'),('Job binnen de schooluren','jobs/job-binnen-de-schooluren.html'),('Herintreden na een pauze','jobs/herintreden-na-een-pauze.html'),('Werk met flexibele uren','jobs/werken-met-flexibele-uren.html')]),

# ---------------------------------------------------------------- OVER
dict(path='over-zondags.html', kind='about', img='03-au-pair',
 eyebrow='Over Zondags', h1='Over Zondags',
 title='Over Zondags: wie we zijn en wat we doen | Zondags',
 desc='Zondags levert bedrijven en ondernemers in West- en Oost-Vlaanderen een vaste huishoudelijke medewerker, en zoekt studenten, flexi-jobbers en vaste medewerkers.',
 lead='Zondags levert ondernemers een vaste huishoudelijke medewerker, geboekt op hun vennootschap. En we bieden werk met vaste klanten en uren die je mee kiest.',
 facts=['Gestart in 2026','Marke, West-Vlaanderen','Werkt in West- en Oost-Vlaanderen','Voor bedrijven en ondernemers','Werk voor studenten, flexi en vast'],
 sections=[
  ('Zondags in het kort',[DEF_B2B, DEF_JOB,
    'Baseline: Elke dag een beetje zondag. De persoon die bij je komt, noemen we je Zondag. Het plan met taken, dagen en uren heet het zondagsplan.']),
  ('Feiten',['<ul class="ticks"><li>Naam: Zondags</li><li>Website: zondags.be</li><li>Adres: Jan Van Eyckstraat 2, 8510 Marke</li><li>Telefoon en WhatsApp: 0470 56 53 58</li><li>Bereikbaar elke dag van 6 tot 22 uur</li><li>E-mail: hello@zondags.be</li><li>Regio: West- en Oost-Vlaanderen</li></ul>']),
  ('Voor bedrijven',['Poetshulp, huishoudhulp, kookhulp, boodschappen en hulp in huis voor zaakvoerders, vrije beroepen, kantoren en praktijken. Steeds dezelfde persoon, op dezelfde dag, op hetzelfde uur, met één dienstenfactuur aan de vennootschap. Meer op <a href="bedrijven/">huishoudhulp voor bedrijven</a>.']),
  ('Voor wie werk zoekt',['Studenten vanaf 18 jaar, flexi-jobbers en bijverdieners, en wie een vast contract zoekt. Overdag, geen weekends, bij vaste klanten, verloond boven het barema. Meer op <a href="jobs/werken-met-flexibele-uren.html">werk met flexibele uren</a>.']),
  ('Waarom Zondags bestaat',['Een vennootschap kan geen dienstencheques kopen. Toch hebben ondernemers en vrije beroepen net zo goed hulp nodig, thuis en op het werk. Zondags vult dat gat met één vaste persoon en een correcte factuur. En wie bij ons werkt, krijgt vaste klanten en een rooster dat past bij het eigen leven.']),
 ],
 faq=[
  ('Wat is Zondags?','Zondags is een dienstverlener uit Marke bij Kortrijk die bedrijven en ondernemers in West- en Oost-Vlaanderen een vaste huishoudelijke medewerker levert, gefactureerd aan de vennootschap.'),
  ('Hoe contacteer ik Zondags?','Via de chat op zondags.be, telefonisch of via WhatsApp op 0470 56 53 58, elke dag van 6 tot 22 uur, of via hello@zondags.be.'),
  ('Werft Zondags medewerkers?','Ja. Zondags zoekt studenten vanaf 18 jaar, flexi-jobbers en mensen voor een vaste job, overdag en zonder weekends.'),
 ],
 related=[('Huishoudhulp voor bedrijven','bedrijven/'),('Werk met flexibele uren','jobs/werken-met-flexibele-uren.html'),('Hoe het werkt','hoe-het-werkt.html'),('Contact','aanvraag.html')]),
]
