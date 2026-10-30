# Guideline Step-by-Step: Pemodelan, Shading, Koreografi, & Rendering 3D Semi-Realis (Lintas Topik)

Status: **SOP & Guideline Standar Produksi Tahap 3 & Tahap 5 (v0.1)**
Tujuan: Menjadi buku panduan langkah demi langkah (*step-by-step playbook*) yang dapat dipakai ulang pada **topik apa pun** (produk harian, mesin otomotif, baterai/elektronik, hingga fenomena fisik) agar menghasilkan kualitas visual **3D Semi-Realis** yang konsisten, hidup, dan bebas dari jalan pintas gambar 2D mentah.

---

## Ringkasan Alur Kerja 8 Langkah (Dari Data Riset hingga Render Sekuens)

```
[Langkah 1] Translasi Data Tahap 2 ──> Dimensi 1:1 + Skala Skematis Terukur
      │
[Langkah 2] Pilih Mode Bedah 3D    ──> Concentric Peel / Axial Explode / Clamshell / X-Ray
      │
[Langkah 3] Stylized Modeling      ──> Solid Closed Manifold + Bevel Tepi + Hierarki Pivot
      │
[Langkah 4] Stylized Texturing     ──> Tanpa Tekstur Kotor + Node AO/Curvature & Fresnel
      │
[Langkah 5] Material & Shading     ──> SSS (Karet/Organik) + Clearcoat + Logam Anisotropik
      │
[Langkah 6] Three-Point + Rim Light──> Key + Fill Sejuk + Strong Dual Rim Light + AgX
      │
[Langkah 7] GERBANG LOOKDEV (2 PNG)──> Validasi Hero Utuh & Bedah Lapisan bersama User
      │
[Langkah 8] Render Sekuens Animasi ──> 16-Beat Audio-Driven Rig + 6 Kurva Graph Editor + JSON Anchor
```

---

## Langkah 1 — Translasi Data Riset (Tahap 2) ke Geometri 3D

Sebelum membuat satu titik pun di Blender, ambil data dari dokumen riset Tahap 2 dan bagi menjadi **3 Kategori Ukuran**:

1. **Ukuran Eksternal 1:1 (Wajib Akurat Fisik):**
   - Tinggi total, diameter/lebar, proporsi siluet luar, dan ukuran bagian yang dikenali mata penonton (contoh pada Termos: tinggi $21{,}50\text{ cm}$, diameter $6{,}50\text{ cm}$, mulut botol $4{,}00\text{ cm}$).
2. **Ukuran Komponen Penentu Jawaban (Skala Skematis Terukur):**
   - Jika komponen kunci di dunia nyata terlalu tipis untuk terlihat di layar HP vertikal $1080 \times 1920$ (misal celah vakum $1\text{ mm}$, lapisan foil mikron, atau celah ring piston $0{,}2\text{ mm}$), perbesar ketebalan visualnya secara terukur ($1{,}5\times \text{ s/d } 3\times$) agar terbaca jelas oleh mata, namun **tetap tampilkan angka ukuran asli pada teks/HUD**.
3. **Elemen Indikator Proses (3D Fenomena Visual):**
   - Ubah proses tak kasatmata (aliran panas, arus elektron, tekanan uap, gesekan) menjadi objek 3D terukur seperti panah pantulan (*ricochet arrows*), partikel udara yang tersedot, atau pendaran emisi termal.

---

## Langkah 2 — Pilih Mode Pembelahan Objek (Taxonomy of 3D Disassembly)

Jangan menggunakan potongan rata (*flat half-cut*) yang membosankan untuk semua topik. Pilih salah satu atau kombinasi dari **4 Mode Pembelahan 3D** berikut sesuai anatomi benda yang dibahas:

| Mode Pembelahan 3D | Kapan Dipakai (Jenis Topik) | Cara Kerja Geometri & Animasi | Contoh Kasus Topik |
| :--- | :--- | :--- | :--- |
| **1. Concentric Layer Peel**<br/>*(Kupasan Berlapis Bertingkat)* | Objek silindris, bola, atau berlapis-lapis dari luar ke dalam. | Setiap lapisan dibuka dengan sudut potong bertingkat (*stepped angle*, misal Lapisan 1 buka $140^\circ$, Lapisan 2 buka $115^\circ$, Lapisan 3 buka $85^\circ$) + pintu cangkang luar bergeser ke samping. | Termos Vakum, Sel Baterai Lithium, Kabel Bawah Laut, Filter Air, Ban Tubeless. |
| **2. Axial / Telescopic Exploded**<br/>*(Bongkar Sumbu Berurutan)* | Objek dengan komponen yang bertumpuk pada satu poros/sumbu kerja. | Komponen bergeser memisah sepanjang sumbu utama ($X, Y,$ atau $Z$) dengan jeda berurutan (*staggered offset*), lalu merapat kembali saat mengunci. | Tutup & Stopper Termos, Transmisi CVT Motor Matic, Lensa Kamera, Injektor Bensin, Shockbreaker. |
| **3. Hinged / Clamshell Open**<br/>*(Buka Engsel / Pintu Mekanis)* | Objek bercangkang, berpenutup engsel, atau katup mekanis. | Titik *origin/pivot* diletakkan persis di as engsel; komponen berputar membuka dengan kurva pegas (*Spring Overshoot*). | Tutup Flip-Lid One-Hand, Katup Mesin, Casing Laptop/HP, Pemutus Arus (MCB). |
| **4. Selective Ghosting / X-Ray**<br/>*(Transparansi Selektif)* | Saat cangkang luar harus tetap utuh untuk konteks bentuk, tetapi aliran di dalam harus terlihat. | *Alpha / Transmission Weight* cangkang luar diturunkan secara halus pada area tertentu sementara komponen inti tetap solid dan menyala. | Aliran Bensin di Tangki Motor, Sirkulasi Air Radiator, Aliran Udara di Hairdryer. |

---

## Langkah 3 — Stylized Modeling (Solid Manifold, Bevel, & Hierarki)

Untuk mendapatkan estetika **Semi-Realis** (anatomi akurat namun siluet bersih, ramah mata, dan meyakinkan secara fisik):

1. **Wajib Solid Closed Manifold (Dilarang Mesh Kertas 1 Lapis):**
   - Setiap dinding atau lapisan yang dibelah **wajib memiliki ketebalan fisik nyata** (dinding luar + dinding dalam + penampang irisan samping yang tertutup rapat).
   - Berikan material khusus yang sedikit lebih terang/spekular pada permukaan bidang irisan (*Cutaway Cross-Section Face*) agar tebal tiap lapisan langsung terlihat kontras.
2. **Beveling & Softening (Sudut Melengkung Halus):**
   - Di dunia nyata atau render kaku, sudut $90^\circ$ terlihat tajam seperti pisau dan tidak menangkap cahaya.
   - Pasang `Bevel Modifier` ($0{,}3\text{ mm} \text{ s/d } 1{,}2\text{ mm}$, `segments = 3` atau `4`, `angle_limit = 32°`) pada setiap komponen. Sudut yang sedikit membulat (*rounded edge*) akan menangkap garis kilau cahaya (*specular highlight*) dari *Rim Light*.
3. **Hierarki *Parent-Child* & Titik Pivot Logis:**
   - Buat satu parent utama `GEO_<TOPIK>_ROOT`.
   - Kelompokkan setiap sub-rakitan ke dalam `GRP_<NAMA_KOMPONEN>` dengan posisi *Origin/Pivot* tepat di sumbu geraknya (misal: pivot tutup berada di engsel belakang, bukan di tengah dunia `[0,0,0]`).

---

## Langkah 4 — Stylized Texturing (Eliminasi Detail Mikro & Curvature/AO)

Gaya semi-realis **tidak menggunakan foto tekstur kotor** (tanpa foto karat, debu, baret acak, atau pori-pori kasar):

1. **Micro-Detail Elimination:**
   - Gunakan warna dasar (*Base Color*) yang bersih dan terkalibrasi secara *Linear RGB*.
   - Jika objek memiliki warna khas di dunia nyata (seperti *Matte Ice Gray* `#6D7E82` pada termos, merah marun pada bodi motor, atau hijau tembaga pada PCB), gunakan warna asli tersebut sebagai identitas objek, lalu naikkan kejelasan nilainya.
2. **Procedural Curvature & Ambient Occlusion (AO) Node Setup:**
   - Di dalam *Shader Node Tree*, gabungkan node `Ambient Occlusion` (untuk menggelapkan lekukan dalam secara lembut sebesar $20\%\text{–}30\%$) dan `Layer Weight -> Facing/Fresnel` (untuk mencerahkan tepi siluet sebesar $15\%\text{–}20\%$).
   - Hasilnya: lekukan mekanis dan volume silinder langsung terlihat tiga dimensi dan tegas bahkan sebelum terkena lampu utama.

---

## Langkah 5 — Material & Shading Fisik Semi-Realis

Setiap keluarga material wajib diatur menggunakan parameter `Principled BSDF` berikut agar benda terlihat "hidup" dan taktil:

| Kategori Benda | Pengaturan Kunci di `Principled BSDF` (Blender 5.2+) | Efek Visual Semi-Realis yang Dihasilkan |
| :--- | :--- | :--- |
| **1. Karet, Silikon, Kulit, & Plastik Kenyal**<br/>*(Stopper, Gasket, Seal, Ban)* | `Subsurface Weight = 0.65–0.85`<br/>`Subsurface Radius = (1.0, 0.8, 0.6)`<br/>`Subsurface Scale = 0.18–0.28`<br/>`Roughness = 0.35–0.42`, `Coat Weight = 0.22` | Cahaya *Rim Light* menembus bagian tepi karet (*Subsurface Scattering / SSS*), membuat silikon tampak empuk, kenyal, dan hidup (bukan plastik mati). |
| **2. Bodi Cat / Powder-Coat Satin**<br/>*(Cangkang Termos, Bodi Kendaraan)* | `Metallic = 0.10–0.18`, `Roughness = 0.32–0.38`<br/>`Coat Weight = 0.25–0.35`, `Coat Roughness = 0.18` | Permukaan mulus berkelas dengan pantulan lembut yang memperjelas lekukan bodi tanpa menjadi cermin yang membingungkan. |
| **3. Logam Mesin / Baja Tahan Karat**<br/>*(Tabung SUS304, Piston, Blok Mesin)* | `Metallic = 0.86–0.92`, `Roughness = 0.18–0.25`<br/>`Anisotropic = 0.35–0.40`, `Coat Weight = 0.15` | Kilau logam bersih terarah (*clean brushed metal*) tanpa bintik-bintik noise kasar. |
| **4. Lapisan Pemantul / Cermin / Krom**<br/>*(Foil Tembaga/Emas, Reflektor)* | `Metallic = 0.96`, `Roughness = 0.06–0.10`<br/>`Coat Weight = 0.40`, `Emission Strength = 0.10` | Pantulan spekular tajam yang langsung menyala ketika kamera bergerak melintasinya (*arc shot*). |
| **5. Cairan / Fluida Berenergi**<br/>*(Air Panas, Bensin, Oli)* | `Transmission Weight = 0.45–0.65`, `IOR = 1.333`<br/>`Subsurface Weight = 0.40–0.55`<br/>`Emission Strength = 0.35–0.55` (inti hangat) | Cairan tampak tembus cahaya, memiliki kedalaman volume, dan memancarkan energi termal/kimia dari bagian intinya. |

---

## Langkah 6 — Setup Pencahayaan Sinematik & Mesin Render Ray-Tracing

1. **Tanpa Garis Hitam Freestyle (`use_freestyle = False`):**
   - Pemisahan antar bagian tidak lagi menggunakan garis tinta hitam 2D, melainkan kontras cahaya fisik.
2. **Rig 5 Lampu Studio Semi-Realis (*Three-Point + Dual Strong Rim + Top Bar*):**
   - **`LIGHT_Key_Main` (Kiri-Depan Atas):** Cahaya hangat-netral (`#FFF9F0`), membentuk volume utama dan bayangan jatuh di meja.
   - **`LIGHT_Fill_Soft` (Kanan-Depan):** Ukuran lampu besar dengan rona sedikit sejuk (`#E3F0FF`) agar area bayangan tetap berwarna bersih dan tidak hitam pekat.
   - **`LIGHT_Rim_Strong_Left` & `LIGHT_Rim_Strong_Right` (Belakang Kiri & Kanan):** Intensitas tinggi (`1.3x – 1.5x Key Light`), berfungsi memisahkan siluet objek dari latar belakang, menyalakan efek *SSS* pada karet/silikon, dan memicu kilau pada bevel irisan lapisan.
   - **`LIGHT_Top_Specular` (Atas Tengah):** Memberi pantulan bersih pada bibir atas botol/mesin.
3. **Kamera Fisik & Lensa:**
   - Gunakan focal length **60mm – 85mm** agar proporsi 1:1 bebas dari distorsi cembung (*fisheye*).
   - Aktifkan **Depth of Field (DoF)** (`f/2.8` saat *macro close-up* celah kecil, `f/4.0–f/5.6` saat *full shot*).
4. **Mesin Render & Manajemen Warna:**
   - Gunakan **Cycles Ray-Tracing + OpenImageDenoise** (atau **EEVEE Next dengan Ray-Tracing & Fast GI aktif** untuk sekuens frame tinggi) agar pantulan antar lapisan dan bayangan lembut terhitung secara fisik.
   - Gunakan `View Transform = AgX` dengan `Look = AgX - Medium High Contrast` agar warna vibrant namun highlight tidak pecah (*blown-out*).

---

## Langkah 7 — Gerbang Validasi LookDev (LookDev Gate — 2 Frame Still)

Sebelum merender ratusan atau ribuan frame animasi (yang memakan waktu komputasi), **wajib merender 2 Frame Validasi Resolusi Penuh ($1080 \times 1920$)** untuk diperiksa bersama pengguna:

1. **Frame LookDev 1 (`lookdev-hero.png`):** Objek dalam keadaan utuh (atau sedikit terbuka) untuk memvalidasi siluet 1:1, warna eksternal, dan kualitas pencahayaan *Rim Light*.
2. **Frame LookDev 2 (`lookdev-peeled.png`):** Objek dalam keadaan **terbelah berlapis (*Multi-Layer Peel / Exploded*)** untuk memvalidasi ketebalan tiap lapisan, kontras material antar bagian dalam, dan efek *SSS* / refleksi.

> **Aturan Keras:** Render still di Langkah 7 ini **bukan** bahan mentah yang digeser-geser menjadi video. Setelah pengguna menyetujui *LookDev Gate* ini, barulah mesin menjalankan Langkah 8 (Render Sekuens Animasi 3D Frame-by-Frame).

---

## Langkah 8 — Koreografi Animasi 3D Berbasis Audio & Ekspor Anchor

Setelah *LookDev Gate* disetujui:

1. **Pecah Durasi Audio VO Menjadi Beat Padat (1 Beat Setiap 2,5 – 3,5 Detik):**
   - Setiap kalimat atau klausa narasi harus memiliki aksi kamera 3D atau aksi mekanis komponen yang spesifik agar visual tidak pernah membeku (*zero dead-freeze*).
2. **Terapkan Variasi Kurva Graph Editor Sesuai Fisika Benda:**
   - *Spring Overshoot* untuk buka tutup/engsel, *Heavy Quintic Ease-In-Out* untuk belahan cangkang logam, *Staggered Cascade* (jeda 4–6 frame per lapisan) untuk kupasan berlapis, *Linear + Sharp Ricochet* untuk pantulan gelombang/partikel, *Whip Expo Ease* untuk pindah fokus kamera cepat, dan *Slow Orbital Drift* ($2^\circ\text{–}4^\circ/\text{detik}$) saat kamera mengamati penjelasan.
3. **Ekspor Sekuens Frame 3D + Matrix Koordinat 2D Anchor (`anchors_per_frame.json`):**
   - Saat Blender merender setiap frame $f$, skrip memproyeksikan posisi 3D titik `ANCHOR_*` ke koordinat layar $(X_f, Y_f)$ sehingga garis penunjuk (*leader line*) pada layer 2D **VOLT DS** menempel secara presisi di atas bagian objek yang bergerak.
