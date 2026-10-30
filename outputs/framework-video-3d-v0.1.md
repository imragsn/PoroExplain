# Framework video penjelasan 3D — draft 0.1

Status: kerangka produksi dan pengukuran untuk didiskusikan. Video referensi belum dianalisis. Dokumen ini belum menetapkan resep gaya referensi dan belum diuji melalui produksi video.

Tujuan: membuat video pendek dengan topik berbeda yang mempertahankan identitas visual, gerakan, suara, dan cara bercerita dari referensi. Dokumen harus bisa dipakai AI lain, dengan penyesuaian alat sesuai kemampuannya.

## 1. Keputusan yang sudah disepakati

| Parameter | Ketentuan |
|---|---|
| Audiens | Penonton umum. |
| Bahasa | Bahasa Indonesia santai, jelas, dan spesifik. |
| Topik | Benda atau fenomena yang dijumpai dalam kehidupan sehari-hari. |
| Fokus | Satu pertanyaan utama dijelaskan sampai tuntas. |
| Format | Video vertikal dengan visual 3D atau motion graphic 3D. |
| Durasi | Target di bawah 60 detik; batas maksimum 80 detik, termasuk seluruh pembukaan dan penutup. |
| Produksi | AI boleh menggunakan kode, pemodelan, animasi, dan alat rendering. |
| Ketelitian | Mekanisme dan komponen yang menjelaskan jawaban harus akurat. Detail lain boleh disederhanakan dengan aturan yang tercatat. |
| Narasi | Satu narator dan satu aset audio narasi utuh. Boleh merekam ulang setelah revisi. |
| Kontrol pengguna | Pengguna memilih ide, memeriksa riset, membandingkan visual, mendengarkan narasi, memberi feedback video, lalu memutuskan bahan tayang. |

Target durasi tidak boleh dicapai dengan menghilangkan hubungan sebab-akibat yang diperlukan. Pangkas lingkup pertanyaan atau kalimat terlebih dahulu. Catat alasan jika hasil menggunakan rentang 60–80 detik. Video di atas 80 detik harus direvisi.

## 2. Status setiap aturan dan bukti

Pisahkan tiga hal berikut dalam guideline akhir:

- **Keputusan pengguna:** berlaku sebagai kebutuhan produksi, termasuk enam prinsip cerita di bagian 7.
- **Temuan referensi:** disertai video, timestamp, dan bukti yang dapat diperiksa. Status temuan: teramati sekali, berulang, atau masih ambigu.
- **Usulan desain:** keputusan kerja yang belum terbukti sebagai ciri referensi. Harus disebut sebagai usulan.

Enam prinsip cerita saat ini merupakan kebutuhan pengguna sekaligus hipotesis mengenai referensi. Kecocokannya dengan referensi belum diverifikasi. Jika ditemukan perbedaan, tampilkan perbedaannya untuk dibahas.

Satu kemunculan tidak cukup untuk menyatakan sebuah pola berlaku universal. Jangan menebak software, model AI, prompt asal, geometri tersembunyi, atau proses rendering hanya berdasarkan tampilan akhir.

Template catatan gaya:

| ID | Ciri yang diamati | Referensi dan timestamp | Pola atau pengecualian | Aturan sementara | Tetap / boleh berubah | Status bukti |
|---|---|---|---|---|---|---|
| G-001 | BELUM DIAMATI | BELUM TERSEDIA | BELUM DIKETAHUI | BELUM DITETAPKAN | BELUM DITETAPKAN | Belum dianalisis |

## 3. Alur produksi enam tahap

### Tahap 1 — Ide

AI memberikan tepat lima ide. Setiap ide berisi:

- Pertanyaan utama dan situasi sehari-hari yang membuka video.
- Jawaban awal yang diberi status perlu diverifikasi.
- Mekanisme atau perubahan yang menarik untuk diperlihatkan.
- Kebutuhan referensi dan kemungkinan keterbatasan visualisasi.

Pengguna memilih satu ide. Jangan memproduksi lima video. Ide yang dipilih menjadi fokus riset; jika riset tidak mendukung premisnya, jelaskan perubahan yang diperlukan sebelum meneruskan.

### Tahap 2 — Riset dan pemeriksaan fakta

AI membuat rantai penjelasan: pertanyaan → penyebab → proses → jawaban. Buang cabang yang tidak diperlukan untuk menjawab pertanyaan.

Setiap klaim penting memiliki ID, sumber yang benar-benar dibuka, lokasi bukti, konteks berlakunya, dan status verifikasi. Prioritaskan sumber primer yang sesuai objek atau fenomena. Catat model produk, satuan, kondisi pengukuran, dan batas generalisasi bila relevan.

| ID klaim | Klaim / angka / satuan | Sumber dan lokasi bukti | Objek serta kondisi | Status / ketidakpastian | Dipakai di scene |
|---|---|---|---|---|---|
| F-001 | BELUM DIRISET | BELUM TERSEDIA | BELUM DITETAPKAN | Belum terverifikasi | BELUM DITETAPKAN |

Tampilkan tiga angka kunci untuk diperiksa pengguna, lengkap dengan makna dan sumbernya. **Usulan penanganan pengecualian:** jika topik tidak membutuhkan tiga angka, gunakan klaim penting sebagai pengganti dan jelaskan alasannya. Jangan menambahkan angka hanya untuk memenuhi kuota. Seluruh klaim tetap wajib diperiksa AI.

Hasil tahap ini: catatan sumber, fakta terverifikasi, rantai sebab-akibat, dan outline singkat kebutuhan visual. Pengguna memeriksa titik pemeriksaan sebelum visual utama dibuat.

### Tahap 3 — Bedah gambar

AI membuat aset dan gambar pemeriksaan menggunakan skill bedah gambar di bagian 4. Tampilkan rujukan asli beserta gambar utuh, potongan atau pembongkaran yang diperlukan, dan label komponen utama.

Pengguna membandingkan bentuk luar dengan rujukan asli. Perbandingan komponen tersembunyi menggunakan rujukan internal yang sesuai; gambar luar saja tidak memverifikasi bagian dalam.

Hasil tahap ini: visual dasar, daftar komponen, hubungan antarbagian, keputusan penyederhanaan, dan informasi yang belum diketahui. Narasi final belum direkam. Outline penjelasan sudah harus cukup jelas untuk menentukan aset yang dibutuhkan.

### Tahap 4 — Narasi dan audio

AI menulis naskah dari fakta serta aset yang sudah diperiksa. Setiap kalimat memiliki fungsi dan hubungan dengan visual. Istilah teknis dijelaskan dalam kalimat yang sama.

Rekam narasi sebagai satu aset audio utuh dari satu narator. Simpan transkrip yang sama dengan audio aktual. Ukur durasi dari hasil rekaman; perkiraan berdasarkan jumlah kata hanya digunakan untuk perencanaan.

Pengguna mendengarkan dan memberi feedback. Jika revisi mengubah klaim atau membutuhkan komponen baru, kembali ke bagian riset atau visual yang terdampak. Revisi narasi menghasilkan satu aset audio utuh yang baru. Setelah audio disetujui, buat timestamp kata atau frasa dari audio tersebut.

### Tahap 5 — Rakit video

AI merakit visual, gerakan, label, teks karaoke, efek suara, ambience, dan musik sesuai kebutuhan cerita dan gaya referensi yang sudah terukur.

Gunakan audio final sebagai acuan waktu. Bedakan teks karaoke yang mengikuti ucapan dengan label yang menunjuk bagian benda. Pastikan keduanya tetap terbaca dan tidak saling menutup.

Hasil tahap ini: video lengkap, peta sinkronisasi, dan daftar masalah pemeriksaan. Pengguna memberi feedback pada hasil video. Perubahan durasi audio mengharuskan pembaruan timing yang terdampak.

### Tahap 6 — Evaluasi dan bahan tayang

AI memeriksa video akhir, cover, judul, caption atau deskripsi, dan bahan tayang yang diperlukan. Klaim dalam judul dan cover harus sesuai isi video.

Hasil evaluasi berisi masalah, timestamp atau lokasi, aturan terkait, bukti, dan perbaikan yang disarankan. Setelah perbaikan, periksa ulang bagian yang berubah serta sambungannya.

Pengguna memutuskan hasil akhir dan penayangan. Tahap ini menghasilkan paket siap diperiksa; penayangan memerlukan keputusan pengguna.

## 4. Kontrak skill bedah gambar

**Fungsi:** mengubah rujukan benda atau fenomena menjadi representasi yang menjelaskan mekanisme dengan akurat dan mengikuti gaya visual.

**Masukan:** topik terpilih, pertanyaan utama, catatan fakta, foto atau dokumentasi, ukuran yang tersedia, dan profil gaya.

**Pemilihan metode:**

| Kebutuhan penjelasan | Metode yang dapat dipilih |
|---|---|
| Hubungan komponen dalam rakitan | Exploded view dengan urutan dan arah yang memperjelas hubungan. |
| Bagian dalam benda | Cutaway, potongan, atau transparansi terarah. |
| Bentuk luar dan letak bagian | Tampilan utuh dengan sorotan lokal. |
| Aliran, gaya, perubahan, atau fenomena | Diagram proses atau visualisasi 3D dengan penanda yang dijelaskan. |

Pilih metode berdasarkan pertanyaan. Jangan menambahkan bagian tersembunyi yang tidak didukung bukti agar visual terlihat lebih rumit. Puluhan komponen tidak menjadi target wajib; jumlah bagian mengikuti mekanisme dan kepadatan yang terbaca.

### Ketelitian per komponen

| Jenis detail | Kewajiban |
|---|---|
| Komponen dan hubungan yang menentukan jawaban | Identitas, urutan proses, sambungan, arah kerja, dan posisi yang relevan harus didukung sumber. Dimensi wajib diverifikasi jika dipakai menjelaskan atau menghitung sesuatu. |
| Bentuk yang membantu mengenali objek | Pertahankan ciri pengenal dan proporsi yang didukung rujukan. Penyederhanaan tidak boleh menyesatkan pemahaman. |
| Detail dekoratif atau tidak berpengaruh | Boleh disederhanakan atau dihilangkan. Catat jika perubahan dapat memengaruhi interpretasi. |

Setiap komponen penting memiliki ID stabil, rujukan, fungsi, hubungan, dan status: sesuai objek spesifik, representasi umum yang didukung sumber, atau ilustrasi konseptual. Sebutkan status yang memengaruhi pemahaman penonton.

Foto tanpa acuan skala tidak memastikan dimensi fisik. Bedakan ukuran fisik, perkiraan proporsi dari gambar, dan skala artistik. Jangan menampilkan estimasi visual sebagai ukuran aktual. Bila informasi penting belum terverifikasi, cari sumber tambahan atau ubah lingkup penjelasan sebelum meluluskan visual.

### Angka dan gerakan

- Simpan fakta, satuan, parameter model, dan nilai keadaan yang diperlukan dalam data bersama.
- Nilai kuantitatif pada layar dan gerakan terkait harus membaca keadaan yang sama. Nilai turunan dihitung dari data tersebut dengan rumus dan satuan yang tercatat.
- Pisahkan nilai fisik bersumber, nilai hasil perhitungan, dan keputusan artistik. Pembesaran jarak antarbagian untuk keterbacaan tidak boleh dibaca sebagai jarak fisik sebenarnya.
- Periksa ketepatan data terhadap sumber serta kecocokan visual terhadap data. Konsistensi keduanya perlu dipenuhi.
- Pembulatan mengikuti ketelitian sumber dan kebutuhan penjelasan. Hindari presisi tambahan yang tidak didukung.

**Keluaran:** gambar pemeriksaan, aset yang dapat dianimasikan sesuai alat produksi, daftar komponen dan sumber, serta catatan penyederhanaan. File gambar saja tidak membuktikan bahwa model 3D atau data penggerak tersedia.

## 5. Kontrak skill film bedah

**Fungsi:** merakit aset terverifikasi menjadi video vertikal dengan narasi, gerakan, label, teks karaoke, audio pendukung, dan loop.

**Masukan:** aset yang sudah diperiksa, naskah dan audio final, timestamp ucapan, data bersama, serta profil gaya referensi.

Gunakan satu tabel penghubung untuk menghindari instruksi visual yang terlepas dari ucapan:

| Scene | Kalimat / frasa | ID klaim | ID komponen | Waktu ucapan | Aksi visual | Label dan waktu | Bunyi | Sumber parameter |
|---|---|---|---|---|---|---|---|---|
| SC-001 | BELUM DITULIS | BELUM DITETAPKAN | BELUM DITETAPKAN | BELUM DIREKAM | BELUM DITETAPKAN | BELUM DITETAPKAN | BELUM DITETAPKAN | BELUM DITETAPKAN |

Gerakan harus membantu menjelaskan kata, hubungan, atau proses. Jangan menganggap semua objek perlu bergerak terus. Detail kamera, material, pencahayaan, bentuk, warna, pola transisi, dan intensitas gerakan diisi dari analisis referensi.

**Keluaran:** video hasil render, audio narasi utuh, transkrip, aset atau proyek yang memang dihasilkan alat, dan laporan pemeriksaan. Jangan menyatakan aset berhasil dibuat, dirender, direkam, atau ditonton tanpa pelaksanaan nyata.

## 6. Struktur cerita dan loop

Kerangka fleksibel:

1. Situasi sehari-hari yang dapat dikenali melalui gambar, aksi, dan bunyi yang relevan.
2. Satu pertanyaan yang muncul dari situasi itu.
3. Rantai penjelasan visual yang menyelesaikan pertanyaannya.
4. Jawaban yang sudah tuntas, lalu jembatan kalimat menuju pembukaan.

Tidak ada pembagian detik wajib sebelum referensi diukur. Kalimat seperti “kita bahas” tidak wajib; pertahankan hanya bila punya fungsi dan sesuai gaya yang diamati.

Untuk loop, tulis fragmen akhir dan kalimat awal sebagai satu rangkaian, lalu dengarkan sambungannya. Pertanyaan harus sudah terjawab sebelum fragmen penghubung. Periksa makna, intonasi, jeda, kesinambungan bunyi, dan visual pada batas pemutaran ulang. Putusnya kalimat dibuat sengaja untuk menyambung ke awal.

## 7. Pengukuran enam prinsip

Pisahkan angka pengukuran, penilaian editorial, dan bukti sumber. Setiap hasil memiliki status: lulus, perlu revisi, atau belum bisa diperiksa. “Belum bisa diperiksa” tidak dihitung lulus.

| Prinsip | Bukti atau pengukuran | Pemeriksaan kelulusan |
|---|---|---|
| Pembukaan dari pengalaman sehari-hari | Timestamp konteks pertama, aksi, bunyi yang relevan, dan pertanyaan. Catat situasi konkretnya. | Konteks dan pemicu pertanyaan dipahami. Kedekatan dengan pengalaman penonton diberi alasan editorial atau hasil feedback penonton yang benar-benar dikumpulkan. |
| Satu pertanyaan, tuntas, dan loop | Satu pertanyaan tertulis; peta fungsi setiap kalimat; rantai penyebab sampai jawaban; sambungan akhir–awal. | Tidak ada langkah penting yang hilang atau cabang tanpa fungsi. Jawaban selesai sebelum jembatan loop. Sambungan bisa diikuti tanpa kontradiksi makna atau gangguan yang belum diselesaikan. |
| Satu narator dan audio utuh | Identitas narator dan audio final. | Satu narator utama, satu aset audio narasi utuh, serta pelafalan dan karakter suara yang konsisten. |
| Padat, spesifik, faktual | Pemetaan klaim ke sumber; nama, angka, satuan, dan kondisi; istilah teknis beserta penjelasannya; fungsi setiap kalimat. | Seluruh klaim penting didukung sumber, tidak ada angka tanpa dasar, istilah teknis dijelaskan di kalimat yang sama, serta kalimat membantu menjawab pertanyaan. Uji keterpahaman melalui feedback yang tersedia. |
| Visual mengikuti kata | Pasangan ucapan–komponen–label; selisih waktu kemunculan label terhadap awal penyebutan; salah sasaran; lama label terlihat. | Label menunjuk bagian yang benar, mengikuti penyebutannya, dan terbaca. Laporkan selisih waktu aktual. Toleransi dan pola kemunculan ditentukan setelah referensi diukur dan keterbacaannya diperiksa. |
| Topik dekat dengan keseharian | Situasi perjumpaan konkret dan audiens yang dimaksud. | Hubungan dengan pengalaman penonton dapat dijelaskan. Jangan menyatakan semua penonton akrab dengan topik tanpa bukti. |

Contoh perhitungan sinkronisasi: selisih waktu = awal kemunculan label − awal penyebutan nama. Nilai negatif berarti label mendahului ucapan. Catat per kejadian dan kasus terburuk; rata-rata saja dapat menyembunyikan label yang sangat terlambat.

Penilaian padat tidak disamakan dengan kecepatan bicara. Catat jumlah kata dan durasi audio bila diperlukan, lalu gunakan feedback untuk mengecek apakah penjelasan masih mudah diikuti.

## 8. Pemeriksaan akhir dan AI juri

Kesalahan fakta penting, mekanisme, hubungan komponen, label sasaran, atau angka wajib diperbaiki. Skor estetika tidak menutup kegagalan tersebut.

AI juri menyatakan bahan dan metode yang benar-benar diperiksa: video, audio, frame, transkrip, atau data proyek. Pemeriksaan frame dan transkrip tidak cukup untuk meluluskan kelancaran gerakan, kualitas audio, dan loop waktu nyata.

Format temuan:

| Lokasi / timestamp | Temuan | Aturan terkait | Bukti | Dampak | Perbaikan | Hasil pemeriksaan ulang |
|---|---|---|---|---|---|---|
| BELUM DIPERIKSA | BELUM DIPERIKSA | BELUM DITETAPKAN | BELUM TERSEDIA | BELUM DINILAI | BELUM DITETAPKAN | Belum diperiksa |

Evaluasi kemiripan gaya menggunakan profil yang sudah diisi dari referensi. Sebelum itu, kemiripan gaya berstatus belum dapat dinilai. Hindari persentase kemiripan atau skor presisi tanpa metode yang jelas.

Jika memakai skor editorial, sertakan definisi tingkatannya dan bukti. Jangan mengklaim evaluasi tersebut memprediksi retensi, monetisasi, atau performa tayangan.

## 9. Bagian yang diisi setelah referensi tersedia

- Siluet, proporsi, kompleksitas bentuk, dan tingkat realisme.
- Material, palet, pencahayaan, bayangan, dan background.
- Framing, sudut kamera, jenis proyeksi, dan gerak kamera. Verifikasi makna “isometrik” dari tampilannya sebelum menjadikannya aturan teknis.
- Pola pembongkaran, potongan, transformasi, transisi, serta tempo dan jeda gerakan.
- Tipografi, label, teks karaoke, penempatan, dan pola kemunculan.
- Pembukaan, kepadatan informasi, durasi beat, karakter narator, ambience, musik, dan efek suara.
- Sambungan loop serta variasi yang tetap menjaga identitas.

Untuk tiap aturan, tulis: **perintah → kapan berlaku → yang boleh berubah → bukti referensi → cara memeriksa → pengecualian**.

## 10. Instruksi penggunaan draft

Gunakan dokumen ini sebagai kerangka kerja. Ketika tahap produksi dimulai, kerjakan tahap yang sedang aktif dan berikan hasil konkret untuk titik pemeriksaan pengguna. Pengguna dapat meminta revisi atau mengubah keputusan sebelumnya.

Jika informasi atau kemampuan alat belum tersedia, jelaskan bagian yang belum dapat dikerjakan dan dampaknya. Teruskan bagian independen yang memang bisa dilakukan; jangan mengisi kekosongan dengan klaim keberhasilan.

Sesudah profil referensi terisi, uji kerangka pada topik uji yang disepakati. Periksa hasil aktual, revisi aturan yang terbukti kurang membantu, lalu susun versi skill yang siap dipakai ulang. Contoh raket nyamuk dari diskusi belum merupakan pilihan topik produksi.
