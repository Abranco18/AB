# -*- coding: utf-8 -*-
"""Uebersetzt die 50 noch spanischen Produkte aus dem Gesamtkatalog (ES -> DE), Preise +5 EUR.

Enthaelt vier Gruppen:
  * 27 Reisetaschen  -> gleiche Vorlage wie reisetaschen_export_DE.csv
  *  1 Wäschekorb    -> gleiche Vorlage wie products_export_DE.csv
  *  1 Tischläufer   -> gleiche Vorlage wie tischlaeufer_export_DE.csv
  * 21 Lampen        -> je einzeln uebersetzt (20x Tag LAMPS + TIFFALIGHT)
Eingebettete <img>-Tags werden unveraendert in Reihenfolge uebernommen.
"""
import csv
import decimal
import re
import sys

SRC, DST = sys.argv[1], sys.argv[2]

PRICE_INCREASE = decimal.Decimal("5.00")
PRICE_COLUMNS = ("Variant Price", "Variant Compare At Price")

# --------------------------------------------------------------------------
# Gruppe 1: Reisetaschen (identisch zur bereits gelieferten Kollektion)
# --------------------------------------------------------------------------
BAG_SUFFIX_ES = "-bolsa-de-viaje-suave-hecha-a-mano"
BAG_SUFFIX_DE = "-handgefertigte-weiche-reisetasche"
BAG_TITLE_DE = " | Handgefertigte weiche Reisetasche"
BAG_TYPE_DE = "Reisetasche"

BAG_SIZES_DE = {
    "Paisaje 18 in L x 9 in W x 9 in H (46x23x23 cm)":
        "Querformat 18 in L × 9 in B × 9 in H (46 × 23 × 23 cm)",
    "Paisaje 19.09 in L x 9.06 in W x 9.06 in H (48.5x23x23 cm)":
        "Querformat 19,09 in L × 9,06 in B × 9,06 in H (48,5 × 23 × 23 cm)",
    "Pequeña Paisaje 15.94 in L x 8.07 in W x 8.07 in H (40.5x20.5x20.5 cm)":
        "Klein – Querformat 15,94 in L × 8,07 in B × 8,07 in H (40,5 × 20,5 × 20,5 cm)",
    "Pequeño Paisaje 15.94 in L x 8.07 in W x 8.07 in H (40.5x20.5x20.5 cm)":
        "Klein – Querformat 15,94 in L × 8,07 in B × 8,07 in H (40,5 × 20,5 × 20,5 cm)",
    "Grande Paisaje 19.09 in L x 9.06 in W x 9.06 in H (48.5x23x23 cm)":
        "Groß – Querformat 19,09 in L × 9,06 in B × 9,06 in H (48,5 × 23 × 23 cm)",
}

BAG_BODY_TRAVEL = "\n".join([
    '<h3>MÜHELOSER STIL FÜR DEINE NÄCHSTE AUSZEIT.</h3>',
    '<p>Verlasse das Haus mit allem ordentlich verstaut und griffbereit für deine Kurzreise. '
    'Diese geräumige Reisetasche verleiht deinem Reise-Look eine weiche, bezaubernde Note und '
    'hält deine Essentials für die Übernachtung perfekt organisiert.</p>',
    '<p>{IMG1}</p>',
    '<p><strong>✔ CLEVERE UND ORGANISIERTE AUFBEWAHRUNG</strong></p>',
    '<p>Mehrere Fächer und ein sicherer Reißverschluss halten alles, was du unterwegs brauchst, '
    'zuverlässig an seinem Platz. So genießt du dein Wochenende, ohne nach Schlüssel, Handy oder '
    'Reiseunterlagen suchen zu müssen.</p>',
    '<p><strong>✔ WEICHES, GESTEPPTES DESIGN</strong></p>',
    '<p>Die elegante Steppnaht gibt der Tasche eine weiche, stilvolle Textur. Sie ist leicht und '
    'bequem zu tragen – zum Auto oder ins Ferienhaus – und setzt ein einzigartiges, edles Detail '
    'in deiner Reisegarderobe.</p>',
    '<p><strong>✔ GEMACHT FÜR WOCHENENDTRIPS</strong></p>',
    '<p>Die robuste, zweilagige Verarbeitung gibt dir zusätzliche Widerstandsfähigkeit auf Reisen. '
    'Ob es zum Kurzurlaub ans Meer geht oder für ein paar Tage zur Familie – deine Sachen bleiben '
    'schön und sicher verstaut.</p>',
    '<p><strong>✔ PFLEGELEICHTER KOMFORT</strong></p>',
    '<p>Das maschinenwaschbare Design macht die Reinigung nach der Reise einfach und stressfrei. '
    'So bleibt deine Reisetasche frisch und bereit für dein nächstes Abenteuer – ganz ohne '
    'zusätzlichen Aufwand.</p>',
    '<p><strong>Mach dich bereit für deine nächste Auszeit – mit einer Tasche, die dich auf '
    'jedem Kilometer begleitet.</strong></p>',
])

BAG_BODY_DAILY = "\n".join([
    '<h3>ALLTAGSSTIL, DER ALLES MITNIMMT.</h3>',
    '<p>Du gehst aus dem Haus mit allem, was du brauchst – ordentlich verstaut und griffbereit. '
    'Diese Tasche verleiht deinem Look eine weiche, bezaubernde Note und lässt deinen Tag '
    'organisierter wirken.</p>',
    '<p>{IMG1}</p>',
    '<p><strong>✔ CLEVERE UND ORGANISIERTE AUFBEWAHRUNG</strong></p>',
    '<p>Mehrere Fächer und ein sicherer Reißverschluss halten deine Essentials zuverlässig an '
    'ihrem Platz. So kommst du durch den Tag, ohne nach Schlüssel, Handy oder Geldbörse '
    'suchen zu müssen.</p>',
    '<p><strong>✔ WEICHES, GESTEPPTES DESIGN</strong></p>',
    '<p>Die elegante Wellen-Steppnaht gibt der Tasche eine weiche, stilvolle Textur. Sie ist '
    'leicht und bequem zu tragen und setzt ein einzigartiges Detail in deinem Outfit.</p>',
    '<p><strong>✔ GEMACHT FÜR DEN ALLTAG</strong></p>',
    '<p>Die zweilagige Verarbeitung gibt dir zusätzliche Widerstandsfähigkeit für den täglichen '
    'Gebrauch. Ob auf dem Markt oder beim Treffen mit Freunden – sie bleibt schön.</p>',
    '<p><strong>✔ PFLEGELEICHTER KOMFORT</strong></p>',
    '<p>Das maschinenwaschbare Design macht die Reinigung einfach und stressfrei. So bleibt deine '
    'Tasche frisch – ganz ohne zusätzlichen Aufwand.</p>',
    '<p><strong>Starte in deinen Tag mit einer Tasche, die sich jedem Moment anpasst.</strong></p>',
])

# --------------------------------------------------------------------------
# Gruppe 2: Wäschekorb (identisch zur bereits gelieferten Kollektion)
# --------------------------------------------------------------------------
CLS = 'class="font-claude-response-body break-words whitespace-normal leading-[1.7]"'

BASKET_BODY_DE = "\n".join([
    f'<p {CLS}><strong>Suchst du einen Wäschekorb, der schön und praktisch zugleich ist?</strong></p>',
    f'<p {CLS}>Dieser gesteppte Wäschekorb bringt einen warmen, gemütlichen Akzent in deinen Alltag. '
    'Ob du das Schlafzimmer aufräumst oder das Badezimmer ordentlich hältst – dieser Korb macht alles mit, '
    'mit Charme und eingebautem Komfort.</p>',
    f'<p {CLS}><strong>PRODUKTDETAILS</strong></p>',
    '<p><strong>Hochwertiges Material:</strong> Gefertigt aus einer hochwertigen Baumwoll-Polyester-Mischung '
    'mit robusten Canvas-Griffen. Weich und dennoch formstabil – unempfindlich gegen Verschüttetes '
    'und für den täglichen Gebrauch gemacht.</p>',
    '<p><strong>Freistehende Konstruktion:</strong> Behält seine Form und steht auch im leeren Zustand '
    'von allein aufrecht.</p>',
    '<p><strong>Verfügbare Größen:</strong></p>',
    '<p><strong>Klein</strong> (14" x 18" | ca. 36 x 46 cm) Perfekt für Badezimmer oder Kinderzimmer</p>',
    '<p><strong>Mittel</strong> (16" x 22" | ca. 41 x 56 cm) Ideal für Schlafzimmer oder Waschküche</p>',
    '<p><strong>Groß</strong> (20" x 28" | ca. 51 x 71 cm) Ideal für die Wäsche der ganzen Familie '
    'oder zur Aufbewahrung von Bettwäsche</p>',
    '<p><strong>Pflegeleicht:</strong> Lässt sich einfach abwischen und bei Bedarf in der Maschine waschen. '
    'Leicht und faltbar für eine platzsparende Aufbewahrung.</p>',
    f'<p {CLS}>Alle Produkte werden mit Liebe auf Bestellung gefertigt. Bitte beachte: Leichte Abweichungen '
    'in Farbe, Muster und Maßen (1–3" bzw. ca. 2,5–7,5 cm) sind aufgrund der handgefertigten Herstellung möglich.</p>',
])

BASKET_SIZES_DE = {"Pequeña": "Klein", "Pequeño": "Klein", "Mediana": "Mittel",
                   "Mediano": "Mittel", "Grande": "Groß"}

# Option2 "Diseño": gleiche Uebersetzungslogik wie in products_export_DE.csv
BASKET_DESIGNS_DE = {
    "Cesta de Ropa Acolchada Encanto de las Tierras Altas":
        "Gesteppter Wäschekorb Zauber der Highlands",
    "Cesta de Ropa Acolchada Ternera Acogedora":
        "Gesteppter Wäschekorb Gemütliches Kälbchen",
    "Cesta de Ropa Acolchada Floral de las Tierras Altas":
        "Gesteppter Wäschekorb Highland-Blumen",
    "Cesta de Ropa Acolchada Bloom de las Tierras Altas":
        "Gesteppter Wäschekorb Highland-Blüte",
    "Cesta de Ropa Acolchada Atardecer de las Tierras Altas":
        "Gesteppter Wäschekorb Highland-Abendrot",
}

# --------------------------------------------------------------------------
# Gruppe 3: Tischläufer (identisch zur bereits gelieferten Kollektion)
# --------------------------------------------------------------------------
RUNNER_BODY_DE = "\n".join([
    '<p>Entdecke den Charme unseres gesteppten Tischläufers – gestaltet, um deinem Essbereich '
    'einen Hauch von Eleganz und Behaglichkeit zu verleihen!<br></p>',
    '<p><strong>PRODUKTDETAILS:</strong></p>',
    '<ul>',
    '<li>',
    '<strong>Hochwertiges Material:</strong> Unsere Tischläufer werden aus einer hochwertigen '
    'Baumwoll-Polyester-Mischung von Jetiy gefertigt und verbinden die Weichheit und '
    'Atmungsaktivität der Baumwolle mit der Langlebigkeit und Pflegeleichtigkeit des Polyesters.<br>',
    '</li>',
    '<li>',
    '<strong>Verschiedene Größen:</strong> Damit für jeden Anlass das Passende dabei ist, gibt es '
    'unseren Tischläufer in drei praktischen Größen:<br>',
    '</li>',
    '</ul>',
    '<p><strong>S: 36 cm × 122 cm </strong>- Perfekt für kleine Runden.'
    '<br><strong>M: 36 cm × 183 cm</strong> - Ideal für Tische in Standardgröße.'
    '<br><strong>L: 36 cm × 275 cm </strong>- Passend für festliche Bankette und lange Tafeln.<br></p>',
    '<ul>',
    '<li>',
    '<strong>Vielfältige Designs: </strong>Entdecke unsere große Auswahl an bezaubernden Designs – '
    'jedes einzelne gestaltet, um die Atmosphäre bei Tisch mit seinem ganz eigenen Charme zu bereichern.<br>',
    '</li>',
    '<li>',
    '<strong>Pflegeleicht: </strong>Das Leben ist schon kompliziert genug! Deshalb ist unser '
    'Tischläufer maschinenwaschbar und trocknergeeignet – das vereinfacht deine Reinigungsroutine.<br>',
    '</li>',
    '</ul>',
    '<p>Alle Produkte werden auf Bestellung gefertigt und nach den besten verfügbaren Standards '
    'bedruckt. Werte deine Tischdekoration mit unserem bezaubernden gesteppten Tischläufer auf – '
    'dort, wo Stil auf Praktikabilität trifft!<br></p>',
    '<p><strong>Hinweis: </strong>Da jedes unserer Produkte auf Bestellung gefertigt wird, kann es '
    'im Vergleich zu den Beispielfotos zu Abweichungen von etwa 20 % bei Farbe, Muster, Verarbeitung '
    'und Nähten kommen. Wir garantieren jedoch, dass das Hauptdesign wie abgebildet erhalten bleibt.<br></p>',
])

RUNNER_SIZES_DE = {
    "S (36 cm x 122 cm)": "S (36 cm × 122 cm)",
    "M (36 cm × 183 cm)": "M (36 cm × 183 cm)",
    "L (36 cm × 275 cm)": "L (36 cm × 275 cm)",
}

# --------------------------------------------------------------------------
# Gruppe 4: Lampen – je einzeln uebersetzt
# --------------------------------------------------------------------------
def lamp_body(headline, intro, why, bullets, specs, imgs=2):
    parts = ["<h2><strong>%s</strong></h2>" % headline,
             "<p>%s</p>" % intro,
             "<p>{IMG1}</p>",
             "<h2><strong>%s</strong></h2>" % why]
    parts += ["<p>✔ <strong>%s</strong>: %s</p>" % (k, v) for k, v in bullets]
    if imgs == 2:
        parts.append("<p>{IMG2}</p>")
    parts.append("<h2><strong>Spezifikationen</strong></h2>")
    parts.append("<ul>")
    parts += ["<li><strong>%s:</strong> %s</li>" % (k, v) for k, v in specs]
    parts.append("</ul>")
    return "\n".join(parts)


LAMPS = {
    "tiffalight-lampara-de-mariposa-de-vitral": (
        "tiffalight-buntglaslampe-mit-schmetterling",
        "TIFFALIGHT | Buntglaslampe mit Schmetterling",
        lamp_body(
            "Faszinierendes Leuchten, das Kunst und Licht vereint",
            "Verwandle jedes Zimmer mit einer faszinierenden Lampe, die künstlerischen Charme und "
            "warmes Licht verbindet. Dieses wunderschön gestaltete Stück bereichert dein Interieur "
            "mit lebendigen Farben und sanfter Beleuchtung und schafft eine behagliche, einladende "
            "Atmosphäre – ideal für Schlafzimmer, Wohnzimmer oder das eigene Büro.",
            "Warum du die TIFFALIGHT Buntglaslampe mit Schmetterling lieben wirst",
            [("Künstlerisch brillant", "Ein beeindruckendes Schmetterlingsdesign, das Farbe, "
              "Eleganz und Persönlichkeit in jedes Zimmer bringt."),
             ("Warmes, einladendes Leuchten", "Gibt ein beruhigendes Licht ab, das sofort eine "
              "ruhige und romantische Atmosphäre schafft."),
             ("Beeindruckende Dekoration", "Funktioniert als Lampe und zugleich als dekorativer "
              "Blickfang, der mühelos Aufmerksamkeit auf sich zieht."),
             ("Stimmungsvolles Licht", "Die sanfte Beleuchtung hilft, Stress abzubauen, und "
              "fördert eine ruhige Atmosphäre."),
             ("Die perfekte Geschenkwahl", "Ein durchdachtes und faszinierendes Geschenk für alle, "
              "die einzigartige und schöne Dekoration lieben.")],
            [("Typ", "Dekorative Lampe"), ("Design", "Schmetterlingsmotiv"),
             ("Stil", "Buntglas"), ("Beleuchtung", "Sanftes Leuchten"),
             ("Verwendung", "Innendekoration")],
            imgs=1)),

    "solelia-lampara-de-vidrio-vintage-con-girasol": (
        "solelia-vintage-glaslampe-mit-sonnenblume",
        "SOLELIA | Vintage-Glaslampe mit Sonnenblume",
        lamp_body(
            "Suchst du eine Lampe, die deine Seele erhellt?",
            "Bring Wärme, Farbe und Magie in dein Zuhause – mit der Vintage-Lampe Solelia mit "
            "Sonnenblume. Ihr leuchtendes, von der Sonnenblume inspiriertes Glasdesign sorgt für "
            "ein behagliches, fröhliches Licht und verwandelt jedes Zimmer in einen gemütlichen "
            "Rückzugsort. Ideal für Schlafzimmer, Cafés oder Leseecken – sie bringt zeitlose "
            "Eleganz in dein Interieur.",
            "Warum du dich in die Vintage-Lampe Solelia mit Sonnenblume verlieben wirst",
            [("Warmes, strahlendes Licht", "Gibt ein sanftes, goldenes Licht ab, das die "
              "Behaglichkeit jeder romantischen Umgebung unterstreicht."),
             ("Magisches Design", "Das Glas mit Sonnenblumenmotiv setzt einen künstlerischen "
              "Akzent und bringt Vintage-Schönheit in deinen Wohnraum."),
             ("Vielseitig platzierbar", "Ideal für Schlafzimmer, Wohnzimmer oder dekorative Ecken, "
              "die sanftes Licht brauchen."),
             ("Langlebige Verarbeitung", "Mit stabilem Sockel und hochwertigem Glas gefertigt – "
              "für dauerhafte Qualität und Standfestigkeit."),
             ("Positives Ambiente", "Schafft eine positive, einladende Stimmung – ideal zum "
              "Entspannen oder für gute Gespräche.")],
            [("Material", "Hochwertige Glasmischung"), ("Typ", "Akzent-Tischlampe"),
             ("Stil", "Florales Vintage-Design"), ("Beleuchtung", "Warmes gelbes Licht")])),

    "azuria-lampara-de-vidrio-azul-lujoso": (
        "azuria-luxus-glaslampe-in-blau",
        "AZURIA | Luxus-Glaslampe in Blau",
        lamp_body(
            "Möchtest du einen Hauch Luxus und Ruhe hinzufügen?",
            "Erhelle dein Zuhause mit der stillen Schönheit der Azuria Luxus-Glaslampe in Blau. "
            "Ihr beeindruckendes blaues Glasdesign fängt das Licht auf bezaubernde Weise ein und "
            "erzeugt ein entspannendes, edles Leuchten. Ideal für Schlafzimmer, Wohnzimmer oder "
            "Büros – Azuria verbindet Kunst mit moderner Eleganz und wertet jeden Raum auf.",
            "Warum du die Azuria Luxus-Glaslampe in Blau lieben wirst",
            [("Elegantes blaues Leuchten", "Bringt eine ruhige, luxuriöse Note in deine "
              "Wohndekoration."),
             ("Künstlerisches Design", "Der wunderschön gearbeitete Glassockel reflektiert das "
              "Licht mit feiner Raffinesse."),
             ("Passt überall", "Ergänzt moderne wie klassische Einrichtungsstile mühelos."),
             ("Langlebige Qualität", "Aus hochwertigen Materialien gefertigt – für dauerhaften "
              "Glanz und Widerstandsfähigkeit."),
             ("Entspannende Stimmung", "Schafft eine beruhigende, einladende Atmosphäre, ideal "
              "zum Entspannen.")],
            [("Material", "Hochwertige Glasmischung"), ("Typ", "Dekorative Akzentlampe"),
             ("Stil", "Moderner Luxus"), ("Lichtfarbe", "Sanftes blaues Leuchten")])),

    "solina-lampara-de-mesa-led-fascinante": (
        "solina-faszinierende-led-tischlampe",
        "SOLINA | Faszinierende LED-Tischlampe",
        lamp_body(
            "Bereit, deinen Wohnraum schön zu erhellen?",
            "Erhelle deine Umgebung mit dem eleganten Charme der faszinierenden LED-Tischlampe "
            "Solina. Ihr modernes, bezauberndes Design verschönert jedes Zimmer – vom Büro bis zum "
            "Nachttisch. Mit sanftem LED-Licht und künstlerischer Verarbeitung verbindet Solina "
            "Praktisches mit ästhetischem Leuchten und macht alltägliche Momente behaglich und "
            "stilvoll.",
            "Warum du die faszinierende LED-Tischlampe Solina lieben wirst",
            [("Elegantes Ambiente", "Bringt Wärme und Raffinesse in dein Büro, deine Leseecke "
              "oder dein Schlafzimmer."),
             ("Sanftes LED-Licht", "Ein weiches, augenfreundliches Licht – ideal zum Entspannen "
              "oder Konzentrieren."),
             ("Kompakt &amp; funktional", "Die perfekte Größe für Schreibtische, Beistelltische "
              "oder dekorative Arrangements."),
             ("Solides Design", "Aus hochwertigen Materialien gefertigt – für Langlebigkeit und "
              "dauerhaften Gebrauch."),
             ("Universeller Stil", "Fügt sich mühelos in moderne, klassische und minimalistische "
              "Interieurs ein.")],
            [("Material", "Hochwertiges Glas und Metallmischung"), ("Typ", "LED-Tischlampe"),
             ("Stil", "Moderne Eleganz"), ("Lichtfarbe", "Sanftes warmes Licht")])),

    "petalyn-lampara-de-mesa-inspirada-en-el-barroco": (
        "petalyn-barock-inspirierte-tischlampe",
        "PETALYN | Barock-inspirierte Tischlampe",
        lamp_body(
            "Bereit für einen Hauch königlichen Glanz?",
            "Erhelle deinen Wohnraum mit zeitloser Eleganz und Charme. Die barock-inspirierte "
            "Tischlampe Petalyn fängt das Wesen des klassischen Luxus ein und bietet kunstvolle "
            "Designdetails, die Kunst mit moderner Raffinesse verbinden. Ideal für Schlafzimmer, "
            "Wohnzimmer oder Leseecken – sie verwandelt jedes Zimmer in einen warmen, eleganten "
            "Rückzugsort.",
            "Warum du die barock-inspirierte Tischlampe Petalyn lieben wirst",
            [("Elegantes Barockdesign", "Von zeitloser europäischer Kunst inspiriert – bringt eine "
              "edle, königliche Atmosphäre in dein Zuhause."),
             ("Warmes Umgebungslicht", "Gibt ein dezentes, beruhigendes Leuchten ab – ideal zum "
              "Entspannen oder für Abende in Gesellschaft."),
             ("Universelles Dekoelement", "Ergänzt klassische wie moderne Interieurs mühelos."),
             ("Robuste Handwerkskunst", "Aus hochwertigen Materialien gefertigt – für dauerhafte "
              "Schönheit und zuverlässige Leistung."),
             ("Perfekte Geschenkwahl", "Ein beeindruckendes Geschenk für alle, die Kunst, Stil "
              "und Raffinesse schätzen.")],
            [("Material", "Hochwertige Glas- und Metallmischung"), ("Typ", "Tischlampe"),
             ("Stil", "Barocke Eleganz"), ("Beleuchtung", "Warmes Leuchten")])),

    "lumora-lampara-vintage-con-brillo-oceanico": (
        "lumora-vintage-lampe-mit-ozean-leuchten",
        "LUMORA | Vintage-Lampe mit Ozean-Leuchten",
        lamp_body(
            "Wünschst du dir einen Hauch ozeanischer Gelassenheit?",
            "Bring ein beruhigendes Leuchten in dein Zuhause – mit der Vintage-Lampe LUMORA mit "
            "Ozean-Leuchten, wo Vintage-Charme auf entspannendes Licht trifft. Inspiriert von den "
            "Farbtönen des Ozeans und zeitloser Handwerkskunst, verwandelt diese elegante Lampe "
            "jeden Raum in einen ruhigen Rückzugsort. Ihr sanftes Umgebungslicht und das "
            "künstlerische Glasdesign machen sie ideal für gemütliche Abende oder stilvolle "
            "Interieurs.",
            "Warum du die Vintage-Lampe LUMORA mit Ozean-Leuchten lieben wirst",
            [("Vom Ozean inspirierte Eleganz", "Fängt das beruhigende Wesen des Meeres in jedem "
              "leuchtenden Detail wunderschön ein."),
             ("Warmes Umgebungslicht", "Schafft eine entspannende Atmosphäre – ideal für "
              "Schlafzimmer, Wohnzimmer oder Leseecken."),
             ("Außergewöhnliche Handwerkskunst", "Sorgfältig aus hochwertigen Materialien "
              "gestaltet – für einen edlen Vintage-Look."),
             ("Vielseitig einsetzbar", "Ideal für Nachttische, Schreibtische oder dekorative "
              "Tische."),
             ("Langlebiges Design", "Gemacht, um zu bleiben – behält Glanz und beeindruckende "
              "Textur über die Zeit.")],
            [("Material", "Hochwertiges Glas und Metallmischung"), ("Typ", "Vintage-Akzentlampe"),
             ("Stil", "Vom Ozean inspirierte Eleganz"), ("Lichtfarbe", "Warmes Umgebungslicht")])),

    "florina-lampara-decorativa-de-vidrio-coloreado": (
        "florina-dekorative-buntglaslampe",
        "FLORINA | Dekorative Buntglaslampe",
        lamp_body(
            "Möchtest du dein Zuhause mit Kunst beleben?",
            "Belebe deinen Wohnraum mit der leuchtenden Magie der dekorativen Buntglaslampe "
            "Florina. Sie verbindet künstlerische Schönheit mit sanftem Licht und verwandelt jede "
            "Ecke in einen warmen, einladenden Rückzugsort. Ihre lebendigen Glasblütenblätter "
            "fangen das Licht wunderschön ein und schaffen eine bezaubernde Atmosphäre, die zum "
            "Entspannen und Genießen einlädt.",
            "Warum du die dekorative Buntglaslampe Florina lieben wirst",
            [("Bezauberndes Design", "Die handgefertigten Glasblütenblätter erblühen in Farbe und "
              "bringen Eleganz und Persönlichkeit in deine Dekoration."),
             ("Sanftes, behagliches Licht", "Bietet ein weiches, beruhigendes Leuchten – ideal für "
              "Abende oder ruhige Momente."),
             ("Fesselndes Dekostück", "Wird mit seinem floral-künstlerischen Look sofort zum "
              "Mittelpunkt jedes Zimmers."),
             ("Langlebige Verarbeitung", "Aus hochwertigen Materialien gefertigt – für dauerhaften "
              "Charme und täglichen Gebrauch."),
             ("Perfekte Geschenkidee", "Ein durchdachtes Geschenk für alle, die Kunst, Schönheit "
              "und stimmungsvolles Licht lieben.")],
            [("Material", "Hochwertige Glasmischung"), ("Typ", "Dekorative Akzentlampe"),
             ("Stil", "Künstlerisches florales Design"),
             ("Lichtfarbe", "Warmes, strahlendes Leuchten")])),

    "chromia-lampara-de-mesa-clasica-colorida": (
        "chromia-klassische-bunte-tischlampe",
        "CHROMIA | Klassische bunte Tischlampe",
        lamp_body(
            "Suchst du eine Lampe, die Freude schenkt?",
            "Erhelle deinen Wohnraum mit dem leuchtenden Charme der klassischen bunten Tischlampe "
            "Chromia. Ihr lebendiges Glasmosaik-Design verwandelt jedes Zimmer in einen warmen, "
            "einladenden Rückzugsort. Ideal für Schlafzimmer, Wohnzimmer oder Cafés – diese Lampe "
            "bringt Farbe, Eleganz und Persönlichkeit in deine Einrichtung, bei Tag und bei Nacht.",
            "Warum du die klassische bunte Tischlampe Chromia lieben wirst",
            [("Lebendiges Mosaikdesign", "Die handgefertigten Muster bringen Leben, Wärme und eine "
              "künstlerische Note in deinen Wohnraum."),
             ("Sanftes Umgebungslicht", "Schafft eine entspannende Atmosphäre – ideal für "
              "gemütliche Abende oder ruhige Momente mit einem Buch."),
             ("Vielseitiges Dekostück", "Ideal für Schlafzimmer, Büros oder als elegantes Element "
              "in jeder Ecke."),
             ("Langlebige Verarbeitung", "Aus soliden Materialien gefertigt – für dauerhafte "
              "Qualität und zuverlässige Leistung."),
             ("Sofortiger Stimmungsaufheller", "Setzt einen fröhlichen, farbenfrohen Akzent, der "
              "jeden Einrichtungsstil bereichert.")],
            [("Material", "Robuste Glasmischung"), ("Typ", "Tischlampe"),
             ("Stil", "Buntes Mosaikdesign"), ("Beleuchtung", "Warmes Umgebungslicht")])),

    "rosavia-lampara-estilo-tiffany-colorida": (
        "rosavia-bunte-lampe-im-tiffany-stil",
        "ROSAVIA | Bunte Lampe im Tiffany-Stil",
        lamp_body(
            "Bereit, deinen Wohnraum mit Kunst zu erhellen?",
            "Bring Farbe, Wärme und zeitlose Eleganz in dein Zuhause – mit der bunten Lampe Rosavia "
            "im Tiffany-Stil. Gestaltet, um jedes Zimmer zu verzaubern, gibt ihr handgefertigter "
            "Glasschirm ein feines, einladendes Licht ab und verwandelt gewöhnliche Räume in "
            "künstlerische, behagliche Rückzugsorte. Ideal für Schlafzimmer, Leseecken oder "
            "Wohnzimmer, die ein besonderes Stück verdienen.",
            "Warum du die bunte Lampe Rosavia im Tiffany-Stil lieben wirst",
            [("Lebendiges Licht", "Wirft satte, farbenfrohe Lichtmuster, die Wärme und Charme in "
              "deinen Wohnraum bringen."),
             ("Handarbeit", "Von Hand präzise zusammengesetzt – für ein einzigartiges, "
              "hochwertiges Finish."),
             ("Universelle Eleganz", "Ideal für Nachttische, Schreibtische oder als "
              "beeindruckendes Herzstück im Wohnzimmer."),
             ("Zeitloses Design", "Von der klassischen Tiffany-Kunst inspiriert – verbindet "
              "Tradition mit moderner Raffinesse."),
             ("Langlebig und zuverlässig", "Aus soliden, hochwertigen Materialien gefertigt – für "
              "dauerhafte Schönheit und Leistung.")],
            [("Material", "Glasmischung mit Buntglas"), ("Typ", "Akzent-Tischlampe"),
             ("Stil", "Klassisches Tiffany-Design"),
             ("Lichtfarbe", "Warmes mehrfarbiges Licht")])),

    "leafora-lampara-de-vidrio-retro-en-forma-de-hoja": (
        "leafora-retro-glaslampe-in-blattform",
        "LEAFORA | Retro-Glaslampe in Blattform",
        lamp_body(
            "Bereit, natürliches Leuchten ins Haus zu holen?",
            "Bring einen Hauch Vintage-Eleganz und organische Schönheit in dein Zuhause – mit der "
            "Retro-Glaslampe Leafora in Blattform. Mit filigranen Glasblättern und einem warmen, "
            "angenehmen Licht verwandelt sie jeden Raum in einen gemütlichen Rückzugsort. Ideal für "
            "Nachttische, Leseecken oder als Akzent im Wohnzimmer.",
            "Warum du die Retro-Glaslampe Leafora in Blattform lieben wirst",
            [("Von der Natur inspiriertes Design", "Die eleganten Glasblätter fangen das Licht "
              "wunderschön ein und bringen natürlichen Charme in deine Dekoration."),
             ("Warmes Umgebungslicht", "Das sanfte Licht schafft eine ruhige, entspannende "
              "Atmosphäre in jedem Zimmer."),
             ("Passt überall", "Ideal für Schlafzimmer, Büros, Cafés oder jeden Raum, der einen "
              "gemütlichen Akzent braucht."),
             ("Hochwertiges Finish", "Aus langlebigen Materialien gefertigt – für Qualität und "
              "Standfestigkeit über lange Zeit."),
             ("Ein Hingucker", "Wertet deinen Wohnraum sofort mit zeitloser Retro-Raffinesse "
              "auf.")],
            [("Material", "Hochwertige Glas- und Harzmischung"), ("Typ", "Akzentlampe"),
             ("Stil", "Retro-Design in Blattform"), ("Beleuchtung", "Warmes Licht")])),

    "vintara-lampara-de-ventana-dorada-brillante": (
        "vintara-goldene-fensterlampe",
        "VINTARA | Goldene Fensterlampe",
        lamp_body(
            "Bereit, jeden Abend in einen goldenen Moment zu verwandeln?",
            "Bring Wärme und Raffinesse in dein Zuhause – mit der strahlend goldenen Fensterlampe "
            "Vintara. Sie taucht deinen Wohnraum in sanftes goldenes Licht; ihre elegante "
            "Verarbeitung und das vom Vintage inspirierte Design schaffen eine entspannende "
            "Atmosphäre. Ideal für Schlafzimmer, Wohnzimmer oder Leseecken – sie verwandelt "
            "gewöhnliche Räume in behagliche Rückzugsorte.",
            "Warum du die strahlend goldene Fensterlampe Vintara lieben wirst",
            [("Goldenes Umgebungslicht", "Gibt ein warmes, beruhigendes Licht ab, das die "
              "Atmosphäre jedes Zimmers verbessert."),
             ("Elegantes Design", "Die schönen Glasdetails bringen zeitlosen Charme und optischen "
              "Reiz in deine Dekoration."),
             ("Passt überall", "Ideal für Fensterbänke, Nachttische oder gemütliche "
              "Entspannungsecken."),
             ("Langlebige Verarbeitung", "Aus hochwertigen Materialien gefertigt – für "
              "Standfestigkeit und dauerhafte Eleganz."),
             ("Beruhigendes Licht", "Schafft eine ruhige Stimmung – ideal, um nach einem langen "
              "Tag abzuschalten.")],
            [("Material", "Hochwertiges Glas und Metallmischung"), ("Typ", "Fenster-Akzentlampe"),
             ("Stil", "Vintage-Eleganz"), ("Lichtfarbe", "Goldenes Leuchten")])),

    "blushen-lampara-glow-clasica-con-flores": (
        "blushen-klassische-blumenlampe",
        "BLUSHEN | Klassische Blumenlampe",
        lamp_body(
            "Möchtest du einen Hauch zeitlosen Charme hinzufügen?",
            "Bring Wärme und Schönheit in dein Zuhause – mit der klassischen Blumenlampe Blushen. "
            "Ihr elegantes florales Glasdesign strahlt Raffinesse aus, während das sanfte Licht "
            "eine beruhigende Atmosphäre schafft. Perfekt für Schlafzimmer, Wohnzimmer oder "
            "gemütliche Ecken – sie verwandelt jeden Raum in einen Ort aus zartem Licht und "
            "feinem Stil.",
            "Warum du die klassische Blumenlampe Blushen lieben wirst",
            [("Elegantes florales Design", "Bringt zeitlosen Charme und Raffinesse in deine "
              "Dekoration."),
             ("Warmes, beruhigendes Licht", "Schafft eine entspannende, angenehme Atmosphäre in "
              "jedem Zimmer."),
             ("Passt überall", "Perfekt für Schlafzimmer, Cafés oder Beistelltische."),
             ("Langlebige Verarbeitung", "Aus hochwertigen Materialien gefertigt – für Eleganz "
              "und dauerhafte Leistung."),
             ("Attraktives Dekoelement", "Wertet deinen Wohnraum auf und ergänzt moderne wie "
              "klassische Interieurs.")],
            [("Material", "Hochwertige Glas- und Metallmischung"), ("Typ", "Akzentlampe"),
             ("Stil", "Florale Eleganz"), ("Lichtfarbe", "Warmes Umgebungslicht")])),

    "tulisse-lampara-de-vidrio-vitrajado-hecha-a-mano": (
        "tulisse-handgefertigte-buntglaslampe",
        "TULISSE | Handgefertigte Buntglaslampe",
        lamp_body(
            "Möchtest du deinen Wohnraum mit Kunst erhellen?",
            "Bring zeitlose Schönheit und eine warme Atmosphäre in dein Zuhause – mit der "
            "handgefertigten Buntglaslampe Tulisse. Jedes Stück wird fein gearbeitet und vereint "
            "Farbe, Textur und Licht zu einem beeindruckenden Kunstwerk. Ob im Schlafzimmer, im "
            "Café oder in der Leseecke – Tulisse verwandelt jeden Raum in einen behaglichen, "
            "eleganten Rückzugsort.",
            "Warum du die handgefertigte Buntglaslampe Tulisse lieben wirst",
            [("Handgefertigte Schönheit", "Jede Lampe entsteht einzeln, mit Sorgfalt und Blick "
              "für künstlerische Details."),
             ("Warmes Umgebungslicht", "Erzeugt ein sanftes, beruhigendes Licht – ideal zum "
              "Entspannen oder für intime Räume."),
             ("Eleganter Dekoakzent", "Bringt Charme und Raffinesse in jeden Einrichtungsstil."),
             ("Langlebiges Design", "Aus hochwertigem Glas und soliden Materialien gefertigt – "
              "für dauerhafte Anziehungskraft."),
             ("Passt überall", "Ideal für Nachttische, Tische, Cafés oder gemütliche Ecken.")],
            [("Material", "Handgefertigte Glasmischung"), ("Typ", "Buntglaslampe"),
             ("Stil", "Künstlerisch &amp; elegant"),
             ("Lichtfarbe", "Warme, sanfte Beleuchtung")])),

    "aurelia-lampara-de-vidrio-del-mundo-antiguo": (
        "aurelia-glaslampe-im-alte-welt-stil",
        "AURELIA | Glaslampe im Alte-Welt-Stil",
        lamp_body(
            "Bereit, zeitlose Eleganz nach Hause zu holen?",
            "Tauche deinen Wohnraum in das warme, nostalgische Licht der Glaslampe Aurelia im "
            "Alte-Welt-Stil. Von klassischer Handwerkskunst inspiriert, besticht sie durch "
            "kunstvolle Glasarbeit und einen wunderschön modellierten Sockel voller "
            "Vintage-Charme. Ideal für Schlafzimmer, Wohnzimmer oder gemütliche Ecken – Aurelia "
            "macht jeden Moment zu einem fein beleuchteten Erlebnis.",
            "Warum du die Glaslampe Aurelia im Alte-Welt-Stil lieben wirst",
            [("Zeitlose Handwerkskunst", "Mit außergewöhnlicher künstlerischer Glasarbeit "
              "gestaltet, inspiriert vom traditionellen europäischen Design."),
             ("Warmes Umgebungslicht", "Erzeugt ein wohltuendes, angenehmes Licht – ideal für "
              "entspannte Abende."),
             ("Vielseitiges Dekoelement", "Passt zu klassischen Interieurs ebenso wie zu modernen "
              "Räumen mit Alte-Welt-Charme."),
             ("Langlebige Verarbeitung", "Aus hochwertigen Materialien gefertigt – für "
              "Standfestigkeit, Langlebigkeit und Eleganz."),
             ("Perfekte Geschenkidee", "Ein bedeutungsvolles, elegantes Geschenk zur Einweihung, "
              "zur Hochzeit oder zum Jahrestag.")],
            [("Material", "Hochwertige Glas- und Metallmischung"), ("Typ", "Akzent-Tischlampe"),
             ("Stil", "Alte-Welt-Eleganz"), ("Beleuchtung", "Warmes Umgebungslicht")])),

    "ivorya-lampara-de-mesa-barroca-luxuosa": (
        "ivorya-luxus-tischlampe-im-barockstil",
        "IVORYA | Luxus-Tischlampe im Barockstil",
        lamp_body(
            "Möchtest du einen Hauch zeitlosen Luxus hinzufügen?",
            "Schaffe eine Atmosphäre der Raffinesse – mit der luxuriösen Barock-Tischlampe Ivorya. "
            "Ihre ornamentalen Details und ihr eleganter Glanz fangen die Schönheit des klassischen "
            "Designs ein und machen sie zum Mittelpunkt jedes Zimmers. Ideal für Schlafzimmer, "
            "Wohnzimmer oder elegante Ecken – Ivorya verbindet Kunst mit warmem Licht.",
            "Warum du die luxuriöse Barock-Tischlampe Ivorya lieben wirst",
            [("Elegantes Licht", "Gibt ein sanftes goldenes Leuchten ab, das eine entspannte und "
              "edle Atmosphäre schafft."),
             ("Barock-inspiriertes Design", "Die kunstvolle Verarbeitung bringt Luxus und "
              "Raffinesse in deine Inneneinrichtung."),
             ("Vielseitig platzierbar", "Ideal für Nachttische, Eingangsbereiche oder Akzentflächen, "
              "die einen Hauch Glamour vertragen."),
             ("Langlebige Verarbeitung", "Aus hochwertigen Materialien gefertigt – für dauerhaften "
              "Stil und tägliche Zuverlässigkeit."),
             ("Außergewöhnliches Stück", "Wertet deinen Wohnraum sofort mit königlichem Charme und "
              "zeitloser Magie auf.")],
            [("Material", "Hochwertige Glas- und Harzmischung"), ("Typ", "Barock-Tischlampe"),
             ("Stil", "Klassischer Luxus"), ("Lichtfarbe", "Warmes Umgebungslicht")])),

    "florencia-lampara-de-vidrio-templado-colorido": (
        "florencia-lampe-aus-buntem-hartglas",
        "FLORENCIA | Lampe aus buntem Hartglas",
        lamp_body(
            "Möchtest du Farbe und Wärme in deinen Wohnraum bringen?",
            "Erfülle dein Zuhause mit Leben und Licht – mit der Lampe Florencia aus buntem "
            "Hartglas. Ihr beeindruckendes Mosaikdesign und das warme Licht schaffen eine "
            "behagliche, künstlerische Atmosphäre, die jedes Zimmer sofort aufwertet. Ideal für "
            "Schlafzimmer, Cafés oder Leseecken – sie bringt Stil und Eleganz an jeden Ort.",
            "Warum du die Lampe Florencia lieben wirst",
            [("Lebendiges Licht", "Schenkt ein warmes, farbenfrohes Licht, das deinen Wohnraum mit "
              "Stil und Persönlichkeit erhellt."),
             ("Hochwertige Handwerkskunst", "Jedes Stück besteht aus sorgfältig gestaltetem "
              "Buntglas – für einen wirklich einzigartigen Look."),
             ("Vielseitig einsetzbar", "Ideal für Nachttische, Wohnzimmer, Büros oder gemütliche "
              "Leseecken."),
             ("Elegantes Design", "Verbindet zeitlose Kunst mit moderner Eleganz und ergänzt jedes "
              "Interieur."),
             ("Auf Langlebigkeit gebaut", "Aus widerstandsfähigen Materialien gefertigt – für "
              "Schönheit und Leistung über lange Zeit.")],
            [("Material", "Hochwertige Glasmischung"), ("Typ", "Dekorative Akzentlampe"),
             ("Stil", "Buntes Mosaik in eleganter Ausführung"),
             ("Lichtfarbe", "Warmes mehrfarbiges Leuchten")])),

    "tiffelle-lampara-elegante-en-forma-de-libelula": (
        "tiffelle-elegante-lampe-in-libellenform",
        "TIFFELLE | Elegante Lampe in Libellenform",
        lamp_body(
            "Möchtest du deinem Wohnraum einen Hauch Magie geben?",
            "Bring zeitlose Kunst und ein zartes Leuchten in dein Zuhause – mit der eleganten Lampe "
            "Tiffelle in Libellenform. Ihr handwerklich gefertigtes Design aus farbigem Glas, "
            "inspiriert von den feinen Flügeln einer Libelle, gibt ein warmes, bezauberndes Licht "
            "ab. Ideal für Schlafzimmer, Wohnzimmer oder Leseecken – sie verwandelt jede Ecke in "
            "ein Bild von Eleganz und Ruhe.",
            "Warum du die elegante Lampe Tiffelle in Libellenform lieben wirst",
            [("Bezauberndes Design", "Mit einem beeindruckenden Libellenmotiv, das Raffinesse und "
              "Charme ausstrahlt."),
             ("Warmes Umgebungslicht", "Erzeugt ein behagliches, einladendes Licht – ideal zum "
              "Entspannen oder für ruhige Abende."),
             ("Vielseitiger Dekoakzent", "Bereichert jeden Ort – vom Nachttisch bis zum "
              "Schreibtisch."),
             ("Erstklassige Handwerkskunst", "Aus hochwertigem Glas mit solidem Sockel gefertigt – "
              "für lange Haltbarkeit."),
             ("Perfekte Geschenkwahl", "Ein durchdachtes Stück für Kunstliebhaber und alle, die "
              "edle Dekoration schätzen.")],
            [("Material", "Hochwertige Buntglasmischung"), ("Typ", "Schreibtischlampe"),
             ("Stil", "Libelle im Jugendstil"), ("Lichtfarbe", "Zartes warmes Leuchten")])),

    "blueris-lampara-clasica-con-sombrero-en-forma-de-petalo": (
        "blueris-klassische-lampe-mit-bluetenblatt-schirm",
        "BLUERIS | Klassische Lampe mit Blütenblatt-Schirm",
        lamp_body(
            "Möchtest du deinem Wohnraum Eleganz verleihen?",
            "Bring zeitlosen Charme und Wärme in dein Zuhause – mit der Lampe Blueris mit "
            "klassischem Blütenblatt-Schirm. Ihr feines, von Blütenblättern inspiriertes Design "
            "und das sanfte Umgebungslicht schaffen eine angenehme Atmosphäre, die jedes Zimmer "
            "aufwertet. Ideal für Schlafzimmer, Cafés oder gemütliche Ecken – sie bringt Schönheit "
            "und Raffinesse in deinen Alltag.",
            "Warum du die Lampe Blueris mit klassischem Blütenblatt-Schirm lieben wirst",
            [("Elegantes Blütenblatt-Design", "Der von der Natur inspirierte Schirm bringt "
              "künstlerische Schönheit in deine Dekoration."),
             ("Sanftes Umgebungslicht", "Gibt ein warmes, beruhigendes Licht ab – ideal zum "
              "Entspannen oder für stimmungsvolle Abende."),
             ("Passt überall", "Ideal für Nachttische, Wohnzimmer oder als Akzent im Mittelpunkt."),
             ("Erstklassige Verarbeitung", "Aus robusten, hochwertigen Materialien gefertigt – für "
              "dauerhafte Eleganz."),
             ("Sofortiger Stimmungsaufheller", "Verwandelt gewöhnliche Räume mühelos in "
              "gemütliche, angenehme Rückzugsorte.")],
            [("Material", "Hochwertige Glasmischung"), ("Typ", "Akzent-Tischlampe"),
             ("Stil", "Von Blüten inspirierte Eleganz"),
             ("Lichtfarbe", "Warmes, sanftes Licht")])),

    "mosaicra-lampara-elegante-con-iluminacion-glow": (
        "mosaicra-elegante-mosaiklampe",
        "MOSAICRA | Elegante Mosaiklampe",
        lamp_body(
            "Möchtest du einen Hauch zeitlosen Luxus hinzufügen?",
            "Bring Raffinesse in deinen Wohnraum – mit der eleganten Mosaiklampe Mosaicra. Ihre "
            "dekorativen Details und ihr feines Leuchten fangen die Schönheit klassischen Designs "
            "ein und machen sie zum Mittelpunkt jedes Zimmers. Ideal für Schlafzimmer, Wohnzimmer "
            "oder elegante Ecken – Mosaicra verbindet Kunst mit warmem Licht.",
            "Warum du die elegante Mosaiklampe Mosaicra lieben wirst",
            [("Elegantes Licht", "Erzeugt ein zartes, goldenes Leuchten für eine entspannte und "
              "edle Atmosphäre."),
             ("Kunstvolles Mosaikdesign", "Die aufwendige Handwerkskunst bringt Luxus und "
              "Raffinesse in deine Wohndekoration."),
             ("Passt überall", "Ideal für Nachttische, Eingangsbereiche oder Akzentflächen, die "
              "einen Hauch Glamour vertragen."),
             ("Langlebige Verarbeitung", "Aus hochwertigen Materialien gefertigt – für dauerhaften "
              "Stil und tägliche Zuverlässigkeit."),
             ("Außergewöhnliches Stück", "Wertet deinen Wohnraum sofort mit königlichem, zeitlosem "
              "Charme auf.")],
            [("Material", "Hochwertige Glas- und Harzmischung"), ("Typ", "Mosaik-Tischlampe"),
             ("Stil", "Klassischer Luxus"), ("Lichtfarbe", "Warmes Umgebungsleuchten")])),

    "glasora-lampara-clasica-de-vitrales": (
        "glasora-klassische-buntglaslampe",
        "GLASORA | Klassische Buntglaslampe",
        lamp_body(
            "Möchtest du deinen Wohnraum mit Kunst beleben?",
            "Belebe dein Zuhause mit Farbe und Wärme – durch die klassische Buntglaslampe Glasora. "
            "Mit kunstvollen Glasmustern und zeitlosem Design strahlt diese Lampe in jedem "
            "Lichtstrahl Eleganz aus. Ob im Schlafzimmer, im Wohnzimmer oder in der Leseecke – sie "
            "bringt einen edlen Charme, der gewöhnliche Räume in ruhige Rückzugsorte verwandelt.",
            "Warum du die klassische Buntglaslampe Glasora lieben wirst",
            [("Elegantes Ambiente", "Schafft eine warme, einladende Stimmung – ideal zum Entspannen "
              "oder für ruhige Abende."),
             ("Künstlerisches Design", "Die detaillierten Buntglasmuster bringen Raffinesse und "
              "Farbe in jedes Zimmer."),
             ("Überall platzierbar", "Ideal für Nachttische, Wohnzimmer oder dekorative Ecken."),
             ("Langlebige Verarbeitung", "Aus hochwertigen Materialien gefertigt – für "
              "Haltbarkeit und langanhaltenden Charme."),
             ("Sofortiger Stimmungsaufheller", "Das sanfte Licht steigert die Behaglichkeit und "
              "bereichert die Ästhetik deines Zuhauses.")],
            [("Material", "Hochwertige Buntglasmischung"), ("Typ", "Akzent-Schreibtischlampe"),
             ("Stil", "Klassisches künstlerisches Design"),
             ("Lichtfarbe", "Warmes Umgebungslicht")])),

    "aurelia-lampara-de-mesa-vintage-barroca": (
        "aurelia-vintage-tischlampe-im-barockstil",
        "AURELIA | Vintage-Tischlampe im Barockstil",
        lamp_body(
            "Bereit, zeitlose Eleganz in dein Zuhause zu holen?",
            "Bring einen Hauch Vintage-Raffinesse in jedes Zimmer – mit der Vintage-Tischlampe "
            "Aurelia im Barockstil. Inspiriert von der klassischen Barockkunst, schaffen ihre "
            "kunstvollen Details und das warme Licht eine luxuriöse Atmosphäre. Ideal für "
            "Schlafzimmer, Wohnzimmer oder Leseecken – Aurelia verwandelt gewöhnliche Räume in "
            "einen eleganten Rückzugsort.",
            "Warum du die Vintage-Tischlampe Aurelia im Barockstil lieben wirst",
            [("Eleganter Vintage-Charme", "Fängt die Schönheit des klassischen Barockdesigns ein – "
              "für ein luxuriöses, zeitloses Gefühl."),
             ("Warmes, einladendes Licht", "Gibt ein sanftes Licht ab, das in jedem Raum eine "
              "behagliche, entspannende Atmosphäre schafft."),
             ("Künstlerische Handwerkskunst", "Detaillierte Muster und modellierte Oberflächen "
              "machen sie zu einem wirklich außergewöhnlichen Stück."),
             ("Universeller Dekoakzent", "Fügt sich mühelos in traditionelle wie moderne "
              "Interieurs ein."),
             ("Langlebige Verarbeitung", "Aus hochwertigen Materialien gefertigt – für dauerhafte "
              "Eleganz und Zuverlässigkeit.")],
            [("Material", "Hochwertige Glas- und Harzmischung"), ("Typ", "Tischlampe"),
             ("Stil", "Vintage-Barock"), ("Lichtfarbe", "Warmes Umgebungslicht")])),
}

IMG_TAG = re.compile(r"<img[^>]*>")
DATA_ATTR = re.compile(r'\s+data-[\w-]+="[^"]*"')


def clean_img(tag):
    return DATA_ATTR.sub("", tag)


def bump_price(value):
    return "%.2f" % (decimal.Decimal(value) + PRICE_INCREASE) if value.strip() else value


def fill(template, body_html):
    imgs = [clean_img(t) for t in IMG_TAG.findall(body_html)]
    expected = len(set(re.findall(r"\{IMG\d\}", template)))
    if len(imgs) != expected:
        raise ValueError("%d <img> in der Quelle, %d im Template" % (len(imgs), expected))
    for i, tag in enumerate(imgs, 1):
        template = template.replace("{IMG%d}" % i, tag)
    return template


def main():
    with open(SRC, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames, rows = reader.fieldnames, list(reader)

    # Gruppe je Handle bestimmen (nur aus der Produktzeile, gilt dann fuer alle Zeilen)
    group = {}
    for row in rows:
        if row["Title"].strip():
            h = row["Handle"]
            if h in LAMPS:
                group[h] = "lamp"
            elif h.endswith(BAG_SUFFIX_ES):
                group[h] = "bag"
            elif row["Tags"] == "Mantelería":
                group[h] = "runner"
            else:
                group[h] = "basket"

    counts = {"lamp": 0, "bag": 0, "runner": 0, "basket": 0}
    for row in rows:
        h = row["Handle"]
        g = group[h]
        is_product = bool(row["Title"].strip())
        if is_product:
            counts[g] += 1

        if g == "lamp":
            new_handle, title, body = LAMPS[h]
            if is_product:
                row["Title"] = title
                row["Body (HTML)"] = fill(body, row["Body (HTML)"])
                if row["Type"] == "Handmade Butterfly Lamps":
                    row["Type"] = "Handgefertigte Schmetterlingslampen"
            row["Handle"] = new_handle

        elif g == "bag":
            name_slug = h[:-len(BAG_SUFFIX_ES)]
            if is_product:
                name = row["Title"].split("|")[0].strip()
                row["Title"] = name + BAG_TITLE_DE
                tpl = BAG_BODY_DAILY if "ESTILO DIARIO" in row["Body (HTML)"] else BAG_BODY_TRAVEL
                row["Body (HTML)"] = fill(tpl, row["Body (HTML)"])
                row["Type"] = BAG_TYPE_DE
            row["Handle"] = name_slug + BAG_SUFFIX_DE
            if row["Option1 Value"].strip():
                row["Option1 Value"] = BAG_SIZES_DE[row["Option1 Value"]]

        elif g == "runner":
            if is_product:
                row["Title"] = "Gesteppter Tischläufer - Leuchtende Menora"
                row["Body (HTML)"] = RUNNER_BODY_DE
                row["Tags"] = "Tischwäsche"
            row["Handle"] = "gesteppter-tischlaeufer-leuchtende-menora"
            if row["Option1 Value"].strip():
                row["Option1 Value"] = RUNNER_SIZES_DE[row["Option1 Value"]]

        else:  # basket
            if is_product:
                row["Title"] = "Zauber der Highlands | Handgefertigter Wäschekorb"
                row["Body (HTML)"] = BASKET_BODY_DE
                row["Type"] = "Gesteppter Wäschekorb"
            row["Handle"] = "zauber-der-highlands-handgefertigter-waeschekorb"
            if row["Option1 Value"].strip():
                row["Option1 Value"] = BASKET_SIZES_DE[row["Option1 Value"]]
            if row["Option2 Value"].strip():
                row["Option2 Value"] = BASKET_DESIGNS_DE[row["Option2 Value"]]

        if row["Option1 Name"].strip() == "Tamaño":
            row["Option1 Name"] = "Größe"
        if row["Option2 Name"].strip() == "Diseño":
            row["Option2 Name"] = "Design"
        for col in PRICE_COLUMNS:
            row[col] = bump_price(row[col])

    with open(DST, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Zeilen: %d | Produkte: %d  (Lampen %d, Taschen %d, Tischläufer %d, Wäschekorb %d)"
          % (len(rows), sum(counts.values()), counts["lamp"], counts["bag"],
             counts["runner"], counts["basket"]))


if __name__ == "__main__":
    main()
