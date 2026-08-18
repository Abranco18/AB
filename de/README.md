# Deutsche Kollektion – Wäschekörbe (Emma Frankfurt)

`products_export_DE.csv` ist die deutsche Fassung des spanischen Shopify-Exports
(35 Produkte, 228 Varianten-Zeilen), erzeugt mit `translate_de.py`.

## Was übersetzt wurde
- `Handle` – neue deutsche URL-Slugs (ohne Umlaute, eindeutig)
- `Title`
- `Body (HTML)` – identische HTML-Struktur und CSS-Klassen wie im Original
- `Type` – „Quilted Laundry Basket“ → „Gesteppter Wäschekorb“
- `Option1 Name` „Tamaño“ → „Größe“, Werte → Klein / Mittel / Groß
- `Option2 Name` „Diseño“ → „Design“, alle 49 Design-Namen übersetzt
  (Artikelcodes wie `NCU0PVL619` bleiben unverändert)

## Was bewusst unverändert bleibt
- `Tags` – bereits englische Keywords, dienen Collection-Regeln und Suche
- `Vendor` (Emma Frankfurt), `Variant SKU`, Bild-URLs, Bestands- und Versandfelder

## Preise
`Variant Price` und `Variant Compare At Price` je +5,00 €:

| Variant Price | alt → neu | Compare At | alt → neu |
|---|---|---|---|
| Klein  | 34.95 → 39.95 / 39.95 → 44.95 | | 114.95 → 119.95 |
| Mittel | 39.95 → 44.95 / 44.95 → 49.95 | | 134.95 → 139.95 |
| Groß   | 44.95 → 49.95 / 49.95 → 54.95 | | 134.99 → 139.99 |
| | | | 150.00 → 155.00 |
| | | | 164.99 → 169.99 |

## Erneut ausführen
```
python3 de/translate_de.py <spanischer-export.csv> de/products_export_DE.csv
```

---

# Deutsche Kollektion – Tischläufer (Emma Frankfurt)

`tischlaeufer_export_DE.csv` ist die deutsche Fassung des zweiten spanischen Exports
(39 Produkte, 124 Zeilen, je 3 Größen S/M/L), erzeugt mit `translate_tischlaeufer_de.py`.

## Was übersetzt wurde
- `Handle` – neue Slugs nach dem Schema `gesteppter-tischlaeufer-<motiv>`
- `Title` – „Gesteppter Tischläufer - <Motiv>“, alle 39 Motivnamen übersetzt
- `Body (HTML)` – identische HTML-Struktur (`<p>`, `<ul>`, `<li>`, `<br>`) wie im Original
- `Tags` – „Mantelería“ → „Tischwäsche“
- `Option1 Name` „Tamaño“ → „Größe“; Maßangaben unverändert, nur das Trennzeichen
  zu „×“ vereinheitlicht (die Quelle mischte „x“ und „×“)

## Was bewusst unverändert bleibt
- `Vendor` (Emma Frankfurt), `Variant SKU`, Bild-URLs, Bestands- und Versandfelder
- Der Lieferantenname „Jetiy“ in der Materialbeschreibung
- Die L-Variante hat auch im Original keine SKU

## Preise
`Variant Price` und `Variant Compare At Price` je +5,00 €:

| Größe | Preis alt → neu | Compare At alt → neu |
|---|---|---|
| S (36 × 122 cm) | 39.95 → 44.95 | 134.95 → 139.95 |
| M (36 × 183 cm) | 44.95 → 49.95 | 149.95 → 154.95 |
| L (36 × 275 cm) | 49.95 → 54.95 | 164.95 → 169.95 |

## Erneut ausführen
```
python3 de/translate_tischlaeufer_de.py <spanischer-export.csv> de/tischlaeufer_export_DE.csv
```

---

# Deutsche Kollektion – Reisetaschen (Emma Frankfurt)

`reisetaschen_export_DE.csv` ist die deutsche Fassung des dritten spanischen Exports
(50 Produkte, 95 Zeilen), erzeugt mit `translate_reisetaschen_de.py`.

## Besonderheit
Jede Beschreibung enthält ein eigenes eingebettetes Produktbild (`<img>`).
Das Skript übernimmt pro Produkt genau dessen Bild-URL in den deutschen Text.
Es gibt zwei Textvarianten, die in der Quelle unterschiedlich positioniert sind:
- **Reise** (47 Produkte) – Wochenendtrip
- **Alltag** (3 Produkte: Wilma, Fern, Veronica)

## Was übersetzt wurde
- `Handle` – `<name>-handgefertigte-weiche-reisetasche`, Vorname bleibt erhalten
- `Title` – `<Name> | Handgefertigte weiche Reisetasche`
- `Body (HTML)` – gleiche Struktur (`<h3>`, `<p>`, `<strong>`, ✔-Abschnitte);
  `<meta charset>`- und `data-start`/`data-end`-Reste aus der Quelle entfernt
- `Type` – „bag“/„Bags“ vereinheitlicht zu „Reisetasche“
- `Option1 Name` „Tamaño“ → „Größe“; „Paisaje“ → „Querformat“, „W“ → „B“,
  Dezimalkomma statt Punkt. Die Maßzahlen selbst sind unverändert.

## Was bewusst unverändert bleibt
- Die Vornamen der Produkte (Joan, Grace, …), auch die spanisch lokalisierten
  (Ámbar, Jazmín, Fe, Adelaida, Clementina)
- `Vendor`, Bild-URLs, Bestands- und Versandfelder; `Tags` sind in der Quelle leer

## Preise
`Variant Price` und `Variant Compare At Price` je +5,00 €:

| Preis alt → neu | Compare At alt → neu |
|---|---|
| 39.95 → 44.95 | 134.99 → 139.99 |
| 44.95 → 49.95 | 150.00 → 155.00 |

## Erneut ausführen
```
python3 de/translate_reisetaschen_de.py <spanischer-export.csv> de/reisetaschen_export_DE.csv
```
