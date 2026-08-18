# -*- coding: utf-8 -*-
"""Uebersetzt den Reisetaschen-Export (ES -> DE) und erhoeht die Preise um 5 EUR.

Besonderheit dieser Kollektion: jede Beschreibung enthaelt ein eigenes
eingebettetes Produktbild (<img>), das pro Produkt uebernommen wird.
Ausserdem gibt es zwei Textvarianten: Reise (47 Produkte) und Alltag (3).
"""
import csv
import decimal
import re
import sys

SRC = sys.argv[1]
DST = sys.argv[2]

PRICE_INCREASE = decimal.Decimal("5.00")
PRICE_COLUMNS = ("Variant Price", "Variant Compare At Price")

HANDLE_SUFFIX_ES = "-bolsa-de-viaje-suave-hecha-a-mano"
HANDLE_SUFFIX_DE = "-handgefertigte-weiche-reisetasche"
TITLE_SUFFIX_DE = " | Handgefertigte weiche Reisetasche"

TYPE_DE = "Reisetasche"          # vereinheitlicht die Quellwerte "bag" / "Bags"
OPTION_NAMES_DE = {"Tamaño": "Größe"}

SIZES_DE = {
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

# Textvariante "Alltag" statt "Reise" – erkannt an der Ueberschrift der Quelle
DAILY_MARKER = "ESTILO DIARIO"

BODY_TRAVEL_DE = "\n".join([
    '<h3>MÜHELOSER STIL FÜR DEINE NÄCHSTE AUSZEIT.</h3>',
    '<p>Verlasse das Haus mit allem ordentlich verstaut und griffbereit für deine Kurzreise. '
    'Diese geräumige Reisetasche verleiht deinem Reise-Look eine weiche, bezaubernde Note und '
    'hält deine Essentials für die Übernachtung perfekt organisiert.</p>',
    '<p><img src="{IMG}" alt=""></p>',
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

BODY_DAILY_DE = "\n".join([
    '<h3>ALLTAGSSTIL, DER ALLES MITNIMMT.</h3>',
    '<p>Du gehst aus dem Haus mit allem, was du brauchst – ordentlich verstaut und griffbereit. '
    'Diese Tasche verleiht deinem Look eine weiche, bezaubernde Note und lässt deinen Tag '
    'organisierter wirken.</p>',
    '<p><img src="{IMG}" alt=""></p>',
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

IMG_SRC = re.compile(r'<img[^>]*src="([^"]+)"')


def bump_price(value):
    if not value.strip():
        return value
    return "%.2f" % (decimal.Decimal(value) + PRICE_INCREASE)


def main():
    with open(SRC, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames
        rows = list(reader)

    daily = 0
    for row in rows:
        handle = row["Handle"]
        if not handle.endswith(HANDLE_SUFFIX_ES):
            raise ValueError("Unerwarteter Handle: %r" % handle)
        name_slug = handle[:-len(HANDLE_SUFFIX_ES)]
        row["Handle"] = name_slug + HANDLE_SUFFIX_DE

        if row["Title"].strip():
            name = row["Title"].split("|")[0].strip()
            row["Title"] = name + TITLE_SUFFIX_DE
            row["Type"] = TYPE_DE

            body = row["Body (HTML)"]
            found = IMG_SRC.findall(body)
            if len(found) != 1:
                raise ValueError("%s: erwartet genau 1 <img>, gefunden %d" % (handle, len(found)))
            template = BODY_DAILY_DE if DAILY_MARKER in body else BODY_TRAVEL_DE
            if template is BODY_DAILY_DE:
                daily += 1
            row["Body (HTML)"] = template.replace("{IMG}", found[0])

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

    products = len([r for r in rows if r["Title"].strip()])
    print("Zeilen: %d | Produkte: %d (Reise: %d, Alltag: %d)"
          % (len(rows), products, products - daily, daily))


if __name__ == "__main__":
    main()
