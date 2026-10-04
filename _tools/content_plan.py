# -*- coding: utf-8 -*-
"""Inhoudsplan voor de unieke B2B-pagina's (poetshulp/, regio/<dienst>-<plaats>, sectoren/, vragen/).
Elke pagina heeft een eigen JSON-bestand in _tools/content/<pad>.json met unieke tekst.
Gebruik: python3 _tools/content_plan.py  -> schrijft _tools/content/plan.json"""
import json, os, re

def slug(s):
    s = s.lower()
    for a, b in (('é', 'e'), ('ë', 'e'), ('è', 'e'), ('ï', 'i'), ("'", '')):
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

# (plaats, postcode, provincie, soort, deel van, deelgemeenten, in de buurt, streek)
WV, OV = 'West-Vlaanderen', 'Oost-Vlaanderen'
PLAATSEN = [
 ("Kortrijk","8500",WV,"stad","",["Aalbeke","Bellegem","Bissegem","Heule","Kooigem","Marke","Rollegem"],["Kuurne","Harelbeke","Wevelgem","Menen","Zwevegem","Lendelede"],"regio Kortrijk"),
 ("Marke","8510",WV,"deelgemeente","Kortrijk",[],["Kortrijk","Bissegem","Aalbeke","Rollegem","Lauwe","Bellegem"],"regio Kortrijk"),
 ("Heule","8501",WV,"deelgemeente","Kortrijk",[],["Kortrijk","Kuurne","Gullegem","Lendelede","Bissegem"],"regio Kortrijk"),
 ("Bissegem","8501",WV,"deelgemeente","Kortrijk",[],["Kortrijk","Marke","Wevelgem","Gullegem","Heule"],"regio Kortrijk"),
 ("Aalbeke","8511",WV,"deelgemeente","Kortrijk",[],["Rollegem","Marke","Rekkem","Lauwe","Kortrijk"],"regio Kortrijk"),
 ("Bellegem","8510",WV,"deelgemeente","Kortrijk",[],["Kortrijk","Rollegem","Kooigem","Zwevegem","Marke"],"regio Kortrijk"),
 ("Rollegem","8510",WV,"deelgemeente","Kortrijk",[],["Aalbeke","Bellegem","Kooigem","Marke","Kortrijk"],"regio Kortrijk"),
 ("Kooigem","8510",WV,"deelgemeente","Kortrijk",[],["Bellegem","Rollegem","Zwevegem","Spiere-Helkijn","Kortrijk"],"regio Kortrijk"),
 ("Wevelgem","8560",WV,"gemeente","",["Gullegem","Moorsele"],["Kortrijk","Menen","Ledegem","Lauwe","Bissegem"],"regio Kortrijk"),
 ("Gullegem","8560",WV,"deelgemeente","Wevelgem",[],["Heule","Moorsele","Wevelgem","Bissegem","Ledegem"],"regio Kortrijk"),
 ("Moorsele","8560",WV,"deelgemeente","Wevelgem",[],["Gullegem","Ledegem","Lendelede","Wevelgem","Dadizele"],"regio Kortrijk"),
 ("Menen","8930",WV,"stad","",["Lauwe","Rekkem"],["Wevelgem","Wervik","Lauwe","Rekkem","Geluwe"],"regio Kortrijk"),
 ("Lauwe","8930",WV,"deelgemeente","Menen",[],["Menen","Rekkem","Marke","Wevelgem","Aalbeke"],"regio Kortrijk"),
 ("Rekkem","8930",WV,"deelgemeente","Menen",[],["Lauwe","Menen","Aalbeke","Marke"],"regio Kortrijk"),
 ("Wervik","8940",WV,"stad","",["Geluwe"],["Menen","Geluwe","Zonnebeke","Ieper"],"regio Kortrijk"),
 ("Geluwe","8940",WV,"deelgemeente","Wervik",[],["Wervik","Menen","Dadizele","Beselare","Ledegem"],"regio Kortrijk"),
 ("Harelbeke","8530",WV,"stad","",["Bavikhove","Hulste"],["Kortrijk","Kuurne","Deerlijk","Zwevegem","Wielsbeke"],"regio Kortrijk"),
 ("Kuurne","8520",WV,"gemeente","",[],["Kortrijk","Harelbeke","Lendelede","Heule"],"regio Kortrijk"),
 ("Zwevegem","8550",WV,"gemeente","",["Heestert","Moen","Otegem","Sint-Denijs"],["Kortrijk","Harelbeke","Deerlijk","Avelgem","Spiere-Helkijn","Anzegem"],"regio Kortrijk"),
 ("Deerlijk","8540",WV,"gemeente","",[],["Harelbeke","Zwevegem","Waregem","Anzegem"],"regio Kortrijk"),
 ("Waregem","8790",WV,"stad","",["Beveren-Leie","Desselgem","Sint-Eloois-Vijve"],["Harelbeke","Deerlijk","Anzegem","Zulte","Wielsbeke","Kruisem"],"Leiestreek"),
 ("Anzegem","8570",WV,"gemeente","",["Gijzelbrechtegem","Ingooigem","Kaster","Tiegem","Vichte"],["Waregem","Deerlijk","Zwevegem","Avelgem"],"regio Kortrijk"),
 ("Avelgem","8580",WV,"gemeente","",["Bossuit","Kerkhove","Outrijve","Waarmaarde"],["Zwevegem","Anzegem","Spiere-Helkijn","Kluisbergen"],"regio Kortrijk"),
 ("Lendelede","8860",WV,"gemeente","",[],["Kuurne","Heule","Izegem","Ingelmunster","Moorsele"],"regio Kortrijk"),
 ("Ledegem","8880",WV,"gemeente","",["Rollegem-Kapelle","Sint-Eloois-Winkel"],["Moorslede","Wevelgem","Izegem","Menen"],"regio Roeselare"),
 ("Moorslede","8890",WV,"gemeente","",["Dadizele"],["Ledegem","Roeselare","Zonnebeke","Staden"],"regio Roeselare"),
 ("Izegem","8870",WV,"stad","",["Emelgem","Kachtem"],["Roeselare","Ingelmunster","Lendelede","Ledegem","Ardooie"],"regio Roeselare"),
 ("Ingelmunster","8770",WV,"gemeente","",[],["Izegem","Meulebeke","Oostrozebeke","Lendelede"],"regio Roeselare"),
 ("Roeselare","8800",WV,"stad","",["Beveren","Oekene","Rumbeke"],["Izegem","Hooglede","Moorslede","Ardooie","Lichtervelde","Staden"],"regio Roeselare"),
 ("Rumbeke","8800",WV,"deelgemeente","Roeselare",[],["Roeselare","Oekene","Ardooie","Izegem","Beveren"],"regio Roeselare"),
 ("Hooglede","8830",WV,"gemeente","",["Gits"],["Roeselare","Staden","Lichtervelde","Kortemark"],"regio Roeselare"),
 ("Staden","8840",WV,"gemeente","",["Oostnieuwkerke","Westrozebeke"],["Hooglede","Roeselare","Moorslede","Langemark-Poelkapelle","Zonnebeke"],"regio Roeselare"),
 ("Lichtervelde","8810",WV,"gemeente","",[],["Torhout","Ardooie","Hooglede","Roeselare"],"regio Roeselare"),
 ("Ardooie","8850",WV,"gemeente","",["Koolskamp"],["Roeselare","Izegem","Lichtervelde","Pittem","Meulebeke"],"regio Roeselare"),
 ("Meulebeke","8760",WV,"gemeente","",[],["Tielt","Ingelmunster","Oostrozebeke","Pittem","Dentergem"],"regio Tielt"),
 ("Tielt","8700",WV,"stad","",["Aarsele","Kanegem","Schuiferskapelle"],["Pittem","Meulebeke","Dentergem","Wingene","Ruiselede"],"regio Tielt"),
 ("Oostrozebeke","8780",WV,"gemeente","",[],["Wielsbeke","Ingelmunster","Meulebeke"],"Leiestreek"),
 ("Wielsbeke","8710",WV,"gemeente","",["Ooigem","Sint-Baafs-Vijve"],["Oostrozebeke","Waregem","Dentergem","Meulebeke"],"Leiestreek"),
 ("Dentergem","8720",WV,"gemeente","",["Markegem","Oeselgem","Wakken"],["Wielsbeke","Tielt","Zulte","Deinze","Meulebeke"],"Leiestreek"),
 ("Zulte","9870",OV,"gemeente","",["Machelen","Olsene"],["Waregem","Deinze","Kruisem","Dentergem","Wielsbeke"],"Leiestreek"),
 ("Pittem","8740",WV,"gemeente","",["Egem"],["Tielt","Ardooie","Wingene","Meulebeke"],"regio Tielt"),
 ("Ieper","8900",WV,"stad","",["Boezinge","Brielen","Dikkebus","Elverdinge","Hollebeke","Sint-Jan","Vlamertinge","Voormezele","Zillebeke","Zuidschote"],["Zonnebeke","Poperinge","Langemark-Poelkapelle","Wervik"],"Westhoek"),
 ("Zonnebeke","8980",WV,"gemeente","",["Beselare","Geluveld","Passendale","Zandvoorde"],["Ieper","Moorslede","Langemark-Poelkapelle","Staden","Wervik"],"Westhoek"),
 ("Oudenaarde","9700",OV,"stad","",["Bevere","Edelare","Eine","Ename","Heurne","Leupegem","Mater","Melden","Mullem","Nederename","Volkegem","Welden"],["Kruisem","Wortegem-Petegem","Kluisbergen","Ronse"],"Vlaamse Ardennen"),
 ("Kruisem","9770",OV,"gemeente","",["Kruishoutem","Zingem","Lozer","Nokere","Wannegem-Lede","Huise","Ouwegem"],["Oudenaarde","Waregem","Zulte","Wortegem-Petegem","Gavere"],"Vlaamse Ardennen"),
 # nieuw
 ("Brugge","8000",WV,"stad","",["Assebroek","Dudzele","Koolkerke","Lissewege","Sint-Andries","Sint-Kruis","Sint-Michiels","Zeebrugge"],["Oostkamp","Zedelgem","Beernem","Damme","Jabbeke"],"regio Brugge"),
 ("Oostende","8400",WV,"stad","",["Stene","Zandvoorde"],["Bredene","Middelkerke","Oudenburg","Gistel"],"kust"),
 ("Torhout","8820",WV,"stad","",[],["Lichtervelde","Kortemark","Zedelgem","Ichtegem","Oostkamp"],"regio Brugge"),
 ("Oostkamp","8020",WV,"gemeente","",["Hertsberge","Ruddervoorde","Waardamme"],["Brugge","Beernem","Zedelgem","Torhout"],"regio Brugge"),
 ("Zedelgem","8210",WV,"gemeente","",["Aartrijke","Loppem","Veldegem"],["Brugge","Oostkamp","Torhout","Jabbeke","Ichtegem"],"regio Brugge"),
 ("Beernem","8730",WV,"gemeente","",["Oedelem","Sint-Joris"],["Oostkamp","Brugge","Wingene","Aalter"],"regio Brugge"),
 ("Wingene","8750",WV,"gemeente","",["Zwevezele"],["Tielt","Ruiselede","Beernem","Pittem","Ardooie"],"regio Tielt"),
 ("Ruiselede","8755",WV,"gemeente","",["Doomkerke"],["Wingene","Tielt","Aalter","Beernem"],"regio Tielt"),
 ("Kortemark","8610",WV,"gemeente","",["Handzame","Werken","Zarren"],["Torhout","Hooglede","Diksmuide","Houthulst","Ichtegem"],"Westhoek"),
 ("Diksmuide","8600",WV,"stad","",["Beerst","Esen","Kaaskerke","Keiem","Lampernisse","Leke","Nieuwkapelle","Oostkerke","Oudekapelle","Pervijze","Sint-Jacobskapelle","Stuivekenskerke","Vladslo","Woumen"],["Kortemark","Houthulst","Lo-Reninge","Koekelare"],"Westhoek"),
 ("Poperinge","8970",WV,"stad","",["Krombeke","Proven","Roesbrugge-Haringe","Watou"],["Ieper","Vleteren","Heuvelland"],"Westhoek"),
 ("Langemark-Poelkapelle","8920",WV,"gemeente","",["Langemark","Poelkapelle","Bikschote"],["Ieper","Staden","Houthulst","Zonnebeke"],"Westhoek"),
 ("Spiere-Helkijn","8587",WV,"gemeente","",["Spiere","Helkijn"],["Avelgem","Zwevegem","Kooigem"],"regio Kortrijk"),
 ("Gent","9000",OV,"stad","",["Afsnee","Drongen","Gentbrugge","Ledeberg","Mariakerke","Oostakker","Sint-Amandsberg","Sint-Denijs-Westrem","Wondelgem","Zwijnaarde"],["Merelbeke","De Pinte","Sint-Martens-Latem","Destelbergen","Lochristi","Evergem"],"regio Gent"),
 ("Deinze","9800",OV,"stad","",["Astene","Bachte-Maria-Leerne","Gottem","Grammene","Meigem","Petegem-aan-de-Leie","Vinkt","Zeveren","Nevele","Landegem","Merendree"],["Zulte","Nazareth","Sint-Martens-Latem","Aalter","Dentergem","Kruisem"],"Leiestreek"),
 ("Nazareth","9810",OV,"gemeente","",["Eke"],["Deinze","De Pinte","Gavere","Kruisem"],"regio Gent"),
 ("De Pinte","9840",OV,"gemeente","",["Zevergem"],["Gent","Nazareth","Sint-Martens-Latem","Merelbeke","Gavere"],"regio Gent"),
 ("Sint-Martens-Latem","9830",OV,"gemeente","",["Deurle"],["Gent","De Pinte","Deinze","Nazareth"],"regio Gent"),
 ("Merelbeke","9820",OV,"gemeente","",["Bottelare","Lemberge","Melsen","Munte","Schelderode"],["Gent","Melle","De Pinte","Oosterzele","Gavere"],"regio Gent"),
 ("Gavere","9890",OV,"gemeente","",["Asper","Baaigem","Dikkelvenne","Semmerzake","Vurste"],["Nazareth","Kruisem","Zwalm","Merelbeke"],"Vlaamse Ardennen"),
 ("Wortegem-Petegem","9790",OV,"gemeente","",["Elsegem","Moregem","Ooike","Petegem-aan-de-Schelde"],["Oudenaarde","Waregem","Kruisem","Anzegem"],"Vlaamse Ardennen"),
 ("Kluisbergen","9690",OV,"gemeente","",["Berchem","Kwaremont","Ruien","Zulzeke"],["Avelgem","Oudenaarde","Ronse","Anzegem"],"Vlaamse Ardennen"),
 ("Ronse","9600",OV,"stad","",[],["Kluisbergen","Maarkedal","Oudenaarde"],"Vlaamse Ardennen"),
 ("Zottegem","9620",OV,"stad","",["Elene","Erwetegem","Godveerdegem","Grotenberge","Leeuwergem","Oombergen","Strijpen","Velzeke-Ruddershove"],["Zwalm","Oosterzele","Herzele","Brakel"],"Vlaamse Ardennen"),
 ("Aalter","9880",OV,"stad","",["Bellem","Lotenhulle","Poeke","Knesselare","Ursel"],["Deinze","Beernem","Ruiselede","Maldegem"],"regio Gent"),
]

ANGLES = [
 "vrije beroepen met een praktijk (wachtzaal, consultatieruimte, sanitair) en daarnaast hun woning",
 "kleine kantoren met een team van een handvol tot vijftien mensen: bureaus, keuken of refter, sanitair",
 "ondernemers met een kantoor aan huis: kantoor en woning in één plan, met splitsing op de factuur",
 "winkels en zaken in de dorpskern of het centrum: poetsen voor de deur opengaat",
 "familiebedrijven waar zaak en woning dicht bij elkaar liggen",
 "starters en jonge vennootschappen die hun eerste kantoor of praktijk inrichten",
 "zaakvoerders die veel onderweg zijn: kantoor en huis lopen door terwijl zij weg zijn",
 "praktijken en kantoren die liefst vroeg in de ochtend of over de middag laten poetsen, buiten de drukte",
 "bedrijven met een showroom of ontvangstruimte waar klanten binnenstappen",
 "land- en tuinbouwbedrijven met een vennootschap: bureau, refter en woning",
 "bedrijven die naast het poetsen ook de was en strijk, het koken of de boodschappen willen uitbesteden",
 "kmo's met een refter, kleedruimte en sanitair voor de ploeg",
]
SCEN = [
 "een kinesitherapeut met een praktijk aan huis", "een accountantskantoor met zes medewerkers", "een kapsalon in de dorpskern",
 "een architect die thuis werkt", "een bouwbedrijf met een kantoor en een refter voor de ploeg", "een tandartspraktijk met twee behandelkamers",
 "een IT-consultant met een thuiskantoor", "een notariskantoor met een wachtzaal", "een groepspraktijk van huisartsen",
 "een showroom met keukens of badkamers", "een landbouwbedrijf met een bureau aan de hoeve", "een webshop met een klein magazijn",
 "een advocatenkantoor met twee vennoten", "een opticien in een winkelstraat", "een verzekeringskantoor met een onthaal",
 "een interieurzaak met een toonzaal", "een logopediste met een praktijk aan huis", "een transportfirma met een chauffeursruimte",
]

def city_pages():
    out = []
    for i, (p, pc, prov, soort, deel, deelg, buurt, streek) in enumerate(PLAATSEN):
        s = slug(p)
        out.append(dict(id=f'poetshulp/{s}', path=f'poetshulp/{s}.html', kind='stad', group='poetshulp',
            h1=f'Poetshulp voor bedrijven in {p}', place=p, postcode=pc, provincie=prov, soort=soort, deel_van=deel,
            deelgemeenten=deelg, in_de_buurt=buurt, streek=streek,
            angle=ANGLES[(i * 5) % len(ANGLES)], scenario=SCEN[(i * 7) % len(SCEN)]))
    return out

REGIOS = [
 ("west-vlaanderen", "West-Vlaanderen", "provincie West-Vlaanderen", None),
 ("oost-vlaanderen", "Oost-Vlaanderen", "provincie Oost-Vlaanderen", None),
 ("regio-kortrijk", "de regio Kortrijk", "regio Kortrijk", "regio Kortrijk"),
 ("regio-roeselare", "de regio Roeselare", "regio Roeselare", "regio Roeselare"),
 ("regio-brugge", "de regio Brugge", "regio Brugge", "regio Brugge"),
 ("regio-gent", "de regio Gent", "regio Gent", "regio Gent"),
 ("leiestreek", "de Leiestreek", "Leiestreek", "Leiestreek"),
 ("westhoek", "de Westhoek", "Westhoek", "Westhoek"),
 ("vlaamse-ardennen", "de Vlaamse Ardennen", "Vlaamse Ardennen", "Vlaamse Ardennen"),
 ("regio-tielt", "de regio Tielt", "regio Tielt", "regio Tielt"),
]
def region_members(key):
    s, naam, label, streek = key
    if s == 'west-vlaanderen': return [p[0] for p in PLAATSEN if p[2] == WV and p[3] != 'deelgemeente']
    if s == 'oost-vlaanderen': return [p[0] for p in PLAATSEN if p[2] == OV]
    return [p[0] for p in PLAATSEN if p[7] == streek]

def region_pages():
    return [dict(id=f'poetshulp/{r[0]}', path=f'poetshulp/{r[0]}.html', kind='regio', group='poetshulp',
                 h1=f'Poetshulp voor bedrijven in {r[1]}', regio=r[2], members=region_members(r)) for r in REGIOS]

B_CITIES = ["Kortrijk", "Roeselare", "Waregem", "Ieper", "Izegem", "Menen", "Harelbeke", "Wevelgem", "Tielt", "Oudenaarde", "Brugge", "Gent"]
B_SERV = [
 ("kookhulp", "Kookhulp aan huis voor ondernemers in {p}", "koken bij de ondernemer thuis of schotels voor de week klaarzetten, weekmenu, rekening houden met allergieën en voorkeuren, boodschappen erbij"),
 ("boodschappendienst", "Boodschappendienst voor ondernemers in {p}", "wekelijkse boodschappen, voorraad aanvullen, apotheek, droogkuis en kleermaker, pakjes afgeven en ophalen, koffie en keukenvoorraad op kantoor"),
 ("hulp-in-huis", "Hulp in huis voor ondernemers in {p}", "allround hulp: poetsen, was en strijk, koken, boodschappen, kinderen ophalen en opvangen na school, tuin en terras, hond uitlaten, huis bijhouden tijdens de vakantie"),
]
def service_city_pages():
    PL = {p[0]: p for p in PLAATSEN}
    out = []
    for si, (key, h1, scope) in enumerate(B_SERV):
        for ci, c in enumerate(B_CITIES):
            p = PL[c]
            out.append(dict(id=f'regio/{key}-{slug(c)}', path=f'regio/{key}-{slug(c)}.html', kind='dienst-stad', group='regio',
                h1=h1.format(p=c), dienst=key, scope=scope, place=c, postcode=p[1], provincie=p[2], deelgemeenten=p[5], in_de_buurt=p[6],
                streek=p[7], scenario=SCEN[(ci * 5 + si * 3) % len(SCEN)]))
    return out

SECTOREN = [
 ("kleine-kantoren","Poetshulp voor kleine kantoren","kantoren met een klein team: bureaus, vergadertafel, keuken, sanitair, vloeren, afval"),
 ("kmo","Poetshulp voor kmo's","kmo's met kantoor, refter, kleedruimte en sanitair naast een atelier of magazijn (geen industriële reiniging van productiehallen)"),
 ("coworkings","Poetshulp voor coworkings en gedeelde kantoren","gedeelde werkplekken, flexplekken, keuken, vergaderruimtes, veel wisselende gebruikers"),
 ("winkels","Poetshulp voor winkels en boetieks","winkelvloer, paskamers, toonbank, etalage langs binnen, stockruimte, poetsen voor de opening"),
 ("showrooms","Poetshulp voor showrooms","toonzalen met keukens, badkamers, meubels of wagens: stof, glas langs binnen, vloeren, onthaal"),
 ("kapsalons","Poetshulp voor kapsalons","salon, wasbakken, haar op de vloer, spiegels, handdoeken wassen en drogen, personeelsruimte"),
 ("schoonheidsinstituten","Poetshulp voor schoonheidsinstituten","behandelkamers, onthaal, linnen en handdoeken, sanitair, rustige uitstraling (de hygiëne van instrumenten blijft bij de zaak)"),
 ("groepspraktijken","Poetshulp voor groepspraktijken","praktijken met meerdere zorgverleners: gedeelde wachtzaal, onthaal, consultatieruimtes, sanitair, teamkeuken (geen sterilisatie of medisch materiaal)"),
 ("paramedische-praktijken","Poetshulp voor paramedische praktijken","kinesitherapeuten, logopedisten, diëtisten, podologen, ergotherapeuten: behandelruimtes, oefenzaal, wachtzaal"),
 ("it-bedrijven","Poetshulp voor IT-bedrijven","kantoren met veel schermen en toetsenborden, kabels, vergaderruimtes, keuken en koffiehoek, voorzichtig rond apparatuur"),
 ("start-ups","Poetshulp voor start-ups en scale-ups","snel groeiende teams, wisselende kantoorindeling, keuken en ontspanningshoek, flexibel bijsturen"),
 ("bouwbedrijven","Poetshulp voor bouwbedrijven","kantoor, refter en kleedruimte voor de ploeg, modder en stof van de werf aan de ingang (geen werf- of bouwopkuis)"),
 ("transportbedrijven","Poetshulp voor transportbedrijven","planningskantoor, chauffeursruimte, refter, douches en sanitair (geen reiniging van vrachtwagens)"),
 ("productiebedrijven","Poetshulp voor de kantoren van productiebedrijven","administratieve kantoren, onthaal, refter en sanitair van een productiebedrijf (geen industriële reiniging van de productiehal)"),
 ("autobedrijven","Poetshulp voor garages en autobedrijven","showroom, verkoopkantoor, klantenonthaal en wachtruimte, sanitair (geen reiniging van de werkplaats of wagens)"),
 ("interieurzaken","Poetshulp voor interieurzaken","toonzaal met meubels en decoratie, stof afnemen, glas langs binnen, vloeren, onthaal"),
 ("opticiens","Poetshulp voor opticiens","winkel met glazen vitrines en spiegels, onthaal, meetruimte, sanitair (de monturen en meetapparatuur blijven bij de opticien)"),
 ("reisbureaus","Poetshulp voor reisbureaus","winkelkantoor met onthaal en klantentafels, folders, vitrines, keuken en sanitair"),
 ("fitness-en-yogastudios","Poetshulp voor fitness- en yogastudio's","zalen, matten en toestellen afnemen, kleedkamers en douches, onthaal (overdag, tussen de lessen of in de daluren)"),
 ("vzw","Poetshulp voor vzw's en verenigingen","secretariaat, ontmoetingsruimte, keuken, sanitair, factuur op naam van de vzw"),
 ("webshops","Poetshulp voor webshops met kantoor en magazijn","kantoor, inpakruimte, refter en sanitair van een webshop (licht onderhoud van het magazijn, geen industriële vloermachines)"),
 ("familiebedrijven","Poetshulp voor familiebedrijven","familiebedrijven waar zaak en woning dicht bij elkaar liggen: kantoor, refter en de woning van de zaakvoerders in één plan"),
 ("landbouwbedrijven","Huishoudhulp en poetshulp voor landbouwbedrijven","land- en tuinbouwbedrijven met een vennootschap: bureau aan de hoeve, refter, woning, was en koken in drukke seizoenen (geen stallen of serres)"),
 ("installateurs","Poetshulp voor installateurs en technische bedrijven","elektriciens, loodgieters, HVAC-installateurs: kantoor, onthaal, refter en kleedruimte, en de woning van de zaakvoerder (geen technische werken)"),
 ("interimkantoren","Poetshulp voor interimkantoren","kantoor met veel bezoekers: onthaal, gesprekshoeken, sanitair, keuken"),
 ("drukkerijen","Poetshulp voor drukkerijen","kantoor, onthaal en toonruimte, refter en sanitair van een drukkerij (niet de drukmachines of productieruimte)"),
 ("eventbureaus","Poetshulp voor eventbureaus","kantoor en ontvangstruimte, opslag van materiaal netjes houden, keuken en sanitair (geen opkuis van events in het weekend)"),
 ("rijscholen","Poetshulp voor rijscholen","kantoor met onthaal, theorielokaal, sanitair (geen reiniging van lesvoertuigen)"),
]
RUIMTES = [
 ("refter-en-bedrijfskeuken","Poetshulp voor de refter en de bedrijfskeuken","refter, koelkast, microgolf, koffiemachine, tafels, vaatwasser, afval"),
 ("sanitair-op-kantoor","Sanitair op kantoor laten poetsen","toiletten, lavabo's, spiegels, aanvullen van papier en zeep, vloeren, regelmaat"),
 ("vergaderzalen","Poetshulp voor vergaderzalen","vergadertafels, stoelen, schermen en whiteboards langs de buitenkant, glazen wanden, klaarzetten voor de volgende vergadering"),
 ("onthaal-en-wachtruimte","Poetshulp voor onthaal en wachtruimte","eerste indruk, balie, zitjes, tijdschriften, deurklinken, ramen langs binnen, ingangsmat"),
 ("kleedkamers-en-douches","Poetshulp voor kleedkamers en douches op het werk","kleedkamers, lockers langs de buitenkant, douches, vloeren, ventilatie en geurtjes"),
]
SITUATIES = [
 ("kantoorverhuis","Poetshulp bij een kantoorverhuis","poetsen van het nieuwe kantoor voor de verhuis en van het oude kantoor erna, als losse opdracht, daarna eventueel een vast plan"),
 ("voorjaarspoets-kantoor","Een grote voorjaarspoets op kantoor","jaarlijkse grote poetsbeurt: kasten, plinten, ramen langs binnen, archief stofvrij, als losse opdracht of in het vaste plan"),
 ("poetshulp-tijdens-bouwverlof","Poetshulp tijdens het bouwverlof","de stille weken in de zomer gebruiken voor een grondige poetsbeurt, het kantoor klaar voor de herstart"),
 ("eindejaarspoets","Eindejaarspoets voor bedrijven","kantoor opgeruimd en proper het nieuwe jaar in, archief, keuken, frigo"),
 ("nieuw-kantoor-of-praktijk","Poetshulp voor een nieuw kantoor of een nieuwe praktijk","opstart van een nieuwe vestiging: eerste grondige poetsbeurt, daarna een vast ritme vanaf dag één"),
 ("kantoor-poetsen-tijdens-verbouwing","Je kantoor poetsen tijdens een verbouwing","stof en vuil tijdens verbouwingswerken onder controle houden in de ruimtes die in gebruik blijven (geen bouwopkuis na oplevering door aannemers)"),
 ("na-een-receptie","Poetshulp na een receptie of personeelsfeest op kantoor","de ochtend na een receptie, nieuwjaarsdrink of teamfeest op een weekdag: opruimen, keuken, glazen, vloeren"),
]
def sector_pages():
    out = []
    for s, h1, scope in SECTOREN: out.append(dict(id=f'sectoren/{s}', path=f'sectoren/{s}.html', kind='sector', group='sectoren', h1=h1, scope=scope))
    for s, h1, scope in RUIMTES: out.append(dict(id=f'sectoren/{s}', path=f'sectoren/{s}.html', kind='ruimte', group='sectoren', h1=h1, scope=scope))
    for s, h1, scope in SITUATIES: out.append(dict(id=f'sectoren/{s}', path=f'sectoren/{s}.html', kind='situatie', group='sectoren', h1=h1, scope=scope))
    return out

VRAGEN = [
 ("welk-bedrijf-poetshulp-voor-bedrijven","Welk bedrijf levert poetshulp voor bedrijven in West- en Oost-Vlaanderen?"),
 ("goede-poetshulp-voor-kantoor-vinden","Hoe vind je een goede poetshulp voor je kantoor?"),
 ("wat-bepaalt-prijs-poetshulp-bedrijf","Wat bepaalt de prijs van poetshulp voor een bedrijf?"),
 ("is-poetshulp-kantoor-aftrekbaar","Is poetshulp voor je kantoor fiscaal aftrekbaar?"),
 ("poetshulp-thuis-via-bv-betalen","Kan ik mijn poetshulp thuis via mijn BV betalen?"),
 ("poetshulp-eenmanszaak","Kan een eenmanszaak poetshulp inboeken?"),
 ("hoe-vaak-kantoor-poetsen","Hoe vaak moet je een kantoor laten poetsen?"),
 ("hoeveel-uur-poetshulp-kantoor","Hoeveel uur poetshulp heeft een kantoor nodig?"),
 ("wat-doet-poetshulp-op-kantoor","Wat doet een poetshulp op kantoor, en wat niet?"),
 ("kantoor-poetsen-buiten-kantooruren","Kan je kantoor buiten de kantooruren gepoetst worden?"),
 ("wie-voorziet-poetsmateriaal","Wie voorziet het poetsmateriaal: jij of de poetsfirma?"),
 ("vertrouwelijke-documenten-poetshulp","Hoe ga je om met vertrouwelijke documenten als er een poetshulp komt?"),
 ("duurzaam-kantoor-poetsen","Hoe laat je je kantoor duurzaam poetsen?"),
 ("poetshulp-in-dienst-of-uitbesteden","Neem je een poetshulp zelf in dienst of besteed je het uit?"),
 ("poetshulp-ziek-of-met-verlof","Wat als je poetshulp ziek is of met verlof gaat?"),
 ("schoonmaakplan-kantoor-maken","Hoe maak je een schoonmaakplan voor je kantoor?"),
 ("schoonmaakplan-winkel-maken","Hoe maak je een schoonmaakplan voor je winkel?"),
 ("vragen-aan-poetsfirma","Welke vragen stel je aan een poetsfirma voor je bedrijf?"),
 ("kantoor-en-woning-een-poetshulp","Kan één poetshulp je kantoor en je woning doen, op één factuur?"),
 ("poetsabonnement-opzeggen","Kan je een poetsabonnement voor je bedrijf maandelijks opzeggen?"),
 ("eerste-maand-poetshulp-kantoor","Hoe verloopt de eerste maand met een poetshulp op kantoor?"),
 ("hygiene-afspraken-praktijk","Welke afspraken maak je over hygiëne met de poetshulp van je praktijk?"),
 ("thuis-laten-koken-terwijl-je-werkt","Kan iemand bij je thuis komen koken terwijl je werkt?"),
 ("boodschappen-laten-doen-ondernemer","Kan je als ondernemer je boodschappen laten doen?"),
 ("strijk-laten-doen-via-zaak","Kan je je strijk thuis laten doen via je zaak?"),
 ("hulp-in-huis-voor-zelfstandigen","Welke hulp in huis bestaat er voor zelfstandigen en zaakvoerders?"),
 ("huishoudhulp-als-extralegaal-voordeel","Kan je huishoudhulp aanbieden als extralegaal voordeel?"),
 ("hoe-snel-start-poetshulp","Hoe snel kan een poetshulp voor je bedrijf starten?"),
 ("verschil-poetshulp-en-kantoorschoonmaak","Wat is het verschil tussen poetshulp en kantoorschoonmaak?"),
 ("wie-komt-er-poetsen-bij-zondags","Wie komt er poetsen bij Zondags?"),
 ("poetshulp-met-contract-en-factuur","Waarom kies je voor een poetshulp met contract en factuur?"),
 ("vaste-poetshulp-of-losse-opdracht","Vaste poetshulp of een losse opdracht: wat past bij je bedrijf?"),
 ("wachtzaal-proper-houden","Hoe hou je een wachtzaal proper tussen twee poetsbeurten?"),
 ("poetshulp-die-ook-kookt","Kan je poetshulp ook koken en boodschappen doen?"),
 ("werkt-zondags-voor-particulieren","Werkt Zondags ook voor particulieren?"),
 ("op-welke-uren-komt-poetshulp","Op welke uren komt een poetshulp van Zondags?"),
 ("van-poetshulp-wisselen","Kan je van poetshulp wisselen als het niet klikt?"),
 ("poetshulp-aanvragen-bedrijf","Hoe vraag je poetshulp voor je bedrijf aan?"),
 ("btw-vrijgestelde-praktijk-poetshulp","Kan een btw-vrijgestelde praktijk de btw op poetshulp recupereren?"),
 ("doet-poetshulp-de-ramen","Doet een poetshulp ook de ramen?"),
 ("was-en-strijk-van-je-zaak","Kan je poetshulp ook de was en strijk van je zaak doen?"),
 ("poetsfirma-of-dienstenchequebedrijf","Wat is het verschil tussen een poetsfirma en een dienstenchequebedrijf?"),
 ("afspraken-met-poetsfirma","Welke afspraken leg je vast met een poetsfirma?"),
 ("kwaliteit-schoonmaak-controleren","Hoe controleer je de kwaliteit van de schoonmaak op kantoor?"),
]
def question_pages():
    return [dict(id=f'vragen/{s}', path=f'vragen/{s}.html', kind='vraag', group='vragen', h1=q) for s, q in VRAGEN]

def plan():
    pages = city_pages() + region_pages() + service_city_pages() + sector_pages() + question_pages()
    return pages

if __name__ == '__main__':
    P = plan()
    ids = [p['id'] for p in P]
    assert len(ids) == len(set(ids)), 'dubbele id'
    os.makedirs('_tools/content', exist_ok=True)
    json.dump(P, open('_tools/content/plan.json', 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(P), Counter(p['kind'] for p in P))
