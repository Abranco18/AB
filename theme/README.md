# `theme.liquid` – mit Rabatt-Rundung

Das unveränderte `layout/theme.liquid` des Shops, ergänzt um **einen** Block:
ein `<script>`, das die Rabatt-Badges auf Vielfache von 5 rundet
(Einerstelle 1–4 → 5, darüber → nächster Zehner; 67 % → 70 %, 61 % → 65 %).

## Was geändert wurde
Nichts außer dem eingefügten Block. Er steht an der vom Theme dafür
vorgesehenen Stelle, zwischen

```
<!-- Paste marketing code or third party scripts below this comment line -->
...
<!-- And above this comment line -->
```

Geprüft: entfernt man den Block wieder, entsteht exakt die Ausgangsdatei –
alle 5 `render`- und 4 `sections`-Aufrufe, der komplette `<style>`-Block und
die Body-Klassen sind unberührt.

## Wie das Skript arbeitet
- Es fasst nur Elemente an, deren **gesamter** Textinhalt eine Badge ist
  (`-67%`, `67 %`, `−67%`). Fließtext wie „etwa 20 %“ bleibt unangetastet.
- Es sucht zuerst die Badge-Klassen dieses Themes (`.sale-box`,
  `.product__price--off--custom`, …), danach folgt ein allgemeiner Durchlauf.
- Es schreibt nur `textContent`, niemals HTML – Markup und Event-Handler
  bleiben erhalten.
- Ein `MutationObserver` (80 ms Debounce) erfasst Karussells, Filter und
  Quick-View, die Inhalte nachladen.

## Kontrolle
In der Browser-Konsole:

```js
__rabattBadges()   // Anzahl der korrigierten Badges
```

`0` bedeutet: das Skript läuft, findet aber keine Badge als Text – dann wird
die Zahl per CSS `content:` oder als Bild erzeugt.

> ⚠️ Das Skript ändert **nur die Anzeige**. Der tatsächliche Rabatt bleibt
> 67 %, während „70 %“ dasteht. In Deutschland verlangt § 11 PAngV, dass die
> angegebene Ersparnis dem tatsächlichen Preisverlauf entspricht.
> `de/loja_final_DE.csv` löst dasselbe über die Vergleichspreise – dort stimmt
> die angezeigte Zahl.
