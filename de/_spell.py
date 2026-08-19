# -*- coding: utf-8 -*-
import json, re, sys
from spellchecker import SpellChecker

sp = SpellChecker(language='de')
D = sp.word_frequency.dictionary

EXTRA = set("""wäschekorb wäschekörbe tischläufer tischläufers kissenbezug kissenbezüge bettwäsche
gesteppt gesteppter gesteppte gesteppten gestepptes handgefertigt handgefertigte handgefertigter
handgefertigtes handgefertigten reisetasche reisetaschen strandtasche strandtaschen dekokissen
karaffe karaffen whisky mikrowellen spülmaschinengeeignet trocknergeeignet maschinenwaschbar
canvas polyester baumwoll steppnaht steppnähte umgebungslicht akzentlampe tischlampe schreibtischlampe
nachtlampe buntglas buntglaslampe glaslampe mosaik mosaikflügel mosaikflügeln schmetterlingslampe
schmetterlingslampen buchtasse buchtassen lesetasse gitarrentasse kaffeetasse kaffeetassen
mineralkristall bücherfreunde bücherwürmer leseratten leseecke leseecken essbereich wohnraum
wohndeko wohndekoration nachttisch nachttische geschenkidee geschenkwahl geschenkfertig
blickfang gesprächsanlass jetiy amethyst obsidian achat vulkanrot querformat
frühlingswiese wiesensonne wiesenblüte waldglanz waldgeist baumglanz sonnenglanz muschelglanz
lilienuhr sternenpfoten katzenschar mitternachtswiese blütenchronik blütenanmut blütenblattpfad
geschichtenblüten kürbiszeit kürbisparade gewürzkürbis smaragdwald lupinenserenade truthahnrennen
kardinalrot herbstsonnenblumen herbstfülle karnevalsmasken elefantenmarsch hahnenparade
herzenkaskade morgenpracht schwarzbärenfamilie frangipani bluebonnet koi menora menorah
halloween pilzlampen tierlampen vintage stil design edition modell größe
""".split())

KNOWN = set(D) | EXTRA
LINK = ('', 's', 'n', 'en', 'e', 'es', 'er')


def known(w):
    return w in KNOWN


def compound_ok(w, depth=0):
    """Erkennt deutsche Komposita: alle Teile muessen bekannt sein."""
    if known(w):
        return True
    if depth > 2 or len(w) < 6:
        return False
    for i in range(3, len(w) - 2):
        head = w[:i]
        for l in LINK:
            if head.endswith(l) and l:
                base = head[:-len(l)]
            else:
                base = head
            if len(base) >= 3 and known(base):
                if compound_ok(w[i:], depth + 1):
                    return True
    return False


def check(text):
    words = re.findall(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]{2,}", text)
    bad = []
    for w in words:
        for part in w.split('-'):
            p = part.lower()
            if len(p) < 3 or p.isupper():
                continue
            if not compound_ok(p):
                bad.append(part)
    return bad
