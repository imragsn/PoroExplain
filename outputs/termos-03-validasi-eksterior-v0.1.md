# Validasi Eksterior 3D — Termos SM-WA48 v0.1

## Status

Model 3D produksi bagian luar sudah dibuat. Versi ini adalah checkpoint bentuk luar sebelum pemodelan dinding ganda, celah vakum, air, leher, dan cutaway.

PNG concept board sebelumnya tetap dipakai sebagai arahan visual, tetapi **bukan** sumber geometri animasi.

## Ukuran

| Parameter | Spesifikasi resmi (≈) | Mesh v0.1 | Selisih |
|---|---:|---:|---:|
| Lebar | 6,50 cm | 6,52 cm | +0,02 cm |
| Kedalaman | 7,00 cm | 7,02 cm | +0,02 cm |
| Tinggi | 21,50 cm | 21,50 cm | 0,00 cm |

Selisih kecil pada lebar dan kedalaman berasal dari bevel serta ring dasar. Angka spesifikasi produsennya sendiri dinyatakan sebagai ukuran perkiraan.

## Objek produksi terpisah

- `outer_shell`
- `base_ring`
- `neck_band`
- `cap_outer`
- `release_button`
- `release_button_inset`
- `safety_lock`
- `safety_lock_ridge`
- `hinge_block`
- `brand_mark_placeholder`

Objek terpisah memungkinkan tombol, tutup, label, kamera, dan exploded view dianimasikan tanpa melukis ulang gambar.

## Tingkat keyakinan

- **Depan — menengah–tinggi:** siluet dan susunan kontrol dibandingkan dengan gambar produk resmi.
- **Tutup dan kontrol — menengah:** bentuk dasar dibantu foto resmi tutup terbuka, tetapi detail mekanis belum dimodelkan.
- **Samping dan belakang — menengah–rendah:** belum tersedia foto ortografis produk yang cukup untuk mengunci detail.
- **Logo — placeholder:** hanya penanda posisi, bukan rekonstruksi bentuk merek.
- **Bagian dalam — belum dibuat:** tidak ada klaim presisi internal pada versi ini.

## Keputusan yang dibutuhkan

Periksa siluet keseluruhan, perbandingan tinggi tutup dengan badan, bentuk bahu, ukuran tombol, dan ring dasar. Setelah bentuk luar diterima, tahap berikutnya adalah membangun bagian internal dengan status bukti per komponen lalu membuat cutaway 3D.

## Sumber utama

- Halaman produk resmi SM-WA: https://www.zojirushi.co.jp/syohin/bottle/smwa/
- Gambar produk dan foto tutup resmi yang disimpan dalam paket referensi proyek.

