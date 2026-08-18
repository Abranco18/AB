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

---

# Deutsche Kollektionen – Lampen und Tassen

Diese drei Exporte enthalten – anders als die Körbe, Tischläufer und Taschen –
**pro Produkt eine eigene Beschreibung**. Sie sind einzeln übersetzt, nicht über
eine gemeinsame Vorlage erzeugt. Eingebettete `<img>`-Tags übernehmen die Skripte
unverändert in Reihenfolge aus der Quelle (Platzhalter `{IMG1}`, `{IMG2}` …), damit
keine Bild-URL von Hand abgeschrieben wird.

## `lampen_schmetterling_export_DE.csv` (6 Produkte, Tag PR3760)
`translate_lampen_pr3760_de.py`. Titel, Beschreibung und `Type`
(„Handmade Butterfly Lamps“ → „Handgefertigte Schmetterlingslampen“) übersetzt.
Preise 94.95 → 99.95, Compare At 198.95 → 203.95.

## `lampen_deko_export_DE.csv` (7 Produkte, 14 Zeilen, Tag PR3759)
`translate_lampen_pr3759_de.py`. Preise 34.95 → 39.95 / 39.95 → 44.95,
Compare At 98.97 → 103.97.

## `tassen_export_DE.csv` (10 Produkte, 28 Zeilen, Tag NM0053)
`translate_tassen_de.py`. Zusätzlich übersetzt: Optionsnamen „Estilo“ → „Stil“,
„Oferta“ → „Angebot“; Optionswerte „1x Taza“ → „1x Tasse“, „Ágata“ → „Achat“,
„Rojo volcánico“ → „Vulkanrot“, „Amatista“ → „Amethyst“.
Preise 24.95–69.95 → 29.95–74.95, Compare At 99.95–299.95 → 104.95–304.95.

### Offene Punkte in der Quelle (nicht stillschweigend geändert)
- **„Menos azul“ / „Menos verde“** (Farbvarianten der Mineralkristall-Tassen) sind
  schon im Spanischen unklar; wörtlich als „Weniger Blau“ / „Weniger Grün“ übersetzt.
  Sobald die echten Farbnamen bekannt sind, in `OPTION_VALUES_DE` anpassen.
- **Fremde Markennamen** im Fließtext der Quelle („Solymall Book Mug“, „Clara San
  Diego“) wurden in der deutschen Fassung durch neutrale Formulierungen ersetzt.
- **Rabattzeile „70 % sparen“** ist übernommen, stimmt aber nicht für jedes Produkt.
- Zwei Beschreibungen betten Bilder von **fremden Domains** ein
  (`ivy-cambridge.co.uk`, `ucarecdn.com`, `d1y4tm6t3pzfj.cloudfront.net`).

## Bereits erledigt
`products_export_1_17.csv` ist byte-identisch mit dem ersten Export
(`products_export_1_16.csv`) – die deutsche Fassung ist `products_export_DE.csv`.

## Erneut ausführen
```
python3 de/translate_lampen_pr3760_de.py <export.csv> de/lampen_schmetterling_export_DE.csv
python3 de/translate_lampen_pr3759_de.py <export.csv> de/lampen_deko_export_DE.csv
python3 de/translate_tassen_de.py        <export.csv> de/tassen_export_DE.csv
```

---

# Audit des Gesamtkatalogs (products_export_1_22.csv, 610 Produkte)

Sprachprüfung des vollständigen Shop-Exports: **413 Produkte auf Deutsch (68 %),
197 auf Spanisch (32 %)**. Die spanischen zerfallen in zwei getrennte Fälle:

## 1. `AUDIT_duplicados_ES_a_apagar.csv` – 147 Duplikate
Beim Import der deutschen Dateien hat Shopify wegen der neuen Handles **neue
Produkte angelegt statt der bestehenden zu aktualisieren**. Die spanischen
Originale sind also weiterhin im Shop, parallel zu den deutschen Fassungen:

| Kollektion | ES-Originale noch im Shop | DE-Fassungen angelegt |
|---|---|---|
| Wäschekörbe | 35 | 35 |
| Tischläufer | 39 | 39 |
| Reisetaschen | 50 | 50 |
| Schmetterlingslampen | 6 | 6 |
| Deko-Lampen | 7 | 7 |
| Tassen | 10 | 10 |
| **Summe** | **147** | **147** |

Die Datei listet Kollektion, ES-Handle und aktuellen Titel – Grundlage zum
Löschen der Duplikate im Shopify-Admin.

Alternative: die sechs DE-Dateien mit den **ursprünglichen spanischen Handles**
neu erzeugen; dann aktualisiert ein Import die bestehenden Produkte, statt neue
anzulegen (die bereits angelegten deutschen Produkte müssten dann gelöscht werden).

## 2. `AUDIT_por_traduzir.csv` – 50 noch nicht übersetzte Produkte
Diese Produkte waren in keinem der bisher gelieferten Exporte enthalten:

| Gruppe | Anzahl |
|---|---|
| Reisetaschen (Jade, Tiffany, Oceane …) | 27 |
| Tiffany-Lampen (Tag `LAMPS`: SOLELIA, AZURIA, SOLINA …) | 20 |
| Schmetterlingslampe TIFFALIGHT | 1 |
| Tischläufer „Menorah Iluminada“ | 1 |
| Wäschekorb „Encanto de las Tierras Altas“ | 1 |

Spalten: Handle, Titel, Type, Tags, Variant Price, Compare At Price.
