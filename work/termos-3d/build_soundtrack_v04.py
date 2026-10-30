"""
Procedural Sound Design Synthesizer & Master Audio Mixer (v0.4)
Generates physical foley SFX (Mechanical Click, Pneumatic Whoosh, Metallic Shimmer Ping, Sub-Bass Drop)
and mixes them with the master voiceover according to the Sound Mapping Protocol (SMP).
"""

import os
import math
import struct
import wave
import subprocess

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
OUTPUTS_DIR = os.path.join(ROOT, "outputs")
SFX_DIR = os.path.join(ROOT, "work", "termos-3d", "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

VO_FILE = os.path.join(OUTPUTS_DIR, "termos-04-narasi-v0.2.mp3")
MASTER_AUDIO_OUT = os.path.join(OUTPUTS_DIR, "termos-04-master-audio-v0.4.mp3")

SAMPLE_RATE = 44100


def write_wav(filename, samples):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        packed = struct.pack(f"<{len(samples)}h", *[max(-32768, min(32767, int(s * 32767))) for s in samples])
        wf.writeframes(packed)


def make_click(filename, duration=0.12):
    """Crisp plastic-metal latch snap click."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Fast sharp noise burst + 1800Hz transient click
        decay = math.exp(-t * 65)
        transient = math.sin(2 * math.pi * 1850 * t) * decay
        pop = math.sin(2 * math.pi * 320 * t) * math.exp(-t * 40)
        # Random noise click
        noise = (math.sin(i * 12345.67) % 1.0 - 0.5) * 0.4 * math.exp(-t * 80)
        sample = (transient * 0.6 + pop * 0.3 + noise) * 0.9
        samples.append(sample)
    write_wav(filename, samples)


def make_whoosh(filename, duration=0.55):
    """Pneumatic vacuum split whoosh."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        prog = t / duration
        # Frequency sweep down
        freq = 380 - 240 * (prog ** 1.5)
        env = math.sin(math.pi * prog)
        osc = math.sin(2 * math.pi * freq * t)
        noise = (math.sin(i * 9876.54) % 1.0 - 0.5) * 0.5
        sample = (osc * 0.4 + noise * 0.6) * env * 0.75
        samples.append(sample)
    write_wav(filename, samples)


def make_ping(filename, duration=0.8):
    """Resonant metallic shimmer / thermal radiation reflection ping."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        decay = math.exp(-t * 5.5)
        # Harmonics of gold/copper shimmer (2200Hz, 3300Hz, 4400Hz)
        h1 = math.sin(2 * math.pi * 2200 * t)
        h2 = 0.5 * math.sin(2 * math.pi * 3350 * t)
        h3 = 0.25 * math.sin(2 * math.pi * 4480 * t)
        sample = (h1 + h2 + h3) * decay * 0.6
        samples.append(sample)
    write_wav(filename, samples)


def make_sub_drop(filename, duration=0.65):
    """Heavy low-frequency sub-bass drop (78Hz -> 42Hz) for metric proof."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        prog = t / duration
        freq = 78 - 36 * prog
        decay = math.exp(-t * 4.0)
        sample = math.sin(2 * math.pi * freq * t) * decay * 0.95
        samples.append(sample)
    write_wav(filename, samples)


def build_and_mix():
    click_path = os.path.join(SFX_DIR, "sfx_click.wav")
    whoosh_path = os.path.join(SFX_DIR, "sfx_whoosh.wav")
    ping_path = os.path.join(SFX_DIR, "sfx_ping.wav")
    sub_path = os.path.join(SFX_DIR, "sfx_sub.wav")

    print("Generating procedural SFX assets...")
    make_click(click_path)
    make_whoosh(whoosh_path)
    make_ping(ping_path)
    make_sub_drop(sub_path)
    print("All SFX wav files generated.")

    # Mix using FFmpeg with exact timestamps matching the narrative beats:
    # 1. Click at 4.0s (lid opening)
    # 2. Whoosh at 5.5s (shell peeling)
    # 3. Ping at 21.0s and 25.5s (radiation reflection)
    # 4. Click at 32.5s (stopper unseal)
    # 5. Sub-drop at 43.2s (metric card entrance)
    # 6. Click at 54.2s (snap-close loop)
    print("Mixing SFX with Voiceover via FFmpeg...")

    # Complex filtergraph to place each SFX at exact millisecond delay
    filter_complex = (
        "[1:a]adelay=4000|4000,volume=0.7[sfx1];"
        "[2:a]adelay=5500|5500,volume=0.8[sfx2];"
        "[3:a]adelay=21000|21000,volume=0.6[sfx3a];"
        "[3:a]adelay=25500|25500,volume=0.6[sfx3b];"
        "[1:a]adelay=32500|32500,volume=0.7[sfx4];"
        "[4:a]adelay=43200|43200,volume=0.9[sfx5];"
        "[1:a]adelay=54200|54200,volume=0.8[sfx6];"
        "[0:a][sfx1][sfx2][sfx3a][sfx3b][sfx4][sfx5][sfx6]amix=inputs=8:duration=first:dropout_transition=2[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", VO_FILE,
        "-i", click_path,
        "-i", whoosh_path,
        "-i", ping_path,
        "-i", sub_path,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        MASTER_AUDIO_OUT
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Master audio with Sound Design created: {MASTER_AUDIO_OUT}")


if __name__ == "__main__":
    build_and_mix()
