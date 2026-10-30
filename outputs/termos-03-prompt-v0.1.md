# Termos — prompt gambar uji tahap 3

Metode: built-in imagegen. Tujuan: papan pemeriksaan tampilan utuh dan penampang ilustratif, sebelum animasi. Sumber ini tidak membuktikan tersedianya model 3D atau ukuran internal produk.

## Rujukan dan peran

1. [Foto resmi model SM-WA48](https://www.zojirushi.co.jp/syohin/bottle/smwa/assets/img/product_size48.png): varian ice gray di kiri bawah menjadi acuan bentuk luar dan warna.
2. [Gambar tutup resmi](https://www.zojirushi.co.jp/syohin/bottle/smwa/assets/img/feature_pic01.png): acuan bentuk umum tutup dan lokasi seal.
3. [Diagram konstruksi dari artikel produsen](https://store.zojirushi.com/blogs/blog/design-explained-our-superior-vacuum-insulation): acuan susunan dinding, vakum, dan lapisan reflektif.
4. Frame CARA KERJA MOTOR MATIC pada 20,5 detik: acuan gaya ilustrasi teknis dan penandaan. Objek, angka, teks, dan identitas kanal tidak disalin.

## Prompt yang dikirim

```text
Use case: scientific-educational.
Create ONE high-quality landscape review board, approximately 1800x1200, with two equally important large views of the SAME vacuum-insulated bottle, for reviewing the visual style and anatomical clarity before animation.
Input image roles:
1. Official Zojirushi SM-WA48 product lineup: use ONLY the ice-gray bottle at the bottom left as the shape and color reference. Preserve its tall slim cylindrical body, gently tapered shoulder, low rounded hinged flip cap, oval front release button, small side lock, and bottom seam. Do not copy logos.
2. Official open lid image: reference for the cap assembly and broad seal location only; do not invent mechanical details.
3. Official conduction diagram: topology reference ONLY, not a design or text reference.
4. Official radiation diagram: reflective layer topology reference ONLY, not a design or text reference.
5. Frame of a scooter CVT educational explainer: STYLE reference ONLY. Match its restrained technical 3D illustration, clean solid gray forms, thin precise dark outlines, simple readable shading, light background, bold sans-serif typography, compact dark pill labels, and yellow attention accents. Do not reproduce any motorcycle, RPM gauge, subtitle sentence, channel badge, or branding.

Composition: A spacious near-white landscape board with a single shared heading at the top. Left panel about 42% width: full intact bottle, closed cap, slightly elevated three-quarter front view, centered with soft contact shadow. Right panel about 58% width: the same bottle with a clean longitudinal half-section removed, preserving its outside proportions and cap identity. Keep the cap seated and show only a simple schematic section of its seal. Show both objects at a matching scale. Make the interior easy to read, not photorealistic or cinematic.

Critical section anatomy:
The liquid occupies the central inner vessel and is pale warm amber. Two thin stainless steel walls surround it: an inner vessel wall, and a distinct outer shell wall. A visually empty narrow annular vacuum gap lies BETWEEN these two metal walls, on the sides AND below the inner vessel. The walls meet through a narrow neck connection at the mouth. The vacuum gap must not connect to the drinking cavity or open mouth.
Show a hairline reflective metallic layer on the OUTER surface of the inner vessel, facing the vacuum gap. It is a thin surface lining, NOT a solid filler occupying the gap. Use a restrained neutral metallic highlight for this lining; the precise foil material is unverified.
Enlarge the gap only enough to distinguish the layers visually. The drinking cavity must remain much wider than the gap. Do not add thick foam, a glass liner, an electric heater, an extra third vessel, invented springs, or exploded scattered pieces.
Use the exposed cut edges so the viewer can trace the sequence: liquid -> inner wall -> thin reflective surface -> empty vacuum gap -> outer wall. Maintain this sequence at both side and base. No glowing smoke or air bubbles inside the vacuum gap.

Labels: Put six compact legible dark pill labels with white text around the right view. Each thin leader line must end on the correct part:
"TUTUP RAPAT" points to the seated lid/seal.
"AIR PANAS" points to the liquid.
"DINDING DALAM" points exactly to the metal wall touching the liquid.
"CELAH VAKUM" points exactly to the empty gap between the walls; this pill alone uses yellow fill and dark text.
"LAPISAN REFLEKTIF" points exactly to the hairline exterior surface of the INNER wall facing the gap.
"DINDING LUAR" points to the outer shell.
Do not let leader lines or label boxes hide the critical cut edges. Anatomical correctness is more important than symmetry. No heat arrows or temperature graphs in this review image.

Text, verbatim, in Indonesian:
Main heading: "Kok termos bisa menahan panas?"
Panel headings: "01  UTUH" and "02  PENAMPANG".
Small bottom note: "Ilustrasi prinsip kerja. Celah dibesarkan; ukuran bagian dalam belum terverifikasi."
The main heading uses heavy black sans-serif, with "menahan panas?" in muted red, like the provided style frame. Generous whitespace, clear hierarchy, no additional text.
This is an original educational rendering guided by references, not a photo, CAD proof, or manufacturer's exact internal blueprint.
```

## Revisi 1 — gaya dan keterbacaan lapisan

Input utama: hasil prompt awal. Acuan tambahan: frame matic, diagram lapisan produsen, serta foto produk.

```text
Edit input image 1, the two-panel bottle review board. Input image 2 is the STYLE target only (technical CVT illustration). Input image 3 is the wall-layer topology reference only. Input image 4 is the official bottle shape reference; use the bottom-left ice-gray bottle.
Keep the two-panel comparison, SAME bottle silhouette and proportions, closed cap and front button identity, all six Indonesian labels, exact heading and exact bottom note. Preserve the current whitespace and clear hierarchy.

Make one focused revision for clearer technical illustration:
Render both bottles in the flat technical 3D illustration language of input image 2: clean solid gray and ice-gray shapes, restrained polygonal surfaces, fine dark contours, simple diffuse shadows, almost no metallic gloss, no photo texture, no brushed grain or studio-product reflections. The liquid remains flat pale amber, not glowing.

Rebuild the cutaway edge so there are exactly TWO structural metal walls, not a stack of extra nested vessels. The radial order is: liquid -> inner metal wall -> hairline reflective surface on the outside of that inner wall -> visibly EMPTY pale gap -> outer metal wall. This gap continues below the inner vessel as well. Inner and outer walls meet only at the narrow mouth/neck connection. It must not open into the drinking cavity.
Use a very thin muted yellow accent stripe for the reflective surface as an explanatory highlight, not a claim about its material. Use a plain white or extremely pale blue EMPTY vacuum gap with crisp outlines so the two targets are clearly distinct.
The "DINDING DALAM" leader ends on the inner metal wall that directly touches the liquid.
The "LAPISAN REFLEKTIF" leader ends on the thin yellow surface stripe on that wall's outer face.
The "CELAH VAKUM" leader ends in the visibly empty gap, spatially separate from that stripe.
The "DINDING LUAR" leader ends on the outer shell.
The "AIR PANAS" leader ends in the liquid and "TUTUP RAPAT" on the cap seal.
Use small dark target dots and avoid overlapping leaders. Keep the vacuum tag yellow, other tags dark gray.
Simplify the cap interior to a seated insulating closure and visible seal. Remove unsupported intricate internal actuator details. Do not invent valves, extra springs, or dimensions.
All original text must remain spelled correctly, including the note that the gap is enlarged and inner dimensions are unverified. No added text, no logos, no temperatures or heat-flow arrows.
```

## Revisi 2 — sasaran label

Input: hasil revisi pertama. Koordinat piksel di bawah khusus untuk gambar uji ini; jangan mengubahnya menjadi aturan universal untuk objek lain.

```text
Make a precise anatomical-label correction to the supplied board. Preserve the entire LEFT intact bottle, heading, panel names, all text, background, style, outside silhouette of the RIGHT bottle, and cap. Change ONLY the inner cutaway layers and the ends of the four wall/gap leader lines.

The current wall layers are too narrow, so the inner-wall and reflective-layer pointers land on the wrong stripes. Make the exposed schematic layers deliberately wider to separate targets. The existing bottom note already states that inner dimensions are unverified and the gap enlarged.

At the straight RIGHT side of the cutaway, the exact order from inside to outside must be:
1. AMBER LIQUID.
2. INNER METAL WALL: a visibly distinct medium-gray strip about 12 pixels wide.
3. REFLECTIVE SURFACE: a SINGLE narrow muted-yellow strip about 5 pixels wide, touching the OUTSIDE face of the inner wall.
4. VACUUM GAP: a visibly empty WHITE strip about 22 pixels wide.
5. OUTER METAL WALL: a pale blue-gray strip about 14 pixels wide.
Then the outside of the bottle. Exactly two structural walls. The yellow stripe is not in the middle of the gap, and there is no second yellow stripe on the outer wall.
Carry this SAME order smoothly around the curved bottom. The vacuum gap remains sealed from the liquid cavity and the two walls join at the narrow neck.

Specific leader-dot placements for the 1536x1024 image:
"DINDING DALAM" dot goes in the CENTER of the medium-gray INNER wall, about x=1071 at y=520.
"LAPISAN REFLEKTIF" dot goes EXACTLY on the SINGLE yellow stripe, about x=1080 at y=627.
"CELAH VAKUM" dot goes in the CENTER of the empty WHITE gap, about x=1095 at y=709.
"DINDING LUAR" dot goes in the CENTER of the pale blue-gray OUTER wall, about x=1115 at y=807.
Coordinates are approximate guides; the logical layer identity takes precedence if the final rendering shifts a few pixels. Use small endpoint dots so they do not cover the entire stripe, with an extremely thin contrasting outline. The four targets must clearly be on DIFFERENT layers.
Keep the already-correct AIR PANAS and TUTUP RAPAT leaders. No other changes or added elements.
```

## Hasil yang dipilih

[Visual bedah termos](termos-03-bedah-v0.1.png). Tiga panggilan built-in imagegen dilakukan: satu generasi awal dan dua revisi. Hasil terakhir dipakai setelah pemeriksaan visual label pada pembesaran. [Catatan ketelitian dan review](termos-03-catatan-v0.1.md).


