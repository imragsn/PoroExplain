# Blueprint Tahap 3 (Rombak Besar): Desain 3D Semi-Realis & Koreografi Multi-Lapisan (v0.3)

Status: **Dokumen Rancangan Utama Tahap 3 (Semi-Realistic Overhaul)**
Kasus Uji: **Termos Zojirushi SM-WA48 (480 ml, Matte Ice Gray)**
Prinsip Utama: **Bukan Gambar 2D yang Digeser Mentah — Melainkan Sekuens Animasi 3D Murni Frame-by-Frame dengan Kupasan Per Lapisan (Multi-Layer Peeling) & Kamera Fisik Dinamis.**

---

## 1. Aturan Keras Anti-Shortcut (Hard Rules)

1. **Dilarang Keras Memakai Gambar 2D Mentah sebagai Animasi:**
   - Video akhir **wajib** berasal dari render sekuensial 3D di Blender (kamera 3D bergerak di ruang $X, Y, Z$ dan komponen mesh 3D bertransformasi per frame), bukan hasil *crop/pan/zoom* 2D dari 1–2 gambar statis.
   - Render still (1–2 frame) hanya digunakan sebagai **Gerbang Validasi Material & Pencahayaan (LookDev Gate)** sebelum proses render sekuens animasi 3D dijalankan.
2. **Gaya Visual Semi-Realis (Bukan Kartun Garis Hitam / Bukan Fotorealisme Kotor):**
   - **Tanpa Garis Hitam Freestyle 2px:** Pemisahan bentuk mengandalkan kontras *Three-Point Lighting*, *Strong Rim Light*, *Bevel Highlights*, dan *Ambient Occlusion*.
   - **Proporsi Akurat 1:1, Permukaan Bersih:** Dimensi eksternal patuh 100% pada Zojirushi SM-WA48 ($21{,}5\text{ cm} \times 6{,}5\text{ cm}$), tetapi tekstur mikro (debu, goresan kasar, noise kotor) dihilangkan agar permukaan terlihat mulus, higienis, dan taktil.
   - **Bevel & Softening:** Setiap tepi potongan dan sudut mekanis diberi *bevel/fillet* ($0{,}5\text{ mm} - 1{,}2\text{ mm}$) agar menangkap pantulan cahaya (*specular highlight*) yang lembut dan ramah mata.
   - **Shading Fisik Semi-Realis:**
     - *Stopper Silikon & Gasket:* Menggunakan **Subsurface Scattering (SSS)** hangat agar terlihat kenyal dan empuk.
     - *Cangkang Luar:* **Matte Ice Gray** (`#6D7E82`, *Roughness* `0.38`, *Clearcoat* tipis `0.15`).
     - *Lapisan Pemantul Radiasi:* **Copper/Gold Mirror** (*Metallic* `0.96`, *Roughness* `0.08`) dengan pantulan cahaya tajam.
     - *Dinding Dalam:* **Brushed Stainless SUS304** (*Metallic* `0.88`, *Roughness* `0.22`).
     - *Inti Cairan Panas:* Shader cairan teh/air panas amber semi-translusen dengan emisi termal lembut.

---

## 2. Arsitektur "Kupasan Per Lapisan" (Multi-Layer Concentric Peeling)

Agar objek 3D benar-benar hidup dan tidak kaku seperti satu dinding yang dibelah rata, kelima lapisan termos dimodelkan sebagai **Mesh Manifold Tertutup yang Independen** dan dibuka secara **berjenjang (Staggered / Telescopic Peel)**:

```
[Lapisan 1: Cangkang Luar Ice Gray]  ──> Membuka geser ke Kiri & Kanan (Radial Split)
       │
[Lapisan 2: Rongga Celah Vakum]      ──> Ruang kosong 3D dengan partikel udara yang "dihisap habis"
       │
[Lapisan 3: Selubung Tembaga/Emas]   ──> Mengelupas berputar (Rotational Peel) menampakkan cermin emas
       │
[Lapisan 4: Tabung Baja Dalam]       ──> Terbuka dengan jendela potong bertingkat (Stepped Window Cut)
       │
[Lapisan 5: Kolom Air Panas 480ml]   ──> Inti cairan utuh di tengah dengan gelombang panas internal
       │
[Bagian Atas: Tutup & Stopper]       ──> Terurai vertikal ke atas (Axial Exploded) pada sumbu leher
```

### Klasifikasi 4 Mode Pembelahan untuk Kasus Lain di Framework:
1. **Concentric Layer Peel (Kupasan Berlapis):** Untuk objek berlapis silindris/bola (Termos, Baterai Listrik, Kabel Bawah Laut, Struktur Bumi).
2. **Axial / Telescopic Exploded (Bongkar Sumbu):** Untuk objek berporos mekanis (Mesin Motor/CVT, Lensa Kamera, Shockbreaker, Injektor).
3. **Hinged / Clamshell Disassembly (Buka Engsel):** Untuk benda bercangkang/tutup (Kunci Pengaman, Katup, Perangkat Elektronik).
4. **Selective X-Ray / Ghosting (Transparansi Selektif):** Untuk memperlihatkan aliran fluida/listrik di dalam pipa atau blok mesin yang sedang bekerja.

---

## 3. Katalog Kurva Graph Editor (Taxonomy of Motion Curves)

Gerakan kamera dan objek **tidak boleh hanya memakai satu kurva yang sama**. Setiap aksi fisik wajib memakai kurva Graph Editor yang sesuai dengan sifat bendanya:

| Jenis Aksi / Gerakan | Nama Kurva (Bezier / Physics) | Karakteristik Fisik & Alasan Penggunaan |
| :--- | :--- | :--- |
| **1. Buka Pengunci & Tutup Flip** | `Back / Spring Overshoot`<br/>`cubic-bezier(0.34, 1.56, 0.64, 1)` | Ada sedikit *anticipation* (tekan ke dalam), lalu melenting terbuka cepat dan memantul halus di engsel atas. |
| **2. Pembelahan Cangkang Baja Luar** | `Heavy Quintic Ease-In-Out`<br/>`cubic-bezier(0.83, 0, 0.17, 1)` | Memberi kesan bobot logam yang padat dan presisi; mulai perlahan, meluncur mantap, lalu mengerem halus. |
| **3. Kupasan Berjenjang Tiap Lapisan** | `Staggered Crit-Damped Spring`<br/>(Delay `4–6 frame` antar lapisan) | Lapisan tidak terbuka serentak (kacau), melainkan berurutan seperti gelombang domino (*overlapping action*). |
| **4. Pantulan Gelombang Radiasi** | `Linear Travel + Sharp Ricochet`<br/>(Sudut datang = Sudut pantul) | Gelombang panas melaju konstan dari air, lalu memantul tajam seketika saat menabrak lapisan cermin emas. |
| **5. Kamera Pindah Fokus Cepat** | `Whip / Expo Ease-In-Out`<br/>`cubic-bezier(0.87, 0, 0.13, 1)` | Memindahkan pandangan penonton dari dasar botol ke leher botol secara sigap dengan *Motion Blur* alami. |
| **6. Kamera Observasi (Saat Penjelasan)** | `Slow Orbital Drift / Float`<br/>(Kecepatan konstan mikro `2°–4°/detik`) | Menjaga agar gambar **tidak pernah mati/beku (zero dead-freeze)** meskipun komponen sedang tidak terbelah. |

---

## 4. Koreografi Kamera & Objek 16-Beat (Padat, Tanpa Diam Lama di Satu Scene)

Untuk mencegah video terasa diam atau membosankan, 55,97 detik dibagi menjadi **16 Beat Sinematik** (rata-rata **setiap 3,0 – 3,5 detik ada aksi kamera atau aksi komponen baru**) yang mengikat langsung ke 13 kalimat VO:

| Beat | Rentang Waktu (Frame @30fps) | Kalimat VO | Aksi Objek 3D (Multi-Layer Action) | Aksi Kamera 3D & Lensa (DoF) |
| :--- | :--- | :--- | :--- | :--- |
| **B-01** | `00.0s – 02.2s`<br/>(F: 0–66) | *"Udah berjam-jam, pas dituang..."* | Termos utuh Matte Ice Gray di atas meja hangat; uap tipis mulai naik saat tutup terbuka. | **Low-Angle Push-In:** Kamera meluncur masuk dari sudut $35^\circ$ menuju bodi atas. |
| **B-02** | `02.2s – 03.7s`<br/>(F: 66–111) | *"...masih panas."* | Inti dalam memancarkan pendar hangat samar dari balik mulut botol. | **Tilt-Up ke Mulut Botol:** Fokus lensa (DoF) mengunci bibir spout minuman. |
| **B-03** | `03.7s – 05.3s`<br/>(F: 111–160) | *"Kok bisa?"* | Tutup mengayun penuh di engsel (`Spring Overshoot`); termos terangkat sedikit dari meja (*anticipation*). | **Quick Orbit & Dolly-Out:** Kamera mengambil ancang-ancang mundur sedikit untuk ruang belah. |
| **B-04** | `05.3s – 07.6s`<br/>(F: 160–228) | *"Coba kita belah termosnya."* | **Aksi Kupas 1:** Cangkang luar Ice Gray terbelah dua bergeser ke kiri-kanan (`Quintic Ease`). | **Dynamic Dolly-In:** Kamera menembus masuk ke bidang belahan depan. |
| **B-05** | `07.6s – 11.2s`<br/>(F: 228–336) | *"Botol ini punya dua dinding, luar dan dalam."* | **Aksi Kupas 2:** Dinding luar dan tabung baja dalam bergeser bertingkat (*stepped offset*) agar keduanya kontras. | **Truck-Left & Pan:** Kamera menggeser ke sisi kiri memperlihatkan profil ketebalan kedua dinding. |
| **B-06** | `11.2s – 15.2s`<br/>(F: 336–456) | *"Di tengah-tengahnya ada celah hampa udara, alias vakum."* | Rongga vakum ~2mm di antara kedua dinding menyala biru dingin; partikel udara tersedot keluar hingga kosong. | **Macro Zoom-In (Lensa 85mm):** Kamera mendekat ekstrem ke celah ~2mm (latar belakang bokeh lembut). |
| **B-07** | `15.2s – 17.8s`<br/>(F: 456–534) | *"Karena nggak ada udara sama sekali..."* | Gelombang rambat panas dari dinding dalam mencoba menyeberang, namun terhenti di bibir ruang vakum. | **Slow Vertical Track:** Kamera menyusuri celah vakum dari bawah ke tengah botol. |
| **B-08** | `17.8s – 20.4s`<br/>(F: 534–612) | *"...panas dari air nggak punya media buat merambat keluar."* | Dinding luar tetap dingin (warna sejuk Ice Gray stabil) sementara dinding dalam hangat. | **Pull-Back Mild:** Kamera mundur sedikit memperlihatkan kontras suhu dinding dalam vs luar. |
| **B-09** | `20.4s – 24.2s`<br/>(F: 612–726) | *"Tapi ingat, panas masih bisa lolos lewat radiasi."* | **Aksi Kupas 3:** Tabung dalam membuka jendela *wedge* $90^\circ$, memperlihatkan pancaran gelombang inframerah dari air. | **Orbit 45° ke Sudut Isometrik:** Kamera berputar mengelilingi silinder untuk melihat kedalaman 3D. |
| **B-10** | `24.2s – 27.5s`<br/>(F: 726–825) | *"Makanya, dinding dalamnya dilapis bahan pemantul mirip cermin..."* | **Aksi Kupas 4:** Selubung foil tembaga/emas (*Copper Mirror*) mengelupas maju, menangkap kilau *Rim Light* tajam. | **Arc Shot Mengelilingi Lapisan Emas:** Pergerakan kamera memicu kilatan pantulan spekular di permukaan emas. |
| **B-11** | `27.5s – 30.5s`<br/>(F: 825–915) | *"...biar gelombang panasnya mantul balik."* | Partikel & gelombang inframerah menabrak permukaan cermin emas lalu memantul balik (*Sharp Ricochet*) ke inti air. | **Push-In ke Titik Pantul:** Kamera mengikuti arah pantulan gelombang kembali ke cairan. |
| **B-12** | `30.5s – 35.3s`<br/>(F: 915–1059) | *"Terus, tutup silikonnya dibuat kedap buat ngunci uap panas di mulut botol."* | **Aksi Kupas 5 (Axial Explode):** Unit tutup dan *Silicone Stopper* (dengan SSS kenyal) terurai vertikal lalu mengunci rapat mulut botol. | **Whip-Tilt ke Atas (Leher Botol):** Kamera meluncur naik dari perut botol ke leher & stopper 4,0 cm. |
| **B-13** | `35.3s – 38.9s`<br/>(F: 1059–1167) | *"Panas cuma bisa merembes tipis lewat sambungan lehernya."* | Aliran panas mikro terlihat merembes sangat tipis hanya di cincin sambungan leher baja. | **Close-Up Orbit Leher:** Kamera berputar pelan di sekitar cincin sambungan leher. |
| **B-14** | `38.9s – 43.2s`<br/>(F: 1167–1296) | *"Jadi air tetap mendingin, cuma butuh waktu jauh lebih lama."* | Seluruh lapisan kupasan merapat setengah jalan namun tetap memperlihatkan jendela penampang utuh. | **Crane-Down & Pull-Out:** Kamera turun kembali menampilkan proporsi penuh botol dari atas ke bawah. |
| **B-15** | `43.2s – 53.1s`<br/>(F: 1296–1593) | *"Di tes resminya, pas diisi air 95°C, setelah 6 jam suhunya masih di atas 71°C, padahal ruangan 20°C."* | **Sub-Beat A (43–46s):** Air panas $95^\circ\text{C}$ berkilau.<br/>**Sub-Beat B (46–50s):** Perisai vakum & emas menahan panas selama 6 jam.<br/>**Sub-Beat C (50–53s):** Kontras udara luar $20^\circ\text{C}$ vs inti $\ge 71^\circ\text{C}$ + Kartu Bukti Data. | **Slow Cinematic Orbit (2°/s):** Kamera tetap mengayun lembut (tidak beku) sambil memberi ruang tenang di bawah untuk Kartu Bukti Data. |
| **B-16** | `53.1s – 55.97s`<br/>(F: 1593–1679) | *"Itulah kenapa, meskipun..."* | Seluruh lapisan menutup rapat kembali (*Snap-Lock*) secara berurutan; tutup mengayun ke posisi awal. | **Match-Cut Loop Orbit:** Kamera kembali persis ke koordinat, sudut, dan fokus Frame 0 (`B-01`). |
