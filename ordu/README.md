# Ordu Defteri · Proje Dosyası
Instagram: **@ordudefteri** · Görünen ad: "Ordu Defteri · Ordu'nun Hikâyeleri"
Sahibi: Ali Can Taze · Son güncelleme: 08.11.2026
Bu dosya iki oturumun bilgisini birleştirir: bulut oturumu "Ordu Defteri" ve Mac'teki "Tarihin Atölyesi" oturumu.

---

## 1. Kararlar (tarih sırasıyla)
| Tarih | Karar |
|---|---|
| 07.11 | @ordulog örnek alınarak Ordu'ya özgü, Reels ağırlıklı bir tarih sayfası açılacak. |
| 07.11 | Biçim: 9:16, 40–55 sn, 6–8 sahne, sonda soru, caption'da kaynakça. |
| 08.11 | İlk bölüm **Kurul Kalesi**. Seslendirme **Pro Enceladus** (Gemini 2.5 Pro TTS). |
| 08.11 | Her bölüm iki versiyon denendi: 2D ve foto gerçekçi. |
| 08.11 | Sayfa adı **Ordu Defteri** (@ordudefteri). Kotyora ikinci aday olarak kaldı. |
| 08.11 | Sayfanın ana dili **foto gerçekçi**. Logo ve marka seti de foto gerçekçi olacak: deri defter kapağında yaldızlı kaya, kale ve dalga amblemi. Tipografi (Playfair Display) yazıda kalır. |
| 08.11 | Altyazı ekranın ~%70 yüksekliğinde (Instagram alt arayüzünün üstünde). |
| 08.11 | Videolarda üst ortada yarı saydam "ordu defteri" filigranı. |

## 2. Durum
| İş | Durum |
|---|---|
| ordulog incelemesi | Bitti · `ORDU_SAYFASI_ONERILER.md` |
| 30 konu başlığı, sayfa stratejisi | Bitti · `ORDU_SAYFASI_ONERILER.md` |
| Hesap açılış rehberi | Bitti · `hesap/KURULUM.md` |
| 2D marka seti (yedek) | Bitti · `hesap/gorseller/` |
| Foto gerçekçi marka seti | **Bekliyor:** 9 fotoğraf üretilecek · `hesap/FOTO_MARKA.md`, `hesap/foto_promptlar.json` |
| Instagram hesabının açılması | **Bekliyor:** Ali Can açacak |
| Kurul Kalesi Reel'i | Üretildi (Mac) · 2D + foto gerçekçi (Veo: sahne 1, 4, 6) · 61 sn · −14,1 LUFS |
| Kurul Kalesi videolarının GitHub'a konması | **Bekliyor:** Mac oturumuna yapıştırılacak mesaj aşağıda |
| Filigran ve #ordudefteri Kurul Kalesi videolarında | **Bekliyor:** Mac'teki videolar filigransız |
| Bulut oturumundan üretim | **Bekliyor:** Gemini kredisi ve kalıcı anahtar |

## 3. Dosya haritası (GitHub · `claude/ordu-instagram-page-a2rs30` dalı · `ordu/`)
| Dosya | İçerik |
|---|---|
| `README.md` | Bu dosya |
| `ORDU_SAYFASI_ONERILER.md` | ordulog incelemesi, ad adayları, 30 konu, strateji, ölçütler |
| `MAC_OTURUMU_ORDU_KAYDI.md` | Mac oturumunun Ordu kaydı: zaman çizelgesi, üretim ayrıntıları, Mac'teki dosya yolları, dersler |
| `hesap/KURULUM.md` | Hesap açılışı, bio, açılış gönderisi metni, öne çıkanlar, ilk hafta takvimi |
| `hesap/FOTO_MARKA.md` | Foto gerçekçi marka değerlendirmesi ve Mac oturumu mesajı |
| `hesap/foto_promptlar.json` | 9 marka fotoğrafının prompt'u |
| `hesap/foto_marka.py` | Fotoğraflardan profil, öne çıkanlar ve açılış karuselini kurar |
| `hesap/marka.py`, `hesap/gorseller/` | 2D marka seti ve filigran |
| `hesap/varlik/` | Yazı tipleri (orijinal OFL dosyaları + birleştirme betiği), ikonlar |
| `01-kurul-kalesi/kurul_kalesi_bolum.md` | Seslendirme, sahneler, caption, kaynakça, doğrulama tablosu |
| `01-kurul-kalesi/URETIM_TALIMATI.md` | 2D ve foto gerçekçi prompt'lar, teslim kuralları |
| `01-kurul-kalesi/uretim/` | Bulut üretim hattı: `gemini.py`, `kurgu.py`, `sahneler.json` |

## 4. Mac'teki dosyalar (`~/Desktop/Ordu-Sayfasi/01-Kurul-Kalesi/`)
- Paylaşım kopyaları (~22 MB): `2d/Kurul-Kalesi-2D-paylasim.mp4`, `foto/Kurul-Kalesi-Foto-paylasim.mp4`
- WhatsApp kopyaları (~8 MB): `2d/Kurul-Kalesi-2D-wa.mp4`, `foto/Kurul-Kalesi-Foto-wa.mp4`
- Ana dosyalar (126–165 MB): `2d/Kurul-Kalesi-2D.mp4`, `foto/Kurul-Kalesi-Foto.mp4`, eski paralaks sürüm `foto/Kurul-Kalesi-Foto-paralaks.mp4` (141 MB)
- Kontak sayfaları: `2d/Kontak-2d.jpg`, `foto/Kontak-foto.jpg`
- Sahne görselleri ve klipleri: `2d/img`, `foto/img`, `2d/vid`, `foto/vid`, ham Veo klipleri `foto/vid/veo/`
- Üretim betikleri: `_uretici/` (`build_reel.py`, `muzik.py`, `zamanlama.json`, `p25/` paralaks)
Ayrıntı: `MAC_OTURUMU_ORDU_KAYDI.md` bölüm 2.8.

## 5. Üretim yolları
**A · Mac (Tarihin Atölyesi oturumu)** — şu an çalışan yol
- Görsel: Flow, Nano Banana 2.1, 0 kredi, 768×1376 → 1080×1920
- Ses: `tts_pro3.py`, Pro Enceladus, Whisper kontrolü
- Hareket: Depth Anything V2 + `render_25d.py` paralaks; Veo 3.1 Flow'da
- Altyazı: PIL PNG bindirme (Mac'teki ffmpeg'de ASS yok)
- Teslim: Telegram ve uygulama (WhatsApp Web QR istiyor)

**B · Bulut (bu oturum, "Ordu Defteri" ortamı)** — hazır, kredi bekliyor
- Gemini API: Nano Banana Pro görsel, 2.5 Pro TTS Enceladus. Veo bu projede şimdilik yok.
- `uretim/kurgu.py`: ASS altyazı, sentez müzik, filigran, −14 LUFS
- Ortam: Instagram ve Gemini adresleri izinli; kurulum betiği paketleri ve yazı tiplerini hazırlıyor
- Eksik: Gemini projesinde ön ödemeli kredi ve anahtarın ortamın Network secrets bölümüne kaydı (Header `x-goog-api-key`)

## 6. Krediler ve maliyetler
| Kalem | Değer |
|---|---|
| Flow görsel | 0 kredi |
| Flow kredisi | 0 · 13 Kasım 18:10'da yenilenir |
| Yapay zeka kredisi (Flow) | 450 → 200 (Kurul Kalesi Veo sonrası) |
| Veo 3.1 Quality | 100 kredi / 8 sn klip |
| Veo 3.1 Fast | 20 kredi / 8 sn klip |
| Gemini API (bulut) | Ön ödeme bitti; yükleme bekleniyor |

## 7. Dersler
1. Pro Enceladus ~125 kelimeyi ~61 sn'de okuyor. 54 sn hedefi için metin 105–110 kelime olmalı.
2. Veo'da "goddess/tanrıça" kelimesi hata verdi, kelime çıkarılınca geçti.
3. Veo "no cuts" denmesine rağmen kendi içinde geçiş yapabiliyor; klip kontrol edilmeli.
4. Fast (20 kredi) ile Quality (100 kredi) arasında 5 kat fark var. Deneme için Fast, final için Quality.
5. Bulut oturumundan Mac oturumuna gönderilen mesajlar görünmüyor. Mac'e iş vermek için metni Mac oturumuna yapıştırmak gerekiyor.
6. Altyazı %70 yükseklikte bazı sahnelerde figürlerin üstüne biniyor; kontur sayesinde okunuyor.

## 8. Açık işler
1. Instagram hesabını aç (`hesap/KURULUM.md`).
2. Foto gerçekçi marka fotoğraflarını üret (`hesap/FOTO_MARKA.md` içindeki Mac mesajı).
3. Kurul Kalesi videolarını GitHub'a koy (aşağıdaki mesaj).
4. Kurul Kalesi videolarına filigran ekle; caption sonuna #ordudefteri.
5. Bulut üretimi için: Gemini ön ödeme kredisi + anahtarın Network secrets'a kaydı. Sohbete yazılan eski anahtarı sil.
6. Kybele için arşiv fotoğrafı izni (kazı heyeti, Valilik ya da Büyükşehir).
7. İlk hafta konuları: Onbinler / Kotyora, 1920'de il oluşu, Boztepe, Ulugöl, fındık harmanı, "Vatan yahut Silistre".

### Mac oturumuna yapıştırılacak mesaj (videolar GitHub'a)
```
Kurul Kalesi çıktılarını GitHub'a koy, onaylıyorum. Depo: https://github.com/alicantaze0-design/gizlilik , dal: claude/ordu-instagram-page-a2rs30 (yalnızca bu dal, depo herkese açık). Klasör: ordu/medya/01-kurul-kalesi/ — iki final videonun paylaşım kopyaları (son altyazı konumlu hâlleri), Kontak-2d.jpg, Kontak-foto.jpg, 2d/img ve foto/img görselleri, varsa Veo klipleri. 100 MB'ı aşan dosya koyma. Bir NOTLAR.md ekle: dosyalar, modeller (Flow, Pro Enceladus, Veo 3.1 Quality B1/B4/B6), süre, LUFS, kredi durumu. Push et ve commit hash'ini yaz.
```
