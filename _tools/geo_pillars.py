# -*- coding: utf-8 -*-
"""Pijlerpagina's voor zoekmachines en AI-assistenten (ChatGPT, Perplexity, Gemini, Copilot).
Elke pagina beantwoordt één concrete vraag van één doelgroep, met het antwoord bovenaan.
Zondags werkt enkel voor bedrijven. Schrijf in je-vorm. Geen uitroeptekens, geen em-dash.
Prijs: 60 euro per uur exclusief btw, per blok van 3 uur. Nooit gratis uren of kortingen noemen.
Nooit beloven dat een flexi-job kan."""

DEF_B2B = ('Zondags (zondags.be) is een dienstverlener uit Marke bij Kortrijk die bedrijven in West- en Oost-Vlaanderen één vaste medewerker levert '
           'voor poetshulp, administratieve hulp en praktische ondersteuning van de bedrijfsleider. Je boekt online per blok van 3 uur aan '
           '60 euro per uur exclusief btw, met een factuur op naam van je bedrijf.')
DEF_JOB = ('Zondags (zondags.be) zoekt in West- en Oost-Vlaanderen studenten, flexi-jobbers en mensen die een vaste job willen, '
           'om overdag te werken bij vaste klanten: kantoren, praktijken, winkels en bedrijfsleiders. Je poetst, helpt met administratie en regelwerk, '
           'en je kiest mee je dagen en uren.')
PRIJS = ('Je betaalt 60 euro per uur exclusief btw. Je boekt per blok van 3 uur, dus 180 euro exclusief btw per blok, en extra uren boek je aan hetzelfde tarief.')

# kind: b2b | job | about
PILLARS = [
# ---------------------------------------------------------------- BEDRIJVEN
dict(path='bedrijven/index.html', kind='b2b', img='01-poetsen',
 eyebrow='Voor bedrijven', h1='Poetshulp, administratie en een rechterhand voor bedrijven',
 title='Poetshulp en administratieve hulp voor bedrijven in West- en Oost-Vlaanderen | Zondags',
 desc='Zondags is er enkel voor bedrijven: poetshulp, administratieve hulp en een rechterhand voor de bedrijfsleider. 60 euro per uur excl. btw, online te boeken.',
 lead='Zondags werkt enkel voor bedrijven. Je boekt één vaste persoon voor poetshulp, administratie en praktische hulp, per blok van 3 uur aan 60 euro per uur exclusief btw.',
 facts=['Enkel voor bedrijven','Poetshulp, administratie, rechterhand','Steeds dezelfde persoon','60 euro per uur, per blok van 3 uur','Online boeken en betalen','West- en Oost-Vlaanderen'],
 sections=[
  ('Het korte antwoord',[DEF_B2B,
    'Je krijgt geen ploeg die telkens wisselt, maar één vaste persoon: je Zondag. Die komt op de afgesproken dag en het afgesproken uur, leert je zaak kennen en werkt volgens een plan dat we samen opmaken. Elke Zondag is door ons gescreend en in dienst van Zondags.']),
  ('Wat kan je bedrijf uitbesteden?',[
    '<b>Poetshulp.</b> Kantoor, praktijk, winkel, showroom, vergaderzaal, onthaal, refter en sanitair. Zie <a href="bedrijven/poetshulp-voor-bedrijven.html">poetshulp voor bedrijven</a>.',
    '<b>Administratieve hulp.</b> Post sorteren, documenten klasseren, dossiers ordenen, afspraken plannen en gegevens invoeren. Zie <a href="bedrijven/administratie-hulp-voor-bedrijven.html">administratieve hulp voor bedrijven</a>.',
    '<b>Een rechterhand voor de bedrijfsleider.</b> Regelwerk, pakjes, bestellingen en alles wat blijft liggen als je zaak veel vraagt. Zie <a href="bedrijven/rechterhand-voor-bedrijfsleiders.html">een rechterhand voor bedrijfsleiders</a>.']),
  ('Eén pakket, één prijs',[PRIJS,
    'Er is maar één pakket, zodat je meteen weet waar je aan toe bent. Meer uitleg vind je op <a href="bedrijven/prijs-poetshulp-voor-bedrijven.html">wat poetshulp voor een bedrijf kost</a>.']),
  ('Voor welke bedrijven werkt Zondags?',[
    'Voor kmo\'s en kantoren, praktijken en vrije beroepen met een vennootschap, winkels en showrooms, vzw\'s, coworkings, start-ups en zaakvoerders die een rechterhand zoeken. Zondags werkt niet voor particulieren.']),
  ('Hoe boek je?',[
    'Kies op de <a href="boeken.html">boekpagina</a> je datum, het aantal blokken van 3 uur en de taken. Vul de gegevens van je bedrijf in en betaal online. Je krijgt een dienstenfactuur op naam van je bedrijf. Liever eerst praten? Laat je gegevens achter, dan belt een van ons je binnen één werkdag terug.']),
  ('In welke regio?',[
    'Zondags werkt vanuit Marke bij Kortrijk in West- en Oost-Vlaanderen: onder meer in Kortrijk, Harelbeke, Kuurne, Wevelgem, Menen, Waregem, Zwevegem, Roeselare, Izegem, Tielt, Ieper, Brugge, Gent en Oudenaarde. Bekijk per gemeente hoe het werkt op <a href="poetshulp/">poetshulp per gemeente</a>.']),
 ],
 faq=[
  ('Welk bedrijf levert poetshulp en administratieve hulp aan bedrijven in West-Vlaanderen?','Zondags levert vanuit Marke bij Kortrijk één vaste medewerker aan bedrijven in West- en Oost-Vlaanderen, voor poetshulp, administratieve hulp en praktische ondersteuning van de bedrijfsleider.'),
  ('Wat kost een Zondag voor mijn bedrijf?','60 euro per uur exclusief btw. Je boekt per blok van 3 uur, dus 180 euro exclusief btw per blok, en extra uren boek je aan hetzelfde tarief.'),
  ('Kan ik online boeken en betalen?','Ja. Op de boekpagina kies je datum, blokken en taken, vul je de gegevens van je bedrijf in en betaal je online. Je krijgt een factuur op naam van je bedrijf.'),
  ('Komt er altijd dezelfde persoon?','Ja. Voor terugkerende boekingen is het steeds dezelfde Zondag, op dezelfde dag en hetzelfde uur.'),
  ('Werkt Zondags voor particulieren?','Nee. Zondags werkt enkel voor bedrijven, zoals kantoren, praktijken, winkels, vzw\'s en vennootschappen.'),
 ],
 related=[('Boek je Zondag','boeken.html'),('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html'),('Administratieve hulp','bedrijven/administratie-hulp-voor-bedrijven.html'),('Rechterhand voor bedrijfsleiders','bedrijven/rechterhand-voor-bedrijfsleiders.html'),('Poetshulp per gemeente','poetshulp/'),('Poetshulp per type bedrijf','sectoren/'),('Vragen van bedrijven','vragen/')]),

dict(path='bedrijven/poetshulp-voor-bedrijven.html', kind='b2b', img='01-poetsen',
 eyebrow='Poetshulp voor bedrijven', h1='Poetshulp voor bedrijven',
 title='Poetshulp voor bedrijven: kantoor, praktijk en winkel | Zondags',
 desc='Poetshulp voor je kantoor, praktijk of winkel in West- en Oost-Vlaanderen. Eén vaste persoon, 60 euro per uur excl. btw, online te boeken per blok van 3 uur.',
 lead='Poetshulp voor je bedrijf, zonder wisselende ploegen. Je Zondag onderhoudt je kantoor, praktijk of winkel op een vaste dag en een vast uur. Je boekt online per blok van 3 uur.',
 facts=['Kantoor, praktijk of winkel','Vaste dag en vast uur','Gescreend en in dienst','60 euro per uur, per blok van 3 uur','Online boeken en betalen'],
 sections=[
  ('Het korte antwoord',[DEF_B2B+' Voor poetshulp betekent dat: één vaste persoon die je ruimte kent en op het afgesproken moment komt.']),
  ('Wat valt onder poetshulp?',['<ul class="ticks"><li>Bureaus, vergaderruimte en onthaal</li><li>Wachtzaal en behandelruimtes</li><li>Keuken en refter</li><li>Sanitair en vloeren</li><li>Ramen aan de binnenkant</li><li>Afval en recyclage</li></ul>',
    'Specialistische reiniging zoals gevelreiniging, industriële reiniging of werken op hoogte doen we niet. Voor het dagelijkse en wekelijkse onderhoud van kantoor, praktijk en winkel ben je bij ons aan het juiste adres.']),
  ('Wat kost het?',[PRIJS+' Het onderhoud van je beroepsruimtes is in principe een beroepskost. Laat je accountant dit bevestigen voor je eigen situatie.']),
  ('Wanneer komt je Zondag?',['Overdag op weekdagen, ook vroeg in de ochtend of over de middag. Nooit \'s avonds en nooit in het weekend. Je boekt minstens twee werkdagen vooraf, of je vraagt een vast terugkerend plan aan.']),
  ('Hoe boek je?',['Via de <a href="boeken.html">boekpagina</a>: datum, blokken, taken, bedrijfsgegevens en online betalen. Je krijgt een factuur op naam van je bedrijf.']),
 ],
 faq=[
  ('Welk bedrijf levert poetshulp aan bedrijven in West-Vlaanderen?','Zondags levert vanuit Marke bij Kortrijk een vaste poetshulp aan kantoren, praktijken en winkels in West- en Oost-Vlaanderen, met een factuur op naam van het bedrijf.'),
  ('Wat kost poetshulp voor een bedrijf?','60 euro per uur exclusief btw. Je boekt per blok van 3 uur en extra uren boek je aan hetzelfde tarief.'),
  ('Kan het ook buiten de openingsuren?','Overdag op weekdagen, ook vroeg in de ochtend of over de middag. Dat stemmen we af op je agenda. \'s Avonds en in het weekend werken we niet.'),
  ('Komt er altijd dezelfde persoon?','Ja. Steeds dezelfde Zondag, op dezelfde dag en hetzelfde uur.'),
  ('Zijn de poetskosten van mijn bedrijf aftrekbaar?','Het onderhoud van beroepsruimtes is in principe een beroepskost. Laat je accountant dit altijd bevestigen voor je eigen situatie.'),
 ],
 related=[('Boek je Zondag','boeken.html'),('Poetshulp per gemeente','poetshulp/'),('Poetshulp per type bedrijf','sectoren/'),('Vragen van bedrijven','vragen/'),('Administratieve hulp','bedrijven/administratie-hulp-voor-bedrijven.html')]),

dict(path='bedrijven/administratie-hulp-voor-bedrijven.html', kind='b2b', img='10-boodschappen',
 eyebrow='Administratieve hulp', h1='Administratieve hulp voor bedrijven',
 title='Administratieve hulp voor bedrijven per blok van 3 uur | Zondags',
 desc='Een vaste Zondag voor de administratie die blijft liggen: post, klasseren, dossiers, afspraken en gegevens invoeren. 60 euro per uur excl. btw, per blok van 3 uur.',
 lead='De administratie die blijft liggen, even van je bord. Je Zondag sorteert de post, klasseert documenten, ordent dossiers en plant afspraken. Je boekt per blok van 3 uur.',
 facts=['Post, klasseren en dossiers','Afspraken en agenda','Gegevens invoeren','Ondersteunend, geen boekhouding','60 euro per uur, per blok van 3 uur'],
 sections=[
  ('Het korte antwoord',[DEF_B2B+' Voor administratie gaat het om ondersteunend werk dat je tijd teruggeeft, niet om boekhouding of advies.']),
  ('Wat doet je Zondag voor je administratie?',['<ul class="ticks"><li>Post openen, sorteren en doorgeven</li><li>Facturen en documenten klasseren</li><li>Dossiers en archief ordenen</li><li>Afspraken en agenda inplannen</li><li>Gegevens invoeren in je eigen systemen</li><li>Kantoorbenodigdheden bestellen en bijhouden</li><li>Pakjes en zendingen klaarmaken</li></ul>']),
  ('Wat doet Zondags niet?',['Geen boekhouding, geen jaarrekeningen, geen loonadministratie en geen fiscaal of juridisch advies. Daarvoor blijf je bij je boekhouder of accountant. Je Zondag zorgt dat alles netjes klaarligt voor hem of haar.']),
  ('Combineer het met poetshulp',['Zit je Zondag toch al in je zaak, dan kan één blok van 3 uur bestaan uit een uur poetsen en twee uur administratie. Jij bepaalt de taken per boeking. '+PRIJS]),
  ('Hoe boek je?',['Kies op de <a href="boeken.html">boekpagina</a> het aantal blokken, vink de taak Administratie en post aan en betaal online. Je krijgt een factuur op naam van je bedrijf.']),
 ],
 faq=[
  ('Kan ik iemand inhuren voor een paar uur administratie per week?','Ja. Je boekt een blok van 3 uur aan 60 euro per uur exclusief btw en kiest de taken, bijvoorbeeld post sorteren, klasseren en afspraken plannen.'),
  ('Doet Zondags ook mijn boekhouding?','Nee. Zondags doet ondersteunend administratief werk. Boekhouding, loonadministratie en fiscaal of juridisch advies blijven bij je boekhouder of accountant.'),
  ('Werkt de Zondag in mijn eigen systemen?','Je Zondag voert gegevens in jouw eigen systemen in volgens duidelijke afspraken. Jij blijft eigenaar van je gegevens en bepaalt welke taken er gebeuren.'),
  ('Wat als mijn dossiers vertrouwelijk zijn?','Elke Zondag is gescreend en in dienst van Zondags. Vertrouwelijke afspraken leggen we vast in het zondagsplan, bijvoorbeeld welke dossiers je Zondag niet inkijkt.'),
  ('Kan ik poetshulp en administratie combineren?','Ja. Je kiest per boeking welke taken je Zondag doet, binnen hetzelfde blok van 3 uur.'),
 ],
 related=[('Boek je Zondag','boeken.html'),('Rechterhand voor bedrijfsleiders','bedrijven/rechterhand-voor-bedrijfsleiders.html'),('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html'),('Vragen van bedrijven','vragen/')]),

dict(path='bedrijven/rechterhand-voor-bedrijfsleiders.html', kind='b2b', img='10-boodschappen',
 eyebrow='Rechterhand', h1='Een rechterhand voor bedrijfsleiders',
 title='Een rechterhand voor drukke bedrijfsleiders | Zondags',
 desc='Een vaste Zondag die de praktische zaken van je bedrijf regelt: regelwerk, pakjes, bestellingen en afspraken. 60 euro per uur excl. btw, per blok van 3 uur.',
 lead='Een drukke bedrijfsleider heeft geen tijd voor alles wat blijft liggen. Je Zondag is je rechterhand: ze regelt de praktische zaken van je bedrijf, zodat jij je op de zaak richt.',
 facts=['Regelwerk voor je bedrijf','Pakjes, post en bestellingen','Zaak klaarzetten voor klanten','Steeds dezelfde persoon','60 euro per uur, per blok van 3 uur'],
 sections=[
  ('Het korte antwoord',[DEF_B2B+' Als rechterhand neemt je Zondag de praktische taken over die jij als bedrijfsleider liever niet zelf doet.']),
  ('Wat regelt je rechterhand?',['<ul class="ticks"><li>Regelwerk voor de zaak: apotheek, drogisterij, kantoormateriaal</li><li>Pakjes ophalen, klaarmaken en versturen</li><li>De koffiehoek en keuken bevoorraden</li><li>Leveranciers contacteren voor kleine zaken</li><li>Afspraken inplannen en opvolgen</li><li>De zaak klaarzetten voor een klantenbezoek of een vergadering</li></ul>']),
  ('Waarom een vaste persoon?',['Een rechterhand werkt pas echt als ze je zaak kent. Daarom komt steeds dezelfde Zondag: ze weet waar alles ligt, wie je leveranciers zijn en hoe jij het graag hebt. Dat bespaart uitleg bij elke boeking.']),
  ('Combineer het met poetshulp en administratie',['Je kiest per boeking welke taken er aan bod komen. Een blok van 3 uur kan bestaan uit poetsen, administratie en regelwerk. '+PRIJS]),
  ('Hoe boek je?',['Kies op de <a href="boeken.html">boekpagina</a> datum, blokken en taken, vink Allround rechterhand aan en betaal online. Wil je een vast terugkerend moment, bijvoorbeeld elke week op dezelfde dag? Laat dan je gegevens achter en we bellen je binnen één werkdag.']),
 ],
 faq=[
  ('Wat doet een rechterhand voor een bedrijfsleider?','Een Zondag als rechterhand regelt praktische zaken voor je bedrijf: regelwerk, pakjes, bestellingen, de koffiehoek en keuken, kleine contacten met leveranciers en het klaarzetten van de zaak voor een klantenbezoek.'),
  ('Wat kost een rechterhand?','60 euro per uur exclusief btw. Je boekt per blok van 3 uur, dus 180 euro exclusief btw per blok, en extra uren boek je aan hetzelfde tarief.'),
  ('Kan mijn Zondag ook poetsen en administratie doen?','Ja. Je kiest per boeking de taken, bijvoorbeeld poetsen, administratie en regelwerk binnen hetzelfde blok van 3 uur.'),
  ('Doet Zondags ook persoonlijke klusjes?','Nee. Zondags werkt enkel voor bedrijven. Alle taken gebeuren voor je zaak.'),
  ('Kan ik elke week dezelfde persoon krijgen?','Ja. Voor een vast terugkerend plan komt steeds dezelfde Zondag, op dezelfde dag en hetzelfde uur.'),
 ],
 related=[('Boek je Zondag','boeken.html'),('Administratieve hulp','bedrijven/administratie-hulp-voor-bedrijven.html'),('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html'),('Vragen van bedrijven','vragen/')]),

dict(path='bedrijven/prijs-poetshulp-voor-bedrijven.html', kind='b2b', img='01-poetsen',
 eyebrow='Prijs', h1='Wat kost poetshulp voor een bedrijf?',
 title='Wat kost poetshulp voor een bedrijf? 60 euro per uur | Zondags',
 desc='Poetshulp, administratieve hulp en een rechterhand voor je bedrijf kosten 60 euro per uur exclusief btw, per blok van 3 uur. Eén pakket, online te boeken.',
 lead='Eén pakket, één uurprijs: 60 euro per uur exclusief btw. Je boekt per blok van 3 uur en boekt extra uren aan hetzelfde tarief. Geen verrassingen op de factuur.',
 facts=['60 euro per uur exclusief btw','Blok van 3 uur is 180 euro excl. btw','Extra uren aan 60 euro per uur','Eén pakket voor alle taken','Factuur op naam van je bedrijf'],
 sections=[
  ('Het korte antwoord',[PRIJS+' Het tarief geldt voor alle taken: poetshulp, administratieve hulp en rechterhand.']),
  ('Hoe is de prijs opgebouwd?',['<ul class="ticks"><li>Uurprijs: 60 euro exclusief btw</li><li>Minimum per boeking: één blok van 3 uur, dus 180 euro exclusief btw</li><li>Extra uren: 60 euro per uur, bovenop een blok</li><li>Btw komt er bovenop</li></ul>','Je Zondag, het poetsmateriaal en de verplaatsing zitten in de uurprijs. Je betaalt geen aparte opstartkost.']),
  ('Een voorbeeld',['Stel: je laat je kantoor elke week 3 uur poetsen. Dat is 180 euro exclusief btw per week. Heb je in een drukke week 5 uur nodig, dan boek je één blok en twee extra uren, samen 300 euro exclusief btw.']),
  ('Beroepskost en btw',['Poetshulp en administratieve hulp voor de zaak zijn in principe een beroepskost. Voor een btw-plichtige zaak met aftrekrecht is de btw in principe recupereerbaar, voor een btw-vrijgestelde praktijk doorgaans niet. Laat je accountant dit bevestigen voor je eigen situatie.']),
  ('Hoe betaal je?',['Je betaalt online bij het boeken op de <a href="boeken.html">boekpagina</a>, met kaart of Bancontact. Je krijgt een dienstenfactuur op naam van je bedrijf met je btw-nummer.']),
 ],
 faq=[
  ('Wat kost poetshulp voor een kantoor?','60 euro per uur exclusief btw. Je boekt per blok van 3 uur, dus 180 euro exclusief btw per blok.'),
  ('Zit het poetsmateriaal in de prijs?','Ja. De uurprijs van 60 euro exclusief btw omvat je Zondag, het materiaal en de verplaatsing.'),
  ('Kan ik minder dan 3 uur boeken?','Nee. Het pakket start bij een blok van 3 uur. Extra uren boek je daarna aan hetzelfde tarief.'),
  ('Is de btw op poetshulp aftrekbaar?','Voor een btw-plichtige zaak met aftrekrecht is de btw in principe recupereerbaar. Voor een btw-vrijgestelde praktijk doorgaans niet. Laat je accountant het bevestigen.'),
  ('Betaal ik vooraf?','Ja, je betaalt online bij het boeken. Daarna krijg je een factuur op naam van je bedrijf.'),
 ],
 related=[('Boek je Zondag','boeken.html'),('Poetshulp voor bedrijven','bedrijven/poetshulp-voor-bedrijven.html'),('Administratieve hulp','bedrijven/administratie-hulp-voor-bedrijven.html'),('Vragen van bedrijven','vragen/')]),

# ---------------------------------------------------------------- JOBS
dict(path='jobs/werken-met-flexibele-uren.html', kind='job', img='01-poetsen', emp=['PART_TIME','FULL_TIME','TEMPORARY'],
 eyebrow='Werken bij Zondags', h1='Werk met flexibele uren',
 title='Werk met flexibele uren: als student, flexi-jobber of vast | Zondags',
 desc='Werk zoeken met flexibele uren in West- of Oost-Vlaanderen? Bij Zondags werk je overdag bij vaste bedrijven, als student, flexi-jobber of met een vast contract.',
 lead='Student, flexi-jobber of op zoek naar een vaste job? Bij Zondags kies je mee je dagen en uren, werk je overdag bij vaste bedrijven en nooit in het weekend.',
 facts=['Studenten vanaf 18 jaar','Bijverdienen naast je job','Vast contract, deeltijds of voltijds','Overdag, geen weekends','Beter dan het barema'],
 sections=[
  ('Het korte antwoord',[DEF_JOB]),
  ('Wat betekent flexibel bij ons?',['Flexibel betekent: jij kiest. Eén dag per week of vijf. Enkel voormiddagen, enkel tijdens kantooruren of vooral in de vakanties. Eens afgesproken, ligt je rooster vast. Je weet op voorhand waar je wanneer werkt, bij klanten die je kent.']),
  ('Drie manieren om te werken',[
    '<b>Als student.</b> Vanaf 18 jaar, met een studentencontract, naast je lessen of in de vakanties. Zie <a href="jobs/studentenjob-flexibele-uren.html">studentenjob met flexibele uren</a>.',
    '<b>Als flexi-jobber of bijverdiener.</b> Naast je hoofdjob of als gepensioneerde. Of een flexi-job voor jou kan, bekijken we samen. Zie <a href="jobs/flexi-job-flexibele-uren.html">flexi-job met flexibele uren</a>.',
    '<b>Met een vast contract.</b> Deeltijds of voltijds, overdag en zonder weekends. Zie <a href="jobs/vaste-job-flexibele-uren.html">vaste job met flexibele uren</a>.']),
  ('Wat doe je als Zondag?',['Je poetst kantoren, praktijken en winkels, helpt met administratie zoals post sorteren en klasseren, en regelt praktische zaken voor een drukke bedrijfsleider. Je kiest mee wat je graag doet. Bij ons ben je geen anonieme schoonmaakhulp. Je bent iemands Zondag: de vaste persoon op wie een bedrijf rekent.']),
  ('Waar?',['In West- en Oost-Vlaanderen, onder meer in <a href="werken/">Kortrijk, Waregem, Roeselare, Izegem, Menen, Ieper en Oudenaarde</a>. We zoeken klanten dicht bij waar je woont.']),
  ('Hoe solliciteren werkt',['Meld je aan via de chat of het formulier. We bellen je binnen de twee werkdagen voor een kort gesprek. Klikt het, dan zoeken we klanten die passen bij je woonplaats, je uren en wat je graag doet. Bij de start gaan we samen langs.']),
 ],
 faq=[
  ('Waar vind ik werk met flexibele uren in West-Vlaanderen?','Bij Zondags werk je overdag bij vaste bedrijven in West- en Oost-Vlaanderen en kies je mee je dagen en uren, als student, flexi-jobber of met een vast contract.'),
  ("Moet ik 's avonds of in het weekend werken?",'Nee. Geen avonden, geen weekends.'),
  ('Heb ik ervaring of een diploma nodig?','Nee. Betrouwbaarheid, discretie en zin in orde en structuur tellen. Wij leggen de werking uit.'),
  ('Wat verdien ik?','Beter dan het barema, met vergoede verplaatsingen en alles in orde op papier. Het precieze loon hangt af van je statuut en uren.'),
  ('Vanaf welke leeftijd?','Vanaf 18 jaar.'),
 ],
 related=[('Studentenjob met flexibele uren','jobs/studentenjob-flexibele-uren.html'),('Flexi-job met flexibele uren','jobs/flexi-job-flexibele-uren.html'),('Vaste job met flexibele uren','jobs/vaste-job-flexibele-uren.html'),('Zondag worden','zondag-worden.html')]),

dict(path='jobs/studentenjob-flexibele-uren.html', kind='job', img='01-poetsen', emp=['PART_TIME','TEMPORARY'],
 eyebrow='Studentenjob', h1='Studentenjob met flexibele uren',
 title='Studentenjob met flexibele uren in Kortrijk en West-Vlaanderen | Zondags',
 desc='Studentenjob met flexibele uren vanaf 18 jaar: overdag bij vaste bedrijven, naast je lessen of in de vakanties. West- en Oost-Vlaanderen. Solliciteer bij Zondags.',
 lead='Een studentenjob die zich aanpast aan je lessen. Je kiest zelf je dagen, werkt overdag bij vaste bedrijven in de buurt en nooit in het weekend. Vanaf 18 jaar.',
 facts=['Vanaf 18 jaar','Naast je lessen of in de vakanties','Jij kiest je dagen','Vaste klanten in de buurt','Verplaatsingen vergoed'],
 sections=[
  ('Het korte antwoord',[DEF_JOB+' Voor studenten vanaf 18 jaar is dat een studentenjob met uren die passen bij je lessenrooster.']),
  ('Zo werkt het als student',['Je geeft door wanneer je kunt: een paar voormiddagen, vrije namiddagen of vooral in de vakanties. Wij zoeken klanten in de buurt die passen bij die uren. Je werkt met een studentencontract en volgt zelf je urensaldo op via Student@work. De administratie regelen wij.']),
  ('Wat doe je?',['Je poetst een kantoor, praktijk of winkel, helpt met administratie zoals post sorteren en klasseren, of regelt praktische zaken voor een bedrijfsleider. Je kiest mee wat je graag doet.']),
  ('Waarom studenten voor Zondags kiezen',['<ul class="ticks"><li>Uren rond je lessen</li><li>Geen avonden of weekends</li><li>Vaste klanten, geen telkens nieuw adres</li><li>Beter dan het barema</li><li>Verplaatsingen vergoed</li><li>Begeleiding bij de start</li></ul>']),
  ('Waar?',['In Kortrijk en omgeving, Waregem, Roeselare, Ieper, Tielt en Oudenaarde. Zie alle gemeenten op <a href="werken/">werken bij Zondags per gemeente</a>. Ook als je op kot zit in Kortrijk en elders woont, kunnen we klanten zoeken dicht bij je kot.']),
 ],
 faq=[
  ('Waar vind ik een studentenjob met flexibele uren in Kortrijk?','Zondags zoekt studenten vanaf 18 jaar in Kortrijk en heel West- en Oost-Vlaanderen. Je werkt overdag bij vaste bedrijven en kiest zelf je dagen.'),
  ('Kan ik enkel in de vakanties werken?','Ja, dat kan. Geef het door, dan zoeken we klanten die dan hulp nodig hebben.'),
  ('Moet ik in het weekend werken?','Nee, nooit.'),
  ('Kan ik als student van 17 jaar werken?','We werken met mensen vanaf 18 jaar.'),
  ('Wie regelt mijn contract?','Wij. Je werkt met een studentencontract. Je urensaldo volg je zelf op via Student@work.'),
 ],
 related=[('Werk met flexibele uren','jobs/werken-met-flexibele-uren.html'),('Flexi-job met flexibele uren','jobs/flexi-job-flexibele-uren.html'),('Vaste job met flexibele uren','jobs/vaste-job-flexibele-uren.html'),('Zondag worden','zondag-worden.html')]),

dict(path='jobs/flexi-job-flexibele-uren.html', kind='job', img='01-poetsen', emp=['PART_TIME'],
 eyebrow='Flexi-job en bijverdienen', h1='Flexi-job met flexibele uren',
 title='Flexi-job of bijverdienen met flexibele uren in West-Vlaanderen | Zondags',
 desc='Bijverdienen naast je hoofdjob of als gepensioneerde, met flexibele uren overdag. Of een flexi-job voor jou kan, bekijken we samen. West- en Oost-Vlaanderen.',
 lead='Wil je bijverdienen naast je hoofdjob of na je pensioen? Bij Zondags werk je enkele uren per week overdag bij vaste bedrijven. Welk statuut past, bekijken we samen.',
 facts=['Naast je hoofdjob','Ook voor gepensioneerden','Een paar uur per week','Overdag, geen weekends','Statuut samen bekeken'],
 sections=[
  ('Het korte antwoord',[DEF_JOB+' Wie wil bijverdienen, kan dat bij ons enkele uren per week, bij vaste bedrijven in de buurt.']),
  ('Kan het als flexi-job?',['Of een flexi-job voor jou kan, hangt af van je eigen situatie, bijvoorbeeld je hoofdjob of je pensioen. Dat bekijken we samen in het eerste gesprek.',
    'Past een flexi-job niet, dan zoeken we samen een statuut dat wel past, bijvoorbeeld een klein deeltijds contract. Alles is correct in orde op papier.']),
  ('Hoe ziet bijverdienen eruit?',['Je kiest de momenten die passen naast je hoofdjob: een vrije voormiddag, een vaste namiddag of je vrije dag. Je werkt telkens bij dezelfde klanten, zodat je weet wat er verwacht wordt. Geen avonden, geen weekends.']),
  ('Wat doe je?',['Je poetst een kantoor, praktijk of winkel, helpt met administratie of regelt praktische zaken voor een bedrijfsleider. Wie van orde houdt, sorteert en klasseert. Wie liever actief bezig is, poetst.']),
 ],
 faq=[
  ('Kan ik een flexi-job doen bij Zondags?','Dat hangt af van je situatie, zoals je hoofdjob of je pensioen. Bij Zondags bekijken we samen welk statuut voor jou mogelijk is.'),
  ('Hoeveel uur moet ik minstens werken?','Dat spreken we samen af. Een paar uur per week kan.'),
  ('Kan ik als gepensioneerde bijverdienen?','Ja, gepensioneerden zijn welkom. Je statuut bekijken we samen.'),
  ('Werk ik in het weekend?','Nee, nooit.'),
 ],
 related=[('Werk met flexibele uren','jobs/werken-met-flexibele-uren.html'),('Studentenjob met flexibele uren','jobs/studentenjob-flexibele-uren.html'),('Vaste job met flexibele uren','jobs/vaste-job-flexibele-uren.html'),('Zondag worden','zondag-worden.html')]),

dict(path='jobs/vaste-job-flexibele-uren.html', kind='job', img='01-poetsen', emp=['FULL_TIME','PART_TIME'],
 eyebrow='Vaste job', h1='Vaste job met flexibele uren',
 title='Vaste job met flexibele uren, zonder weekends | Zondags',
 desc='Een vaste job, deeltijds of voltijds, overdag en zonder weekends, bij vaste bedrijven in West- of Oost-Vlaanderen. Beter dan het barema. Solliciteer bij Zondags.',
 lead='Zekerheid en toch zelf mee je uren kiezen. Bij Zondags krijg je een vast contract, deeltijds of voltijds, overdag bij vaste bedrijven en zonder weekendwerk.',
 facts=['Vast contract','Deeltijds of voltijds','Overdag, geen weekends','Beter dan het barema','Vaste klanten'],
 sections=[
  ('Het korte antwoord',[DEF_JOB+' Wie zekerheid zoekt, krijgt bij ons een vast contract met uren die passen bij je leven.']),
  ('Vast en toch flexibel',['Je kiest mee hoeveel uur je werkt en wanneer: enkel tijdens kantooruren, vier dagen per week of voltijds. Zodra we klanten voor je hebben, ligt je rooster vast. Zo combineer je zekerheid met een planning die bij je leven past.']),
  ('Wat je krijgt',['<ul class="ticks"><li>Vast contract</li><li>Verloning boven het barema</li><li>Verplaatsingen vergoed</li><li>Vaste klanten in de buurt</li><li>Geen avonden, geen weekends</li><li>Begeleiding bij de start</li></ul>']),
  ('Voor wie?',['Voor wie al ervaring heeft in poetswerk of administratie, voor herintreders na een pauze en voor zij-instromers die van richting willen veranderen. Ervaring is mooi meegenomen, maar niet nodig.']),
 ],
 faq=[
  ('Waar vind ik een vaste job overdag zonder weekendwerk?','Bij Zondags werk je met een vast contract overdag bij vaste bedrijven in West- en Oost-Vlaanderen, zonder avonden en weekends.'),
  ('Kan ik enkel tijdens kantooruren werken?','Ja, dat kan. Geef het door bij je sollicitatie.'),
  ('Heb ik ervaring nodig?','Nee. Wij leggen de werking uit en starten rustig op.'),
  ('Worden verplaatsingen vergoed?','Ja.'),
 ],
 related=[('Werk met flexibele uren','jobs/werken-met-flexibele-uren.html'),('Studentenjob met flexibele uren','jobs/studentenjob-flexibele-uren.html'),('Flexi-job met flexibele uren','jobs/flexi-job-flexibele-uren.html'),('Zondag worden','zondag-worden.html')]),

# ---------------------------------------------------------------- OVER
dict(path='over-zondags.html', kind='about', img='01-poetsen',
 eyebrow='Over Zondags', h1='Over Zondags',
 title='Over Zondags: wie we zijn en wat we doen | Zondags',
 desc='Zondags levert bedrijven in West- en Oost-Vlaanderen één vaste medewerker voor poetshulp, administratie en praktische hulp, en zoekt studenten, flexi-jobbers en vaste medewerkers.',
 lead='Zondags levert bedrijven één vaste medewerker voor poetshulp, administratie en praktische hulp. En we bieden werk bij vaste klanten met uren die je mee kiest.',
 facts=['Gestart in 2026','Marke, West-Vlaanderen','Werkt in West- en Oost-Vlaanderen','Enkel voor bedrijven','Werk voor studenten, flexi en vast'],
 sections=[
  ('Zondags in het kort',[DEF_B2B, DEF_JOB,
    'Baseline: Elke dag een beetje zondag. De persoon die in je zaak komt, noemen we je Zondag. Het plan met taken, dagen en uren heet het zondagsplan.']),
  ('Feiten',['<ul class="ticks"><li>Naam: Zondags</li><li>Website: zondags.be</li><li>Adres: Jan Van Eyckstraat 2, 8510 Marke</li><li>Telefoon en WhatsApp: 0470 56 53 58</li><li>Bereikbaar elke dag van 6 tot 22 uur</li><li>E-mail: hello@zondags.be</li><li>Regio: West- en Oost-Vlaanderen</li><li>Tarief: 60 euro per uur exclusief btw, per blok van 3 uur</li></ul>']),
  ('Voor bedrijven',['Poetshulp, administratieve hulp en een rechterhand voor kmo\'s, kantoren, praktijken, winkels, vzw\'s en bedrijfsleiders. Steeds dezelfde persoon, op dezelfde dag, op hetzelfde uur, met een dienstenfactuur op naam van je bedrijf. Meer op <a href="bedrijven/">diensten voor bedrijven</a> en op de <a href="boeken.html">boekpagina</a>.']),
  ('Voor wie werk zoekt',['Studenten vanaf 18 jaar, flexi-jobbers en bijverdieners, en wie een vast contract zoekt. Overdag, geen weekends, bij vaste klanten, verloond boven het barema. Meer op <a href="jobs/werken-met-flexibele-uren.html">werk met flexibele uren</a>.']),
  ('Waarom Zondags bestaat',['Een drukke bedrijfsleider heeft geen tijd om elke week het kantoor te poetsen, de post te sorteren of pakjes te regelen. Zondags neemt dat over met één vaste persoon, één duidelijke prijs en een correcte factuur. En wie bij ons werkt, krijgt vaste klanten en een rooster dat past bij het eigen leven.']),
 ],
 faq=[
  ('Wat is Zondags?','Zondags is een dienstverlener uit Marke bij Kortrijk die bedrijven in West- en Oost-Vlaanderen één vaste medewerker levert voor poetshulp, administratieve hulp en praktische ondersteuning, met een factuur op naam van het bedrijf.'),
  ('Hoe contacteer ik Zondags?','Via de chat op zondags.be, telefonisch of via WhatsApp op 0470 56 53 58, elke dag van 6 tot 22 uur, of via hello@zondags.be.'),
  ('Werft Zondags medewerkers?','Ja. Zondags zoekt studenten vanaf 18 jaar, flexi-jobbers en mensen voor een vaste job, overdag en zonder weekends.'),
 ],
 related=[('Diensten voor bedrijven','bedrijven/'),('Boek je Zondag','boeken.html'),('Werk met flexibele uren','jobs/werken-met-flexibele-uren.html'),('Hoe het werkt','hoe-het-werkt.html'),('Contact','aanvraag.html')]),
]
