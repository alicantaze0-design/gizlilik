"""Ordu Defteri dinamik Reel müziği (sentez): 100 BPM, Dm-Bb-F-C, sahneye göre yoğunluk,
geçişlerde whoosh, kuşatmaya yükselen gerilim ve vuruş, sahne 5'te düşüş.
Kullanım: muzik_uret(sahne_sureleri, cikti_wav, bpm=100)"""
import numpy as np, wave

SR = 48000
RNG = np.random.default_rng(42)

def _env(n, a=0.002, d=0.3):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1.0) * np.exp(-t / d)

def kick(amp=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 85 * np.exp(-t * 30); ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 7.5); s[:150] += RNG.normal(0, 0.4, 150) * np.linspace(1, 0, 150)
    return amp * s

def hp(x, k=3):
    y = x.copy()
    for _ in range(k): y = np.diff(y, prepend=0)
    return y / (np.abs(y).max() + 1e-9)

def lp(x, w):
    return np.convolve(x, np.ones(w) / w, mode="same")

def snare(amp=1.0):
    n = int(0.22 * SR); t = np.arange(n) / SR
    s = 0.6 * hp(RNG.normal(0, 1, n), 1) * np.exp(-t * 22) + 0.5 * np.sin(2 * np.pi * 185 * t) * np.exp(-t * 30)
    return amp * s

def clap(amp=1.0):
    n = int(0.2 * SR); s = np.zeros(n); t = np.arange(n) / SR
    for o in (0, 0.011, 0.022):
        i = int(o * SR); m = n - i; s[i:] += hp(RNG.normal(0, 1, m), 2) * np.exp(-np.arange(m) / SR * 35)
    return amp * 0.5 * s

def hat(amp=1.0, uzun=False):
    n = int((0.12 if uzun else 0.045) * SR); t = np.arange(n) / SR
    return amp * 0.35 * hp(RNG.normal(0, 1, n), 4) * np.exp(-t * (18 if uzun else 70))

def tom(f, amp=1.0):
    n = int(0.35 * SR); t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.5 * np.exp(-t * 20))) / SR
    return amp * np.sin(ph) * np.exp(-t * 9)

def bas(f, sure, amp=1.0):
    n = int(sure * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * h * t) / h ** 1.3 for h in range(1, 7))
    return amp * lp(s, 24) * _env(n, 0.004, sure * 0.55)

def pluck(f, sure=0.32, amp=1.0):
    n = int(sure * SR); p = max(2, int(SR / f)); buf = RNG.uniform(-1, 1, p); out = np.zeros(n); i = 0
    while i < n:
        k = min(p, n - i); out[i:i + k] = buf[:k]; i += k
        buf = 0.996 * 0.5 * (buf + np.roll(buf, -1))
    return amp * out * np.linspace(1, 0.6, n)

def pad(frekanslar, sure, amp=1.0):
    n = int(sure * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f in frekanslar:
        for dt in (-0.004, 0.0, 0.004):
            s += sum(np.sin(2 * np.pi * f * (1 + dt) * h * t + h) / h ** 1.8 for h in range(1, 5))
    s = lp(s, 40); a = min(0.6, sure / 3)
    e = np.minimum(t / a, 1) * np.minimum((sure - t) / a, 1)
    return amp * s * np.clip(e, 0, 1) / (len(frekanslar) * 3)

def gurultu_supur(sure, f0, f1, f2=None, amp=1.0):
    """STFT ile bant geçiren süpürme: whoosh ve riser için."""
    n = int(sure * SR); x = RNG.normal(0, 1, n + 2048); out = np.zeros(n + 2048); win = np.hanning(2048)
    kare = list(range(0, n, 512)); frek = np.fft.rfftfreq(2048, 1 / SR)
    for j, s in enumerate(kare):
        u = j / max(len(kare) - 1, 1)
        fc = f0 * (f1 / f0) ** u if f2 is None else (f0 * (f1 / f0) ** (2 * u) if u < .5 else f1 * (f2 / f1) ** (2 * u - 1))
        X = np.fft.rfft(x[s:s + 2048] * win); X *= np.exp(-0.5 * (np.log(frek + 1) - np.log(fc)) ** 2 / 0.35 ** 2)
        out[s:s + 2048] += np.fft.irfft(X) * win
    out = out[:n]; return amp * out / (np.abs(out).max() + 1e-9)

def impact(amp=1.0):
    n = int(1.6 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (38 + 40 * np.exp(-t * 6)) * t) * np.exp(-t * 2.2)
    s += 0.5 * lp(RNG.normal(0, 1, n), 8) * np.exp(-t * 5)
    return amp * s / (np.abs(s).max() + 1e-9)

def topla(*xs):
    n = max(len(x) for x in xs); y = np.zeros(n)
    for x in xs: y[:len(x)] += x
    return y

def ekle(buf, x, t):
    i = int(t * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(len(buf), i + len(x))
    if j > i: buf[i:j] += x[:j - i]

# Sahne başına yoğunluk (1..8): kick, clap, hat, bas, pluck, pad, tom
YOGUN = {1: (1, 0, .6, .8, .5, .3, 0), 2: (1, .8, .7, .9, .6, .3, 0), 3: (1, .9, 1, 1, .9, .4, .3),
         4: (1.2, 1, 1, 1.1, 1, .8, 1), 5: (.4, 0, 0, 0, 0, .7, 0), 6: (.6, 0, .5, .6, 1, .7, 0),
         7: (1.1, 1, 1, 1, 1, .5, .5), 8: (1, .8, .8, 1, .9, .6, .3)}
AKOR = [(73.42, (293.66, 349.23, 440.0)), (58.27, (233.08, 293.66, 349.23)),
        (87.31, (349.23, 440.0, 523.25)), (65.41, (261.63, 329.63, 392.0))]

def muzik_uret(sureler, yol, bpm=100):
    beat = 60 / bpm; T = sum(sureler) + 1.5; N = int(T * SR)
    kanal = {k: np.zeros(N) for k in ("dr", "bas", "mel", "fx")}
    bas_t = np.cumsum([0] + list(sureler[:-1]))
    def sahne_at(t):
        for i in range(len(sureler) - 1, -1, -1):
            if t >= bas_t[i]: return i + 1
        return 1
    nb = int(T / (beat / 4))
    for k in range(nb):
        t = k * beat / 4; s = sahne_at(t); ki, cl, ha, ba, pl, pa, to = YOGUN.get(s, YOGUN[8])
        vurus = k // 4; on6 = k % 16; bar = int(t // (4 * beat)); kok, akor = AKOR[bar % 4]
        if k % 4 == 0:
            if ki and (vurus % 2 == 0 or s in (4, 7)): ekle(kanal["dr"], kick(ki), t)
            if s == 5 and vurus % 2 == 0: ekle(kanal["dr"], kick(0.5), t)
            if cl and vurus % 2 == 1: ekle(kanal["dr"], topla(clap(cl), snare(0.4 * cl)), t)
        if ha:
            if k % 2 == 0: ekle(kanal["dr"], hat(ha * (0.9 if k % 4 == 2 else 0.5)), t)
            elif s in (3, 4, 7): ekle(kanal["dr"], hat(ha * 0.35), t)
        if ba and k % 2 == 0: ekle(kanal["bas"], bas(kok, beat / 2 * 0.95, ba * (1 if k % 4 == 0 else 0.7)), t)
        if pl and (k % 2 == 0 or s in (3, 4, 6, 7)):
            f = akor[[0, 1, 2, 1][on6 % 4]] * (2 if on6 % 8 >= 4 else 1)
            ekle(kanal["mel"], pluck(f, 0.3, 0.45 * pl), t)
        if to and on6 in (12, 13, 14, 15) and bar % 2 == 1:
            ekle(kanal["dr"], tom([196, 165, 131, 110][on6 - 12], 0.8 * to), t)
        if on6 == 0 and pa:
            ekle(kanal["mel"], pad(akor, 4 * beat, 0.9 * pa), t)
    # Geçiş efektleri
    for i, b in enumerate(bas_t[1:], start=2):
        if i in (4, 6):
            r = 3.6 if i == 4 else 2.4
            ekle(kanal["fx"], gurultu_supur(r, 300, 6000, amp=0.5) * np.linspace(0, 1, int(r * SR)) ** 2, b - r)
            ekle(kanal["fx"], impact(1.0 if i == 4 else 0.6), b)
        else:
            ekle(kanal["fx"], gurultu_supur(0.6, 400, 3500, 800, amp=0.45) * np.hanning(int(0.6 * SR)), b - 0.35)
    ekle(kanal["fx"], impact(0.7), 0.0)
    son = sum(sureler) - 1.2; ekle(kanal["fx"], impact(0.8), son)
    # Son vuruştan sonra her şeyi sustur
    for k in ("dr", "bas", "mel"):
        i = int((son + 0.05) * SR); kanal[k][i:] *= np.exp(-np.arange(N - i) / SR * 6)
    m = 0.9 * kanal["dr"] + 0.8 * kanal["bas"] + 0.55 * kanal["mel"] + 0.6 * kanal["fx"]
    m = np.tanh(1.3 * m / (np.abs(m).max() + 1e-9)) ; m /= np.abs(m).max() + 1e-9
    L = m.copy(); R = np.roll(m, int(0.012 * SR)) * 0.9 + 0.1 * m  # hafif genişlik
    st = np.stack([L, R], 1) * 0.89
    with wave.open(yol, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    return yol
