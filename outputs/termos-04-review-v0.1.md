# Termos — tahap 4: naskah dan narasi

Status: audio versi pertama sudah dibuat; menunggu feedback pengguna sebelum tahap rakit. Riset dan gambar sudah diterima pengguna. Narasi ini belum dinyatakan sama dengan karakter suara video referensi.

## Dengarkan

![Narasi termos](termos-04-narasi-v0.1.mp3)

- [Naskah yang dibacakan](termos-04-narasi-v0.1.txt).
- [Cuplikan uji akhir ke awal](termos-04-tes-loop-v0.1.mp3), diambil dari rekaman yang sama.
- [Cue per kalimat](termos-04-cue-kalimat-v0.1.srt).
- [Data narasi dan pemetaan visual](termos-04-cue-v0.1.json).

## Hasil aktual

| Parameter | Nilai / status |
|---|---|
| Suara | id-ID-ArdiNeural, Microsoft Edge Read Aloud melalui edge-tts. |
| Pengiriman teks | Pengguna secara eksplisit menjawab “Boleh, buat audionya”. |
| Naskah | 103 kata berdasarkan pemisah spasi. |
| Generasi | Satu naskah penuh, satu suara, satu audio sumber. |
| Durasi sumber | 52,68 detik. |
| Pemrosesan | Hening sebelum 0,17 detik dan setelah 51,93 detik pada sumber dipangkas; tidak ada potongan internal ucapan. |
| Durasi audio review | **51,76 detik**, berdasarkan pemeriksaan file hasil. |
| Format | MP3, mono, 24 kHz. |
| Cue tersedia | 13 rentang kalimat dari metadata penyedia suara, disesuaikan terhadap pemangkasan. |

Durasi tersebut merupakan durasi narasi. Video final tetap harus diperiksa durasinya sendiri. Cue kalimat belum menjadi alignment per kata untuk teks karaoke atau label.

## Hubungan cerita dan visual

1. Momen menuang dan pertanyaan mengenalkan pengalaman sehari-hari.
2. Termos dibuka secara ilustratif; dinding dan celah diperkenalkan.
3. Penjelasan berpindah dari fungsi celah ke radiasi dan permukaan reflektif.
4. Tutup dan sambungan leher menjelaskan mengapa perpindahan panas tetap ada.
5. Kesimpulan mekanisme sudah diberikan sebelum contoh spesifikasi.
6. Kartu contoh menggunakan model serta kondisi dalam [data riset](termos-02-data-v0.1.json), termasuk operator minimal dan toleransi pada teks layar.
7. Fragmen akhir menyambung kembali ke pembukaan.

Pasangan loop yang ditulis:

> Itulah kenapa, meskipun... Udah berjam-jam, pas dituang... masih panas. Kok bisa?

Cuplikan uji loop memperlihatkan sambungan bunyi yang benar-benar diambil dari audio hasil. Kelancaran intonasi tetap perlu dinilai melalui pendengaran pengguna.

## Pemeriksaan yang sudah dilakukan

- File audio berhasil didekode dan durasi berada di bawah 60 detik.
- Gabungan teks pada cue penyedia sama dengan naskah input setelah normalisasi spasi.
- Transkripsi lokal dari audio sumber mencakup rangkaian penjelasan, contoh angka, dan fragmen penutup.
- ASR menulis merek sebagai “Zodirushi”; hal ini belum membuktikan kesalahan pelafalan. Pengguna perlu mendengarkan penyebutan nama tersebut.
- Cue kalimat tidak tumpang tindih setelah penyesuaian dan berada di dalam durasi file.

Lingkungan asisten tidak mendukung pemeriksaan dengar langsung. Pemeriksaan di atas tidak meluluskan karakter suara, rasa natural, kenyamanan tempo, atau intonasi loop secara otomatis. Musik, ambience, efek suara, dan video belum dirakit pada tahap ini.

## Feedback yang diperlukan

Dengarkan suara dan nilai tempo, jeda, serta kejelasan penyebutan. Periksa apakah fragmen akhir terasa menyambung ke awal menggunakan cuplikan uji. Jika perlu revisi narasi, hasil revisi tetap berupa satu audio utuh; cue mengikuti versi audio yang benar-benar dipakai.

Setelah audio diterima, lanjut ke tahap 5: alignment per kata, persiapan aset gerak yang diperlukan, animasi, label, teks karaoke, dan audio pendukung.
