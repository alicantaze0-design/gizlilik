# Ordu Defteri · DEVAM (Mac oturumu için devir dosyası)
Bu dosyayı okuyan oturum, Ordu Defteri projesinin **ana oturumudur**. Tarihin Atölyesi gibi Ali Can'ın Mac'inde çalışır.
Bulut oturumu "Ordu Defteri" (gizlilik deposu) bu işi buraya devretti. 08.11.2026.

## 0. İlk açılışta yap
1. Depoyu yerel klasöre al (yoksa):
   ```
   cd ~/Desktop/Ordu-Sayfasi
   git clone -b claude/ordu-instagram-page-a2rs30 https://github.com/alicantaze0-design/gizlilik.git repo
   ```
   Varsa: `cd ~/Desktop/Ordu-Sayfasi/repo && git pull`
2. Sırayla oku: `repo/ordu/README.md` (proje dosyası), `repo/ordu/MAC_OTURUMU_ORDU_KAYDI.md` (Kurul Kalesi Mac üretim ayrıntıları), `repo/ordu/ORDU_SAYFASI_ONERILER.md`, `repo/ordu/hesap/KURULUM.md`, `repo/ordu/hesap/FOTO_MARKA.md`.
3. Hafızaya proje notu yaz (Ordu Defteri, Tarihin Atölyesi'nden ayrı; ana klasör `~/Desktop/Ordu-Sayfasi`; depo dalı yukarıda). Mevcut not: `project_ordu_instagram_sayfasi.md` — "Ordu Defteri" adıyla güncelle.
4. Python ortamı: `cd repo/ordu/hesap/varlik && python3 -m pip install --user fonttools brotli cairosvg && python3 fontlar_hazirla.py` (Merriweather ve Source Sans 3 Türkçe TTF'leri hazırlar).

## 1. Kesinleşen kararlar
- Ad: **Ordu Defteri**, kullanıcı adı **@ordudefteri** (hesap henüz açılmadı; rehber `hesap/KURULUM.md`).
- Ana görsel dil: **foto gerçekçi**. 2D yalnızca yedek/deneme.
- Yazı tipi ailesi: **Merriweather Black** (altyazı, filigran, başlıklar) + Source Sans 3 (küçük metin).
- Filigran: üst orta, "ordu defteri", ~330 px genişlik (1080'de), %80 opaklık. Dosya: `hesap/gorseller/filigran.png`.
- Altyazı: Merriweather Black 68, beyaz, kalın siyah kontur, vurgular sarı (#FFD700), ekranın ~%70 yüksekliğinde, hafif "pop" girişli.
- Seslendirme: **Pro Enceladus** (`~/Desktop/Bilim-Adamlari-Atlasi-Video/tts_pro3.py`, SES=Enceladus).
- Müzik ve kurgu: **dinamik** (100 BPM, sahne geçişleri vuruşa oturur, her sahnenin ortasında %12 yakınlaştırma kesmesi), **ses efektleri** sahnelere göre.
- Teslim: Telegram + uygulama (WhatsApp Web QR istiyor; Ali Can QR okutursa WhatsApp "Kendine mesaj").
- Hiçbir şey Ali Can'ın onayı olmadan yayımlanmaz.

## 2. Hazır araçlar (depoda)
| Yol | Ne yapar |
|---|---|
| `01-kurul-kalesi/uretim/kurgu.py` | Bölüm kurgusu: TTS süresine göre zamanlama, görsel/klip segmentleri, dinamik müzik + efekt miksi, ASS altyazı, filigran, −14 LUFS, kontak sayfası, kapak. `--sakin` eski düz kurgu. |
| `01-kurul-kalesi/uretim/muzik_dinamik.py` | Sentez dinamik müzik (Dm-Bb-F-C, 100 BPM, sahne yoğunlukları, riser/impact) |
| `01-kurul-kalesi/uretim/sfx.py` | Sentez efektler + Kurul Kalesi yerleşim planı (`PLAN`) |
| `01-kurul-kalesi/uretim/gemini.py` | Gemini API (görsel/TTS/Veo) — bulut içindi; Mac'te Flow + tts_pro3 kullan |
| `hesap/marka.py`, `hesap/foto_marka.py` | 2D ve foto gerçekçi marka setleri (profil, öne çıkanlar, açılış karuseli) |

**kurgu.py'yi Mac'te kullanma notu:** Mac'teki ffmpeg'de libass/ASS yok. İki yol: (a) `brew install ffmpeg` ile libass'lı ffmpeg kur ya da (b) altyazıyı Kurul Kalesi'ndeki gibi PIL PNG bindirmeyle yap (`~/Desktop/Ordu-Sayfasi/01-Kurul-Kalesi/_uretici/build_reel.py`), yazı tipini Merriweather Black yap. Girdi düzeni: `<cikti>/tts/NN.wav`, `<cikti>/<surum>/img/NN.png`, `<cikti>/<surum>/vid/NN.mp4` (varsa klip, yoksa görselden Ken Burns). Mevcut dosyalar yeniden üretilmez.

## 3. Sıradaki işler (öncelik sırası)
1. **Kurul Kalesi · dinamik final (foto gerçekçi önce, sonra 2D):**
   - Enerjik seslendirme: tts_pro3, Enceladus, TON şu metin:
     "Aşağıdaki Türkçe metni Instagram Reels için enerjik ve merak uyandıran bir belgesel anlatıcısı gibi oku. Tempo canlı ve akıcı olsun, normal konuşmadan biraz hızlı; cümleler arasında kısa nefes. Sayıları ve yer adlarını hafifçe öne çıkar. İlk cümlede sır açıklıyormuş gibi dikkat çeken bir ton, kuşatma cümlesinde gerilim, Kybele cümlesinde şaşırtıcı bir keşif hissi, son soruda samimi merak olsun. Cümle sonlarındaki -yor, -dı, -di eklerini vurgulama, tonu yapay yükseltip düşürme; abartılı reklam sesi olmasın."
     Whisper kontrolü. Hedef süre ≤ 55 sn (gerekirse metni 105–110 kelimeye kısalt, Ali Can'a göster).
   - Klipler: foto için Veo B1/B4/B6 + paralaks B2/B3/B5/B7/B8 (`_uretici/p25/vid/`).
   - kurgu.py (dinamik) ile kur; filigran + Merriweather altyazı + müzik + efektler. Bulut önizlemeleri Ali Can'da: "dinamik müzik" ve "müzik + efekt".
   - Teslim Telegram + uygulama; ayrıca `ordu/medya/01-kurul-kalesi/` altına push.
2. **Foto gerçekçi marka seti:** `hesap/FOTO_MARKA.md` ve `hesap/foto_promptlar.json` → Flow (Nano Banana, 0 kredi) ile 9 fotoğraf (profil 4 deneme) → `foto_marka.py` ile birleştir → Ali Can'a göster.
3. **Instagram hesabı:** Ali Can açınca açılış karuseli + Kurul Kalesi Reel'i (rehber `hesap/KURULUM.md`). Paylaşım saati 20.30.
4. **İlk hafta konuları:** Onbinler/Kotyora, 1920'de il oluşu, Boztepe, Ulugöl, fındık harmanı, "Vatan yahut Silistre" (OBKT arşivi). Her biri için Kurul Kalesi bölüm dosyası biçiminde senaryo + kaynakça + doğrulama tablosu; üretime Ali Can onayıyla geç.

## 4. Krediler (08.11)
Flow görsel 0 kredi · Flow kredisi 0 (13 Kasım 18:10 yenilenir) · yapay zeka kredisi 200 · Veo 3.1 Quality 100/klip, Fast 20/klip · Gemini API (bulut) ön ödemesi bitti.

## 5. Dersler
`MAC_OTURUMU_ORDU_KAYDI.md` bölüm 4.2 ve `README.md` bölüm 7. En önemlileri: "goddess/tanrıça" kelimesi Veo'yu durduruyor; Enceladus ~125 kelimeyi ~61 sn'de okuyor; Veo "no cuts" dese de geçiş yapabiliyor; Flow'da uzun JS döngüleri 45 sn'de zaman aşımına düşüyor.
