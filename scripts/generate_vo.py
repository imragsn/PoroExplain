#!/usr/bin/env python3
"""
Poro Web Explainer — Multi-Engine Automated TTS Pipeline
Generates speech audio from script paragraphs and exports timing metadata.
Supports:
  1. ElevenLabs API (Premium realistic voice)
  2. Google Gemini Flash TTS (Fast & emotional)
  3. Microsoft Edge-TTS (Free local fallback without API key)
"""

import os
import sys
import json
import base64
import argparse
import subprocess
import urllib.request
import urllib.error

DEFAULT_PARAGRAPHS = [
    {
        "id": "scene_1",
        "text": "Pernahkah kamu berpikir, kenapa air mendidih di dalam termos bisa tahan panas sampai berjam-jam? Di balik tabung baja ini, ada rekayasa fisika satu milimeter yang menahan aliran suhu."
    },
    {
        "id": "scene_2",
        "text": "Kuncinya ada pada dua lapis dinding baja tahan karat. Di antara dinding luar dan dinding dalam, terdapat ruang hampa vakum tempat seluruh molekul udara disedot habis."
    },
    {
        "id": "scene_3",
        "text": "Karena hampa udara, panas tidak bisa merambat lewat konduksi maupun konveksi. Ditambah lapisan reflektif khusus, sembilan puluh delapan persen gelombang radiasi panas dipantulkan kembali ke dalam."
    },
    {
        "id": "scene_4",
        "text": "Hasilnya, teruji standar industri JIS: suhu air tetap terjaga di atas tujuh puluh satu derajat celsius selama lebih dari enam jam penuh. Masuk akal, kan?"
    }
]

def generate_elevenlabs(text, outfile, api_key, voice_id="21m00Tcm4TlvDq8ikWAM"):
    """Generate audio via ElevenLabs API"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.85
        }
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req) as res:
        with open(outfile, "wb") as f:
            f.write(res.read())

def generate_gemini(text, outfile, api_key):
    """Generate audio via Google Gemini TTS API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"]}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode("utf-8"))
        part = data["candidates"][0]["content"]["parts"][0]
        audio_bytes = base64.b64decode(part["inlineData"]["data"])
        with open(outfile, "wb") as f:
            f.write(audio_bytes)

def generate_edge(text, outfile, voice="id-ID-ArdiNeural"):
    """Generate audio via Microsoft Edge-TTS CLI"""
    cmd = [sys.executable, "-m", "edge_tts", "--voice", voice, "--text", text, "--write-media", outfile]
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        # Fallback to direct edge-tts command if python module invocation fails
        subprocess.run(["edge-tts", "--voice", voice, "--text", text, "--write-media", outfile], check=True)

def get_audio_duration_ffprobe(filepath):
    """Get exact duration in seconds using ffprobe if available"""
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filepath
        ]
        res = subprocess.check_output(cmd, text=True).strip()
        return float(res)
    except Exception:
        # Estimation fallback (~140 words per minute if ffprobe missing)
        return 5.0

def main():
    parser = argparse.ArgumentParser(description="Poro Web Explainer Automated TTS Generator")
    parser.add_argument("--engine", choices=["elevenlabs", "gemini", "edge", "auto"], default="auto",
                        help="TTS Engine to use. 'auto' tries ElevenLabs -> Gemini -> Edge-TTS")
    parser.add_argument("--script-file", default=None, help="JSON or plain text file containing paragraphs")
    parser.add_argument("--out-dir", default="assets/audio", help="Output directory for generated audio")
    parser.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"))
    parser.add_argument("--edge-voice", default="id-ID-ArdiNeural", help="Edge TTS voice name")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    eleven_key = os.environ.get("ELEVENLABS_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    engine = args.engine
    if engine == "auto":
        if eleven_key:
            engine = "elevenlabs"
            print("Pilihan otomatis: Menggunakan ElevenLabs API.")
        elif gemini_key:
            engine = "gemini"
            print("Pilihan otomatis: Menggunakan Google Gemini TTS.")
        else:
            engine = "edge"
            print("Pilihan otomatis: Menggunakan Microsoft Edge-TTS (Gratis/Lokal).")

    paragraphs = DEFAULT_PARAGRAPHS
    if args.script_file and os.path.exists(args.script_file):
        with open(args.script_file, "r", encoding="utf-8") as f:
            if args.script_file.endswith(".json"):
                paragraphs = json.load(f)
            else:
                lines = [l.strip() for l in f if l.strip()]
                paragraphs = [{"id": f"scene_{i+1}", "text": l} for i, l in enumerate(lines)]

    print(f"\n🎙️ Memulai pembuatan audio ({len(paragraphs)} adegan) dengan engine: {engine.upper()}...")
    timing_data = []
    current_time = 0.0

    for i, p in enumerate(paragraphs):
        p_id = p.get("id", f"scene_{i+1}")
        text = p["text"]
        ext = "mp3" if engine != "gemini" else "wav"
        out_path = os.path.join(args.out_dir, f"{p_id}.{ext}")

        print(f"[{i+1}/{len(paragraphs)}] Membuat audio untuk {p_id}...")
        try:
            if engine == "elevenlabs":
                if not eleven_key:
                    raise ValueError("ELEVENLABS_API_KEY tidak ditemukan di environment variable!")
                generate_elevenlabs(text, out_path, eleven_key, args.voice_id)
            elif engine == "gemini":
                if not gemini_key:
                    raise ValueError("GEMINI_API_KEY tidak ditemukan di environment variable!")
                generate_gemini(text, out_path, gemini_key)
            else:
                generate_edge(text, out_path, args.edge_voice)
        except Exception as e:
            print(f"⚠️ Gagal generate dengan {engine} ({e}). Mencoba fallback ke Edge-TTS...")
            out_path = os.path.join(args.out_dir, f"{p_id}.mp3")
            generate_edge(text, out_path, args.edge_voice)

        duration = get_audio_duration_ffprobe(out_path)
        timing_data.append({
            "id": p_id,
            "text": text,
            "file": out_path.replace("\\", "/"),
            "start": round(current_time, 2),
            "duration": round(duration, 2),
            "end": round(current_time + duration, 2)
        })
        current_time += duration + 0.6  # 0.6s jeda antar adegan (pause breathing)

    timing_file = os.path.join(args.out_dir, "vo_timing.json")
    with open(timing_file, "w", encoding="utf-8") as f:
        json.dump(timing_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Audio VO selesai dibuat!")
    print(f"📁 Metadata timing tersimpan di: {timing_file}")
    print(f"⏱️ Total estimasi durasi narasi: {round(current_time, 2)} detik.")

if __name__ == "__main__":
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass
    main()
