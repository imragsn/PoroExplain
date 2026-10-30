# Termos — tahap 4: narasi v0.2 (ElevenLabs)

Status: audio v0.2 sudah dibuat dengan ElevenLabs atas permintaan pengguna (“untuk audio ganti pake elevenlabs … langsung eksekusi”). Versi ini menggantikan v0.1 (edge-tts) dan masih menunggu feedback pengguna. Naskah tidak berubah.

## Dengarkan

![Narasi termos v0.2](termos-04-narasi-v0.2.mp3)

- [Naskah](termos-04-narasi-v0.2.txt), isinya sama dengan v0.1.
- [Cuplikan uji loop dari akhir ke awal](termos-04-tes-loop-v0.2.mp3).
- [Cue per kalimat](termos-04-cue-kalimat-v0.2.srt) dan [cue per kata](termos-04-cue-kata-v0.2.srt).
- [Manifest narasi, alignment kata, dan pemetaan visual](termos-04-cue-v0.2.json).
- Skrip: `work/generate_termos_elevenlabs.py`. Take mentah dan alignment disimpan di `work/termos-audio/eleven-take-v1*`. Skrip memakai ulang take yang sudah ada; generasi ulang hanya terjadi dengan `--regen`.

## Hasil aktual

| Parameter | Nilai |
|---|---|
| Penyedia | ElevenLabs, endpoint `text-to-speech/with-timestamps` |
| Suara | Zan - Conversational (`zmqLb9Ysr8fUvDD7hXK8`), pria, Indonesia, *professional voice* di akun |
| Model | `eleven_multilingual_v2` |
| Setelan | stability 0.45, similarity 0.8, style 0.15, speaker boost aktif, speed 1.0 |
| Generasi | Satu panggilan untuk seluruh naskah, satu suara, satu audio |
| Durasi | **55,08 detik**. Ucapan mulai di 0 detik dan diakhiri hening sekitar 0,34 detik, jadi tidak ada yang dipangkas. |
| Format | MP3, mono, 44,1 kHz, 128 kbps |
| Alignment | Kata per kata dari alignment karakter ElevenLabs: 103 kata, 13 kalimat |

Dibanding v0.1: durasi bertambah sekitar 3,3 detik (51,76 → 55,08 detik), tetapi masih di bawah target 60 detik. Hasil v0.2 sudah punya alignment per kata, sehingga satu langkah tahap 5 berkurang.

## Pemeriksaan otomatis

- Teks alignment sama persis dengan naskah input. Gabungan 13 cue kalimat sama dengan naskah setelah spasi dinormalisasi.
- Cue tidak tumpang tindih dan semuanya berada di dalam durasi file.
- Jeda antar-kalimat menurut silencedetect (−40 dB): sekitar 0,16–0,72 detik.
- Transkripsi Whisper lokal (`work/termos-audio/asr-eleven-v0.2.srt`) memuat seluruh rangkaian kalimat. Ada dua perbedaan ejaan:
  - “pemantul” → “pemandul”
  - “Zojirushi” → “Zojirusi”

  Perbedaan ini belum tentu salah ucap, tetapi kedua kata itu perlu didengar langsung.
- Fragmen akhir “Itulah kenapa, meskipun...” terbaca oleh ASR dengan intonasi tanya (“Itulah kenapa? Meskipun?”). Periksa apakah sambungan ke awal tetap terasa natural lewat cuplikan uji loop.

Asisten tidak bisa mendengarkan audio. Karakter suara, kenaturalan, tempo, dan intonasi loop belum dinilai.

## Feedback yang diperlukan

1. Apakah suara Zan cocok? Alternatif di akun: dua *cloned voice* berbahasa Indonesia, Imra Gusnedi (pria) dan Vika Yvanka (wanita).
2. Apakah “pemantul” dan “Zojirushi” terdengar benar?
3. Apakah fragmen loop menyambung?

Jika audio diterima, lanjut ke tahap 5. Cue per kata dari file ini sudah bisa langsung dipakai untuk teks karaoke dan label.
