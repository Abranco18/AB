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

---

# `restantes50_export_DE.csv` – die 50 fehlenden Produkte

Erzeugt mit `translate_falta50_de.py` aus den 50 Produkten, die das Katalog-Audit
noch auf Spanisch gefunden hat (131 Zeilen). Vier Gruppen:

| Gruppe | Anzahl | Vorlage |
|---|---|---|
| Lampen (20x Tag `LAMPS` + TIFFALIGHT) | 21 | je einzeln übersetzt |
| Reisetaschen (Jade, Tiffany, Oceane …) | 27 | wie `reisetaschen_export_DE.csv` |
| Tischläufer „Leuchtende Menora“ | 1 | wie `tischlaeufer_export_DE.csv` |
| Wäschekorb „Zauber der Highlands“ | 1 | wie `products_export_DE.csv` |

Preise: `Variant Price` und `Variant Compare At Price` je +5,00 € (u. a.
94.95 → 99.95 und 239.95 → 244.95 bei den Lampen).

Der Wäschekorb hat zusätzlich `Option2` („Diseño“ → „Design“) mit fünf
Designnamen, die ebenfalls übersetzt sind (Zauber der Highlands, Gemütliches
Kälbchen, Highland-Blumen, Highland-Blüte, Highland-Abendrot).

### Offene Punkte in der Quelle
- **MOSAICRA** trägt im spanischen Text durchgehend die Beschreibung der Lampe
  **Ivorya** („Ivorya Luxury Baroque Table“) – ein Copy-Paste-Fehler. Die deutsche
  Fassung beschreibt die Mosaiklampe, nicht Ivorya.
- Zwei Produkte heißen beide **AURELIA**; sie sind über Untertitel und Handle
  unterschieden („Glaslampe im Alte-Welt-Stil“ / „Vintage-Tischlampe im Barockstil“).

## Erneut ausführen
```
python3 de/translate_falta50_de.py <die-50-spanischen-zeilen.csv> de/restantes50_export_DE.csv
```

---

# `tischlaeufer_titel_DE.csv` – nur die Titel

Erzeugt mit `translate_titel_tischlaeufer.py` aus dem Shop-Export der 39
Tischläufer (124 Zeilen). **Es ist ausschließlich die Spalte `Title` geändert** –
alle übrigen 58 Spalten sind Zeichen für Zeichen identisch mit dem Export.

Wichtig: die **Handles bleiben die spanischen Originale**. Dadurch aktualisiert
ein Import die bestehenden Produkte, statt neue anzulegen – anders als bei
`tischlaeufer_export_DE.csv`, das deutsche Handles verwendet und deshalb
Duplikate erzeugt hat.

Die Motivnamen sind dieselben wie in `tischlaeufer_export_DE.csv`, damit die
Benennung im Shop konsistent bleibt.

Noch auf Spanisch in diesen Produkten: `Body (HTML)`, `Option1 Name` („Tamaño“)
und `Tags` („Mantelería“).

## Erneut ausführen
```
python3 de/translate_titel_tischlaeufer.py <shop-export.csv> de/tischlaeufer_titel_DE.csv
```

---

# `loja_toda_DE.csv` – der komplette Shop auf Deutsch, ohne Duplikate

Erzeugt mit `build_loja_toda_DE.py` aus dem vollständigen Shop-Export
(660 Produkte). **305 Produkte / 931 Zeilen.** Die Datei verwendet
ausschließlich **bestehende Handles** – ein Import aktualisiert die Produkte,
er legt keine neuen an.

| Teil | Produkte | Was geändert wird |
|---|---|---|
| Noch spanische Produkte | 197 | Titel, Beschreibung, Produkttyp, Tags, Optionsnamen und -werte + Preise +5 € |
| Deutscher Text, englischer Optionsname | 108 | nur `Size`/`Style`/`Model` → `Größe`/`Stil`/`Modell`; Preise unverändert |

## Warum es beim ersten Mal schiefging
Die früheren Dateien (`products_export_DE.csv` usw.) trugen **deutsche
Handles**. Der Handle ist in Shopify der Schlüssel: bei einem Import mit neuem
Handle wird ein **neues Produkt angelegt**, das bestehende bleibt unverändert.
So entstanden 197 deutsche Dubletten, während die spanischen Originale weiter
im Shop standen – und da nur die Originale den Collections zugeordnet sind,
zeigte die Storefront weiterhin Spanisch.

`loja_toda_DE.csv` behält deshalb die Original-Handles bei.

## Reihenfolge
1. `loja_toda_DE.csv` importieren (Overwrite aktivieren)
2. Die 197 deutschen Dubletten löschen – Liste in `APAGAR_duplicados_DE.csv`

## Erneut ausführen
```
python3 de/build_loja_toda_DE.py <shop-export.csv> de/loja_toda_DE.csv
```
