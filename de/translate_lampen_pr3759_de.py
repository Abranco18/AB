# -*- coding: utf-8 -*-
"""Uebersetzt den Deko-Lampen-Export PR3759 (ES -> DE), Preise +5 EUR.

Jede Beschreibung ist einzeln uebersetzt; eingebettete <img>-Tags werden
unveraendert aus der Quelle uebernommen (Platzhalter {IMG1}, {IMG2}).
"""
import csv
import decimal
import re
import sys

SRC, DST = sys.argv[1], sys.argv[2]

PRICE_INCREASE = decimal.Decimal("5.00")
PRICE_COLUMNS = ("Variant Price", "Variant Compare At Price")


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
    "snailglow-lampara-de-escritorio-en-forma-de-caracol": dict(
        handle="snailglow-schreibtischlampe-in-schneckenform",
        title="SNAILGLOW | Schreibtischlampe in Schneckenform",
        body=body(
            "Bringe verspielte, magische Stimmung mit buntem Licht in jedes Zimmer",
            "Erhelle deinen Wohnraum mit einer faszinierenden Verbindung aus Kunst und sanftem, "
            "farbenfrohem Licht. Diese außergewöhnliche Lampe verwandelt gewöhnliche Räume in einen "
            "magischen Rückzugsort und schafft eine gemütliche Atmosphäre – ideal zum Entspannen, "
            "Lesen oder einfach, um ihr verspieltes Design und ihr warmes Umgebungslicht zu "
            "genießen.",
            "Warum du SnailGlow | Buntglaslampe in Schneckenform lieben wirst",
            [("Lebendiges Licht:", "Erzeugt ein farbenfrohes Leuchten, das jeden Raum sofort "
              "erhellt und die Atmosphäre verbessert."),
             ("Verspieltes Design:", "Die bezaubernde Schneckenform bringt Persönlichkeit und einen "
              "einzigartigen künstlerischen Stil in deine Wohndeko."),
             ("Fesselnder Akzent:", "Macht sich hervorragend als Blickfang auf Schreibtischen, "
              "Regalen oder Nachttischen."),
             ("Beruhigende Atmosphäre:", "Das sanfte Licht schafft ein ruhiges, gemütliches "
              "Ambiente – ideal zum Entspannen nach langen Tagen."),
             ("Schönes Geschenk:", "Ideal für alle, die kreative Beleuchtung oder einzigartige "
              "Dekostücke lieben.")],
            [("Typ:", "Dekorative Lampe"), ("Design:", "Schneckenmotiv"),
             ("Stil:", "Buntglas-Optik"), ("Beleuchtung:", "Sanftes Licht"),
             ("Verwendung:", "Innendekoration")],
            second_img=True)),

    "deepglow-lampara-marina-con-motivo-de-tentaculos": dict(
        handle="deepglow-maritime-lampe-mit-tentakelmotiv",
        title="DEEPGLOW | Maritime Lampe mit Tentakelmotiv",
        body=body(
            "Erhelle deinen Wohnraum mit einem Hauch geheimnisvoller Tiefe",
            "Hole dir eine faszinierende Unterwasseratmosphäre nach Hause – mit einer Lampe, die "
            "begeistert und inspiriert. Ihre künstlerische Tentakelstruktur und das sanfte Leuchten "
            "schaffen ein Ambiente, das zugleich ausdrucksstark und beruhigend wirkt: ein "
            "beeindruckender Blickfang für jedes Schlafzimmer, Büro oder jede gemütliche Ecke.",
            "Warum du die DeepGlow Lampe mit maritimen Tentakeln lieben wirst",
            [("Beeindruckendes, vom Ozean inspiriertes Design:", "Setzt einen maritim-"
              "künstlerischen Akzent, der die Ästhetik jedes Zimmers sofort aufwertet."),
             ("Warmes Umgebungslicht:", "Erzeugt ein beruhigendes Leuchten – ideal zum Entspannen, "
              "Lesen oder Ausruhen am Abend."),
             ("Einzigartiges Dekoelement:", "Funktioniert als Leuchte und zugleich als fesselnder "
              "dekorativer Blickfang."),
             ("Gesprächsstoff garantiert:", "Ihre kreative Tentakelform zieht die Blicke auf sich "
              "und weckt die Neugier deiner Gäste."),
             ("Die perfekte Geschenkwahl:", "Ideal für Ozeanliebhaber, Fantasy-Fans und alle, die "
              "außergewöhnliche Dekoration schätzen.")],
            [("Typ:", "Tischlampe"), ("Design:", "Tentakel-Stil"),
             ("Beleuchtung:", "Warmes Leuchten"), ("Thema:", "Maritime Dekoration"),
             ("Verwendung:", "Innenbereich")])),

    "pinkglow-lampara-de-mesa-rosa-con-efecto-de-luz-delicada": dict(
        handle="pinkglow-rosa-tischlampe-mit-sanftem-lichteffekt",
        title="PINKGLOW | Rosa Tischlampe mit sanftem Lichteffekt",
        body=body(
            "Bringe einen Hauch magisches Licht in jedes Zimmer",
            "Schaffe eine bezaubernde Atmosphäre mit einem Licht, das Verspieltheit, Magie und "
            "warme Beleuchtung vereint. Ideal für Schlafzimmer, Büros und gemütliche Ecken – es "
            "verwandelt gewöhnliche Räume in einen beruhigenden Rückzugsort und setzt zugleich ein "
            "schönes dekoratives Element, das Fantasie und Behaglichkeit weckt.",
            "Warum du die bezaubernde PinkGlow Lampe lieben wirst",
            [("Sanftes Umgebungslicht:", "Erzeugt ein beruhigendes Leuchten, das sofort für eine "
              "ruhige und behagliche Stimmung sorgt."),
             ("Verspieltes Design:", "Die von Pilzen inspirierte Form bringt eine verspielte, "
              "bezaubernde Note und verschönert deine Wohndeko."),
             ("Kompakt und vielseitig:", "Passt perfekt auf Nachttische, Regale oder Schreibtische, "
              "ohne viel Platz zu beanspruchen."),
             ("Stimmungsvolles Licht:", "Die sanfte Beleuchtung hilft, Stress abzubauen, und schafft "
              "eine beruhigende Atmosphäre."),
             ("Magische Geschenkidee:", "Ein niedliches, durchdachtes Geschenk für alle, die "
              "einzigartige Dekostücke lieben.")],
            [("Typ:", "Dekorative Leuchte"), ("Design:", "Pilzform"),
             ("Stil:", "Sanftes Licht"), ("Beleuchtung:", "Warmes Ambiente"),
             ("Verwendung:", "Innendekoration")])),

    "colorshroom-lampara-magica-con-diseno-de-hongo": dict(
        handle="colorshroom-magische-lampe-im-pilzdesign",
        title="COLORSHROOM | Magische Lampe im Pilzdesign",
        body=body(
            "Bringe ein magisches Leuchten in jedes Zimmer",
            "Erhelle deinen Wohnraum mit einer verspielten Note, die faszinierende Farben und "
            "sanftes Licht verbindet. Diese bezaubernde Lampe in Pilzform schafft eine "
            "verträumte, anregende Atmosphäre – ideal für Schlafzimmer, Spielbereiche, Wohnzimmer "
            "oder kreative Räume. So werden gewöhnliche Zimmer im Handumdrehen zu lebendigen, "
            "gemütlichen Rückzugsorten.",
            "Warum du den magischen COLORSHROOM Pilz lieben wirst",
            [("Buntes Leuchten:", "Erzeugt ein strahlendes Licht in Regenbogenfarben, das die "
              "Stimmung hebt und jeden Raum magisch wirken lässt."),
             ("Verspieltes Design:", "Die von Pilzen inspirierte Form bringt spielerischen Charme "
              "und dient als außergewöhnliches Dekoelement."),
             ("Behagliche Beleuchtung:", "Das sanfte Licht schafft eine warme, entspannende "
              "Atmosphäre – ideal zum Ausruhen."),
             ("Perfekter Akzent:", "Wertet Tische, Nachttische oder Regale mit einer einzigartigen "
              "und attraktiven Dekoration auf."),
             ("Geschenkfertig:", "Eine schöne Überraschung für alle, die kreative und farbenfrohe "
              "Dekoelemente für ihr Zuhause lieben.")],
            [("Typ:", "Akzentlampe"), ("Design:", "Pilzform"),
             ("Stil:", "Regenbogenleuchten"), ("Beleuchtung:", "Sanftes Licht"),
             ("Verwendung:", "Innendekoration")])),

    "gardenluxe-lampara-de-mesa-floral-colorida": dict(
        handle="gardenluxe-bunte-florale-tischlampe",
        title="GARDENLUXE | Bunte florale Tischlampe",
        body=body(
            "Bringe einen verspielten, warmen Farbtupfer in jedes Zimmer",
            "Erhelle deinen Wohnraum mit einer bezaubernden Lampe, die florale Kunst und ein "
            "fesselndes, von Pilzen inspiriertes Design verbindet. Ihr farbenfrohes Licht "
            "verwandelt Schlafzimmer, Wohnzimmer und gemütliche Ecken in angenehme, aufmunternde "
            "Räume und setzt zugleich einen einzigartigen dekorativen Akzent, der in jedes Zuhause "
            "passt.",
            "Warum du die GardenLuxe Lampe mit floralem Pilz lieben wirst",
            [("Lebendiges Ambiente:", "Erzeugt ein farbenfrohes, beruhigendes Licht, das die "
              "Entspannung fördert und die Stimmung im Zimmer hebt."),
             ("Fesselndes Design:", "Die von Pilzen inspirierten Details verleihen deiner "
              "Einrichtung eine verspielte und zugleich elegante Note."),
             ("Blickfang garantiert:", "Sie wird sofort zum Mittelpunkt, sorgt für Komplimente und "
              "bringt Persönlichkeit in jeden Raum."),
             ("Beruhigende Beleuchtung:", "Das sanfte Licht hilft, Stress abzubauen, und fördert "
              "eine ruhige, behagliche Atmosphäre."),
             ("Durchdachte Geschenkidee:", "Ideal für alle, die von der Natur inspirierte "
              "Dekoration und außergewöhnliche Leuchten lieben.")],
            [("Typ:", "Dekorative Lampe"), ("Design:", "Floraler Pilz"),
             ("Stil:", "Buntes Licht"), ("Beleuchtung:", "Sanftes Licht"),
             ("Verwendung:", "Innendekoration")])),

    "blueaura-lampara-de-escritorio-azul-con-un-aire-mistico": dict(
        handle="blueaura-blaue-schreibtischlampe-mit-mystischem-flair",
        title="BLUEAURA | Blaue Schreibtischlampe mit mystischem Flair",
        body=body(
            "Erhelle deinen Wohnraum mit einem faszinierenden blauen Leuchten",
            "Erlebe ein faszinierendes Licht, das jedes Zimmer in eine ruhige, elegante Oase "
            "verwandelt. Diese wunderschön geschwungene Lampe bringt eine beruhigende blaue "
            "Atmosphäre und ist damit ideal für Schlafzimmer, Wohnzimmer oder Arbeitsplätze. Ihr "
            "künstlerisches Design wertet die Einrichtung auf und schenkt zugleich eine "
            "wohltuende Note, die deinen Alltag bereichert.",
            "Warum du die BlueAura Mystic Blue Lampe lieben wirst",
            [("Beruhigendes blaues Licht:", "Schafft eine entspannende Atmosphäre, in der du nach "
              "einem langen Tag zur Ruhe kommst."),
             ("Künstlerische Optik:", "Das einzigartige, geschwungene Design bringt Persönlichkeit "
              "und Charme in jedes Interieur."),
             ("Sanftes Umgebungslicht:", "Das weiche Licht ist angenehm für die Augen und macht "
              "gemütliche Momente noch schöner."),
             ("Passt überall:", "Ergänzt moderne, Retro- oder minimalistische Einrichtungen "
              "mühelos und elegant."),
             ("Durchdachte Geschenkwahl:", "Ein schönes Geschenk für alle, die beruhigendes Licht "
              "und kreative Dekoration lieben.")],
            [("Typ:", "Dekorative Lampe"), ("Design:", "Mystisches Blau"),
             ("Stil:", "Sanftes Licht"), ("Beleuchtung:", "Umgebungslicht"),
             ("Verwendung:", "Innendekoration")])),

    "shroomglow-lampara-de-noche-artesanal-en-forma-de-hongo": dict(
        handle="shroomglow-handgefertigte-nachtlampe-in-pilzform",
        title="SHROOMGLOW | Handgefertigte Nachtlampe in Pilzform",
        body=body(
            "Bringe magischen Charme und behagliches Licht in jedes Zimmer",
            "Hole dir einen Hauch Magie nach Hause – mit einer Lampe, die sanft leuchtet und vom "
            "Charme der Natur inspiriert ist. Ihr warmes Licht schafft eine beruhigende "
            "Atmosphäre, ideal zum Einschlafen, Entspannen oder für abendliche Aufgaben, während "
            "ihr handgefertigtes Pilzdesign jedem Interieur Charakter und Stil verleiht.",
            "Warum du die ShroomGlow Nachtlampe lieben wirst",
            [("Magische Ästhetik:", "Zaubert eine märchenhafte Waldatmosphäre und verschönert "
              "Schlafzimmer, Tische oder Leseecken."),
             ("Beruhigendes Licht:", "Gibt ein sanftes Licht ab – ideal zum Entspannen, für ruhige "
              "Abende und einen friedlichen Schlafrhythmus."),
             ("Handgefertigte Details:", "Jedes Stück trägt die einzigartige Handschrift des "
              "Handwerks und macht deine Lampe zu etwas ganz Besonderem."),
             ("Passt in jedes Zimmer:", "Das kompakte Design fügt sich nahtlos auf Nachttische, "
              "Regale oder Schreibtische ein, ohne Unordnung zu schaffen."),
             ("Durchdachtes Geschenk:", "Ein schönes und unvergessliches Geschenk für "
              "Naturliebhaber, Deko-Fans oder Kinder.")],
            [("Typ:", "Nachtlampe"), ("Design:", "Pilz-Stil"),
             ("Beleuchtung:", "Warmes Licht"), ("Textur:", "Weiche Oberfläche"),
             ("Verwendung:", "Innendekoration")])),
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
