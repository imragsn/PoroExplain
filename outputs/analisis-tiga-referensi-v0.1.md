# Analisis tiga video referensi — v0.1

Analisis untuk menyusun framework video penjelasan 3D. Ketiga referensi diperlakukan setara karena pengguna belum memilih referensi utama. Pola dalam tiga contoh ini belum membuktikan kebiasaan seluruh karya kreatornya.

## 1. Bahan dan metode

| ID | File | Durasi kontainer | Resolusi gambar | Frame rate |
|---|---|---|---|---|
| A | MOTOR LISTRIK ATAU BENSIN.mp4 | 76,457 detik | 720 × 1280 | 30 fps |
| B | ISI BENSIN.mp4 | 78,505 detik | 720 × 1280 | 30 fps |
| C | CARA KERJA MOTOR MATIC.mp4 | 42,167 detik | 540 × 960 | 30 fps |

Metode yang benar-benar dilakukan:

- Membaca metadata file dan stream.
- Mengekstrak serta menjalankan OCR pada 196 frame dengan sampling satu frame per detik. Meninjau contact sheet, rangkaian frame terpilih, dan 15 sampel PNG pada waktu tertentu, termasuk awal serta akhir.
- Mentranskripsikan audio ketiga file secara lokal menggunakan Whisper. Menyilangkan bagian transkrip dengan teks yang terlihat. ASR memiliki kesalahan nama, angka, dan batas segmen; hasil mentah tidak dipakai sebagai bukti fakta atau alignment kata yang presisi.
- Membandingkan kalimat penutup dengan pembukaan berdasarkan transkrip dan teks tertanam.

**Batas pemeriksaan:** lingkungan analisis ini tidak menerima input audio untuk didengarkan langsung. Karakter suara, jumlah identitas suara secara perseptual, musik, efek suara, level mixing, serta kehalusan sambungan audio belum dinilai melalui pendengaran. Gerak diamati melalui perubahan frame berurutan; kurva easing, kecepatan subdetik, dan alignment kata-ke-label dalam milidetik belum diukur.

Rentang beat di bawah dibulatkan dari sampling dan transkripsi, sehingga bersifat perkiraan sekitar satu detik. Timestamp sampel PNG pada papan bukti merupakan waktu pengambilan frame tertentu.

## 2. Temuan utama: satu keluarga, beberapa cara menjelaskan

Inti yang terlihat adalah **benda yang dikenali → bagian atau persoalan yang dibuka → bukti visual dan angka → jawaban → kembali ke pembukaan**.

- **A:** perbandingan keputusan membeli, didukung pembongkaran baterai dan perhitungan biaya.
- **B:** situasi membeli bahan bakar → potongan mekanisme → pembanding data → keputusan berdasarkan kondisi.
- **C:** mekanisme sebagai pusat seluruh cerita, dengan perubahan bagian, penunjuk angka, dan sorotan komponen.

B menggunakan kendaraan yang terlihat tiga dimensi, lalu berpindah ke penampang silinder yang tampil sebagai diagram teknis frontal dengan arsiran. C memakai tampilan mekanisme bergaya ilustrasi teknis yang memberi kesan ruang. Karena itu, resep visual perlu mengizinkan kombinasi objek bervolume, penampang, diagram, dan kartu data. Pipeline pembuatannya tidak dapat dipastikan dari hasil akhir.

## 3. Peta beat

### A — MOTOR LISTRIK ATAU BENSIN

| Waktu perkiraan | Fungsi |
|---|---|
| 0–10 dtk | Harga awal dibandingkan; baterai mengubah kesan harga murah. |
| 10–13 dtk | Pertanyaan biaya sebenarnya dan janji membedah sampai penggantian baterai. |
| 13–24 dtk | Perbandingan energi dan biaya pemakaian. |
| 24–34 dtk | Perawatan dan perbedaan komponen. |
| 34–39 dtk | Pajak. |
| 39–54 dtk | Sewa, kepemilikan, penggantian, dan pemakaian baterai. |
| 54–65 dtk | Grafik biaya beberapa skenario jarak. |
| 65–73 dtk | Jawaban bersyarat berdasarkan pemakaian. |
| 73–akhir | Kembali ke dua motor dan harga awal; kalimat menjembatani pembukaan. |

### B — ISI BENSIN

| Waktu perkiraan | Fungsi |
|---|---|
| 0–11 dtk | Situasi isi bensin, perbandingan harga, dan perbedaan oktan. |
| 11–14 dtk | Klaim sehari-hari tentang mesin ngelitik; kap dan mesin dibuka. |
| 14–23 dtk | Penampang silinder menjelaskan proses yang dimaksud. |
| 23–27 dtk | Arti oktan dalam konteks penjelasan. |
| 27–36 dtk | Sensor dan perubahan pengapian. |
| 36–49 dtk | Kartu hasil pengujian yang dikutip video. |
| 49–59 dtk | Perbandingan harga dan penghematan. |
| 59–67 dtk | Buku manual dan contoh persyaratan kendaraan. |
| 67–76 dtk | Jawaban berupa aturan memilih menurut kondisi. |
| 76–akhir | Kembali ke pompa; kalimat menuju pertanyaan pembuka. |

### C — CARA KERJA MOTOR MATIC

| Waktu perkiraan | Fungsi |
|---|---|
| 0–7 dtk | Isyarat lampu hijau dan gas; pertanyaan tidak mengoper gigi; mekanisme sudah terlihat. |
| 7–13 dtk | Kondisi diam dan bagian kopling yang belum menyentuh. |
| 13–16 dtk | Bagian bergerak keluar dan menyambung. |
| 16–21 dtk | Lokasi roller dan data komponennya. |
| 21–26 dtk | Arah gerak dan analogi gaya. |
| 26–32 dtk | Hubungan gerak puli depan, belt, dan bagian belakang. |
| 32–36 dtk | Perubahan rasio yang digambarkan. |
| 36–40 dtk | Kembali ke pengalaman suara dan laju kendaraan. |
| 40–akhir | Kesimpulan dan fragmen kalimat menuju awal. |

Peta ini menghitung unit penjelasan, bukan jumlah shot atau potongan edit. Tidak ada dasar untuk memaksakan jumlah scene atau panjang hook yang sama pada semua topik.

## 4. Pemeriksaan enam hipotesis pengguna

| Hipotesis | Bukti dari referensi | Implikasi untuk guideline |
|---|---|---|
| Pembukaan berupa pengalaman sehari-hari lengkap | B menampilkan situasi pompa dan teks “Isi full, Pak?”; C memakai isyarat lampu hijau sambil langsung memperlihatkan mekanisme; A membuka dari harga dua kendaraan. | Kedekatan keseharian terlihat. Adegan lingkungan lengkap dan ambience belum terbukti sebagai syarat universal. Cukupkan konteks pada isyarat yang membuat masalah dikenali. Audio suasana masih perlu pemeriksaan dengar. |
| Satu pertanyaan dijawab dan ditutup loop | A mengarah ke biaya total, B ke pemilihan bahan bakar, C ke mekanisme perubahan rasio. Kalimat akhir ketiganya berhubungan dengan awal. | Gunakan satu pertanyaan payung. Subpertanyaan boleh ada jika diperlukan untuk jawaban. Pisahkan penilaian tuntas, loop makna, loop visual, dan loop audio. |
| Satu narator, satu rekaman | Ada stream audio campuran dan transkripsi narasi. MP4 tidak menyediakan aset narator terpisah atau riwayat rekaman. | Satu audio narasi utuh tetap menjadi keputusan produksi pengguna. Identitas suara dan cara rekam asal belum terverifikasi. |
| Padat, spesifik, angka dan nama asli; semua istilah dijelaskan di kalimat yang sama | Banyak angka, nama produk, unit, dan kartu sumber terlihat. C menyebut CVT, rpm, roller, puli, dan belt; tidak semuanya mendapat definisi dalam kalimat yang sama. | Kekonkretan teramati. Kebenaran angka dan sumber belum diaudit. Penjelasan istilah dalam kalimat yang sama merupakan standar tambahan pengguna yang perlu dipertahankan dan diuji keterpahamannya. |
| Label muncul tepat saat namanya disebut | B sekitar 14,5 dtk memperlihatkan label piston saat dibahas. C sekitar 18,5–20,5 dtk mempertahankan label “ROLLER 15 g”; header roller sudah tampil sebelum bagian itu selesai diucapkan. Kartu harga A sudah ada pada pembukaan. | Bedakan subtitle karaoke, label bagian, dan kartu data. Informasi boleh mendahului ucapan untuk orientasi, tetapi harus tersedia dan tepat sasaran saat diperlukan. Selisih timing kata secara presisi belum diukur. |
| Benda atau fenomena dekat dengan keseharian | Kendaraan, pompa bensin, biaya penggunaan, dan pengalaman mengendarai matic. | Sesuai tiga contoh, dengan lingkup pengalaman pengguna kendaraan. Keterkenalan pada seluruh penonton umum belum diuji. |

Angka yang ditampilkan video diperlakukan sebagai **isi referensi**, bukan fakta yang sudah disahkan analisis ini. Tidak dilakukan browsing sumber teknis, harga, pajak, spesifikasi, atau hasil uji dalam putaran analisis gaya ini.

## 5. Bukti visual yang dapat dijadikan aturan

| Pola | Bukti | Kekuatan bukti |
|---|---|---|
| Kanvas 9:16, 30 fps | Metadata A, B, C. | Terukur pada 3 file. |
| Latar terang, benda netral, aksen yang menandai informasi | Seluruh papan bukti. | Berulang pada 3 video. Warna spesifik berbeda. |
| Judul sans-serif tebal di bagian atas | Papan bukti dan rangkaian frame. | Berulang pada 3 video. Keluarga font persis belum diketahui. |
| Subtitle di bawah pusat gambar dengan sorotan kuning | Papan bukti; kata atau frasa yang disorot berubah pada rangkaian frame. | Berulang pada 3 video. Akurasi terhadap ucapan belum diukur per kata. |
| Tampilan mendekat pada bagian yang dibahas | A baterai sekitar 5–10 dan 39–54 dtk; B kap–mesin–silinder sekitar 12–16 dtk; C roller sekitar 17–26 dtk. | Berulang. Tidak membuktikan apakah perubahan dibuat lewat kamera 3D atau transformasi grup. |
| Penanda waktu ilustrasi | A menampilkan “ILUSTRASI · DIPERCEPAT”; B “GERAK LAMBAT”; C “GERAK LAMBAT”. | Teramati pada ketiganya. Mendukung pemisahan waktu presentasi dan waktu fisik dalam rancangan produksi. |
| Kartu bukti dan asumsi | A kartu harga, perawatan, baterai, serta grafik; B pengujian, kutipan manual, dan keputusan. | Berulang pada A/B. C memakai HUD angka, bukan pola kartu sumber yang sama. |
| Branding kecil di kanan | Badge pada A/B. | Teramati pada 2 video; bukan unsur wajib semua referensi. |

Perkiraan zona tata letak: judul sekitar 10–17% tinggi layar; subtitle sekitar 62–75% tinggi; objek mengambil sebagian besar ruang tengah. Ini merupakan pembacaan posisi pada sampel, belum pengukuran bounding box menyeluruh atau aturan safe area platform.

Sampel warna latar PNG pada t=0,5 detik, area x=60–90% dan y=2–6%:

- A: sekitar **#EAE3D3**.
- B: sekitar **#EFE9E0**.
- C: sekitar **#FBFBF9**.

Nilai tersebut adalah sampel area pada file terkompresi yang didekode, bukan kode palet asli atau syarat kesamaan piksel. Gunakan keluarga netral terang yang sama sambil mengikuti fungsi scene.

## 6. Pemeriksaan loop

| Video | Sambungan makna dari teks | Sambungan visual yang diamati |
|---|---|---|
| A | “Makanya, sebelum tergoda harga di dealer:” → pembukaan harga motor. | Akhir kembali ke komposisi dua motor dan kartu harga. |
| B | “Cek bukumu dulu, sebelum petugas nanya:” → “Isi full, Pak?” | Akhir kembali ke mobil, pompa, dan penghitung harga. Sampel akhir dan awal berada pada keadaan angka yang berdekatan, bukan identik. |
| C | “Giginya pindah sendiri, tiap kali…” → “Lampu ijo, gas pol…” | Akhir kembali ke bagian depan mekanisme, tetapi judul, status, dan angka RPM berubah saat mulai ulang. |

Ketiganya mendukung loop makna. Ini tidak membuktikan sambungan audio tanpa jeda atau loop visual yang identik pada setiap state. Kualitas sambungan audio tetap belum diperiksa lewat pendengaran.

## 7. Keputusan untuk framework berikutnya

Pertahankan inti bersama: pengalaman sehari-hari, satu pertanyaan payung, benda yang terus menjadi pegangan, penjelasan bagian demi bagian, bukti konkret, jawaban, dan jembatan loop.

Sediakan dua mode yang bisa digabung:

1. **Mode mekanisme:** bagian, gerak, arah, penampang, dan hubungan antarbagian menjadi pusat. C merupakan contoh paling langsung untuk mode ini.
2. **Mode perbandingan:** objek yang dapat dikenali menjadi pegangan, sementara kartu data, skenario, dan grafik menjelaskan keputusan. A/B menyediakan contoh mode ini.

Nama kedua mode adalah rumusan kerja dari analisis ini, bukan istilah kreator yang diketahui. B menunjukkan bahwa keduanya dapat dipakai dalam satu video.

Untuk target di bawah 60 detik, sempitkan pertanyaan dan jumlah faktor sejak tahap ide. C membuktikan satu contoh berdurasi 42 detik; A/B tidak membuktikan bahwa penjelasan mereka dapat dipersingkat tanpa kehilangan konteks.

Hal yang masih terbuka: pemeriksaan dengar audio; pengukuran subdetik untuk gerak dan sinkronisasi kata; audit fakta serta sumber; font dan parameter render asli; dimensi benda; dan pembuktian bahwa angka serta gerakan benar-benar memakai model data yang sama.

Lihat [papan bukti visual](papan-bukti-visual.jpg) dan [framework v0.2](framework-video-3d-v0.2.md).
