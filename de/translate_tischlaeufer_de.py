# -*- coding: utf-8 -*-
"""Uebersetzt den Tischlaeufer-Export (ES -> DE) und erhoeht die Preise um 5 EUR."""
import csv
import decimal
import sys

SRC = sys.argv[1]
DST = sys.argv[2]

PRICE_INCREASE = decimal.Decimal("5.00")
PRICE_COLUMNS = ("Variant Price", "Variant Compare At Price")

BODY_DE = "\n".join([
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

# Handle (ES) -> Motiv (DE).  Titel und Handle werden daraus gebildet.
MOTIFS = {
    "camino-de-mesa-acolchado-jardin-en-flores": ("Blühender Garten", "bluehender-garten"),
    "camino-de-mesa-acolchado-magnolia-tranquila": ("Stille Magnolie", "stille-magnolie"),
    "camino-de-mesa-acolchado-jardin-de-girasoles": ("Sonnenblumengarten", "sonnenblumengarten"),
    "camino-de-mesa-acolchado-flores-de-frangipani": ("Frangipani-Blüten", "frangipani-blueten"),
    "camino-de-mesa-acolchado-corazones-y-rosas": ("Herzen und Rosen", "herzen-und-rosen"),
    "camino-de-mesa-acolchado-sueno-de-carpas-koi": ("Koi-Traum", "koi-traum"),
    "camino-de-mesa-acolchado-temporada-de-calabazas": ("Kürbiszeit", "kuerbiszeit"),
    "camino-de-mesa-acolchado-gracia-divina": ("Göttliche Gnade", "goettliche-gnade"),
    "camino-de-mesa-acolchado-familia-de-osos-negros": ("Schwarzbärenfamilie", "schwarzbaerenfamilie"),
    "camino-de-mesa-acolchado-abundancia-de-otono": ("Herbstfülle", "herbstfuelle"),
    "camino-de-mesa-acolchado-corazones-calidos": ("Warme Herzen", "warme-herzen"),
    "camino-de-mesa-acolchado-paisaje-de-pinos-nevados": ("Verschneite Kiefernlandschaft", "verschneite-kiefernlandschaft"),
    "camino-de-mesa-acolchado-arte-ecuestre": ("Pferdekunst", "pferdekunst"),
    "camino-de-mesa-acolchado-estrella-de-belen": ("Stern von Bethlehem", "stern-von-bethlehem"),
    "camino-de-mesa-acolchado-cascabeles-festivos": ("Festliche Glöckchen", "festliche-gloeckchen"),
    "camino-de-mesa-acolchado-sendero-de-petalos": ("Blütenblattpfad", "bluetenblattpfad"),
    "camino-de-mesa-acolchado-camino-helado": ("Frostiger Pfad", "frostiger-pfad"),
    "camino-de-mesa-acolchado-serenata-de-lupinos": ("Lupinenserenade", "lupinenserenade"),
    "camino-de-mesa-acolchado-carrera-de-pavos": ("Truthahnrennen", "truthahnrennen"),
    "camino-de-mesa-acolchado-rojo-cardenal": ("Kardinalrot", "kardinalrot"),
    "camino-de-mesa-acolchado-girasoles-de-otono": ("Herbstsonnenblumen", "herbstsonnenblumen"),
    "camino-de-mesa-acolchado-calabaza-especiada": ("Gewürzkürbis", "gewuerzkuerbis"),
    "camino-de-mesa-acolchado-bosque-de-esmeralda": ("Smaragdwald", "smaragdwald"),
    "camino-de-mesa-acolchado-desfile-de-calabazas": ("Kürbisparade", "kuerbisparade"),
    "camino-de-mesa-acolchado-arbol-celta": ("Keltischer Baum", "keltischer-baum"),
    "camino-de-mesa-acolchado-corazones-en-flor": ("Herzen in Blüte", "herzen-in-bluete"),
    "camino-de-mesa-acolchado-cascada-de-corazones": ("Herzenkaskade", "herzenkaskade"),
    "camino-de-mesa-acolchado-mascaras-de-carnaval": ("Karnevalsmasken", "karnevalsmasken"),
    "camino-de-mesa-acolchado-marcha-de-los-elefantes": ("Elefantenmarsch", "elefantenmarsch"),
    "camino-de-mesa-acolchado-gracia-en-flores": ("Blütenanmut", "bluetenanmut"),
    "camino-de-mesa-acolchado-caballo-al-galope": ("Galoppierendes Pferd", "galoppierendes-pferd"),
    "camino-de-mesa-acolchado-alas-escarlatas": ("Scharlachrote Flügel", "scharlachrote-fluegel"),
    "camino-de-mesa-acolchado-desfile-de-gallos": ("Hahnenparade", "hahnenparade"),
    "camino-de-mesa-acolchado-esplendor-artico": ("Arktische Pracht", "arktische-pracht"),
    "camino-de-mesa-acolchado-espiritu-celta": ("Keltischer Geist", "keltischer-geist"),
    "camino-de-mesa-acolchado-luz-de-belen": ("Licht von Bethlehem", "licht-von-bethlehem"),
    "camino-de-mesa-acolchado-belleza-estrellada": ("Sternenschönheit", "sternenschoenheit"),
    "camino-de-mesa-acolchado-alegria-de-halloween": ("Halloween-Freude", "halloween-freude"),
    "camino-de-mesa-acolchado-flor-de-magnolia-rustica": ("Rustikale Magnolienblüte", "rustikale-magnolienbluete"),
}

TITLE_PREFIX = "Gesteppter Tischläufer - "
HANDLE_PREFIX = "gesteppter-tischlaeufer-"

TAGS_DE = {"Mantelería": "Tischwäsche"}

OPTION_NAMES_DE = {"Tamaño": "Größe"}

# Groessen: Buchstabe + Masse bleiben, das "x" wird zu "×" vereinheitlicht
SIZES_DE = {
    "S (36 cm x 122 cm)": "S (36 cm × 122 cm)",
    "M (36 cm × 183 cm)": "M (36 cm × 183 cm)",
    "L (36 cm × 275 cm)": "L (36 cm × 275 cm)",
}


def translate_tags(value):
    parts = [p.strip() for p in value.split(",") if p.strip()]
    return ", ".join(TAGS_DE.get(p, p) for p in parts)


def bump_price(value):
    if not value.strip():
        return value
    return "%.2f" % (decimal.Decimal(value) + PRICE_INCREASE)


def main():
    with open(SRC, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames
        rows = list(reader)

    for row in rows:
        handle = row["Handle"]
        if handle not in MOTIFS:
            raise ValueError("Unbekannter Handle: %r" % handle)
        motif_de, slug = MOTIFS[handle]
        row["Handle"] = HANDLE_PREFIX + slug

        if row["Title"].strip():
            row["Title"] = TITLE_PREFIX + motif_de
            row["Body (HTML)"] = BODY_DE
            row["Tags"] = translate_tags(row["Tags"])

        for col in ("Option1 Name", "Option2 Name", "Option3 Name"):
            if row[col].strip():
                row[col] = OPTION_NAMES_DE.get(row[col], row[col])

        if row["Option1 Value"].strip():
            row["Option1 Value"] = SIZES_DE[row["Option1 Value"]]

        for col in PRICE_COLUMNS:
            row[col] = bump_price(row[col])

    with open(DST, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Zeilen: %d | Produkte: %d" % (len(rows), len(MOTIFS)))


if __name__ == "__main__":
    main()
