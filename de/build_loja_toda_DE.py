# -*- coding: utf-8 -*-
"""Baut EINE Import-Datei, die den Shop vollstaendig auf Deutsch bringt.

Teil 1 – die 197 noch spanischen Produkte: vollstaendig deutscher Inhalt
         (Titel, Beschreibung, Produkttyp, Tags, Optionsnamen und -werte),
         aber mit den ORIGINAL-HANDLES. Ein Import aktualisiert damit die
         bestehenden Produkte, statt Duplikate anzulegen.

Teil 2 – Produkte, deren Text bereits deutsch ist, deren Optionsnamen aber
         noch englisch sind (Size / Style / Model). Dort wird nur der
         Optionsname uebersetzt, alles andere bleibt unveraendert.
"""
import csv
import sys

STORE = sys.argv[1]
DST = sys.argv[2]

U = '/root/.claude/uploads/51dc155a-661e-5cfe-b886-c70074f25584/'

# (spanische Quelle, bereits uebersetzte Fassung) – zeilengleich
PAIRS = [
    (U + '840e09c9-products_export_1_16.csv', 'products_export_DE.csv'),
    (U + '01ea28d5-products_export.csv',      'tischlaeufer_export_DE.csv'),
    (U + '90f5a4ea-products_export.csv',      'reisetaschen_export_DE.csv'),
    (U + '1e218f67-products_export_1_18.csv', 'lampen_schmetterling_export_DE.csv'),
    (U + '09597f72-products_export_1_19.csv', 'lampen_deko_export_DE.csv'),
    (U + '123623b9-products_export_1_20.csv', 'tassen_export_DE.csv'),
    ('_src50.csv',                            'restantes50_export_DE.csv'),
]

# Optionsnamen, die der Kunde sieht. "Title" ist ein Shopify-Systemwert und bleibt.
OPTION_NAMES_DE = {
    'Tamaño': 'Größe', 'Diseño': 'Design', 'Estilo': 'Stil', 'Oferta': 'Angebot',
    'Size': 'Größe', 'Style': 'Stil', 'Model': 'Modell', 'Modelle': 'Modell',
}


def read(path):
    with open(path, encoding='utf-8-sig', newline='') as fh:
        reader = csv.DictReader(fh)
        return reader.fieldnames, list(reader)


def main():
    fieldnames, store = read(STORE)
    store_by_handle = {}
    for row in store:
        store_by_handle.setdefault(row['Handle'], []).append(row)

    out = []
    handled = set()

    # ---- Teil 1: spanische Produkte, deutscher Inhalt, Original-Handle ----
    for src_path, de_path in PAIRS:
        _, src = read(src_path)
        _, de = read(de_path)
        if len(src) != len(de):
            raise ValueError('%s: %d Quellzeilen, %d uebersetzte Zeilen'
                             % (de_path, len(src), len(de)))
        for src_row, de_row in zip(src, de):
            handle = src_row['Handle']
            if handle not in store_by_handle:
                raise ValueError('Handle nicht im Shop: %r' % handle)
            row = dict(de_row)
            row['Handle'] = handle            # Original-Handle wiederherstellen
            for col in ('Option1 Name', 'Option2 Name', 'Option3 Name'):
                if row[col].strip():
                    row[col] = OPTION_NAMES_DE.get(row[col], row[col])
            out.append(row)
            handled.add(handle)

    part1 = len(handled)

    # ---- Teil 2: deutsche Produkte mit englischem Optionsnamen ----
    needs_option_fix = set()
    option_name = {}
    for row in store:
        for i in (1, 2, 3):
            name = row['Option%d Name' % i].strip()
            if name:
                option_name[(row['Handle'], i)] = name
            current = option_name.get((row['Handle'], i))
            if current in OPTION_NAMES_DE and row['Handle'] not in handled:
                needs_option_fix.add(row['Handle'])

    for handle in store_by_handle:
        if handle not in needs_option_fix:
            continue
        for row in store_by_handle[handle]:
            row = dict(row)
            for col in ('Option1 Name', 'Option2 Name', 'Option3 Name'):
                if row[col].strip():
                    row[col] = OPTION_NAMES_DE.get(row[col], row[col])
            out.append(row)

    with open(DST, 'w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out)

    print('Zeilen: %d | Produkte: %d  (voll uebersetzt: %d, nur Optionsname: %d)'
          % (len(out), part1 + len(needs_option_fix), part1, len(needs_option_fix)))


if __name__ == '__main__':
    main()
