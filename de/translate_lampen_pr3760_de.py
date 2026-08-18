# -*- coding: utf-8 -*-
"""Uebersetzt den Schmetterlingslampen-Export (ES -> DE), Preise +5 EUR.

Jede Beschreibung ist einzeln uebersetzt. Die eingebetteten <img>-Tags werden
unveraendert aus der Quelle uebernommen (Platzhalter {IMG1}, {IMG2} ...),
damit keine URL per Hand abgeschrieben wird.
"""
import csv
import decimal
import re
import sys

SRC, DST = sys.argv[1], sys.argv[2]

PRICE_INCREASE = decimal.Decimal("5.00")
PRICE_COLUMNS = ("Variant Price", "Variant Compare At Price")
TYPE_DE = {"Handmade Butterfly Lamps": "Handgefertigte Schmetterlingslampen"}

SPECS = "\n".join(["<h2><strong>Spezifikationen</strong></h2>", "<ul>", "{SPECS}", "</ul>"])


def body(headline, intro, why_title, bullets, specs, second_img=False):
    parts = ["<h2><strong>%s</strong></h2>" % headline,
             "<p>%s</p>" % intro,
             "<p>{IMG1}</p>",
             "<h2><strong>%s</strong></h2>" % why_title]
    parts += ["<p>✔ <strong>%s</strong> %s</p>" % (k, v) for k, v in bullets]
    if second_img:
        parts.append("<p>{IMG2}</p>")
    parts.append("<h2><strong>Spezifikationen</strong></h2>")
    parts.append("<ul>")
    parts += ["<li><strong>%s</strong> %s</li>" % (k, v) for k, v in specs]
    parts.append("</ul>")
    return "\n".join(parts)


PRODUCTS = {
    "vitafly-lampara-de-iluminacion-con-alas-de-mosaico": dict(
        handle="vitafly-leuchte-mit-mosaikfluegeln",
        title="VITAFLY | Leuchte mit Mosaikflügeln",
        body=body(
            "Verleihe jedem Raum einen Hauch bunter Magie",
            "Erhelle dein Zimmer mit einem faszinierenden Leuchten, das künstlerische Schönheit "
            "und sanftes Licht vereint. Diese bezaubernde Lampe verbindet lebendige Mosaikfarben "
            "mit einem von Flügeln inspirierten Charme und schafft eine warme, einladende "
            "Atmosphäre – ideal für Schlafzimmer, Wohnzimmer und gemütliche Ecken, in denen "
            "Kreativität und Behaglichkeit erstrahlen sollen.",
            "Warum du die VitaFly Leuchte mit Mosaikflügeln lieben wirst",
            [("Lebendiges Licht:", "Erzeugt ein lebendiges, farbenfrohes Leuchten, das die "
              "Atmosphäre deines Zimmers sofort aufwertet."),
             ("Künstlerisches Design:", "Das Mosaikmuster der Flügel setzt ein einzigartiges "
              "dekoratives Element, das jeden Einrichtungsstil bereichert."),
             ("Stimmungsvolles Licht:", "Das sanfte Leuchten lädt zum Entspannen ein und bringt "
              "ein fröhliches, aufmunterndes Gefühl in dein Zuhause."),
             ("Das perfekte Akzentstück:", "Kompakt und dennoch ausdrucksstark – ideal für "
              "Nachttische, Schreibtische oder Regale."),
             ("Geschenkfertig:", "Ein bezauberndes, durchdachtes Geschenk für alle, die kreative "
              "und künstlerische Dekoration lieben.")],
            [("Typ:", "Dekorative Lampe"), ("Design:", "Mosaikflügel"),
             ("Stil:", "Buntes Leuchten"), ("Beleuchtung:", "Sanftes Leuchten"),
             ("Verwendung:", "Innendekoration")])),

    "lumifly-lampara-con-motivo-de-mariposa-en-estilo-art-deco": dict(
        handle="lumifly-schmetterlingslampe-im-art-deco-stil",
        title="LUMIFLY | Schmetterlingslampe im Art-déco-Stil",
        body=body(
            "Betörendes Leuchten, inspiriert von Kunst und Natur",
            "Werte deinen Wohnraum mit einer Lampe auf, die künstlerischen Charme und sanftes "
            "Licht verbindet. Dieses von Schmetterlingen inspirierte Design erzeugt ein warmes, "
            "faszinierendes Leuchten, das jeden Raum in eine Oase der Ruhe verwandelt. Ideal für "
            "Schlafzimmer, Wohnzimmer oder gemütliche Ecken – sie verbessert die Atmosphäre und "
            "setzt zugleich ein elegantes dekoratives Element.",
            "Warum du die Lumifly Schmetterlingslampe im Art-déco-Stil lieben wirst",
            [("Art-déco-Schönheit:", "Bringt zeitlosen Charme mit eleganter, von Schmetterlingen "
              "inspirierter Kunst, die jede Einrichtung bereichert."),
             ("Warmes Umgebungslicht:", "Das sanfte Licht schafft eine entspannende Atmosphäre – "
              "ideal für ruhige Momente und erholsame Abende."),
             ("Kompakt und vielseitig:", "Passt perfekt auf Tische, Nachttische oder Regale und "
              "bringt Schönheit, ohne viel Platz zu beanspruchen."),
             ("Stimmungsvolles Licht:", "Das sanfte Leuchten schafft ein behagliches Ambiente zum "
              "Lesen, Entspannen oder Ausruhen."),
             ("Einzigartiges Geschenk:", "Eine schöne Wahl für alle, die künstlerische Beleuchtung "
              "und bedeutungsvolle Dekostücke schätzen.")],
            [("Typ:", "Dekorative Lampe"), ("Design:", "Schmetterlingsmotiv"),
             ("Stil:", "Art déco"), ("Beleuchtung:", "Sanftes Leuchten"),
             ("Verwendung:", "Innendekoration")])),

    "colorfly-lampara-de-escritorio-colorida-con-motivo-de-mariposa": dict(
        handle="colorfly-bunte-schreibtischlampe-mit-schmetterlingsmotiv",
        title="COLORFLY | Bunte Schreibtischlampe mit Schmetterlingsmotiv",
        body=body(
            "Verleihe jedem Raum einen Hauch bunter Magie",
            "Erhelle dein Zimmer mit einer lebendigen, faszinierenden Schreibtischlampe, die für "
            "eine warme und einladende Atmosphäre sorgt. Ihr künstlerisches Design mit "
            "Schmetterlingen und das sanfte Licht machen sie ideal für Schlafzimmer, Wohnzimmer "
            "oder Büros – gewöhnliche Ecken verwandeln sich im Handumdrehen in wunderschön "
            "beleuchtete, bezaubernde Orte.",
            "Warum du die ColorFly Schreibtischlampe mit bunten Schmetterlingen lieben wirst",
            [("Lebendiger Lichteffekt:", "Schafft eine farbenfrohe Atmosphäre, die jedem Zimmer "
              "Leben, Wärme und Persönlichkeit schenkt."),
             ("Bezauberndes Design:", "Die künstlerischen Schmetterlingsdetails wirken verspielt "
              "und zugleich elegant und werten deine Einrichtung auf."),
             ("Stimmungsvolles Licht:", "Die sanfte Beleuchtung hebt die Stimmung und macht deinen "
              "Wohnraum behaglich."),
             ("Kompakt &amp; vielseitig:", "Passt perfekt auf Tische, Nachttische oder Regale und "
              "lässt sich überall leicht aufstellen."),
             ("Ideal als Geschenk:", "Eine großartige Wahl zu Geburtstagen, Einweihungsfeiern oder "
              "für alle, die außergewöhnliche Dekoration lieben.")],
            [("Typ:", "Schreibtischlampe"), ("Design:", "Schmetterlingsmotiv"),
             ("Stil:", "Buntes Licht"), ("Beleuchtung:", "Sanftes Leuchten"),
             ("Verwendung:", "Innendekoration")])),

    "butterglow-lampara-de-vidrio-hecha-a-mano-con-mariposa": dict(
        handle="butterglow-handgefertigte-glaslampe-mit-schmetterling",
        title="BUTTERGLOW | Handgefertigte Glaslampe mit Schmetterling",
        body=body(
            "Ein bezauberndes Leuchten, das Kunst und Eleganz in jeden Raum bringt",
            "Werte deinen Wohnraum mit einer bezaubernden Lampe auf, die die feine Kunst der "
            "Schmetterlinge mit einem warmen, wohltuenden Leuchten verbindet. Dieses fesselnde "
            "Dekostück bringt Schönheit, sanftes Licht und eine handgefertigte Note – ideal für "
            "Schlafzimmer, Wohnzimmer oder als Geschenk, das einen bleibenden Eindruck "
            "hinterlässt.",
            "Warum du die handgefertigte ButterGlow Glaslampe mit Schmetterling lieben wirst",
            [("Bezaubernde Ästhetik:", "Ein wunderschönes Schmetterlingsdesign, das jede "
              "Einrichtung sofort mit künstlerischer Magie bereichert."),
             ("Warmes, wohltuendes Licht:", "Schafft eine sanfte Atmosphäre, in der du nach einem "
              "langen Tag zur Ruhe kommst."),
             ("Handgefertigte Details:", "Mit Sorgfalt gefertigt für einen einzigartigen, "
              "hochwertigen Look, der in jedem Raum auffällt."),
             ("Vielseitig platzierbar:", "Passt perfekt auf Nachttische, Tische oder Regale und "
              "bringt Licht in deinen Wohnraum."),
             ("Durchdachtes Geschenk:", "Ein berührendes Geschenk für alle, die besondere und "
              "elegante Dekoration schätzen.")],
            [("Typ:", "Dekorative Lampe"), ("Design:", "Schmetterlingsmotiv"),
             ("Beleuchtung:", "Warmes Leuchten"), ("Stil:", "Handgefertigte Optik"),
             ("Verwendung:", "Innendekoration")])),

    "sunwing-lampara-con-alas-de-mosaico-amarillo": dict(
        handle="sunwing-lampe-mit-gelben-mosaikfluegeln",
        title="SUNWING | Lampe mit gelben Mosaikflügeln",
        body=body(
            "Verleihe jeder Ecke deines Zuhauses strahlende Eleganz",
            "Erhelle deinen Wohnraum mit einem warmen, goldenen Licht, inspiriert von "
            "künstlerischen Mosaikflügeln. Diese bezaubernde Lampe verbindet dekorative Schönheit "
            "mit sanfter Beleuchtung und schafft eine angenehme Atmosphäre – perfekt für "
            "Schlafzimmer, Wohnzimmer und gemütliche Leseecken. Ein beeindruckendes Akzentstück, "
            "das den Charakter und die Wärme deines Zuhauses unterstreicht.",
            "Warum du die SunWing Lampe mit gelben Mosaikflügeln lieben wirst",
            [("Goldenes Ambiente:", "Erzeugt ein beruhigendes gelbes Leuchten, das jedem Zimmer "
              "sofort Wärme und Behaglichkeit schenkt."),
             ("Künstlerisches Mosaikdesign:", "Das fesselnde Flügeldesign bereichert dein Interieur "
              "mit einer einzigartigen, eleganten Ästhetik."),
             ("Stimmungsvolles Licht:", "Die sanfte Beleuchtung fördert die Entspannung und eine "
              "ruhige Atmosphäre."),
             ("Überall ein Blickfang:", "Ideal für Nachttische, Tische oder Regale, um deinen "
              "Wohnraum zu beleben und zu verschönern."),
             ("Durchdachte Geschenkwahl:", "Ein bezauberndes Geschenk für alle, die künstlerische "
              "und bedeutungsvolle Wohndeko schätzen.")],
            [("Typ:", "Dekorative Lampe"), ("Design:", "Mosaikflügel"),
             ("Stil:", "Warmes Gelb"), ("Beleuchtung:", "Sanftes Leuchten"),
             ("Verwendung:", "Innendekoration")])),

    "brightwing-lampara-con-acento-de-arcoiris": dict(
        handle="brightwing-lampe-mit-regenbogen-akzent",
        title="BRIGHTWING | Lampe mit Regenbogen-Akzent",
        body=body(
            "Bringe Farbe und Magie in jedes Zimmer",
            "Verwandle deinen Wohnraum mit einem lebendigen Akzentstück voller Charme und "
            "Persönlichkeit. Diese bezaubernde Lampe erzeugt ein farbenfrohes, belebendes Leuchten, "
            "das deine Stimmung hebt und jedes Zimmer bereichert. Ideal für Schlafzimmer, auf "
            "Tischen oder in gemütlichen Ecken – sie verleiht deiner Einrichtung eine verspielte "
            "und zugleich elegante Note.",
            "Warum du die BrightWing Lampe mit Regenbogen-Akzent lieben wirst",
            [("Farbenfrohe Beleuchtung:", "Strahlt ein lebendiges Regenbogenleuchten aus, das deine "
              "Umgebung sofort belebt und auffrischt."),
             ("Fesselndes Design:", "Die von Flügeln inspirierte Form setzt einen künstlerischen "
              "Akzent, der als beeindruckendes Dekoelement heraussticht."),
             ("Belebendes Leuchten:", "Das sanfte, mehrfarbige Licht schafft jederzeit eine "
              "fröhliche und inspirierende Atmosphäre."),
             ("Kompakt und vielseitig:", "Passt perfekt auf Nachttische, Regale oder Tische, ohne "
              "viel Platz zu beanspruchen."),
             ("Durchdachtes Geschenk:", "Ein bezauberndes, einzigartiges Geschenk für alle, die "
              "lebendige und ausdrucksstarke Akzente zu Hause lieben.")],
            [("Typ:", "Akzentlampe"), ("Design:", "Flügelform"),
             ("Beleuchtung:", "Regenbogenleuchten"), ("Stil:", "Bunte Dekoration"),
             ("Verwendung:", "Innenbereich")],
            second_img=True)),
}

IMG_TAG = re.compile(r"<img[^>]*>")
# Page-Builder-Metadaten (data-gemlang, data-lazy-loaded ...) aus <img> entfernen;
# src, alt, style, width und height bleiben unangetastet.
DATA_ATTR = re.compile(r'\s+data-[\w-]+="[^"]*"')


def clean_img(tag):
    return DATA_ATTR.sub("", tag)


def bump_price(value):
    return "%.2f" % (decimal.Decimal(value) + PRICE_INCREASE) if value.strip() else value


def main():
    with open(SRC, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames, rows = reader.fieldnames, list(reader)

    for row in rows:
        spec = PRODUCTS[row["Handle"]]
        if row["Title"].strip():
            imgs = [clean_img(t) for t in IMG_TAG.findall(row["Body (HTML)"])]
            new_body = spec["body"]
            expected = len(re.findall(r"\{IMG\d\}", new_body))
            if len(imgs) != expected:
                raise ValueError("%s: %d <img> in der Quelle, %d im Template"
                                 % (row["Handle"], len(imgs), expected))
            for i, tag in enumerate(imgs, 1):
                new_body = new_body.replace("{IMG%d}" % i, tag)
            row["Title"] = spec["title"]
            row["Body (HTML)"] = new_body
            row["Type"] = TYPE_DE.get(row["Type"], row["Type"])
        row["Handle"] = spec["handle"]
        for col in PRICE_COLUMNS:
            row[col] = bump_price(row[col])

    with open(DST, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Zeilen: %d | Produkte: %d" % (len(rows), len(PRODUCTS)))


if __name__ == "__main__":
    main()
