"""Gemini API yardımcıları: görsel (Nano Banana), seslendirme (Pro TTS Enceladus), video (Veo).
Anahtar ağ vekili tarafından x-goog-api-key başlığına eklenir; kodda anahtar yok."""
import base64, json, os, sys, time, wave
import requests

BASE = "https://generativelanguage.googleapis.com/v1beta"
S = requests.Session()
S.headers["Content-Type"] = "application/json"

def _post(path, body, timeout=300):
    r = S.post(f"{BASE}/{path}", data=json.dumps(body), timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f"{path} -> HTTP {r.status_code}: {r.text[:600]}")
    return r.json()

def modeller():
    out, tok = [], None
    while True:
        r = S.get(f"{BASE}/models", params={"pageSize": 1000, **({"pageToken": tok} if tok else {})}, timeout=60)
        r.raise_for_status(); j = r.json()
        out += j.get("models", []); tok = j.get("nextPageToken")
        if not tok: return out

def model_sec(anahtarlar, yontem):
    """Listeden ilk eşleşen modeli seç (anahtarlar öncelik sırasıyla)."""
    ms = modeller()
    for a in anahtarlar:
        for m in ms:
            ad = m["name"].split("/")[-1]
            if a in ad and yontem in m.get("supportedGenerationMethods", []):
                return ad
    raise RuntimeError(f"Model bulunamadı: {anahtarlar} / {yontem}")

def gorsel(model, prompt, cikti, oran="9:16", deneme=3):
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": oran}}}
    for i in range(deneme):
        try:
            j = _post(f"models/{model}:generateContent", body)
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    open(cikti, "wb").write(base64.b64decode(p["inlineData"]["data"]))
                    return cikti
            raise RuntimeError("Görsel dönmedi: " + json.dumps(j)[:400])
        except Exception as e:
            print(f"  görsel deneme {i+1} hata: {e}", file=sys.stderr); time.sleep(5 * (i + 1))
    raise RuntimeError(f"Görsel üretilemedi: {cikti}")

TON = ("Aşağıdaki Türkçe metni belgesel anlatıcısı gibi oku: sakin, sıcak, merak uyandıran ve doğal. "
       "Cümle sonlarındaki -yor, -yorsun, -dı, -di gibi ekleri vurgulama; tonu yükseltip düşürme; "
       "cümleleri düz, sakin ve doğal bitir. Soru cümlelerinde hafif merak tonu kullan. Metin:\n")

def ses(model, metin, cikti, ses_adi="Enceladus", deneme=3):
    body = {"contents": [{"parts": [{"text": TON + metin}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": ses_adi}}}}}
    for i in range(deneme):
        try:
            j = _post(f"models/{model}:generateContent", body)
            p = next(p for p in j["candidates"][0]["content"]["parts"] if "inlineData" in p)
            pcm = base64.b64decode(p["inlineData"]["data"])
            mime = p["inlineData"].get("mimeType", "")
            rate = int(mime.split("rate=")[1].split(";")[0]) if "rate=" in mime else 24000
            with wave.open(cikti, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
            return cikti
        except Exception as e:
            print(f"  ses deneme {i+1} hata: {e}", file=sys.stderr); time.sleep(5 * (i + 1))
    raise RuntimeError(f"Ses üretilemedi: {cikti}")

def video(model, prompt, gorsel_yolu, cikti, sure=8, oran="9:16"):
    inst = {"prompt": prompt}
    if gorsel_yolu:
        inst["image"] = {"bytesBase64Encoded": base64.b64encode(open(gorsel_yolu, "rb").read()).decode(),
                         "mimeType": "image/png"}
    body = {"instances": [inst], "parameters": {"aspectRatio": oran, "durationSeconds": sure}}
    op = _post(f"models/{model}:predictLongRunning", body)
    ad = op["name"]
    for _ in range(90):
        time.sleep(10)
        r = S.get(f"{BASE}/{ad}", timeout=60); r.raise_for_status(); j = r.json()
        if j.get("done"):
            if "error" in j: raise RuntimeError(f"Veo hata: {j['error']}")
            resp = j.get("response", {})
            ornek = (resp.get("generateVideoResponse", {}).get("generatedSamples")
                     or resp.get("generatedVideos") or resp.get("videos"))
            if not ornek: raise RuntimeError("Veo video dönmedi: " + json.dumps(j)[:600])
            v = ornek[0].get("video", ornek[0])
            if "uri" in v:
                d = S.get(v["uri"], timeout=300, allow_redirects=True); d.raise_for_status()
                open(cikti, "wb").write(d.content)
            else:
                open(cikti, "wb").write(base64.b64decode(v["bytesBase64Encoded"]))
            return cikti
    raise RuntimeError("Veo zaman aşımı")
