# -*- coding: utf-8 -*-
"""Uebersetzt NUR die Spalte 'Title' der Tischlaeufer (ES -> DE).

Handles bleiben unveraendert, damit ein Import die bestehenden Produkte
aktualisiert statt neue anzulegen. Alle anderen Spalten werden 1:1 uebernommen.
"""
import csv
import re
import sys

SRC, DST = sys.argv[1], sys.argv[2]

TITLE_PREFIX_DE = "Gesteppter Tischläufer - "

# Motivnamen: identisch zu tischlaeufer_export_DE.csv, damit die Benennung
# im Shop konsistent bleibt.
MOTIFS = {
    "camino-de-mesa-acolchado-jardin-en-flores": "Blühender Garten",
    "camino-de-mesa-acolchado-magnolia-tranquila": "Stille Magnolie",
    "camino-de-mesa-acolchado-jardin-de-girasoles": "Sonnenblumengarten",
    "camino-de-mesa-acolchado-flores-de-frangipani": "Frangipani-Blüten",
    "camino-de-mesa-acolchado-corazones-y-rosas": "Herzen und Rosen",
    "camino-de-mesa-acolchado-sueno-de-carpas-koi": "Koi-Traum",
    "camino-de-mesa-acolchado-temporada-de-calabazas": "Kürbiszeit",
    "camino-de-mesa-acolchado-gracia-divina": "Göttliche Gnade",
    "camino-de-mesa-acolchado-familia-de-osos-negros": "Schwarzbärenfamilie",
    "camino-de-mesa-acolchado-abundancia-de-otono": "Herbstfülle",
    "camino-de-mesa-acolchado-corazones-calidos": "Warme Herzen",
    "camino-de-mesa-acolchado-paisaje-de-pinos-nevados": "Verschneite Kiefernlandschaft",
    "camino-de-mesa-acolchado-arte-ecuestre": "Pferdekunst",
    "camino-de-mesa-acolchado-estrella-de-belen": "Stern von Bethlehem",
    "camino-de-mesa-acolchado-cascabeles-festivos": "Festliche Glöckchen",
    "camino-de-mesa-acolchado-sendero-de-petalos": "Blütenblattpfad",
    "camino-de-mesa-acolchado-camino-helado": "Frostiger Pfad",
    "camino-de-mesa-acolchado-serenata-de-lupinos": "Lupinenserenade",
    "camino-de-mesa-acolchado-carrera-de-pavos": "Truthahnrennen",
    "camino-de-mesa-acolchado-rojo-cardenal": "Kardinalrot",
    "camino-de-mesa-acolchado-girasoles-de-otono": "Herbstsonnenblumen",
    "camino-de-mesa-acolchado-calabaza-especiada": "Gewürzkürbis",
    "camino-de-mesa-acolchado-bosque-de-esmeralda": "Smaragdwald",
    "camino-de-mesa-acolchado-desfile-de-calabazas": "Kürbisparade",
    "camino-de-mesa-acolchado-arbol-celta": "Keltischer Baum",
    "camino-de-mesa-acolchado-corazones-en-flor": "Herzen in Blüte",
    "camino-de-mesa-acolchado-cascada-de-corazones": "Herzenkaskade",
    "camino-de-mesa-acolchado-mascaras-de-carnaval": "Karnevalsmasken",
    "camino-de-mesa-acolchado-marcha-de-los-elefantes": "Elefantenmarsch",
    "camino-de-mesa-acolchado-gracia-en-flores": "Blütenanmut",
    "camino-de-mesa-acolchado-caballo-al-galope": "Galoppierendes Pferd",
    "camino-de-mesa-acolchado-alas-escarlatas": "Scharlachrote Flügel",
    "camino-de-mesa-acolchado-desfile-de-gallos": "Hahnenparade",
    "camino-de-mesa-acolchado-esplendor-artico": "Arktische Pracht",
    "camino-de-mesa-acolchado-espiritu-celta": "Keltischer Geist",
    "camino-de-mesa-acolchado-luz-de-belen": "Licht von Bethlehem",
    "camino-de-mesa-acolchado-belleza-estrellada": "Sternenschönheit",
    "camino-de-mesa-acolchado-alegria-de-halloween": "Halloween-Freude",
    "camino-de-mesa-acolchado-flor-de-magnolia-rustica": "Rustikale Magnolienblüte",
}


def main():
    with open(SRC, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames, rows = reader.fieldnames, list(reader)

    n = 0
    for row in rows:
        if row["Title"].strip():
            handle = row["Handle"]
            if handle not in MOTIFS:
                raise ValueError("Unbekannter Handle: %r" % handle)
            row["Title"] = TITLE_PREFIX_DE + MOTIFS[handle]
            n += 1

    with open(DST, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Zeilen: %d | uebersetzte Titel: %d" % (len(rows), n))


if __name__ == "__main__":
    main()
