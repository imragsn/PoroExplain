from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess
import time

ROOT = Path(__file__).resolve().parent / 'video-analysis'

def transcribe(key):
    folder = ROOT / key
    command = [
        'ffmpeg', '-hide_banner', '-nostdin', '-y', '-i', 'audio.wav',
        '-af', 'whisper=model=../../models/ggml-small-q5_1.bin:language=id:queue=30:use_gpu=false:destination=transcript.srt:format=srt',
        '-f', 'null', '-',
    ]
    started = time.time()
    with (folder / 'transcription.log').open('w', encoding='utf-8') as log:
        result = subprocess.run(command, cwd=folder, stdout=log, stderr=log)
    print(f'{key}: exit={result.returncode}, elapsed={time.time()-started:.1f}s', flush=True)
    if result.returncode:
        print((folder/'transcription.log').read_text(encoding='utf-8',errors='replace')[-3000:],flush=True)

with ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(transcribe,['C','A','B']))
