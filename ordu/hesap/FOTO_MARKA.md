# Ordu Defteri · Foto Gerçekçi Marka Yönü
Hazırlayan: Claude · 08.11.2026

## Değerlendirme
Sayfanın akışı foto gerçekçi olacaksa çizim tarzı logo videolarla aynı aileden görünmez. Profil fotoğrafı, öne çıkanlar ve açılış gönderisi de foto gerçekçi olmalı.

Ancak foto gerçekçi bir logonun iki riski var:
- **Küçük boyutta okunmazlık:** Profil fotoğrafı akışta yaklaşık 40 piksel görünür. Ayrıntılı bir manzara bu boyutta renkli bir lekeye döner.
- **İçerikle karışma:** Logo bir Reel karesine çok benzerse sayfanın imzası olmaktan çıkar, sıradan bir gönderi gibi durur.

Bu yüzden önerim **"fotoğraf gerçekçi amblem"**: tek bir nesnenin yakın çekimi, ortada sade ve güçlü bir siluet. Sayfa adındaki "defter" fikri de nesnenin kendisi olur.

| Seçenek | Görsel | Artısı | Eksisi |
|---|---|---|---|
| **A · Deri defter (önerilen)** | Eskimiş kahverengi deri defter, kapağa kabartma yaldızlı kaya, kale ve dalga amblemi | Adı anlatır, küçükte okunur, her konuyla uyumlu | Kabartma ayrıntısının Flow'da birkaç denemede oturması gerekebilir |
| B · Kale silueti | Alacakaranlıkta sivri kaya ve kale kalıntısı, altın gökyüzü | Etkileyici, Kurul Kalesi ile güçlü bağ | Tek bir yere bağlanır, küçükte manzara lekesi olur |
| C · Defter ve fındık | Açık eski defter, üstünde fındık dalı ve eski Ordu kartpostalı | Ordu'yu en çok anlatan | Kalabalık, küçükte okunmaz |

**Tipografi değişmiyor:** Filigran ve başlıklardaki "ordu defteri" yazısı Playfair Display serif olarak kalıyor. Yazı fotoğraf gerçekçi yapılmaz. Yazının keskin ve her boyutta okunur kalması gerekir. Foto gerçekçilik görsellerde, tipografi yazıda.

**Bütünlük kuralları:**
- Tüm marka fotoğraflarında aynı ışık: sıcak, sol üstten pencere ışığı. Aynı palet: koyu kahve, Karadeniz turkuazı, altın.
- Öne çıkan kapakları aynı aile: koyu zemin üzerinde tek nesnenin yakın çekimi (taş duvar, kemer, tabela, perde, eski kitaplar).
- Yazılar krem ve altın renkte, yumuşak gölgeli. Fotoğrafın üstünde koyu geçiş ile okunurluk sağlanır.

## Üretilecek 9 fotoğraf
Prompt'ların tamamı `foto_promptlar.json` dosyasında. Her prompt'un başına şu stil eklenir:
```
Photorealistic still-life and landscape photography, 85mm lens, shallow depth of field, warm natural light, rich but natural color grade with deep browns, Black Sea teal and soft golden highlights, subtle film grain. No text, no letters, no numbers, no logos, no watermark.
```

| Dosya adı | Oran | Kullanım |
|---|---|---|
| profil.png | 1:1 | Profil fotoğrafı (A seçeneği) |
| oc-kaleler.png | 1:1 | Öne çıkan: Kaleler (taş duvar ve mazgal) |
| oc-yapilar.png | 1:1 | Öne çıkan: Yapılar (taş kilise kemeri) |
| oc-koy-adlari.png | 1:1 | Öne çıkan: Köy Adları (yazısız eski tabela) |
| oc-tiyatro.png | 1:1 | Öne çıkan: Tiyatro (kırmızı kadife perde) |
| oc-kaynakca.png | 1:1 | Öne çıkan: Kaynakça (eski kitaplar ve büyüteç) |
| bg-1.png | 4:5 | Açılış karuseli 1: pencere önünde açık defter |
| bg-2.png | 4:5 | Açılış karuseli 2: ceviz masa zemini |
| bg-3.png | 4:5 | Açılış karuseli 3: Kurul Kalesi alacakaranlıkta |

Profil için Flow'da 4 deneme üretilip en net amblemli olan seçilmeli.

## Birleştirme
Fotoğraflar geldiğinde `foto_marka.py` tek komutla şunları yapar: ortak sıcak ton ve vinyet, profil fotoğrafı, beş öne çıkan kapağı ve yazılı üç açılış görseli. Betik yer tutucularla denendi.

## Üretim yolları
1. **Mac'teki Tarihin Atölyesi oturumu:** Aşağıdaki mesajı yapıştırın. Flow'da 9 fotoğrafı üretip GitHub'a koyar ya da size gönderir.
2. **Bu bulut oturumu:** Gemini projesine kredi yüklenirse `--uret` seçeneğiyle hepsini kendim üretirim.

### Mac oturumuna yapıştırılacak mesaj
```
Ordu Defteri Instagram sayfası için foto gerçekçi marka fotoğrafları üret, onaylıyorum. Tarihin Atölyesi'yle ilgisi yok, hiçbir şey yayımlama.

Prompt'lar burada (9 adet, dosya adı + oran + prompt):
https://raw.githubusercontent.com/alicantaze0-design/gizlilik/claude/ordu-instagram-page-a2rs30/ordu/hesap/foto_promptlar.json

Her prompt'un başına şu stili ekle:
"Photorealistic still-life and landscape photography, 85mm lens, shallow depth of field, warm natural light, rich but natural color grade with deep browns, Black Sea teal and soft golden highlights, subtle film grain. No text, no letters, no numbers, no logos, no watermark."

- Flow, Nano Banana Pro (en iyi foto gerçekçi model), oranlar JSON'daki gibi (1:1 ya da 4:5; 4:5 yoksa 3:4).
- "profil" için 4 deneme üret; amblemi (kaya + küçük kale + üç dalga, yaldızlı kabartma) en net ve ortada olanı profil.png olarak seç, diğerlerini profil-2/3/4.png diye sakla.
- Diğer 8 fotoğraf için 1'er deneme; yazı ya da harf çıkarsa yeniden üret.
- Klasör: ~/Desktop/Ordu-Sayfasi/marka/girdi/ — dosya adları JSON'daki anahtarlar (profil.png, oc-kaleler.png, ... bg-3.png).
- Teslim: Mümkünse bu dosyaları git ile alicantaze0-design/gizlilik deposunun claude/ordu-instagram-page-a2rs30 dalına ordu/hesap/foto_girdi/ klasörüne koyup push et. Olmazsa 9 fotoğrafı bana WhatsApp'tan kendi sohbetime ("Kendine mesaj") gönder.
```
