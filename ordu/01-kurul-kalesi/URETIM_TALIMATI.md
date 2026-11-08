# Kurul Kalesi · Üretim Talimatı (Mac'teki Tarihin Atölyesi oturumu için)

Bu talimat Ali Can'ın onayıyla hazırlandı. Ali Can'ın istekleri, kendi sözleriyle:
- "Bana bu bölüm örneğini hem 2D hem de foto gerçekçi örnek olarak ver. Flow ve Veo'yu kullanabilirsin."
- "Seslendirme olarak Pro Enceladus gibi bir isim vardı, ona seslendirt."
- "Tamam bitince WhatsApp'tan bana gönder."

Hikâye, sahne prompt'ları, caption ve kaynakça bu klasördeki `kurul_kalesi_bolum.md` ve `kurul_kalesi_script.json` dosyalarında. Seslendirme metni ve prompt'lar aşağıda da tam olarak var.

## Kapsam ve sınırlar
- Yeni bir Ordu Instagram sayfası için deneme Reel'i. Tarihin Atölyesi kanalıyla ilgisi yok. Hiçbir şey yayımlama, YouTube'a dokunma, Uluğ Bey zamanlamasına ve 10–12 Kasım görevine dokunma.
- Çıktı klasörü: `~/Desktop/Ordu-Sayfasi/01-Kurul-Kalesi/` altında `2d/` ve `foto/` (img/, vid/, tts/, final mp4).
- Görseller: Flow, Nano Banana, Resim, 9:16, x1 (0 kredi).
- Veo: yalnızca işaretli sahnelerde, image-to-video (ilgili still'den), 9:16, ~6–8 sn. Kredi yetmezse ya da 0 ise Veo'yu atla, Ken Burns / render_25d paralaks kullan. Toplam Veo kullanımını ve kalan krediyi raporla.
- Seslendirme: **Pro Enceladus**, tts_pro3.py (aynı TON talimatı). İki versiyon aynı ses dosyasını kullanabilir.
- Altyazı: ortada kalın beyaz, vurgu kelimeleri sarı (ASS + ffmpeg). Hızlı olmazsa altyazısız bırak ve söyle. Filigran: sayfa adı **Ordu Defteri**. Üst ortada, ~330 px genişlik, %80 opaklık: https://raw.githubusercontent.com/alicantaze0-design/gizlilik/claude/ordu-instagram-page-a2rs30/ordu/hesap/gorseller/filigran.png
- Müzik: alçak davul + tok yaylı. Sahne 4'te yükselsin, 5'te sussun, 6'da yumuşak açılsın. Final −14 LUFS.

## Teslim
1. İki MP4 (1080x1920, ~54 sn) ve her versiyondan 8 still'lik kontak sayfası.
2. **WhatsApp:** Chrome'da yeni sekmede WhatsApp Web, Ali Can'ın KENDİ sohbeti ("Kendine mesaj" / kendi numarası). Başka kişiye ya da gruba gönderme. Açıklamalar: "Kurul Kalesi · 2D" ve "Kurul Kalesi · Foto gerçekçi". WhatsApp Web'e ulaşamazsan (QR istiyor vb.) Telegram'dan gönder ve nedenini yaz.
3. Uygulamaya da gönder (30 MB sınırı, gerekirse sıkıştır).
4. Kısa rapor: dosya yolları, Veo kullanımı ve kalan kredi, atlanan ya da sorunlu sahneler.

## Seslendirme (8 sahne, ~125 kelime)
| # | Süre | Metin | Sarı vurgu |
|---|---|---|---|
| 1 | 0–5 | Ordu'dan sadece on üç kilometre uzakta, sivri bir kayanın tepesinde, iki bin yıldan uzun zaman önce bir kale yandı. Ve oraya bir daha kimse yerleşmedi. | on üç kilometre · yandı |
| 2 | 5–12 | Burası Kurul Kalesi. Roma'ya kafa tutan Pontus kralı Mithridates'in, Melet vadisini bekleyen kalelerinden biri. | Kurul Kalesi · Mithridates |
| 3 | 12–19 | Kayaya oyulmuş yaklaşık üç yüz basamak, su sarnıçları ve erzakla dolu altmışa yakın küp. Kale uzun bir kuşatmaya hazırdı. | üç yüz basamak · altmış küp |
| 4 | 19–27 | Ama Roma geldi. Kazıcılar yanık toprağın içinde Roma lejyonerlerinin pilum mızraklarını ve surları sökmek için kullanılan orak-mızrağı buldu. | Roma · pilum · orak-mızrak |
| 5 | 27–33 | Kale yandı ve terk edildi. Üstüne kimse yeni bir şey kurmadığı için her şey düştüğü yerde kaldı. | düştüğü yerde |
| 6 | 33–42 | Ve iki bin on altıda toprağın altından oturan bir tanrıça çıktı: Kybele. Kucağında hâlâ bir sikke duruyordu. | Kybele · sikke |
| 7 | 42–48 | Kazılar iki bin onda başladı ve kalenin henüz yarısı bile açılmadı. | yarısı bile |
| 8 | 48–54 | Sizce o sikkeyi Kybele'nin kucağına kim bıraktı? Ne diliyordu? Yorumlara yazın. | kim bıraktı? |

## Versiyon A: 2D
Stil (her prompt'un başına):
```
2D cartoon comic illustration for a vertical 9:16 Instagram Reel. Detailed background in fine black ink linework with cross-hatching and soft watercolor wash, warm sepia paper texture mixed with Black Sea greens and teal. Characters are simple stick figures with a plain white round head, two small black dot eyes and tiny simple eyebrows and mouth for expression, thin black limbs, small flat-colored clothing pieces (red, ochre, green, blue). Characters sit clearly on top of the detailed background like a separate layer. Leave the top 12% and the middle band calm for a watermark and subtitles. No text, no letters, no numbers, no watermark.
```
- **A1:** Low-angle dramatic view of a sharp pointed rocky peak rising above a deep green river valley, ruins of a Hellenistic stone fortress on its summit with thin smoke rising into a dusky orange sky. Hazelnut orchards and a winding modern road at the bottom. In the foreground a stick-figure narrator in a green jacket stands on the road looking up with a surprised expression.
- **A2:** A stick-figure Pontic king with a small golden diadem and long purple cloak stands on the fortress wall atop the rocky peak, pointing down at a winding river valley. Banners with an eight-rayed star and crescent emblem flutter on the towers. The Black Sea glimmers far on the horizon. Two stick-figure guards with round bronze shields stand beside him.
- **A3:** Cutaway view inside the rock: a long staircase carved directly into the stone descends deep into the mountain toward an underground water cistern. Next to it a storage room filled with rows of large clay pithos jars. Stick-figure soldiers in ochre tunics carry grain sacks and water jars down the steps. Torchlight, warm shadows.
- **A4:** Siege scene at the fortress walls: stick-figure Roman legionaries in red tunics, metal helmets and curved rectangular shields climb the rocky slope and hurl long iron-shanked javelins (pila). One legionary uses a long pole with a curved hooked blade to pull stones off the battlements. Arrows in the air, flames starting on a wooden tower. Dramatic, dark sky. **[Veo: opsiyonel, kredi yeterse]**
- **A5:** The burned fortress at night after the battle: charred wooden beams, collapsed walls, broken clay pithos jars spilling grain, a single Roman javelin stuck in the ash. Silent and empty, moonlight, wisps of smoke. Grass and moss beginning to creep over the stones.
- **A6:** Modern archaeological excavation trench on the rocky summit with string grid lines and labelled buckets. Two stick-figure archaeologists in sun hats kneel with trowels and brushes, uncovering a seated marble mother-goddess statue. A small bronze coin rests on the goddess's lap and catches a soft beam of light. One archaeologist has an amazed expression.
- **A7:** Present-day view of the excavation site on top of the pointed rock: wooden walkways, white tents, parts of ancient walls exposed while large areas are still covered in earth and grass. A few stick-figure visitors look around. Far in the distance the city of Ordu and the Black Sea under a clear afternoon sky.
- **A8:** Close-up of the seated marble goddess statue's lap with the small ancient bronze coin. The stick-figure narrator from scene 1 leans in from the side, chin on hand, curious thoughtful expression. Warm soft light, shallow depth, calm background.

Hareket: Ken Burns (gerekirse render_25d). Veo yalnızca A4 için ve kredi yeterse.

## Versiyon B: Foto gerçekçi
Stil (her prompt'un başına):
```
Photorealistic cinematic historical reconstruction for a vertical 9:16 Instagram Reel, documentary realism, natural light, 35mm film look, rich but natural color grade. People are seen from behind, in silhouette or at a distance; no close-up faces. Leave the top 12% and the middle band calm for a watermark and subtitles. No text, no letters, no numbers, no watermark.
```
- **B1:** Aerial dusk drone shot of a sharp pointed rocky peak above a lush green river valley in the eastern Black Sea mountains, hazelnut orchards on the slopes, ruins of an ancient stone fortress on the summit with a thin column of smoke rising, a winding road far below, moody orange and violet sky. **[VEO: yavaş drone itişi, duman süzülüyor]**
- **B2:** A Hellenistic king in a long purple cloak and gold diadem, seen from behind, standing on a stone fortress wall overlooking a winding river valley toward the distant Black Sea; banners with an eight-rayed star and crescent emblem; two guards with round bronze shields beside him.
- **B3:** Torchlit staircase carved into solid rock descending deep into a mountain, worn stone steps leading to an underground water cistern; a side chamber with rows of large terracotta pithos jars; soldiers in linen tunics seen from behind carrying grain sacks down the steps.
- **B4:** Late Roman Republic legionaries in red tunics, chainmail and bronze Montefortino helmets with oval scutum shields, seen from behind, advancing up a rocky slope toward fortress walls and hurling iron pila; one legionary uses a long pole with a hooked iron blade to pull stones from the battlements; smoke, arrows, dramatic overcast sky. **[VEO: askerler ilerliyor, mızrak atılıyor]**
- **B5:** Aftermath at night: a burned hilltop fortress, charred beams, collapsed stone walls, broken terracotta pithoi spilling grain, a Roman pilum stuck upright in the ashes, moonlight, thin smoke.
- **B6:** Modern archaeological excavation on a hilltop with string grid lines; archaeologists in sun hats seen from behind gently brushing soil from a seated marble mother-goddess statue; a small ancient bronze coin rests on her lap and catches the sunlight. **[VEO: fırça toprağı süpürüyor, sikke ortaya çıkıyor]**
- **B7:** Present-day excavation site on a rocky summit: wooden walkways, white tents, partly exposed ancient walls with large areas still under earth and grass; a few visitors at a distance; the city of Ordu and the Black Sea far in the background, clear afternoon light.
- **B8:** Extreme close-up macro of an ancient bronze coin resting on the marble lap of a seated goddess statue, soft warm light, floating dust particles, shallow depth of field.

Hareket: B1, B4, B6 Veo. Kalanlar render_25d paralaks.

Not: Kybele heykeli gerçek eserin kopyası olmasın, temsili oturan tanrıça yeterli.
