## 9. Profil gaya berdasarkan tiga referensi

Profil ini mengubah pengamatan menjadi instruksi produksi. Bedakan **pola teramati** dari **keputusan penerapan**. Keputusan penerapan merupakan rancangan untuk mendekati hasil yang terlihat; ia tidak mengungkap proses pembuatan aslinya.

Sumber bukti: A = MOTOR LISTRIK ATAU BENSIN; B = ISI BENSIN; C = CARA KERJA MOTOR MATIC. Rincian metode, beat, dan batas pemeriksaan tersedia dalam [analisis tiga referensi](analisis-tiga-referensi-v0.1.md). [Papan bukti visual](papan-bukti-visual.jpg) menyediakan sembilan sampel bertimestamp.

### 9.1 Pilih cara menjelaskan sejak tahap ide

| Mode | Pilih ketika | Bentuk visual | Bukti |
|---|---|---|---|
| Mekanisme | Pertanyaan berpusat pada bagaimana atau mengapa sesuatu bekerja. | Objek atau penampang menjadi pusat; komponen, arah, hubungan gerak, dan perubahan keadaan menjelaskan jawaban. | C; bagian silinder B sekitar 14–36 detik. |
| Perbandingan | Pertanyaan berpusat pada pilihan dengan syarat atau beberapa faktor. | Objek tetap menjadi pegangan; kartu data, skenario, grafik, dan aturan keputusan menghubungkan bukti. | A; bagian harga, pengujian, dan keputusan B. |

Kedua mode dapat digabung jika diperlukan oleh jawaban. Nama mode adalah rumusan kerja. Jumlah scene dan komponen mengikuti pertanyaan. Jangan menetapkan puluhan komponen sebagai target kualitas atau membelah fenomena secara literal.

### 9.2 Visual dan tata letak

| ID | Instruksi produksi | Bukti referensi | Ruang variasi dan pemeriksaan |
|---|---|---|---|
| V-01 | Gunakan kanvas vertikal 9:16 dan 30 fps sebagai profil awal. | Metadata A/B/C. | Resolusi keluaran dapat berubah dengan rasio sama. Target durasi mengikuti bagian 1. |
| V-02 | Gunakan latar netral terang, objek dengan warna relatif tenang, dan aksen untuk informasi yang sedang dijelaskan. | A/B krem; C hampir putih. | Warna aktual objek penting boleh dipertahankan. Jangan menganggap warna yang sama wajib untuk semua mode. |
| V-03 | Buat objek mudah dikenali melalui siluet, proporsi, dan hubungan bagian. Pilih tingkat detail yang mendukung pembacaan di layar vertikal. | Kendaraan utuh A/B; mekanisme C. | Realisme dan detail disesuaikan kebutuhan. Dimensi serta komponen tetap mengikuti bagian 4. |
| V-04 | Izinkan penampang frontal, potongan, transparansi lokal, dan tampilan bervolume dalam satu film. | B berpindah dari kendaraan ke penampang berarsir; C memperlihatkan bagian yang dibuka. | Jangan mengunci semua shot ke proyeksi isometrik teknis. Pilih sudut yang paling menjelaskan hubungan. Parameter proyeksi asal belum diketahui. |
| V-05 | Tempatkan judul singkat dengan sans-serif tebal di bagian atas. Pakai aksen pada bagian kalimat yang membawa perbedaan atau perubahan. | Header A/B memakai sorotan kuning; C memakai warna merah pada bagian tertentu. | Font persis belum teridentifikasi. Zona judul sekitar 10–17% tinggi layar merupakan patokan awal dari sampel, bukan batas tetap. |
| V-06 | Pertahankan objek atau mekanisme sebagai pusat perhatian saat kartu dan label muncul. Gunakan pembesaran tampilan untuk bagian kecil. | B sekitar 12–16 detik; C sekitar 17–26 detik; A baterai. | Objek boleh terpotong frame untuk kedekatan, selama bagian yang menjelaskan jawaban tetap terbaca. |
| V-07 | Gunakan subtitle ringkas pada bidang gelap dengan sorotan kuning dan huruf gelap untuk kata atau frasa aktif. | Rangkaian frame A/B/C. | Teks lain memakai putih atau abu-abu sesuai keadaan. Subtitle berada sekitar 62–75% tinggi layar pada sampel; geser bila menutup mekanisme penting. Timing dibuat dari audio final. |
| V-08 | Gunakan label kecil dekat bagian yang ditunjuk. Bedakan label komponen, caption ucapan, HUD, dan kartu bukti. | Label piston B; label roller C; kartu harga dan grafik A. | Label nama bagian mengikuti aturan sinkronisasi pengguna. Kartu orientasi dan HUD boleh menetap selama relevan; keduanya tidak diperlakukan sebagai label yang harus muncul ulang pada setiap kata. |
| V-09 | Sajikan kartu data sebagai satu tugas baca: angka, perbandingan, kutipan, atau keputusan. Pertahankan satuan serta konteks sumber yang memengaruhi makna. | Kartu dan grafik A/B. | Referensi memakai kartu terang, gelap, dan kuning menurut fungsi. Jangan memaksakan semua data menjadi kartu putih yang sama. |
| V-10 | Jika memakai identitas kanal, buat kecil dan konsisten. | Badge pada A/B; tidak terlihat pada C dalam pemeriksaan ini. | Opsional. Gunakan identitas kanal sendiri. |

Sampel warna latar pada PNG t=0,5 detik: A sekitar #EAE3D3; B #EFE9E0; C #FBFBF9. Sampel berasal dari area x=60–90%, y=2–6% file yang didekode. Ini titik awal palet, bukan kode warna desain asli atau syarat kesamaan piksel.

Kesan permukaan objek dapat didekati dengan material yang tenang, perbedaan nilai terang-gelap yang jelas, dan bayangan yang membantu membaca volume. Parameter material, pencahayaan, serta render engine asli belum diketahui. Nilai teknis seperti roughness, ukuran lampu, atau focal length tidak boleh diklaim sebagai hasil pengukuran saat ini.

### 9.3 Gerakan dan pembukaan bagian

Pola teramati: memperlihatkan konteks objek, mendekat pada bagian, membuka atau memotong, menyorot komponen, menunjukkan proses, lalu kembali ke tampilan yang membantu menyimpulkan. A/B/C menggunakan sebagian pola ini sesuai kebutuhan; tidak semua langkah wajib terjadi di setiap scene.

Untuk setiap gerakan, instruksi harus menyebut:

1. Bagian atau state yang berubah, memakai ID komponen.
2. Keadaan sebelum dan sesudah serta hubungan yang hendak dijelaskan.
3. Kata atau frasa pemicu dari audio final.
4. Apa yang perlu tetap terlihat agar penonton memahami perubahan.
5. Apakah gerak merupakan kejadian fisik, pembongkaran ilustratif, atau perubahan framing.

Pertahankan identitas objek saat berpindah dari tampilan utuh ke bagian dalam. Pergeseran tampilan dapat dilakukan dengan kamera, perpindahan aset, atau teknik lain yang menghasilkan kontinuitas yang dibutuhkan. Cara asli pembuatannya belum diketahui.

Jangan mengganti scene pada setiap kalimat bila satu mekanisme dapat menjelaskan beberapa langkah. B sekitar 14–36 detik dan sebagian besar C mempertahankan benda utama sambil mengubah sorotan atau keadaan.

A/B/C menampilkan penanda seperti ilustrasi dipercepat atau gerak lambat. Dalam penerapan, pisahkan **waktu fisik atau keadaan model** dari **waktu presentasi**. Angka RPM, jarak, atau nilai fisik tidak boleh dihitung dari kecepatan playback ilustrasi yang sengaja diperlambat. Ini aturan implementasi untuk konsistensi; arsitektur model asli tidak terverifikasi.

Kurva easing, durasi transisi subdetik, dan amplitudo gerakan belum ditetapkan dari pengukuran. Beri status belum diukur pada parameter itu, lalu kalibrasikan melalui uji adegan; jangan menyebut nilai pilihan sebagai temuan referensi.

### 9.4 Cerita, bahasa, dan suara

- Buka dari isyarat keseharian yang cukup untuk mengenali masalah. B memakai situasi pompa; C memakai lampu hijau sambil mekanisme langsung terlihat; A memakai harga kendaraan. Adegan lingkungan lengkap tidak menjadi syarat visual universal.
- Gunakan satu pertanyaan payung. Pertanyaan kecil boleh mengantar langkah berikutnya jika berkontribusi ke jawaban utama. B memakai pertanyaan lanjutan untuk menghubungkan mekanisme, hasil uji, dan keputusan.
- Pertahankan nama, angka, satuan, dan kondisi yang dibutuhkan untuk jawaban. Tulis istilah teknis sesedikit yang diperlukan dan jelaskan dalam kalimat yang sama sesuai standar pengguna. Standar definisi ini lebih ketat daripada pola yang teramati pada referensi.
- Gunakan hasil yang sesuai pertanyaan: penjelasan sebab-akibat untuk mekanisme; keputusan bersyarat jika jawaban bergantung pada kondisi. Jangan memaksakan pemenang tunggal pada pertanyaan yang bersyarat.
- Selesaikan jawaban sebelum fragmen penutup menghubungkan ke awal. Contoh pola dari teks: “sebelum petugas nanya:” → kalimat situasi pompa; “tiap kali…” → isyarat lampu hijau pada pembukaan.
- Pertahankan satu narator dan satu audio narasi utuh sebagai keputusan pengguna. Karakter suara, tempo, intonasi, musik, ambience, efek suara, dan level mixing referensi masih menunggu pemeriksaan dengar. Onomatopoeia yang terlihat tidak otomatis membuktikan adanya efek suara terpisah.

Referensi mendukung loop makna pada ketiganya. A/B kembali ke situasi pembuka. C kembali ke bagian mekanisme yang mirip, tetapi state angka berubah. Loop visual identik dan loop audio yang halus dinilai terpisah dari kelengkapan kalimat.

### 9.5 Catatan aturan yang belum terbukti dari file akhir

| Hal | Status | Tindakan produksi |
|---|---|---|
| Semua angka faktual benar | Belum diaudit; kartu sumber terlihat pada A/B. | Tetap riset dan cocokkan setiap klaim penting terhadap sumber. |
| Angka dan gerak dibuat dari satu model | Tidak dapat dibuktikan dari MP4. | Terapkan data bersama sebagai kebutuhan produksi dan periksa hasilnya. |
| Ukuran atau geometri mengikuti produk asli secara tepat | Belum diverifikasi. | Gunakan rujukan dan catatan ketelitian per komponen. |
| Setiap label tepat mengikuti nama pada tingkat milidetik | Pola terkait ucapan terlihat; selisih per kata belum diukur. | Buat alignment dari audio final, log cue, lalu periksa label bagian dan kata yang relevan. |
| Seluruh istilah dijelaskan dalam kalimat yang sama | Tidak teramati konsisten pada referensi. | Pertahankan sebagai standar tambahan pengguna. |
| Satu identitas narator dan proses rekaman asal | Belum diverifikasi lewat pendengaran atau aset sumber. | Gunakan satu narator dan satu aset audio utuh sesuai spesifikasi. |

### 9.6 Uji adaptasi sesudah profil disepakati

Gunakan satu topik baru yang dipilih pengguna. Pada tahap ide, tentukan pertanyaan, mode penjelasan, bukti yang dibutuhkan, dan risiko kehilangan konteks jika dipadatkan. Untuk target di bawah 60 detik, sempitkan lingkup pertanyaan sebelum menghapus langkah sebab-akibat.

Periksa hasil terhadap aturan pengguna, fakta, serta profil yang teramati. Jika gagal, catat apakah penyebabnya aturan yang kurang jelas, aset yang salah, keterbatasan alat, atau pelaksanaan yang tidak mengikuti aturan. Perbarui aturan berdasarkan hasil aktual. Belum ada video uji yang diproduksi dalam versi ini.

