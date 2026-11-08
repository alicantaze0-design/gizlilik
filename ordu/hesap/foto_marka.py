"""Ordu Defteri foto gerçekçi marka seti.
Girdi klasöründe şu fotoğraflar olmalı (Flow/Nano Banana ya da Gemini çıktısı):
  profil.png, oc-kaleler.png, oc-yapilar.png, oc-koy-adlari.png, oc-tiyatro.png, oc-kaynakca.png,
  bg-1.png, bg-2.png, bg-3.png
Kullanım: python3 foto_marka.py GIRDI CIKTI [--uret]  (yazı tipi ve ikonlar varlik/ klasöründen)
--uret: eksik fotoğrafları Gemini API ile üretir (GEMINI_KEY_FILE gerekir)."""
import io, os, re, sys, json
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

_B = os.path.dirname(os.path.abspath(__file__)); _a = [x for x in sys.argv[1:] if not x.startswith("--")]
if len(_a) >= 4: FONT, IKON, GIR, OUT = _a[:4]
else: FONT, IKON, (GIR, OUT) = f"{_B}/varlik/fonts", f"{_B}/varlik/ikonlar", _a[:2]
URET = "--uret" in sys.argv
ALTIN, KREM = "#E8C77A", "#F4EBDD"
def F(ad, b): return ImageFont.truetype(f"{FONT}/{ad}.ttf", b)

STIL = ("Photorealistic still-life and landscape photography, 85mm lens, shallow depth of field, "
        "warm natural light, rich but natural color grade with deep browns, Black Sea teal and soft golden highlights, "
        "subtle film grain. No text, no letters, no numbers, no logos, no watermark.")
PROMPT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "foto_promptlar.json"), encoding="utf-8"))

def uret_eksik():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../01-kurul-kalesi/uretim"))
    import gemini
    model = gemini.model_sec(["gemini-3-pro-image", "gemini-2.5-flash-image", "image"], "generateContent")
    for ad, p in PROMPT.items():
        y = f"{GIR}/{ad}.png"
        if not os.path.exists(y):
            print("üretiliyor:", ad); gemini.gorsel(model, STIL + "\n\n" + p["prompt"], y, oran=p["oran"])

def kirp(im, w, h):
    r = max(w / im.width, h / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2; return im.crop((x, y, x + w, y + h))

def renk_birlik(im, sicak=0.06):
    """Hafif sıcak ton + kontrast: farklı fotoğrafları tek aile gibi gösterir."""
    im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(0.92)
    ton = Image.new("RGB", im.size, (120, 84, 48)); return Image.blend(im, ton, sicak)

def vinyet(im, guc=0.55):
    w, h = im.size; m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    d.ellipse((-w * 0.15, -h * 0.15, w * 1.15, h * 1.15), fill=255); m = m.filter(ImageFilter.GaussianBlur(min(w, h) * 0.12))
    koyu = Image.new("RGB", (w, h), (12, 9, 6)); return Image.composite(im, Image.blend(im, koyu, guc), m)

def gradyan(im, ust=0.0, alt=0.0):
    w, h = im.size; g = Image.new("L", (1, h))
    for y in range(h):
        t = y / h; a = max(ust * (1 - t / 0.45) if t < 0.45 else 0, alt * ((t - 0.55) / 0.45) if t > 0.55 else 0)
        g.putpixel((0, y), int(255 * min(a, 1)))
    g = g.resize((w, h)); return Image.composite(Image.new("RGB", (w, h), (10, 8, 6)), im, g)

def yaz(d, y, t, f, renk, W, golge=True):
    w = d.textlength(t, font=f); x = (W - w) / 2
    if golge: d.text((x + 3, y + 4), t, font=f, fill=(0, 0, 0, 160))
    d.text((x, y), t, font=f, fill=renk)

def ikon(ad, renk, px):
    s = open(f"{IKON}/{ad}.svg").read().replace('stroke="currentColor"', f'stroke="{renk}"')
    s = re.sub(r'stroke-width="[\d.]+"', 'stroke-width="1.8"', s)
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(), output_width=px, output_height=px))).convert("RGBA")

def main():
    os.makedirs(OUT, exist_ok=True)
    if URET: uret_eksik()
    eksik = [a for a in PROMPT if not os.path.exists(f"{GIR}/{a}.png")]
    if eksik: sys.exit(f"Eksik fotoğraflar: {eksik}")
    # Profil
    p = vinyet(renk_birlik(kirp(Image.open(f"{GIR}/profil.png").convert("RGB"), 1080, 1080)), 0.35)
    p.save(f"{OUT}/profil.png", quality=95)
    # Öne çıkanlar
    for ad in ["kaleler", "yapilar", "koy-adlari", "tiyatro", "kaynakca"]:
        im = vinyet(renk_birlik(kirp(Image.open(f"{GIR}/oc-{ad}.png").convert("RGB"), 1080, 1080), 0.10), 0.6)
        im.save(f"{OUT}/one-cikan-{ad}.png", quality=92)
    W, H = 1080, 1350
    # Karusel 1
    s = gradyan(renk_birlik(kirp(Image.open(f"{GIR}/bg-1.png").convert("RGB"), W, H)), ust=0.75, alt=0.55)
    d = ImageDraw.Draw(s, "RGBA")
    yaz(d, 120, "Ordu Defteri", F("Playfair-800", 132), KREM, W)
    yaz(d, 300, "Önünden geçip hikâyesini", F("SourceSans-600", 52), ALTIN, W)
    yaz(d, 362, "bilmediğimiz yerler", F("SourceSans-600", 52), ALTIN, W)
    yaz(d, 1235, "kaydır  »", F("SourceSans-400", 40), KREM, W)
    s.save(f"{OUT}/acilis-1.png", quality=93)
    # Karusel 2
    s = Image.blend(renk_birlik(kirp(Image.open(f"{GIR}/bg-2.png").convert("RGB"), W, H)), Image.new("RGB", (W, H), (10, 8, 6)), 0.55)
    d = ImageDraw.Draw(s, "RGBA"); yaz(d, 110, "Bu defterde neler var?", F("Playfair-800", 76), KREM, W)
    y = 290
    for ik, bas, alt in [("castle", "Önünden geçtiğimiz yer", "Tanıdık yerlerin bilinmeyen hikâyesi"),
                         ("signpost", "Adının hikâyesi", "Köy, mahalle ve ilçe adlarının kökeni"),
                         ("scroll", "Arşivden", "Eski fotoğraflarla o zaman ve şimdi"),
                         ("drama", "Perde arkası", "Ordu sahnesinin 60 yıllık hafızası"),
                         ("map-pin", "Ordulu sordu", "Sizin sorularınızın cevabı")]:
        i = ikon(ik, ALTIN, 110); s.paste(i, (110, y), i)
        d.text((260, y + 2), bas, font=F("Playfair-700", 54), fill=KREM)
        d.text((260, y + 68), alt, font=F("SourceSans-400", 40), fill=ALTIN); y += 175
    yaz(d, 1200, "Her akşam 20.30'da yeni bir sayfa", F("SourceSans-600", 46), ALTIN, W)
    s.save(f"{OUT}/acilis-2.png", quality=93)
    # Karusel 3
    s = gradyan(renk_birlik(kirp(Image.open(f"{GIR}/bg-3.png").convert("RGB"), W, H)), ust=0.8, alt=0.85)
    d = ImageDraw.Draw(s, "RGBA")
    yaz(d, 120, "İlk sayfa:", F("SourceSans-600", 56), ALTIN, W)
    yaz(d, 195, "Kurul Kalesi", F("Playfair-800", 128), KREM, W)
    for k, sat in enumerate(["Ordu'dan sadece 13 km uzakta,", "2.000 yıl önce bir kale yandı.", "Ve oraya bir daha kimse yerleşmedi."]):
        yaz(d, 960 + k * 66, sat, F("SourceSans-600", 46), KREM, W)
    yaz(d, 1180, "Bildiğiniz bir hikâye varsa yorumlara yazın", F("SourceSans-400", 40), ALTIN, W)
    yaz(d, 1250, "@ordudefteri", F("Playfair-700", 44), KREM, W)
    s.save(f"{OUT}/acilis-3.png", quality=93)
    print("foto marka seti hazır:", OUT)

if __name__ == "__main__":
    main()
