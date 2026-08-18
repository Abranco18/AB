# -*- coding: utf-8 -*-
"""Uebersetzt den Tassen-Export NM0053 (ES -> DE), Preise +5 EUR.

Alle Beschreibungen sind einzeln uebersetzt. Eingebettete <img>-Tags werden
unveraendert in Reihenfolge aus der Quelle uebernommen ({IMG1}, {IMG2} ...).
"""
import csv
import decimal
import re
import sys

SRC, DST = sys.argv[1], sys.argv[2]

PRICE_INCREASE = decimal.Decimal("5.00")
PRICE_COLUMNS = ("Variant Price", "Variant Compare At Price")

OPTION_NAMES_DE = {"Estilo": "Stil", "Oferta": "Angebot"}   # "Title" ist ein Shopify-Systemwert
OPTION_VALUES_DE = {
    "1x Taza": "1x Tasse", "2x Tazas": "2x Tassen", "3x Tazas": "3x Tassen",
    "Ágata": "Achat", "Amatista": "Amethyst", "Rojo volcánico": "Vulkanrot",
    # "Menos azul"/"Menos verde" sind schon im spanischen Original unklar – siehe README
    "Menos azul": "Weniger Blau", "Menos verde": "Weniger Grün",
}


def book_mug_body(subject="Buch"):
    """Gemeinsame Vorlage der 3D-Buchtassen (im Original 6x leicht umformuliert)."""
    if subject == "Gitarre":
        hero = ("<strong>Von Hand gefertigt mit detailreichen 3D-Gitarren</strong>, ist jede Tasse "
                "ein echtes Unikat.<br>Als hättest du ein Stück Musikgeschichte in den Händen.")
        intro_h2 = "Eine Tasse, die Musikfans begeistert – das Geschenk des Jahres"
        opener = ("<strong>Diese Gitarrentasse</strong> ist nicht einfach nur eine Tasse –<br>"
                  "sie ist ein kleines Stück Magie für alle, die Musik lieben.<br>")
        cup = "Die Gitarrentasse"
        closing_h2 = "Die Magie der Musik – in jedem Schluck"
        closing = ("Starte deinen Tag mit einem Lächeln, deinem Lieblingssong<br>und "
                   "<strong>deiner Gitarrentasse</strong> –<br>und mach jeden Schluck zu einem "
                   "fröhlichen, ruhigen Moment.")
        gift = ("Ein bedeutungsvolles Geschenk – für dich oder für jemanden, der Musik genauso "
                "liebt wie du.")
        moments = "Ob bei ruhigen Momenten mit Musik oder im Gespräch mit Freunden –"
    else:
        hero = ("<strong>Von Hand gefertigt mit detailreichen 3D-Buchrücken</strong>, ist jede "
                "Tasse ein echtes Unikat.<br>Als hättest du eine Mini-Bibliothek in den Händen.")
        intro_h2 = "Eine Tasse, die Bücherfreunde begeistert – das Geschenk des Jahres"
        opener = ("<strong>Diese Buchtasse</strong> ist nicht einfach nur eine Tasse –<br>"
                  "sie ist ein kleines Stück Magie für alle, die Bücher lieben.<br>")
        cup = "Die Buchtasse"
        closing_h2 = "Die Magie des Lesens – in jedem Schluck"
        closing = ("Starte deinen Tag mit einem Lächeln, einem guten Buch<br>und "
                   "<strong>deiner Buchtasse</strong> –<br>und mach jeden Schluck zu einem "
                   "fröhlichen, ruhigen Moment.")
        gift = ("Ein bedeutungsvolles Geschenk – für dich oder für jemanden, der Bücher genauso "
                "liebt wie du.")
        moments = "Ob bei ruhigen Lesestunden oder im Gespräch mit Freunden –"

    return "\n".join([
        "<div>",
        "<h3>Warum alle diese Tasse lieben:</h3>",
        "<p>✨ <strong>Beeindruckendes 3D-Design</strong><br>Faszinierende Details, die im Licht "
        "zum Leben erwachen.</p>",
        "<p>🖐️ <strong>Handgefertigte Handwerkskunst</strong><br>Jede Tasse ist ein Kunstwerk – "
        "ganz einzigartig für dich.</p>",
        "<p>🥇 <strong>Hochwertiges Glas</strong><br>Fühlt sich angenehm an und wirkt elegant "
        "und robust.</p>",
        "<p>💬 <strong>Ein echter Gesprächsanlass</strong><br>Deine Freunde und Gäste werden "
        "begeistert sein.</p>",
        "<p>🎁 <strong>Die perfekte Geschenkidee</strong><br>Persönlich, stilvoll und "
        "unvergesslich.</p>",
        "<p>Farben, die im Licht funkeln, und feine Handwerkskunst machen jeden Moment besonders."
        "<br>Nicht nur eine Tasse – ein Stück, das deinen Alltag bereichert.</p>",
        "<p>{IMG1}</p>",
        '<div style="text-align: left;">',
        "<h2>%s</h2>" % intro_h2,
        "<p>%s%s</p>" % (opener, hero),
        "<h2>Gemacht für jeden Tag – und für bewundernde Blicke</h2>",
        "<p>Ob heißer Espresso oder kalter Tee:<br><strong>%s</strong> hält dein Getränk perfekt "
        "in Balance und liegt angenehm in der Hand.<br><strong>Wärmeisolierend, robust und "
        "elegant – vom Morgen bis zum Abend.</strong></p>" % cup,
        "<h2>Warum diese Tasse mehr ist als nur ein Trinkgefäß</h2>",
        "<p>Mit ihrer perfekten Größe ist sie ideal für den Kaffee am Morgen, den Tee am "
        "Nachmittag oder zum Entspannen am Abend.<br>Aus dickem, widerstandsfähigem Glas – "
        "<strong>mikrowellen- und spülmaschinengeeignet</strong>.<br>Pflegeleicht und für den "
        "täglichen Gebrauch gemacht.</p>",
        "<p>%s<br>diese Tasse verleiht jedem Moment eine besondere Magie.<br><strong>Nicht nur "
        "ein Gefäß – eine Erinnerung mit Herz.</strong></p>" % moments,
        '<div style="text-align: left;"><br></div>',
        "<h2>Ein Geschenk, das du nie vergisst</h2>",
        "<p>Du suchst etwas Besonderes?<br>Diese handgefertigte Tasse <strong>vereint Kunst, "
        "Funktionalität und Persönlichkeit</strong>.<br>%s</p>" % gift,
        '<div style="text-align: left;"><br></div>',
        "<h2>%s</h2>" % closing_h2,
        "<p>%s</p>" % closing,
        "<hr>🎉 <strong>Jetzt bestellen und 70 % sparen!</strong> – nur solange der Vorrat "
        "reicht!</div>",
        "</div>",
    ])


BODY_MUG_BOOK = "\n".join([
    '<h2 style="text-align: center;" class="gf_gs-text-heading-2">Das perfekte Geschenk für '
    'Bücherfreunde – handgefertigte 3D-Buchtasse, magisch und voller Details</h2>',
    "<p>{IMG1}</p>",
    "<p><strong>Warum alle die 3D-Bibliothekstasse lieben:</strong></p>",
    "<p>📚 <strong>Bezauberndes 3D-Buchdesign</strong><br>Jede Tasse ist einem Stapel geliebter "
    "Klassiker nachempfunden – Literatur, Poesie, Geschichte und Romane – und wird so zum echten "
    "Schatz für alle Bücherfreunde.</p>",
    "<p>🖐️ <strong>Handgefertigt mit viel Liebe zum Detail</strong><br>Jede Rundung, jede Textur "
    "und jeder Buchrücken ist sorgfältig modelliert und von Hand bemalt – das gibt der Tasse ihre "
    "Wärme und ihr handwerkliches Finish.</p>",
    "<p>☕ <strong>Robust, funktional und ein Blickfang</strong><br>Aus langlebigen Materialien für "
    "den täglichen Gebrauch – perfekt für Kaffee, Tee oder heiße Schokolade. Der Henkel liegt "
    "bequem in der Hand und ist gemacht, um zu halten.</p>",
    "<p>🎁 <strong>Ein bedeutungsvolles Geschenk für Leseratten</strong><br>Ideal für Bücherwürmer, "
    "Autorinnen und Autoren, Lehrkräfte und Kaffeeliebhaber. Ein kreatives Geschenk, das die "
    "Schönheit von Geschichten und ruhigen Morgenstunden feiert.</p>",
    "<p>💫 <strong>Maße und Fassungsvermögen</strong><br>Höhe: 12 cm | Breite: 10 cm | "
    "Fassungsvermögen: ca. 330 ml (11 oz)</p>",
    "<p>{IMG2}</p>",
    "<h2>Die Tasse, die lesende Freunde begeistert – das Geschenk des Jahres</h2>",
    "<p><strong>Der Rückzugsort für Bücherfreunde</strong> ist nicht einfach nur eine Tasse – sie "
    "ist ein kleines Stück Magie für alle, die Bücher lieben. <strong>Von Hand gefertigt mit sehr "
    "detailreichen 3D-Buchrücken</strong>, ist jede Tasse ein echtes Unikat. Fast so, als hieltest "
    "du eine Mini-Bibliothek in den Händen.</p>",
    "<p>{IMG3}</p>",
    "<h2>Gemacht für den Alltag – entworfen, um zu überraschen</h2>",
    "<p>Ob heißer Espresso oder eisgekühlter Tee:<br>Die Tasse hält dein Getränk perfekt in Balance "
    "und liegt angenehm in der Hand.<br><strong>Isolierend, robust und stilvoll – vom Morgen bis "
    "zum Abend.</strong></p>",
    "<p>{IMG4}</p>",
    "<h2>Warum diese Tasse mehr ist als nur eine Tasse</h2>",
    "<p>Sie hat genau die richtige Größe für den Kaffee am Morgen, den Tee am Nachmittag oder die "
    "Pause am Abend.<br>– <strong>mikrowellen- und spülmaschinengeeignet</strong>.<br>Pflegeleicht "
    "und für den täglichen Gebrauch gedacht.</p>",
    "<p>Ob bei ruhigen Lesestunden oder im Gespräch mit Freunden –<br>diese Tasse verleiht jedem "
    "Moment einen besonderen Zauber.<br><strong>Mehr als eine Tasse – eine Erinnerung mit "
    "Herz.</strong></p>",
    "<p><strong>Die 3D-Bibliothekstasse ist nicht nur eine Tasse – sie ist eine Hommage an jede "
    "Geschichte, die je erzählt wurde.</strong><br><strong>Ein Miniatur-Bücherregal, das deine "
    "Hände und dein Herz wärmt.</strong><br><strong>Perfekt für gemütliche Leseabende oder als "
    "Dekostück in deinem eigenen Bücherregal.</strong></p>",
])

BODY_TAZA_LIBRO = "\n".join([
    '<h2 class="gf_gs-text-heading-2">Das perfekte Geschenk für Bücherfreunde – handgefertigte '
    '3D-Buchtasse, magisch und voller Details</h2>',
    "<p>{IMG1}</p>",
    "<h2>Warum alle die 3D-Lesetasse lieben:</h2>",
    "<ul>",
    "<li>",
    "<p>📘 <strong>Beeindruckendes 3D-Buchdesign</strong><br>Fesselnde Details, die im Sonnenlicht "
    "zum Leben erwachen.</p>",
    "</li>",
    "<li>",
    "<p>🖐️ <strong>Handgefertigt mit Liebe zum Detail</strong><br>Jede Tasse ist ein Kunstwerk – "
    "so einzigartig wie dein Bücherregal.</p>",
    "</li>",
    "<li>",
    "<p>🥇 <strong>Dickes, hochwertiges Glas</strong><br>Liegt angenehm in der Hand, wirkt elegant "
    "und ist robust.</p>",
    "</li>",
    "<li>",
    "<p>🗨️ <strong>Ein echter Gesprächsanlass</strong><br>Deine Freunde und Gäste werden begeistert "
    "sein – garantiert!</p>",
    "</li>",
    "<li>",
    "<p>🎁 <strong>Das perfekte Geschenk für Leseratten</strong><br>Persönlich, stilvoll und "
    "unvergesslich.</p>",
    "</li>",
    "</ul>",
    "<p>Sobald das Sonnenlicht die Tasse berührt, beginnt sie zu leuchten:<br><strong>tiefrote "
    "Buchrücken, goldene Details und tintenblaue Akzente</strong> – ein faszinierender 3D-Effekt, "
    "der jedes Bücherherz höherschlagen lässt.</p>",
    "<p>{IMG2}</p>",
    "<h2>Die Tasse, die Leseratten verzaubert – das Geschenk des Jahres</h2>",
    "<p>Die <strong>Lesefreude-Tasse</strong> ist nicht einfach nur eine Tasse – sie ist ein "
    "kleines Stück Magie für alle, die Bücher lieben.<br><strong>Von Hand gefertigt mit "
    "kunstvollen 3D-Buchrücken</strong>, ist jede Tasse ein echtes Unikat.<br>Fast so, als hättest "
    "du eine Mini-Bibliothek in den Händen.</p>",
    "<p>{IMG3}</p>",
    "<h2>Gemacht für den Alltag – entworfen, um zu überraschen</h2>",
    "<p>Ob heißer Espresso oder eisgekühlter Tee:<br>Die Lesefreude-Tasse hält dein Getränk in "
    "perfekter Balance und liegt angenehm in der Hand.<br><strong>Isolierend, robust und stilvoll – "
    "vom Morgen bis zum Abend.</strong></p>",
    "<p>{IMG4}</p>",
    "<h2>Warum diese Tasse weit mehr ist als eine einfache Tasse</h2>",
    "<p>Sie hat genau die richtige Größe für den Kaffee am Morgen, den Tee am Nachmittag oder die "
    "Pause am Abend.<br>Aus dickem, langlebigem Glas – <strong>mikrowellen- und "
    "spülmaschinengeeignet</strong>.<br>Pflegeleicht und bereit für den täglichen Gebrauch.</p>",
    "<p>Ob bei ruhigen Lesemomenten oder im Gespräch mit Freunden – diese Tasse verleiht jedem "
    "Augenblick einen besonderen Zauber.<br><strong>Mehr als eine Tasse – eine Erinnerung mit "
    "Herz.</strong></p>",
    '<div style="text-align: left;">{IMG5}</div>',
    "<h2>Ein Geschenk, das du nie vergisst</h2>",
    "<p>Du suchst etwas Besonderes?<br>Diese handgefertigte Tasse vereint <strong>Kunst, "
    "Funktionalität und Persönlichkeit</strong>.<br>Ein bedeutungsvolles Geschenk – für dich oder "
    "für die Person, die Bücher genauso liebt wie du.</p>",
    '<div style="text-align: left;">{IMG6}</div>',
    "<h2>Die Magie des Lesens – in jedem Schluck</h2>",
    "<p>Starte deinen Tag mit einem Lächeln, einem guten Buch und deiner <strong>Lesetasse</strong> "
    "– und mach jeden Schluck zu einem ruhigen, fröhlichen Moment.</p>",
    "<hr>",
    '<div style="text-align: left;">{IMG7}</div>',
    "<p>Denn keine gewöhnliche Tasse trägt diesen Geist in sich.</p>",
    "<p>Den Geist der Geschichten, der Erinnerungen und der stillen Freude.</p>",
    '<div style="text-align: left;">{IMG8}</div>',
    "<h3>So praktisch wie beeindruckend</h3>",
    "<p>Die unglaublich realistischen 3D-Texturen der Buchrücken, die leuchtenden Farben, der "
    "sanfte Glanz in der Sonne …</p>",
    "<p>Wer die Lesetasse sieht, verliebt sich auf den ersten Blick.</p>",
    "<p>Doch sobald du sie in den Händen hältst, wird klar: Sie ist weit mehr als nur schön.</p>",
    "<p>Hinter ihrem künstlerischen Charme steckt auch eine überraschend praktische Seite: Mit "
    "großzügigen 330 ml Fassungsvermögen ist sie ideal für Kaffee, Tee, Saft – oder was immer du "
    "am liebsten trinkst.</p>",
    "<p>Ob zu Hause, im Büro oder wenn du Gäste empfängst – diese Tasse passt perfekt in deinen "
    "Alltag.</p>",
    "<p>Die handwerkliche Sorgfalt sorgt nicht nur für ein besonderes Aussehen, sondern auch für "
    "erstklassige Qualität. Hochwertige Materialien stehen für Langlebigkeit, Hitzebeständigkeit "
    "und angenehme Isolierung.</p>",
    "<p>Und das Beste: Die Lesetasse ist mikrowellen- und spülmaschinengeeignet – für maximalen "
    "Komfort im Alltag.</p>",
])

BODY_COFFE_CUPS = "\n".join([
    '<h2 style="text-align: center;"><strong>Hol dir die Schönheit der Natur in deinen '
    'Morgenkaffee!</strong></h2>',
    "<p>{IMG1}</p>",
    "<p>Genieße einen Hauch Luxus mit unseren <em><strong>Kaffeetassen aus "
    "Mineralkristall</strong></em>, die <strong>Eleganz und Funktionalität</strong> verbinden. "
    "Diese von <strong>beeindruckenden Edelsteinen</strong> inspirierten Tassen bringen ein Stück "
    "Magie und Schönheit in deinen Alltag.</p>",
    "<p>{IMG2}</p>",
    "<h3><strong>Einzigartiges Design</strong></h3>",
    "<p>Jede Tasse spiegelt die natürliche Schönheit von Kristallen wie Amethyst oder Obsidian "
    "wider und wird garantiert zum Mittelpunkt aller Blicke.</p>",
    "<h3><strong>Hochwertige Handwerkskunst</strong></h3>",
    "<p>Sorgfältig gefertigt und von Hand poliert – diese Tassen sind langlebig und von hoher "
    "Qualität.</p>",
    "<p>{IMG3}</p>",
    "<h3><strong>Vielseitig</strong></h3>",
    "<p>Dank ihrer isolierenden Eigenschaften perfekt für Kaffee, Tee, Wein oder kalte "
    "Getränke.</p>",
    "<h3><strong>Ein besonderes Geschenk</strong></h3>",
    "<p>Eine ideale Wahl für alle, die Kunst, Eleganz oder einen Hauch Magie im Alltag "
    "schätzen.</p>",
    "<p>{IMG4}</p>",
    "<h3><strong>Spezifikationen:</strong></h3>",
    "<ul>",
    "<li>Maße: ca. 11,5 cm hoch und 9 cm breit (leichte Abweichungen möglich)</li>",
    "<li>Fassungsvermögen: 250 ml</li>",
    "<li>Gewicht: 100–200 g</li>",
    "<li>Pflegehinweise: spülmaschinen- und mikrowellengeeignet</li>",
    "<li>Garantie: frei von Schadstoffen wie Blei</li>",
    "</ul>",
    "<p>{IMG5}</p>",
])

BODY_HALLOWEEN = "\n".join([
    "<h3>Das perfekte Geschenk für Halloween-Fans – handgefertigte 3D-Hexentasse, magisch und "
    "voller schaurigem Charme</h3>",
    "<p>{IMG1}</p>",
    "<hr>",
    "<p><strong>Warum alle die 3D-Halloween-Tasse lieben:</strong><br>🧙 Bezauberndes "
    "3D-Hexendesign<br>Eine mystische Szene mit Hexe, Katze und Wald, die in schaurig-schönem "
    "Charme erstrahlt.</p>",
    "<p><strong>🖐️ Handgefertigt mit Liebe zum Detail</strong><br>Jede Tasse wird sorgfältig "
    "gefertigt und erhält so ihre einzigartige, magische Ausstrahlung.</p>",
    "<p><strong>🥇 Hochwertige Handwerkskunst</strong><br>Langlebig und angenehm in der Hand – "
    "gemacht, um zu beeindrucken und deine Getränke köstlich zu halten.</p>",
    "<p><strong>🗨️ Ein echter Gesprächsanlass</strong><br>Perfekt für Halloween-Partys oder "
    "gemütliche Herbstabende.</p>",
    "<p><strong>🎁 Das perfekte Geschenk zur Saison</strong><br>Eine durchdachte und unvergessliche "
    "Überraschung für alle, die Halloween und Fantasy lieben.</p>",
    "<p>{IMG2}</p>",
    "<hr>",
    "<p><strong>Sie leuchtet im Geist von Halloween</strong><br>Wenn das Licht auf die Tasse "
    "fällt, erwachen die Silhouette der Hexe, der leuchtende Wald und die verzauberten Details zum "
    "Leben und schaffen eine warme, magische Stimmung, die perfekt zur schaurigsten Jahreszeit "
    "passt.</p>",
    "<p><strong>Die Tasse, die Halloween-Fans verzaubert</strong><br>Das ist nicht nur eine Tasse: "
    "Es ist ein Kunstwerk voller Geheimnis. Die kunstvollen 3D-Details lassen jeden Schluck wie "
    "einen Teil einer Geschichte wirken.</p>",
    "<p><strong>Gemacht für den Alltag</strong><br>Ob heiße Schokolade, Kaffee oder Tee – diese "
    "Tasse erfüllt deinen Tag mit einem magischen Leuchten. Robust, isolierend und ebenso "
    "funktional wie schön gestaltet.</p>",
    "<p><strong>Ein Geschenk, das in Erinnerung bleibt</strong><br>Ideal für Halloween-Partys, "
    "herbstliche Zusammenkünfte oder als Sammlerstück – diese Tasse verbindet Kunst, "
    "Funktionalität und Charme in einem unvergesslichen Design.</p>",
    "<p>{IMG3}</p>",
    "<hr>",
    "<p>✨ Bring Magie und Geheimnis in jeden Schluck – mit der 3D-Halloween-Tasse.</p>",
])

PRODUCTS = {
    "handcrafted-eterna-cup-set-of-3": dict(
        handle="handgefertigte-3d-tasse-eterna",
        title="Handgefertigte 3D-Tasse Eterna",
        body=book_mug_body()),
    "mug-book": dict(
        handle="buecherliebhaber-handgefertigte-3d-kaffeetasse",
        title="Bücherliebhaber – Handgefertigte 3D-Kaffeetasse",
        body=BODY_MUG_BOOK),
    "artisan-crafted-luna-cup": dict(
        handle="handgefertigte-tasse-luna",
        title="Handgefertigte Tasse Luna",
        body=book_mug_body()),
    "handcrafted-dwarf-mug-for-3-books": dict(
        handle="handgefertigte-zwergen-tasse-mit-3d-buechern",
        title="Handgefertigte Zwergen-Tasse mit 3D-Büchern",
        body=book_mug_body()),
    "taza-libro": dict(
        handle="handgefertigte-lesetasse-original",
        title="Handgefertigte Lesetasse – Original",
        body=BODY_TAZA_LIBRO),
    "handcrafted-colorful-book-mug": dict(
        handle="handgefertigte-bunte-buchtasse",
        title="Handgefertigte bunte Buchtasse",
        body=book_mug_body()),
    "handcrafted-mug-featuring-3-guitar-designs": dict(
        handle="handgefertigte-tasse-mit-3d-gitarrendesign",
        title="Handgefertigte Tasse mit 3D-Gitarrendesign",
        body=book_mug_body("Gitarre")),
    "coffe-cups": dict(
        handle="kaffeetassen-aus-mineralkristall",
        title="Kaffeetassen aus Mineralkristall",
        body=BODY_COFFE_CUPS),
    "halloween-mug": dict(
        handle="handgefertigte-3d-tasse-hexe-und-katze",
        title="Handgefertigte 3D-Tasse – Hexen- und Katzendesign",
        body=BODY_HALLOWEEN),
    "handcrafted-aurora-3-book-mug": dict(
        handle="handgefertigte-3d-buchtasse-aurora",
        title="Handgefertigte 3D-Buchtasse Aurora",
        body=book_mug_body()),
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
            expected = len(set(re.findall(r"\{IMG\d\}", new_body)))
            if len(imgs) != expected:
                raise ValueError("%s: %d <img> in der Quelle, %d im Template"
                                 % (row["Handle"], len(imgs), expected))
            for i, tag in enumerate(imgs, 1):
                new_body = new_body.replace("{IMG%d}" % i, tag)
            row["Title"] = spec["title"]
            row["Body (HTML)"] = new_body
        row["Handle"] = spec["handle"]

        for col in ("Option1 Name", "Option2 Name", "Option3 Name"):
            if row[col].strip():
                row[col] = OPTION_NAMES_DE.get(row[col], row[col])
        for col in ("Option1 Value", "Option2 Value", "Option3 Value"):
            if row[col].strip():
                row[col] = OPTION_VALUES_DE.get(row[col], row[col])
        for col in PRICE_COLUMNS:
            row[col] = bump_price(row[col])

    with open(DST, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Zeilen: %d | Produkte: %d" % (len(rows), len(PRODUCTS)))


if __name__ == "__main__":
    main()
