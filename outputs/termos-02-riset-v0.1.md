# Termos — tahap 2: riset dan titik pemeriksaan

Topik pilihan pengguna: **Kok termos bisa menahan panas?**

Status: riset dan angka sudah diperiksa pengguna melalui balasan “udah sesuai”; tahap bedah gambar sedang dikerjakan. Storyboard final, naskah final, rekaman, dan video belum dibuat. Tanggal pemeriksaan sumber: 29 Oktober 2026.

## 1. Lingkup uji framework

Mode: **mekanisme**. Fokus pada termos vakum berdinding ganda yang pasif. Pembahasan sejarah, rekomendasi merek, harga, dan perbandingan produk tidak masuk cerita ini.

Gunakan Zojirushi **SM-WA48** sebagai rujukan produk untuk data contoh dan bentuk luar. Penampang yang akan dibuat berstatus **ilustrasi prinsip kerja**, sampai geometri internal khusus model ini benar-benar didukung dokumentasi. Rujukan konstruksi umum tidak boleh dipresentasikan sebagai hasil membongkar unit tersebut.

Pertanyaan payung: bagaimana konstruksi termos memperlambat keluarnya energi dari air panas?

## 2. Fakta dan batas bukti

| ID | Fakta yang didukung sumber | Sumber dan lokasi bukti | Batas penerapan |
|---|---|---|---|
| F-01 | Vakum di antara dua dinding menghambat perpindahan melalui gas pada celah itu. Radiasi tetap dapat melintasi vakum. | [HKU — The Vacuum flask](https://www.physics.hku.hk/~phys1055/lectures/chap01.html), bagian tersebut; [Zojirushi — prinsip insulasi](https://store.zojirushi.com/blogs/blog/design-explained-our-superior-vacuum-insulation), paragraf tentang conduction dan radiation. | Prinsip fisika; diagram HKU memakai wadah kaca. Material dan detail produk stainless mengikuti dokumentasi produsennya. |
| F-02 | Produsen menjelaskan lapisan aluminium atau tembaga di luar dinding bagian dalam untuk mengurangi perpindahan radiasi. | [Zojirushi — prinsip insulasi](https://store.zojirushi.com/blogs/blog/design-explained-our-superior-vacuum-insulation), paragraf thin sheet. | Penjelasan konstruksi umum. Jenis foil dan ketebalannya pada SM-WA48 belum dikonfirmasi. |
| F-03 | Tutup yang rapat dan gasket membatasi pertukaran melalui bukaan. | [Zojirushi — prinsip insulasi](https://store.zojirushi.com/blogs/blog/design-explained-our-superior-vacuum-insulation), paragraf lids dan gasket. | Fungsi umum. Geometri tutup khusus model harus diperiksa sebelum digambar secara rinci. |
| F-04 | Sambungan logam di sekitar mulut tetap menjadi jalur pelepasan panas. | [Zojirushi — penjelasan teknologi](https://www.zojirushi.co.jp/syohin/bottle_tumbler/ondo_mahou/), catatan di bagian vakum dan diagram jalur panas pada bagian mulut. | Sumber juga membahas inovasi Thermo Ring pada produk lain. Fitur itu tidak diasumsikan ada pada model pilihan. |
| F-05 | Data contoh dan kondisi pengujian tercantum pada tabel model yang dipilih. | [Zojirushi — halaman resmi SM-WA](https://www.zojirushi.co.jp/syohin/bottle/smwa/), baris SM-WA48 dan catatan ※4. | Spesifikasi pabrikan; bukan pengukuran independen yang dilakukan untuk proyek ini. Nilainya ada di bagian 3 dan data JSON. |

Sumber sudah dibuka. Indeks manual [SM-WA48](https://www.zojirushi.co.jp/toiawase/manual/search/?s=SMWA48) juga sudah ditemukan dan dibuka; PDF manualnya belum dibaca. Jangan mengklaim detail internal dari PDF tersebut sudah terverifikasi.

## 3. Tiga angka untuk diperiksa pengguna

| ID | Angka | Makna |
|---|---|---|
| N-01 | **95°C ±1°C** | Suhu awal air pada prosedur uji. |
| N-02 | **6 jam** | Waktu sampai pemeriksaan retensi. |
| N-03 | **≥71°C** | Batas suhu akhir yang dicantumkan untuk SM-WA48. |

Konteks wajib: suhu ruangan **20°C ±2°C**, posisi tegak, dan isi sampai posisi yang disebut petunjuk. Rujuk [tabel serta catatan uji resmi](https://www.zojirushi.co.jp/syohin/bottle/smwa/).

Pada halaman yang sama, ilustrasi umum menampilkan angka akhir 67°C, sedangkan tabel SM-WA48 mencantumkan angka N-03. Gunakan tabel model yang dipilih; jangan menukar data antarvarian.

Keputusan editorial: ketiga angka tersedia untuk pemeriksaan. Penyertaannya dalam video diputuskan saat menyusun cerita, sesuai kontribusinya terhadap penjelasan dan batas durasi.

## 4. Rantai jawaban

Rangka berikut merupakan sintesis penjelasan untuk produksi, dengan F-01 sampai F-04 sebagai bukti:

**Air lebih panas daripada lingkungan → energi dapat keluar melalui beberapa jalur → konstruksi termos menghambat jalur-jalur itu → pelepasan energi melambat → minuman bertahan panas lebih lama dan tetap mendingin bertahap.**

Tiga tugas penjelasan yang perlu dijaga:

1. Tunjukkan lokasi celah vakum dan perannya, dengan F-01 sebagai rujukan.
2. Jelaskan alasan vakum perlu didampingi pengendalian radiasi, memakai F-02.
3. Tutup penjelasan dengan fungsi bukaan serta jalur yang masih tersisa, memakai F-03 dan F-04.

Kalimat inti yang hendak disampaikan: **termos memperlambat hilangnya panas yang sudah dimiliki minuman**. Ini kesimpulan mekanisme, bukan klaim bahwa suhunya akan tetap sama selamanya.

## 5. Outline kebutuhan visual untuk tahap berikutnya

Ini daftar kebutuhan aset, bukan storyboard final atau hasil render.

| Aset | Yang harus terbaca | Dasar / status |
|---|---|---|
| OBJ-01 — termos utuh | Bentuk luar dan bagian tutup yang konsisten. | Foto resmi model; bentuk rinci belum diperiksa melalui gambar. |
| OBJ-02 — penampang | Dinding bagian dalam, celah di antaranya, dinding luar, dan hubungan di mulut. | F-01/F-04; ilustrasi prinsip. |
| OBJ-03 — lapisan reflektif | Letak pada sisi luar dinding dalam; tidak mengisi seluruh celah. | F-02; jenis foil khusus model masih terbuka. |
| OBJ-04 — tutup dan area seal | Fungsi menutup bukaan; bentuk rakitan tidak ditebak. | F-03; perlu gambar/manual sebelum detail dibuat. |
| FX-01 — penanda jalur energi | Memisahkan jalur melalui bahan/gas dan radiasi. | Representasi konseptual dari F-01/F-02; bukan partikel yang terlihat langsung. |
| DATA-01 — kartu contoh | Identitas contoh, N-01/N-02/N-03, dan kondisi ujinya. | F-05; opsional secara editorial. |

Untuk memperjelas potongan, celah boleh dibesarkan secara ilustratif dan diberi keterangan. Jangan menambahkan dimensi celah, ketebalan dinding, tekanan vakum, atau nilai reflektivitas tanpa data.

Jika perlu memakai istilah konduksi, konveksi, atau radiasi, tulis penjelasannya dalam kalimat yang sama. Pembedaan ini mengikuti [penjelasan fisika HKU](https://www.physics.hku.hk/~phys1055/lectures/chap01.html); pilih istilah yang benar-benar membantu cerita.

## 6. Aturan angka dan animasi

Gunakan [data terstruktur](termos-02-data-v0.1.json) sebagai sumber label dan kartu.

- Pertahankan operator ≥ pada N-03. Nilai batas tidak boleh diubah menjadi hasil ukur tepat.
- Tidak tersedia deret waktu pendinginan untuk contoh ini. Jangan membuat kurva terukur atau angka suhu per menit yang seolah bersumber dari pabrikan.
- Jika memakai perpindahan waktu, tampilkan kartu awal dan kartu setelah interval secara terpisah. Grafik fisik kontinu memerlukan data atau model termal yang divalidasi lebih dulu.
- Jumlah panah dan tingkat terang warna merupakan pilihan ilustrasi. Jangan memberi makna watt atau persentase kehilangan energi tanpa perhitungan yang didukung parameter.
- Penampang tidak boleh diberi kesan sebagai ruang minum yang divakumkan. Letak yang dimaksud F-01 adalah celah antardinding.
- Pertukaran panas pada bagian yang tidak ditunjukkan tidak otomatis bernilai nol. Hindari label penutupan total semua jalur.

## 7. Usulan pembukaan dan penutup

Usulan situasi: termos dibuka setelah dibawa berjam-jam; minuman dituangkan, lalu muncul pertanyaan kenapa panasnya bertahan. Bunyi tutup dan tuangan merupakan arahan produksi yang belum dibuat.

Tujuan loop: setelah jawaban tuntas, kalimat terakhir mengantar kembali ke tindakan membuka atau menuang pada pembukaan. Pasangan kalimat ditulis pada tahap naskah, lalu diperiksa dengan audio final.

Target tetap di bawah 60 detik. Kurangi materi yang tidak berkontribusi pada jawaban; jangan menghapus salah satu tugas penjelasan di bagian 4 hanya untuk mempercepat durasi.

## 8. Titik pemeriksaan

Pengguna memeriksa N-01, N-02, N-03 beserta kondisi dan model rujukannya. Titik pemeriksaan ini berasal dari alur enam tahap yang dipilih pengguna.

Sesudah pemeriksaan tersebut, tahap 3 menghasilkan perbandingan rujukan asli dengan visual utuh dan penampang yang dapat ditinjau. Akurasi geometri internal yang belum diketahui tetap dinyatakan terbuka sampai ada bukti yang cukup.
