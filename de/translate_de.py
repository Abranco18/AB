# -*- coding: utf-8 -*-
"""Uebersetzt den Shopify-Produktexport (ES -> DE) und erhoeht Preise um 5 EUR."""
import csv
import decimal
import re
import sys

SRC = sys.argv[1]
DST = sys.argv[2]

PRICE_INCREASE = decimal.Decimal("5.00")
PRICE_COLUMNS = ("Variant Price", "Variant Compare At Price")

CLS = 'class="font-claude-response-body break-words whitespace-normal leading-[1.7]"'

BODY_DE = "\n".join([
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

# Handle (ES) -> (neuer Handle DE, Titel DE)
PRODUCTS = {
    "cesta-de-ropa-hecha-a-mano-pradera-primaveral": (
        "handgefertigter-waeschekorb-fruehlingswiese",
        "Handgefertigter Wäschekorb | Frühlingswiese"),
    "camino-de-suenos-de-bluebonnet-cesta-de-ropa-hecha-a-mano": (
        "bluebonnet-traumpfad-handgefertigter-waeschekorb",
        "Bluebonnet-Traumpfad | Handgefertigter Wäschekorb"),
    "serenidad-del-arroyo-de-montana-cesta-de-ropa-hecha-a-mano": (
        "bergbach-idylle-handgefertigter-waeschekorb",
        "Bergbach-Idylle | Handgefertigter Wäschekorb"),
    "sueno-de-girasol-cesta-de-ropa-acolchada": (
        "sonnenblumentraum-gesteppter-waeschekorb",
        "Sonnenblumentraum | Gesteppter Wäschekorb"),
    "cesta-de-ropa-huellas-de-oso-cesta-de-lavanderia-hecha-a-mano": (
        "waeschekorb-baerenspuren-handgefertigt",
        "Wäschekorb Bärenspuren | Handgefertigter Wäschekorb"),
    "cesta-de-ropa-acogedora-cesta-de-lavanderia-hecha-a-mano-ol": (
        "gemuetlicher-waeschekorb-handgefertigt-ol",
        "Gemütlicher Wäschekorb | Handgefertigter Wäschekorb"),
    "jardin-literario-cesta-de-ropa-hecha-a-mano": (
        "literarischer-garten-handgefertigter-waeschekorb",
        "Literarischer Garten | Handgefertigter Wäschekorb"),
    "western-spirit-cesta-de-ropa-hecha-a-mano": (
        "western-spirit-handgefertigter-waeschekorb",
        "Western Spirit | Handgefertigter Wäschekorb"),
    "perros-coloridos-cesta-de-ropa-hecha-a-mano": (
        "bunte-hunde-handgefertigter-waeschekorb",
        "Bunte Hunde | Handgefertigter Wäschekorb"),
    "perros-felices-cesta-de-ropa-hecha-a-mano": (
        "glueckliche-hunde-handgefertigter-waeschekorb",
        "Glückliche Hunde | Handgefertigter Wäschekorb"),
    "calma-costera-cesta-de-ropa-hecha-a-mano": (
        "kuestenruhe-handgefertigter-waeschekorb",
        "Küstenruhe | Handgefertigter Wäschekorb"),
    "carnaval-de-gatos-acogedor-cesta-de-ropa-hecha-a-mano": (
        "gemuetlicher-katzenkarneval-handgefertigter-waeschekorb",
        "Gemütlicher Katzenkarneval | Handgefertigter Wäschekorb"),
    "encanto-de-perro-dorado-cesta-de-ropa-hecha-a-mano": (
        "goldiger-hundezauber-handgefertigter-waeschekorb",
        "Goldiger Hundezauber | Handgefertigter Wäschekorb"),
    "sol-radiante-cesta-de-ropa-hecha-a-mano": (
        "strahlende-sonne-handgefertigter-waeschekorb",
        "Strahlende Sonne | Handgefertigter Wäschekorb"),
    "gato-ingenioso-cesta-de-ropa-hecha-a-mano": (
        "schlaue-katze-handgefertigter-waeschekorb",
        "Schlaue Katze | Handgefertigter Wäschekorb"),
    "espuma-de-mar-suave-cesta-de-ropa-hecha-a-mano": (
        "sanfte-meeresgischt-handgefertigter-waeschekorb",
        "Sanfte Meeresgischt | Handgefertigter Wäschekorb"),
    "sunburst-de-pradera-cesta-de-ropa-hecha-a-mano": (
        "wiesen-sonnenstrahl-handgefertigter-waeschekorb",
        "Wiesen-Sonnenstrahl | Handgefertigter Wäschekorb"),
    "desfile-de-dachshund-cesta-de-ropa-hecha-a-mano": (
        "dackelparade-handgefertigter-waeschekorb",
        "Dackelparade | Handgefertigter Wäschekorb"),
    "sueter-rey-carlos-cesta-de-ropa-hecha-a-mano": (
        "king-charles-pullover-handgefertigter-waeschekorb",
        "King-Charles-Pullover | Handgefertigter Wäschekorb"),
    "arbol-de-la-vida-cesta-de-ropa-hecha-a-mano": (
        "baum-des-lebens-handgefertigter-waeschekorb",
        "Baum des Lebens | Handgefertigter Wäschekorb"),
    "ficcion-escape-cesta-de-ropa-hecha-a-mano": (
        "buecherflucht-handgefertigter-waeschekorb",
        "Bücherflucht | Handgefertigter Wäschekorb"),
    "cesta-acolchada-de-tortuga-cesta-hecha-a-mano": (
        "gesteppter-schildkroeten-waeschekorb-handgefertigt",
        "Gesteppter Schildkröten-Wäschekorb | Handgefertigter Korb"),
    "cesta-de-ropa-hecha-a-mano-pradera-primaveral-8x": (
        "handgefertigter-waeschekorb-fruehlingswiese-8x",
        "Handgefertigter Wäschekorb | Frühlingswiese"),
    "cesta-acolchada-para-gatos-cesta-hecha-a-mano": (
        "gesteppter-katzen-waeschekorb-handgefertigt",
        "Gesteppter Katzen-Wäschekorb | Handgefertigter Korb"),
    "cesta-de-ropa-hecha-a-mano-girasol-en-flor": (
        "handgefertigter-waeschekorb-sonnenblumenbluete",
        "Handgefertigter Wäschekorb | Sonnenblumenblüte"),
    "cesta-de-ropa-hecha-a-mano-cancion-del-prado": (
        "handgefertigter-waeschekorb-wiesenlied",
        "Handgefertigter Wäschekorb | Wiesenlied"),
    "arbol-de-la-vida-cesto-de-ropa-hecho-a-mano": (
        "lebensbaum-handgefertigter-waeschekorb",
        "Lebensbaum | Handgefertigter Wäschekorb"),
    "pradera-brillante-cesta-de-ropa-hecha-a-mano": (
        "leuchtende-wiese-handgefertigter-waeschekorb",
        "Leuchtende Wiese | Handgefertigter Wäschekorb"),
    "mountain-view-cesto-de-ropa-hecho-a-mano": (
        "bergblick-handgefertigter-waeschekorb",
        "Bergblick | Handgefertigter Wäschekorb"),
    "cesta-de-ropa-hecha-a-mano-bloom-bright": (
        "handgefertigter-waeschekorb-bluetenpracht",
        "Handgefertigter Wäschekorb Blütenpracht"),
    "gato-cesta-de-ropa-hecha-a-mano-nt": (
        "katze-handgefertigter-waeschekorb-nt",
        "Katze | Handgefertigter Wäschekorb"),
    "ambiente-maritimo-cesta-de-ropa-hecha-a-mano": (
        "maritimes-ambiente-handgefertigter-waeschekorb",
        "Maritimes Ambiente | Handgefertigter Wäschekorb"),
    "gato-de-bosque-canasta-de-ropa-hecha-a-mano": (
        "waldkatze-handgefertigter-waeschekorb",
        "Waldkatze | Handgefertigter Wäschekorb"),
    "cesta-de-ropa-acogedora-cesta-de-lavanderia-hecha-a-mano": (
        "gemuetlicher-waeschekorb-handgefertigt",
        "Gemütlicher Wäschekorb | Handgefertigter Wäschekorb"),
    "gatos-de-jardin-cesta-de-ropa-hecha-a-mano": (
        "gartenkatzen-handgefertigter-waeschekorb",
        "Gartenkatzen | Handgefertigter Wäschekorb"),
}

TYPE_DE = {"Quilted Laundry Basket": "Gesteppter Wäschekorb"}

OPTION_NAMES_DE = {"Tamaño": "Größe", "Diseño": "Design"}

SIZES_DE = {
    "Pequeña": "Klein", "Pequeño": "Klein",
    "Mediana": "Mittel", "Mediano": "Mittel",
    "Grande": "Groß",
}

# Praefix der Design-Namen (Cesta/Cesto de Ropa/Lavanderia Acolchada/o)
DESIGN_PREFIX = re.compile(
    r"^(?:Cesta|Cesto|Canasta) de (?:Ropa|Lavandería) Acolchad[ao]\s+", re.UNICODE)

DESIGNS_DE = {
    "Jardín Literario": "Literarischer Garten",
    "Flores de Historia": "Geschichtenblüten",
    "Crónica de Flores": "Blütenchronik",
    "Biblioteca en Flor": "Blühende Bibliothek",
    "Cuentos de Pétalos": "Blütenblatt-Geschichten",
    "Pradera de Primavera": "Frühlingswiese",
    "Pradera de Primavera 1": "Frühlingswiese 1",
    "Pradera de Primavera 2": "Frühlingswiese 2",
    "Pradera Brillante 3": "Leuchtende Wiese 3",
    "Sol de Pradera": "Wiesensonne",
    "Flor de Pradera": "Wiesenblüte",
    "Picos Dorados": "Goldene Gipfel",
    "Brillo del Sol": "Sonnenglanz",
    "Amanecer del Desierto": "Wüstenmorgen",
    "Brillo del Bosque": "Waldglanz",
    "Bosque Antiguo": "Alter Wald",
    "Espíritu del Bosque": "Waldgeist",
    "Brillo del Árbol": "Baumglanz",
    "Raíces de la Naturaleza": "Wurzeln der Natur",
    "Raíces Doradas": "Goldene Wurzeln",
    "Árbol Sagrado": "Heiliger Baum",
    "Luz enraizada": "Verwurzeltes Licht",
    "de Ánimo Marítimo": "Maritime Stimmung",
    "Espíritu del Mar": "Geist des Meeres",
    "Lenta y Serena": "Langsam und Gelassen",
    "Brillo de Concha": "Muschelglanz",
    "Viajero Pequeño": "Kleiner Reisender",
    "Encantadora": "Bezaubernd",
    "Reloj de Lirio": "Lilienuhr",
    "Bigotes de Medianoche": "Mitternachts-Schnurrhaare",
    "Patas Estrelladas": "Sternenpfoten",
    "Libros Durmiendo": "Schlafende Bücher",
    "con Gato Blanco Encantadora": "mit bezaubernder weißer Katze",
    "Páginas Ronroneantes": "Schnurrende Seiten",
    "Gatos Encantados": "Verzauberte Katzen",
    "Raíces Eternas": "Ewige Wurzeln",
    "Árbol Místico": "Mystischer Baum",
    "Bosque Sagrado": "Heiliger Wald",
    "Roble Celestial": "Himmlische Eiche",
    "Horizonte Brillante": "Leuchtender Horizont",
    "Gloria de la Mañana": "Morgenpracht",
    "Horizonte Dorado": "Goldener Horizont",
    "Gato del Carnaval Acogedor": "Gemütlicher Karnevalskater",
    "Pradera de Medianoche": "Mitternachtswiese",
    "Compañía Perfecta": "Perfekte Gesellschaft",
    "La Multitud de Gatos": "Die Katzenschar",
    "Encuentro de Maullidos": "Miau-Treffen",
    "Gatos en Flor": "Katzen in Blüte",
}

# Artikelcodes am Ende eines Design-Namens (z. B. NCU0PVL619) bleiben erhalten
CODE_SUFFIX = re.compile(r"\s+([A-Z0-9]{8,})$")


def translate_design(value):
    """'Cesta de Ropa Acolchada Jardin Literario' -> 'Gesteppter Waeschekorb Literarischer Garten'."""
    rest = DESIGN_PREFIX.sub("", value.strip())
    if rest == value.strip():
        raise ValueError("Unbekanntes Design-Praefix: %r" % value)
    code = ""
    m = CODE_SUFFIX.search(rest)
    if m:
        code = " " + m.group(1)
        rest = rest[:m.start()]
    try:
        name = DESIGNS_DE[rest]
    except KeyError:
        raise ValueError("Unbekannter Design-Name: %r" % rest)
    return "Gesteppter Wäschekorb %s%s" % (name, code)


def bump_price(value):
    if not value.strip():
        return value
    new = decimal.Decimal(value) + PRICE_INCREASE
    return "%.2f" % new


def main():
    with open(SRC, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames
        rows = list(reader)

    design_cache = {}
    for row in rows:
        handle = row["Handle"]
        if handle not in PRODUCTS:
            raise ValueError("Unbekannter Handle: %r" % handle)
        new_handle, new_title = PRODUCTS[handle]
        row["Handle"] = new_handle
        if row["Title"].strip():
            row["Title"] = new_title
            row["Body (HTML)"] = BODY_DE
            row["Type"] = TYPE_DE.get(row["Type"], row["Type"])

        for col in ("Option1 Name", "Option2 Name", "Option3 Name"):
            if row[col].strip():
                row[col] = OPTION_NAMES_DE.get(row[col], row[col])

        if row["Option1 Value"].strip():
            row["Option1 Value"] = SIZES_DE[row["Option1 Value"]]

        val = row["Option2 Value"].strip()
        if val:
            if val not in design_cache:
                design_cache[val] = translate_design(val)
            row["Option2 Value"] = design_cache[val]

        for col in PRICE_COLUMNS:
            row[col] = bump_price(row[col])

    with open(DST, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Zeilen: %d | Produkte: %d | Designs: %d" % (len(rows), len(PRODUCTS), len(design_cache)))


if __name__ == "__main__":
    main()
