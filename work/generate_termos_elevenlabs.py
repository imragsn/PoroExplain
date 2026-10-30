"""Termos tahap 4 v0.2: narasi ElevenLabs (satu generasi utuh) + cue kalimat dan kata dari alignment penyedia."""
from pathlib import Path
import base64
import hashlib
import json
import os
import re
import subprocess
import sys

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs'
WORK = ROOT / 'work' / 'termos-audio'
WORK.mkdir(parents=True, exist_ok=True)

VOICE_ID = 'zmqLb9Ysr8fUvDD7hXK8'  # Zan - Conversational (professional, male, id)
VOICE_NAME = 'Zan - Conversational'
MODEL_ID = 'eleven_multilingual_v2'
OUTPUT_FORMAT = 'mp3_44100_128'
SETTINGS = {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.15, 'use_speaker_boost': True, 'speed': 1.0}
LEAD_PAD = 0.12
TAIL_PAD = 0.25

script_out = OUT / 'termos-04-narasi-v0.2.txt'
raw_audio = WORK / 'eleven-take-v2-humanized.mp3'
raw_align = WORK / 'eleven-take-v2-humanized-alignment.json'
audio = OUT / 'termos-04-narasi-v0.2.mp3'

humanized_script = """Udah berjam-jam, pas dituang... masih panas.
Kok bisa?

Coba kita belah termosnya.

Botol ini punya dua dinding, luar dan dalam.
Di tengah-tengahnya ada celah hampa udara, alias vakum.

Karena nggak ada udara sama sekali, panas dari air nggak punya media buat merambat keluar.

Tapi ingat, panas masih bisa lolos lewat radiasi.

Makanya, dinding dalamnya dilapis bahan pemantul mirip cermin, biar gelombang panasnya mantul balik.

Terus, tutup silikonnya dibuat kedap buat ngunci uap panas di mulut botol.

Panas cuma bisa merembes tipis lewat sambungan lehernya.
Jadi air tetap mendingin, cuma butuh waktu jauh lebih lama.

Di tes resminya, pas diisi air sembilan puluh lima derajat Celsius, setelah enam jam suhunya masih di atas tujuh puluh satu derajat, padahal ruangan sekitarnya dua puluh derajat.

Itulah kenapa, meskipun..."""

paragraphs = [p.strip() for p in humanized_script.split('\n') if p.strip()]
text = '\n\n'.join(paragraphs)
script_out.write_text(text + '\n', encoding='utf-8')

# 1. Satu panggilan sintesis untuk seluruh naskah (dilewati jika take sudah ada, agar kuota tidak terpakai ulang).
if not raw_audio.exists() or '--regen' in sys.argv:
    r = requests.post(
        f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps',
        params={'output_format': OUTPUT_FORMAT},
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'},
        json={'text': text, 'model_id': MODEL_ID, 'voice_settings': SETTINGS},
        timeout=180,
    )
    if r.status_code != 200:
        sys.exit(f'ElevenLabs error {r.status_code}: {r.text[:500]}')
    data = r.json()
    raw_audio.write_bytes(base64.b64decode(data['audio_base64']))
    raw_align.write_text(json.dumps({'alignment': data['alignment'], 'normalized_alignment': data.get('normalized_alignment')}, ensure_ascii=False), encoding='utf-8')

al = json.loads(raw_align.read_text(encoding='utf-8'))['alignment']
chars, starts, ends = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
assert ''.join(chars) == text, 'alignment text differs from input'

def probe(path):
    p = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)], capture_output=True, text=True, check=True).stdout)
    return float(p['format']['duration']), next(s for s in p['streams'] if s['codec_type'] == 'audio')

src_dur, _ = probe(raw_audio)
spoken = [i for i, c in enumerate(chars) if not c.isspace()]
t_in = max(0.0, starts[spoken[0]] - LEAD_PAD)
t_out = min(src_dur, ends[spoken[-1]] + TAIL_PAD)

# 2. Pangkas hening awal/akhir saja; tidak ada potongan di tengah ucapan.
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(raw_audio), '-ss', f'{t_in:.3f}', '-to', f'{t_out:.3f}',
                '-c:a', 'libmp3lame', '-b:a', '128k', '-ar', '44100', str(audio)], check=True)
duration, stream = probe(audio)

def shift(t):
    return min(int(duration * 1000) / 1000, round(max(0.0, t - t_in), 3))

# 3. Kata dari alignment karakter.
words = []
for m in re.finditer(r'\S+', text):
    idx = [i for i in range(m.start(), m.end())]
    words.append({'text': m.group(), 'start_seconds': shift(starts[idx[0]]), 'end_seconds': shift(ends[idx[-1]]), 'char_start': m.start(), 'char_end': m.end()})

mapping = [
    ('B01', 'momen sehari-hari', ['P-02'], [], 'Termos dibuka dan minuman dituangkan; bunyi dibuat pada tahap rakit.'),
    ('B02', 'pertanyaan utama', [], [], 'Pertahankan benda sebagai fokus dan tampilkan pertanyaan.'),
    ('B03', 'membuka penjelasan', ['P-03', 'P-05', 'P-06'], [], 'Beralih dari benda utuh ke penampang yang sudah diterima.'),
    ('B04', 'identifikasi dinding', ['P-03', 'P-06'], ['F-01'], 'Sorot dua dinding.'),
    ('B05', 'mengenalkan vakum', ['P-05'], ['F-01'], 'Sorot celah di antara dinding; tunjukkan lokasi yang benar.'),
    ('B06', 'fungsi celah', ['P-05'], ['F-01'], 'Ilustrasikan penghambatan transfer melalui gas tanpa memberi nilai watt atau tekanan.'),
    ('B07', 'jalur radiasi', ['P-04'], ['F-01'], 'Tunjukkan bahwa jalur radiasi masih dapat melintasi celah; arah energi konseptual.'),
    ('B08', 'lapisan reflektif', ['P-04'], ['F-02'], 'Sorot permukaan di sisi luar dinding dalam; warna hanya penanda ilustratif.'),
    ('B09', 'fungsi tutup', ['P-01'], ['F-03'], 'Sorot penutup dan area seal; jangan menambahkan komponen yang belum didukung sumber.'),
    ('B10', 'jalur tersisa', ['P-03', 'P-06'], ['F-04'], 'Tunjukkan sambungan leher sebagai salah satu jalur yang masih tersisa.'),
    ('B11', 'jawaban mekanisme', ['P-01', 'P-03', 'P-04', 'P-05', 'P-06'], ['F-01', 'F-02', 'F-03', 'F-04'], 'Rangkum penghambatan jalur panas; tidak menampilkan kurva pendinginan rekaan.'),
    ('B12', 'contoh spesifikasi', [], ['F-05'], 'Kartu menyebut SM-WA48, suhu awal beserta toleransi, durasi, batas akhir, dan kondisi ruangan; data diambil dari JSON riset.'),
    ('B13', 'jembatan loop', [], [], 'Kembali ke keadaan menjelang pembukaan; sambungkan ke awal tanpa menambah fakta baru.'),
]

# Kalimat: pisah tiap paragraf pada akhir kalimat (. ? !) yang diikuti spasi; elipsis "..." di tengah kalimat tidak memisah.
sentences, pos = [], 0
for p in paragraphs:
    base = text.index(p, pos)
    pos = base + len(p)
    for m in re.finditer(r'.+?(?:(?<![.])(?<!\.\.)[.?!](?![.])(?=\s|$)|$)', p):
        s = m.group().strip()
        if s:
            off = base + m.start() + (len(m.group()) - len(m.group().lstrip()))
            sentences.append((s, off, off + len(s)))
assert len(sentences) == len(mapping), (len(sentences), [s[0] for s in sentences])

cues = []
for (s, a, b), (key, function, parts, claims, action) in zip(sentences, mapping):
    ws = [w for w in words if w['char_start'] >= a and w['char_end'] <= b]
    cues.append({'id': key, 'start_seconds': ws[0]['start_seconds'], 'end_seconds': ws[-1]['end_seconds'], 'text': s,
                 'function': function, 'part_ids': parts, 'claim_ids': claims, 'planned_visual': action,
                 'words': [{k: w[k] for k in ('text', 'start_seconds', 'end_seconds')} for w in ws]})
for i, c in enumerate(cues):
    assert 0 <= c['start_seconds'] < c['end_seconds'] <= duration
    if i: assert cues[i - 1]['end_seconds'] <= c['start_seconds'] + 1e-3
assert ' '.join(c['text'] for c in cues) == ' '.join(text.split())

def tc(v):
    t = round(v * 1000); h, t = divmod(t, 3600000); m, t = divmod(t, 60000); s, ms = divmod(t, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

(OUT / 'termos-04-cue-kalimat-v0.2.srt').write_text('\n\n'.join(f"{i+1}\n{tc(c['start_seconds'])} --> {tc(c['end_seconds'])}\n{c['text']}" for i, c in enumerate(cues)) + '\n', encoding='utf-8')
(OUT / 'termos-04-cue-kata-v0.2.srt').write_text('\n\n'.join(f"{i+1}\n{tc(w['start_seconds'])} --> {tc(w['end_seconds'])}\n{w['text']}" for i, w in enumerate(words)) + '\n', encoding='utf-8')

# 4. Cuplikan uji loop: ~3,5 dtk akhir + ~4 dtk awal dari file yang sama.
loop = OUT / 'termos-04-tes-loop-v0.2.mp3'
tail_start = max(0, cues[-1]['start_seconds'] - 0.3)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(audio), '-i', str(audio), '-filter_complex',
                f"[0:a]atrim=start={tail_start:.3f},asetpts=PTS-STARTPTS[a];[1:a]atrim=end={cues[1]['end_seconds'] + 0.3:.3f},asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1",
                '-c:a', 'libmp3lame', '-b:a', '128k', str(loop)], check=True)

manifest = {
    'status': 'awaiting_user_audio_feedback',
    'audio_file': audio.name,
    'script_file': script_out.name,
    'sentence_cues_file': 'termos-04-cue-kalimat-v0.2.srt',
    'word_cues_file': 'termos-04-cue-kata-v0.2.srt',
    'loop_test_file': loop.name,
    'duration_seconds': round(duration, 3),
    'word_count_whitespace': len(text.split()),
    'voice': {'provider': 'ElevenLabs', 'voice_id': VOICE_ID, 'voice_name': VOICE_NAME, 'model_id': MODEL_ID, 'output_format': OUTPUT_FORMAT,
              'voice_settings': SETTINGS, 'single_full_text_synthesis': True},
    'external_text_permission': {'status': 'explicitly_approved', 'user_reply': 'untuk audio ganti pake elevenlabs ... langsung eksekusi', 'destination_host': 'api.elevenlabs.io'},
    'edits': {'source_duration_seconds': round(src_dur, 3), 'source_in_seconds': round(t_in, 3), 'source_out_seconds': round(t_out, 3),
              'internal_speech_splices': False, 'purpose': 'trim leading and trailing silence only'},
    'format': {'codec': stream['codec_name'], 'sample_rate_hz': int(stream['sample_rate']), 'channels': stream['channels']},
    'alignment': {'source': 'ElevenLabs with-timestamps character alignment', 'word_level': True, 'shifted_by_trim_seconds': round(t_in, 3)},
    'hashes': {'script_sha256': hashlib.sha256(script_out.read_bytes()).hexdigest(), 'audio_sha256': hashlib.sha256(audio.read_bytes()).hexdigest()},
    'cues': cues,
}
(OUT / 'termos-04-cue-v0.2.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'source_duration': round(src_dur, 3), 'duration_seconds': round(duration, 3), 'trim': [round(t_in, 3), round(t_out, 3)],
                  'sentences': len(cues), 'words': len(words), 'format': manifest['format']}, ensure_ascii=False))
