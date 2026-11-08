"""Ordu Defteri marka seti: profil görseli, öne çıkanlar kapakları, filigran, açılış karuseli."""
import io, os, re, sys
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = sys.argv[1]; IKON = sys.argv[2]; OUT = sys.argv[3]
KAGIT, SAYFA, MUREKKEP, SEPYA, TURKUAZ, SARI = "#F1E6CF", "#FBF5E8", "#2B2118", "#8A5A2B", "#2F6F6A", "#F2C230"
def F(ad, b): return ImageFont.truetype(f"{FONT}/{ad}.ttf", b)
def svg_png(svg, w, h): return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=w, output_height=h))).convert("RGBA")

def sahne_svg(arka=True):
    """Açık defterden yükselen sivri kaya ve kale (viewBox 1080)."""
    hatch = "".join(f'<line x1="{x}" y1="{700-(x-330)*0.9 if x<470 else 470}" x2="{x-40}" y2="700" stroke="{MUREKKEP}" stroke-width="5" opacity=".35"/>' for x in range(380, 470, 28))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080">
{'<rect width="1080" height="1080" fill="%s"/>' % KAGIT if arka else ''}
<circle cx="735" cy="330" r="78" fill="{SARI}" opacity=".9"/>
<g stroke="{MUREKKEP}" stroke-width="5" opacity=".35" fill="none">
  <path d="M120 600 q40 -18 80 0 t80 0"/><path d="M800 600 q40 -18 80 0 t80 0"/><path d="M850 640 q30 -14 60 0 t60 0"/>
</g>
<path d="M300 705 L455 425 L505 470 L555 300 L640 455 L690 420 L790 705 Z" fill="{TURKUAZ}" stroke="{MUREKKEP}" stroke-width="14" stroke-linejoin="round"/>
<path d="M555 300 L520 520 M640 455 L610 600 M455 425 L440 560" stroke="{MUREKKEP}" stroke-width="7" opacity=".45" fill="none"/>
{hatch}
<path d="M520 300 V232 h14 v14 h14 v-14 h14 v14 h14 v-14 h14 v14 h14 v-14 h14 V300 Z" fill="{SAYFA}" stroke="{MUREKKEP}" stroke-width="10" stroke-linejoin="round"/>
<rect x="551" y="262" width="20" height="38" rx="10" fill="{MUREKKEP}"/>
<path d="M540 330 q-10 -30 10 -45 q-14 22 4 36" fill="none" stroke="{MUREKKEP}" stroke-width="0"/>
<path d="M540 720 C 440 676, 290 676, 180 712 L 180 880 C 290 846, 440 846, 540 890 Z" fill="{SAYFA}" stroke="{MUREKKEP}" stroke-width="14" stroke-linejoin="round"/>
<path d="M540 720 C 640 676, 790 676, 900 712 L 900 880 C 790 846, 640 846, 540 890 Z" fill="{SAYFA}" stroke="{MUREKKEP}" stroke-width="14" stroke-linejoin="round"/>
<line x1="540" y1="720" x2="540" y2="890" stroke="{MUREKKEP}" stroke-width="14"/>
<g stroke="{SEPYA}" stroke-width="6" opacity=".55">
  <path d="M225 752 C 310 728, 430 728, 505 756" fill="none"/><path d="M225 792 C 310 768, 430 768, 505 796" fill="none"/><path d="M225 832 C 310 808, 430 808, 505 836" fill="none"/>
  <path d="M575 756 C 650 728, 770 728, 855 752" fill="none"/><path d="M575 796 C 650 768, 770 768, 855 792" fill="none"/><path d="M575 836 C 650 808, 770 808, 855 832" fill="none"/>
</g>
</svg>'''

def kagit_doku(w, h, renk=KAGIT):
    import random
    im = Image.new("RGB", (w, h), renk); px = im.load(); r = random.Random(7)
    for _ in range(w * h // 40):
        x, y = r.randrange(w), r.randrange(h); c = px[x, y]; d = r.randint(-10, 6)
        px[x, y] = tuple(max(0, min(255, v + d)) for v in c)
    return im.filter(ImageFilter.GaussianBlur(0.6))

def ortala(dr, y, txt, font, fill, W, **kw):
    w = dr.textlength(txt, font=font); dr.text(((W - w) / 2, y), txt, font=font, fill=fill, **kw)

# 1) Profil görseli
pro = kagit_doku(1080, 1080); art = svg_png(sahne_svg(False), 1080, 1080)
pro.paste(art, (0, -20), art); pro.save(f"{OUT}/profil.png")

# 2) Filigran (şeffaf)
fw, fh = 900, 220; fil = Image.new("RGBA", (fw, fh), (0, 0, 0, 0)); d = ImageDraw.Draw(fil)
f = F("Playfair-800", 120); t = "ordu defteri"; tw = d.textlength(t, font=f)
golge = Image.new("RGBA", (fw, fh), (0, 0, 0, 0)); ImageDraw.Draw(golge).text(((fw - tw) / 2, 30), t, font=f, fill=(0, 0, 0, 150))
golge = golge.filter(ImageFilter.GaussianBlur(6)); fil = Image.alpha_composite(fil, golge); d = ImageDraw.Draw(fil)
d.text(((fw - tw) / 2, 30), t, font=f, fill=(255, 255, 255, 215)); fil = fil.crop(fil.getbbox()); fil.save(f"{OUT}/filigran.png")

# 3) Öne çıkanlar kapakları
ikonlar = [("kaleler", "castle"), ("yapilar", "landmark"), ("koy-adlari", "signpost"), ("tiyatro", "drama"), ("kaynakca", "book-open")]
for ad, ik in ikonlar:
    svg = open(f"{IKON}/{ik}.svg").read()
    svg = re.sub(r'stroke="currentColor"', f'stroke="{KAGIT}"', svg); svg = re.sub(r'stroke-width="[\d.]+"', 'stroke-width="1.6"', svg)
    k = kagit_doku(1080, 1080, TURKUAZ); ic = svg_png(svg, 520, 520); k.paste(ic, (280, 280), ic)
    k.save(f"{OUT}/one-cikan-{ad}.png")

# 4) Açılış karuseli (1080x1350)
W, H = 1080, 1350
s1 = kagit_doku(W, H); a = svg_png(sahne_svg(False), 900, 900); s1.paste(a, (90, 330), a); d = ImageDraw.Draw(s1)
ortala(d, 120, "Ordu Defteri", F("Playfair-800", 132), MUREKKEP, W)
ortala(d, 290, "Önünden geçip hikâyesini", F("SourceSans-600", 52), SEPYA, W)
ortala(d, 352, "bilmediğimiz yerler", F("SourceSans-600", 52), SEPYA, W)
ortala(d, 1230, "kaydır  »", F("SourceSans-400", 40), MUREKKEP, W)
s1.save(f"{OUT}/acilis-1.png")

s2 = kagit_doku(W, H); d = ImageDraw.Draw(s2)
ortala(d, 110, "Bu defterde neler var?", F("Playfair-800", 76), MUREKKEP, W)
diziler = [("castle", "Önünden geçtiğimiz yer", "Tanıdık yerlerin bilinmeyen hikâyesi"),
           ("signpost", "Adının hikâyesi", "Köy, mahalle ve ilçe adlarının kökeni"),
           ("scroll", "Arşivden", "Eski fotoğraflarla o zaman ve şimdi"),
           ("drama", "Perde arkası", "Ordu sahnesinin 60 yıllık hafızası"),
           ("map-pin", "Ordulu sordu", "Sizin sorularınızın cevabı")]
y = 290
for ik, bas, alt in diziler:
    svg = open(f"{IKON}/{ik}.svg").read().replace('stroke="currentColor"', f'stroke="{TURKUAZ}"')
    svg = re.sub(r'stroke-width="[\d.]+"', 'stroke-width="2"', svg); ic = svg_png(svg, 110, 110); s2.paste(ic, (110, y), ic)
    d.text((260, y + 2), bas, font=F("Playfair-700", 54), fill=MUREKKEP)
    d.text((260, y + 68), alt, font=F("SourceSans-400", 40), fill=SEPYA); y += 175
ortala(d, 1200, "Her akşam 20.30'da yeni bir sayfa", F("SourceSans-600", 46), TURKUAZ, W)
s2.save(f"{OUT}/acilis-2.png")

s3 = kagit_doku(W, H); d = ImageDraw.Draw(s3)
ortala(d, 150, "İlk sayfa:", F("SourceSans-600", 56), SEPYA, W)
ortala(d, 230, "Kurul Kalesi", F("Playfair-800", 128), MUREKKEP, W)
for i, sat in enumerate(["Ordu'dan sadece 13 km uzakta,", "sivri bir kayanın tepesinde,", "2.000 yıl önce bir kale yandı.", "Ve oraya bir daha", "kimse yerleşmedi."]):
    ortala(d, 470 + i * 78, sat, F("SourceSans-400", 52), MUREKKEP, W)
d.rounded_rectangle((140, 930, 940, 1150), radius=28, fill=TURKUAZ)
ortala(d, 965, "Sizin bildiğiniz bir hikâye mi var?", F("SourceSans-600", 44), KAGIT, W)
ortala(d, 1030, "Yorumlara yazın,", F("SourceSans-600", 44), KAGIT, W)
ortala(d, 1085, "defteri birlikte dolduralım.", F("SourceSans-600", 44), KAGIT, W)
ortala(d, 1230, "@ordudefteri", F("Playfair-700", 48), MUREKKEP, W)
s3.save(f"{OUT}/acilis-3.png")
print("tamam")
