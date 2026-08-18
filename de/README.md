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
