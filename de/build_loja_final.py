# -*- coding: utf-8 -*-
"""Baut die finale Import-Datei: deutscher Text + auf 5 aufgerundete Rabatte.

Der Rabatt-Badge im Theme rechnet floor((compare - price) / compare * 100).
Damit dort eine durch 5 teilbare Zahl steht, wird der Vergleichspreis so
gesetzt, dass der tatsaechliche Rabatt genau den Zielwert erreicht.
Beispiel: 44.95 bei 139.99 = 67 % -> Vergleichspreis 149.95 = 70 %.
"""
import csv
import math
import sys

STORE, MINE, DST = sys.argv[1], sys.argv[2], sys.argv[3]

DE_FILES = ['products_export_DE.csv', 'tischlaeufer_export_DE.csv',
            'reisetaschen_export_DE.csv', 'lampen_schmetterling_export_DE.csv',
            'lampen_deko_export_DE.csv', 'tassen_export_DE.csv',
            'restantes50_export_DE.csv']


def read(path):
    with open(path, encoding='utf-8-sig', newline='') as fh:
        r = csv.DictReader(fh)
        return r.fieldnames, list(r)


def shown(price, compare):
    return math.floor((1 - price / compare) * 100)


def target(pct):
    """1-4 in der Einerstelle -> 5, darueber -> naechster Zehner."""
    return pct if pct % 5 == 0 else (pct // 5 + 1) * 5


def new_compare(price, goal):
    """Kleinster auf .95 endender Betrag, der den Zielrabatt erreicht."""
    need = price / (1 - goal / 100.0)
    c = math.floor(need) + 0.95
    if c < need or shown(price, c) < goal:
        c = math.floor(need) + 1 + 0.95
    return round(c, 2)


def main():
    fieldnames, store = read(STORE)
    _, mine = read(MINE)

    translated = {}
    for row in mine:
        translated.setdefault(row['Handle'], []).append(row)

    # die deutschen Dubletten fliegen raus, sie werden geloescht
    dup = set()
    for f in DE_FILES:
        for row in read(f)[1]:
            dup.add(row['Handle'])

    final, seen = [], set()
    for row in store:
        h = row['Handle']
        if h in translated:
            if h not in seen:
                seen.add(h)
                final.extend(dict(x) for x in translated[h])
        elif h not in dup:
            final.append(dict(row))

    changed_price = set()
    for row in final:
        p, c = row['Variant Price'].strip(), row['Variant Compare At Price'].strip()
        if not p or not c:
            continue
        p, c = float(p), float(c)
        if c <= p or p <= 0:
            continue
        goal = target(shown(p, c))
        if goal == shown(p, c):
            continue
        row['Variant Compare At Price'] = '%.2f' % new_compare(p, goal)
        changed_price.add(row['Handle'])

    # nur Produkte ausgeben, die sich gegenueber dem Shop unterscheiden
    store_by = {}
    for row in store:
        store_by.setdefault(row['Handle'], []).append(row)

    out, products = [], 0
    by_handle = {}
    for row in final:
        by_handle.setdefault(row['Handle'], []).append(row)

    for h, rows in by_handle.items():
        orig = store_by[h]
        if len(orig) != len(rows) or any(a[k] != b[k] for a, b in zip(orig, rows) for k in a):
            out.extend(rows)
            products += 1

    with open(DST, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out)

    print('Zeilen: %d | Produkte zu importieren: %d | davon mit neuem Vergleichspreis: %d'
          % (len(out), products, len(changed_price)))


if __name__ == '__main__':
    main()
