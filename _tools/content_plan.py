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
 # week 2b (6 oktober 2026): extra gemeenten in Oost-Vlaanderen
 ("Lochristi","9080",OV,"gemeente","",["Beervelde","Zaffelare","Zeveneken"],["Gent","Destelbergen","Lokeren","Wachtebeke","Laarne"],"regio Gent"),
 ("Destelbergen","9070",OV,"gemeente","",["Heusden"],["Gent","Lochristi","Laarne","Wetteren","Melle"],"regio Gent"),
 ("Evergem","9940",OV,"gemeente","",["Ertvelde","Kluizen","Sleidinge"],["Gent","Lievegem","Zelzate","Assenede","Kaprijke"],"regio Gent"),
 ("Lievegem","9920",OV,"gemeente","",["Lovendegem","Vinderhoute","Waarschoot","Zomergem","Oostwinkel","Ronsele"],["Gent","Evergem","Eeklo","Aalter","Deinze"],"Meetjesland"),
 ("Wetteren","9230",OV,"gemeente","",["Massemen","Westrem"],["Destelbergen","Laarne","Wichelen","Lede","Oosterzele","Melle"],"regio Gent"),
 ("Oosterzele","9860",OV,"gemeente","",["Balegem","Gijzenzele","Landskouter","Moortsele","Scheldewindeke"],["Merelbeke","Zottegem","Herzele","Sint-Lievens-Houtem","Wetteren"],"regio Gent"),
 ("Herzele","9550",OV,"gemeente","",["Borsbeke","Hillegem","Ressegem","Sint-Antelinks","Sint-Lievens-Esse","Steenhuize-Wijnhuize","Woubrechtegem"],["Zottegem","Oosterzele","Sint-Lievens-Houtem","Haaltert","Lierde"],"Vlaamse Ardennen"),
 ("Brakel","9660",OV,"gemeente","",["Elst","Everbeek","Michelbeke","Nederbrakel","Opbrakel","Parike","Zegelsem"],["Zottegem","Zwalm","Horebeke","Lierde","Geraardsbergen","Maarkedal"],"Vlaamse Ardennen"),
 ("Zwalm","9630",OV,"gemeente","",["Beerlegem","Dikkele","Hundelgem","Meilegem","Munkzwalm","Paulatem","Roborst","Rozebeke","Sint-Blasius-Boekel","Sint-Denijs-Boekel","Sint-Maria-Latem"],["Oudenaarde","Zottegem","Brakel","Gavere","Horebeke"],"Vlaamse Ardennen"),
 ("Maarkedal","9680",OV,"gemeente","",["Etikhove","Maarke-Kerkem","Nukerke","Schorisse"],["Ronse","Oudenaarde","Horebeke","Brakel","Kluisbergen"],"Vlaamse Ardennen"),
 ("Lierde","9570",OV,"gemeente","",["Deftinge","Hemelveerdegem","Sint-Maria-Lierde","Sint-Martens-Lierde"],["Geraardsbergen","Brakel","Zottegem","Herzele","Ninove"],"Vlaamse Ardennen"),
 ("Geraardsbergen","9500",OV,"stad","",["Goeferdinge","Grimminge","Idegem","Moerbeke","Nederboelare","Nieuwenhove","Onkerzele","Ophasselt","Overboelare","Schendelbeke","Smeerebbe-Vloerzegem","Viane","Zandbergen","Zarlardinge"],["Ninove","Lierde","Brakel"],"Denderstreek"),
 ("Ninove","9400",OV,"stad","",["Appelterre-Eichem","Aspelare","Denderwindeke","Lieferinge","Meerbeke","Nederhasselt","Neigem","Okegem","Outer","Pollare","Voorde"],["Denderleeuw","Haaltert","Geraardsbergen","Lierde"],"Denderstreek"),
 ("Aalst","9300",OV,"stad","",["Baardegem","Erembodegem","Gijzegem","Herdersem","Hofstade","Meldert","Moorsel","Nieuwerkerken"],["Lede","Erpe-Mere","Haaltert","Denderleeuw","Lebbeke"],"Denderstreek"),
 ("Lede","9340",OV,"gemeente","",["Impe","Oordegem","Smetlede","Wanzele"],["Aalst","Erpe-Mere","Wichelen","Wetteren","Oosterzele"],"Denderstreek"),
 ("Erpe-Mere","9420",OV,"gemeente","",["Aaigem","Bambrugge","Burst","Erondegem","Ottergem","Vlekkem","Mere"],["Aalst","Lede","Haaltert","Herzele","Sint-Lievens-Houtem"],"Denderstreek"),
 ("Dendermonde","9200",OV,"stad","",["Appels","Baasrode","Grembergen","Mespelare","Oudegem","Schoonaarde","Sint-Gillis-bij-Dendermonde"],["Hamme","Zele","Berlare","Lebbeke","Buggenhout","Wichelen"],"Denderstreek"),
 ("Zele","9240",OV,"gemeente","",[],["Dendermonde","Berlare","Lokeren","Hamme","Waasmunster","Laarne"],"Scheldeland"),
 ("Berlare","9290",OV,"gemeente","",["Overmere","Uitbergen"],["Zele","Dendermonde","Wichelen","Laarne"],"Scheldeland"),
 ("Hamme","9220",OV,"gemeente","",["Moerzeke"],["Dendermonde","Zele","Waasmunster","Temse"],"Scheldeland"),
 ("Lokeren","9160",OV,"stad","",["Daknam","Eksaarde"],["Zele","Waasmunster","Lochristi","Sint-Niklaas"],"Waasland"),
 ("Sint-Niklaas","9100",OV,"stad","",["Belsele","Nieuwkerken-Waas","Sinaai"],["Beveren","Temse","Waasmunster","Stekene","Sint-Gillis-Waas","Lokeren"],"Waasland"),
 ("Eeklo","9900",OV,"stad","",[],["Kaprijke","Maldegem","Lievegem","Sint-Laureins"],"Meetjesland"),
 ("Maldegem","9990",OV,"gemeente","",["Adegem","Middelburg"],["Eeklo","Aalter","Sint-Laureins","Beernem"],"Meetjesland"),
]

ANGLES = [
 "vrije beroepen met een praktijk (wachtzaal, consultatieruimte, sanitair) die buiten de consulturen gepoetst wil worden",
 "kleine kantoren met een team van een handvol tot vijftien mensen: bureaus, keuken of refter, sanitair",
 "kleine bedrijven in een verhuurd kantoor of bedrijfsunit die poetshulp en administratieve hulp willen combineren",
 "winkels en zaken in de dorpskern of het centrum: poetsen voor de deur opengaat",
 "familiebedrijven met een klein team waar niemand tijd heeft om te poetsen",
 "starters en jonge vennootschappen die hun eerste kantoor of praktijk inrichten",
 "bedrijfsleiders die veel onderweg zijn en een rechterhand zoeken die het kantoor en het regelwerk laat doorlopen",
 "praktijken en kantoren die liefst vroeg in de ochtend of over de middag laten poetsen, buiten de drukte",
 "bedrijven met een showroom of ontvangstruimte waar klanten binnenstappen",
 "landbouwbedrijven met een vennootschap: bureau, refter en kleedruimte",
 "bedrijven die naast het poetsen ook administratie, post en regelwerk willen uitbesteden",
 "kmo's met een refter, kleedruimte en sanitair voor de ploeg",
]
SCEN = [
 "een kinesitherapeut met een praktijk in een winkelstraat", "een accountantskantoor met zes medewerkers", "een kapsalon in de dorpskern",
 "een architectenbureau met een vergaderzaal", "een bouwbedrijf met een kantoor en een refter voor de ploeg", "een tandartspraktijk met twee behandelkamers",
 "een IT-consultant met een kantoor voor vijf mensen", "een notariskantoor met een wachtzaal", "een groepspraktijk van huisartsen",
 "een showroom met keukens of badkamers", "een landbouwbedrijf met een bureau aan de hoeve", "een webshop met een klein magazijn",
 "een advocatenkantoor met twee vennoten", "een opticien in een winkelstraat", "een verzekeringskantoor met een onthaal",
 "een interieurzaak met een toonzaal", "een logopediste met een groepspraktijk", "een transportfirma met een chauffeursruimte",
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
# week 2 (5 oktober 2026): dezelfde drie diensten voor alle overige gemeenten (geen deelgemeenten) uit het plan
B_CITIES2 = [p[0] for p in PLAATSEN if p[3] != 'deelgemeente' and p[0] not in B_CITIES]
def service_city_pages():
    PL = {p[0]: p for p in PLAATSEN}
    out = []
    for si, (key, h1, scope) in enumerate(B_SERV):
        for ci, c in enumerate(B_CITIES + B_CITIES2):
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
 ("familiebedrijven","Poetshulp voor familiebedrijven","familiebedrijven met een klein team waar niemand tijd heeft om te poetsen: kantoor, refter en de woning van de zaakvoerders in één plan"),
 ("landbouwbedrijven","Poetshulp voor landbouwbedrijven","landbouwbedrijven met een vennootschap: bureau aan de hoeve, refter en kleedruimte in drukke seizoenen (geen stallen of serres)"),
 ("installateurs","Poetshulp voor installateurs en technische bedrijven","elektriciens, loodgieters, HVAC-installateurs: kantoor, onthaal, refter en kleedruimte (geen technische werken)"),
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

# ---------------- KANDIDATEN (werken/<soort>-<plaats>): voor wie werk zoekt bij Zondags ----------------
K_CITIES = ["Kortrijk", "Roeselare", "Waregem", "Ieper", "Izegem", "Menen", "Harelbeke", "Wevelgem", "Tielt", "Oudenaarde", "Brugge", "Gent",
            "Deinze", "Oostende", "Torhout", "Zwevegem", "Aalter", "Zottegem", "Ronse", "Poperinge", "Kuurne", "Merelbeke"]
# week 2b: kandidatenpagina's voor de overige gemeenten van het oorspronkelijke plan (zonder deelgemeenten en zonder de nieuwe Oost-Vlaamse gemeenten)
K_CITIES = K_CITIES + [p[0] for p in PLAATSEN[:PLAATSEN.index(next(q for q in PLAATSEN if q[0] == "Lochristi"))] if p[3] != 'deelgemeente' and p[0] not in K_CITIES]
K_SOORT = [
 ("studentenjob", "Studentenjob met flexibele uren in {p}", "studenten vanaf 18 jaar: een job overdag op weekdagen bij vaste klanten, met dagen en uren die samen met de student rond het lessenrooster worden gekozen (vrije voormiddagen, vrije namiddagen, schoolvakanties); studentencontract, de student volgt zelf het urensaldo op via Student@work", ['PART_TIME', 'TEMPORARY']),
 ("flexi-job", "Flexi-job of bijverdienen in {p}", "bijverdienen naast een hoofdjob, als gepensioneerde of op een vrije dag: een paar uur per week overdag bij vaste klanten; of een flexi-job mogelijk is hangt af van de eigen situatie, Zondags bekijkt het statuut samen met de kandidaat (nooit beloven dat een flexi-job kan); anders zoeken we samen een statuut dat wel past", ['PART_TIME']),
 ("vaste-job-overdag", "Vaste job overdag zonder weekends in {p}", "een vast contract, deeltijds of voltijds, overdag op weekdagen bij vaste klanten, nooit 's avonds of in het weekend; kan ook enkel binnen de schooluren; voor herintreders, zij-instromers, ouders en wie zekerheid zoekt", ['FULL_TIME', 'PART_TIME']),
]
K_PERSONA = [
 "een student verpleegkunde met lessen vooral in de voormiddag", "een student die op kot zit en in de vakanties extra wil werken",
 "een masterstudent met twee vrije namiddagen per week", "een student office management die graag met planning en administratie bezig is",
 "een bediende met een vierdagenweek die de vrije dag wil invullen", "een gepensioneerde die een paar voormiddagen per week wil werken",
 "een zelfstandige in bijberoep die vaste uren zoekt", "een ploegarbeider met vrije voormiddagen in bepaalde weken",
 "een mama of papa die wil werken binnen de schooluren", "een herintreder na enkele jaren pauze",
 "een zij-instromer uit de horeca die geen avonden en weekends meer wil", "iemand uit de winkelsector die een rooster zonder zaterdagen zoekt",
 "iemand die graag actief bezig is en liever niet de hele dag achter een bureau zit", "iemand die van orde en structuur houdt",
]
def candidate_pages():
    PL = {p[0]: p for p in PLAATSEN}
    out = []
    for si, (key, h1, scope, emp) in enumerate(K_SOORT):
        for ci, c in enumerate(K_CITIES):
            p = PL[c]
            out.append(dict(id=f'werken/{key}-{slug(c)}', path=f'werken/{key}-{slug(c)}.html', kind='kandidaat', group='werken',
                h1=h1.format(p=c), soort_job=key, scope=scope, employment=emp, place=c, postcode=p[1], provincie=p[2],
                deelgemeenten=p[5], in_de_buurt=p[6], streek=p[7], persona=K_PERSONA[(ci * 3 + si * 5) % len(K_PERSONA)]))
    return out


# ---------------- 7 OKTOBER 2026: 502 extra pagina's (Kortrijk-focus, schoonmaak, au pair, grotere kinderen) ----------------
PL_MAP = {p[0]: p for p in PLAATSEN}
def _ctx(c):
    p = PL_MAP[c]
    return dict(place=c, postcode=p[1], provincie=p[2], soort=p[3], deel_van=p[4], deelgemeenten=p[5], in_de_buurt=p[6], streek=p[7])

N_SERV = {
 "schoonmaak-kantoor": ("Schoonmaakhulp voor kantoren in {p}", "wekelijks of tweewekelijks onderhoud van kantoren: bureaus, vergaderruimte, keuken, sanitair, vloeren, afval; dezelfde vaste persoon, overdag op weekdagen"),
 "schoonmaak-praktijk": ("Schoonmaakhulp voor praktijken in {p}", "praktijken van vrije beroepen en zorgverleners: wachtzaal, onthaal, consultatie- en behandelruimtes, sanitair; geen sterilisatie of medisch materiaal"),
 "schoonmaak-winkel": ("Schoonmaakhulp voor winkels in {p}", "winkelvloer, paskamers, toonbank, etalage langs binnen, stockruimte, sanitair; poetsen voor de winkel opengaat"),
 "kookhulp": ("Kookhulp aan huis voor ondernemers in {p}", "koken bij de ondernemer thuis of schotels voor de week klaarzetten, weekmenu, allergieën en voorkeuren"),
 "boodschappendienst": ("Boodschappendienst voor ondernemers in {p}", "wekelijkse boodschappen, voorraad aanvullen, apotheek, droogkuis, pakjes, koffie en keukenvoorraad op kantoor"),
 "hulp-in-huis": ("Hulp in huis voor ondernemers in {p}", "allround hulp: poetsen, was en strijk, koken, boodschappen, kinderen ophalen, tuin en terras, hond uitlaten"),
 "au-pair-alternatief": ("Alternatief voor een au pair voor ondernemers in {p}", "ondernemersgezinnen die overwegen een au pair te nemen en een vaste hulp overdag zonder inwonende persoon willen vergelijken: wat een au pair typisch is (een uitwisselingsprogramma met een gastgezin, regels bij het bureau of de organisatie nakijken) en wat Zondags anders doet: een vaste Zondag in dienst van Zondags, overdag op weekdagen, niemand die bij je inwoont"),
 "vaste-huishoudhulp-ipv-au-pair": ("Vaste huishoudhulp in plaats van een au pair in {p}", "een vaste huishoudhulp overdag voor poetsen, was en strijk, koken en boodschappen als alternatief voor een au pair: vaste dag en uur, factuur op de vennootschap, geen inwoning, geen kamer nodig, bij ziekte of verlof zoeken we een oplossing"),
 "hulp-ondernemersgezin-schoolkinderen": ("Hulp voor ondernemersgezinnen met schoolkinderen in {p}", "gezinnen met kinderen in het lager en de eerste jaren van het secundair: kinderen ophalen van school, vieruurtje, opvang tot ouders thuis zijn, plus huishouden, was en strijk en koken; Zondags is geen erkende kinderopvang en doet geen baby's of peuters"),
 "kinderen-ophalen-school": ("Kinderen laten ophalen van school in {p}", "een vaste Zondag staat aan de schoolpoort, brengt de kinderen naar huis of naar de training, in overleg met de school en de ouders; grotere kinderen van het lager en de eerste jaren van het secundair; geen baby's of peuters"),
 "opvang-na-school": ("Opvang na school aan huis in {p}", "een vaste Zondag vangt de kinderen na school op bij het gezin thuis tot de ouders thuiskomen: vieruurtje, rustig huiswerkmoment, huisregels volgen; geen erkende kinderopvang, geen huiswerkbegeleiding beloven"),
 "opvang-woensdagnamiddag": ("Opvang op woensdagnamiddag in {p}", "de woensdagnamiddag als vast moment: een vaste Zondag ontvangt de kinderen thuis na school, middageten of vieruurtje, vervoer naar activiteiten in overleg; overdag op weekdagen"),
 "vieruurtje-en-avondeten": ("Vieruurtje en avondeten voor schoolkinderen in {p}", "vieruurtje klaarzetten en het avondeten koken of opwarmen voor de kinderen terwijl de ouders nog werken; rekening houden met allergieën en voorkeuren; combineren met ophalen van school"),
}
N_H1 = {k: v[0] for k, v in N_SERV.items()}
N_SCOPE = {k: v[1] for k, v in N_SERV.items()}

def _dienst_page(key, c, i, extra_angle=True):
    ctx = _ctx(c)
    return dict(id=f'regio/{key}-{slug(c)}', path=f'regio/{key}-{slug(c)}.html', kind='dienst-stad', group='regio',
        h1=N_H1[key].format(p=c), dienst=key, scope=N_SCOPE[key], scenario=SCEN[(i * 5 + len(key)) % len(SCEN)],
        angle=ANGLES[(i * 7 + len(key)) % len(ANGLES)], **ctx)

# blok 1: schoonmaakhulp voor kantoren, praktijken en winkels in 40 gemeenten (120)
N_CITIES = [p[0] for p in PLAATSEN if p[3] != 'deelgemeente'][:40]
def block1():
    return [_dienst_page(k, c, i) for k in ("schoonmaak-kantoor", "schoonmaak-praktijk", "schoonmaak-winkel") for i, c in enumerate(N_CITIES)]

# blok 2: de 7 deelgemeenten van Kortrijk x 5 diensten (35)
KORTRIJK_DEEL = ["Marke", "Heule", "Bissegem", "Aalbeke", "Bellegem", "Rollegem", "Kooigem"]
def block2():
    return [_dienst_page(k, c, i) for k in ("schoonmaak-kantoor", "schoonmaak-praktijk", "kookhulp", "boodschappendienst", "hulp-in-huis") for i, c in enumerate(KORTRIJK_DEEL)]

# blok 3: ruimtes in Kortrijk en omgeving (5 ruimtes x 8 plaatsen = 40)
RUIMTE_STAD = [
 ("refter-en-bedrijfskeuken", "Refter en bedrijfskeuken laten poetsen in {p}", "refter, koelkast, microgolf, koffiemachine, tafels, vaatwasser, afval"),
 ("sanitair-op-kantoor", "Sanitair op kantoor laten poetsen in {p}", "toiletten, lavabo's, spiegels, aanvullen van papier en zeep, vloeren, regelmaat"),
 ("vergaderzalen", "Vergaderzalen laten schoonmaken in {p}", "vergadertafels, stoelen, schermen en whiteboards langs de buitenkant, glazen wanden, klaarzetten voor de volgende vergadering"),
 ("onthaal-en-wachtruimte", "Onthaal en wachtruimte laten poetsen in {p}", "eerste indruk, balie, zitjes, tijdschriften, deurklinken, ramen langs binnen, ingangsmat"),
 ("kleedkamers-en-douches", "Kleedkamers en douches op het werk laten poetsen in {p}", "kleedkamers, lockers langs de buitenkant, douches, vloeren, ventilatie en geurtjes"),
]
R_CITIES = ["Kortrijk", "Wevelgem", "Menen", "Harelbeke", "Zwevegem", "Kuurne", "Waregem", "Izegem"]
def block3():
    out = []
    for ri, (key, h1, scope) in enumerate(RUIMTE_STAD):
        for ci, c in enumerate(R_CITIES):
            out.append(dict(id=f'sectoren/{key}-{slug(c)}', path=f'sectoren/{key}-{slug(c)}.html', kind='ruimte-stad', group='sectoren',
                h1=h1.format(p=c), ruimte=key, scope=scope, scenario=SCEN[(ci * 3 + ri * 5) % len(SCEN)],
                angle=ANGLES[(ci * 5 + ri * 3) % len(ANGLES)], **_ctx(c)))
    return out

# blok 4: 28 sectoren x 3 invalshoeken (84)
def block4():
    out = []
    for si, (s, h1, scope) in enumerate(SECTOREN):
        lbl = h1.split(' voor ', 1)[1]
        variants = [
         ('checklist', f'Schoonmaakchecklist voor {lbl}', 'een concrete checklist: wat wekelijks, wat maandelijks en wat jaarlijks aan de beurt komt in deze soort zaak, en wat de zaak zelf blijft doen'),
         ('zaak-en-woning', f'Zaak en woning in één plan: hulp voor {lbl}', 'de zaakvoerder van dit soort bedrijf laat zaak en woning door dezelfde vaste persoon doen, met splitsing op de factuur tussen beroepsmatig en privé, en de nodige fiscale voorzichtigheid'),
         ('regio-kortrijk', f'Poetshulp voor {lbl} in Kortrijk en omgeving', 'lokale invalshoek Kortrijk, de deelgemeenten en de buurgemeenten uit het plan van poetshulp/kortrijk: hoe het werkt, wanneer er gepoetst wordt, hoe je start'),
        ]
        for vi, (vk, vh1, vscope) in enumerate(variants):
            out.append(dict(id=f'sectoren/{s}-{vk}', path=f'sectoren/{s}-{vk}.html', kind='sector-dienst', group='sectoren',
                h1=vh1, sector=s, sector_h1=h1, sector_scope=scope, variant=vk, scope=vscope,
                scenario=SCEN[(si * 3 + vi * 7) % len(SCEN)]))
    return out

# blok 5: au pair en vaste hulp (12 steden x 3 + 24 vragen = 60)
B_CITIES_N = ["Kortrijk", "Roeselare", "Waregem", "Ieper", "Izegem", "Menen", "Harelbeke", "Wevelgem", "Tielt", "Oudenaarde", "Brugge", "Gent"]
def block5():
    out = []
    for k in ("au-pair-alternatief", "vaste-huishoudhulp-ipv-au-pair", "hulp-ondernemersgezin-schoolkinderen"):
        out += [_dienst_page(k, c, i) for i, c in enumerate(B_CITIES_N)]
    return out
AU_VRAGEN = [
 ("au-pair-of-huishoudhulp-voor-ondernemers", "Au pair of huishoudhulp: wat past bij een ondernemersgezin?"),
 ("hulp-in-huis-zonder-au-pair", "Kan je hulp in huis hebben zonder een au pair in huis te nemen?"),
 ("wat-doet-een-au-pair-algemeen", "Wat doet een au pair doorgaans, en waar kijk je best naar de regels?"),
 ("vaste-hulp-voor-druk-ondernemersgezin", "Hoe organiseer je vaste hulp in huis als beide ouders ondernemen?"),
 ("wie-haalt-kinderen-van-school-ondernemer", "Wie haalt je kinderen van school als je zelf een zaak runt?"),
 ("hulp-in-huis-zonder-inwonende-persoon", "Hoe regel je hulp in huis zonder dat er iemand bij je inwoont?"),
 ("verschil-au-pair-en-vaste-huishoudhulp", "Wat is het verschil tussen een au pair en een vaste huishoudhulp?"),
 ("hulp-in-huis-als-je-veel-onderweg-bent", "Welke hulp in huis past als je veel onderweg bent voor je zaak?"),
 ("hulp-in-huis-tijdens-schoolvakanties", "Hoe regel je hulp in huis tijdens de schoolvakanties?"),
 ("privacy-gezin-en-huishoudhulp", "Hoe gaat een huishoudhulp om met de privacy van je gezin?"),
 ("vertrouwen-opbouwen-met-huishoudhulp", "Hoe bouw je vertrouwen op met iemand die bij je thuis komt?"),
 ("sleutel-en-toegang-huishoudhulp", "Hoe regel je de sleutel en de toegang voor je huishoudhulp?"),
 ("huishoudhulp-en-hond-uitlaten", "Kan je huishoudhulp ook je hond uitlaten?"),
 ("weekplanning-hulp-in-huis-ondernemersgezin", "Hoe maak je een weekplanning voor hulp in huis in een ondernemersgezin?"),
 ("hulp-in-huis-als-je-zaak-snel-groeit", "Hoeveel hulp in huis heb je nodig als je zaak snel groeit?"),
 ("wie-kookt-thuis-als-beide-ouders-ondernemen", "Wie kookt er thuis als beide ouders een zaak runnen?"),
 ("gezonde-schotels-voor-de-hele-week", "Kan je gezonde schotels voor de hele week laten klaarzetten?"),
 ("hulp-bij-kinderen-ophalen-via-vennootschap", "Kan de hulp bij het ophalen van je kinderen via je vennootschap lopen?"),
 ("taken-vaste-huishoudhulp-schoolkinderen", "Welke taken doet een vaste huishoudhulp in een gezin met schoolkinderen?"),
 ("juiste-dagen-kiezen-voor-hulp-in-huis", "Hoe kies je de juiste dagen voor hulp in huis?"),
 ("huishoudhulp-en-tuin-terras", "Kan je huishoudhulp ook de tuin en het terras bijhouden?"),
 ("huis-bijhouden-tijdens-vakantie", "Kan iemand je huis bijhouden terwijl je op vakantie bent?"),
 ("au-pair-of-opvang-na-school", "Au pair of opvang na school: wat past bij schoolgaande kinderen?"),
 ("vaste-persoon-of-wisselende-hulp-thuis", "Waarom kies je thuis liever voor één vaste persoon dan voor wisselende hulp?"),
]

# blok 6: kinderopvang voor grotere kinderen (12 steden x 4 + 30 vragen = 78)
def block6():
    out = []
    for k in ("kinderen-ophalen-school", "opvang-na-school", "opvang-woensdagnamiddag", "vieruurtje-en-avondeten"):
        out += [_dienst_page(k, c, i) for i, c in enumerate(B_CITIES_N)]
    return out
KIND_VRAGEN = [
 ("opvang-schoolgaande-kinderen-ondernemer", "Welke opvang bestaat er voor schoolgaande kinderen als je zelf ondernemer bent?"),
 ("wat-is-opvang-na-school-aan-huis", "Wat houdt opvang na school aan huis in?"),
 ("kan-iemand-anders-kinderen-van-school-halen", "Kan iemand anders je kinderen van school halen?"),
 ("afspraken-met-persoon-die-kinderen-ophaalt", "Welke afspraken maak je met de persoon die je kinderen van school haalt?"),
 ("vieruurtje-laten-klaarzetten", "Kan iemand het vieruurtje klaarzetten als de kinderen thuiskomen?"),
 ("wie-let-op-kinderen-na-school", "Wie let op de kinderen na school terwijl jij nog werkt?"),
 ("woensdagnamiddag-regelen-als-je-werkt", "Hoe regel je de woensdagnamiddag als je werkt?"),
 ("hebben-grotere-kinderen-nog-opvang-nodig", "Hebben grotere kinderen nog opvang na school nodig?"),
 ("kinderen-naar-training-laten-brengen", "Kan iemand je kinderen naar de training of academie brengen?"),
 ("vaste-persoon-voor-je-kinderen", "Waarom is een vaste persoon voor je kinderen beter dan wisselende opvang?"),
 ("kennismaking-kinderen-en-je-zondag", "Hoe verloopt de kennismaking tussen je kinderen en je Zondag?"),
 ("opvangpersoon-ziek-wat-nu", "Wat als de persoon die je kinderen opvangt ziek is?"),
 ("opvang-en-huishouden-combineren", "Kan één persoon de kinderen opvangen en het huishouden doen?"),
 ("thuisregels-uitleggen-aan-opvangpersoon", "Hoe leg je de thuisregels uit aan de persoon die je kinderen opvangt?"),
 ("opvang-overdag-in-schoolvakanties", "Kan je overdag opvang voor je kinderen regelen in de schoolvakanties?"),
 ("is-zondags-een-erkende-kinderopvang", "Is Zondags een erkende kinderopvang?"),
 ("opvang-aan-huis-of-buitenschoolse-opvang", "Wat is het verschil tussen opvang aan huis en buitenschoolse opvang?"),
 ("allergieen-en-voorkeuren-bij-koken-voor-kinderen", "Hoe ga je om met allergieën en voorkeuren als iemand voor je kinderen kookt?"),
 ("gezonde-maaltijd-voor-schoolkinderen-laat-thuis", "Hoe zorg je voor een gezonde maaltijd voor schoolkinderen als je laat thuiskomt?"),
 ("schermtijd-en-snacks-afspreken-met-opvang", "Hoe spreek je regels over schermtijd en snacks af met de opvangpersoon?"),
 ("kinderen-ophalen-via-je-vennootschap", "Kan je de hulp bij het ophalen van je kinderen via je vennootschap laten lopen?"),
 ("opvang-meerdere-kinderen-verschillende-uren", "Hoe organiseer je opvang voor meerdere schoolkinderen met verschillende uren?"),
 ("contact-houden-met-opvangpersoon", "Hoe houd je contact met de persoon die je kinderen opvangt?"),
 ("hoeveel-uur-opvang-na-school-nodig", "Waarvan hangt het af hoeveel uur opvang je na school nodig hebt?"),
 ("kinderen-ophalen-en-boodschappen-doen", "Kan de persoon die je kinderen ophaalt ook boodschappen doen?"),
 ("kinderen-ophalen-op-twee-scholen", "Kan iemand je kinderen van twee verschillende scholen ophalen?"),
 ("opvangpersoon-en-hond-uitlaten", "Kan de persoon die je kinderen opvangt ook de hond uitlaten?"),
 ("school-op-de-hoogte-brengen-ophaalpersoon", "Wat regel je met de school als iemand anders je kind ophaalt?"),
 ("opvang-en-hulp-bij-start-schooljaar", "Hoe regel je opvang en hulp bij de start van het schooljaar?"),
 ("vragen-aan-opvangpersoon-grotere-kinderen", "Welke vragen stel je aan een opvangpersoon voor je grotere kinderen?"),
]

# blok 7: vragen over kosten, fiscaliteit, contracten en vergelijken (55)
PRIJS_VRAGEN = [
 ("offertes-poetsfirmas-vergelijken", "Hoe vergelijk je offertes van poetsfirma's?"),
 ("uurprijs-of-vaste-prijs-poetsen", "Uurprijs of vaste prijs voor poetshulp: wat past bij je bedrijf?"),
 ("verborgen-kosten-poetsfirma", "Welke verborgen kosten kunnen er zijn bij een poetsfirma?"),
 ("minimum-uren-per-bezoek-poetshulp", "Waarom hanteren poetsfirma's een minimum aantal uren per bezoek?"),
 ("wat-staat-in-offerte-poetshulp-kantoor", "Wat moet er in een offerte voor poetshulp op kantoor staan?"),
 ("schoonmaakbedrijf-of-vaste-poetshulp", "Schoonmaakbedrijf of vaste poetshulp: wat is het verschil?"),
 ("ploeg-of-een-vaste-persoon-kantoor", "Een ploeg of één vaste persoon voor je kantoor?"),
 ("poetshulp-in-dienst-van-de-firma", "Wat betekent het voor jou als klant dat de poetshulp in dienst is van de firma?"),
 ("wat-staat-op-dienstenfactuur-poetshulp", "Wat staat er op een dienstenfactuur voor poetshulp?"),
 ("factuur-splitsen-beroepsmatig-en-prive", "Hoe wordt een factuur gesplitst tussen beroepsmatig en privé?"),
 ("btw-op-poetshulp-voor-bedrijven", "Btw op poetshulp: wat moet je als bedrijf weten?"),
 ("is-poetshulp-kantoor-bedrijfskost", "Is poetshulp voor je kantoor een bedrijfskost?"),
 ("voordeel-alle-aard-poetshulp-woning", "Wat is een voordeel van alle aard bij poetshulp voor je woning?"),
 ("wat-vraag-je-accountant-over-poetshulp", "Wat vraag je je accountant over poetshulp via je zaak?"),
 ("poetshulp-registreren-in-boekhouding", "Hoe registreer je poetshulp in je boekhouding?"),
 ("waarom-geen-dienstencheques-voor-vennootschap", "Waarom kan een vennootschap geen dienstencheques gebruiken?"),
 ("alternatief-dienstencheques-voor-bedrijven", "Wat is het alternatief voor dienstencheques voor een bedrijf?"),
 ("eigen-woning-laten-poetsen-via-de-zaak", "Mag een bedrijfsleider zijn eigen woning laten poetsen via de zaak?"),
 ("wat-staat-in-contract-poetshulp", "Wat staat er in een contract voor poetshulp?"),
 ("opzegtermijn-poetshulp-bedrijven", "Hoe werkt de opzegtermijn bij poetshulp voor bedrijven?"),
 ("kennismaking-voor-je-vastlegt", "Kan je poetshulp uitproberen voor je je vastlegt?"),
 ("wat-gebeurt-in-eerste-twee-gratis-uren", "Wat gebeurt er in de eerste twee gratis uren?"),
 ("intake-poetshulp-wat-bespreek-je", "Wat bespreek je bij de intake voor poetshulp?"),
 ("wat-is-een-zondagsplan", "Wat is een zondagsplan?"),
 ("uren-bijboeken-of-afbouwen-poetshulp", "Kan je uren bijboeken of afbouwen bij poetshulp?"),
 ("wanneer-losse-grote-poetsbeurt-boeken", "Wanneer boek je een losse grote poetsbeurt?"),
 ("poetshulp-als-kantoor-gesloten-is", "Wat doe je met poetshulp als je kantoor gesloten is?"),
 ("poetshulp-rond-feestdagen-en-brugdagen", "Hoe werkt poetshulp rond feestdagen en brugdagen?"),
 ("poetsproducten-afspreken-met-poetshulp", "Hoe spreek je af welke poetsproducten gebruikt worden?"),
 ("collega-allergisch-voor-poetsproducten", "Wat als een collega allergisch is voor bepaalde poetsproducten?"),
 ("sleutel-en-alarm-poetshulp-kantoor", "Hoe regel je sleutel en alarm voor de poetshulp van je kantoor?"),
 ("poetshulp-alleen-op-kantoor", "Wat als je poetshulp alleen op kantoor is?"),
 ("discretie-poetshulp-in-praktijk", "Hoe regel je discretie bij poetshulp in een praktijk?"),
 ("patientendossiers-en-poetshulp", "Wat met patiëntendossiers als er een poetshulp in de praktijk komt?"),
 ("poetshulp-tijdens-openingsuren", "Kan poetshulp tijdens de openingsuren van je zaak?"),
 ("waarom-poetsen-voor-de-opening", "Waarom poetsen veel zaken liefst voor de opening?"),
 ("hoe-vaak-sanitair-kantoor-poetsen", "Hoe vaak moet het sanitair op kantoor gepoetst worden?"),
 ("keuken-en-frigo-op-kantoor-hygienisch", "Hoe hou je de keuken en frigo op kantoor hygiënisch?"),
 ("vloeren-op-kantoor-onderhouden", "Hoe onderhoud je verschillende vloeren op kantoor?"),
 ("ramen-van-je-kantoor", "Wat doe je met de ramen van je kantoor?"),
 ("afvalsortering-op-kantoor", "Hoe organiseer je afvalsortering op kantoor?"),
 ("kantoor-ordelijk-tussen-twee-poetsbeurten", "Hoe hou je een klein kantoor ordelijk tussen twee poetsbeurten?"),
 ("afspraken-met-team-opgeruimd-kantoor", "Hoe maak je afspraken met je team over een opgeruimd kantoor?"),
 ("poetshulp-voor-starter-eerste-kantoor", "Welke poetshulp past bij een starter met een eerste kantoor?"),
 ("poetshulp-bij-groeiend-team", "Hoe groeit de poetshulp mee met een groeiend team?"),
 ("poetshulp-thuiskantoor-beroepsmatig-prive", "Poetshulp voor een thuiskantoor: wat is beroepsmatig en wat privé?"),
 ("poetshulp-gedeeld-kantoorgebouw", "Poetshulp in een gedeeld kantoorgebouw: wie regelt wat?"),
 ("wat-doet-poetshulp-in-winkel-voor-opening", "Wat doet poetshulp in een winkel voor de opening?"),
 ("etalage-langs-binnen-laten-doen", "Kan poetshulp ook de etalage langs binnen doen?"),
 ("welke-ruimtes-door-vaste-persoon-laten-onderhouden", "Welke ruimtes laat je het best door een vaste persoon onderhouden?"),
 ("niet-tevreden-over-de-schoonmaak", "Wat doe je als je niet tevreden bent over de schoonmaak?"),
 ("poetshulp-evalueren-na-eerste-maanden", "Hoe evalueer je je poetshulp na de eerste maanden?"),
 ("jaarplanning-onderhoud-kantoor", "Hoe maak je een jaarplanning voor het onderhoud van je kantoor?"),
 ("onnodige-kosten-schoonmaak-vermijden", "Hoe vermijd je dat schoonmaak op kantoor onnodig veel kost?"),
 ("poetshulp-voor-kantoor-in-kortrijk-wat-te-weten", "Poetshulp voor je kantoor in Kortrijk: wat moet je vooraf weten?"),
]
def block_vragen():
    return [dict(id=f'vragen/{s}', path=f'vragen/{s}.html', kind='vraag', group='vragen', h1=q) for s, q in AU_VRAGEN + KIND_VRAGEN + PRIJS_VRAGEN]

# blok 8: checklists en gidsen (30)
GIDSEN = [
 ("checklist-wekelijkse-kantoorpoets", "Checklist voor de wekelijkse poetsbeurt van je kantoor", "wat bij een wekelijkse poetsbeurt op kantoor aan de beurt komt, per ruimte"),
 ("checklist-wekelijkse-praktijkpoets", "Checklist voor de wekelijkse poetsbeurt van je praktijk", "wachtzaal, onthaal, consultatie- en behandelruimtes, sanitair; wat bij de praktijk blijft (instrumenten, medisch materiaal)"),
 ("checklist-winkel-poetsen-voor-opening", "Checklist: je winkel poetsen voor de opening", "vloer, paskamers, toonbank, etalage langs binnen, stock, sanitair, in welke volgorde en hoe lang vooraf"),
 ("checklist-eerste-dag-nieuwe-poetshulp", "Checklist voor de eerste dag van je nieuwe poetshulp", "toegang, sleutel en alarm, rondleiding, wat staat waar, wat niet aangeraakt mag worden, contactpersoon"),
 ("gids-poetshulp-kiezen-voor-je-bedrijf", "Gids: zo kies je poetshulp voor je bedrijf", "criteria om poetshulp te vergelijken: vaste persoon, in dienst, factuur, flexibiliteit, planning, communicatie"),
 ("gids-zondagsplan-opstellen", "Gids: zo stel je een zondagsplan op", "van taken en frequentie tot dag en uur: een plan op één pagina met afspraken tussen jou en je Zondag"),
 ("checklist-intakegesprek-poetshulp", "Checklist voor het intakegesprek met je poetshulp", "wat je voorbereidt en doorneemt bij de intake ter plaatse"),
 ("gids-kantoor-en-woning-in-een-plan", "Gids: kantoor en woning in één plan", "hoe je beroepsmatig en privé in één plan zet, de factuursplitsing en wat je accountant moet bevestigen"),
 ("checklist-vergaderzaal-klaarzetten", "Checklist: een vergaderzaal klaarzetten voor de volgende vergadering", "tafel, stoelen, schermen, glazen wand, water en koffie, afval, geur en verluchting"),
 ("checklist-sanitair-op-kantoor-wekelijks", "Checklist voor het sanitair op kantoor", "toiletten, lavabo's, spiegels, aanvullen, vloeren, afval"),
 ("checklist-refter-en-keuken-op-kantoor", "Checklist voor de refter en keuken op kantoor", "frigo, koffiemachine, microgolf, tafels, vaatwasser, afval en geur"),
 ("checklist-frisse-wachtzaal", "Checklist voor een frisse wachtzaal", "zitjes, tafeltjes, tijdschriften, speelhoek, vloer, ramen langs binnen, geur, ingangsmat"),
 ("gids-eerste-grote-poetsbeurt-nieuw-kantoor", "Gids: een eerste grote poetsbeurt voor een nieuw kantoor", "plannen, voorbereiden en uitvoeren van de eerste beurt voor je intrekt, daarna overgaan op een vast ritme"),
 ("checklist-grote-poetsbeurt-praktijk", "Checklist voor de grote poetsbeurt van je praktijk", "kasten, plinten, behandelruimtes, wachtzaal, archief stofvrij, als losse opdracht"),
 ("gids-hulp-in-huis-voor-ondernemers-in-vijf-stappen", "Gids: hulp in huis voor ondernemers in vijf stappen", "van behoefte bepalen tot de eerste vaste dag: aanvraag, telefoon, intake, plan, start"),
 ("checklist-weekmenu-en-boodschappenlijst", "Checklist: weekmenu en boodschappenlijst voor drukke ondernemers", "weekmenu opstellen, voorraad nakijken, boodschappenlijst doorgeven, allergieën en voorkeuren"),
 ("gids-gezonde-schotels-voor-de-week", "Gids: gezonde schotels voor de week laten klaarzetten", "hoe een Zondag schotels voor meerdere dagen kookt, bewaart en etiketteert, afspraken over smaak en allergieën"),
 ("checklist-kinderen-van-school-laten-ophalen", "Checklist: iemand anders je kinderen van school laten ophalen", "afspraken met school, kinderen en ophaalpersoon, wat je doorgeeft, hoe je op de hoogte blijft"),
 ("gids-opvang-na-school-thuis-organiseren", "Gids: opvang na school bij jou thuis organiseren", "dagritme, vieruurtje, regels, communicatie, wat Zondags wel en niet doet"),
 ("checklist-start-schooljaar-ondernemersgezin", "Checklist voor de start van het schooljaar in een ondernemersgezin", "weekritme, ophaalmomenten, vaste dagen voor hulp in huis, planning van de eerste weken"),
 ("gids-alternatieven-voor-een-au-pair", "Gids: alternatieven voor een au pair", "wat een au pair is, welke alternatieven er zijn voor een ondernemersgezin en waar ze verschillen; Zondags als vaste hulp overdag zonder inwoning"),
 ("gids-vaste-hulp-vinden-in-kortrijk", "Gids: vaste hulp vinden in Kortrijk en omgeving", "waar je op let bij hulp in huis in Kortrijk, de deelgemeenten en de buurgemeenten, en hoe Zondags start"),
 ("checklist-kantoor-voor-het-bouwverlof", "Checklist: je kantoor klaarmaken voor het bouwverlof", "afsluiten, opruimen, frigo leegmaken, afval, grondige poetsbeurt, planten, herstart"),
 ("checklist-praktijk-proper-het-nieuwe-jaar-in", "Checklist: je praktijk proper het nieuwe jaar in", "jaarafsluiting van de praktijk: archief, kasten, grondige poetsbeurt, frisse start"),
 ("gids-administratie-poetshulp-via-vennootschap", "Gids: de administratie van poetshulp via je vennootschap", "offerte, contract, dienstenfactuur, betalingen en wat je bewaart voor je accountant"),
 ("gids-vragen-voor-je-accountant-over-hulp-in-huis", "Gids: vragen voor je accountant over hulp in huis via je zaak", "een lijst vragen om met je accountant door te nemen, zonder zelf adviseren"),
 ("checklist-kantoor-ordelijk-tussen-twee-beurten", "Checklist: je kantoor ordelijk houden tussen twee poetsbeurten", "kleine gewoontes van het team die de poetsbeurt makkelijker maken"),
 ("gids-poetshulp-voor-een-klein-team", "Gids: poetshulp voor een klein team", "hoe je poetshulp inricht voor een klein team: frequentie, momenten, verdeling van taken tussen team en Zondag"),
 ("checklist-huis-laten-bijhouden-tijdens-vakantie", "Checklist: je huis laten bijhouden tijdens je vakantie", "post, planten, ramen openen, vuilnis, lichten, huisdieren; wat je Zondag wel en niet doet"),
 ("gids-hulp-voor-ondernemers-in-kortrijk-per-dienst", "Gids: hulp voor ondernemers in Kortrijk, per dienst", "overzicht van schoonmaak, kookhulp, boodschappen, hulp in huis, kinderen ophalen en opvang na school in Kortrijk en de deelgemeenten"),
]
def block8():
    return [dict(id=f'sectoren/{s}', path=f'sectoren/{s}.html', kind='gids', group='sectoren', h1=h1, scope=scope) for s, h1, scope in GIDSEN]

def block_nieuw():
    return block1() + block2() + block3() + block4() + block5() + block6() + block_vragen() + block8()

def plan():
    pages = city_pages() + region_pages() + service_city_pages() + sector_pages() + question_pages() + candidate_pages() + block_nieuw()
    return pages

if __name__ == '__main__':
    P = plan()
    ids = [p['id'] for p in P]
    assert len(ids) == len(set(ids)), 'dubbele id'
    os.makedirs('_tools/content', exist_ok=True)
    json.dump(P, open('_tools/content/plan.json', 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(P), Counter(p['kind'] for p in P))
