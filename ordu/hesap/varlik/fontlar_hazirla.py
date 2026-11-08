"""Fontsource'un latin ve latin-ext parçalarını Türkçe karakterli tek TTF'de birleştirir (yerel kullanım).
Çıktı: varlik/fonts/*.ttf (git'e eklenmez). Kaynak dosyalar değiştirilmeden kaynak/ klasöründe durur."""
import os
from fontTools.ttLib import TTFont
from fontTools.merge import Merger
B = os.path.dirname(os.path.abspath(__file__)); K = f"{B}/fonts/kaynak"; O = f"{B}/fonts"
for ad, w, hedef in [("merriweather", 900, "Merriweather-900"), ("merriweather", 700, "Merriweather-700"),
                     ("playfair-display", 800, "Playfair-800"), ("playfair-display", 700, "Playfair-700"),
                     ("source-sans-3", 600, "SourceSans-600"), ("source-sans-3", 400, "SourceSans-400")]:
    if os.path.exists(f"{O}/{hedef}.ttf"): continue
    parca = []
    for alt in ("latin", "latin-ext"):
        f = TTFont(f"{K}/{ad}-{alt}-{w}-normal.woff"); f.flavor = None
        p = f"{O}/_{ad}-{alt}-{w}.ttf"; f.save(p); parca.append(p)
    Merger().merge(parca).save(f"{O}/{hedef}.ttf")
    for p in parca: os.remove(p)
    print("hazır:", hedef)
