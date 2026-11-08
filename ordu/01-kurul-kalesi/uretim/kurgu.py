"""Kurul Kalesi Reel üretimi.
Kullanım: python3 kurgu.py --cikti DIR [--surum 2d|foto|hepsi] [--veo] [--test]
--test: API çağırmadan yer tutucu görsel ve sessiz anlatımla hattı dener."""
import argparse, json, math, os, re, shutil, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, SR = 1080, 1920, 30, 48000
BURADA = os.path.dirname(os.path.abspath(__file__))
VERI = json.load(open(os.path.join(BURADA, "sahneler.json"), encoding="utf-8"))
SAHNE = VERI["sahneler"]

def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(" ".join(a[:6]) + "...\n" + r.stderr[-1500:])
    return r.stdout

def sure(yol):
    v = sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", yol).strip()
    try: return float(v)
    except ValueError: return 0.0

# ---------- 1. Seslendirme ----------
def seslendirme(d, test):
    os.makedirs(f"{d}/tts", exist_ok=True)
    model = None
    for s in SAHNE:
        y = f"{d}/tts/{s['no']:02d}.wav"
        if os.path.exists(y): continue
        if test:
            n = int(SR * (0.42 * len(s["anlatim"].split()) + 0.4))
            with wave.open(y, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(b"\0\0" * n)
        else:
            import gemini
            model = model or gemini.model_sec(["2.5-pro-preview-tts", "pro-tts", "2.5-pro-tts", "tts"], "generateContent")
            print(f"  TTS {s['no']} ({model}, Enceladus)")
            gemini.ses(model, s["anlatim"], y)
        if test: continue
        # sessizlik kırp + standart format
        t = y + ".tmp.wav"
        sh("ffmpeg", "-y", "-i", y, "-af",
           "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,aresample=48000",
           "-ac", "1", t)
        if sure(t) > 0.3: os.replace(t, y)
        else: os.remove(t)
    return [sure(f"{d}/tts/{s['no']:02d}.wav") for s in SAHNE]

DINAMIK = True; BPM = 100
def zamanlama(ses_sureleri):
    ON, ARA, SON = (0.15, 0.3, 1.6) if DINAMIK else (0.20, 0.45, 1.4)
    yarim = 60 / BPM / 2
    plan, t = [], 0.0
    for i, v in enumerate(ses_sureleri):
        dur = ON + v + (SON if i == len(ses_sureleri) - 1 else ARA)
        if DINAMIK: dur = math.ceil(dur / yarim) * yarim
        plan.append({"bas": t, "ses_bas": t + ON, "ses": v, "sure": dur}); t += dur
    return plan

# ---------- 2. Görseller ----------
def gorseller(d, surum, test):
    os.makedirs(f"{d}/{surum}/img", exist_ok=True)
    model = None
    for s in SAHNE:
        y = f"{d}/{surum}/img/{s['no']:02d}.png"
        if os.path.exists(y): continue
        if test:
            im = Image.new("RGB", (768, 1344), (60 + 20 * s["no"], 90, 120)); dr = ImageDraw.Draw(im)
            dr.text((40, 600), f"{surum} sahne {s['no']}", fill="white"); im.save(y)
        else:
            import gemini
            model = model or gemini.model_sec(["gemini-3-pro-image", "gemini-2.5-flash-image", "image"], "generateContent")
            print(f"  görsel {surum} {s['no']} ({model})")
            gemini.gorsel(model, VERI["stil"][surum] + "\n\nScene: " + s[surum]["prompt"], y)

def veo_klipler(d, surum):
    import gemini
    os.makedirs(f"{d}/{surum}/vid", exist_ok=True)
    model, sonuc = None, {}
    for s in SAHNE:
        if not s[surum]["veo"]: continue
        y = f"{d}/{surum}/vid/{s['no']:02d}.mp4"
        if not os.path.exists(y):
            try:
                model = model or gemini.model_sec(["veo-3.1-fast", "veo-3.0-fast", "veo-3.1", "veo-3", "veo"], "predictLongRunning")
                print(f"  Veo {surum} {s['no']} ({model})")
                stil = "Photorealistic cinematic." if surum == "foto" else "Keep the 2D ink-and-watercolor cartoon style exactly; animate gently."
                gemini.video(model, f"{stil} {s[surum]['hareket']} No text, no subtitles.", f"{d}/{surum}/img/{s['no']:02d}.png", y)
            except Exception as e:
                print(f"  Veo {s['no']} atlandı: {e}", file=sys.stderr); sonuc[s["no"]] = f"atlandı: {str(e)[:200]}"; continue
        sonuc[s["no"]] = "veo"
    return sonuc

# ---------- 3. Sahne segmentleri ----------
HAREKET = ["in", "up", "in", "out", "down", "in", "up", "in"]
def segment(d, surum, s, dur):
    out = _segment(d, surum, s, dur)
    if not DINAMIK or dur < 3: return out
    yarim = 60 / BPM / 2; kes = round((dur / 2) / yarim) * yarim
    son = out.replace(".mp4", "_d.mp4")
    fc = (f"[0:v]split[a][b];[a]trim=0:{kes},setpts=PTS-STARTPTS[a1];"
          f"[b]trim={kes}:{dur},setpts=PTS-STARTPTS,scale=iw*1.12:ih*1.12,crop={W}:{H},setsar=1[b1];[a1][b1]concat=n=2:v=1[v]")
    sh("ffmpeg", "-y", "-i", out, "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", son)
    return son

def _segment(d, surum, s, dur):
    n = s["no"]; out = f"{d}/{surum}/seg/{n:02d}.mp4"; os.makedirs(os.path.dirname(out), exist_ok=True)
    vid = f"{d}/{surum}/vid/{n:02d}.mp4"
    frames = int(round(dur * FPS))
    if os.path.exists(vid):
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
              f"tpad=stop_mode=clone:stop_duration={dur},trim=duration={dur},setsar=1,format=yuv420p")
        sh("ffmpeg", "-y", "-i", vid, "-an", "-vf", vf, "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out)
        return out
    img = f"{d}/{surum}/img/{n:02d}.png"
    D = max(frames - 1, 1); h = HAREKET[(n - 1) % len(HAREKET)]
    z = {"in": f"1+0.10*on/{D}", "out": f"1.10-0.10*on/{D}"}.get(h, "1.08")
    x = "iw/2-(iw/zoom/2)"
    y = {"up": f"(ih-ih/zoom)*(1-on/{D})", "down": f"(ih-ih/zoom)*(on/{D})"}.get(h, "ih/2-(ih/zoom/2)")
    vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
          f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p")
    sh("ffmpeg", "-y", "-loop", "1", "-i", img, "-vf", vf, "-frames:v", str(frames),
       "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out)
    return out

# ---------- 4. Müzik ----------
def muzik(plan, yol):
    T = plan[-1]["bas"] + plan[-1]["sure"]; N = int(T * SR); t = np.arange(N) / SR
    def zarf(degerler, ramp=0.6):
        g = np.zeros(N)
        for p, v in zip(plan, degerler):
            a, b = int(p["bas"] * SR), int((p["bas"] + p["sure"]) * SR); g[a:b] = v
        k = int(ramp * SR); ker = np.ones(k) / k
        return np.convolve(g, ker, mode="same")
    # Dron: D2-A2-D3, yumuşak testere
    dron = np.zeros(N)
    for f0, a in [(73.42, 1.0), (110.0, 0.7), (146.83, 0.5)]:
        for h in range(1, 9):
            dron += a * np.sin(2 * np.pi * f0 * h * t + h) / h ** 1.6
    dron *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.18 * t)
    # Yüksek tel pad (sahne 6+)
    pad = sum(np.sin(2 * np.pi * f * t * (1 + 0.003 * np.sin(2 * np.pi * 5 * t))) for f in (293.66, 349.23, 440.0))
    # Davul: 72 BPM tok vuruş
    davul = np.zeros(N); beat = 60 / 72; L = int(0.45 * SR); tt = np.arange(L) / SR
    vur = np.sin(2 * np.pi * (45 + 50 * np.exp(-tt * 18)) * tt) * np.exp(-tt * 7)
    vur[:200] += np.random.default_rng(1).normal(0, 0.3, 200) * np.linspace(1, 0, 200)
    for i in range(int(T / beat)):
        a = int(i * beat * SR)
        for off, amp in ([(0, 1.0)] + ([(beat / 2, 0.6)] if i % 2 else [])):
            s = a + int(off * SR)
            if s + L < N: davul[s:s + L] += amp * vur
    g_dron = zarf([0.5, 0.5, 0.6, 1.0, 0.0, 0.35, 0.5, 0.45])
    g_davul = zarf([0.45, 0.5, 0.6, 1.0, 0.0, 0.0, 0.3, 0.2], 0.3)
    g_pad = zarf([0, 0, 0, 0, 0, 0.8, 0.7, 0.8], 2.0)
    m = 0.35 * dron * g_dron + 0.9 * davul * g_davul + 0.12 * pad * g_pad
    m = np.convolve(m, np.ones(6) / 6, mode="same")  # hafif yumuşatma
    m = m / (np.abs(m).max() + 1e-9) * 0.9
    st = np.stack([m, m], 1)
    with wave.open(yol, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

# ---------- 5. Ses miksi ----------
def miks(d, plan, test):
    T = plan[-1]["bas"] + plan[-1]["sure"]
    ses = np.zeros(int(T * SR) + SR)
    for s, p in zip(SAHNE, plan):
        with wave.open(f"{d}/tts/{s['no']:02d}.wav") as w:
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32767
        a = int(p["ses_bas"] * SR); ses[a:a + len(x)] += x
    with wave.open(f"{d}/anlatim.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(ses, -1, 1) * 32767).astype(np.int16).tobytes())
    if DINAMIK:
        import muzik_dinamik, sfx
        sureler = [p["sure"] for p in plan]
        muzik_dinamik.muzik_uret(sureler, f"{d}/muzik.wav", bpm=BPM); sfx.sfx_uret(sureler, f"{d}/sfx.wav")
        fc = ("[1:a]volume=-17dB[m];[2:a]volume=-15dB[x];[0:a]aformat=channel_layouts=stereo,asplit=3[v][vs1][vs2];"
              "[m][vs1]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=350[md];"
              "[x][vs2]sidechaincompress=threshold=0.06:ratio=2.5:attack=10:release=250[xd];"
              "[v][md][xd]amix=inputs=3:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
        girdiler = ["-i", f"{d}/anlatim.wav", "-i", f"{d}/muzik.wav", "-i", f"{d}/sfx.wav"]
    else:
        muzik(plan, f"{d}/muzik.wav")
        fc = ("[1:a]volume=-21dB[m];[0:a]aformat=channel_layouts=stereo[v];"
              "[m][v]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];"
              "[v][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
        girdiler = ["-i", f"{d}/anlatim.wav", "-i", f"{d}/muzik.wav"]
    sh("ffmpeg", "-y", *girdiler, "-filter_complex", fc,
       "-map", "[a]", "-ar", "48000", "-t", f"{T:.3f}", f"{d}/miks.wav")

# ---------- 6. Altyazı ----------
def tr_kucuk(s): return s.replace("İ", "i").replace("I", "ı").lower()
def temiz(w): return re.sub(r"[^\wçğıöşüâî-]", "", tr_kucuk(w))
def ass_zaman(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
def altyazi(plan, yol):
    bas = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n"
           "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
           "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
           "Alignment, MarginL, MarginR, MarginV, Encoding\n"
           "Style: A,Merriweather Black,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,5,3,2,70,70,560,1\n\n"
           "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    satir = []
    for s, p in zip(SAHNE, plan):
        kelimeler = s["anlatim"].split()
        tokens = set()
        for v in s["vurgu"]: tokens |= {temiz(x) for x in v.split() if temiz(x)}
        gruplar, g = [], []
        for k in kelimeler:
            g.append(k)
            if len(g) >= 3 or len(" ".join(g)) >= 16 or k[-1] in ".?!,:":
                gruplar.append(g); g = []
        if g: gruplar.append(g)
        toplam = sum(len(" ".join(x)) for x in gruplar); t = p["ses_bas"]
        for x in gruplar:
            dt = p["ses"] * len(" ".join(x)) / toplam
            parca = []
            for k in x:
                c = temiz(k)
                sari = c in tokens or any(len(tk) >= 4 and c.startswith(tk) for tk in tokens)
                parca.append("{\\c&H0000D7FF&}" + k + "{\\c&H00FFFFFF&}" if sari else k)
            satir.append(f"Dialogue: 0,{ass_zaman(t)},{ass_zaman(t + dt)},A,,0,0,0,,{{\\fscx86\\fscy86\\t(0,90,\\fscx100\\fscy100)}}{' '.join(parca)}")
            t += dt
    open(yol, "w", encoding="utf-8").write(bas + "\n".join(satir) + "\n")

# ---------- 7. Kontak sayfası ve kapak ----------
def kontak(d, surum, yol):
    w, h, pad = 270, 480, 10
    sheet = Image.new("RGB", (4 * w + 5 * pad, 2 * h + 3 * pad), "#111")
    for i, s in enumerate(SAHNE):
        im = Image.open(f"{d}/{surum}/img/{s['no']:02d}.png").convert("RGB").resize((w, h))
        sheet.paste(im, (pad + (i % 4) * (w + pad), pad + (i // 4) * (h + pad)))
    sheet.save(yol, quality=88)

def kapak(d, surum, yol):
    im = Image.open(f"{d}/{surum}/img/01.png").convert("RGB").resize((W, H))
    dr = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 92)
    for i, (txt, renk) in enumerate([("2.000 yıl önce yandı.", "white"), ("Kimse geri dönmedi.", "#FFD700")]):
        bw = dr.textlength(txt, font=f); y = 1180 + i * 120
        dr.text(((W - bw) / 2, y), txt, font=f, fill=renk, stroke_width=6, stroke_fill="black")
    im.save(yol, quality=90)

# ---------- Ana akış ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cikti", required=True); ap.add_argument("--surum", default="hepsi")
    ap.add_argument("--veo", action="store_true"); ap.add_argument("--test", action="store_true")
    ap.add_argument("--sakin", action="store_true", help="eski sakin müzik ve düz kurgu")
    ap.add_argument("--filigran", default=os.path.join(BURADA, "../../hesap/gorseller/filigran.png"))
    a = ap.parse_args(); d = a.cikti; os.makedirs(d, exist_ok=True)
    global DINAMIK; DINAMIK = not a.sakin
    surumler = ["2d", "foto"] if a.surum == "hepsi" else [a.surum]
    if not a.test: sys.path.insert(0, BURADA)
    print("1) Seslendirme"); ses_s = seslendirme(d, a.test); plan = zamanlama(ses_s)
    print("   süreler:", [round(x, 1) for x in ses_s], "toplam", round(plan[-1]["bas"] + plan[-1]["sure"], 1), "sn")
    print("2) Ses miksi + altyazı"); miks(d, plan, a.test); altyazi(plan, f"{d}/altyazi.ass")
    rapor = {"sureler": ses_s}
    for v in surumler:
        print(f"3) Görseller [{v}]"); gorseller(d, v, a.test)
        if a.veo and not a.test: print(f"4) Veo [{v}]"); rapor[f"veo_{v}"] = veo_klipler(d, v)
        print(f"5) Kurgu [{v}]")
        segs = [segment(d, v, s, p["sure"]) for s, p in zip(SAHNE, plan)]
        lst = f"{d}/{v}/liste.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in segs))
        sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{d}/{v}/goruntu.mp4")
        ad = {"2d": "2D", "foto": "Foto-Gercekci"}[v]
        son = f"{d}/Kurul-Kalesi-{ad}.mp4"
        fil = os.path.abspath(a.filigran) if a.filigran and os.path.exists(a.filigran) else None
        fd = os.path.abspath(os.path.join(BURADA, "../../hesap/varlik/fonts"))
        fc = (f"[0:v]ass={d}/altyazi.ass:fontsdir={fd}[v1];[2:v]scale=330:-1,format=rgba,colorchannelmixer=aa=0.8[wm];"
              f"[v1][wm]overlay=(W-w)/2:120[v]") if fil else f"[0:v]ass={d}/altyazi.ass:fontsdir={fd}[v]"
        sh("ffmpeg", "-y", "-i", f"{d}/{v}/goruntu.mp4", "-i", f"{d}/miks.wav", *(["-i", fil] if fil else []),
           "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "21",
           "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
           "-movflags", "+faststart", son)
        kontak(d, v, f"{d}/Kurul-Kalesi-{ad}-kareler.jpg"); kapak(d, v, f"{d}/Kurul-Kalesi-{ad}-kapak.jpg")
        rapor[v] = {"dosya": son, "sure": round(sure(son), 1), "MB": round(os.path.getsize(son) / 1e6, 1)}
        print("   ->", rapor[v])
    json.dump(rapor, open(f"{d}/rapor.json", "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
