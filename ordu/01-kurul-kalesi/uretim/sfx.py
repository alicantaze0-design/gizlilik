"""Ordu Defteri ses efektleri (sentez) ve Kurul Kalesi yerleşim planı.
Instagram mantığı: ilk saniyede dikkat çeken vuruş, her eylemde kısa ve net efekt,
anlatımın altında kalan ortam sesi; efektler anlatımı bastırmaz."""
import numpy as np, wave
from muzik_dinamik import SR, hp, lp, gurultu_supur, impact, ekle, topla

R = np.random.default_rng(7)
def t_(sure): return np.arange(int(sure * SR)) / SR
def norm(x, a=1.0): return a * x / (np.abs(x).max() + 1e-9)

def kilic(amp=1.0):
    """Metal şakırtısı: uyumsuz kısmi sesler + sıyırma."""
    t = t_(1.1); s = np.zeros_like(t)
    for f, d, a in [(523, 0.9, 1), (1307, 0.6, .7), (2473, 0.45, .55), (3891, 0.3, .4), (5210, 0.2, .3)]:
        s += a * np.sin(2 * np.pi * f * t * (1 + 0.002 * np.sin(2 * np.pi * 6 * t))) * np.exp(-t / d * 3)
    s[:int(.01 * SR)] += R.normal(0, 2, int(.01 * SR))
    syr = gurultu_supur(0.25, 3000, 9000, amp=.5) * np.hanning(int(.25 * SR))
    return norm(topla(syr, np.concatenate([np.zeros(int(.12 * SR)), s])), amp)

def mizrak(amp=1.0):
    """Mızrak savruluşu + saplanma (whoosh + tok darbe)."""
    w = gurultu_supur(0.45, 500, 4000, 1200, amp=.8) * np.hanning(int(.45 * SR))
    t = t_(0.35); dar = np.sin(2 * np.pi * (90 + 120 * np.exp(-t * 40)) * t) * np.exp(-t * 14)
    dar[:300] += R.normal(0, 1.2, 300) * np.linspace(1, 0, 300)
    return norm(np.concatenate([w, dar]), amp)

def tas_kirilma(amp=1.0, sure=1.4):
    """Taş kırılıp dökülme: tok çatlak + rastgele taş taneleri."""
    t = t_(sure); s = np.zeros_like(t)
    cat = lp(R.normal(0, 1, int(.08 * SR)), 3) * np.exp(-t_(.08) * 40); s[:len(cat)] += 1.5 * cat
    s[:int(.6 * SR)] += 0.8 * np.sin(2 * np.pi * 55 * t_(.6)) * np.exp(-t_(.6) * 6)
    for _ in range(70):
        i = int(R.uniform(0.03, sure * 0.85) * SR); n = int(R.uniform(.01, .04) * SR)
        if i + n < len(s): s[i:i + n] += R.uniform(.2, .8) * lp(R.normal(0, 1, n), R.integers(2, 9)) * np.exp(-np.arange(n) / SR * 90)
    return norm(s * np.exp(-t * 1.6), amp)

def tahta_cat(amp=1.0):
    """Yanmış kirişin çatırdayıp kırılması."""
    t = t_(1.2); s = np.zeros_like(t)
    for k in range(14):
        i = int((0.02 + 0.03 * k + R.uniform(0, .02)) * SR); n = int(.012 * SR)
        s[i:i + n] += R.uniform(.4, 1) * hp(R.normal(0, 1, n), 2)
    s[int(.5 * SR):int(.5 * SR) + int(.7 * SR)] += 0.9 * np.sin(2 * np.pi * 70 * t_(.7)) * np.exp(-t_(.7) * 5)
    return norm(s, amp)

def ates(sure, amp=1.0):
    """Yangın çıtırtısı: kahverengi gürültü + kıvılcım tıkırtıları."""
    n = int(sure * SR); s = lp(np.cumsum(R.normal(0, 1, n)) * 0.002, 200); s -= lp(s, 4000)
    for _ in range(int(sure * 22)):
        i = int(R.uniform(0, sure) * SR); m = int(.004 * SR)
        if i + m < n: s[i:i + m] += R.uniform(.05, .3) * hp(R.normal(0, 1, m), 3)
    e = np.minimum(t_(sure) / .4, 1) * np.minimum((sure - t_(sure)) / .6, 1)
    return norm(s * np.clip(e, 0, 1), amp)

def ruzgar(sure, amp=1.0):
    n = int(sure * SR); s = lp(R.normal(0, 1, n), 60)
    mod = 0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * t_(sure)) * np.sin(2 * np.pi * 0.07 * t_(sure) + 1)
    e = np.minimum(t_(sure) / 1.0, 1) * np.minimum((sure - t_(sure)) / 1.0, 1)
    return norm(s * mod * np.clip(e, 0, 1), amp)

def boru(amp=1.0, sure=1.6):
    """Savaş borusu: titreşimli bakır ton."""
    t = t_(sure); f = 116 * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t)) * (1 + 0.03 * np.minimum(t / .15, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR; s = sum(np.sin(h * ph) / h ** 1.1 for h in range(1, 10))
    e = np.minimum(t / .18, 1) * np.minimum((sure - t) / .5, 1)
    return norm(lp(s, 6) * np.clip(e, 0, 1), amp)

def adim(n_adim=4, aralik=0.42, amp=1.0):
    s = np.zeros(int((n_adim * aralik + .3) * SR))
    for k in range(n_adim):
        i = int(k * aralik * SR); n = int(.12 * SR)
        x = 0.7 * np.sin(2 * np.pi * 95 * t_(.12)) * np.exp(-t_(.12) * 35) + 0.4 * lp(R.normal(0, 1, n), 5) * np.exp(-t_(.12) * 45)
        s[i:i + n] += x * (0.8 + 0.2 * (k % 2))
    return norm(s, amp)

def damla(amp=1.0):
    t = t_(0.18); s = np.sin(2 * np.pi * (1400 - 3000 * t) * t) * np.exp(-t * 30)
    out = np.zeros(int(1.2 * SR)); out[:len(s)] += s
    for k, g in [(1, .45), (2, .25), (3, .12)]:
        i = int(k * .19 * SR); out[i:i + len(s)] += g * s
    return norm(out, amp)

def kup_tik(amp=1.0):
    t = t_(0.5); s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in [(780, 1, 18), (2120, .6, 25), (3490, .3, 35)])
    return norm(s, amp)

def bayrak(sure=1.5, amp=1.0):
    n = int(sure * SR); s = hp(R.normal(0, 1, n), 1); s = lp(s, 6)
    mod = np.abs(np.sin(2 * np.pi * 3.1 * t_(sure)) * np.sin(2 * np.pi * 1.3 * t_(sure) + .5)) ** 2
    return norm(s * mod, amp)

def firca(n_vurus=3, amp=1.0):
    s = np.zeros(int((n_vurus * .5 + .4) * SR))
    for k in range(n_vurus):
        i = int(k * .5 * SR); x = gurultu_supur(.38, 2500, 6000, amp=1) * np.hanning(int(.38 * SR))
        s[i:i + len(x)] += x
    return norm(s, amp)

def sikke(amp=1.0):
    """Sikke çınlaması + parıltı."""
    t = t_(1.6); s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in [(2093, 1, 2.2), (5440, .5, 3), (8150, .3, 4), (3136, .4, 2.6)])
    for k in range(6):
        i = int((.05 + .07 * k) * SR); n = int(.06 * SR)
        s[i:i + n] += .25 * np.sin(2 * np.pi * (6000 + 800 * k) * t_(.06)) * np.exp(-t_(.06) * 50)
    return norm(s, amp)

def kus(amp=1.0):
    out = np.zeros(int(1.4 * SR))
    for k in range(4):
        t = t_(.11); f = 3500 + 900 * np.sin(2 * np.pi * 18 * t); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.hanning(len(t))
        i = int((.15 + .28 * k + R.uniform(0, .05)) * SR); out[i:i + len(s)] += s
    return norm(out, amp)

def pop(amp=1.0):
    t = t_(.12); return norm(np.sin(2 * np.pi * (900 - 2500 * t) * t) * np.exp(-t * 40), amp)

# Plan: sahne -> [(efekt, sahne içi saniye ya da oran (<1), kazanç)]
# "son-x": sahne sonundan x sn önce
PLAN = {
 1: [("impact", 0.0, .9), ("ruzgar", 0.0, .35), ("ates", 0.15, .45), ("kus", .7, .25)],
 2: [("boru", 0.25, .5), ("bayrak", 0.35, .45)],
 3: [("adim", 0.08, .5), ("damla", .45, .45), ("kup_tik", .7, .5), ("kup_tik", .76, .35)],
 4: [("boru", 0.02, .55), ("mizrak", .18, .7), ("mizrak", .30, .6), ("kilic", .42, .65), ("kilic", .55, .55),
     ("tas_kirilma", .68, .75), ("ates", .2, .45), ("kilic", .85, .5)],
 5: [("tahta_cat", .08, .7), ("ates", 0.0, .35), ("ruzgar", .3, .35)],
 6: [("firca", .12, .5), ("sikke", .62, .7), ("kus", .85, .2)],
 7: [("ruzgar", 0.0, .25), ("kus", .3, .3), ("adim", .55, .3)],
 8: [("sikke", .1, .55), ("pop", "son-1.6", .35)],
}
URET = {"kilic": kilic, "mizrak": mizrak, "tas_kirilma": tas_kirilma, "tahta_cat": tahta_cat, "boru": boru,
        "adim": adim, "damla": damla, "kup_tik": kup_tik, "bayrak": bayrak, "firca": firca, "sikke": sikke,
        "kus": kus, "pop": pop, "impact": impact}

def sfx_uret(sureler, yol):
    T = sum(sureler) + 2; buf = np.zeros(int(T * SR)); bas = np.cumsum([0] + list(sureler[:-1]))
    for sahne, liste in PLAN.items():
        if sahne > len(sureler): continue
        b, d = bas[sahne - 1], sureler[sahne - 1]
        for ad, an, g in liste:
            t = d - float(an.split("-")[1]) if isinstance(an, str) else (an * d if an < 1 else an)
            if ad == "ates": x = ates(max(1.0, d - t), g)
            elif ad == "ruzgar": x = ruzgar(max(1.5, d - t), g)
            else: x = URET[ad](amp=g)
            ekle(buf, x, b + t)
    buf = np.tanh(1.2 * buf) / np.tanh(1.2)
    st = np.stack([buf, np.roll(buf, int(.008 * SR))], 1) * 0.85
    with wave.open(yol, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())
    return yol
