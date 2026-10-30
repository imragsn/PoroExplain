# Rekap Status Terkunci (Locked): Tahap 3 (Master 3D Semi-Realis) & Header Dinamis VOLT DS (v0.3)

Status: **LOCKED & VERIFIED BY USER (DILARANG MENGUBAH / DILARANG HALU TANPA PERSETUJUAN)**
Tanggal: **30 Oktober 2026**
Target Produksi: **Termos Zojirushi SM-WA48 (480 ml, Matte Ice Gray) — "Kenapa Termos Bisa Tahan Panas?"**

---

## 1. Status Komponen 3D Semi-Realis (Tahap 3 - FIX & ACC)

1. **Geometri & Modeling:**
   - Dimensi 1:1 fisik asli: Tinggi total $21{,}50\text{ cm}$, Diameter bodi $6{,}50\text{ cm}$, Mulut botol (*Koukei*) $4{,}00\text{ cm}$, Kapasitas $480\text{ ml}$.
   - **Solid Closed Manifold:** Setiap lapisan memiliki ketebalan nyata (bukan mesh tipis 1 lapis), dengan *beveling/softening* ($0{,}3\text{–}1{,}2\text{ mm}$) pada seluruh siku potongan.
   - **Multi-Layer Concentric Peeling & Axial Exploded:**
     - *Lapisan 1:* Cangkang Luar *Matte Ice Gray* (`#73868A`) membuka radial ke kiri dengan pintu kelupasan berjarak nyata.
     - *Lapisan 2:* Rongga Celah Vakum skematis $\approx 2{,}0\text{ mm}$ (latar cobalt gelap `#15283B`) dengan partikel cyan yang tersedot.
     - *Lapisan 3:* Selubung Tembaga/Emas (*Copper/Gold Mirror*, Metallic `0.96`, Roughness `0.08`) dengan kelupasan bertingkat yang menangkap pantulan *Rim Light*.
     - *Lapisan 4:* Tabung Baja Dalam (*Brushed SUS304*, Metallic `0.90`).
     - *Lapisan 5:* Inti Cairan Panas $480\text{ ml}$ (Amber translusen dengan pendaran emisi termal) + Panah Pantulan Radiasi 3D.
     - *Unit Atas:* Tutup *Flip-Lid* membuka ke belakang pada engsel, terpisah vertikal di leher (*Axial Exploded*) dengan **Stopper Silikon hijau kenyal ber-SSS (*Subsurface Scattering*)** dan **Corong Minum $4{,}0\text{ cm}$**.
2. **Pencahayaan & Studio:**
   - *Curved Infinity Cyclorama* putih-hangat (`#F4F1EA`) tanpa garis horison.
   - *Three-Point Lighting* + *Dual Strong Rim Light* + *AgX Color Management* (tanpa garis kartun Freestyle).
3. **File Master & Aset Terkunci:**
   - Master Blend: [`outputs/termos-03-master-semi-realis-v0.3.blend`](file:///c:/Users/lenovo/Documents/Codex/2026-10-29/gw-mau-reverse-enginering-sebuah-style/outputs/termos-03-master-semi-realis-v0.3.blend)
   - Render Hero: [`outputs/termos-03-lookdev-hero-v0.3.png`](file:///c:/Users/lenovo/Documents/Codex/2026-10-29/gw-mau-reverse-enginering-sebuah-style/outputs/termos-03-lookdev-hero-v0.3.png)
   - Render Bedah Lapisan: [`outputs/termos-03-lookdev-peeled-v0.3.png`](file:///c:/Users/lenovo/Documents/Codex/2026-10-29/gw-mau-reverse-enginering-sebuah-style/outputs/termos-03-lookdev-peeled-v0.3.png)
   - Papan Inspeksi VOLT DS: [`outputs/termos-03-lookdev-sheet-v0.3.png`](file:///c:/Users/lenovo/Documents/Codex/2026-10-29/gw-mau-reverse-enginering-sebuah-style/outputs/termos-03-lookdev-sheet-v0.3.png)

---

## 2. Status Design System VOLT DS Murni (Tahap 5 UI - FIX & ACC)

1. **Tipografi & Tracking:**
   - Font: Arial / Helvetica Bold dengan *tight negative letter-spacing* (`-0.055em` s/d `-0.065em`) dan *line-height* rapat (`0.95`).
   - Eyebrow: Arial Regular kecil dengan spasi renggang (`letter-spacing: +0.08em`).
2. **Modular Grid & Kotak Informasi:**
   - Border: `1px–2px solid #101110` tegas.
   - Sudut: Radius $0\text{ px}$ (siku tegak).
   - **DILARANG memakai drop-shadow hitam tebal (+4px) atau pita warna-warni di setiap kotak.**
   - **One Signal Highlight:** Hanya 1 kotak utama yang sedang dibahas yang diberi blok kuning `#E8F500` (*Electric*), kotak pendamping tetap putih `#FFFFFA` (*Paper*).
   - Pin penunjuk: Kotak kecil persegi (`10x10 px`, radius $0\text{ px}$) sesuai standar `SH04 / ICON01` VOLT DS.
3. **Kartu Bukti Data (Detik 43–53):**
   - Format Grid 3 Kotak (P06 Numbers):
     - Kotak Kiri Atas (`#FFFFFA`): `95°C` (Suhu awal)
     - Kotak Kanan Atas (`#FFFFFA`): `6 Jam` (Durasi uji pada ruang 20°C)
     - Kotak Bawah Lebar (`#E8F500` Electric): `≥71°C` (Suhu bertahan JIS S 2006)

---

## 3. Status Naskah Header Dinamis (`humanizer` - FIX & ACC)

Header atas video vertikal akan berganti secara dinamis mengikuti obrolan narasi:

| Waktu | Kalimat Narasi VO | Micro Eyebrow | Title Dinamis (Tight Stacked) |
| :--- | :--- | :--- | :--- |
| **00.0s – 05.3s** | *"Udah berjam-jam, pas dituang... masih panas. Kok bisa?"* | `DARI KESEHARIAN KITA` | **PAGI DISEDUH.<br/>SIANG MASIH PANAS.** |
| **05.3s – 15.2s** | *"Coba kita belah termosnya... celah hampa udara..."* | `KITA BELAH DUA` | **KOSONG DI TENGAH,<br/>PANAS NGGAK LEWAT.** |
| **15.2s – 20.4s** | *"...panas dari air nggak punya media buat merambat..."* | `NGGAK ADA UDARA` | **JALANNYA BUNTU.** |
| **20.4s – 30.5s** | *"Tapi ingat, panas masih bisa lolos lewat radiasi..."* | `JALUR TERSEMBUNYI` | **GELOMBANGNYA<br/>DIPANTULIN BALIK.** |
| **30.5s – 38.9s** | *"Terus, tutup silikonnya dibuat kedap... merembes tipis..."* | `MULUT BOTOL` | **DIKUNCI RAPAT,<br/>BOCOR DIKIT DI LEHER.** |
| **38.9s – 53.1s** | *"Di tes resminya, pas diisi air 95°C, setelah 6 jam..."* | `ANGKA NYATANYA` | **ENAM JAM,<br/>TETAP DI ATAS 71°C.** |
| **53.1s – 56.0s** | *"Itulah kenapa, meskipun..."* | `RAHASIA TERMOS` | **TIAP KALI DITUANG.** |

---

## 4. Next Step: Tahap 5 (Perakitan Video Animasi Penuh)

- **Input:**
  - Audio Master: `outputs/termos-04-narasi-v0.2.mp3` ($55{,}968\text{ detik}$, 1679 frame @ 30fps).
  - Subtitle Cues: `outputs/termos-04-cue-kata-v0.2.srt` (125 kata tersinkronisasi).
  - Master 3D Model: `outputs/termos-03-master-semi-realis-v0.3.blend`.
- **Target Eksekusi:**
  1. Setup Rig Animasi 16-Beat di Blender (pergerakan kamera 3D continuous, belahan cangkang, kupasan emas, uap panas, dan stopper silikon).
  2. Ekspor sekuens 3D render + koordinat *anchor* 3D-ke-2D per frame.
  3. Compositing UI VOLT DS + Subtitle karaoke aktif + Audio master menjadi video final vertikal ($1080 \times 1920$).
