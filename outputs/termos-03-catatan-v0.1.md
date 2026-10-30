# Termos — tahap 3: gambar utuh dan penampang

Status: visual diterima pengguna melalui balasan “gambrnya udh oke. lanjutin”. Angka tahap 2 sudah diterima melalui balasan “udah sesuai”. Narasi versi pertama sudah dibuat dan menunggu feedback pada tahap 4.

## Hasil untuk diperiksa

- [Papan gambar utuh dan penampang](termos-03-bedah-v0.1.png), PNG 1536 × 1024.
- [Foto produk asli dari produsen](termos-03-rujukan-produk.png). Bandingkan dengan varian ice gray di kiri bawah.
- [Prompt awal dan dua revisi](termos-03-prompt-v0.1.md), termasuk peran setiap rujukan dan koreksi label.
- [Data dan sumber riset](termos-02-data-v0.1.json).

Gambar dibuat memakai built-in imagegen. File ini adalah papan pemeriksaan raster. Mesh 3D, bagian terpisah yang dapat dianimasikan, dan simulasi perpindahan panas belum dibuat atau dibuktikan oleh gambar ini.

## Dasar visual

Bentuk luar mengikuti siluet [foto resmi SM-WA48](https://www.zojirushi.co.jp/syohin/bottle/smwa/assets/img/product_size48.png): badan tinggi, bahu membulat, tutup berengsel, tombol depan, pengunci samping, dan garis bawah. Penempatan umum seal dibantu [gambar tutup resmi](https://www.zojirushi.co.jp/syohin/bottle/smwa/assets/img/feature_pic01.png). Ini pemeriksaan kemiripan bentuk, bukan pengukuran geometri terhadap CAD.

Susunan lapisan mengikuti [penjelasan konstruksi produsen](https://store.zojirushi.com/blogs/blog/design-explained-our-superior-vacuum-insulation). Penampang berstatus ilustrasi prinsip kerja; dimensi internal dan jenis foil khusus model belum terverifikasi.

Gaya mengacu pada frame CARA KERJA MOTOR MATIC sekitar 20,5 detik: bidang solid dengan kontur tipis, warna relatif tenang, latar terang, judul tebal dengan aksen merah, serta tag gelap dan aksen kuning. Komposisi dua panel dipakai untuk membandingkan keadaan utuh dan terbuka pada tahap pemeriksaan. Ini bukan komposisi final setiap scene video vertikal.

## Daftar bagian dan ketelitian

| ID | Bagian | Yang diperiksa dalam gambar | Status bukti |
|---|---|---|---|
| P-01 | Tutup dan seal | Penunjuk mengarah ke bagian penutup yang duduk di mulut botol. | Bentuk luar punya foto rujukan; potongan internal tutup disederhanakan, bukan rekonstruksi teknis. |
| P-02 | Air panas | Penunjuk berada di cairan dalam wadah. Warna amber membedakan ruang isi dari lapisan dinding. | Warna merupakan pilihan ilustrasi, bukan termometri. |
| P-03 | Dinding dalam | Penunjuk mengarah ke bidang abu-abu yang berbatasan dengan cairan. | Identitas lapisan diperiksa; ketebalan tidak terukur. |
| P-04 | Lapisan reflektif | Penunjuk mengarah ke strip kuning di sisi luar dinding dalam. | Warna kuning hanya sorotan penjelasan; jenis bahan dan ketebalan aktual belum dipastikan. |
| P-05 | Celah vakum | Penunjuk berada di bidang kosong terang di antara lapisan dalam dan dinding luar. | Letak prinsip kerja didukung sumber; lebar gambar dibesarkan untuk keterbacaan. |
| P-06 | Dinding luar | Penunjuk mengarah ke bidang biru-abu di sisi paling luar. | Bentuk luar mengikuti rujukan; ukuran internal tidak disimpulkan dari tampilan ini. |

Urutan yang harus terbaca dari isi ke luar: **cairan → dinding dalam → permukaan reflektif → celah vakum → dinding luar**. Pemisahan lapisan pada sisi potongan dibesarkan secara skematik agar penunjuk tidak ambigu. Papan ini tidak boleh dipakai untuk menghitung ketebalan, tekanan, laju pendinginan, atau kapasitas.

## Pemeriksaan dan perbaikan yang sudah dilakukan

1. Generasi awal menghasilkan bentuk serta teks yang terbaca, tetapi material terlalu mengilap dan sasaran lapisan berdekatan.
2. Revisi pertama menyederhanakan render menjadi ilustrasi teknis. Penunjuk beberapa lapisan masih ambigu.
3. Revisi kedua memperjelas pemisahan lapisan dan mengarahkan penunjuk ke bidang berbeda. Sasaran dinding dalam, permukaan reflektif, celah, dan dinding luar diperiksa lagi pada potongan yang diperbesar.

Enam label dan catatan keterbatasan diperiksa melalui pembacaan visual. Gambar tidak memuat angka suhu atau grafik yang belum disimulasikan. Penilaian ini bukan bukti ketepatan ukuran internal, kesamaan mutlak dengan produk, atau konsistensi animasi antarframe.

## Pelajaran untuk framework

Aturan label yang benar memerlukan pemeriksaan ujung penunjuk terhadap bidang sasaran. Nama label yang benar saja tidak menjamin gambar benar. Untuk bagian sangat tipis, pakai pembesaran skematik atau inset yang diberi keterangan, lalu periksa kembali. Koordinat yang dipakai memperbaiki gambar ini merupakan instruksi khusus aset, bukan template lintas topik.

Karena pembesaran skematik mengubah proporsi internal, aset animasi kuantitatif kelak harus memisahkan parameter fisik bersumber dari skala tampilan. Gambar ini baru menguji bahasa visual dan keterbacaan bagian.

## Feedback pengguna yang diperlukan

Bandingkan bentuk luar dengan foto resmi, lalu nilai kedekatan gaya terhadap video matic. Sebutkan bagian yang masih terasa berbeda atau sulit dibaca. Sesudah visual diterima, tahap berikutnya menyusun naskah yang mengikuti bagian-bagian ini dan menyiapkan satu narasi utuh.
