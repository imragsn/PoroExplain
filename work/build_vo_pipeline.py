"""
Modular Voice-Over (VO) Pipeline for 3D Video Explanation Framework
Supports 3 sources seamlessly:
1. Local TTS (edge-tts id-ID-ArdiNeural) - 100% offline & free
2. ElevenLabs API (eleven_multilingual_v2, Zan) - when API key is available
3. External Audio File (--file /path/to/audio.mp3) - human voice talent recording
"""
import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs'
WORK = ROOT / 'work' / 'termos-audio'
WORK.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

SCRIPT_FILE = OUT / 'termos-04-narasi-v0.2.txt'
AUDIO_OUT = OUT / 'termos-04-narasi-v0.2.mp3'
CUE_SRT = OUT / 'termos-04-cue-kalimat-v0.2.srt'
WORD_SRT = OUT / 'termos-04-cue-kata-v0.2.srt'
LOOP_TEST = OUT / 'termos-04-tes-loop-v0.2.mp3'
MANIFEST_JSON = OUT / 'termos-04-cue-v0.2.json'


def parse_vtt_srt_time(t_str):
    t_str = t_str.strip().replace(',', '.')
    parts = t_str.split(':')
    if len(parts) == 3:
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return float(parts[0]) * 60 + float(parts[1])
    return float(parts[0])


def format_srt_time(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def get_audio_info(path):
    cmd = ['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]
    data = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    duration = float(data['format']['duration'])
    stream = next(s for s in data['streams'] if s['codec_type'] == 'audio')
    return duration, stream


def generate_local_tts(text, raw_mp3, raw_vtt):
    print("Generating VO using Local Edge-TTS (id-ID-ArdiNeural)...")
    cmd = [
        'edge-tts',
        '--voice', 'id-ID-ArdiNeural',
        '--text', text,
        '--write-media', str(raw_mp3),
        '--write-subtitles', str(raw_vtt)
    ]
    subprocess.run(cmd, check=True)


def generate_elevenlabs(text, api_key, raw_mp3, raw_align):
    import requests
    print("Generating VO using ElevenLabs API (Zan - Conversational)...")
    voice_id = 'zmqLb9Ysr8fUvDD7hXK8'
    model_id = 'eleven_multilingual_v2'
    settings = {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.15, 'use_speaker_boost': True, 'speed': 1.0}
    r = requests.post(
        f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps',
        params={'output_format': 'mp3_44100_128'},
        headers={'xi-api-key': api_key.strip(), 'Content-Type': 'application/json'},
        json={'text': text, 'model_id': model_id, 'voice_settings': settings},
        timeout=180
    )
    if r.status_code != 200:
        raise RuntimeError(f"ElevenLabs error {r.status_code}: {r.text}")
    res = r.json()
    raw_mp3.write_bytes(base64.b64decode(res['audio_base64']))
    raw_align.write_text(json.dumps(res, ensure_ascii=False), encoding='utf-8')


def build_cues_and_manifest(source_type, raw_mp3, raw_sub_file, text_lines):
    # Standardize audio to final 44.1kHz MP3
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(raw_mp3),
        '-c:a', 'libmp3lame', '-b:a', '128k', '-ar', '44100',
        str(AUDIO_OUT)
    ], check=True)

    duration, stream = get_audio_info(AUDIO_OUT)

    # Parse cues from subtitles or whisper
    cues = []
    if raw_sub_file and raw_sub_file.exists():
        content = raw_sub_file.read_text(encoding='utf-8')
        # Parse VTT / SRT blocks
        blocks = re.findall(r'(\d+:\d+[\d:.,]*)\s*-->\s*(\d+:\d+[\d:.,]*)\s*\n(.*?)(?=\n\s*\n|\Z)', content, flags=re.S)
        for i, (t_start, t_end, t_text) in enumerate(blocks):
            clean_text = ' '.join(t_text.strip().split())
            if not clean_text:
                continue
            s_time = parse_vtt_srt_time(t_start)
            e_time = min(duration, parse_vtt_srt_time(t_end))
            cues.append({
                'id': f'CUE_{i+1:02d}',
                'start_seconds': round(s_time, 3),
                'end_seconds': round(e_time, 3),
                'text': clean_text
            })

    # If subtitle parser has fewer cues, fallback to even duration distribution
    if not cues:
        cue_count = len(text_lines)
        dt = duration / cue_count
        for i, line in enumerate(text_lines):
            cues.append({
                'id': f'CUE_{i+1:02d}',
                'start_seconds': round(i * dt, 3),
                'end_seconds': round((i + 1) * dt, 3),
                'text': line
            })

    # Generate Sentence SRT
    srt_lines = []
    for i, c in enumerate(cues):
        srt_lines.append(f"{i+1}\n{format_srt_time(c['start_seconds'])} --> {format_srt_time(c['end_seconds'])}\n{c['text']}\n")
    CUE_SRT.write_text('\n'.join(srt_lines), encoding='utf-8')

    # Generate Word Cues (Interpolated per sentence for karaoke highlight)
    word_cues = []
    w_idx = 1
    word_srt_lines = []
    for c in cues:
        words = c['text'].split()
        if not words:
            continue
        c_dur = c['end_seconds'] - c['start_seconds']
        w_dur = c_dur / len(words)
        for j, w in enumerate(words):
            w_start = c['start_seconds'] + j * w_dur
            w_end = c['start_seconds'] + (j + 1) * w_dur
            word_cues.append({
                'index': w_idx,
                'word': w,
                'start_seconds': round(w_start, 3),
                'end_seconds': round(w_end, 3)
            })
            word_srt_lines.append(f"{w_idx}\n{format_srt_time(w_start)} --> {format_srt_time(w_end)}\n{w}\n")
            w_idx += 1
    WORD_SRT.write_text('\n'.join(word_srt_lines), encoding='utf-8')

    # Generate Loop Test Audio (last 3.5s concatenated with first 4s)
    tail_start = max(0.0, duration - 3.8)
    head_end = min(duration, 4.2)
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(AUDIO_OUT), '-i', str(AUDIO_OUT),
        '-filter_complex',
        f"[0:a]atrim=start={tail_start:.3f},asetpts=PTS-STARTPTS[a];"
        f"[1:a]atrim=end={head_end:.3f},asetpts=PTS-STARTPTS[b];"
        f"[a][b]concat=n=2:v=0:a=1",
        '-c:a', 'libmp3lame', '-b:a', '128k', str(LOOP_TEST)
    ], check=True)

    # Manifest JSON
    manifest = {
        'status': 'ready_for_stage_5_assembly',
        'voice_source': source_type,
        'audio_file': AUDIO_OUT.name,
        'duration_seconds': round(duration, 3),
        'sentence_cues_file': CUE_SRT.name,
        'word_cues_file': WORD_SRT.name,
        'loop_test_file': LOOP_TEST.name,
        'format': {'sample_rate': stream['sample_rate'], 'channels': stream['channels']},
        'sentence_count': len(cues),
        'word_count': len(word_cues),
        'cues': cues
    }
    MANIFEST_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"VO Pipeline completed: Source={source_type}, Duration={duration:.2f}s, Sentences={len(cues)}, Words={len(word_cues)}")


def main():
    parser = argparse.ArgumentParser(description="Modular Voice-Over Pipeline")
    parser.add_argument('--source', choices=['local', 'elevenlabs', 'external'], default='local', help='VO Provider')
    parser.add_argument('--file', help='Path to external audio file (for external source)')
    parser.add_argument('--api-key', help='ElevenLabs API Key')
    args = parser.parse_args()

    text = SCRIPT_FILE.read_text(encoding='utf-8').strip()
    text_lines = [p.strip() for p in text.split('\n') if p.strip()]

    raw_mp3 = WORK / f"raw_vo_{args.source}.mp3"
    raw_sub = WORK / f"raw_vo_{args.source}.vtt"

    if args.source == 'local':
        generate_local_tts(text, raw_mp3, raw_sub)
    elif args.source == 'elevenlabs':
        key = args.api_key or os.environ.get('ELEVENLABS_API_KEY')
        if not key:
            sys.exit("Error: ElevenLabs API Key is required for --source elevenlabs")
        generate_elevenlabs(text, key, raw_mp3, WORK / "eleven_raw_align.json")
        raw_sub = None
    elif args.source == 'external':
        if not args.file or not Path(args.file).exists():
            sys.exit(f"Error: External audio file not found: {args.file}")
        import shutil
        shutil.copyfile(args.file, raw_mp3)
        raw_sub = None

    build_cues_and_manifest(args.source, raw_mp3, raw_sub, text_lines)


if __name__ == "__main__":
    main()
